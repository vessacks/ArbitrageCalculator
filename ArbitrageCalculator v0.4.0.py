from cmath import nan
from numpy import NaN
import pandas as pd
import pandas
import numpy
import csv
import requests
import json

#Pulls Predictit Data and expresses in json
PredictitURL = "https://www.predictit.org/api/marketdata/all/"
PredictitResponse = requests.get(PredictitURL)
PredictitDataJSON = PredictitResponse.json()


#Creates list of lists with PredictitData
PredictitDataList = []
for x in PredictitDataJSON['markets']:
        for y in x['contracts']:
            PredictitDataList.append([x['name'], x['shortName'], y['dateEnd'], y['name'], y['shortName'], y['status'], y['bestBuyYesCost'], y['bestBuyNoCost'], y['bestSellYesCost'], y['bestSellNoCost'] ])

#Creates DataFrame of PredictDataList
PredictitDataframe = pd.DataFrame(data=PredictitDataList, columns=("EventName","EventShortName", "DateEnd", "ContractName", "ContractShortName", "Open?", "YesAsk", "NoAsk", "YesBid", "NoBid" ))
PredictitDataframe.to_csv("C:\\Users\\username\\Documents\\Personal\\Projects\\Visual Studio Code 4.12.22\\Arbitrage bot\\PredictitDataframe.csv")




#reads input csv of matched market data. As of 4.19.22 you don't have a csv of matched market data. You may also need to clean it
CombinedDataframe = pd.read_csv("C:/Users/username/Documents/Personal/Projects/Visual Studio Code 4.12.22/Arbitrage bot/DataTableExample v0.4.0.csv", header=0)

#df.shape[0] is the 0th element of the tuple df.shape, which returns the x and y dimensions of df
print("The number of contracts is " +str(CombinedDataframe.shape[0]))

# column 0 = BinaryEvent
# Column 1 = DaysToExpiry
# Column 2 = PredictitAskYes
# Column 3 = PredictitBidYes
# Column 4 = SmarketsAskYes
# Column 5 = SmarketsBidYes
# Column 6 = PredictitAskNo
# Column 7 = PredictitBidNo
# Column 8 = SmarketsAskNo
# Column 9 = SmarketsBidNo

#this makes a list of lists containing each contact and its data. If there is no profitable trade, it returns a Nan to ProfitLessFees and a none to BuyPredictit
Contracts = []
Index = []
for x in range(CombinedDataframe.shape[0]):
    ProfitYesPredictit = 1 - CombinedDataframe.iloc[x,2] - CombinedDataframe.iloc[x,8]    #1 - PredictitAskYes - SmarketsAskNo (Fees not included)
    ProfitNoPredictit = 1 - CombinedDataframe.iloc[x,6] - CombinedDataframe.iloc[x,4]     #1 - PredictitAskNo - SmarketsAskYes (Fees not included)
    ContractinQuestion = CombinedDataframe.iloc[x,0]                       #name of contract
    Index.append(ContractinQuestion)                        #adds name of contract to index
    ProfitLessFee = numpy.float64                           #defines profit less fee (used later)
    ContractRow = [CombinedDataframe.iloc[x,0],CombinedDataframe.iloc[x,1],CombinedDataframe.iloc[x,2],CombinedDataframe.iloc[x,3],CombinedDataframe.iloc[x,4],CombinedDataframe.iloc[x,5],CombinedDataframe.iloc[x,6],CombinedDataframe.iloc[x,7],CombinedDataframe.iloc[x,8],CombinedDataframe.iloc[x,9]] #list of contract data
    
    #adds profit and trade pair (ie buy yes in Predictit or not) data in position 10 and 11 of contract row
    if type(ProfitYesPredictit) == numpy.float64 and type(ProfitNoPredictit) == numpy.float64: 
        if ProfitYesPredictit > ProfitNoPredictit:
            ProfitLessFee = ProfitYesPredictit
            ContractRow.append(ProfitYesPredictit)
            ContractRow.append(True)
        else: 
            ProfitLessFee = ProfitNoPredictit
            ContractRow.append(ProfitNoPredictit)
            ContractRow.append(False)
    elif type(ProfitYesPredictit) == numpy.float64:
        ProfitLessFee = ProfitYesPredictit
        ContractRow.append(ProfitYesPredictit)
        ContractRow.append(True)
    elif type(ProfitNoPredictit) == numpy.float64:
        ProfitLessFee = ProfitNoPredictit
        ContractRow.append(ProfitNoPredictit)  
        ContractRow.append(False)
    else:
        ProfitLessFee = float("NaN")
        ContractRow.append(float("NaN"))
        ContractRow.append(None)

    #adds probability of outcome yes in position 12 of contract row. 
    pYes = (CombinedDataframe.iloc[x,2] + CombinedDataframe.iloc[x,3] + CombinedDataframe.iloc[x,4] + CombinedDataframe.iloc[x,5] + (1-CombinedDataframe.iloc[x,6]) + (1-CombinedDataframe.iloc[x,7]) + (1-CombinedDataframe.iloc[x,8]) + (1-CombinedDataframe.iloc[x,9]))//8 #pYes is the average of of the yes bids and asks on both markets and the inverse of the no bids and asks 
    ContractRow.append(pYes)
    
    #defines probability of winning in Predictit and Smarkets
    if ContractRow[11] == True:
        PwinP = pYes
        PwinS = 1 - pYes
        PContractCost = CombinedDataframe.iloc[x,2] #the predictit yes ask
        SContractCost = CombinedDataframe.iloc[x,8] #the smarkets no ask
    if ContractRow[11] == False:
        PwinP = 1 - pYes 
        PwinS = pYes
        PContractCost = CombinedDataframe.iloc[x,6] #the predictit no ask
        SContractCost = CombinedDataframe.iloc[x,4] #the smarkets yes ask 
    if ContractRow[11] == None:
        PwinP = float("NaN")
        PwinS = float("NaN")

    # defines expected fee E[Fee] = p(predictitwin)*(1-predictit contract cost)*.1 + p(smarketswin)*(1-smarkets contract cost)*.02
    eFee = PwinP*(1-PContractCost)*.1 + PwinS*(1-SContractCost)*.02
    ContractRow.append(eFee) # appends expected fee to ContractRow position 13

    #defines loss potential (ie worst case fee scenario) and appends to ContractRow position 14
    WorstCaseProfit = ProfitLessFee - ((1-PContractCost)*.1)
    ContractRow.append(WorstCaseProfit)

    #defines the expected profit outcome and appends to ContractRow position 15
    eProfit = ProfitLessFee - eFee
    ContractRow.append(eProfit)

    # appends complete contract row to list of contracts
    Contracts.append(ContractRow)

output = pd.DataFrame(data=Contracts, columns=("BinaryEvent","DaysToExpiry","PredictitAskYes","PredictitBidYes","SmarketsAskYes","SmarketsBidYes","PredictitAskNo","PredictitBidNo","SmarketsAskNo","SmarketsBidNo","ProfitLessFees","YesPredictit?","pYes", "eFee", "WorstCaseProfit", "eProfit") )
print(output.to_string)

output.to_csv("C:\\Users\\username\\Documents\\Personal\\Projects\\Visual Studio Code 4.12.22\\Arbitrage bot\\outputexample v0.4.0.csv")
