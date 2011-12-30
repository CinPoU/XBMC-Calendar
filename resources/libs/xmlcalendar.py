        
# Generate and manipulate the main calendar 

import os
import re
import sys

#For Xml Files
import xml.dom.minidom
import shutil

from xbmcaddon import Addon

__addonID__      = "script.calendar"
__settings__     = Addon(id=__addonID__)
__string__       = __settings__.getLocalizedString
__language__     = __settings__


# INITIALISATION CHEMIN RACINE
ROOTDIR = __settings__.getAddonInfo('path')
# Shared resources
BASE_RESOURCE_PATH = os.path.join( ROOTDIR, "resources" )
# append the proper platforms folder to our path, xbox is the same as win32
env = ( os.environ.get( "OS", "win32" ), "win32", )[ os.environ.get( "OS", "win32" ) == "xbox" ]
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "platform_libraries", env ) )
# append the proper libs folder to our path
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "libs" ) )

from specialpath import *

from traceback import print_exc

from googlecalendar import *

class XmlCalendar :

    def __init__(self):
        
        #Call the Google Class
        self.googleCalendar = GoogleCalendar()

        #Init script parameters for add calendar
        xmldoc = xml.dom.getDOMImplementation()
        self.xmlAddCalendarTree = xmldoc.createDocument('', 'calendars', '')         
        
        #Init the calendars xml file
        self.xmlCalendarPath = os.path.join( sys.modules[ "__main__" ].SPECIAL_SCRIPT_DATA, "calendar.xml" )
        if not os.path.isfile( self.xmlCalendarPath ):
            calendar_xml_src = os.path.join( BASE_RESOURCE_PATH, "modeles" , "calendar.xml" )
        try :
            shutil.copy2(calendar_xml_src,self.xmlCalendarPath)
        except : "Unable to write the list calendar xml file" 
        self.xmlCalendarTree = xml.dom.minidom.parse(self.xmlCalendarPath)
        self.xmlEventTree = xml.dom.minidom.parse(self.xmlCalendarPath)
        
        self.xml_accounts = self.xml_get_account()
        self.xml_calendars = self.xml_get_calendar()
        

        
    def xml_get_account (self) : 
    
        xml_accounts = []
        
        for e in self.xmlCalendarTree.firstChild.childNodes :
        
            if e.nodeType == e.ELEMENT_NODE and e.localName == "account" :
                #if e.getAttribute("type") == "Google" and e.hasChildNodes() == True :
                    xml_accounts.append(e)
        
        return xml_accounts        
        
    def xml_return_type (self) :
    
        xml_types = []
        
        for e in self.xml_accounts :
                xml_types.append(e.getAttribute("type"))
                
        xml_types = list(set(xml_types))
        return xml_types
                   
    def xml_return_account (self) :
    
        xml_accounts = []
        
        for e in self.xml_accounts :
            xml_account = {"title" : 0 , "type" : 0 , "login" : 0 , "password" : 0}
            
            xml_account["title"] = e.getAttribute("title")
            xml_account["type"] = e.getAttribute("type")
            xml_account["login"] = e.getAttribute("login")
            xml_account["password"] = e.getAttribute("password")
                
            xml_accounts.append(xml_account)
            print xml_accounts
                
        return xml_accounts
        
        
    def xml_return_account_title (self) :
        
        xml_accounts_title = []
        xml_accounts = self.xml_return_account()
        
        for e in self.xml_accounts :
        
            xml_accounts_title.append(a["title"])
                
        return xml_accounts_title
        
        
        
    def xml_get_calendar (self) :
    
        xml_accounts = []
        
        for xml_account in self.xml_accounts :
        
            xml_calendars = []                
                
            for xml_calendar in xml_account.childNodes :
    
                if xml_calendar.nodeType == xml_calendar.ELEMENT_NODE and xml_calendar.localName == "calendar" :
                                        
                    xml_calendars.append(xml_calendar)
                    
            xml_accounts.append(xml_calendars)
                                        
        return xml_accounts
        
    
    def xml_return_calendar (self) :
    
        xml_accounts = []
        
        for xml_account_num,xml_account in enumerate(self.xml_calendars) :
        
            xml_calendars = []
                
                
            for xml_calendar in xml_account :
            
                xml_calendarInfo = {"title" : 0 , "color" : 0 , "id" : 0 , "activate" : 0 , "accesslevel" : 0, "type" : 0}
            
                xml_calendarInfo["title"] = xml_calendar.getAttribute("title")
                xml_calendarInfo["color"] = xml_calendar.getAttribute("color")
                xml_calendarInfo["id"] = xml_calendar.getAttribute("id")
                xml_calendarInfo["activate"] = xml_calendar.getAttribute("activate")
                xml_calendarInfo["accesslevel"] = xml_calendar.getAttribute("accesslevel")
                xml_calendarInfo["type"] = self.xml_accounts[xml_account_num].getAttribute("type")
                
                xml_calendars.append(xml_calendarInfo)
                        
            xml_accounts.append(xml_calendars)
            print xml_accounts
                                        
        return xml_accounts
    
    def xml_activate_calendar(self, accountNum , calendarNum, force = False) :
                        
        c = self.xml_calendars[accountNum][calendarNum]
        
        if c.getAttribute("activate") == "true" or force == True :
            c.setAttribute("activate" , "false")
        else :
            c.setAttribute("activate" , "true")

        print "activateChild"
    
        outputfile = open(self.xmlCalendarPath, 'wb')
        self.xmlCalendarTree.writexml(writer=outputfile , indent="" , addindent="" , newl="" , encoding="UTF-8")
        outputfile.close()
    
    def xml_update_calendar(self, accountNum , calendarNum, title, color) :
                        
        c = self.xml_calendars[accountNum][calendarNum]
        c.setAttribute("title" , title)
        c.setAttribute("color" , color)

        print "updateChild"
    
        outputfile = open(self.xmlCalendarPath, 'wb')
        self.xmlCalendarTree.writexml(writer=outputfile , indent="" , addindent="" , newl="" , encoding="UTF-8")
        outputfile.close()
    
    def xml_update_account(self, accountNum , title, login, password) :
    
        print title, login, password
                        
        a = self.xml_accounts[accountNum]
        a.setAttribute("title" , title)
        a.setAttribute("login" , login)
        a.setAttribute("password" , password)

        print "updateChild"
    
        outputfile = open(self.xmlCalendarPath, 'wb')
        self.xmlCalendarTree.writexml(writer=outputfile , indent="" , addindent="" , newl="" , encoding="UTF-8")
        outputfile.close()
    
    def xml_remove_calendar(self, accountNum , calendarNum) :
    
        self.xml_accounts[accountNum].removeChild(self.xml_calendars[accountNum][calendarNum])

        print "removeChild"
    
        outputfile = open(self.xmlCalendarPath, 'wb')
        self.xmlCalendarTree.writexml(writer=outputfile , indent="" , addindent="" , newl="" , encoding="UTF-8")
        outputfile.close()
    
    def xml_remove_account(self, accountNum) :
    
        self.xmlCalendarTree.firstChild.removeChild(self.xml_accounts[accountNum])
        print self.xmlCalendarTree.firstChild.toprettyxml()

        print "removeChild"
    
        outputfile = open(self.xmlCalendarPath, 'wb')
        self.xmlCalendarTree.writexml(writer=outputfile , indent="" , addindent="" , newl="" , encoding="UTF-8")
        outputfile.close()
        
        
    def xml_add_account(self, title, type, login, pwd): 
        
        #read the calendars list xml
        xml_list_account = self.xmlCalendarTree
        accounts = self.xmlCalendarTree.firstChild
        
        # Create a main <account> element
        xml_account = xml_list_account.createElement("account")
        
        xml_account.setAttribute("title" , title)
        xml_account.setAttribute("type" , type)
        xml_account.setAttribute("login" , login)
        xml_account.setAttribute("password" , pwd)
        
        xml_accountBal = accounts.appendChild(xml_account)
        
        
        outputfile = open(self.xmlCalendarPath, 'wb')
        self.xmlCalendarTree.writexml(writer=outputfile , indent="" , addindent="" , newl="" , encoding="UTF-8")
        outputfile.close()
        
        
    def xml_add_calendar(self, type, title, color, id, accesslevel="true", login="", password=""): 
        
        #writable = "true" 
        if type == "Web" :
            writable = "false"
        
        for e in self.xmlCalendarTree.firstChild.childNodes :
        
            if e.nodeType == e.ELEMENT_NODE and e.localName == "account" and e.hasAttribute("type") :
            
                if e.getAttribute("type") == type :
                
                    if type == "Google":
                        if e.getAttribute("login") == login:
                            nodeTest = True
                        else :
                            nodeTest = False
                    else :
                            nodeTest = True
                    
                    if nodeTest == True :
                        # Create a main <calendar> element
                        xml_calendar = self.xmlCalendarTree.createElement("calendar")
                        
                        xml_calendar.setAttribute("title" , title)
                        xml_calendar.setAttribute("color" , color)
                        xml_calendar.setAttribute("accesslevel" , accesslevel)
                        xml_calendar.setAttribute("activate" , "true")
                        xml_calendar.setAttribute("id" , id)
                        
                        e.appendChild(xml_calendar) 
                    
                        outputfile = open(self.xmlCalendarPath, 'wb')
                        self.xmlCalendarTree.writexml(writer=outputfile , indent="" , addindent="" , newl="" , encoding="UTF-8")
                        outputfile.close()
                    
        return True
        
        
    def xml_add_google_calendar(self, type, title, color, login, url, writable): 
        
        for e in self.xmlCalendarTree.firstChild.childNodes :
        
            if e.nodeType == e.ELEMENT_NODE and e.localName == "account" and e.hasAttribute("login") :
            
                if e.getAttribute("login") == login :
        
                    
                    
                    # Create a main <calendar> element
                    xml_calendar = self.xmlCalendarTree.createElement("calendar")
                    xml_calendarBal = e.appendChild(xml_calendar)
                    
                    
                    # Create the calendar <title> element
                    xml_title = self.xmlCalendarTree.createElement("title")
                    xml_titleBal = xml_calendarBal.appendChild(xml_title)
                    
                    # Give the <title> element some text
                    xml_titletext = self.xmlCalendarTree.createTextNode(title)
                    xml_titleBal.appendChild(xml_titletext)
                    
                    
                    # Create the calendar <color> element
                    xml_color = self.xmlCalendarTree.createElement("color")
                    xml_colorBal = xml_calendarBal.appendChild(xml_color)
                    
                    # Give the <color> element some text
                    xml_colortext = self.xmlCalendarTree.createTextNode(color)
                    xml_colorBal.appendChild(xml_colortext)
                    
                    
                    # Create the calendar <url> element
                    xml_url = self.xmlCalendarTree.createElement("url")
                    xml_urlBal = xml_calendarBal.appendChild(xml_url)
                    
                    # Give the <write> element some text
                    xml_urltext = self.xmlCalendarTree.createTextNode(url)
                    xml_urlBal.appendChild(xml_urltext) 
                    
                    
                    # Create the calendar <visible> element
                    xml_visible = self.xmlCalendarTree.createElement("activate")
                    xml_visibleBal = xml_calendarBal.appendChild(xml_visible)
                    
                    # Give the <visible> element some text
                    xml_visibletext = self.xmlCalendarTree.createTextNode("true")
                    xml_visibleBal.appendChild(xml_visibletext) 
                    
                    
                    # Create the calendar <write> element
                    xml_write = self.xmlCalendarTree.createElement("write")
                    xml_writeBal = xml_calendarBal.appendChild(xml_write)
                    
                    # Give the <write> element some text
                    xml_writetext = self.xmlCalendarTree.createTextNode(writable)
                    xml_writeBal.appendChild(xml_writetext)  
                
                    outputfile = open(self.xmlCalendarPath, 'wb')
                    self.xmlCalendarTree.writexml(writer=outputfile , indent="" , addindent="" , newl="" , encoding="UTF-8")
                    outputfile.close()
                
