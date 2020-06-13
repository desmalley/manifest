import pandas as pd
import my_ebay_lib as ebay
import datetime

#read manifest
man_df= pd.read_csv('manifests/b3.csv')
#man_df=df.fillna(" ") #replace NA fields with empty fields

#read cache
cache_df=pd.read_csv('ebay_cache.csv')

#find pallet cost
pallet_cost=sum(ebay.str_to_float_price(man_df["Ave. Price per Unit"]))
print("pallet_cost = ${}".format(pallet_cost))

#find total if all items sold on ebay today
pnames=man_df["Product Name"]
ebay_sale_total=0
old_name=""
old_price=0

this_session_df=pd.DataFrame({'NAME':['New Price Entry Spacer'], 'PRICE':[0.0], 'DATE':datetime.datetime.now(),'URL':['www.google.com']})
for name in pnames:
    print("PRODUCT NAME: {}".format(name))
    if name==old_name: #Did we just looked up this price?
        print("(Repeat Price)")
        price=old_price
    elif cache_df['NAME'].str.contains(name,regex=False).any():#Is this price in the cache?
        print("(Cached Price)")
        row=cache_df[cache_df.NAME==name]
        price=row.PRICE.values[0]
    else: #If not, let's look up the price on ebay
        print("Fetch Ebay Price")
        price,url=ebay.fetch_ebay_price(name)
        this_session_df=this_session_df.append({'NAME':name, 'PRICE':price, 'DATE':datetime.datetime.now(),'URL':url}, ignore_index=True)
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
print(cache_df)
#add new prices to cache
cache_df=cache_df.append(this_session_df, ignore_index=True)
cache_df.to_csv('ebay_cache.csv',index=False)




