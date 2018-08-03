from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import getpass
import os
import base64

print 'enter user id'
id=raw_input()
if len(id)==0:
  id='sukanthk'

email=id+'@microland.com'

password=getpass.getpass()
#if len(password)==0:
#    password=base64.b64decode("")

print 'working...'

driver = webdriver.Firefox()
#driver.set_window_position(-2000, 0)
driver.get('https://microland.greythr.com/v2/attendance/info/attendanceinfo')
timeout = 20

try:
    logo_present = EC.presence_of_element_located((By.ID, 'userNameInput'))
    WebDriverWait(driver, timeout).until(logo_present)
except TimeoutException:
    print "Timed out waiting for page to load"

userNameInput = driver.find_element_by_xpath('//input[@id="userNameInput"]')
userNameInput.send_keys(email)
passwordInput = driver.find_element_by_xpath('//input[@id="passwordInput"]')
passwordInput.send_keys(password)
submitButton=driver.find_element_by_xpath('//span[@id="submitButton"]')
submitButton.click()

try:
    logo_present = EC.presence_of_element_located((By.NAME, 'fromdate'))
    WebDriverWait(driver, timeout).until(logo_present)
except TimeoutException:
    print "Timed out waiting for page to load"

import datetime
from dateutil.relativedelta import relativedelta

now = datetime.datetime.now()
if now.day>=16: fromdate=str(now.strftime('16 %b %Y')); now=now+relativedelta(months=+1); todate= str(now.strftime('15 %b %Y'))
else:  todate= str(now.strftime('15 %b %Y')); now=now+relativedelta(months=-1);  fromdate=str(now.strftime('16 %b %Y'))

fromdate1 = driver.find_element_by_xpath('//input[@name="fromdate"]')
fromdate1.clear()
fromdate1.send_keys(fromdate)
todate1 = driver.find_element_by_xpath('//input[@name="todate"]')
todate1.clear()
todate1.send_keys(todate)
show=driver.find_element_by_xpath('//span[@class="btn btn-primary customSearch"]')
show.click()

import time
time.sleep(3)

try:
    total=map(int,list(str(driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[4]/div[4]/div/div/div[2]/div/table[1]/tbody/tr[32]/td[2]').text).split(':')))
except:
    try:
        total=map(int,list(str(driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[4]/div[4]/div/div/div[2]/div/table[1]/tbody/tr[31]/td[2]').text).split(':')))
    except:
        try:
            total=map(int,list(str(driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[4]/div[4]/div/div/div[2]/div/table[1]/tbody/tr[30]/td[2]').text).split(':')))
        except:
            total=map(int,list(str(driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[4]/div[4]/div/div/div[2]/div/table[1]/tbody/tr[29]/td[2]').text).split(':')))

total[0]*=60
total=sum(total)
days=int(str(driver.find_element_by_xpath('//*[@id="presentDays"]').text))

absent=int(driver.find_element_by_xpath('//*[@id="absent"]').text)

driver.quit()

try:
    os.remove(r'geckodriver.log')
    os.system('tskill plugin-container')
except:
    pass

print email+' = '+ str(int((total-days*9.5*60)//60))+':'+"%02d"  % (int((total-days*9.5*60)%60),) + ' excess'
if absent!=0:
    print 'Absent : '+str(absent)
raw_input()
