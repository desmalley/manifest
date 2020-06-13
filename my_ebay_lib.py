from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import datetime

#fetches just first ebay price
def fetch_ebay_price(product_name):
    browser= webdriver.Chrome(executable_path="C:/Users/smalley/Desktop/PYTHON/Panda/chromedriver.exe")
    browser.get('https://www.ebay.com/')
    searchbar=browser.find_element_by_id("gh-ac")
    searchbar.send_keys(product_name)
    searchbar.send_keys(Keys.ENTER)
    url=browser.current_url
    try:
        price=browser.find_element_by_class_name("s-item__price")
        tprice=price.text
        print("EBAY PRICE IS:{}".format(tprice))
        first_tprice_elem=tprice.split(" ")[0]
        
        try:
            first_first_tprice_elem=first_tprice_elem.replace(",","")#if the price is more than one thousand replace commas 
            digits_only=first_tprice_elem.split('$')[1]
            fprice=float(digits_only)
           
        except: #not a valid price example, Best Buy click to see price
            print("not a valid price")
            fprice=0
    except:  #for example selenium.common.exceptions.NoSuchElementException:  thrown when 'no exact matches found'
        fprice=0
    #print(fprices)    
    browser.quit()
    try:
        return fprice,url
    except:
        return float(0),url  #this neads to return a float to be the same as the other case



def find_prices(pnames):
    ebay_sale_total=0
    old_name=""
    old_price=0
    cache_df=pd.read_csv('ebay_cache.csv')
    this_session_df=pd.DataFrame({'NAME':['New Price Entry Spacer'], 'PRICE':[0.0], 'DATE':datetime.datetime.now(),'URL':['www.google.com']})
    
    for name in pnames:
        print("PRODUCT NAME: {}".format(name))
        if name:
            if name==old_name: #Did we just looked up this price?
                print("(Repeat Price)")
                price=old_price
            elif cache_df['NAME'].str.contains(name,regex=False).any():#Is this price in the cache?
                print("(Cached Price)")
                row=cache_df[cache_df.NAME==name]
                price=row.PRICE.values[0]
            else: #If not, let's look up the price on ebay
                print("Fetch Ebay Price")
                price,url=fetch_ebay_price(name)
                this_session_df=this_session_df.append({'NAME':name, 'PRICE':price, 'DATE':datetime.datetime.now(),'URL':url}, ignore_index=True)
        else:
            print('no name')
            price=0
        print("PRICE: {}".format(price))
        ebay_sale_total+=price
        old_name=name
        old_price=price
    return this_session_df, ebay_sale_total



def update_cache(new_df):
    cache_df=pd.read_csv('ebay_cache.csv')
    cache_df=cache_df.append(new_df, ignore_index=True)
    cache_df.to_csv('ebay_cache.csv',index=False)



def str_to_float_price(str_prices):
    float_prices=[]
    for str_price in str_prices:
        str_price=str_price.replace(",","") #in case price has a comma
        float_price=float(str_price.strip('$'))
        float_prices.append(float_price)
    return float_prices
#may need to add 



#***************************************************************************************
#***********************OLD DEPRICATED FUNCTIONS****************************************
#***************************************************************************************
#Fetches all ebay prices

def fetch_ebay_prices(product_name):
    browser= webdriver.Chrome(executable_path="C:/Users/smalley/Desktop/PYTHON/Panda/chromedriver.exe")
    browser.get('https://www.ebay.com/')
    searchbar=browser.find_element_by_id("gh-ac")
    searchbar.send_keys(product_name)
    searchbar.send_keys(Keys.ENTER)
    url=browser.current_url
    

    prices=browser.find_elements_by_class_name("s-item__price")
    #print("EBAY PRICE IS:")
    fprices=[]
    for price in prices:
        tprice=price.text
        first_tprice_elem=tprice.split(" ")[0]
        try:
            digits_only=first_tprice_elem.split('$')[1]
            fprices.append(float(digits_only))
        except: #not a valid price
            print("not a valid price")
            fprices=[0]
        
    #print(fprices)    
    browser.quit()
    try:
        return fprices[0],url
    except:
        return float(0),url  #this neads to return a float to be the same as the other case
