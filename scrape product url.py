import json
import requests
from bs4 import BeautifulSoup
import mysql.connector
import pandas as pd
import smtplib


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase

from email import encoders
import os
import mysql.connector
import sys

def anand():
    '''auther: ms. Harshal Lad'''

    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Anishad@123",
    database="abc"
    )
    mycursor = mydb.cursor() 
    mycursor.execute("""CREATE TABLE if not exists `lllreptile_product_url` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `product_id` varchar(255) DEFAULT NULL,
    `category` varchar(255) DEFAULT NULL,
    `sub_category` varchar(255) DEFAULT NULL,
    `sub_sub_category` varchar(255) DEFAULT NULL,
    `sub_sub_sub_category` varchar(255) DEFAULT NULL,
    `product_name` varchar(255) DEFAULT NULL,
    `url` varchar(255) DEFAULT NULL,
    `processed` int(1) DEFAULT '0',
    `add_url` int(1) DEFAULT '0',
    KEY `id` (`id`)
    ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1""")
    pid = 'LP01000001'
    urls = "https://www.lllreptile.com"
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}   
    url = "https://www.lllreptile.com/catalog"
    response = requests.get(url, headers = headers)
    html = response.text
    soup = BeautifulSoup(html)
    z=soup.find_all('div',attrs = {'class':'catalog-category card'})
    for i in z:
 
        z1=i.find_all('a',attrs = {'title':'Browse this category.'})
        for i1 in z1:

            cat1 =i1.text
            #print(cat1)
        for link in z1:

            m=link.get('href')
            #print(m)
            u = urls+str(m)
            # print(u)
            response1 = requests.get(u, headers = headers)
            html1 = response1.text
            soup1 = BeautifulSoup(html1)
            z2=soup1.find_all('div',attrs = {'class':'catalog-category card'})
            for i2 in z2:
  
                #print(i.text)
                z3=i2.find_all('a',attrs = {'title':'Browse this category.'})
                for i2 in z3:
     
                    cat2 =i2.text
                    #print(cat2)
                for link1 in z3:
       
                    m2=link1.get('href')
                    #print(m)
                    u2= urls+str(m2)
                    #print(u2)
                    try:
                        response2 = requests.get(u2, headers = headers)
                        html2 = response2.text
                        soup2 = BeautifulSoup(html2)
                        cat4=''
                        cat3=''
                        try:
                            z8=soup2.find_all('div',attrs = {'class':'product-wrap x_analyticsProductInList'})
                            for p in z8:
                 
                                #print(z8)
                                pro=p.find('div',attrs = {'class':'product-title'})
                                title = pro.text
                                pl=pro.find('a')
                                prom=pl.get('href')
                                prod= urls +str(prom)
                                #print(prod)
                                try:
                                    mycursor = mydb.cursor()     
                                    mycursor.execute("SELECT id FROM `lllreptile_product_url` WHERE product_name = %s", (title,))
                                    myresult = mycursor.fetchall()
                                    # print(myresult)
                                except Exception as e:
                                    # print (e)
                                    pass
                                if myresult == []:
                                      
                                    val=list(zip((pid,),(cat1,),(cat2,),(cat3,),(cat4,),(title,),(prod,)))
                                    #print(val)
                                    mycursor = mydb.cursor()
                                    sql = """insert into `lllreptile_product_url`(`product_id`,`category`, `sub_category`, `sub_sub_category`,`sub_sub_sub_category`,`product_name`,`url`) values (%s,%s,%s,%s,%s,%s,%s)""" 
                                    mycursor.executemany(sql,val)
                        except Exception as e:
                            # print (e)  
                            pass  
                        z4=soup2.find_all('div',attrs = {'class':'catalog-category card'})
                        for i3 in z4:
           
                            #print(i.text)
                            z5=i3.find_all('a',attrs = {'title':'Browse this category.'})
                            for i4 in z5:
                                cat3 =i4.text
                                #print(cat3)
                          
                            for link2 in z5:
                             
                                m3=link2.get('href')
                                #print(m)
                                u3= urls+str(m3)
                                #print(u3)
                                try:
                                    response3 = requests.get(u3, headers = headers)
                                    html3 = response3.text
                                    soup3 = BeautifulSoup(html3)
                                    cat4=''
                                    try:
                                        z8=soup3.find_all('div',attrs = {'class':'product-wrap x_analyticsProductInList'})
                                        for p in z8:
                                            
                                            #print(z8)
                                            pro=p.find('div',attrs = {'class':'product-title'})
                                            title = pro.text
                                            pl=pro.find('a')
                                            prom=pl.get('href')
                                            prod= urls +str(prom)
                                            #print(prod)
                                            try:
                                                mycursor = mydb.cursor()     
                                                mycursor.execute("SELECT id FROM `lllreptile_product_url` WHERE product_name = %s", (title,))
                                                myresult = mycursor.fetchall()
                                                # print(myresult)
                                            except Exception as e:
                                                # print (e)
                                                pass
                                            if myresult == []:
                                                val=list(zip((pid,),(cat1,),(cat2,),(cat3,),(cat4,),(title,),(prod,)))
                                                #print(val)
                                                mycursor = mydb.cursor()
                                                sql = """insert into `lllreptile_product_url`(`product_id`,`category`, `sub_category`, `sub_sub_category`,`sub_sub_sub_category`,`product_name`,`url`) values (%s,%s,%s,%s,%s,%s,%s)""" 
                                                mycursor.executemany(sql,val)
                                    except Exception as e:
                                        # print (e)    
                                        pass
                                    z6=soup3.find_all('div',attrs = {'class':'catalog-category card'})
                                    for i5 in z6:
                                 
                                        #print(i.text)
                                        z7=i5.find_all('a',attrs = {'title':'Browse this category.'})
                                        for i6 in z7:
                                       
                                            cat4 =i6.text
                                            #print(cat4)
                                        for link3 in z7:
                                           
                                            m4=link3.get('href')
                                            #print(m4)
                                            u4= urls+str(m4)
                                            #print(u4)
                                            try:
                                                response4 = requests.get(u4, headers = headers)
                                                html4 = response4.text
                                                soup4 = BeautifulSoup(html4)
                                                z8=soup4.find_all('div',attrs = {'class':'product-wrap x_analyticsProductInList'})
                                                for p in z8:
                                                 
                                                    #print(z8)
                                                    pro=p.find('div',attrs = {'class':'product-title'})
                                                    title = pro.text
                                                    pl=pro.find('a')
                                                    prom=pl.get('href')
                                                    prod= urls +str(prom)
                                                    #print(prod)
                                                    try:
                                                        mycursor = mydb.cursor()     
                                                        mycursor.execute("SELECT id FROM `lllreptile_product_url` WHERE product_name = %s", (title,))
                                                        myresult = mycursor.fetchall()
                                                        # print(myresult)
                                                    except Exception as e:
                                                        # print (e)
                                                        pass
                                                    if myresult == []:
                                                        val=list(zip((pid,),(cat1,),(cat2,),(cat3,),(cat4,),(title,),(prod,)))
                                                        #print(val)
                                                        mycursor = mydb.cursor()
                                                        sql = """insert into `lllreptile_product_url`(`product_id`,`category`, `sub_category`, `sub_sub_category`,`sub_sub_sub_category`,`product_name`,`url`) values (%s,%s,%s,%s,%s,%s,%s)""" 
                                                        mycursor.executemany(sql,val)
                                            except Exception as e:
                                                # print (e)
                                                pass
                                except Exception as e:
                                    # print (e)
                                    pass    
                    except Exception as e:
                        # print (e)
                        pass
                        
    mycursor = mydb.cursor()
    sql ='''UPDATE `lllreptile_product_url`  SET product_id =CONCAT('LP01',LPAD(id,5,0))'''
    mycursor.execute(sql)
    mydb.commit() 
def mail_send(s):
    fromaddr = "anandn@fcsus.com"
    toaddr = "nishadaman4438@gmail.com"
    msg = MIMEMultipart()
    # storing the senders email address  
    msg['From'] = fromaddr
    # storing the receivers email address 
    msg['To'] = toaddr
    # storing the subject 
    msg['Subject'] = "Differences between vnp & stock(qty) "
    # string to store the body of the mail
    body = s
    msg.attach(MIMEText(body, 'plain'))
    # open the file to be sent 
    s = smtplib.SMTP('smtp.office365.com', 587)
    s.starttls()  
    # Authentication(password)
    s.login(fromaddr, 'Aman@123')
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit() 
def main():
    try:
        anand()
        s = "Script Executed Successfully "
        mail_send(s)
        print(s)
    except:
        s = "Script Executed Unsuccessfully"
        print(s)


if __name__ == "__main__":
    main()           