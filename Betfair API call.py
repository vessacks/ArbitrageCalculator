#Request A List Of Available Event Types (listEventTypes)
#Request a List of Events for an Event Type (listEvents)
#Request the Market Information for an Event (listMarketCatalogue)
#Horse Racing - Today's Win & Place Markets
#Request a List of Football Competitions (listCompetitions)
#Request Market Prices (listMarketBook)
#Placing a Bet (placeOrders)
#Placing a Betfair SP Bet - MARKET_ON_CLOSE (placeOrders)
#Placing a Betfair SP Bet - LIMIT_ON_CLOSE (placeOrders)
#Retrieving Details of Bet/s Placed on a Market/s (listCurrentOrders)
#Retrieving the Result of a Settled (listMarketBook)
#Retrieving Details of Bets on a Settled Market - including P&L & Commission paid (listClearedOrders)
  
#This stolen code uses JSON-RPC, not JSON REST. I don't know what that means. 
import requests
import json
 
url="https://api.betfair.com/exchange/betting/json-rpc/v1"
header = { 'X-Application' : 'WAo2COnXamSBoBx6', 'X-Authentication' : 'lOt2bs4Itd+UUjyDeBlIAVBHmOoRbUaw54O8rW/knAQ=' ,'content-type' : 'application/json' }
 #your identifying details go in these fields


jsonrpc_req=[
    {
        "jsonrpc": "2.0",
        "method": "SportsAPING/v1.0/listEventTypes",
        "params": {
            "filter": {
                "eventTypeIds": [
                    "2378961"
                ]
            },
            "maxResults": "2",
            
        },
        "id": 1
    }
]

 #See https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Getting+Started 
#"id": 1 seems to be in all example code. Just leave it I guess

response = requests.post(url, data=jsonrpc_req, headers=header)

print(json.dumps(json.loads(response.text), indent=3))