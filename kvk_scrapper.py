import encodings
import time
from unicodedata import name
from scrapy.selector import Selector
import csv
import re
import pandas as pd
import datetime
import requests
import os
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
# import chromedriver_binary



class DB_Scraping():
    count = 0
    names = []

    def start(self):
        options = Options()
        options.add_experimental_option("detach", True)
        #options.binary_location = "C:/Program Files/Google/Chrome Beta/Application/chrome.exe"
        options.add_argument("--headless")
        # options.add_argument("--no-sandbox")
        # options.add_argument('--disable-gpu')

        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36')
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
    
    def check_file_exist(self):
        if os.path.exists("place_api_companies.csv"):
            
            return True
        else:
            return False


    def read_from_csv(self):
        with open("place_api_companies.csv", 'r', encoding='utf-8') as input_file:
            reader = csv.reader(input_file,delimiter=",")
            print(reader)
            for idx, ri in enumerate(reader):
                if idx > 0:
                    riw = str(ri[5])
                    self.names.append(riw)
                

    def result_scrap(self):
        if self.check_file_exist() == True:
            self.read_from_csv()
            for name in self.names:
                name_web_text = self.normalize_text(name)
                name_web_text = self.convert_space_into_web_space(name_web_text)
                print('name_web_text',name_web_text)
                kvk_url = "https://www.kvk.nl/zoeken/?source=all&q="+name_web_text+"&start=0&site=kvk2014"
                # bovag_url = "https://www.bovag.nl/zoek-bovag-bedrijf?l="+name_web_text+"&d=-1&s=distance#search"
                # google_url = "https://www.google.com/search?q="+name_web_text

                
                print(kvk_url)
                # print(bovag_url)
                # print(google_url)
                self.kvk_scrap(name,kvk_url)
                
                

        
    def normalize_text(self,line):
        line = str(line)
        line = line.replace('  ',' ')
        line = line.strip()
        return line

    def convert_space_into_web_space(self,line):
        line = str(line)
        line = line.replace(' ','%20')
        line = line.replace("'","%27")
        line = line.replace('"','%22')
        return line
        

    def normaize_list(self,text):
        text = str(text)
        text = text.replace('"','')
        text = text.replace(',','')
        text = text.replace('[','')
        text = text.replace(']','')
        text = text.replace("'","")
        text = text.replace("  "," ")
        text = text.strip()
        return text

    def kvk_scrap(self,name,kvk_url):

        self.start()
        self.driver.get(kvk_url)
        time.sleep(5)
        try:
            WebDriverWait(self.driver,10).until(EC.presence_of_element_located(
                (By.XPATH, "//h5[contains(text(),'Bestaande handelsnamen')]/following-sibling::p")))
            time.sleep(3)
        except:
            print("wait problem")
        html = self.driver.page_source
        resp = Selector(text=html)
        existing_trade_name = resp.xpath("normalize-space(//h5[contains(text(),'Bestaande handelsnamen')]/following-sibling::p[1]/text())").extract_first()
        partnership_name = resp.xpath("normalize-space(//h5[contains(text(),'Naam samenwerkingsverband')]/following-sibling::p[1]/text())").extract_first()
        chamber_of_commerce = resp.xpath("normalize-space(//ul[@class='kvk-meta']/li[contains(text(),'KVK')][1]/text())").extract_first()
        chamber_of_commerce = str(chamber_of_commerce)
        chamber_of_commerce = chamber_of_commerce.replace('KVK','')
        chamber_of_commerce = chamber_of_commerce.strip()
        establishment_no = resp.xpath("normalize-space(//ul[@class='kvk-meta']/li[contains(text(),'Vestigingsnr')][1]/text())").extract_first()
        establishment_no = str(establishment_no)
        establishment_no = establishment_no.replace('Vestigingsnr.','')
        establishment_no = establishment_no.strip()
        address = resp.xpath("//ul[@class='kvk-meta']/li[not(contains(text(),'Vestigingsnr')) and not(contains(text(),'KVK'))]/text()").getall()
        address = self.normaize_list(address)
        other = resp.xpath("//p[@class='snippet-result']//text()").getall()
        other = self.normaize_list(other)


        # compare_name = name
        # compare_name = str(compare_name)
        # compare_name = compare_name.replace('"','')
        # compare_name = compare_name.replace("'","")
        # compare_name = compare_name.replace("&","")
        # compare_name = compare_name.replace("|","")
        # compare_name = compare_name.replace("!","")
        # compare_name = compare_name.replace(".","")
        # compare_name = compare_name.replace("  "," ")
        # compare_name = compare_name.replace(" ","-")
        # compare_name = compare_name.strip()
        
        # bovag = []
        # gs_reviews = []
        # compare_name_2 = name
        # compare_name_2 = str(compare_name_2)
        # compare_name_2_xpath = "//strong[contains(text(),'"+compare_name_2+"')]/ancestor::li[1]/a/@href"
        # self.driver.get(bovag_url)
        # time.sleep(5)
        # html = self.driver.page_source
        # resp = Selector(text=html)

        # compare_name_xpath = "//li/a[contains(@href,'"+compare_name+"')]/@href"
        # detail_url = resp.xpath(compare_name_xpath).extract_first()
        # if detail_url == None or detail_url == '' or detail_url == "":  
        #     detail_url = resp.xpath(compare_name_2_xpath).extract_first()
        #     if detail_url == None or detail_url == '' or detail_url == "":
        #         None
        #     else:
        #         detail_url = "https://www.bovag.nl"+detail_url
        # else:
        #     detail_url = "https://www.bovag.nl"+detail_url

        
        # bovag_other_details = ""
        # if detail_url == None or detail_url == '' or detail_url == "":
        #         None
        # else:
        #     self.driver.get(detail_url)
        #     time.sleep(5)
        #     html = self.driver.page_source
        #     resp = Selector(text=html)
        #     bovag = resp.xpath("//div[contains(@class,'large-7 medium-6 columns padding-top-40')]/p/text()").getall()
        #     bovag_other_details = resp.xpath("//strong[contains(text(),'Contactgegevens')]/parent::h3/following-sibling::p/text()").getall()

        # self.driver.get(google_url)
        # time.sleep(5)
        # try:
        #     element = self.driver.find_element(by=By.XPATH, value="//button[contains(text(),'Alle akzeptieren')]")
        #     self.driver.execute_script("arguments[0].click();", element)
        # except:
        #     None
        # try:
        #     element = self.driver.find_element(by=By.XPATH, value="//div[contains(text(),'Alle akzeptieren')/parent::a")
        #     self.driver.execute_script("arguments[0].click();", element)
        # except:
        #     None
        # try:
        #     element = self.driver.find_element(by=By.XPATH, value="//a[contains(text(),'Alle akzeptieren')")
        #     self.driver.execute_script("arguments[0].click();", element)
        # except:
        #     None
        # html = self.driver.page_source
        # resp = Selector(text=html)
        # rating = resp.xpath("normalize-space(//span[@class='Aq14fc']/text())").extract_first()
        # try:
            
        #     element = self.driver.find_element(by=By.XPATH, value="//span[contains(text(),'Google reviews')]/parent::a")
        #     self.driver.execute_script("arguments[0].click();", element)
        #     time.sleep(3)
        #     html = self.driver.page_source
        #     resp = Selector(text=html)
        #     gs_reviews = resp.xpath("//div[@class='Jtu6Td']/span//text()").getall()  
        # except:
        #     None
            
            

        self.driver.quit()
        # gs_reviews = str(gs_reviews)
        # gs_reviews = gs_reviews.replace('[','')
        # gs_reviews = gs_reviews.replace(']','')
        # gs_reviews = gs_reviews.replace('"','')
        # gs_reviews = gs_reviews.replace("'","")
        # gs_reviews = gs_reviews.replace(',',';')
        # gs_reviews = gs_reviews.replace('More','')
        # gs_reviews = gs_reviews.replace('…;','')
        # gs_reviews = gs_reviews.strip()
        print('Search text',name)
        print('existing_trade_name',existing_trade_name)
        print('partnership_name',partnership_name)
        print('chamber_of_commerce',chamber_of_commerce)
        print('establishment_no',establishment_no)
        print('address',address)
        print('other',other)
        # print('BOVAG',bovag)
        # print('rating',rating)
        # print('Review',gs_reviews)
        # print('bovag_other_details')

        with open("kvk_scrapped_data.csv",'a',newline='',encoding='utf-8') as file:
            writer = csv.writer(file)
            if self.count == 0:
                writer.writerow(['search_text','existing_trade_name','partnership_name','chamber_of_commerce','establishment_no','address','other'])
            writer.writerow([name,existing_trade_name,partnership_name,chamber_of_commerce,establishment_no,address,other])
            self.count = self.count + 1
            print("Data saved in CSV: ",self.count)   



if __name__ == '__main__':
    scraper = DB_Scraping()
    scraper.result_scrap()