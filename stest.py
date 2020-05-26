from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser= webdriver.Chrome(executable_path="C:/Users/smalley/Desktop/PYTHON/Panda/chromedriver.exe")
browser.get('https://www.ebay.com/')
searchbar=browser.find_element_by_id("gh-ac")
searchbar.send_keys("weird al yancovich")
searchbar.send_keys(Keys.ENTER)

