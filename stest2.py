from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser= webdriver.Chrome(executable_path="C:/Users/smalley/Desktop/PYTHON/Panda/chromedriver.exe")
browser.get('https://www.ebay.com/')
searchbar=browser.find_element_by_id("gh-ac")
searchbar.send_keys("Griffin GB36152-3 Survivor Skin iPod Touch 5th Generation - Blue")
searchbar.send_keys(Keys.ENTER)
prices=browser.find_elements_by_class_name("s-item__price")
print("PRICE IS:")
fprices=[]
for price in prices:
    tprice=price
    print(tprice.text)
    first_tprice_elem=tprice.text.split(" ")[0]
    digits_only=first_tprice_elem.split('$')[1]
    
    fprices.append(float(digits_only))

print(fprices)    
browser.quit()   