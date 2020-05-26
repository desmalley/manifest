import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
driver = webdriver.Chrome('./chromedriver')
driver.get("https://my.byu.edu/")
time.sleep(1)
print(driver.title)
time.sleep(10)
print("Signing In...")
driver.find_element_by_id("portalCASLoginLink").click()
time.sleep(10)
print("Signing In...some more")
driver.find_element_by_id("username").send_keys("des32")
driver.find_element_by_id("password").send_keys("Urop925fest00n")
driver.find_element_by_name("submit").click()