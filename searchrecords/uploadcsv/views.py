from django.shortcuts import render
import pandas as pd 
# Create your views here.
from io import StringIO
import csv, io
from django.shortcuts import render
from django.contrib import messages
# Create your views here.
# one parameter named request
from django.http import HttpResponse
import requests
import re
import csv
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
import time 
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import csv 
import os
from twilio.rest import Client
from dotenv import load_dotenv
import base64
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (Mail, Attachment, FileContent, FileName, FileType, Disposition)
load_dotenv()
def Input_File_upload(request):
    # declaring template
    template = "input_upload.html"

    if request.method == "GET":
        return render(request, template)
    else:    
        csv_file = request.FILES['file']
        startdate=request.POST['startdate'].split("-")
        enddate=request.POST['enddate'].split("-")
        modifystartdate=startdate[1]+"/"+startdate[2]+"/"+startdate[0] 
        modifyenddate=enddate[1]+"/"+enddate[2]+"/"+enddate[0] 
        print(modifystartdate,modifyenddate,"ddddddddddddddddddddddddddd")
        # let's check if it is a csv file
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'THIS IS NOT A CSV FILE')
        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
      
        # print(io_string)
        # next(io_string)
        options = Options()
    
        # options.add_argument('--no-sandbox')
    
        # options.add_argument('--disable-extensions')
        
        # options.add_argument('--no-sandbox')
        # options.add_argument('--disable-dev-shm-usage')
        # options.headless=True 
        # driver = uc.Chrome(options=options)
        header = ['Address', 'Name', 'Index','File Date', 'Type','Film Code']
            
            
        with open('test.csv', 'w') as f:
                writer = csv.writer(f)
            
                # write the header
                writer.writerow(header)
        driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
        "login code ...."
        driver.get("https://cclerk.hctx.net/Applications/WebSearch/Registration/Login.aspx?ReturnUrl=%2fApplications%2fWebSearch%2fRP.aspx")
        driver.maximize_window() 
        driver.find_element(By.ID,"ctl00_ContentPlaceHolder1_Login1_UserName").send_keys("KentWare59@gmail.com")
        driver.find_element(By.ID,"ctl00_ContentPlaceHolder1_Login1_Password").send_keys("P@ssw0rd!")
        driver.find_element(By.ID,"ctl00_ContentPlaceHolder1_Login1_Password").send_keys(Keys.RETURN)
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            lot=column[-5]
            block=column[-4]
            address=column[0]
            name=column[2]
            index=column[-6]
            firstname=column[3]
            lastname=column[4]
            # print(lot,block,address,name,index)
            
           
            
            
            # reading the input the simple ...
          
    
            # for i in range(0,len(df['Lot'])):
            #  for i in range(0,len(df['Blk'])):
               
                
            if "First" not in firstname: 
                "Filling entry  code ...."
                N_DAYS_AGO = 6
            
                today = datetime.now()    
                n_days_ago = today - timedelta(days=N_DAYS_AGO)
            
              
                driver.find_element(By.ID,"ctl00_ContentPlaceHolder1_txtFrom").send_keys(modifystartdate)
                driver.find_element(By.ID,"ctl00_ContentPlaceHolder1_txtTo").send_keys(modifyenddate)
                Grantor=lastname+" "+firstname
                
                driver.find_element(By.ID,"ctl00_ContentPlaceHolder1_txtOR").send_keys(Grantor)
                try:
                    driver.find_element(By.ID,"ctl00_ContentPlaceHolder1_txtLot").send_keys(lot)
                except:
                    pass
                try:
                    driver.find_element(By.ID,"ctl00_ContentPlaceHolder1_txtBlock").send_keys(block)
                except:
                    pass
                driver.find_element(By.ID,"ctl00_ContentPlaceHolder1_btnSearch").click()
                
                
                
                "retrive the data from web page .." 
                
                soup=BeautifulSoup(driver.page_source ,"html.parser")
                all_rows=soup.find_all('tr',{'class':'odd'})
                data_list=[]
              
                for row in all_rows :
                    file_date=row.find_all('td')[2]
                    type=row.find_all('td')[3]
                    flim_code=row.find_all('td')[-1]
                    data_list.append(address.strip())
                    data_list.append(name.strip())
                    data_list.append(str(index).replace("\u00A0"," "))
                    
                    data_list.append(file_date.text.strip())
                    data_list.append(type.text.strip())
                    data_list.append(flim_code.text.strip())
                    print(data_list)
                    
                    df1=pd.DataFrame([data_list])
                    df1.to_csv("test.csv",header=False,index=False,mode="a" )
                    data_list.clear()
                    dict={}
                    dict['Name']=name.strip()
                    dict['Address']=address.strip()
                    dict['File Date']=file_date.text.strip()
                    dict['Flim code']=flim_code.text.strip()
                    # print(dict)
                    account_sid=os.getenv('account_sid')
                    auth_token=os.getenv('auth_token')
                    
                    client = Client(account_sid, auth_token)
                    
                    message = client.messages.create(    # sending the output over the phone text ...
                      body=str(dict),
                      from_="+18444130093",
                      to="+16143618186"
                    )
                    
                    print(message.sid)
                    dict.clear()
                driver.get("https://cclerk.hctx.net/Applications/WebSearch/RP.aspx")
                time.sleep(2)
        
        
        # sending output csv over the email ...
        
        
        message = Mail(
        from_email='ResearchedAssets@gmail.com',
        to_emails='ResearchedAssets@gmail.com',
        subject='output data ',
        html_content='output data ')
        
        
        with open('test.csv', 'rb') as f:
            data = f.read()
            f.close()
        encoded_file = base64.b64encode(data).decode()
        
        attachedFile = Attachment(
            FileContent(encoded_file),
            FileName('output.csv'),
            FileType('application/csv'),
            Disposition('attachment')
        )
        message.attachment = attachedFile
                            
        
        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        
        response = sg.send(message)
        print(response.status_code, response.body, response.headers)        
        return  HttpResponse("""
        Done ......
        Thanks to visit this page ......
        To continue please refreash the page .....
        """)       