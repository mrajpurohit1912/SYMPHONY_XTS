from prac_connect import Symphony


xts = Symphony()

market_res = xts.market_login('8a9387319828d236c91364','Ugjc752$WZ')
#print(market_res)

inter_res = xts.interactive_login('a3588f2d63becf7d67a954','Lyou415#kU')
#print(inter_res)

# #print(xtss.dealer_order_book(clientid="TEST"))
# response = xts.place_order(    exchangeSegment="NSECM",
#     exchangeInstrumentID=25,
#     productType="MIS",
#     orderType="MARKET",
#     orderSide="BUY",
#     timeInForce="DAY",
#     disclosedQuantity=0,
#     orderQuantity=5,
#     limitPrice=0,
#     stopPrice=0,
#     orderUniqueIdentifier="454845",
#     clientid="TEST")

# if response['type'] != 'error':
#     OrderID = response['result']['AppOrderID']


# print(xts.order_history(appOrderID=OrderID))

print(xts.dealer_positions(dayOrNet="DayWise",clientid="TEST"))