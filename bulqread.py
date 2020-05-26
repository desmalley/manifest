import pandas as pd
import my_ebay_lib as ebay
import datetime


def str_to_float_price(str_prices):
    float_prices=[]
    for str_price in str_prices:
        float_price=float(str_price.strip('$'))
        float_prices.append(float_price)
    return float_prices


df= pd.read_csv('gen2.csv')
old_cache_df=pd.read_csv('ebay_cache.csv')
dfnew=df.fillna(" ") #replace NA fields with empty fields

#find pallet cost
pallet_cost=sum(str_to_float_price(df["Ave. Price per Unit"]))
print("pallet_cost = ${}".format(pallet_cost))

#find total if all items sold on ebay today
pnames=df["Product Name"]
ebay_sale_total=0
old_name=""
old_price=0

ebay_cache_df=pd.DataFrame({'NAME':['New Price Entry Spacer'], 'PRICE':[0.0], 'DATE':datetime.datetime.now(),'URL':['www.google.com']})
for name in pnames:
    print("PRODUCT NAME: {}".format(name))
    if name==old_name:
        print("(Repeat Price)")
        price=old_price
    elif old_cache_df['NAME'].str.contains(name).any():
        print("(Cached Price)")
        row=old_cache_df[old_cache_df.NAME==name]
        price=row.PRICE.values[0]
    else:
        print("Fetch Ebay Price")
        price,url=ebay.fetch_ebay_price(name)
        ebay_cache_df=ebay_cache_df.append({'NAME':name, 'PRICE':price, 'DATE':datetime.datetime.now(),'URL':url}, ignore_index=True)
    print("PRICE: {}".format(price))
    ebay_sale_total+=price
    old_name=name
    old_price=price

    
#calculate potential profit    
profit=ebay_sale_total-pallet_cost
print("profit:")
print(profit)
if profit>100:
    print("this is a good deal!")
else:
    print("this is a bad deal")
print(old_cache_df)
#add new prices to cache
old_chace_df=old_cache_df.append(ebay_cache_df, ignore_index=True)
old_chace_df.to_csv('ebay_cache.csv',index=False)




