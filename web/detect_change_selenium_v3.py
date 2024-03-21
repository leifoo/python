#!/usr/bin/env python3
import re
import argparse
import configparser
import datetime
from datetime import timedelta
import difflib
import hashlib
# import html2text
import logging
import smtplib, ssl
import time
from urllib.request import Request, urlopen
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent

n_top = 5

class UrlChange:
    """ URL is checked and a hash is made. Changes are regcognized and
    reported
    """

    def __init__(self, url, interval, timeEnd, showdiff, sendemail, stop):
        self.url = url
        self.interval = interval
        self.timeEnd = timeEnd
        self.showdiff = showdiff
        self.sendemail = sendemail
        self.stop = stop

        # print(self.url)
        self.driver = self.create_driver()

        # try:
        #     element = WebDriverWait(self.driver, 2).until(
        #         EC.presence_of_element_located((By.CLASS_NAME, 'result-price'))
        #     )
        #     print(element.text)
        # finally:
        #     self.driver.quit()

        # self.url_hash = self.create_hash()
        # logger.debug("url_hash")
        # self.driver.implicitly_wait(3) # gives an implicit wait for 20 seconds

        time.sleep(5)
        self.content = self.get_content()
        # print(type(self.content))

        # # self.driver.implicitly_wait(10) # gives an implicit wait for 20 seconds
        price = self.driver.find_elements(By.CLASS_NAME, 'result-price')
        # print([x.text for x in price][:10])
        logger.info(f"Start Monitoring {url}")
        price_lowest = [tuple(map(int, re.split('\n\$|\$|\n|\ ', x.text.lstrip('\$').replace(',', '')))) for x in price][:n_top]
        discount = [str(p[1]-p[0]) for p in price_lowest]
        discount = ',  '.join(discount)
        discount = '[ ' + discount + ']'
        print(f'    Price:    {[p[0] for p in price_lowest]}')
        print(f'    Discount: {discount}')
        print(f'    MSRP:     {[price[1] for price in price_lowest]} \n')

        logger.debug("content")

        # logger.info(("Start Monitoring... hash "
        #             "{url_hash}").format(url_hash=self.url_hash))

    def get_content(self):
        """ The data is read from the url. """
        try:
            # driver.get(self.url)
            price = self.driver.find_elements(By.CLASS_NAME, 'result-price')
            # print(len(price))
            # print([tuple(map(int, re.split('\n\$|\$|\n|\ ', x.text.lstrip('\$').replace(',', '')))) for x in price][:10])
            return [tuple(map(int, re.split('\n\$|\$|\n|\ ', x.text.lstrip('\$').replace(',', '')))) for x in price][:n_top]
            # url_data = driver.page_source

            # price = WebDriverWait(driver, 10).until(
            #         EC.presence_of_element_located((By.CLASS_NAME, 'result-price'))
            #         )
            # print(price)

            # return True #url_data

            # driver.implicitly_wait(3) # gives an implicit wait for 20 seconds
            # return self.driver.find_element(By.CLASS_NAME, 'result-price').text.split()

            # try:
            #     price = WebDriverWait(driver, 10).until(
            #         EC.presence_of_element_located((By.CLASS_NAME, 'result-price'))
            #     )

            #     price = self.driver.find_elements(By.CLASS_NAME, 'result-price')
            #     # print([x.text for x in price][:10])
            #     # print([tuple(map(int, re.split('\n\$|\$|\n|\ ', x.text.lstrip('\$').replace(',', '')))) for x in price][:10])
            #     return [tuple(map(int, re.split('\n\$|\$|\n|\ ', x.text.lstrip('\$').replace(',', '')))) for x in price][:10]
            # finally:
            #     driver.quit()
            # print(self.driver.find_element(By.CLASS_NAME, 'result-price').text)
            # return self.driver.find_element(By.CLASS_NAME, 'result-purchase-price').text
        except Exception as e:
            self.driver.quit()
            logger.critical("Error: {}".format(e))
            raise
        
    def create_driver(self):
        """ Create driver
        """
        try:
            options = Options()
            options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1200")

            driver = webdriver.Chrome(options=options)
            # driver.implicitly_wait(10)
            driver.get(self.url)
            return driver
        except Exception as e:
            logger.critical("Error: {}".format(e))
            raise

    def create_hash(self):
        """ The data is read from the url.
        A md5 hash is created from the url_data. 
        """
        try:
            options = Options()
            options.headless = True
            options.add_argument("--window-size=1920,1200")

            url_data = self.get_content()

            return url_data

        except Exception as e:
            logger.critical("Error: {}".format(e))
            raise

    def compare_hash(self):
        """ The hash is compared with the stored value. If there is a change
        a function is opend witch alerts the user.
        """

        if datetime.datetime.now() > self.timeEnd:
            print(f'Reach time limt, stop monitoring...')
            self.driver.quit()
            return True

        # print(self.driver.find_element(By.ID, 'clock').text)
        # print(self.get_content(self.driver) == self.url_hash)
        self.driver.refresh()
        time.sleep(self.interval)
        # print(f'self.get_content(), self.content: \
        #                {self.get_content()}, {self.content}')
        content_curr = self.get_content()

        if not content_curr:
            logger.info("Website is not responding...")
        elif content_curr == self.content:
            print(f'  {datetime.datetime.now().strftime("%y/%m/%d %H:%M:%S")} No change...', end="\r", flush=True)
        else:
            logger.info("Change detected!!!")
            if self.sendemail:
                # print("Something changed!")
                send_mail(f"[Price Tracker] {self.url} has changed!", 
                          f"{self.url} \nOld: {self.content} \nNew: {content_curr}")
            
            if self.showdiff:
                print(f'Old: {self.content}')
                print(f'New: {content_curr}')

            if self.stop:
                self.driver.quit()
                return True
            
            self.content = list(content_curr)
        
        return False

    def diff(self):
        """ The function tries to extract the changed part of the url content.
        """
        result = ["", ""]
        new_content = self.get_content()
        s = difflib.SequenceMatcher(None, self.content, new_content)
        for tag, i1, i2, j1, j2 in s.get_opcodes():
            if tag != "equal":    
            # if tag == "insert" or tag == "replace":    
                result[0] += self.content[i1-9:i2+1].strip()
                result[1] += new_content[j1-9:j2+1].strip()
        return result


def send_mail(subject, message):
    """ A connection to the smtp server is build. A mail is sent. """
    try:
        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        sender_email = "dealalert001@gmail.com"  # Enter your address
        receiver_email = "wemva001@outlook.com".replace(' ', '').replace(',', ';').split(';') # Enter receiver address
        password = 'rmql ltma plbm kzsn'

        date = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        msg = (f"From: {sender_email}\nSubject: {subject}\nDate: {date}\n"
        f"\n{message}")

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg)
            server.quit()
            logging.info("email was sent")

    except Exception as e:
            logger.critical("Error: {}".format(e))
            raise

if __name__ == "__main__":
    # Arguments from the console are parsed
    parser = argparse.ArgumentParser(
                                    description=("Monitor if a website"
                                                "has changed.")
                                    )
    parser.add_argument("url", help="url that should be monitored")
    parser.add_argument("-i", "--interval",
                        help="seconds between checks (default: 30)",
                        default=30, type=int)
    parser.add_argument("-d", "--duration",
                        help="total monitoring hours (default: 7)",
                        default=168, type=float)
    parser.add_argument("-sd", "--diff", help="show difference",
                        action="store_false")
    parser.add_argument("-e", "--email", help="no email is sent",
                        action="store_false")
    parser.add_argument("-s", "--stop", help="stop monitoring when change is detected",
                        action="store_true")
    args = parser.parse_args()

    # A new logging object is created
    logging.basicConfig(format="%(asctime)s %(message)s",
                        datefmt="%d.%m.%Y %H:%M:%S")
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # # Parse the configuration file
    # config = configparser.ConfigParser()
    # try:
    #     config.read("config.conf")
    #     if("SMTP" not in config):
    #         raise ValueError("Can't find smtp data in config.conf")
    # except Exception as e:
    #     logger.critical("Error: {}".format(e))
    #     raise

    timeEnd = datetime.datetime.now() + timedelta(hours=args.duration)

    # print(f'args.url: {args.url}\n')
    print('\n' + '-'*48)
    print(f'    Check interval:   {args.interval} seconds \n\
    Monitor duration: {args.duration} hours \n\
    Ending time:      {timeEnd.strftime("%Y/%m/%d %H:%M:%S")} \n\
    Show difference:  {args.diff} \n\
    Send email:       {args.email} \n\
    Stop when detect: {args.stop}')
    print('-'*48 + '\n')

    # Main part
    url1 = UrlChange(args.url, args.interval, timeEnd, args.diff, args.email, args.stop)
    
    # time.sleep(args.time)
    while(True):
        if(url1.compare_hash()):
            # print(f'4. args.time: {args.time}')
            break
        # time.sleep(args.time)