# -*- coding: utf-8 -*-
# !/usr/bin/env python
__author__ = 'Johannes Gontrum <gontrum@vogelschwarm.com>'

import sys
import time
from Configuration import Configuration
from email.mime.text import MIMEText
import smtplib
import WebsiteParser
# import prowlpy  # Optional for iOS push messages

# Global variables
conf = None
prowl = None
smtpSender = None

""" Sends an email to the configured recipient."""
def sendMail(subject, message):
    try:
        msg = MIMEText(message)
        msg['To'] = conf.smtpRecipient
        msg['From'] = conf.smtpMail
        msg['Subject'] = subject

        # Send the message via an SMTP server
        try:
            smtpSender.sendmail(conf.smtpMail, conf.smtpRecipient, msg.as_string())
        except:
            smtpSender = smtplib.SMTP(conf.smtpServer)
            smtpSender.login(conf.smtpUser, conf.smtpPassword)
            smtpSender.sendmail(conf.smtpMail, conf.smtpRecipient, msg.as_string())
    except smtplib.SMTPDataError, e:
        print "Error sending email: " + str(e)
    except Exception, e:
        print "Sending email fails for unknown reasons. (" +  str(e) +  ")"

""" Sends a message to an iOS device via Prowl."""
def sendProwl(subject, message, url):
    try:
        prowl.add(subject, message, conf.prowlPriority, None, url)
    except Exception, e:
        print "Sending Prowl message fails for unknown reasons. (" + str(e) + ")"

""" Creates a message from an offer and sends emails etc """
def notify(offer):
    print(offer)
    pass

""" Converts the given text to unicode """
def makeUnicode(text):
    return text.decode('utf-8')

""" Initialize variables """
def init():
    """ Read configuration file """
    if len(sys.argv) != 2:
        print "Try to use 'flatfinder.config' as default configuration file..."
        try:
            configuration = Configuration("flatfinder.config")
        except Exception, e:
            print "Loading 'flatfinder.config' failed (" + str(e) + "), leaving now!"
            sys.exit(1)
    else:
        print "Try to use '" + sys.argv[1] + "' as configuration file..."
        try:
            configuration = Configuration(sys.argv[1])
        except Exception, e:
            print "Loading '" + sys.argv[1] + "' failed (" + str(e) + "), leaving now!"
            sys.exit(1)

    """ Initialize the messaging protocols
    if configuration.useProwl:
        prowl = prowlpy.Prowl(configuration.prowlApi)
    if configuration.useMail:
        try:
            smtpSender = smtplib.SMTP(configuration.smtpServer)
            smtpSender.login(configuration.smtpUser, configuration.smtpPassword)
        except Exception, e:
            print "Failed to connect to mailserver: " + str(e) + ".\nLeaving now!"
            sys.exit(1)
    """
    """ Convert the blacklist to unicode """
    if len(configuration.blacklist) > 0:
        ublacklist = []
        for item in configuration.blacklist:
            ublacklist.append(makeUnicode(item))
        configuration.blacklist = ublacklist
    return configuration

""" The main loop that never stops. NEVER! """
def loop():
    # Dict to save the last seen URL.
    latestURL = dict(conf.URLs)
    for id in latestURL.keys():
        latestURL[id] = None

    while True:
        print "Checking again..."
        for site, url in conf.URLs.items():
            if len(url) > 0:
                offer = WebsiteParser.parse(site, url)
                if offer['url'] != latestURL[site]:
                    latestURL[site] = offer['url']
                    notify(offer)
        time.sleep(conf.interval)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
if __name__ == '__main__':
    conf = init()
    loop()














