import schedule
from xml.dom import minidom
import time
import datetime
import os
import datetime
import glob
from xml.etree import cElementTree as ET
import shutil
import schedule
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains


browser = None
Contact = []
message = []
Link = "https://web.whatsapp.com/"
wait = None
choice = None
docChoice = None
doc_filename = None
unsaved_Contacts = []
filename="C:\\Users\\kpf-admin\\Documents\\PyWhatsapp-master\\INPUT\\"
destination="C:\\Users\\kpf-admin\\Documents\\PyWhatsapp-master\\OUTPUT\\"
chromedriver = "C:\\Users\\kpf-admin\\Downloads\\chromedriver_win32\\chromedriver.exe"
def whatsapp_login():
    global wait,browser,Link
    
    browser = webdriver.Chrome(chromedriver)
    wait = WebDriverWait(browser, 600)
    browser.get(Link)
    browser.maximize_window()
    print("QR scanned")

def send_message(target,msg):
    global message,wait, browser
    try:
        x_arg = '//span[contains(@title,' + target + ')]'
        group_title = wait.until(EC.presence_of_element_located((By.XPATH, x_arg)))
        group_title.click()
        input_box = browser.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
        for ch in msg:
            if ch == "\n":
                ActionChains(browser).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.BACKSPACE).perform()
            else:
                input_box.send_keys(ch)
        input_box.send_keys(Keys.ENTER)
        print("Message sent successfuly")
        time.sleep(5)
    except NoSuchElementException:
        return

def send_unsaved_contact_message(msg):
    global message
    try:
        time.sleep(7)
        input_box = browser.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
        for ch in msg:
            if ch == "\n":
                ActionChains(browser).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.BACKSPACE).perform()
            else:
                input_box.send_keys(ch)
        input_box.send_keys(Keys.ENTER)
        print("Message sent successfuly")
       
    except NoSuchElementException:
        print("Failed to send message")
        return

def sender():
    global Contact,choice, docChoice, unsaved_Contacts
    count=0
    for i in Contact:
        send_message(i,message[count])
        print("Message sent to "+message[count],i)
        count=count+1
        
    time.sleep(5)
    if len(unsaved_Contacts)>0:
        count=0
        for i in unsaved_Contacts:
            link = "https://api.whatsapp.com/send?phone="+i
            #driver  = webdriver.Chrome()
            browser.get(link)
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="action-button"]').click()
            time.sleep(5)
            print("Sending message to", i)
            send_unsaved_contact_message(message[count])
            count=count+1
            try:
                WebDriverWait(browser, 3).until(EC.alert_is_present(),'Timed out waiting for PA creation ' +'confirmation popup to appear.')
                alert = browser.switch_to.alert
                alert.dismiss()
                print("alert Dismissed")
            except TimeoutException:
                print("no alert")
            
#This Function will read Data from Input File to Send Messages
def readFilesData():
    
    txtfiles = []
    for file in glob.glob(filename+"*.xml"):
        txtfiles.append(file)
        for f_name in txtfiles:
            tree = ET.parse(f_name)  
            root = tree.getroot()
            print('\nAll item data:') 
            count=0 
            for elem in root:  
                count=0
                my_dict={}
                for subelem in elem:
                    if count==0:
                        print("Case0:"+subelem.text)
                        my_dict['name']=subelem.text
                        #Contact.append(subelem.text)
                    if count==1:
                        print("Case1:"+subelem.text)
                        my_dict['mobile']=subelem.text
                        unsaved_Contacts.append(subelem.text)
                    if count==2:
                        print("Case2:"+subelem.text)
                        my_dict['message']=subelem.text
                        message.append(subelem.text) 
                    if count==3:
                        print("Case3:"+subelem.text)
                        my_dict['attachment']=subelem.text  
                    count=count+1
                my_list.append(my_dict)
            milli=int(round(time.time() * 1000))
            dest=destination+str(milli)+".xml"
            shutil.move(f_name,dest)
            
            

# To schedule your msgs
def scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)
if __name__ == "__main__":
    
    my_list=[]
    my_dict={}
    print("SCAN YOUR QR CODE FOR WHATSAPP WEB")
    whatsapp_login()
    
    while True:
        unsaved_Contacts=[]
        Contact=[]
        message=[]
        readFilesData()
        sender()
        # First time message sending Task Complete
        time.sleep(30)