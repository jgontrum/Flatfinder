# -*- coding: utf-8 -*-
# !/usr/bin/env python
__author__ = 'Johannes Gontrum <gontrum@vogelschwarm.com>'

import sys
import time
from Configuration import Configuration
from email.mime.text import MIMEText
from email.header import Header
import smtplib
import WebsiteParser
# import prowlpy  # Optional for iOS push messages

# Global variables
conf = None
prowl = None
smtpSender = None
counter = 0
starttime = ""

# Sends an email to the configured recipient.
def sendMail(subject, message):
    global smtpSender
    try:
        msg = MIMEText(message, _charset="UTF-8")
        msg['To'] = conf.smtpRecipient
        msg['From'] = conf.smtpMail
        msg['Subject'] = Header(subject, "utf-8")

        # Send the message via an SMTP server
        try:
            smtpSender.ehlo()
            smtpSender.starttls()
            smtpSender.ehlo()
            smtpSender.login(conf.smtpUser, conf.smtpPassword)
            smtpSender.sendmail(conf.smtpMail, conf.smtpRecipient, msg.as_string())
        except:
            smtpSender = smtplib.SMTP(conf.smtpServer)
            smtpSender.ehlo()
            smtpSender.starttls()
            smtpSender.ehlo()
            smtpSender.login(conf.smtpUser, conf.smtpPassword)
            smtpSender.sendmail(conf.smtpMail, conf.smtpRecipient, msg.as_string())
    except smtplib.SMTPDataError as e:
        print("Error sending email: " + str(e))
    except Exception as e:
        print("Sending email fails for unknown reasons. (" + str(e) + ")")

# DEPRECATED: Sends a message to an iOS device via Prowl
def sendProwl(subject, message, url):
    global prowl
    try:
        prowl.add(subject, message, conf.prowlPriority, None, url)
    except Exception as e:
        print("Sending Prowl message fails for unknown reasons. (" + str(e) + ")")

# Creates a message from an offer and sends emails etc
def notify(offer):
    global counter
    counter += 1
    subject = "Flatfinder found a new flat in " + offer['location']
    message =   "Description:\t" + offer['title'] + "\n" \
              + "Rent:          \t" + offer['rent'] + "\n" \
              + "Location:   \t" + offer['location'] + ".\n" \
              + "Found at:   \t" + offer['time'] + "\n" \
              + "URL:        \t" + offer['url'] + "\n"

    meta = "\n-----------------\n" + \
           "Flatfinder started on " + starttime + " and found " + str(counter) + " ads since."

    if conf.useMail:
        sendMail(subject, message + meta)
    if conf.useProwl:
        sendProwl(subject, message, offer['url'])
    print(subject)

# Checks weather the offer is okay
def checkBlacklist(offer):
    for blackword in conf.blacklist:
        if blackword in offer['location'].lower(): return False
        if blackword in offer['title'].lower(): return False
    return True

# Converts the given text to unicode
def makeUnicode(text):
    if not isinstance(text, str):
        return text.decode('utf-8')
    return text

# Converts a whole offer object to unicode
def makeOfferUnicode(offer):
    uoffer = {}
    for key, value in offer.items():
        uoffer[key] = makeUnicode(value)
    return uoffer

# Initialize variables
def init():
    global starttime
    global conf
    global prowl
    global smtpSender
    # Read configuration file
    if len(sys.argv) != 2:
        print("Try to use 'flatfinder.config' as default configuration file...")
        try:
            conf = Configuration("flatfinder.config")
        except Exception as e:
            print("Loading 'flatfinder.config' failed (" + str(e) + "), leaving now!")
            sys.exit(1)
    else:
        print("Try to use '" + sys.argv[1] + "' as configuration file...")
        try:
            conf = Configuration(sys.argv[1])
        except Exception as e:
            print("Loading '" + sys.argv[1] + "' failed (" + str(e) + "), leaving now!")
            sys.exit(1)

    # Initialize the messaging protocols
    # if conf.useProwl:
    #    prowl = prowlpy.Prowl(conf.prowlApi)
    if conf.useMail:
        try:
            smtpSender = smtplib.SMTP(conf.smtpServer)
            smtpSender.ehlo()
            smtpSender.starttls()
            smtpSender.ehlo()
            smtpSender.login(conf.smtpUser, conf.smtpPassword)
            smtpSender.quit()
        except Exception as e:
            print("Failed to connect to mailserver: " + str(e) + ".\nLeaving now!")
            sys.exit(1)

    # Convert the blacklist to unicode
    if len(conf.blacklist) > 0:
        ublacklist = []
        for item in conf.blacklist:
            ublacklist.append(makeUnicode(item).lower())
        conf.blacklist = ublacklist

    starttime = time.strftime("%A, %e. %B at %H:%M")

# The main loop that never stops. NEVER!
def loop():
    # Dict to save the last seen URL.
    latestURL = dict(conf.URLs)
    for id in latestURL.keys():
        latestURL[id] = None

    while True:
        for site, url in conf.URLs.items():
            if len(url) > 0:
                offer = WebsiteParser.parse(site, url)
                if offer['url'] != latestURL[site]:
                    latestURL[site] = offer['url']
                    offer = makeOfferUnicode(offer)
                    if checkBlacklist(offer):
                        notify(offer)
        time.sleep(conf.interval)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
if __name__ == '__main__':
    init()
    loop()
