# -*- coding: utf-8 -*-
# !/usr/bin/env python
__author__ = 'Johannes Gontrum <gontrum@vogelschwarm.com>'

import ConfigParser  # Read configuration files
import sys

class Configuration(object):
    def __init__(self, filename):
        config = ConfigParser.RawConfigParser()
        config.read(filename)
        self.__readConfig(config)
        self.__checkValidity()
        # Maps idetifiers to their URLs
        self.URLs = {'eBay': self.urlEbayKleinanzeigen,
                     'WG1Zimmer': self.urlWGGesucht1ZimmerWohnung,
                     'WGWohnung': self.urlWGGesuchtWohnung,
                     'WohnungsBoerse': self.urlWohnungsBoerse,
                     'Immowelt': self.urlImmowelt,
                     'ImmoScout24': self.urlImmobilienScout24,
                     'Immonet': self.urlImmonet}

    def __readConfig(self, config):
        # Mail
        try:
            self.useMail = True
            self.smtpMail = config.get("E-Mail", "Address")
            self.smtpServer = config.get("E-Mail", "SMTP-Server")
            self.smtpUser = config.get("E-Mail", "SMTP-User")
            self.smtpPassword = config.get("E-Mail", "SMTP-Password")
            self.smtpRecipient = config.get("E-Mail", "Recipient")
        except:
            self.useMail = False

        # Prowl
        try:
            self.useProwl = True
            self.prowlApi = config.get("Prowl", "API")
            self.prowlPriority = config.get("Prowl", "Priority")
        except:
            self.useProwl = False

        # Log
        try:
            self.log = config.get("Config", "Logfile")
        except:
            self.log = "flatfinder.log"

        # Interval
        try:
            self.interval = int(config.get("Config", "Interval"))
        except:
            self.interval = 60

        # Blacklist
        try:
            blacklist = config.get("Config", "Blacklist")
            if len(blacklist) > 0:
                self.blacklist = blacklist.split(';')
            else:
                self.blacklist = []
        except:
            self.blacklist = []

        # URLS
        try:
            self.urlEbayKleinanzeigen = config.get("URL", "EbayKleinanzeigen")
            self.urlWGGesucht1ZimmerWohnung = config.get("URL", "WGGesucht1ZimmerWohnung")
            self.urlWGGesuchtWohnung = config.get("URL", "WGGesuchtWohnung")
            self.urlWohnungsBoerse = config.get("URL", "WohnungsBoerse")
            self.urlImmowelt = config.get("URL", "Immowelt")
            self.urlImmobilienScout24 = config.get("URL", "ImmobilienScout24")
            self.urlImmonet = config.get("URL", "Immonet")
        except:
            print "Please specify the URLs in the configuration file!"
            sys.exit(1)

    def __checkValidity(self):
        if not "kleinanzeigen.ebay.de" in self.urlEbayKleinanzeigen and len(self.urlEbayKleinanzeigen) > 0:
            print "The URL for 'eBay Kleinanzeigen' is not valid."
            self.urlEbayKleinanzeigen = ""

        if not "www.wg-gesucht.de/1-zimmer-wohnungen" in self.urlWGGesucht1ZimmerWohnung and len(self.urlWGGesucht1ZimmerWohnung) > 0:
            print "The URL for 'WG Gesucht (1-Zimmerwohnung)' is not valid."
            self.urlWGGesucht1ZimmerWohnung = ""

        if not "www.wg-gesucht.de/wohnungen" in self.urlWGGesuchtWohnung and len(self.urlWGGesuchtWohnung) > 0:
            print "The URL for 'WG Gesucht' is not valid."
            self.urlWGGesuchtWohnung = ""

        if not "www.wohnungsboerse.net" in self.urlWohnungsBoerse and len(self.urlWohnungsBoerse) > 0:
            print "The URL for 'Wohnungsboerse' is not valid."
            self.urlWohnungsBoerse = ""

        if not "www.immowelt.de" in self.urlImmowelt and len(self.urlImmowelt) > 0:
            print "The URL for 'Immowelt' is not valid."
            self.urlImmowelt = ""

        if not "www.immobilienscout24.de" in self.urlImmobilienScout24 and len(self.urlImmobilienScout24) > 0:
            print "The URL for 'ImmobilienScout24' is not valid."
            self.urlImmobilienScout24 = ""

        if not "www.immonet.de" in self.urlImmonet and len(self.urlImmonet) > 0:
            print "The URL for 'Immonet' is not valid."
            self.urlImmonet = ""
