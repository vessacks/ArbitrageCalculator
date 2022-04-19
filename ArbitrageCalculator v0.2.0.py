from cmath import nan
from numpy import NaN
import pandas as pd
import pandas
import numpy


#reads input csv of cleaned and matched market data
df = pd.read_csv("C:/Users/username/Documents/Personal/Projects/Visual Studio Code 4.12.22/Arbitrage bot/DataTableExample5.csv", header=0)

#df.shape[0] is the 0th element of the tuple df.shape, which returns the x and y dimensions of df
print("The number of contracts is " +str(df.shape[0]))

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
for x in range(df.shape[0]):
    ProfitYesPredictit = 1 - df.iloc[x,2] - df.iloc[x,8]    #1 - PredictitAskYes - SmarketsAskNo (Fees not included)
    ProfitNoPredictit = 1 - df.iloc[x,6] - df.iloc[x,4]     #1 - PredictitAskNo - SmarketsAskYes (Fees not included)
    ContractinQuestion = df.iloc[x,0]                       #name of contract
    Index.append(ContractinQuestion)                        #adds name of contract to index
    ProfitLessFee = numpy.float64                           #defines profit less fee (used later)
    ContractRow = [df.iloc[x,0],df.iloc[x,1],df.iloc[x,2],df.iloc[x,3],df.iloc[x,4],df.iloc[x,5],df.iloc[x,6],df.iloc[x,7],df.iloc[x,8],df.iloc[x,9]] #list of contract data
    
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
    pYes = (df.iloc[x,2] + df.iloc[x,3] + df.iloc[x,4] + df.iloc[x,5] + (1-df.iloc[x,6]) + (1-df.iloc[x,7]) + (1-df.iloc[x,8]) + (1-df.iloc[x,9]))//8 #pYes is the average of of the yes bids and asks on both markets and the inverse of the no bids and asks 
    ContractRow.append(pYes)
    
    #defines probability of winning in Predictit and Smarkets
    if ContractRow[11] == True:
        PwinP = pYes
        PwinS = 1 - pYes
        PContractCost = df.iloc[x,2] #the predictit yes ask
        SContractCost = df.iloc[x,8] #the smarkets no ask
    if ContractRow[11] == False:
        PwinP = 1 - pYes 
        PwinS = pYes
        PContractCost = df.iloc[x,6] #the predictit no ask
        SContractCost = df.iloc[x,4] #the smarkets yes ask 
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

output.to_csv("C:\\Users\\username\\Documents\\Personal\\Projects\\Visual Studio Code 4.12.22\\Arbitrage bot\\outputexample1.csv")
