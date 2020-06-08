
'''
This code looks prices for lots of one item from liquidation.com
'''
import pandas as pd
import my_ebay_lib as ebay
import datetime


single=input("Is there more than one type of item in the lot?")
if single.lower() =='y' or single.lower=='yes':
    bid=float(input("What is the current bid?:  "))
    name=input("input product name:  ")
    qty=float(input("input product quantity:  "))

    cost=bid
    price,url=ebay.fetch_ebay_price(name)
    gross=price*qty
    profit=gross-cost
else:
    pnames=[]
    bid=float(input("What is the current bid?:  "))
    man_txt_name=input('manifest file name including suffix (.txt or .csv): ' )


    f = open("manifests\\"+man_txt_name+".txt", "r")
    manifest=f.read()
    f.close()
    lines=manifest.split("\n")[2:-1] #don't leading empty space and column titles
    try:
        lines.remove('')#get rid of empty lines
    except:
        #nothing
        pass
    for line in lines:
        elems=line.split("$")
        print(elems)
        name=elems[0][:-1]
        
        print(name)#strip trailing qty (usually 1)
        pnames.append(name)



    df,gross=ebay.find_prices(pnames)
    ebay.update_cache(df)
    profit=gross-bid

print("cost is {}".format(bid))
print("gross is {}".format(gross))
print("profit is {}".format(profit))



