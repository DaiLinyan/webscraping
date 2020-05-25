#!/usr/bin/env python
# coding: utf-8




import requests
from bs4 import BeautifulSoup
import time
import re
import os
import pymysql


# # Part 1
#Go to http://numbersapi.com and familiarize yourself with the API.
#a) Write a program that accesses all trivia results for the numbers from 0 
#(zero) to 99 using batch requests only (One single query for all the numbers). 
#Print the output result to the screen in the format of [3-digit number with leading zeros] 
#- [TRIVIA] (One number per each line). E.g.,

numbers = []
for i in range(100):
    if i < 10:
        numbers.append('00'+str(i))
    else:
        numbers.append('0'+str(i))



for i in range(100):
    url = 'http://numbersapi.com/'+str(i)+'/math'
    text = requests.get(url)
    strings = numbers[i] + '-' + text.text
    print(strings)


# # Part 2


#a) 
#How would you modify your search query to only include buy-it-now (non-auction)
# items? What is the GET request's variable name corresponding to buy-it-now 
# searches? How would you modify your search query to include 100 items per 
# search result page? What is the GET request's variable name corresponding to 
# items per page searches? Include your answers as a comment in your code marking
# it as Part 2-a. (This section does not involve coding)

# Answer:
# I would use &_ipg=100 to define page limit
# I would use &LH_BIN=1 to define 'Buy it Now'

# GET request's variable name corresponding to page-limit:
# _nkw: samsung tv
# _ipg: 100

# GET request's variable name corresponding to buy-it-now searches
# _nkw: samsung tv
# _ipg: 100
# rt: nc
# LH_BIN: 1


# b  For the first 10 pages of 100 items/page, save all the URLs of 
# sponsored items' pages to the file "sponsored.txt" and all the URLs 
# of non-sponsored items' pages to the file "non-sponsored.txt" 
# in the same directory as your code.

urllist=[]
for i in range(10):
    urllist.append('https://www.ebay.com/sch/i.html?_nkw=canon+eos+5d&LH_BIN=1&_ipg=100&_pgn='+str(i+1))

sponsor_link = []
nosponsor_link = []

for url in urllist:
    content = requests.get(url)
    soup = BeautifulSoup(content.text,'html.parser')
    for item in soup('a','s-item__link'):
        if 's-item__title s-item__title--has-tags' in str(item):
            sponsor_link.append(item.attrs['href'])
        else:
            nosponsor_link.append(item.attrs['href'])
    time.sleep(1)


f = open('sponsored.txt','w')
for link in sponsor_link:
    f.write(link)

f = open('non-sponsored.txt','w')
for link in nosponsor_link:
    f.write(link)


# c Create two folders in the same directory as your code and name them 
# "sponsored" and "non-sponsored". Write a program that opens the two files in 
# (b) and downloads each of the pages (URLs) into the folders "sponsored" and 
# "non-sponsored". Each file should be named as "<item-id>.htm" where you 
# replace "item- id" with the ID of the item you are saving. 
# E.g., "264616053293.htm" for the item with ID "264616053293". 
# Note it is always good to put a 2-second pause between queries. 
# Make sure to catch an error and continue if your query runs into problems 
# connecting to eBay. 

mydir = os.getcwd()

os.mkdir('sponsored')

os.chdir('sponsored')

sponsor_profile_names = []

# Store all the sponsored item into profile
try:
    for link in sponsor_link:
        a = requests.get(link)
        soup = BeautifulSoup(a.text,'html.parser')
        ItemID = soup.select('#descItemNumber')[0].text
        profile_name = ItemID+'.htm'
        sponsor_profile_names.append(profile_name)
        content = a.text
        f = open(profile_name,'w')
        f.write(content)
        f.close()
        time.sleep(2)
except Exception as e:
    print(e)


os.chdir(mydir)

os.mkdir('non-sponsored')

os.chdir('non-sponsored')

nonsponsor_profile_names = []

# Store all the non-sponsored item into profile
try:
    for link in nosponsor_link:
        a = requests.get(link)
        soup = BeautifulSoup(a.text,'html.parser')
        ItemID = soup.select('#descItemNumber')[0].text
        profile_name = ItemID+'.htm'
        nonsponsor_profile_names.append(profile_name)
        f = open(profile_name,'w')
        f.write(a.text)
        f.close()
        time.sleep(2)
except Exception as e:
    print(e)


# d) Write a separate piece of code that loops through the pages you downloaded 
# in (c) and opens and parses them into a Python or Java xxxxsoup-object. Identify and select:
# seller name, seller score, item price, # items sold, best offer available, 
# title, returns allowed, shipping price, condition (e.g., used, new, like new, seller refurbished, ...).
# In your code, highlight the selector command you choose to obtain each element using comments.



# Define the function to get all the information
def get_value(profile):

    file=open(profile,'r')
    soup=BeautifulSoup(file,'html.parser')

    try:
    #selector command for seller name
        seller_name = soup.select('#RightSummaryPanel>div>div>div>div>div>div>a>span.mbg-nw')[0].text
    except:
        seller_name = None

    try:
    #selector command for seller score
        seller_score = soup.select('#RightSummaryPanel>div>div>div>div>div>div>span>a')[0].text
    except:
        seller_score = None

    #selector command for item price
    try:
        item_price = soup.select('span#prcIsum.notranslate')[0].text
    except:
        try:
            item_price = soup.select('span#mm-saleDscPrc.notranslate')[0].text
        except:
            item_price = soup.select('span#prcIsum_bidPrice.notranslate')[0].text

    try:
        item_price = int(float(item_price.split('$')[1].replace(',',''))*100)
    except:
        try:
            item_price = int(float(item_price.split('$')[1].replace(',','').split('/')[0])*100)
        except:
            item_price = soup.select('span#convbinPrice')[0].text
            item_price = int(float(item_price.split('$')[1].replace(',','').split('(')[0])*100)
    #selector command for itemssold
    try:
        items_sold = soup.select('#mainContent>form>div>div>div>div>span>span>span>a.vi-txt-underline')[0].text
        items_sold = int(items_sold.split(' ')[0].replace(',',''))
    except:
        items_sold = None

    #selector command for shipping price
    try:
        shipping_price = soup.select('a#e3.si-pd.sh-nwr')[0].text
        shipping_price = None
        shipping_computed = 1
    except:
        try:
            shipping_price = soup.select('#fshippingCost>span')[0].text
            if shipping_price == 'FREE':
                shipping_price = 0
            else:
                shipping_price = int(float(shipping_price)*100)
            shipping_computed = 0
        except:
            try:
                shipping_price = soup.select('#shSummary>div>span>strong.sh_gr_bld')[0].text
                shipping_price = 0
                shipping_computed = 0
            except:
                try:
                    shipping_price = soup.select('span#fShippingSvc')[0].text
                    shipping_price = None
                    shipping_computed = 0
                except:
                    try:
                        shipping_price = soup.select('a#e4.si-pd.sh-nwr')[0].text
                        shipping_price = None
                        shipping_computed = 1
                    except:
                        shipping_price = None
                        shipping_computed = 0

    #selector command for best offer available
    try:
        best_offer_available = soup.select('#mainContent>form>div>div>div>div.vi-bbox-dspn.u-flL.lable.boLable')[0].text
        best_offer_available = 1
    except:
        best_offer_available = 0

    #selector command for title
    title = soup.select('#itemTitle')[0].text
    title = title.split('Details about  \xa0')[1]

    #selector command for return allowed
    try:
        returns_allowed = soup.select('#why2buy>div>div.w2b-cnt.w2b-3.w2b-brdr>span.w2b-sgl')[0].text
    except:
        returns_allowed = soup.select('#why2buy>div>div>span.w2b-sgl')
        for i in returns_allowed:
            if 'Returns' in i.text or 'returns' in i.text:
                returns_allowed = i.text
    if returns_allowed == 'Returns accepted':
        returns_allowed = 1
    else:
        returns_allowed = 0

    #selector command for condition
    condition = soup.select('div#vi-itm-cond.u-flL.condText')[0].text

    #create a dictionary to store the data
    information = {}
    information['seller_name'] = seller_name
    information['seller_score'] = seller_score
    information['item_price'] = item_price
    information['items_sold'] = items_sold
    information['shipping_price'] = shipping_price
    information['shipping_computed'] = shipping_computed
    information['best_offer_available'] = best_offer_available
    information['title'] = title
    information['returns_allowed'] = returns_allowed
    information['condition'] = condition
    return information


os.chdir(mydir)

os.chdir('sponsored')

data = []
# Get information from sponsored item
for profile in sponsor_profile_names:
    item = get_value(profile)
    item['sponsored'] = 1
    data.append(item)

os.chdir(mydir)

os.chdir('non-sponsored')

# Get information from non-sponsored item
for profile in nonsponsor_profile_names:
    item = get_value(profile)
    item['sponsored'] = 0
    data.append(item)


# e) Use your code script to connect to SQL (either MySQL, MariaDB, or SQLite. 
# Do NOT use SQL GUI or command terminal). Create a database and name it "eBay". 
# Save the information of items in (d) into a single table named "eBay_items" 
# (You are allowed to use only one table). This table should contain both 
# sponsored and non-sponsored information and have a column that specifies 
# which item is sponsored/non- sponsored. If an item misses ANY of the information
# in (d), you should insert that missing value as NULL into the table. 
# Convert any price (item price and shipping price) into a "dollar-cent" format 
# (e.g., convert $12.34 into 1234 and $12 into 1200. Make sure the two least 
# significant digits are cents. If an item does not include cents in the price, 
# insert zeros.) and insert the price as INT into the table.



# Create database and table
try:

     #connect to server
    conn = pymysql.connect(host='localhost', user = 'root', password = '')
    cursor = conn.cursor()

    query = "CREATE DATABASE IF NOT EXISTS eBay;"
    print(query)
    cursor.execute(query)
    conn.commit()
        
    query = "CREATE TABLE IF NOT EXISTS eBay.eBay_items (id int not null auto_increment primary key, seller_name varchar(30)," +     "seller_score smallint(10), item_price_cent smallint(10), items_sold smallint(10), best_offer_available tinyint(1), title varchar(100)," +     "returns_allowed tinyint(1), shipping_price_cent smallint(6), shipping_computed tinyint(1), _condition varchar(20), sponsored tinyint(1));"
    
    print(query)
    cursor.execute(query)
    conn.commit
    cursor.close()
    conn.close()

except IOError as e:
    print(e)


# Insert data into database
for information in data:
    try:
        conn = pymysql.connect(host='localhost', user = 'root', password = '')
        cursor = conn.cursor()

        insert_query='insert ignore into eBay.eBay_items (seller_name, seller_score, item_price_cent, items_sold, shipping_price_cent, shipping_computed, best_offer_available,  title,  returns_allowed, _condition, sponsored) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        
        cursor.execute(insert_query,[information['seller_name'], information['seller_score'], information['item_price'], information['items_sold'], information['shipping_price'], information['shipping_computed'], information['best_offer_available'], information['title'], information['returns_allowed'], information['condition'], information['sponsored']])
        
        print(insert_query,information['seller_name'], information['seller_score'], information['item_price'], information['items_sold'], information['shipping_price'], information['shipping_computed'], information['best_offer_available'], information['title'], information['returns_allowed'], information['condition'], information['sponsored'])
        
        conn.commit()
        cursor.close()
        conn.close()
    except IOError as e:
        print(e)


# f) Use your code script (and NOT SQL GUI or command terminal) to run summary 
# stats on each item. Print to the screen the mean, min, max, and mean 
# for each column, grouped by "sponsor/non-sponsor" and "condition" 
# (group by at the same time, not separately). For binary categorical columns, 
# use 0-1 conversion. For e.g., for the "returns allowed" convert YES to 1 
# and NO to 0 and then calculate the stats. If it is NOT a numerical/binary 
# categorical column, print to the screen the count of each category level. 
# You will need to ignore NULL values in your statistic calculations.


results = []

try:
    conn = pymysql.connect(host='localhost', user = 'root', password = '')
    cursor = conn.cursor()

    query = 'use eBay;'
    cursor.execute(query)

    query = 'select min(seller_score), max(seller_score), avg(seller_score), sponsored, _condition from eBay_items group by sponsored, _condition;'
    cursor.execute(query)
    result = cursor.fetchall()
    print(query)
    for i in result:
        print(i)
    results.append(result)
    
    query = 'select min(item_price_cent), max(item_price_cent), avg(item_price_cent), sponsored, _condition from eBay_items group by sponsored, _condition;'
    cursor.execute(query)
    result = cursor.fetchall()
    print(query)
    for i in result:
        print(i)
    results.append(result)
    
    query = 'select min(best_offer_available), max(best_offer_available), avg(best_offer_available), sponsored, _condition from eBay_items group by sponsored, _condition;'
    cursor.execute(query)
    result = cursor.fetchall()
    print(query)
    for i in result:
        print(i)
    results.append(result)
    
    query = 'select min(returns_allowed), max(returns_allowed), avg(returns_allowed), sponsored, _condition from eBay_items group by sponsored, _condition;'
    cursor.execute(query)
    result = cursor.fetchall()
    print(query)
    for i in result:
        print(i)
    results.append(result)  
    
    query = 'select min(items_sold), max(items_sold), avg(items_sold), sponsored, _condition from eBay_items group by sponsored, _condition;'
    cursor.execute(query)
    result = cursor.fetchall()
    print(query)
    for i in result:
        print(i)
    results.append(result) 
    
    query = 'select min(shipping_price_cent), max(shipping_price_cent), avg(shipping_price_cent), sponsored, _condition from eBay_items group by sponsored, _condition;'
    cursor.execute(query)
    result = cursor.fetchall()
    print(query)
    for i in result:
        print(i)
    results.append(result)  
    
    query = 'select min(shipping_computed), max(shipping_computed), avg(shipping_computed), sponsored, _condition from eBay_items group by sponsored, _condition;'
    cursor.execute(query)
    result = cursor.fetchall()
    print(query)
    for i in result:
        print(i)
    results.append(result)  
    
    conn.commit()
    cursor.close()
    conn.close()
except IOError as e:
    print(e)    

#Result:
# select min(seller_score), max(seller_score), avg(seller_score), sponsored, _condition from eBay_items group by sponsored, _condition;
# (9, 32767, Decimal('5381.5102'), 1, 'Used')
# (10, 32767, Decimal('21848.0000'), 1, 'Seller refurbished')
# (0, 32767, Decimal('24343.5952'), 1, 'New')
# (174, 22957, Decimal('11565.5000'), 1, 'Open box')
# (1, 32767, Decimal('24577.4907'), 0, 'New')
# (0, 32767, Decimal('4154.8477'), 0, 'Used')
# (9, 32767, Decimal('14851.1111'), 0, 'Seller refurbished')
# (9, 32767, Decimal('10200.5556'), 0, 'Open box')
# (370, 1234, Decimal('802.0000'), 0, 'Manufacturer refurbi')
# (0, 32767, Decimal('5599.3529'), 0, 'For parts or not wor')
# select min(item_price_cent), max(item_price_cent), avg(item_price_cent), sponsored, _condition from eBay_items group by sponsored, _condition;
# (22900, 32767, Decimal('32147.2245'), 1, 'Used')
# (31160, 32767, Decimal('32231.3333'), 1, 'Seller refurbished')
# (32767, 32767, Decimal('32767.0000'), 1, 'New')
# (32767, 32767, Decimal('32767.0000'), 1, 'Open box')
# (1587, 32767, Decimal('32362.4018'), 0, 'New')
# (14940, 32767, Decimal('32273.9004'), 0, 'Used')
# (32205, 32767, Decimal('32704.5556'), 0, 'Seller refurbished')
# (2820, 32767, Decimal('31103.2778'), 0, 'Open box')
# (32767, 32767, Decimal('32767.0000'), 0, 'Manufacturer refurbi')
# (9999, 32767, Decimal('26307.4706'), 0, 'For parts or not wor')
# select min(best_offer_available), max(best_offer_available), avg(best_offer_available), sponsored, _condition from eBay_items group by sponsored, _condition;
# (0, 1, Decimal('0.3061'), 1, 'Used')
# (0, 0, Decimal('0.0000'), 1, 'Seller refurbished')
# (0, 1, Decimal('0.0484'), 1, 'New')
# (1, 1, Decimal('1.0000'), 1, 'Open box')
# (0, 1, Decimal('0.0203'), 0, 'New')
# (0, 1, Decimal('0.4363'), 0, 'Used')
# (0, 1, Decimal('0.2222'), 0, 'Seller refurbished')
# (0, 1, Decimal('0.3333'), 0, 'Open box')
# (0, 1, Decimal('0.5000'), 0, 'Manufacturer refurbi')
# (0, 1, Decimal('0.4706'), 0, 'For parts or not wor')
# select min(returns_allowed), max(returns_allowed), avg(returns_allowed), sponsored, _condition from eBay_items group by sponsored, _condition;
# (0, 1, Decimal('0.4082'), 1, 'Used')
# (0, 0, Decimal('0.0000'), 1, 'Seller refurbished')
# (0, 1, Decimal('0.1613'), 1, 'New')
# (0, 0, Decimal('0.0000'), 1, 'Open box')
# (0, 1, Decimal('0.2054'), 0, 'New')
# (0, 1, Decimal('0.3127'), 0, 'Used')
# (0, 0, Decimal('0.0000'), 0, 'Seller refurbished')
# (0, 1, Decimal('0.2778'), 0, 'Open box')
# (0, 0, Decimal('0.0000'), 0, 'Manufacturer refurbi')
# (0, 0, Decimal('0.0000'), 0, 'For parts or not wor')
# select min(items_sold), max(items_sold), avg(items_sold), sponsored, _condition from eBay_items group by sponsored, _condition;
# (None, None, None, 1, 'Used')
# (None, None, None, 1, 'Seller refurbished')
# (26, 77, Decimal('51.5000'), 1, 'New')
# (None, None, None, 1, 'Open box')
# (11, 2371, Decimal('274.4545'), 0, 'New')
# (60, 60, Decimal('60.0000'), 0, 'Used')
# (21, 21, Decimal('21.0000'), 0, 'Seller refurbished')
# (None, None, None, 0, 'Open box')
# (None, None, None, 0, 'Manufacturer refurbi')
# (None, None, None, 0, 'For parts or not wor')
# select min(shipping_price_cent), max(shipping_price_cent), avg(shipping_price_cent), sponsored, _condition from eBay_items group by sponsored, _condition;
# (0, 0, Decimal('0.0000'), 1, 'Used')
# (None, None, None, 1, 'Seller refurbished')
# (0, 0, Decimal('0.0000'), 1, 'New')
# (None, None, None, 1, 'Open box')
# (0, 0, Decimal('0.0000'), 0, 'New')
# (0, 0, Decimal('0.0000'), 0, 'Used')
# (0, 0, Decimal('0.0000'), 0, 'Seller refurbished')
# (0, 0, Decimal('0.0000'), 0, 'Open box')
# (None, None, None, 0, 'Manufacturer refurbi')
# (0, 0, Decimal('0.0000'), 0, 'For parts or not wor')
# select min(shipping_computed), max(shipping_computed), avg(shipping_computed), sponsored, _condition from eBay_items group by sponsored, _condition;
# (0, 1, Decimal('0.1429'), 1, 'Used')
# (0, 1, Decimal('0.6667'), 1, 'Seller refurbished')
# (0, 1, Decimal('0.7742'), 1, 'New')
# (0, 1, Decimal('0.5000'), 1, 'Open box')
# (0, 1, Decimal('0.7291'), 0, 'New')
# (0, 1, Decimal('0.2251'), 0, 'Used')
# (0, 1, Decimal('0.7778'), 0, 'Seller refurbished')
# (0, 1, Decimal('0.2778'), 0, 'Open box')
# (0, 0, Decimal('0.0000'), 0, 'Manufacturer refurbi')
# (0, 1, Decimal('0.3529'), 0, 'For parts or not wor')




# g tell what I found in f

# 1. Sponsor mean seller score is always higher than non-sponsor mean seller score
# 2. Seller score: New > Seller refurbished > Open box > Used
# 3. Not much difference in item price
# 4. Sponsored item with open box always have best offer available
# 5. Seller refurbished can not returns
# 6. More sellers of used item is allowed to return than those of New
# 7. There not much items have items sold listed
# 8. I think seller score, and (shipping_computed, returns_allowed, 
#best_offer_available) interaction with condition can be used to predict sponsor and 
#non-sponsor item.





