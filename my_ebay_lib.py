from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#"Griffin GB36152-3 Survivor Skin iPod Touch 5th Generation - Blue"


#fetches just first ebay price
def fetch_ebay_price(product_name):
    browser= webdriver.Chrome(executable_path="C:/Users/smalley/Desktop/PYTHON/Panda/chromedriver.exe")
    browser.get('https://www.ebay.com/')
    searchbar=browser.find_element_by_id("gh-ac")
    searchbar.send_keys(product_name)
    searchbar.send_keys(Keys.ENTER)
    url=browser.current_url
    price=browser.find_element_by_class_name("s-item__price")
    tprice=price.text
    print("EBAY PRICE IS:{}".format(tprice))
    first_tprice_elem=tprice.split(" ")[0]
    
    try:
        digits_only=first_tprice_elem.split('$')[1]
        fprice=float(digits_only)
       
    except: #not a valid price
        print("not a valid price")
        fprice=0
       
    #print(fprices)    
    browser.quit()
    try:
        return fprice,url
    except:
        return float(0),url  #this neads to return a float to be the same as the other case











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
