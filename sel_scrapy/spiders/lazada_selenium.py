import scrapy
from scrapy.utils.project import get_project_settings
from selenium import webdriver
import time
from sel_scrapy.items import LaptopItem
import requests
import telegram
import socket
import os
TELEGRAM_BOT_TOKEN = '5257428717:AAEJf0oswu-p_Y7w2JJoKh946mmlmyf0uYs'
TELEGRAM_CHAT_ID = '1003940708'


class LazadaSeleniumSpider(scrapy.Spider):
    name = 'lazada_sel'
    
    def start_requests(self):
        settings = get_project_settings()
        driver_path = 'chromedriver.exe'
        # driver_path = settings['CHROME_DRIVER_PATH']
        options = webdriver.ChromeOptions()
        options.add_argument('--window-size=1920,1080')
        options.headless = True
        driver = webdriver.Chrome(driver_path, options=options)
        driver.maximize_window()
        with open("urllist.txt") as f:
            urls = f.read().splitlines()        
        # with open("urllist.txt") as file_in:
        #     urls = []
        #     for line in file_in:
        #         urls.append(line)        
        # urls = ['https://vuaapp.com','https://google.com' ]
        for url in urls:
            try:
                driver.get("https://"+url)
                time.sleep(1)
                # print(driver.page_source)
                driver.get_screenshot_as_file("capture.png")
                res = requests.get("https://"+url)
                ip = socket.gethostbyname(url)
                status = res.status_code
                # link_elements = driver.find_elements_by_xpath('//div[@data-sqe="item"]//a[text()]')
                print('123123123123')
                # el = driver.find_element_by_tag_name('body')
                # el.screenshot("capture1.png")
                #get window size
                s = driver.get_window_size()
                #obtain browser height and width
                w = driver.execute_script('return document.body.parentNode.scrollWidth')
                h = driver.execute_script('return document.body.parentNode.scrollHeight')
                #set to new window size
                driver.set_window_size(w, h)
                #obtain screenshot of page within body tag
                driver.find_element_by_tag_name('body').screenshot("tutorialspoint.png")
                driver.set_window_size(s['width'], s['height'])
                # print(link_elements)
                # for link in link_elements:
                #     yield scrapy.Request(link.get_attribute('href'), callback=self.parse)
                PHOTO_PATH = 'capture.png'
                bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

                bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=url+" image "+str(status)+ " "+ip)

                bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=open(PHOTO_PATH, 'rb'))
            except:
                bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
                response = os.popen(f"ping {url}").read()
                if "Received = 4" in response:
                    print(f"UP {url} Ping Successful")
                    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=url+"Ping Successful errorrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr")

                else:
                    print(f"DOWN {url} Ping Unsuccessful")
                # ip = socket.gethostbyname(url)
                # status = res.status_code
                    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=url+"Ping Unsuccessful errorrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr")

                # bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=open(PHOTO_PATH, 'rb'))        
        driver.close()

    # def parse(self, response, **kwargs):
    #     item = LaptopItem(
    #         # name=response.css('.breadcrumb_item_anchor.breadcrumb_item_anchor_last ::text').get(),
    #         price=response.css('._3g8My- ::text').get()
    #     )

    #     yield item
