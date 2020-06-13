from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import datetime



#fetches just first ebay price
def fetch_ebay_price(product_name):
    '''
    in: string product name
    out: tuple float, string  price,url
    '''
    if not isinstance(product_name,str):
        print('Your input is not a string name, instead you input {}'.format(product_name))
        return 0,'no url'
    elif not product_name:
        print('Your entered an empty string as a product name, Silly!')
        return 0,'no url'
    else: #normal operation
        browser= webdriver.Chrome(executable_path="C:/Users/smalley/Desktop/PYTHON/Panda/chromedriver.exe")
        browser.get('https://www.ebay.com/')
        searchbar=browser.find_element_by_id("gh-ac")
        searchbar.send_keys(product_name)
        searchbar.send_keys(Keys.ENTER)
        url=browser.current_url

        try:
            price=browser.find_element_by_class_name("s-item__price")
            tprice=price.text
            print("EBAY PRICE for {} IS:{}".format(product_name,tprice))
            first_tprice_elem=tprice.split(" ")[0]
            try:
                dig_punc_only=first_tprice_elem.replace('$','')
                dig_only=dig_punc_only.replace(',','')
                fprice=float(dig_only)
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
            return float(0),url 


def update_cache(new_df):
    cache_df=pd.read_csv('ebay_cache_lower.csv')
    cache_df=cache_df.append(new_df, ignore_index=True)
    cache_df.to_csv('ebay_cache_lower.csv',index=False)


def find_prices(name_qty_df):
    '''
    in: data frame with two columns: 'name' and 'qty'
    out: data frame with cols: 'name' 'qty' 'price' 'url' 'date'
    '''
    name_qty_dict=dict(zip(name_qty_df.name.to_list(),name_qty_df.qty.to_list()))
    name_list=name_qty_df["name"].to_list()
    old_name=""
    old_price=0
    old_url=''
    cache_df=pd.read_csv('ebay_cache_lower.csv')
    master_df=pd.DataFrame({'name':[None],'qty':[None],'price':[None],'date':[None],'url':[None]})
    for name,qty in name_qty_dict.items():
        print("PRODUCT NAME: {}".format(name))
        if name:
            if name==old_name: #Did we just looked up this price?
                print("(Repeat Price)")
                price=old_price
                url=old_url
            elif cache_df['name'].str.contains(name,regex=False).any():#Is this price in the cache?
                print("(Cached Price)")
                row=cache_df[cache_df.name==name]
                price=row.price.values[0]
                url=row.url.values[0]
            else: #If not, let's look up the price on ebay
                print("Fetch Ebay Price")
                price,url=fetch_ebay_price(name)
                cache_entry_df=pd.DataFrame({'name':[name],'price':[price],'date':[datetime.datetime.now()],'url':[url]})
                update_cache(cache_entry_df)
            session_df=pd.DataFrame({'name':[name], 'qty':[qty],'price':[price], 'date':[datetime.datetime.now()],'url':[url]})    
            master_df=master_df.append(session_df, ignore_index=True)
        else:
            print('no name')
            price=0
        old_name=name
        old_url=url
        old_price=price
        master_df=master_df.fillna('')
    return master_df