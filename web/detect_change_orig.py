#!/usr/bin/env python3
import argparse
import configparser
import datetime
import difflib
import hashlib
import html2text
import logging
import smtplib
import time
import urllib.request

# https://codereview.stackexchange.com/questions/120208/email-a-notification-when-detecting-changes-on-a-website-follow-up

class UrlChange:
    """ URL is checked and a hash is made. Changes are regcognized and
    reported
    """

    def __init__(self, url):
        self.url = url
        self.url_hash = self.create_hash()
        self.content = self.get_content()
        logger.info(("Start Monitoring... hash "
                    "{url_hash}").format(url_hash=self.url_hash))

    def get_content(self):
        """ The data is read from the url. """
        try:
            url_data = urllib.request.urlopen(self.url)
            url_data = url_data.read()
            url_data = url_data.decode("utf-8", "ignore")
            url_data = html2text.html2text(url_data)
        except Exception as e:
            logger.critical("Error: {}".format(e))
            raise
        return url_data

    def create_hash(self):
        """ A md5 hash is created from the url_data. """
        url_data = self.get_content().encode("utf-8")
        md5_hash = hashlib.md5()
        md5_hash.update(url_data)
        return md5_hash.hexdigest()

    def compare_hash(self):
        """ The hash is compared with the stored value. If there is a change
        a function is opend witch alerts the user.
        """
        if(self.create_hash() == self.url_hash):
            logger.info("Nothing has changed")
            return False
        else:
            logger.info("Something has changed")
            date = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            if(not args.nomail):
                send_mail("Url has changed!",
                        ("The Url {url} has changed at "
                        "{date} .").format(url=self.url, date=date))
            if(not args.nodiff):
                diff = self.diff()
                logger.info("{diff}".format(**locals()))
                if(not args.nomail):
                    diff.encode("ascii", "ignore")
                    send_mail("Url difference!",
                            ("The Url {url} has changed at {date} ."
                            "\n\nNew content\n{diff}").format(url=self.url,
                                                                date=date,
                                                                diff=diff))
            return True

    def diff(self):
        """ The function tries to extract the changed part of the url content.
        """
        result = ""
        new_content = self.get_content()
        s = difflib.SequenceMatcher(None, self.content, new_content)
        for tag, i1, i2, j1, j2 in s.get_opcodes():
            if(tag == "insert" or tag == "replaced"):
                result += new_content[j1:j2]
        return result


def send_mail(subject, message):
    """ A connection to the smtp server is build. A mail is sent. """
    try:
        smtp_url = config["SMTP"]["url"]
        smtp_port = config["SMTP"]["port"]
        smtp_user = config["SMTP"]["user"]
        smtp_password = config["SMTP"]["password"]
        destination = config["SMTP"]["destination"]

        server = smtplib.SMTP(smtp_url, smtp_port)
        server.set_debuglevel(0)
        server.ehlo()
        server.starttls()
        server.login(smtp_user, smtp_password)
    except Exception as e:
            logger.critical("Error: {}".format(e))
            raise

    date = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    msg = ("From: {source}\nSubject: {subject}\nDate: {date}\n"
        "\n{message}").format(source=smtp_user, subject=subject, date=date,
                                message=message)

    server.sendmail(smtp_user, destination, msg)
    server.quit()
    logging.info("email was sent")

# Arguments from the console are parsed
parser = argparse.ArgumentParser(
                                description=("Monitor ifa website"
                                            "has changed.")
                                )
parser.add_argument("url", help="url that should be monitored")
parser.add_argument("-t", "--time",
                    help="seconds between checks (default: 600)",
                    default=600, type=int)
parser.add_argument("-nd", "--nodiff", help="show no difference",
                    action="store_true")
parser.add_argument("-n", "--nomail", help="no email is sent",
                    action="store_true")
args = parser.parse_args()

# A new logging object is created
logging.basicConfig(format="%(asctime)s %(message)s",
                    datefmt="%d.%m.%Y %H:%M:%S")
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Parse the configuration file
config = configparser.ConfigParser()
try:
    config.read("config.conf")
    if("SMTP" not in config):
        raise ValueError("Can't find smtp data in config.conf")
except Exception as e:
    logger.critical("Error: {}".format(e))
    raise

# Main part
url1 = UrlChange(args.url)
time.sleep(args.time)
while(True):
    if(url1.compare_hash()):
        break
    time.sleep(args.time)