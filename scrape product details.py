"""Ms. Harshal Lad"""

from bs4 import BeautifulSoup 
import random
import re
import time
import requests
import sys
import time
import mysql.connector
import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import json 
def anand():

    new_prod = []
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Anishad@123",
    database="abc"
    )
    # NOT NULL AUTO_INCREMENT PRIMARY KEY
    mycursor = mydb.cursor()
    mycursor.execute("""CREATE TABLE if not exists `lllreptile_op` (
    `id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `Product_Title` varchar(300) NOT NULL,
    `sku` varchar(200) NOT NULL,
    `parent_sku` varchar(200) DEFAULT NULL,
    `primary_sku` varchar(200) DEFAULT NULL,
    `size` varchar(200) DEFAULT NULL,
    `species` varchar(200) DEFAULT NULL,
    `gender` varchar(200) DEFAULT NULL,
    `UPC` varchar(15) DEFAULT NULL,
    `EAN` varchar(12) DEFAULT NULL,
    `LMP_SKU` varchar(200) DEFAULT NULL,
    `mfg_id` varchar(30) DEFAULT NULL,
    `FF_Latency` varchar(10) DEFAULT NULL,
    `Amazon_ASIN` varchar(10) DEFAULT NULL,
    `is_change` binary(1) DEFAULT NULL,
    `notions_unit_of_sale` int(3) DEFAULT NULL,
    `previous_vnp` decimal(7,2) DEFAULT NULL,
    `fcsus_unit_of_sale` int(3) DEFAULT NULL,
    `vnp` decimal(7,2) DEFAULT NULL,
    `inward_freight` decimal(7,2) DEFAULT '0.00',
    `Product_Net_Weight_Oz` decimal(7,2) DEFAULT NULL,
    `previous_shipping_weight` decimal(7,2) DEFAULT '0.00',
    `shipping_weight` decimal(7,2) DEFAULT NULL,
    `product_introduce_date` varchar(255) DEFAULT NULL,
    `length` decimal(7,2) DEFAULT NULL,
    `width` decimal(7,2) DEFAULT NULL,
    `height` decimal(7,2) DEFAULT NULL,
    `product_description` text,
    `price_update_override` int(1) DEFAULT '0',
    `wgt_update_override` int(1) DEFAULT '0',
    `Minimum_Advertised_Price` decimal(7,2) DEFAULT NULL,
    `frt_collect` varchar(1) DEFAULT 'N',
    `image1` varchar(500) DEFAULT NULL,
    `previous_qty_avb` int(1) DEFAULT '0',
    `qty_avb` int(1) DEFAULT '0',
    `stock` int(1) DEFAULT '0',
    `category` text,
    `sub_category` text,
    `sub_sub_category` text,
    `sub_sub_sub_category` text,
    `Product_link` text,
    `discontinued` int(1) DEFAULT '0',
    `last_updated` varchar(255) DEFAULT NULL,
    `doba_categories` varchar(255) DEFAULT NULL,
    `doba_allowed` int(1) NOT NULL DEFAULT '1'
    ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1
    """)
    # mycursor.execute("UPDATE `lllreptile_op`  SET previous_vnp = vnp")
    # mycursor.execute("ALTER TABLE llreptile.`lllreptile_op` CONVERT TO CHARACTER SET utf8;")
    urls = "https://www.lllreptile.com"
    mycursor = mydb.cursor()
    Query = ("select * from  `lllreptile_product_url`where `processed` = '0'")
    mycursor.execute(Query)
    records = mycursor.fetchall()
    if records != []:
        mycursor = mydb.cursor()
        mycursor.execute("UPDATE `lllreptile_op`  SET previous_vnp = vnp")
        mycursor = mydb.cursor()
        mycursor.execute('UPDATE `lllreptile_op`  SET previous_qty_avb = qty_avb')

    #print(records)
    def fun(gender,vnp):
        new_prod.append(product_id)
        val=list(zip((title,),(product_id,),(product_id,),(product_id,),(size,),(species,),(gender,),(vnp,),(description,),(img,),('1',),(category,),(sub_category,),(sub_sub_category,),(sub_sub_sub_category,),(url,)))
        #print(val)
        mycursor = mydb.cursor()
        sql = """insert into `lllreptile_op`(`Product_Title`, `sku`,`parent_sku`,`primary_sku`,`size`,`species`,`gender`,`vnp`,`product_description`,`image1`,`stock`,`category`,`sub_category`,`sub_sub_category`,`sub_sub_sub_category`,`Product_link`) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""" 
        mycursor.executemany(sql,val) 
        mydb.commit() 
        

    for rows in records:
    
        url=rows[7]
        #print(rows[7])
        headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}   
        try:
            response = requests.get(url, headers = headers)
        except:
            time.sleep(random.randint(1,5))
            response = requests.get(url, headers = headers)

        html = response.text
        soup = BeautifulSoup(html,"lxml")
        productdata=soup.find_all('div',attrs = {'class':'catalog-show-product x_analyticsProduct'})
        for tag in productdata:

            title_val=rows[6]
            title= title_val.lstrip().rstrip()
            product_id =rows[1]
            category =rows[2]
            sub_category =rows[3]
            sub_sub_category =rows[4]
            sub_sub_sub_category =rows[5]
            #print(title)
            description=''
            try:
                desc=tag.find_all('div',attrs = {'class':'markdown'})
                for d in desc:
                    description=d.text.lstrip().rstrip()
            except Exception as e:
                # print (e)
                pass
            size=''
            try:
                size_element=tag.find_all('p',attrs = {'class':'product-size'})
                for s in size_element:
                    size=s.text.lstrip().rstrip()
            except Exception as e:
                pass
                # print (e)
            img=''
            try:
                img_element=tag.find('img')
                link=img_element.get('src')
                img = urls+str(link)
            except Exception as e:
                pass
                # print (e) 
            species=''
            try:
                species_element=tag.find_all('p',attrs = {'class':'product-species'})
                for sp in species_element:
                    species=sp.text.lstrip().rstrip()
            except Exception as e:
                pass
                # print (e)
            try:
                stock_element=tag.find('div',attrs = {'class':'catalog-product-archived'})
                stock=stock_element.text
                if 'product is restocked' in stock:
                    try: 
                        mycursor = mydb.cursor()     
                        mycursor.execute("SELECT sku FROM `lllreptile_op` WHERE Product_Title = %s", (title,))
                        myresult = mycursor.fetchall()
                        #print(myresult)
                        mycursor = mydb.cursor()
                        mycursor.execute("UPDATE `lllreptile_product_url` SET `processed` = '1' WHERE product_name = %s  ", (title_val,))
                        mycursor = mydb.cursor()
                        mycursor.execute("UPDATE `lllreptile_op` SET `stock` = %s  WHERE Product_Title = %s", ('0',title,)) 
                    except Exception as e:
                        pass
                        # print (e)
                    if myresult == []:
                        new_prod.append(product_id)
                        val=list(zip((title,),(product_id,),(product_id,),(product_id,),(size,),(species,),(description,),(img,),('0',),(category,),(sub_category,),(sub_sub_category,),(sub_sub_sub_category,),(url,)))
                        #print(val)
                        mycursor = mydb.cursor()
                  
                        sql = """insert into `lllreptile_op`(`Product_Title`, `sku`,`parent_sku`,`primary_sku`,`size`,`species`,`product_description`,`image1`,`stock`,`category`,`sub_category`,`sub_sub_category`,`sub_sub_sub_category`,`Product_link`) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""" 
                        mycursor.executemany(sql,val) 
                        mydb.commit() 
            except Exception as e:
                pass
                # print (e)    
            price_element=tag.find_all('label',attrs = {'class':'form-check-label'})
            for p in price_element:
         
                price=p.text.lstrip().rstrip()
                #print(price)
                array_numeric_values=re.findall('\d*\.?\d+',price)
                try:
                    decimal_value=re.findall('\d+\.\d*\s',price)
                    vnp=decimal_value[-1]
                    if 'each' in price:
                        try: 
                            mycursor = mydb.cursor()     
                            mycursor.execute("SELECT sku FROM `lllreptile_op` WHERE Product_Title = %s", (title,))
                            myresult = mycursor.fetchall()
                            #print(myresult)
                            mycursor = mydb.cursor()
                            mycursor.execute("UPDATE `lllreptile_product_url` SET `processed` = '1' WHERE product_name = %s  ", (title_val,))
                            mycursor = mydb.cursor()
                            mycursor.execute("UPDATE `lllreptile_op` SET `vnp`= %s WHERE Product_Title = %s", (vnp,title,)) 
                        except Exception as e:
                            pass
                            # print (e)
                        if myresult == []:
                            gender=''
                   
                            fun(gender,vnp)

                    if '(female)' in price:
                        gender='female'
                        if'(male)' in price:
                            vnp=array_numeric_values[1]
                        else:
                            vnp=array_numeric_values[0]
                        try:
                            mycursor = mydb.cursor()     
                            mycursor.execute("SELECT sku FROM `lllreptile_op` WHERE Product_Title = %s", (title,))
                            myresult = mycursor.fetchall()
                            #print(myresult)
                            mycursor = mydb.cursor()
                            mycursor.execute("UPDATE `lllreptile_product_url` SET `processed` = '1' WHERE product_name = %s", (title_val,))
                            mycursor = mydb.cursor()
                            mycursor.execute("UPDATE `lllreptile_op` SET  `vnp`= %s WHERE Product_Title = %s and `gender` =%s ", (vnp,title,gender,)) 
                        except Exception as e:
                            pass
                            # print (e)
                        if myresult == [] : 
                      
                            fun(gender,vnp)
                        if myresult != []:
                            mycursor = mydb.cursor()     
                            mycursor.execute("SELECT gender FROM `lllreptile_op` WHERE Product_Title = %s", (title,))
                            myresult = mycursor.fetchall()
                            #print(myresult)
                            if myresult == [('male',)] or myresult == [('0',)]:
                                #print(gender)
                                gender='female'
                       
                                fun(gender,vnp)
                    if '(male)' in price:
                        gender='male'
                        if'(female)' in price:
                            vnp=array_numeric_values[1]
                        else:
                            vnp=array_numeric_values[0]
                        try:    
                            mycursor = mydb.cursor()     
                            mycursor.execute("SELECT sku FROM `lllreptile_op` WHERE Product_Title = %s", (title,))
                            myresult = mycursor.fetchall()
                        # print(myresult)
                            mycursor = mydb.cursor()
                            mycursor.execute("UPDATE `lllreptile_product_url` SET `processed` = '1' WHERE product_name = %s ", (title_val,))
                            mycursor = mydb.cursor()
                            mycursor.execute("UPDATE `lllreptile_op` SET  `vnp`= %s WHERE Product_Title = %s and `gender` = %s ", (vnp,title,gender,)) 
                        except Exception as e:
                            # print (e)
                            pass
                        if myresult == [] :
                     
                            fun(gender,vnp)
                        if myresult != []:
                            mycursor = mydb.cursor()     
                            mycursor.execute("SELECT gender FROM `lllreptile_op` WHERE Product_Title = %s", (title,))
                            myresult = mycursor.fetchall()
                            #print(myresult)
                        if myresult == [('female',)]or myresult == [('0',)]:
                            #print(gender)
                            gender='male'
               
                            fun(gender,vnp)
                    if 'pair' in price:
                        gender='pair'
                        vnp=array_numeric_values[-1]
                        try:    
                            mycursor = mydb.cursor()     
                            mycursor.execute("SELECT sku FROM `lllreptile_op` WHERE Product_Title = %s", (title,))
                            myresult = mycursor.fetchall()
                            #print(myresult)
                            mycursor = mydb.cursor()
                            mycursor.execute("UPDATE `lllreptile_product_url` SET `processed` = '1' WHERE product_name = %s ", (title_val,))
                            mycursor = mydb.cursor()
                            mycursor.execute("UPDATE `lllreptile_op` SET  `vnp`= %s WHERE Product_Title = %s and `gender` = %s  ", (vnp,title,gender,)) 
                        except Exception as e:
                            pass
                            # print (e)
                        if myresult == [] :
                  
                            fun(gender,vnp)
                        if myresult != []:
                            mycursor = mydb.cursor()     
                            mycursor.execute("SELECT gender FROM `lllreptile_op` WHERE Product_Title = %s", (title,))
                            myresult = mycursor.fetchall()
                            #print(myresult)
                            if myresult == [('male',), ('female',)]or myresult == [('0',)]:
                                #print(gender)
                      
                                fun(gender,vnp)
                except Exception as e:
                    pass    
                    # print (e)
    mycursor = mydb.cursor()
    mycursor.execute("UPDATE `lllreptile_op`  SET qty_avb = stock") 
    mydb.commit()

    mycursor = mydb.cursor()    
    mycursor.execute("select sku,vnp,previous_vnp,previous_qty_avb,qty_avb from `lllreptile_op`")
    result = mycursor.fetchall()
    with open('lllreptile_vnp.csv', 'w',  newline='') as outcsv:
            writer = csv.writer(outcsv)
            writer = csv.DictWriter(outcsv, fieldnames = ["sku", "vnp", "previous_vnp"])
            writer.writeheader()
            
    with open('lllreptile_stock.csv', 'w',  newline='') as stcsv:
            writers = csv.writer(stcsv)
            writers = csv.DictWriter(stcsv, fieldnames = ["sku", "previous quantity", "quantity available"])
            writers.writeheader()
    with open('lllreptile_new_prod.csv', 'w',  newline='') as skucsv:
            writers = csv.writer(skucsv)
            writers = csv.DictWriter(skucsv, fieldnames = ["new_prod"])
            writers.writeheader()
    for x in result:
        sku=x[0]
        vnp= x[1]
        pvnp= x[2]
        pqty=x[3]
        qty=x[4]
        if vnp!=pvnp:
            with open('lllreptile_vnp.csv', 'a', newline='') as vnpcsv:
                writer = csv.writer(vnpcsv)
                writer = csv.DictWriter(vnpcsv, fieldnames =[sku,vnp,pvnp])
                writer.writeheader()
        if pqty != qty:
            with open('lllreptile_stock.csv', 'a', newline='') as stockcsv:
                writers = csv.writer(stockcsv)
                writers = csv.DictWriter(stockcsv, fieldnames =[sku,pqty,qty])
                writers.writeheader()
    for i in new_prod:
        with open('lllreptile_new_prod.csv', 'a', newline='') as stockcsv:
            writers = csv.writer(stockcsv)
            writers = csv.DictWriter(stockcsv, fieldnames =[i])
            writers.writeheader()
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
    filename = "File_name_with_extension"
    attachment = open('./lllreptile_vnp.csv', "rb")
    
    parter1 = MIMEBase('application', 'octet-stream')
    parter1.set_payload((attachment).read())
    encoders.encode_base64(parter1)
    parter1.add_header('Content-Disposition', 'attachment', filename='lllreptile_vnp.csv')
    msg.attach(parter1)
    
    parter2 = MIMEBase('application', "octet-stream")
    parter2.set_payload(open('./lllreptile_stock.csv', "rb").read())
    encoders.encode_base64(parter2)
    parter2.add_header('Content-Disposition', 'attachment', filename='lllreptile_stock.csv')  
    msg.attach(parter2)

    parter3 = MIMEBase('application', "octet-stream")
    parter3.set_payload(open('./lllreptile_new_prod.csv', "rb").read())
    encoders.encode_base64(parter3)
    parter3.add_header('Content-Disposition', 'attachment', filename='lllreptile_new_prod.csv')  
    msg.attach(parter3)
    
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
        s = "Script Executed Successfully"
        mail_send(s)
        print(s)
    except:
        s = "Script Executed Unsuccessfully"
        print(s)

if __name__ == "__main__":
    main()  
