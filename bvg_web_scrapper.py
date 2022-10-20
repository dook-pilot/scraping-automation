import time
from unicodedata import name
from scrapy.selector import Selector
import csv
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from googletrans import Translator
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
# import chromedriver_binary


class DB_Scraping():
    count = 0
    translator = Translator()
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
    

    def target_url(self,url):
        self.start()
        self.driver.get(url)
        time.sleep(5)
    def result_scrap(self):
        for i in range(0,844): #844
            try:
                element = self.driver.find_element(by=By.XPATH, value="//a[@id='showMore']")
                self.driver.execute_script("arguments[0].click();", element)
                time.sleep(5)
            except:
                break
        self.kvk_scrap()
        
    def kvk_scrap(self):
        
        html = self.driver.page_source
        resp = Selector(text=html)
        
        data =  resp.xpath("//ul[@id='memberGridResult']/li")
        print("length",len(data))
        for dat in range(1,len(data)+1):
            dat_tags_trans = []
            company_name = resp.xpath("(//ul[@id='memberGridResult']/li//h3/strong/text())["+str(dat)+"]").extract_first()
            Street_Address = resp.xpath("(//ul[@id='memberGridResult']/li//div[contains(@class,'address')])["+str(dat)+"]/text()[1]").extract_first()
            City_Address = resp.xpath("(//ul[@id='memberGridResult']/li//div[contains(@class,'address')])["+str(dat)+"]/text()[2]").extract_first()
            Telephone = resp.xpath("(//ul[@id='memberGridResult']/li//div[contains(@class,'address')])["+str(dat)+"]/text()[3]").extract_first()
            email = resp.xpath("(//ul[@id='memberGridResult']/li//div[contains(@class,'address')])["+str(dat)+"]/text()[4]").extract_first()
            websiteurl = resp.xpath("(//ul[@id='memberGridResult']/li//div[contains(@class,'address')])["+str(dat)+"]/strong/text()").extract_first()
            tags = resp.xpath("(//ul[@id='memberGridResult']/li//h4[contains(text(),'Producten / diensten')]/parent::div)["+str(dat)+"]/span/text()").getall()
            urls = resp.xpath("(//ul[@id='memberGridResult']/li//a[@class='dealer-wrap' and contains(@href,'Leden')]/@href)["+str(dat)+"]").extract_first()
            ul = str(urls)
            ul = "https://www.bovag.nl"+ul

            for j in tags:
                j = str(j)
                try:
                    j = self.translator.translate(str(j)).text
                except:None
                dat_tags_trans.append(j)
            
            ##translatioon part
            n =0
            while n < 3:
                try:
                    company_name = self.translator.translate(str(company_name)).text
                    break
                except:
                    n = n+1

            n =0
            while n<3:
                try:
                    Street_Address = self.translator.translate(str(Street_Address)).text
                    break
                except:
                    n = n+1
            n =0
            while n<3:      
                try:
                    City_Address = self.translator.translate(str(City_Address)).text
                    break
                except:
                    n = n+1

            #ends
            with open("bovag_dataset.csv",'a',newline='',encoding='utf-8') as file:
                writer = csv.writer(file)
                if self.count == 0:
                    writer.writerow(['company_name','Street_Address','City_Address','Telephone','email','websiteurl','ul','tags'])
                writer.writerow([company_name,Street_Address,City_Address,Telephone,email,websiteurl,ul,dat_tags_trans])
            
    def exit(self):
        self.driver.quit()



if __name__ == '__main__':
    scraper = DB_Scraping()
    URL = "https://www.bovag.nl/zoek-bovag-bedrijf?l=The%20hague&d=-1&s=distance#search"
    scraper.target_url(URL)
    scraper.result_scrap()
    scraper.exit()