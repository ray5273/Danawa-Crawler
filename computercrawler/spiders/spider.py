# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 11:23:18 2020

@author: sammy310
"""

import scrapy
#from scrapy.spiders import Spider
from computercrawler.items import ComputercrawlerItem
from scrapy.selector import Selector

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#import time
import datetime
from datetime import timedelta
import csv


SAVETIME = 9

class cpu_Spider(scrapy.Spider):
    name = "cpucrawler"
    allowed_domains = ["www.danawa.com"]
    
    chrome_option = webdriver.ChromeOptions()
    chrome_option.add_argument('--headless')
    chrome_option.add_argument('--window-size=1920,1080');
    chrome_option.add_argument('--start-maximized');
    chrome_option.add_argument('--disable-gpu')
    chrome_option.add_argument('lang=ko=KR')
    
    
    def __init__(self):
        self.siteURL = 'http://prod.danawa.com/list/?cate=112747'
        #self.browser = webdriver.Chrome("chromedriver.exe")
        self.browser = webdriver.Chrome("chromedriver", chrome_options=self.chrome_option)
        file = open('ComputerCrawlerFile.csv','a', newline='')
        csvWriter = csv.writer(file)
        csvWriter.writerow(["---", "CPU"])
        csvWriter.writerow([(datetime.datetime.now() + timedelta(hours=SAVETIME)).strftime('%Y-%m-%d %H:%M:%S')])
        file.close()
        
        file = open('cpu_data.csv','a', newline='')
        csvWriter = csv.writer(file)
        csvWriter.writerow([(datetime.datetime.now() + timedelta(hours=SAVETIME)).strftime('%Y-%m-%d %H:%M:%S')])
        file.close()

    def start_requests(self):
        yield scrapy.Request(self.siteURL ,self.parse)

    def parse(self, response):
        self.browser.implicitly_wait(2)
        self.browser.get(self.siteURL)
        
        self.browser.find_element_by_xpath('//option[@value="90"]').click()
        
        wait = WebDriverWait(self.browser,5)
        wait.until(EC.invisibility_of_element((By.CLASS_NAME, 'product_list_cover')))
        
        for i in range(-1, 2):
            if i == -1:
                self.browser.find_element_by_xpath('//li[@data-sort-method="NEW"]').click()
            elif i == 0:
                self.browser.find_element_by_xpath('//li[@data-sort-method="BEST"]').click()
            elif i > 0:
                self.browser.find_element_by_xpath('//a[@class="num "][%d]'%i).click()
            wait.until(EC.invisibility_of_element((By.CLASS_NAME, 'product_list_cover')))
            
            html = self.browser.find_element_by_xpath('//div[@class="main_prodlist main_prodlist_list"]').get_attribute('outerHTML')
            selector = Selector(text=html)
            
            productIds = selector.xpath('//li[@class="prod_item prod_layer "]/@id').getall()
            productNames = selector.xpath('//a[@name="productName"]/text()').getall()
            productPriceList = selector.xpath('//div[@class="prod_pricelist"]/ul')
            
            adCounter = 0
            errCounter = 0
            for j in range(len(productIds)) :
                item = ComputercrawlerItem()
                item['productId'] = productIds[j][11:]
                item['productName'] = productNames[j].strip()
                
                bNotAd = False
                priceStr = ""
                while not bNotAd:
                    pList = productPriceList[j+adCounter+errCounter].xpath('li')
                    if pList[0].xpath('@class').get() == "opt_item":
                        adCounter += 1
                        bNotAd = False
                        continue
                    else:
                        if not pList[0].xpath('div').get():
                            errCounter += 1
                            continue
                        bNotAd = True
                    
                    for k in range(len(pList)):
                        for pStr in pList[k].xpath('div/p/text()').getall():
                            if bool(pStr.strip()):
                                priceStr += ''.join(pStr.strip().split(' '))
                        priceStr += '_'
                        priceStr += pList[k].xpath('p[2]/a/strong/text()').get()
                        priceStr += ' '
                    
                    
                item['productPrice'] = priceStr
                yield item
                
            
        self.browser.close()


class ram_Spider(scrapy.Spider):
    name = "ramcrawler"
    allowed_domains = ["www.danawa.com"]
    
    chrome_option = webdriver.ChromeOptions()
    chrome_option.add_argument('--headless')
    chrome_option.add_argument('--window-size=1920,1080');
    chrome_option.add_argument('--start-maximized');
    chrome_option.add_argument('--disable-gpu')
    chrome_option.add_argument('lang=ko=KR')
    
    def __init__(self):
        self.siteURL = 'http://prod.danawa.com/list/?cate=112752'
        self.browser = webdriver.Chrome("chromedriver", chrome_options=self.chrome_option)
        file = open('ComputerCrawlerFile.csv','a', newline='')
        csvWriter = csv.writer(file)
        csvWriter.writerow(["---", "RAM"])
        csvWriter.writerow([(datetime.datetime.now() + timedelta(hours=SAVETIME)).strftime('%Y-%m-%d %H:%M:%S')])
        file.close()
        
        file = open('ram_data.csv','a', newline='')
        csvWriter = csv.writer(file)
        csvWriter.writerow([(datetime.datetime.now() + timedelta(hours=SAVETIME)).strftime('%Y-%m-%d %H:%M:%S')])
        file.close()
        

    def start_requests(self):
        yield scrapy.Request(self.siteURL ,self.parse)

    def parse(self, response):
        self.browser.implicitly_wait(2)
        self.browser.get(self.siteURL)
        
        self.browser.find_element_by_xpath('//option[@value="90"]').click()

        wait = WebDriverWait(self.browser,5)
        wait.until(EC.invisibility_of_element((By.CLASS_NAME, 'product_list_cover')))
        
        for i in range(-1, 10):
            if i == -1:
                self.browser.find_element_by_xpath('//li[@data-sort-method="NEW"]').click()
            elif i == 0:
                self.browser.find_element_by_xpath('//li[@data-sort-method="BEST"]').click()
            elif i > 0:
                if i % 10 == 0:
                    self.browser.find_element_by_xpath('//a[@class="edge_nav nav_next"]').click()
                else:
                    self.browser.find_element_by_xpath('//a[@class="num "][%d]'%(i%10)).click()
            wait.until(EC.invisibility_of_element((By.CLASS_NAME, 'product_list_cover')))
            
            html = self.browser.find_element_by_xpath('//div[@class="main_prodlist main_prodlist_list"]').get_attribute('outerHTML')
            selector = Selector(text=html)
            
            productIds = selector.xpath('//li[@class="prod_item prod_layer "]/@id').getall()
            productNames = selector.xpath('//a[@name="productName"]/text()').getall()
            productPriceList = selector.xpath('//div[@class="prod_pricelist"]/ul')
            
            adCounter = 0
            errCounter = 0
            for j in range(len(productIds)) :
                item = ComputercrawlerItem()
                item['productId'] = productIds[j][11:]
                item['productName'] = productNames[j].strip()
                
                bNotAd = False
                priceStr = ""
                while not bNotAd:
                    pList = productPriceList[j+adCounter+errCounter].xpath('li')
                    if pList[0].xpath('@class').get() == "opt_item":
                        adCounter += 1
                        bNotAd = False
                        continue
                    else:
                        if not pList[0].xpath('div').get():
                            errCounter += 1
                            continue
                        bNotAd = True
                    
                    for k in range(len(pList)):
                        for pStr in pList[k].xpath('div/p/text()').getall():
                            if bool(pStr.strip()):
                                priceStr += pStr.strip()
                        priceStr += '_'
                        if pList[k].xpath('div/p/a/span/text()').get():
                            priceStr += pList[k].xpath('div/p/a/span/text()').get()
                        elif pList[k].xpath('div/p/a/span/em/text()').get():
                            priceStr += pList[k].xpath('div/p/a/span/em/text()').get()
                        else:
                            priceStr += "---"
                        priceStr += '_'
                        priceStr += pList[k].xpath('p[2]/a/strong/text()').get()
                        priceStr += ' '
                    
                    
                item['productPrice'] = priceStr
                yield item
            
        self.browser.close()
        
        
class vga_Spider(scrapy.Spider):
    name = "vgacrawler"
    allowed_domains = ["www.danawa.com"]
    
    chrome_option = webdriver.ChromeOptions()
    chrome_option.add_argument('--headless')
    chrome_option.add_argument('--window-size=1920,1080');
    chrome_option.add_argument('--start-maximized');
    chrome_option.add_argument('--disable-gpu')
    chrome_option.add_argument('lang=ko=KR')
    
    def __init__(self):
        self.siteURL = 'http://prod.danawa.com/list/?cate=112753'
        self.browser = webdriver.Chrome("chromedriver", chrome_options=self.chrome_option)
        file = open('ComputerCrawlerFile.csv','a', newline='')
        csvWriter = csv.writer(file)
        csvWriter.writerow(["---", "VGA"])
        csvWriter.writerow([(datetime.datetime.now() + timedelta(hours=SAVETIME)).strftime('%Y-%m-%d %H:%M:%S')])
        file.close()
        
        file = open('vga_data.csv','a', newline='')
        csvWriter = csv.writer(file)
        csvWriter.writerow([(datetime.datetime.now() + timedelta(hours=SAVETIME)).strftime('%Y-%m-%d %H:%M:%S')])
        file.close()

    def start_requests(self):
        yield scrapy.Request(self.siteURL ,self.parse)

    def parse(self, response):
        self.browser.implicitly_wait(2)
        self.browser.get(self.siteURL)
        
        self.browser.find_element_by_xpath('//option[@value="90"]').click()

        wait = WebDriverWait(self.browser,5)
        wait.until(EC.invisibility_of_element((By.CLASS_NAME, 'product_list_cover')))
        
        for i in range(-1, 10):
            if i == -1:
                self.browser.find_element_by_xpath('//li[@data-sort-method="NEW"]').click()
            elif i == 0:
                self.browser.find_element_by_xpath('//li[@data-sort-method="BEST"]').click()
            elif i > 0:
                if i % 10 == 0:
                    self.browser.find_element_by_xpath('//a[@class="edge_nav nav_next"]').click()
                else:
                    self.browser.find_element_by_xpath('//a[@class="num "][%d]'%(i%10)).click()
            wait.until(EC.invisibility_of_element((By.CLASS_NAME, 'product_list_cover')))
        
            html = self.browser.find_element_by_xpath('//div[@class="main_prodlist main_prodlist_list"]').get_attribute('outerHTML')
            selector = Selector(text=html)
            
            productIds = selector.xpath('//li[@class="prod_item prod_layer width_change"]/@id').getall()
            productNames = selector.xpath('//a[@name="productName"]/text()').getall()
            productPriceList = selector.xpath('//div[@class="prod_pricelist"]/ul')
            
            adCounter = 0
            errCounter = 0
            for j in range(len(productIds)) :
                item = ComputercrawlerItem()
                item['productId'] = productIds[j][11:]
                item['productName'] = productNames[j].strip()
                
                bNotAd = False
                while not bNotAd:
                    pList = productPriceList[j+adCounter+errCounter].xpath('li')
                    if pList[0].xpath('@class').get() == "opt_item":
                        adCounter += 1
                        bNotAd = False
                        continue
                    else:
                        item['productPrice'] = pList[0].xpath('p[2]/a/strong/text()').get()
                        if not item['productPrice']:
                            errCounter += 1
                            continue
                        bNotAd = True
                        
                yield item
            
        self.browser.close()

        
class mboard_Spider(scrapy.Spider):
    name = "mboardcrawler"
    allowed_domains = ["www.danawa.com"]
    
    chrome_option = webdriver.ChromeOptions()
    chrome_option.add_argument('--headless')
    chrome_option.add_argument('--window-size=1920,1080');
    chrome_option.add_argument('--start-maximized');
    chrome_option.add_argument('--disable-gpu')
    chrome_option.add_argument('lang=ko=KR')
    
    def __init__(self):
        self.siteURL = 'http://prod.danawa.com/list/?cate=112751'
        self.browser = webdriver.Chrome("chromedriver", chrome_options=self.chrome_option)
        file = open('ComputerCrawlerFile.csv','a', newline='')
        csvWriter = csv.writer(file)
        csvWriter.writerow(["---", "MBoard"])
        csvWriter.writerow([(datetime.datetime.now() + timedelta(hours=SAVETIME)).strftime('%Y-%m-%d %H:%M:%S')])
        file.close()
        
        file = open('mboard_data.csv','a', newline='')
        csvWriter = csv.writer(file)
        csvWriter.writerow([(datetime.datetime.now() + timedelta(hours=SAVETIME)).strftime('%Y-%m-%d %H:%M:%S')])
        file.close()

    def start_requests(self):
        yield scrapy.Request(self.siteURL ,self.parse)

    def parse(self, response):
        self.browser.implicitly_wait(2)
        self.browser.get(self.siteURL)
        
        self.browser.find_element_by_xpath('//option[@value="90"]').click()

        wait = WebDriverWait(self.browser,5)
        wait.until(EC.invisibility_of_element((By.CLASS_NAME, 'product_list_cover')))
        
        for i in range(-1, 10):
            if i == -1:
                self.browser.find_element_by_xpath('//li[@data-sort-method="NEW"]').click()
            elif i == 0:
                self.browser.find_element_by_xpath('//li[@data-sort-method="BEST"]').click()
            elif i > 0:
                if i % 10 == 0:
                    self.browser.find_element_by_xpath('//a[@class="edge_nav nav_next"]').click()
                else:
                    self.browser.find_element_by_xpath('//a[@class="num "][%d]'%(i%10)).click()
            wait.until(EC.invisibility_of_element((By.CLASS_NAME, 'product_list_cover')))
            
            html = self.browser.find_element_by_xpath('//div[@class="main_prodlist main_prodlist_list"]').get_attribute('outerHTML')
            selector = Selector(text=html)
            
            productIds = selector.xpath('//li[@class="prod_item prod_layer width_change"]/@id').getall()
            productNames = selector.xpath('//a[@name="productName"]/text()').getall()
            productPriceList = selector.xpath('//div[@class="prod_pricelist"]/ul')
            
            adCounter = 0
            errCounter = 0
            for j in range(len(productIds)) :
                item = ComputercrawlerItem()
                item['productId'] = productIds[j][11:]
                item['productName'] = productNames[j].strip()
                
                bNotAd = False
                while not bNotAd:
                    pList = productPriceList[j+adCounter+errCounter].xpath('li')
                    if pList[0].xpath('@class').get() == "opt_item":
                        adCounter += 1
                        bNotAd = False
                        continue
                    else:
                        item['productPrice'] = pList[0].xpath('p[2]/a/strong/text()').get()
                        if not item['productPrice']:
                            errCounter += 1
                            continue
                        bNotAd = True
                        
                yield item
            
        self.browser.close()

        
class ssd_Spider(scrapy.Spider):
    name = "ssdcrawler"
    allowed_domains = ["www.danawa.com"]
    
    chrome_option = webdriver.ChromeOptions()
    chrome_option.add_argument('--headless')
    chrome_option.add_argument('--window-size=1920,1080');
    chrome_option.add_argument('--start-maximized');
    chrome_option.add_argument('--disable-gpu')
    chrome_option.add_argument('lang=ko=KR')
    
    def __init__(self):
        self.siteURL = 'http://prod.danawa.com/list/?cate=112760'
        self.browser = webdriver.Chrome("chromedriver", chrome_options=self.chrome_option)
        file = open('ComputerCrawlerFile.csv','a', newline='')
        csvWriter = csv.writer(file)
        csvWriter.writerow(["---", "SSD"])
        csvWriter.writerow([(datetime.datetime.now() + timedelta(hours=SAVETIME)).strftime('%Y-%m-%d %H:%M:%S')])
        file.close()
        
        file = open('ssd_data.csv','a', newline='')
        csvWriter = csv.writer(file)
        csvWriter.writerow([(datetime.datetime.now() + timedelta(hours=SAVETIME)).strftime('%Y-%m-%d %H:%M:%S')])
        file.close()

    def start_requests(self):
        yield scrapy.Request(self.siteURL ,self.parse)

    def parse(self, response):
        self.browser.implicitly_wait(2)
        self.browser.get(self.siteURL)
        
        self.browser.find_element_by_xpath('//option[@value="90"]').click()

        wait = WebDriverWait(self.browser,5)
        wait.until(EC.invisibility_of_element((By.CLASS_NAME, 'product_list_cover')))
        
        for i in range(-1, 4):
            if i == -1:
                self.browser.find_element_by_xpath('//li[@data-sort-method="NEW"]').click()
            elif i == 0:
                self.browser.find_element_by_xpath('//li[@data-sort-method="BEST"]').click()
            elif i > 0:
                self.browser.find_element_by_xpath('//a[@class="num "][%d]'%i).click()
            wait.until(EC.invisibility_of_element((By.CLASS_NAME, 'product_list_cover')))
            
            html = self.browser.find_element_by_xpath('//div[@class="main_prodlist main_prodlist_list"]').get_attribute('outerHTML')
            selector = Selector(text=html)
            
            productIds = selector.xpath('//li[@class="prod_item prod_layer "]/@id').getall()
            productNames = selector.xpath('//a[@name="productName"]/text()').getall()
            productPriceList = selector.xpath('//div[@class="prod_pricelist"]/ul')
            
            
            adCounter = 0
            errCounter = 0
            for j in range(len(productIds)) :
                item = ComputercrawlerItem()
                item['productId'] = productIds[j][11:]
                item['productName'] = productNames[j].strip()
                
                bNotAd = False
                priceStr = ""
                while not bNotAd:
                    pList = productPriceList[j+adCounter+errCounter].xpath('li')
                    if pList[0].xpath('@class').get() == "opt_item":
                        adCounter += 1
                        bNotAd = False
                        continue
                    else:
                        if not pList[0].xpath('div').get():
                            errCounter += 1
                            continue
                        bNotAd = True
                    
                    for k in range(len(pList)):
                        for pStr in pList[k].xpath('div/p/text()').getall():
                            if bool(pStr.strip()):
                                priceStr += pStr.strip()
                        priceStr += '_'
                        if pList[k].xpath('div/p/a/span/text()').get():
                            priceStr += pList[k].xpath('div/p/a/span/text()').get()
                        elif pList[k].xpath('div/p/a/span/em/text()').get():
                            priceStr += pList[k].xpath('div/p/a/span/em/text()').get()
                        else:
                            priceStr += "---"
                        priceStr += '_'
                        priceStr += pList[k].xpath('p[2]/a/strong/text()').get()
                        priceStr += ' '
                    
                    
                item['productPrice'] = priceStr
                yield item
            
        self.browser.close()


class hdd_Spider(scrapy.Spider):
    name = "hddcrawler"
    allowed_domains = ["www.danawa.com"]
    
    chrome_option = webdriver.ChromeOptions()
    chrome_option.add_argument('--headless')
    chrome_option.add_argument('--window-size=1920,1080');
    chrome_option.add_argument('--start-maximized');
    chrome_option.add_argument('--disable-gpu')
    chrome_option.add_argument('lang=ko=KR')
    
    def __init__(self):
        self.siteURL = 'http://prod.danawa.com/list/?cate=112763'
        self.browser = webdriver.Chrome("chromedriver", chrome_options=self.chrome_option)
        file = open('ComputerCrawlerFile.csv','a', newline='')
        csvWriter = csv.writer(file)
        csvWriter.writerow(["---", "HDD"])
        csvWriter.writerow([(datetime.datetime.now() + timedelta(hours=SAVETIME)).strftime('%Y-%m-%d %H:%M:%S')])
        file.close()
        
        file = open('hdd_data.csv','a', newline='')
        csvWriter = csv.writer(file)
        csvWriter.writerow([(datetime.datetime.now() + timedelta(hours=SAVETIME)).strftime('%Y-%m-%d %H:%M:%S')])
        file.close()

    def start_requests(self):
        yield scrapy.Request(self.siteURL ,self.parse)

    def parse(self, response):
        self.browser.implicitly_wait(2)
        self.browser.get(self.siteURL)
        
        self.browser.find_element_by_xpath('//option[@value="90"]').click()

        wait = WebDriverWait(self.browser,5)
        wait.until(EC.invisibility_of_element((By.CLASS_NAME, 'product_list_cover')))
        
        for i in range(-1, 2):
            if i == -1:
                self.browser.find_element_by_xpath('//li[@data-sort-method="NEW"]').click()
            elif i == 0:
                self.browser.find_element_by_xpath('//li[@data-sort-method="BEST"]').click()
            elif i > 0:
                self.browser.find_element_by_xpath('//a[@class="num "][%d]'%i).click()
            wait.until(EC.invisibility_of_element((By.CLASS_NAME, 'product_list_cover')))
            
            html = self.browser.find_element_by_xpath('//div[@class="main_prodlist main_prodlist_list"]').get_attribute('outerHTML')
            selector = Selector(text=html)
            
            productIds = selector.xpath('//li[@class="prod_item prod_layer "]/@id').getall()
            productNames = selector.xpath('//a[@name="productName"]/text()').getall()
            productPriceList = selector.xpath('//div[@class="prod_pricelist"]/ul')
            
            
            adCounter = 0
            errCounter = 0
            for j in range(len(productIds)) :
                item = ComputercrawlerItem()
                item['productId'] = productIds[j][11:]
                item['productName'] = productNames[j].strip()
                
                bNotAd = False
                priceStr = ""
                while not bNotAd:
                    pList = productPriceList[j+adCounter+errCounter].xpath('li')
                    if pList[0].xpath('@class').get() == "opt_item":
                        adCounter += 1
                        bNotAd = False
                        continue
                    else:
                        if not pList[0].xpath('div').get():
                            errCounter += 1
                            continue
                        bNotAd = True
                    
                    for k in range(len(pList)):
                        for pStr in pList[k].xpath('div/p/text()').getall():
                            if bool(pStr.strip()):
                                priceStr += pStr.strip()
                        priceStr += '_'
                        if pList[k].xpath('div/p/a/span/text()').get():
                            priceStr += pList[k].xpath('div/p/a/span/text()').get()
                        elif pList[k].xpath('div/p/a/span/em/text()').get():
                            priceStr += pList[k].xpath('div/p/a/span/em/text()').get()
                        else:
                            priceStr += "---"
                        priceStr += '_'
                        priceStr += pList[k].xpath('p[2]/a/strong/text()').get()
                        priceStr += ' '
                    
                    
                item['productPrice'] = priceStr
                yield item
            
        self.browser.close()

        
class power_Spider(scrapy.Spider):
    name = "powercrawler"
    allowed_domains = ["www.danawa.com"]
    
    chrome_option = webdriver.ChromeOptions()
    chrome_option.add_argument('--headless')
    chrome_option.add_argument('--window-size=1920,1080');
    chrome_option.add_argument('--start-maximized');
    chrome_option.add_argument('--disable-gpu')
    chrome_option.add_argument('lang=ko=KR')
    
    def __init__(self):
        self.siteURL = 'http://prod.danawa.com/list/?cate=112777'
        self.browser = webdriver.Chrome("chromedriver", chrome_options=self.chrome_option)
        file = open('ComputerCrawlerFile.csv','a', newline='')
        csvWriter = csv.writer(file)
        csvWriter.writerow(["---", "Power"])
        csvWriter.writerow([(datetime.datetime.now() + timedelta(hours=SAVETIME)).strftime('%Y-%m-%d %H:%M:%S')])
        file.close()
        
        file = open('power_data.csv','a', newline='')
        csvWriter = csv.writer(file)
        csvWriter.writerow([(datetime.datetime.now() + timedelta(hours=SAVETIME)).strftime('%Y-%m-%d %H:%M:%S')])
        file.close()

    def start_requests(self):
        yield scrapy.Request(self.siteURL ,self.parse)
 
    def parse(self, response):
        self.browser.implicitly_wait(2)
        self.browser.get(self.siteURL)
        
        self.browser.find_element_by_xpath('//option[@value="90"]').click()
        
        wait = WebDriverWait(self.browser,5)
        wait.until(EC.invisibility_of_element((By.CLASS_NAME, 'product_list_cover')))
        
        for i in range(-1, 6):
            if i == -1:
                self.browser.find_element_by_xpath('//li[@data-sort-method="NEW"]').click()
            elif i == 0:
                self.browser.find_element_by_xpath('//li[@data-sort-method="BEST"]').click()
            elif i > 0:
                self.browser.find_element_by_xpath('//a[@class="num "][%d]'%i).click()
            wait.until(EC.invisibility_of_element((By.CLASS_NAME, 'product_list_cover')))
            
            html = self.browser.find_element_by_xpath('//div[@class="main_prodlist main_prodlist_list"]').get_attribute('outerHTML')
            selector = Selector(text=html)
            
            productIds = selector.xpath('//li[@class="prod_item prod_layer width_change"]/@id').getall()
            productNames = selector.xpath('//a[@name="productName"]/text()').getall()
            productPriceList = selector.xpath('//div[@class="prod_pricelist"]/ul')
            
            adCounter = 0
            errCounter = 0
            for j in range(len(productIds)) :
                item = ComputercrawlerItem()
                item['productId'] = productIds[j][11:]
                item['productName'] = productNames[j].strip()
                
                bNotAd = False
                while not bNotAd:
                    pList = productPriceList[j+adCounter+errCounter].xpath('li')
                    if pList[0].xpath('@class').get() == "opt_item":
                        adCounter += 1
                        bNotAd = False
                        continue
                    else:
                        item['productPrice'] = pList[0].xpath('p[2]/a/strong/text()').get()
                        if not item['productPrice']:
                            errCounter += 1
                            continue
                        bNotAd = True
                        
                yield item
            
        self.browser.close()

       
class cooler_Spider(scrapy.Spider):
    name = "coolercrawler"
    allowed_domains = ["www.danawa.com"]
    
    chrome_option = webdriver.ChromeOptions()
    chrome_option.add_argument('--headless')
    chrome_option.add_argument('--window-size=1920,1080');
    chrome_option.add_argument('--start-maximized');
    chrome_option.add_argument('--disable-gpu')
    chrome_option.add_argument('lang=ko=KR')
    
    def __init__(self):
        self.siteURL = 'http://prod.danawa.com/list/?cate=11236855'
        self.browser = webdriver.Chrome("chromedriver", chrome_options=self.chrome_option)
        file = open('ComputerCrawlerFile.csv','a', newline='')
        csvWriter = csv.writer(file)
        csvWriter.writerow(["---", "Cooler"])
        csvWriter.writerow([(datetime.datetime.now() + timedelta(hours=SAVETIME)).strftime('%Y-%m-%d %H:%M:%S')])
        file.close()
        
        file = open('cooler_data.csv','a', newline='')
        csvWriter = csv.writer(file)
        csvWriter.writerow([(datetime.datetime.now() + timedelta(hours=SAVETIME)).strftime('%Y-%m-%d %H:%M:%S')])
        file.close()

    def start_requests(self):
        yield scrapy.Request(self.siteURL ,self.parse)
 
    def parse(self, response):
        self.browser.implicitly_wait(2)
        self.browser.get(self.siteURL)
        
        self.browser.find_element_by_xpath('//option[@value="90"]').click()

        wait = WebDriverWait(self.browser,5)
        wait.until(EC.invisibility_of_element((By.CLASS_NAME, 'product_list_cover')))
        
        for i in range(-1, 15):
            if i == -1:
                self.browser.find_element_by_xpath('//li[@data-sort-method="NEW"]').click()
            elif i == 0:
                self.browser.find_element_by_xpath('//li[@data-sort-method="BEST"]').click()
            elif i > 0:
                if i % 10 == 0:
                    self.browser.find_element_by_xpath('//a[@class="edge_nav nav_next"]').click()
                else:
                    self.browser.find_element_by_xpath('//a[@class="num "][%d]'%(i%10)).click()
            wait.until(EC.invisibility_of_element((By.CLASS_NAME, 'product_list_cover')))
            
            html = self.browser.find_element_by_xpath('//div[@class="main_prodlist main_prodlist_list"]').get_attribute('outerHTML')
            selector = Selector(text=html)
            
            productIds = selector.xpath('//li[@class="prod_item prod_layer "]/@id').getall()
            productNames = selector.xpath('//a[@name="productName"]/text()').getall()
            productPriceList = selector.xpath('//div[@class="prod_pricelist"]/ul')
            
            adCounter = 0
            errCounter = 0
            for j in range(len(productIds)) :
                item = ComputercrawlerItem()
                item['productId'] = productIds[j][11:]
                item['productName'] = productNames[j].strip()
                
                bNotAd = False
                while not bNotAd:
                    pList = productPriceList[j+adCounter+errCounter].xpath('li')
                    if pList[0].xpath('@class').get() == "opt_item":
                        adCounter += 1
                        bNotAd = False
                        continue
                    else:
                        item['productPrice'] = pList[0].xpath('p[2]/a/strong/text()').get()
                        if not item['productPrice']:
                            errCounter += 1
                            continue
                        bNotAd = True
                        
                yield item
            
        self.browser.close()

     
class Case_Spider(scrapy.Spider):
    name = "casecrawler"
    allowed_domains = ["www.danawa.com"]
    
    chrome_option = webdriver.ChromeOptions()
    chrome_option.add_argument('--headless')
    chrome_option.add_argument('--window-size=1920,1080');
    chrome_option.add_argument('--start-maximized');
    chrome_option.add_argument('--disable-gpu')
    chrome_option.add_argument('lang=ko=KR')
    
    def __init__(self):
        self.siteURL = 'http://prod.danawa.com/list/?cate=112775'
        self.browser = webdriver.Chrome("chromedriver", chrome_options=self.chrome_option)
        file = open('ComputerCrawlerFile.csv','a', newline='')
        csvWriter = csv.writer(file)
        csvWriter.writerow(["---", "Case"])
        csvWriter.writerow([(datetime.datetime.now() + timedelta(hours=SAVETIME)).strftime('%Y-%m-%d %H:%M:%S')])
        file.close()
        
        file = open('case_data.csv','a', newline='')
        csvWriter = csv.writer(file)
        csvWriter.writerow([(datetime.datetime.now() + timedelta(hours=SAVETIME)).strftime('%Y-%m-%d %H:%M:%S')])
        file.close()
 
    def start_requests(self):
        yield scrapy.Request(self.siteURL ,self.parse)
 
    def parse(self, response):
        self.browser.implicitly_wait(2)
        self.browser.get(self.siteURL)
        
        self.browser.find_element_by_xpath('//option[@value="90"]').click()

        wait = WebDriverWait(self.browser,5)
        wait.until(EC.invisibility_of_element((By.CLASS_NAME, 'product_list_cover')))
        
        for i in range(-1, 10):
            if i == -1:
                self.browser.find_element_by_xpath('//li[@data-sort-method="NEW"]').click()
            elif i == 0:
                self.browser.find_element_by_xpath('//li[@data-sort-method="BEST"]').click()
            elif i > 0:
                if i % 10 == 0:
                    self.browser.find_element_by_xpath('//a[@class="edge_nav nav_next"]').click()
                else:
                    self.browser.find_element_by_xpath('//a[@class="num "][%d]'%(i%10)).click()
            wait.until(EC.invisibility_of_element((By.CLASS_NAME, 'product_list_cover')))
            
            html = self.browser.find_element_by_xpath('//div[@class="main_prodlist main_prodlist_list"]').get_attribute('outerHTML')
            selector = Selector(text=html)
            
            productIds = selector.xpath('//li[@class="prod_item prod_layer "]/@id').getall()
            productNames = selector.xpath('//a[@name="productName"]/text()').getall()
            productPriceList = selector.xpath('//div[@class="prod_pricelist"]/ul')
            
            adCounter = 0
            errCounter = 0
            for j in range(len(productIds)) :
                item = ComputercrawlerItem()
                item['productId'] = productIds[j][11:]
                item['productName'] = productNames[j].strip()
                
                bNotAd = False
                while not bNotAd:
                    pList = productPriceList[j+adCounter+errCounter].xpath('li')
                    if pList[0].xpath('@class').get() == "opt_item":
                        adCounter += 1
                        bNotAd = False
                        continue
                    else:
                        item['productPrice'] = pList[0].xpath('p[2]/a/strong/text()').get()
                        if not item['productPrice']:
                            errCounter += 1
                            continue
                        bNotAd = True
                        
                yield item
            
        self.browser.close()
        
        
class Monitor_Spider(scrapy.Spider):
    name = "monitorcrawler"
    allowed_domains = ["www.danawa.com"]
    
    chrome_option = webdriver.ChromeOptions()
    chrome_option.add_argument('--headless')
    chrome_option.add_argument('--window-size=1920,1080');
    chrome_option.add_argument('--start-maximized');
    chrome_option.add_argument('--disable-gpu')
    chrome_option.add_argument('lang=ko=KR')
    
    def __init__(self):
        self.siteURL = 'http://prod.danawa.com/list/?cate=112757'
        #self.browser = webdriver.Chrome("chromedriver.exe")
        self.browser = webdriver.Chrome("chromedriver", chrome_options=self.chrome_option)
        file = open('ComputerCrawlerFile.csv','a', newline='')
        csvWriter = csv.writer(file)
        csvWriter.writerow(["---", "Monitor"])
        csvWriter.writerow([(datetime.datetime.now() + timedelta(hours=SAVETIME)).strftime('%Y-%m-%d %H:%M:%S')])
        file.close()
        
        file = open('monitor_data.csv','a', newline='')
        csvWriter = csv.writer(file)
        csvWriter.writerow([(datetime.datetime.now() + timedelta(hours=SAVETIME)).strftime('%Y-%m-%d %H:%M:%S')])
        file.close()
 
    def start_requests(self):
        yield scrapy.Request(self.siteURL ,self.parse)
 
    def parse(self, response):
        self.browser.implicitly_wait(2)
        self.browser.get(self.siteURL)
        
        self.browser.find_element_by_xpath('//option[@value="90"]').click()

        wait = WebDriverWait(self.browser,5)
        wait.until(EC.invisibility_of_element((By.CLASS_NAME, 'product_list_cover')))
        
        for i in range(-1, 20):
            if i == -1:
                self.browser.find_element_by_xpath('//li[@data-sort-method="NEW"]').click()
            elif i == 0:
                self.browser.find_element_by_xpath('//li[@data-sort-method="BEST"]').click()
            elif i > 0:
                if i % 10 == 0:
                    self.browser.find_element_by_xpath('//a[@class="edge_nav nav_next"]').click()
                else:
                    self.browser.find_element_by_xpath('//a[@class="num "][%d]'%(i%10)).click()
            wait.until(EC.invisibility_of_element((By.CLASS_NAME, 'product_list_cover')))
            
            html = self.browser.find_element_by_xpath('//div[@class="main_prodlist main_prodlist_list"]').get_attribute('outerHTML')
            selector = Selector(text=html)
            
            productIds = selector.xpath('//li[@class="prod_item prod_layer width_change"]/@id').getall()
            productNames = selector.xpath('//a[@name="productName"]/text()').getall()
            productPriceList = selector.xpath('//div[@class="prod_pricelist"]/ul')
            
            adCounter = 0
            errCounter = 0
            for j in range(len(productIds)) :
                item = ComputercrawlerItem()
                item['productId'] = productIds[j][11:]
                item['productName'] = productNames[j].strip()
                
                bNotAd = False
                while not bNotAd:
                    pList = productPriceList[j+adCounter+errCounter].xpath('li')
                    if pList[0].xpath('@class').get() == "opt_item":
                        adCounter += 1
                        bNotAd = False
                        continue
                    else:
                        item['productPrice'] = pList[0].xpath('p[2]/a/strong/text()').get()
                        if not item['productPrice']:
                            errCounter += 1
                            continue
                        bNotAd = True
                        
                yield item
            
        self.browser.close()

