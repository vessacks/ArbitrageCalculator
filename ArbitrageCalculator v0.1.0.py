import pandas as pd
import pandas

df = pd.read_csv("C:/Users/username/Documents/Personal/Projects/Visual Studio Code 4.12.22/Arbitrage bot/DataTableExample4.csv")

#print(df.to_string)

##testing what iloc prints
#Macrondays = df.iloc[0]
#print(Macrondays)


NumberofContracts = len(df.iloc[:,0])
IndexUnit = range(NumberofContracts)
ContractIndex = []
for x in IndexUnit:
    ContractIndex.append(x)
print("The ContractIndex is " +str(ContractIndex))
# column 0 = BinaryEvent
# Column 1 = DaysToExpiry
# Column 2 = PredictitAsk
# Column 3 = PredictitBid
# Column 4 = SmarketsAsk
# Column 5 = SmarketsBid 


for x in ContractIndex:
    ProfitBuyPredictIt = df.iloc[x,5] - df.iloc[x,2]
    ProfitBuySmarkets = df.iloc[x,3] - df.iloc[x,4]
    ContractinQuestion = df.iloc[x,0]
    if ProfitBuyPredictIt > ProfitBuySmarkets and ProfitBuyPredictIt > 0:
        print(str(ContractinQuestion)+ "--Buy Predictit, sell Smarkets for profit "+ str(ProfitBuyPredictIt))
    elif ProfitBuySmarkets > ProfitBuyPredictIt and ProfitBuySmarkets > 0:
        print(str(ContractinQuestion)+"-- Buy Smarkets, sell Predictit for profit "+ str(ProfitBuySmarkets))
    else:
        print(str(ContractinQuestion) + " sucks")
    