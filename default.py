# -*- coding: utf-8 -*-
"""This script can show and read calendars from the web (http), from a local file, or from Google Calendar service"""


import os
import re
import sys
import xbmc, xbmcgui
from xbmcaddon import Addon

# script constants
__script__       = "Calendar"
__plugin__       = "Calendar"
__author__       = "CinPoU"
__credits__      = ""
__platform__     = "xbmc media center, [LINUX, OS X, WIN32, XBOX]"
__date__         = "30-12-2011"
__version__      = "1.5"
__addonID__      = "script.calendar"
__settings__     = Addon(id=__addonID__)
__string__       = __settings__.getLocalizedString
__language__     = __settings__



# INITIALISATION CHEMIN RACINE
ROOTDIR = __settings__.getAddonInfo('path')

#module to test url
from urllib2 import Request, urlopen

# Shared resources
BASE_RESOURCE_PATH = os.path.join( ROOTDIR, "resources" )
# append the proper platforms folder to our path, xbox is the same as win32
env = ( os.environ.get( "OS", "win32" ), "win32", )[ os.environ.get( "OS", "win32" ) == "xbox" ]
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "platform_libraries", env ) )
# append the proper libs folder to our path
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "libs" ) )
# append the proper GUI folder to our path
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "libs", "GUI" ) )
# append the proper xml folder to our path
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "libs", "xml" ) )
# append the proper gdata folder to our path
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "libs", "gdata" ) )
# append the proper atom folder to our path
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "libs", "atom" ) )


#modules custom
from specialpath import *
from maincalendar import *
from xmlcalendar import *
from googlecalendar import *
from icscalendar import *
import MyFont
xbmc.executebuiltin( "Skin.Reset(TabSettings)" )
xbmc.executebuiltin( "Skin.SetString(TabSettings,1)" )
xbmc.executebuiltin( "Skin.SetString(showcalendar,0)" )
xbmc.executebuiltin( "Skin.SetString(modEvent,0)" )
xbmc.executebuiltin( "Skin.SetString(scriptbackground,WP-Events.jpg)" )
#Add Fonts
try:  
  MyFont.addFont( "calendar45caps_title" , "calendarTitleCaps.ttf" , "45")
  MyFont.addFont( "calendar30caps_title" , "calendarTitleCaps.ttf" , "30")
  MyFont.addFont( "calendar25caps_title" , "calendarTitleCaps.ttf" , "25")
  MyFont.addFont( "calendar12_title" , "calendarTitle.ttf" , "12")
  MyFont.addFont( "calendar16" , "calendarDefaultCaps.ttf" , "16")
  MyFont.addFont( "calendar15" , "calendarDefaultCaps.ttf" , "15")
  MyFont.addFont( "calendar14" , "calendarDefaultCaps.ttf" , "14")
  MyFont.addFont( "calendar12" , "calendarDefaultCaps.ttf" , "12")
  MyFont.addFont( "calendar10" , "calendarDefaultCaps.ttf" , "10")

except :
    pass



#get actioncodes from keymap.xml
ACTION_PREVIOUS_MENU = 10
ACTION_PARENT_DIR = 9



class AgendaGUI(xbmcgui.WindowXML):
    """The main Calendar GUI"""

    def __init__(self,strXMLname, strFallbackPath, strDefaultName ):
        # Changing the three varibles passed won't change, anything
        # Doing strXMLname = "bah.xml" will not change anything.
        # don't put GUI sensitive stuff here (as the xml hasn't been read yet
        # Idea to initialize your variables here
        pass
 
    def onInit(self):
    
        #Language :
        self.Language = __language__
    
        self.pDialog = xbmcgui.DialogProgress()
        self.pDialog.create(self.Language.getLocalizedString(30))
        self.pDialog.update(0)
        # Put your List Populating code/ and GUI startup stuff here
        self.calendarMonthViewList = self.getControl(150)
        self.daysname = self.getControl(250)
        self.monthname = self.getControl(602)
        self.calendar_list = self.getControl(8901)
        
        #Events list
        self.eventsListTitle = self.getControl(8800)
        self.eventsListGUI = self.getControl(8801)
        
        
        #Init button id
        self.calendarList = 8901
        self.dayNameList = 250
        self.btn_next = 130
        self.btn_prev = 131 
        self.btn_refresh = 1 
        self.btn_exit = 4 
        
        self.calendarMonthView = 150
        
        self.addcalendar_btn_title = 9001
        self.addcalendar_btn_decrease_color = 9021
        self.addcalendar_btn_increase_color = 9022
        self.addcalendar_btn_label_color = 9023
        self.addcalendar_btn_image_color = 9024
        self.addcalendar_btn_decrease_type = 9031
        self.addcalendar_btn_increase_type = 9032
        self.addcalendar_btn_label_type = 9033
        self.addcalendar_btn_group_account = 9004
        self.addcalendar_btn_decrease_account = 9042
        self.addcalendar_btn_increase_account = 9043
        self.addcalendar_btn_label_account = 9044
        self.addcalendar_btn_add_account = 9005
        self.addcalendar_btn_group_calendar = 9006
        self.addcalendar_btn_decrease_calendar = 9061
        self.addcalendar_btn_increase_calendar = 9062
        self.addcalendar_btn_label_calendar = 9063
        self.addcalendar_btn_add_calendar = 9064
        self.addcalendar_btn_url = 9009
        self.addcalendar_btn_ok = 9010 
        self.addevent_btn_decrease_calendar = 8711
        self.addevent_btn_increase_calendar = 8712
        self.addevent_btn_label_calendar = 8713
        self.addevent_btn_title = 8702
        self.addevent_btn_start = 8703
        self.addevent_btn_end = 8704
        self.addevent_btn_option = 8705
        self.addevent_btn_ok = 8706
        self.addevent_btn_delete = 8707
        self.modEvent_List = 8801
        self.addEvent_menu = 90202
        self.modCalendar_title = 9101
        self.modCalendar_decrease_color = 9121
        self.modCalendar_increase_color = 9122
        self.modCalendar_label_color = 9123
        self.modCalendar_image_color = 9124
        self.modCalendar_show_unstar = 91310
        self.modCalendar_show_star = 91311
        self.modCalendar_delete = 9132
        self.modCalendar_update_account = 9133
        self.modCalendar_update = 9134
        self.modAccount_title = 9201
        self.modAccount_login = 9202
        self.modAccount_password = 9203
        self.modCalendar_validate_account = 9240
        self.modCalendar_delete_account = 9241
        self.returnTabSettings = 0
        
        
        #Init Language string
        self.monthNameTitle = [0,self.Language.getLocalizedString(101),self.Language.getLocalizedString(102),self.Language.getLocalizedString(103),self.Language.getLocalizedString(104),self.Language.getLocalizedString(105),self.Language.getLocalizedString(106),self.Language.getLocalizedString(107),self.Language.getLocalizedString(108),self.Language.getLocalizedString(109),self.Language.getLocalizedString(110),self.Language.getLocalizedString(111),self.Language.getLocalizedString(112)]
        self.dayAbbr = [self.Language.getLocalizedString(131),self.Language.getLocalizedString(132),self.Language.getLocalizedString(133),self.Language.getLocalizedString(134),self.Language.getLocalizedString(135),self.Language.getLocalizedString(136),self.Language.getLocalizedString(137)]
        self.dayName = [self.Language.getLocalizedString(121),self.Language.getLocalizedString(122),self.Language.getLocalizedString(123),self.Language.getLocalizedString(124),self.Language.getLocalizedString(125),self.Language.getLocalizedString(126),self.Language.getLocalizedString(127)]    
        self.colorName = [self.Language.getLocalizedString(141),self.Language.getLocalizedString(142),self.Language.getLocalizedString(143),self.Language.getLocalizedString(144),self.Language.getLocalizedString(145),self.Language.getLocalizedString(146),self.Language.getLocalizedString(147),self.Language.getLocalizedString(148),self.Language.getLocalizedString(149),self.Language.getLocalizedString(150),self.Language.getLocalizedString(151)]        
        
        
        self.pDialog.update(20)
        
        ##Display the Day's Name 
        #Check the settings for first week day
        settings = __settings__
        firstWeekDay = settings.getSetting("fwday")
        
        if firstWeekDay == "true" :
            firstweekday = 6
        else :
            firstweekday = 0
            
   
        for x in xrange(0,7):
          dn = firstweekday + x
          if dn > 6 :
              dn = dn - 7
          self.daysname.addItem( xbmcgui.ListItem( self.dayAbbr[ dn ] ) )
        
        self.pDialog.update(40)
        
        #Call the XML Class
        self.XmlCalendar = None
        #Accounts and Calendar Info
        self.calendarsInfo = None
        self.accountsInfo = None
        #Populate the View Calendar List
        self.view_calendars()
        
        #Call the Agenda Class
        self.calendar = Agenda()
        #Days in the calendar
        self.dayList = self.calendar.set_container_days()
        #Events date range
        self.eventsDateRange = self.calendar.get_event_time_range()
        
        self.pDialog.update(60)
        
        #Call the Google Class
        self.googleCalendar = GoogleCalendar()
        #Events in the Google Calendars
        print self.accountsInfo, self.calendarsInfo, self.eventsDateRange["start"], self.eventsDateRange["end"]
        self.eventsGoogle = self.googleCalendar.DateRangeQuery(self.accountsInfo, self.calendarsInfo, self.eventsDateRange["start"], self.eventsDateRange["end"])
        
        #Call the Ics Class
        #Init the tempdir path
        self.tempDir = os.path.join( sys.modules[ "__main__" ].SPECIAL_TEMP_DIR, "calendar" )
        if not os.path.isfile( self.tempDir ):
            try :
                os.mkdir(self.tempDir)
            except : "Unable to create the temp directory" 
        self.icsCalendar = IcsCalendar()
        self.eventsIcs = self.icsCalendar.DateRangeQuery(self.accountsInfo, self.calendarsInfo, self.eventsDateRange["start"], self.eventsDateRange["end"],self.tempDir)
        
        self.pDialog.update(80)
        
        #Init color var
        self.calendarColor = [{'name' : 'Red' , 'color' : 'FFA32929'} , {'name' : 'Pink' , 'color' : 'FFB1365F'} , {'name' : 'Violet' , 'color' : 'FF7A367A'} , {'name' : 'Purple' , 'color' : 'FF5229A3'} , {'name' : 'Navy' , 'color' : 'FF29527A'} , {'name' : 'Blue' , 'color' : 'FF2952A3'} , {'name' : 'Cyan' , 'color' : 'FF1B887A'} , {'name' : 'Green' , 'color' : 'FF0D7813'} , {'name' : 'Lime' , 'color' : 'FF528800'} , {'name' : 'Orange' , 'color' : 'FFBE6D00'} , {'name' : 'Marron' , 'color' : 'FF8D6F47'}]

        #Populate the Calendar
        self.populate_calendar()
        #Populate the list events
        self.dayEvents = []
        self.returnListEvents()
        #Init button visibility
        self.getControl(self.addcalendar_btn_group_account).setVisible(False)
        self.getControl(self.addcalendar_btn_group_calendar).setVisible(False)
        self.getControl(self.addcalendar_btn_url).setVisible(True)
        #Init url var
        self.addCalendarUrl = 0
        
        
        #Init color var
        self.calendarColorId = ['Red' , 'Pink' , 'Violet' , 'Purple' , 'Navy' , 'Blue' , 'Cyan' , 'Green' , 'Lime' , 'Orange' , 'Marron']
        self.addCalendar_CurrentColor = 0
        self.decrease_button (self.colorName, 1, self.addcalendar_btn_label_color, self.Language.getLocalizedString(1221))
        color = "color-%s.png" % (self.calendarColor[int(self.addCalendar_CurrentColor)]['name'])
        self.getControl( self.addcalendar_btn_image_color).setImage(color)
        #Init account type var
        self.CalendarAccountType = ["Local" , "Web" , "Google"]
        self.addCalendar_CurrentType = 0 
        self.decrease_button (self.CalendarAccountType, 1, self.addcalendar_btn_label_type, self.Language.getLocalizedString(1222))
        #Init Add Calendar - account title var
        self.addCalendar_CurrentAccount = 0
        self.addCalendar_GoogleAccount = []
        self.addCalendar_GoogleAccountInfo = []
        self.addCalendar_CurrentCalendar = 0
        self.addCalendar_GoogleCalendar = []
        self.addCalendar_GoogleCalendarInfo = []
        #Init Add Calendar - Get google info 
        self.returnGoogleInfoTitle()
        #Init Add Calendar - Populate Google title for account and calendar
        if not self.addCalendar_GoogleAccount == [] :
            self.decrease_button (self.addCalendar_GoogleAccount, 1,  self.addcalendar_btn_label_account, self.Language.getLocalizedString(1224))
        if not self.addCalendar_GoogleCalendar == [] and self.addCalendar_GoogleCalendar[self.addCalendar_CurrentAccount] != [] :
            self.decrease_button (self.addCalendar_GoogleCalendar[self.addCalendar_CurrentAccount], 1,  self.addcalendar_btn_label_calendar, self.Language.getLocalizedString(1225))
        #Init Add Event - calendar title var
        self.addEventTitle = ""
        self.addEventLocation = ""
        self.addEventComment = ""
        self.addEvent_CurrentCalendar = 0
        self.addEventStartDate = ""
        self.addEventStartTime = ""
        self.addEventStopDate = ""
        self.addEventStopTime = ""
        self.addEventAllday = 0
        self.addEventRecurrence = 0
        self.addEventRecurDate = "00000000" 
        self.addEventUrl = None
        self.modEventRecurrence = False
        self.addEventCalendar = {}
        #Init Add Event - Populate calendars title
        if self.addEvent_CalendarsTitle != [] :
            self.decrease_button (self.addEvent_CalendarsTitle, 1,  self.addevent_btn_label_calendar, self.Language.getLocalizedString(1230))
        #Init Mod Calendar
        self.modCalendar_calendarId = 0
        self.modCalendar_accountId = 0
        self.modCalendar_Title = ""
        self.modCalendar_CurrentColor = 0

        self.pDialog.update(100)
        
        self.pDialog.close()
        
        xbmc.executebuiltin( "Skin.SetString(showcalendar,2)" )
        self.setFocusId(150)
    
    
    def isInteger(self , x , y = 0) :
        try :
            return int(x,y)
        except :
            return "Error"
    
    def return_Write_Calendars(self,xml_return_account,xml_return_calendar) :
        
        addEventCalendars = []
        addEventCalendarsTitle = []
        for i , a in enumerate(xml_return_account) :
            if a['type'] == "Google" :
                account_calendars_title = []
                
                for c in xml_return_calendar[i] :
                    if c['accesslevel'] == "owner" :
                        c['login'] = a['login']
                        c['password'] = a['password']
                        addEventCalendars.append(c)
                        addEventCalendarsTitle.append(c['title'])
                
        return addEventCalendarsTitle, addEventCalendars
                    
                
    def populate_calendar(self) :
        """Add all the days of the selected month in the main calendar"""
        
        item_pos = 0
        today_pos = 0
        
        #Display the current month name
        month_num, month_year = self.calendar.get_month_parm()
        month_text = '%s %s' % (self.monthNameTitle[month_num].encode('utf-8').upper(), month_year)
        self.monthname.setLabel(month_text)
        
        #Init the events
        #month_events = ReadEvents().findMonthEvts(self.dayList, self.calendarsInfo)
        for item_pos, day in enumerate(self.dayList) :
            
            if day['type'] == "previous" :
                dayColor = "ccbbbbbb"
                path = "special://skin/media/button-Back.png"
            if day['type'] == "next" :
                dayColor = "ccbbbbbb"
                path = "special://skin/media/button-Back.png"
            if day['type'] == "current" :
                dayColor = "ffffffff"
                path = "special://skin/media/button-Back.png"
            if day['type'] == "today" :
                dayColor = "ff000000"
                path = "special://skin/media/button-Back.png"
                
                
            ## Add the days to the list
            
            #text color
            label_colored = "[COLOR=%s]%i[/COLOR]" % ( dayColor, day['number'] )
            
            #create Listitem
            listitem = xbmcgui.ListItem( label_colored )
            
            #Check today case
            if day['type'] ==  "today" :
                listitem.setProperty( "today", "True" )
                
            # Get Event for the day
            day_code = '%04d-%02d-%02d' % (day['year'],day['month'],day['number'])
            for eventNumber, eventInfo in enumerate(self.eventsGoogle + self.eventsIcs) :            
                if eventInfo['startdate'] == day_code:
                    listitem.setProperty( "event", "True" )
            
            #Add day information
            listitem.setProperty( "date", day_code )
                    
            #Add the listitem to the list    
            dayItem = self.calendarMonthViewList.addItem( listitem )
            
            #Autoselect today day    
            if day['type'] ==  "today" :
              today_pos = item_pos
              
        self.calendarMonthViewList.selectItem(today_pos)
            
                    
    def show_keyboard (self, textDefault, textHead, textHide=False) :
        """Show the keyboard's dialog"""
        keyboard = xbmc.Keyboard(textDefault, textHead)
        inputText = ""
        if textHide == True :
            keyboard.setHiddenInput(True)
        keyboard.doModal()
        if (keyboard.isConfirmed()):
            inputText = keyboard.getText()         
            dialogInfo = xbmcgui.Dialog()
        del keyboard
        return inputText
        
    def increase_button (self, value, valueCurrent, labelBtn, label) :
        """Take the next item in the value, and change the button's label """
        valueLength = len(value)
        if valueCurrent == valueLength - 1 :
             valueCurrent = 0
        else :
             valueCurrent = valueCurrent + 1
        label_colored = "[COLOR=%s]%s[/COLOR]" % ( "ff555555", value[valueCurrent] )
        self.getControl( labelBtn ).setLabel( label, label2=label_colored )
        return valueCurrent
        
    def decrease_button (self, value, valueCurrent, labelBtn, label) :
        """Take the previous item in the value, and change the button's label"""
        valueLength = len(value)
        if valueCurrent == 0 :
             valueCurrent = valueLength - 1
        else :
             valueCurrent = valueCurrent - 1
        label_colored = "[COLOR=%s]%s[/COLOR]" % ( "ff555555", value[valueCurrent] )
        self.getControl( labelBtn ).setLabel( label, label2=label_colored )
        return valueCurrent     
        
        
    def view_calendars(self) :
        """List the calendars to show/hide them"""
        
        #Call the XML Class
        self.XmlCalendar = XmlCalendar()
        #Accounts and Calendar Info
        self.calendarsInfo = self.XmlCalendar.xml_return_calendar()
        self.accountsInfo = self.XmlCalendar.xml_return_account()
                
        self.addEvent_CalendarsTitle, self.addEvent_Calendars = self.return_Write_Calendars(self.accountsInfo,self.calendarsInfo)
        
        self.calendar_list.reset()    
        
        #Define Colors        
        for accountnumber, account in enumerate(self.calendarsInfo+[[{'color':'add' , 'title' : self.Language.getLocalizedString(11) , 'type' : 'Add' , 'activate' : 'true'}]]) :
            for calendarnumber, calendar in enumerate(account) :
                print calendarnumber
                print calendar
                colortitle = calendar['color']
                if calendar["activate"] == "false" :
                    text_color = "99555555"
                    colortitle = "Grey"
                    label_colored = "[COLOR=%s]%s[/COLOR]" % ( text_color, calendar['title'] )
                else :
                    label_colored = calendar['title']
                    
                #Define Thumb
                type_thumb =  { 'Google':'calendar_thumb_google.png' , 'Local':'calendar_thumb_local.png' , 'Web':'calendar_thumb_web.png' , 'Add':'calendar_thumb_add.png'}
                calendar_thumb = type_thumb[calendar["type"]]
                
                # Add the calendars to the list
                listitem = xbmcgui.ListItem( label_colored )
                #color
                color = "color-%s.png" % (colortitle)
                colorfocus = "color-%s-focus.png" % (colortitle)
                listitem.setProperty( "color", color )        
                listitem.setProperty( "colorfocus", colorfocus ) 
                listitem.setProperty( "type", calendar["type"] )
                if colortitle != "add" :
                    listitem.setProperty( "accountid", str(accountnumber) )
                    listitem.setProperty( "accounttitle", self.accountsInfo[accountnumber]["title"] )
                    listitem.setProperty( "accounttype", self.accountsInfo[accountnumber]["type"] )
                    listitem.setProperty( "calendarid", str(calendarnumber) )
                    listitem.setProperty( "calendartitle", calendar["title"] )
                    listitem.setProperty( "accountid", str(accountnumber) )
                    listitem.setProperty( "accounttitle", self.accountsInfo[accountnumber]["title"] )
                    listitem.setProperty( "accounttype", self.accountsInfo[accountnumber]["type"] )
                listitem.setThumbnailImage(calendar_thumb)
                #Add the item in the list
                calendar_list_item = self.calendar_list.addItem( listitem )
                #calendar_list_item.getControl(1).setColorDiffuse("0xff456dfa")
            
            
    def test_calendar_url(self, url) :
        req =  Request(url)
        try:
            handle = urlopen(req)
        except IOError, e:
            return False
            if hasattr(e, 'reason'):
                print "Can not contact the server"
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'The server can not find the file'
                print 'Code d\' erreur : ', e.code
        else:
            return True 
            
    def test_mail(self, email):
    
        emailregex = "^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$"
        if len(email) > 7:
            if re.match(emailregex, email) != None:
                return True
            return False
        else:
            return False
            
    def returnDayEvents(self, dayNum) :
        dayEvents = []
        for eventNumber, eventInfo in enumerate(self.eventsGoogle+self.eventsIcs) :            
            if eventInfo['startdate'] == dayNum:
                eventInfo["color"] = self.calendarsInfo[eventInfo["accountnumber"]][eventInfo["calendarnumber"]]["color"] 
                dayEvents.append(eventInfo)
        if len(self.addEvent_CalendarsTitle) > 0 :
            dayEvents.append({"title" : self.Language.getLocalizedString(11) , "startdate" : dayNum , "enddate" : "0000-00-00" , "starttime" : "" , "endtime" : "" , "description" : "" , "accountnumber" : 0, "calendarnumber" : 0, "color" : "Add", "accesslevel" : "add", "recurrence" : {}})
        return dayEvents
        
    def returnListEvents(self) :    
            #Find the current listitem
            selectedDay = self.calendarMonthViewList.getSelectedItem()
            #Get day date
            dateNum = selectedDay.getProperty('date')
            #Clear the list
            self.eventsListGUI.reset()
            #Return day title
            dateTitle = self.calendar.returnDateTitle(dateNum, self.monthNameTitle, self.dayName)
            if dateTitle == "today" :
                dateTitle = self.Language.getLocalizedString(1210)
            
            self.eventsListTitle.setLabel(dateTitle)
            #Get day events
            self.dayEvents = self.returnDayEvents(dateNum)
            print self.dayEvents
            ## Add the event to the list
            for dayEvent in self.dayEvents :
                #calendarInfo = self.calendarsInfo[dayEvent["accountnumber"]][dayEvent["calendarnumber"]]
                #text color
                color = "color-%s.png" % (dayEvent['color'])
                colorfocus = "color-%s-focus.png" % (dayEvent['color'])
                print dayEvent
                if dayEvent.has_key("where") and dayEvent["where"] != "" :
                    label = "%s@%s" % (dayEvent['title'],dayEvent['where'])
                else :
                    label = dayEvent['title'] 
                #create Listitem
                listitem = xbmcgui.ListItem( label )  
                if dayEvent['startdate'] == "" :
                    length = ""
                else :
                    if int(dayEvent['enddate'].replace("-","")) -  int(dayEvent['startdate'].replace("-","")) == 1 and dayEvent['starttime'] == "00:00" and dayEvent['starttime'] == "00:00" :
                        length = "%s" % ( self.Language.getLocalizedString(1212) )
                    elif dayEvent['starttime'] != "" :
                        length = "%s %s %s" % ( dayEvent['starttime'], self.Language.getLocalizedString(1211) , dayEvent['endtime'] ) 
                    else :
                        length = ""

                listitem.setProperty( "length", length )
                listitem.setProperty( "color", color )      
                listitem.setProperty( "colorfocus", colorfocus )                                
                #Add the listitem to the list    
                self.eventsListGUI.addItem( listitem )    
                
    def returnGoogleInfoTitle(self) :   
        #Populate the View Calendar List
        self.view_calendars()
          
        self.addCalendar_CurrentAccount = 0
        self.addCalendar_CurrentCalendar = 0
    
        self.addCalendar_GoogleAccount = []
        self.addCalendar_GoogleAccountInfo = []
        self.addCalendar_GoogleCalendar = []
        self.addCalendar_GoogleCalendarInfo = []
        print self.accountsInfo
        calendarsAccountsInfo = self.googleCalendar.getUserCalendars(self.accountsInfo)
        
        for accountNumber, accountInfo in enumerate(self.accountsInfo) :
            
            if accountInfo["type"] == "Google" :
                self.addCalendar_GoogleAccount.append(accountInfo["title"])
                self.addCalendar_GoogleAccountInfo.append(accountInfo)
                
                self.addCalendar_GoogleCalendarInfo.append(calendarsAccountsInfo[accountNumber])
                
                calendarsAccount = []
                for calendarNumber, calendarInfo in enumerate(calendarsAccountsInfo[accountNumber]) :
                      calendarsAccount.append(calendarInfo["title"])
                self.addCalendar_GoogleCalendar.append(calendarsAccount)
                
    def modEvent(self) :
        pass
                
    def refreshCalendars(self) :
            xbmc.executebuiltin( "Skin.SetString(showcalendar,0)" )
            time.sleep(1)
            self.pDialog = xbmcgui.DialogProgress()
            self.pDialog.create(self.Language.getLocalizedString(30))
            self.pDialog.update(0)
     
            #Populate the View Calendar List
            self.view_calendars()
            #Days in the calendar
            self.dayList = self.calendar.set_container_days()
            self.pDialog.update(20)
            #Events date range
            self.eventsDateRange = self.calendar.get_event_time_range()
            #Events in the Google Calendars
            self.eventsGoogle = self.googleCalendar.DateRangeQuery(self.accountsInfo, self.calendarsInfo, self.eventsDateRange["start"], self.eventsDateRange["end"])
            self.pDialog.update(40)
            #Events in the Ics Calendars
            self.eventsIcs = self.icsCalendar.DateRangeQuery(self.accountsInfo, self.calendarsInfo, self.eventsDateRange["start"], self.eventsDateRange["end"],self.tempDir)
            self.pDialog.update(60)
            #Populate the Calendar
            self.getControl(self.calendarMonthView).reset()
            self.populate_calendar()
            #Populate the list events
            self.returnListEvents()  
            self.pDialog.update(80)     
            #Init color var
            self.decrease_button (self.colorName, 1, self.addcalendar_btn_label_color, "Color :")
            color = "color-%s.png" % (self.colorName[int(self.addCalendar_CurrentColor)])
            self.getControl( self.addcalendar_btn_image_color).setImage(color)
            #Init account type var
            self.decrease_button (self.CalendarAccountType, 1, self.addcalendar_btn_label_type, "Type :")
            #Init Add Calendar - Get google info 
            self.returnGoogleInfoTitle()
            #Init Add Calendar - Populate Google title for account and calendar
            if not self.addCalendar_GoogleAccount == [] :
                self.decrease_button (self.addCalendar_GoogleAccount, 1,  self.addcalendar_btn_label_account, "Account :")
            if not self.addCalendar_GoogleCalendar == [] and self.addCalendar_GoogleCalendar[self.addCalendar_CurrentAccount] != [] :
                self.decrease_button (self.addCalendar_GoogleCalendar[self.addCalendar_CurrentAccount], 1,  self.addcalendar_btn_label_calendar, "Calendar :")
            xbmc.executebuiltin( "Skin.SetString(showcalendar,2)" )
            self.pDialog.update(100)
            self.pDialog.close()
            
    def addEventRefresh (self, refreshCalendars = False) :
                                
        xbmc.executebuiltin( "Skin.SetString(TabSettings,1)" )
        self.returnTabSettings = 1
                     
        if refreshCalendars == True :
            self.refreshCalendars()
        
        #Init Add Event - calendar title var
        self.addEventTitle = ""
        self.addEventLocation = ""
        self.addEventComment = ""
        self.addEvent_CurrentCalendar = 0
        self.addEvent_CalendarsTitle, self.addEvent_Calendars = self.return_Write_Calendars(self.accountsInfo,self.calendarsInfo)
        self.addEventStartDate = ""
        self.addEventStartTime = ""
        self.addEventStopDate = ""
        self.addEventStopTime = ""
        self.addEventAllday = 0
        self.addEventRecurrence = 0
        self.addEventRecurDate = "00000000" 
        self.addEventUrl = None
        self.addEventCalendar = {}
        #Init Add Event - Populate calendars title
        self.decrease_button (self.addEvent_CalendarsTitle, 1,  self.addevent_btn_label_calendar, self.Language.getLocalizedString(1230))
            
        ##Init modEvent Panel
        self.getControl( self.addevent_btn_title ).setLabel( self.Language.getLocalizedString(1231), label2 = "" )
        
        self.getControl( self.addevent_btn_start ).setLabel( self.Language.getLocalizedString(1232), label2 = "" )
        
        self.getControl( self.addevent_btn_end ).setLabel( self.Language.getLocalizedString(1234), label2 = "")
    
        self.getControl( self.addevent_btn_option ).setLabel( self.Language.getLocalizedString(1236), label2 = "" )
        
        
    def checkStartEnd(self, startDate, endDate, startTime = "0000", endTime= "0000") :
        
        startInt = int("%s%s" % (startDate, startTime))
        endInt = int("%s%s" % (endDate, endTime))
        
        if startInt < endInt :
            return True
        else :
            return False       
   

    def onContainer9000( self ):
        """ content item not work in onClick( self, controlID )
            but use <onclick>SetProperty(Container_9000_item_id,int)</onclick> and in onAction( self, action )
            use if self.getFocusId() == 9000: print self.getProperty( "Container_9000_item_id" )
        """
        try:
            if self.getFocusId() == 9000:
                item_id = self.getProperty( "Container_9000_item_id" )
                if item_id:
                    #print "Container_9000_item_id", item_id
                    if item_id == "1":
                        self.getControl(9000).selectItem(1)
                        xbmc.executebuiltin( "SetProperty(Container_9000_item_id,2)" )
                        self.refreshCalendars()
                    #if item_id == "3":
                    #    xbmc.executebuiltin( "SetProperty(Container_9000_item_id,0)" )
                    #    self.setFocusId(10001)
                        
        
                    if item_id == "4":
                        self.close()
        except:
            pass         
 
    def onAction(self, action):
        #Close the script
        if action == ACTION_PREVIOUS_MENU :
            self.close()
            
        if action == ACTION_PARENT_DIR :
            panel_id = self.returnTabSettings
            print panel_id
            if panel_id == 2 :
                xbmc.executebuiltin( "Skin.SetString(TabSettings,1)" )
                self.returnTabSettings = 1
            elif panel_id == 5 :
                xbmc.executebuiltin( "Skin.SetString(TabSettings,3)" )
                self.returnTabSettings = 3
            elif panel_id == 6 :
                xbmc.executebuiltin( "Skin.SetString(TabSettings,5)" )
                self.returnTabSettings = 5
        
            
        self.onContainer9000()
            
        if (self.pDialog.iscanceled()): 
            self.close()
        
    def onClick(self, controlID):
        """
            Notice: onClick not onControl
            Notice: it gives the ID of the control not the control object
        """
        if controlID == self.dayNameList: pass
        
        #print controlID
            
        #Power Off Button             
        if controlID == 20: 
            self.close()
            
        #Calendar Buttons Click                
        if controlID == self.btn_next: 
            self.calendar.get_next_month()
            self.getControl( 150 ).reset()
            
            #Days in the calendar
            self.dayList = self.calendar.set_container_days()
            
            #Events date range
            self.eventsDateRange = self.calendar.get_event_time_range()
            
            #Events in the Google Calendars
            self.eventsGoogle = self.googleCalendar.DateRangeQuery(self.accountsInfo, self.calendarsInfo, self.eventsDateRange["start"], self.eventsDateRange["end"])
            
            #Populate the Calendar
            self.populate_calendar()
            
            #Populate the list events
            self.returnListEvents()
            
            self.setFocusId(150)
        
        if controlID == self.btn_prev: 
            self.calendar.get_prev_month()
            self.getControl( 150 ).reset()
            
            #Days in the calendar
            self.dayList = self.calendar.set_container_days()
            
            #Events date range
            self.eventsDateRange = self.calendar.get_event_time_range()
            print self.eventsDateRange
            
            #Events in the Google Calendars
            self.eventsGoogle = self.googleCalendar.DateRangeQuery(self.accountsInfo, self.calendarsInfo, self.eventsDateRange["start"], self.eventsDateRange["end"])
            
            #Populate the Calendar
            self.populate_calendar()
            
            #Populate the list events
            self.returnListEvents()
            
            self.setFocusId(150)
        
        #Hide calendar list  
        
        if controlID == self.calendarList : 
            #Find the current item position
            calendarItem = self.calendar_list.getSelectedItem()
            modCalendar_type = calendarItem.getProperty('type')
            if modCalendar_type == "Add" :
                xbmc.executebuiltin( "Skin.SetString(TabSettings,4)" )
                self.returnTabSettings = 4 
                self.setFocusId(9001)              
            else :
                self.modCalendar_calendarId = int(calendarItem.getProperty('calendarid'))
                self.modCalendar_accountId = int(calendarItem.getProperty('accountid'))
                self.modCalendar_Title = calendarItem.getProperty('calendartitle')
                ##Change modEvent label
                #Label
                label = self.Language.getLocalizedString(1220)
                label_colored = "[COLOR=%s]%s[/COLOR]" % ( "ff555555", self.modCalendar_Title )
                self.getControl( self.modCalendar_title ).setLabel( label , label2=label_colored )
                #Color
                self.modCalendar_CurrentColor = self.calendarColorId.index(self.calendarsInfo[self.modCalendar_accountId][self.modCalendar_calendarId]["color"])
                self.decrease_button (self.colorName, int(self.modCalendar_CurrentColor)+1, self.modCalendar_label_color, self.Language.getLocalizedString(1221))
                color = "color-%s.png" % (self.calendarColor[int(self.modCalendar_CurrentColor)]['name'])
                self.getControl( self.modCalendar_image_color).setImage(color)
                #activate
                if self.calendarsInfo[self.modCalendar_accountId][self.modCalendar_calendarId]["activate"] == "true" :
                    xbmc.executebuiltin( "Skin.SetString(starCalendar,1)" )
                else :
                    xbmc.executebuiltin( "Skin.SetString(starCalendar,0)" )
                #Delete Account
                if self.accountsInfo[self.modCalendar_accountId]["type"] == "Google" :
                        xbmc.executebuiltin( "Skin.SetString(delAccount,1)" )
                else :
                        xbmc.executebuiltin( "Skin.SetString(delAccount,0)" )
                
                xbmc.executebuiltin( "Skin.SetString(TabSettings,5)" )
                self.returnTabSettings = 5
                self.setFocusId(9101)
            
        
        if controlID == self.modCalendar_title : 
            self.modCalendar_Title = self.show_keyboard (self.modCalendar_Title, self.Language.getLocalizedString(1301))
            label = self.Language.getLocalizedString(1220)
            label_colored = "[COLOR=%s]%s[/COLOR]" % ( "ff555555", self.modCalendar_Title )
            self.getControl( self.modCalendar_title ).setLabel( label , label2=label_colored )
        
        if controlID == self.modCalendar_decrease_color : 
            self.modCalendar_CurrentColor = self.decrease_button (self.colorName, self.modCalendar_CurrentColor, self.modCalendar_label_color, self.Language.getLocalizedString(1221))
            color = "color-%s.png" % (self.calendarColor[int(self.modCalendar_CurrentColor)]['name'])
            self.getControl( self.modCalendar_image_color).setImage(color)
        
        if controlID == self.modCalendar_increase_color : 
            self.modCalendar_CurrentColor = self.increase_button (self.colorName, self.modCalendar_CurrentColor, self.modCalendar_label_color, self.Language.getLocalizedString(1221))
            color = "color-%s.png" % (self.calendarColor[int(self.modCalendar_CurrentColor)]['name'])
            self.getControl( self.modCalendar_image_color).setImage(color)
        
        if controlID == self.modCalendar_delete : 
            yesno = xbmcgui.Dialog().yesno(self.Language.getLocalizedString(2003), self.Language.getLocalizedString(2004))
            if yesno == True :
                self.XmlCalendar.xml_remove_calendar(self.modCalendar_accountId,self.modCalendar_calendarId)
                
                self.refreshCalendars()
                xbmc.executebuiltin( "Skin.SetString(TabSettings,3)" )
                self.returnTabSettings = 3
                                    
                self.setFocusId(8901)
        
        if controlID == self.modCalendar_delete_account : 
            yesno = xbmcgui.Dialog().yesno(self.Language.getLocalizedString(2104), self.Language.getLocalizedString(2105))
            if yesno == True :
                self.XmlCalendar.xml_remove_account(self.modCalendar_accountId)
            
                self.refreshCalendars()
                xbmc.executebuiltin( "Skin.SetString(TabSettings,3)" )
                self.returnTabSettings = 3
                                    
                self.setFocusId(8901)
        
        if controlID == self.modCalendar_update :
            yesno = xbmcgui.Dialog().yesno(self.Language.getLocalizedString(2003), self.Language.getLocalizedString(2005))
            if yesno == True :
                
                self.XmlCalendar.xml_update_calendar(self.modCalendar_accountId,self.modCalendar_calendarId,self.modCalendar_Title,self.calendarColor[int(self.modCalendar_CurrentColor)]['name'])
            
                
                self.refreshCalendars()
                xbmc.executebuiltin( "Skin.SetString(TabSettings,3)" )
                self.returnTabSettings = 3
                                    
                self.setFocusId(8901)
            
        if controlID == self.modCalendar_show_star or controlID == self.modCalendar_show_unstar : 
            #activate
            if self.calendarsInfo[self.modCalendar_accountId][self.modCalendar_calendarId]["activate"] == "true" :
                xbmc.executebuiltin( "Skin.SetString(starCalendar,0)" )
            else :
                xbmc.executebuiltin( "Skin.SetString(starCalendar,1)" )
            time.sleep(1)
            self.pDialog = xbmcgui.DialogProgress()
            self.pDialog.create(self.Language.getLocalizedString(30))
            self.pDialog.update(0)
            #Find the current item position
            self.XmlCalendar.xml_activate_calendar(self.modCalendar_accountId,self.modCalendar_calendarId)
        
            #Call the XML Class
            self.getControl( 150 ).reset()
            #Days in the calendar
            self.dayList = self.calendar.set_container_days()
            #Populate the View Calendar List
            self.view_calendars() 
            self.pDialog.update(50)           
            #Events in the Google Calendars
            self.eventsGoogle = self.googleCalendar.DateRangeQuery(self.accountsInfo, self.calendarsInfo, self.eventsDateRange["start"], self.eventsDateRange["end"])
            #Populate the Calendar
            self.populate_calendar()
            #Populate the list events
            self.returnListEvents()
            self.pDialog.update(100)
            self.pDialog.close()
            xbmc.executebuiltin( "Skin.SetString(showcalendar,2)" )
            
            
        #Add Calendar Buttons Click
        if controlID == self.addcalendar_btn_title :
            self.addCalendarTitle = self.show_keyboard ("", self.Language.getLocalizedString(1301))
            label = self.Language.getLocalizedString(1220)
            label_colored = "[COLOR=%s]%s[/COLOR]" % ( "ff555555", self.addCalendarTitle )
            self.getControl( self.addcalendar_btn_title ).setLabel( label , label2=label_colored )
            
        if controlID == self.addcalendar_btn_decrease_color :
            self.addCalendar_CurrentColor = self.decrease_button (self.colorName, self.addCalendar_CurrentColor, self.addcalendar_btn_label_color, self.Language.getLocalizedString(1221))
            color = "color-%s.png" % (self.calendarColor[int(self.addCalendar_CurrentColor)]['name'])
            self.getControl( self.addcalendar_btn_image_color).setImage(color)
            
        if controlID == self.addcalendar_btn_increase_color :
            self.addCalendar_CurrentColor = self.increase_button (self.colorName, self.addCalendar_CurrentColor, self.addcalendar_btn_label_color, self.Language.getLocalizedString(1221))
            color = "color-%s.png" % (self.calendarColor[int(self.addCalendar_CurrentColor)]['name'])
            self.getControl( self.addcalendar_btn_image_color).setImage(color)
            
        if controlID == self.addcalendar_btn_decrease_type :
            self.addCalendar_CurrentType = self.decrease_button (self.CalendarAccountType, self.addCalendar_CurrentType, self.addcalendar_btn_label_type, self.Language.getLocalizedString(1222))
            if self.CalendarAccountType[self.addCalendar_CurrentType] == "Google" :
                self.getControl(self.addcalendar_btn_group_account).setVisible(True)
                self.getControl(self.addcalendar_btn_group_calendar).setVisible(True)
                self.getControl(self.addcalendar_btn_url).setVisible(False)
            else :
                self.getControl( self.addcalendar_btn_url ).setLabel( "URL :   ", label2="" )
                self.getControl(self.addcalendar_btn_group_account).setVisible(False)
                self.getControl(self.addcalendar_btn_group_calendar).setVisible(False)
                self.getControl(self.addcalendar_btn_url).setVisible(True)
            
        if controlID == self.addcalendar_btn_increase_type :
            self.addCalendar_CurrentType = self.increase_button (self.CalendarAccountType, self.addCalendar_CurrentType, self.addcalendar_btn_label_type, "Type :")
            if self.CalendarAccountType[self.addCalendar_CurrentType] == "Google" :
                self.getControl(self.addcalendar_btn_group_account).setVisible(True)
                self.getControl(self.addcalendar_btn_group_calendar).setVisible(True)
                self.getControl(self.addcalendar_btn_url).setVisible(False)
            else :
                self.getControl( self.addcalendar_btn_url ).setLabel( "URL :   ", label2="" )
                self.getControl(self.addcalendar_btn_group_account).setVisible(False)
                self.getControl(self.addcalendar_btn_group_calendar).setVisible(False)
                self.getControl(self.addcalendar_btn_url).setVisible(True)
            
        if controlID == self.addcalendar_btn_decrease_account :
            self.addCalendar_CurrentAccount = self.decrease_button (self.addCalendar_GoogleAccount, self.addCalendar_CurrentAccount,  self.addcalendar_btn_label_account, self.Language.getLocalizedString(1224))
            self.addCalendar_CurrentCalendar = self.decrease_button (self.addCalendar_GoogleCalendar[self.addCalendar_CurrentAccount], 1,  self.addcalendar_btn_label_calendar, self.Language.getLocalizedString(1225))
            
        if controlID == self.addcalendar_btn_increase_account :
            self.addCalendar_CurrentAccount = self.increase_button (self.addCalendar_GoogleAccount, self.addCalendar_CurrentAccount,  self.addcalendar_btn_label_account, self.Language.getLocalizedString(1224))
            self.addCalendar_CurrentCalendar = self.decrease_button (self.addCalendar_GoogleCalendar[self.addCalendar_CurrentAccount], 1,  self.addcalendar_btn_label_calendar, self.Language.getLocalizedString(1225))
            
        if controlID == self.addcalendar_btn_decrease_calendar :
            self.addCalendar_CurrentCalendar = self.decrease_button (self.addCalendar_GoogleCalendar[self.addCalendar_CurrentAccount], self.addCalendar_CurrentCalendar,  self.addcalendar_btn_label_calendar, self.Language.getLocalizedString(1225))
                        
        if controlID == self.addcalendar_btn_increase_calendar :
            self.addCalendar_CurrentCalendar = self.increase_button (self.addCalendar_GoogleCalendar[self.addCalendar_CurrentAccount], self.addCalendar_CurrentCalendar,  self.addcalendar_btn_label_calendar, self.Language.getLocalizedString(1225))
        
        if controlID == self.addcalendar_btn_add_account :
            #Init var
            title = self.show_keyboard ("", self.Language.getLocalizedString(1320))
            login = self.show_keyboard ("@gmail.com", self.Language.getLocalizedString(1321))
            pwd = self.show_keyboard ("", self.Language.getLocalizedString(1322), True)
            type = self.CalendarAccountType[self.addCalendar_CurrentType]
            #Check if login is email            
            check_mail = True
            check_mail = self.test_mail(login)
                
            if check_mail == True and self.googleCalendar.googleAccountConnect(login , pwd) == True:
                
                pDialog = xbmcgui.DialogProgress()
                pDialog.create(self.Language.getLocalizedString(30))
                #Add the account in the xml tree
                self.XmlCalendar.xml_add_account(title, type, login, pwd)
                #Update the account info
                self.accountsInfo = self.XmlCalendar.xml_return_account()
                #Get google's accounts info 
                self.returnGoogleInfoTitle()
                #Update the add calendar's titles info
                self.addCalendar_CurrentAccount = self.decrease_button (self.addCalendar_GoogleAccount, 0,  self.addcalendar_btn_label_account, self.Language.getLocalizedString(1224))
                self.addCalendar_CurrentCalendar = self.decrease_button (self.addCalendar_GoogleCalendar[self.addCalendar_CurrentAccount], 1,  self.addcalendar_btn_label_calendar, self.Language.getLocalizedString(1225))
                
                pDialog.close()
            
            else : 
                xbmcgui.Dialog().ok(self.Language.getLocalizedString(1270) , self.Language.getLocalizedString(1323))
                
        
        if controlID == self.addcalendar_btn_add_calendar :
            if self.CalendarAccountType[self.addCalendar_CurrentType] == "Google" :
                #Init var
                title = self.show_keyboard ("", self.Language.getLocalizedString(1320))
                login = self.addCalendar_GoogleAccountInfo[self.addCalendar_CurrentAccount]['login']
                password = self.addCalendar_GoogleAccountInfo[self.addCalendar_CurrentAccount]['password']
                color = self.calendarColor[self.addCalendar_CurrentColor]["color"]
                
                pDialog = xbmcgui.DialogProgress()
                pDialog.create(self.Language.getLocalizedString(30))
                
                #Create the onLine Google's Calendar
                self.googleCalendar.add_google_calendar(title,login,password,color)
                #Get google's accounts info 
                self.returnGoogleInfoTitle()
                
                #Update the add calendar's titles info
                calendarPosition = self.addCalendar_CurrentCalendar + 1
                for calendarNumber, calendarTitle in enumerate(self.addCalendar_GoogleCalendar[self.addCalendar_CurrentAccount]) :
                    if calendarTitle == title :
                        calendarPosition = calendarNumber + 1
                self.addCalendar_CurrentCalendar = self.decrease_button (self.addCalendar_GoogleCalendar[self.addCalendar_CurrentAccount], calendarPosition,  self.addcalendar_btn_label_calendar, "Calendar :")
                
                pDialog.close()
        
        if controlID == self.addcalendar_btn_url :
            if self.CalendarAccountType[self.addCalendar_CurrentType] == "Local" :
                self.addCalendarUrl = xbmcgui.Dialog().browse( 1 , self.Language.getLocalizedString(1283) , 'files' , '.ics')
                label_colored = "[COLOR=%s]%s[/COLOR]" % ( "ff555555", self.addCalendarUrl )
                self.getControl( self.addcalendar_btn_url ).setLabel( "URL :   ", label2=label_colored )
            elif self.CalendarAccountType[self.addCalendar_CurrentType] == "Web" :
                self.addCalendarUrl = self.show_keyboard ("http://", "")
                label_colored = "[COLOR=%s]%s[/COLOR]" % ( "ff555555", self.addCalendarUrl )
                self.getControl( self.addcalendar_btn_url ).setLabel( "URL :   ", label2=label_colored )
            
        if controlID == self.addcalendar_btn_ok :
            xbmc.executebuiltin( "Skin.SetString(TabSettings,0)" )
            self.returnTabSettings = 0
            time.sleep(1)
            self.pDialog = xbmcgui.DialogProgress()
            self.pDialog.create(self.Language.getLocalizedString(30))
            self.pDialog.update(0)
            self.pDialog.create(self.Language.getLocalizedString(1283))
            if hasattr(self, 'addCalendarTitle') and not self.addCalendarTitle == 0 :
                
                #Init Var
                title = self.addCalendarTitle
                color = self.calendarColor[self.addCalendar_CurrentColor]['name']
                type = self.CalendarAccountType[self.addCalendar_CurrentType]
                accesslevel = "owner"
                login = ""
                password = ""
                #Specific var for Google
                if type == "Google" :
                    #Accounts Info
                    login = self.addCalendar_GoogleAccountInfo[self.addCalendar_CurrentAccount]['login']
                    password = self.addCalendar_GoogleAccountInfo[self.addCalendar_CurrentAccount]['password']
                    #Calendars Info
                    print self.addCalendar_GoogleCalendarInfo
                    print self.addCalendar_CurrentAccount
                    print self.addCalendar_CurrentCalendar
                    accesslevel = self.addCalendar_GoogleCalendarInfo[self.addCalendar_CurrentAccount][self.addCalendar_CurrentCalendar]['accesslevel']
                    id = self.addCalendar_GoogleCalendarInfo[self.addCalendar_CurrentAccount][self.addCalendar_CurrentCalendar]['id']
                    print login, password
                #Specific var for ICS Files    
                else :
                    if hasattr(self, 'addCalendarTitle') and not self.addCalendarTitle == 0 :
                        id = self.addCalendarUrl
                        
                        check_url = True
                        if type == "web" :
                            check_url = self.test_calendar_url(url)
                            accesslevel = "read"
                            
                        if check_url == True :
                            
                            self.XmlCalendar.xml_add_calendar(type, title, color, id)
                            
                            xbmcgui.Dialog().ok(self.Language.getLocalizedString(1285) , self.Language.getLocalizedString(1286))
                            
                            self.addCalendarTitle = 0
                            self.getControl( self.addcalendar_btn_title ).setLabel( self.Language.getLocalizedString(1220) , label2="")
                            
                            self.addCalendarUrl = 0
                            self.getControl( self.addcalendar_btn_url ).setLabel( self.Language.getLocalizedString(1223) , label2="")
                            
                            self.view_calendars()
                        else :
                            xbmcgui.Dialog().ok(self.Language.getLocalizedString(1287) , self.Language.getLocalizedString(1289))
                        
                    else : 
                        xbmcgui.Dialog().ok(self.Language.getLocalizedString(1288) , self.Language.getLocalizedString(1289))
                
                self.pDialog.update(40)
                
                xbmc.executebuiltin( "Skin.SetString(showcalendar,0)" )
                time.sleep(1)
                #Add the Calendar in the XML
                self.XmlCalendar.xml_add_calendar(type, title, color, id, accesslevel, login, password)    
                #Init the add calendar panel        
                self.addCalendarTitle = 0
                self.getControl( self.addcalendar_btn_title ).setLabel( self.Language.getLocalizedString(1220) , label2="")
                xbmcgui.Dialog().ok(self.Language.getLocalizedString(1285) , self.Language.getLocalizedString(1286))
                
                self.getControl( 150 ).reset()
                #Days in the calendar
                self.dayList = self.calendar.set_container_days()
                self.pDialog.update(60)
                #Populate the View Calendar List
                self.view_calendars() 
                #Get google's accounts info 
                self.returnGoogleInfoTitle()           
                #Events in the Google Calendars
                self.eventsGoogle = self.googleCalendar.DateRangeQuery(self.accountsInfo, self.calendarsInfo, self.eventsDateRange["start"], self.eventsDateRange["end"])
                self.pDialog.update(80)
                #Populate the Calendar
                self.populate_calendar()
                #Populate the list events
                self.returnListEvents()
                self.pDialog.update(100)
                
                xbmc.executebuiltin( "Skin.SetString(TabSettings,4)" )
                self.returnTabSettings = 4
                time.sleep(1)
                xbmc.executebuiltin( "Skin.SetString(showcalendar,2)" )
                self.pDialog.close()
                
            else : 
                xbmcgui.Dialog().ok(self.Language.getLocalizedString(1290) , self.Language.getLocalizedString(1291))
                xbmc.executebuiltin( "Skin.SetString(TabSettings,4)" )
                self.returnTabSettings = 4
                time.sleep(1)
                xbmc.executebuiltin( "Skin.SetString(showcalendar,2)" )
                self.pDialog.close()
            
            
        #Add Event Buttons Click
        if controlID == self.addevent_btn_decrease_calendar and self.addEventUrl == None:
            self.addEvent_CurrentCalendar = self.decrease_button (self.addEvent_CalendarsTitle, self.addEvent_CurrentCalendar,  self.addevent_btn_label_calendar, self.Language.getLocalizedString(1230))
            
        if controlID == self.addevent_btn_increase_calendar and self.addEventUrl == None:
            self.addEvent_CurrentCalendar = self.increase_button (self.addEvent_CalendarsTitle, self.addEvent_CurrentCalendar,  self.addevent_btn_label_calendar, self.Language.getLocalizedString(1230))
            
        if controlID == self.addevent_btn_title :
            self.addEventTitle = self.show_keyboard (self.addEventTitle, self.Language.getLocalizedString(1250))
            label = self.Language.getLocalizedString(1231)
            label_colored = "[COLOR=%s]%s[/COLOR]" % ( "ff555555", self.addEventTitle )
            self.getControl( self.addevent_btn_title ).setLabel( label , label2=label_colored )
            
            
        if controlID == self.addevent_btn_start :
             if not self.addEventUrl is None and self.modEventRecurrence == True :
                xbmcgui.Dialog().ok(self.Language.getLocalizedString(1265) , self.Language.getLocalizedString(1266))
             else:
            
                self.addEventStartDate = self.show_keyboard (self.addEventStartDate, self.Language.getLocalizedString(1252))
                    
                #Dialog AllDay
                self.addEventAllday = xbmcgui.Dialog().yesno(self.Language.getLocalizedString(23), self.Language.getLocalizedString(1251))
                print self.addEventAllday
                if self.addEventAllday == 0 :
                    self.addEventStartTime = self.show_keyboard (self.addEventStartTime, self.Language.getLocalizedString(1253))
                else :
                    self.addEventStartTime = "0000"
                if self.addEventUrl is None :
                    self.addEventRecurrence = xbmcgui.Dialog().select(self.Language.getLocalizedString(1258), [self.Language.getLocalizedString(1260),self.Language.getLocalizedString(1261),self.Language.getLocalizedString(1262),self.Language.getLocalizedString(1263),self.Language.getLocalizedString(1264)])
                    
                if not self.addEventRecurrence == 0 :
                    if self.addEventRecurDate == "00000000" :
                        recurText = ""
                    else : 
                        recurText = self.addEventRecurDate 
                    self.addEventRecurDate = self.show_keyboard (recurText, self.Language.getLocalizedString(1259))
                
                labeltitle = ""
                if not self.isInteger(self.addEventStartDate) == "Error" and not self.isInteger(self.addEventStartTime) == "Error" and not self.isInteger(self.addEventRecurDate) == "Error" and  len(self.addEventStartDate) == 8 and  len(self.addEventRecurDate) == 8 and len(self.addEventStartTime) == 4 and  self.isInteger(self.addEventStartDate[4:6]) <= 12 :
                    addEventMonthTitle = 100 + self.isInteger(self.addEventStartDate[4:6])
                    if self.addEventRecurrence == 0 :
                        recurText = ""
                    else :
                        recurText = " *"
                    if self.addEventAllday == 0 :
                        labeltitle = "%s %s %s %s %sh%s%s" % (self.addEventStartDate[6:8] , self.Language.getLocalizedString(addEventMonthTitle) , self.addEventStartDate[0:4] , self.Language.getLocalizedString(5) , self.addEventStartTime[0:2] , self.addEventStartTime[2:4], recurText)
                    else :
                        labeltitle = "%s %s %s%s" % (self.addEventStartDate[6:8] , self.Language.getLocalizedString(addEventMonthTitle) , self.addEventStartDate[0:4], recurText)
                
                elif self.isInteger(self.addEventStartDate) == "Error" or len(self.addEventStartDate) != 8 or  self.isInteger(self.addEventStartDate[4:6]) >= 13:
                    xbmcgui.Dialog().ok(self.Language.getLocalizedString(1270) , self.Language.getLocalizedString(1232)+self.Language.getLocalizedString(1271))
                    
                    self.addEventStartDate = ""
                    self.addEventAllday = 0 
                    
                elif self.isInteger(self.addEventStartTime) == "Error" or len(self.addEventStartTime) != 4:
                    xbmcgui.Dialog().ok(self.Language.getLocalizedString(1270) , self.Language.getLocalizedString(1233)+self.Language.getLocalizedString(1271))
              
                    self.addEventStartTime = ""
                    self.addEventAllday = 0 
                    
                elif self.isInteger(self.addEventRecurDate) == "Error" or len(self.addEventRecurDate) != 8:
                    xbmcgui.Dialog().ok(self.Language.getLocalizedString(1270) , self.Language.getLocalizedString(1237)+self.Language.getLocalizedString(1271))
              
                    self.addEventRecurDate = "00000000" 
                    
                else :
                    xbmcgui.Dialog().ok(self.Language.getLocalizedString(1270) , self.Language.getLocalizedString(1271))
              
                    self.addEventStartDate = ""
                    self.addEventStartTime = ""
                    self.addEventAllday = 0 
                    self.addEventRecurDate = "00000000"
                
                label = self.Language.getLocalizedString(1232)
                label_colored = "[COLOR=%s]%s[/COLOR]" % ( "ff555555", labeltitle )
                self.getControl( self.addevent_btn_start ).setLabel( label , label2=label_colored )
                
                
                if self.addEventAllday == 1 :
                    
                    self.addEventEndDate = self.calendar.get_next_day(self.addEventStartDate)
                    self.addEventEndTime = "0000"
                    labeltitle = "%s" % (self.Language.getLocalizedString(1212))
                    label = self.Language.getLocalizedString(1234)
                    label_colored = "[COLOR=%s]%s[/COLOR]" % ( "ff555555", labeltitle )
                    self.getControl( self.addevent_btn_end ).setLabel( label , label2=label_colored )
                
                
        if controlID == self.addevent_btn_end :
        
             if not self.addEventUrl is None and self.modEventRecurrence == True :
                xbmcgui.Dialog().ok(self.Language.getLocalizedString(1265) , self.Language.getLocalizedString(1266))
             else:
                
                self.addEventEndDate = self.show_keyboard (self.addEventEndDate, self.Language.getLocalizedString(1254))
                self.addEventEndTime = self.show_keyboard (self.addEventEndTime, self.Language.getLocalizedString(1255))
                labeltitle = ""
                
                if not self.isInteger(self.addEventEndDate) == "Error" and not self.isInteger(self.addEventEndTime) == "Error" and  len(self.addEventEndDate) == 8 and len(self.addEventEndTime) == 4 and  self.isInteger(self.addEventEndDate[4:6]) <= 12 :
                    addEventMonthTitle = 100 + self.isInteger(self.addEventEndDate[4:6])
                    labeltitle = "%s %s %s %s %sh%s" % (self.addEventEndDate[6:8] , self.Language.getLocalizedString(addEventMonthTitle) , self.addEventEndDate[0:4] , self.Language.getLocalizedString(5) , self.addEventEndTime[0:2] , self.addEventEndTime[2:4])
                
                elif self.isInteger(self.addEventEndDate) == "Error" or len(self.addEventEndDate) != 8 or  self.isInteger(self.addEventEndDate[4:6]) >= 13:
                    xbmcgui.Dialog().ok(self.Language.getLocalizedString(1270) , self.Language.getLocalizedString(1234)+self.Language.getLocalizedString(1271))
                    
                    self.addEventEndDate = ""
                    
                elif self.isInteger(self.addEventEndTime) == "Error" or len(self.addEventEndTime) != 4:
                    xbmcgui.Dialog().ok(self.Language.getLocalizedString(1270) , self.Language.getLocalizedString(1235)+self.Language.getLocalizedString(1271))
              
                    self.addEventEndTime = ""
                    
                else :
                    xbmcgui.Dialog().ok(self.Language.getLocalizedString(1270) , self.Language.getLocalizedString(1271))
              
                    self.addEventEndDate = ""
                    self.addEventEndTime = ""
                    
                label = self.Language.getLocalizedString(1234)
                label_colored = "[COLOR=%s]%s[/COLOR]" % ( "ff555555", labeltitle )
                self.getControl( self.addevent_btn_end ).setLabel( label , label2=label_colored )
                
            
        if controlID == self.addevent_btn_option :
            #Lieu
            self.addEventLocation = self.show_keyboard (self.addEventLocation, self.Language.getLocalizedString(1256))
            
            #Description
            self.addEventComment = self.show_keyboard (self.addEventComment, self.Language.getLocalizedString(1257))
            
            label = self.Language.getLocalizedString(1236)
            label_colored = self.addEventComment
            if self.addEventLocation != ""  :
                label_colored = "%s @%s" % (label_colored, self.addEventLocation)
            label_colored = "[COLOR=%s]%s[/COLOR]" % ( "ff555555", label_colored )
            self.getControl( self.addevent_btn_option ).setLabel( label , label2=label_colored )

            
        if controlID == self.addevent_btn_ok :
            
            if self.addEventTitle != "" :
                if self.addEventStartDate != "" and self.addEventStartTime != "" :
                    if self.addEventEndDate != "" and self.addEventEndTime != "" :
                      
                        if self.addEventRecurrence != 0 and self.addEventRecurDate == "00000000" :
                            xbmcgui.Dialog().ok(self.Language.getLocalizedString(1270) , self.Language.getLocalizedString(1237)+self.Language.getLocalizedString(1272))
                        else :
                            
                            if self.checkStartEnd(self.addEventStartDate, self.addEventEndDate, self.addEventStartTime, self.addEventEndTime) is True :
                            
                                ###
                                if not self.addEventUrl is None :
                                    yesno = xbmcgui.Dialog().yesno(self.Language.getLocalizedString(25), self.Language.getLocalizedString(1280))
                                    if yesno == True :
                                        self.googleCalendar.UpdateTitle(self.addEventUrl, self.addEventCalendar, self.addEventStartDate+self.addEventStartTime, self.addEventEndDate+self.addEventEndTime, title=self.addEventTitle,
                                           content=self.addEventComment, where=self.addEventLocation)
                                        xbmcgui.Dialog().ok(self.Language.getLocalizedString(25) , self.Language.getLocalizedString(1276))
                                                     
                                        self.addEventRefresh(refreshCalendars = True)
                                        
                                else :
                                    if self.addEventRecurrence != 0 :
                                        self.addEventRecurDate = self.calendar.get_next_day(self.addEventRecurDate)
                                        
                                    self.googleCalendar.InsertRecurringEvent(self.addEvent_Calendars[self.addEvent_CurrentCalendar], self.addEventStartDate+self.addEventStartTime, self.addEventEndDate+self.addEventEndTime, title=self.addEventTitle,
                                                 content=self.addEventComment, where=self.addEventLocation,
                                                 recurrence=self.addEventRecurrence, recurDate=self.addEventRecurDate)
                                             
                                    xbmcgui.Dialog().ok(self.Language.getLocalizedString(23) , self.Language.getLocalizedString(1274))
                                                 
                                    self.addEventRefresh(refreshCalendars = True)
                                    
                                self.setFocusId(8801)
                                    
                                    
                            else :
                                xbmcgui.Dialog().ok(self.Language.getLocalizedString(1270) , self.Language.getLocalizedString(1282)) 
                                
                            
                            
                            
                            
                            
                    else :    
                        xbmcgui.Dialog().ok(self.Language.getLocalizedString(1270) , self.Language.getLocalizedString(1234)+self.Language.getLocalizedString(1272))    
                else :    
                    xbmcgui.Dialog().ok(self.Language.getLocalizedString(1270) , self.Language.getLocalizedString(1232)+self.Language.getLocalizedString(1272))    
            else :    
                xbmcgui.Dialog().ok(self.Language.getLocalizedString(1270) , self.Language.getLocalizedString(1231)+self.Language.getLocalizedString(1273))    
        
        
        if controlID == self.addevent_btn_delete :
          yesno = xbmcgui.Dialog().yesno(self.Language.getLocalizedString(26), self.Language.getLocalizedString(1281))
          if yesno == True :
            if self.googleCalendar.DeleteEvent(self.addEventCalendar, self.addEventUrl) is True :
                        xbmcgui.Dialog().ok(self.Language.getLocalizedString(26) , self.Language.getLocalizedString(1277))
          
                        self.addEventRefresh(refreshCalendars = True)
                        
            else :
                        xbmcgui.Dialog().ok(self.Language.getLocalizedString(1270) , self.Language.getLocalizedString(1279))
                        
                        
                        
        if controlID == self.addEvent_menu :
            self.addEventRefresh()
            
            #View the modEvent Panel
            xbmc.executebuiltin( "Skin.SetString(modEvent,0)" )
            xbmc.executebuiltin( "Skin.SetString(TabSettings,2)" )
            self.returnTabSettings = 2
            
                        
    
        ##ModEvent
        if controlID == self.modEvent_List :
            #Find the current item position
            modEventNum = self.eventsListGUI.getSelectedPosition()
            
            #Check if calendar is writable
            if self.dayEvents[modEventNum].has_key('accesslevel') and self.dayEvents[modEventNum]['accesslevel'] == "add" :
                writable = "add"
            elif self.calendarsInfo[int(self.dayEvents[modEventNum]['accountnumber'])][int(self.dayEvents[modEventNum]['calendarnumber'])].has_key('accesslevel') :
                writable = self.calendarsInfo[int(self.dayEvents[modEventNum]['accountnumber'])][int(self.dayEvents[modEventNum]['calendarnumber'])]['accesslevel']
            else : 
                writable = "readonly"
            if writable in ["owner","add"] :
               
                if writable == "owner" :
                    ##Init modEvent var
                    self.addEventTitle = self.dayEvents[modEventNum]['title']
                    self.addEventStartDate = string.replace(self.dayEvents[modEventNum]['startdate'],"-","")
                    self.addEventStartTime = string.replace(self.dayEvents[modEventNum]['starttime'],":","")
                    self.addEventEndDate = string.replace(self.dayEvents[modEventNum]['enddate'],"-","")
                    self.addEventEndTime = string.replace(self.dayEvents[modEventNum]['endtime'] ,":","") 
                    self.addEventUrl = self.dayEvents[modEventNum]['event']
                    if self.dayEvents[modEventNum].has_key('recurrence') and self.dayEvents[modEventNum]['recurrence'] != {} :
                        self.modEventRecurrence = True
                    else :
                        self.modEventRecurrence = False
                    self.addEventLocation = self.dayEvents[modEventNum]['where']
                    self.addEventComment = self.dayEvents[modEventNum]['comment']
                    self.addEventCalendar = self.calendarsInfo[int(self.dayEvents[modEventNum]['accountnumber'])][int(self.dayEvents[modEventNum]['calendarnumber'])]
                    #Check Allday
                    self.addEventAllday = 0
                    self.addEventRecurDate = "00000000"
                    
                    
                    addEventMonthTitle = 100 + self.isInteger(self.addEventStartDate[4:6])
                    
               
                else :
                    ##Init modEvent var
                    self.addEventTitle = ""
                    self.addEventStartDate = string.replace(self.dayEvents[modEventNum]['startdate'],"-","")
                    self.addEventStartTime = "0000"
                    self.addEventEndDate = string.replace(self.dayEvents[modEventNum]['startdate'],"-","")
                    self.addEventEndTime = "0000" 
                    self.addEventUrl = None
                    self.modEventRecurrence = False
                    self.addEventLocation = ""
                    self.addEventComment = ""
                    self.addEventCalendar = writable
                    #Check Allday
                    self.addEventAllday = 0
                    self.addEventRecurDate = "00000000"
                      
                    addEventMonthTitle = 100 + self.isInteger(self.addEventStartDate[4:6])
            
                self.setFocusId(8702)
                
                    
                ##Init modEvent Panel
                label = self.Language.getLocalizedString(1231)
                label_colored = "[COLOR=%s]%s[/COLOR]" % ( "ff555555", self.addEventTitle )
                self.getControl( self.addevent_btn_title ).setLabel( label , label2=label_colored )   
                 
                labeltitlestart = "%s %s %s %s %sh%s" % (self.addEventStartDate[6:8] , self.Language.getLocalizedString(addEventMonthTitle) , self.addEventStartDate[0:4] , self.Language.getLocalizedString(5) , self.addEventStartTime[0:2] , self.addEventStartTime[2:4])
                
                labeltitleend = "%s %s %s %s %sh%s" % (self.addEventEndDate[6:8] , self.Language.getLocalizedString(addEventMonthTitle) , self.addEventEndDate[0:4] , self.Language.getLocalizedString(5) , self.addEventEndTime[0:2] , self.addEventEndTime[2:4])
                
                if self.dayEvents[modEventNum].has_key('recurrence') and self.dayEvents[modEventNum]['recurrence'] != {} :
                    labeltitlestart = "%s *" % (labeltitlestart)
                    labelstart = "[COLOR=%s]%s[/COLOR]" % ( "ff555555", self.Language.getLocalizedString(1232))
                    labelend = "[COLOR=%s]%s[/COLOR]" % ( "ff555555", self.Language.getLocalizedString(1234))
                    
                else :
                    labelstart = self.Language.getLocalizedString(1232)
                    labelend = self.Language.getLocalizedString(1234)

                label_colored_start = "[COLOR=%s]%s[/COLOR]" % ( "ff555555", labeltitlestart )
                label_colored_end = "[COLOR=%s]%s[/COLOR]" % ( "ff555555", labeltitleend )
                self.getControl( self.addevent_btn_start ).setLabel( labelstart , label2=label_colored_start )
                self.getControl( self.addevent_btn_end ).setLabel( labelend , label2=label_colored_end )
            
                label = self.Language.getLocalizedString(1236)
                label_colored = self.addEventComment
                if self.addEventLocation != ""  :
                    label_colored = "%s @%s" % (label_colored, self.addEventLocation)
                label_colored = "[COLOR=%s]%s[/COLOR]" % ( "ff555555", label_colored )
                self.getControl( self.addevent_btn_option ).setLabel( label , label2=label_colored )
                
                self.addEvent_CurrentCalendar = 0
                label = self.Language.getLocalizedString(1230)
                if writable == "owner" :
                    label_colored = "[COLOR=%s]%s[/COLOR]" % ( "ff555555", self.calendarsInfo[int(self.dayEvents[modEventNum]['accountnumber'])][int(self.dayEvents[modEventNum]['calendarnumber'])]['title'] )
                    self.getControl( self.addevent_btn_label_calendar ).setLabel( label , label2=label_colored )
                    xbmc.executebuiltin( "Skin.SetString(modEvent,1)" )
                else : 
                    self.addEvent_CurrentCalendar = 0
                    self.addEvent_CalendarsTitle, self.addEvent_Calendars = self.return_Write_Calendars(self.accountsInfo,self.calendarsInfo)
                    #Init Add Event - Populate calendars title
                    self.decrease_button (self.addEvent_CalendarsTitle, 1,  self.addevent_btn_label_calendar, self.Language.getLocalizedString(1230))
                    xbmc.executebuiltin( "Skin.SetString(modEvent,0)" )
                xbmc.executebuiltin( "Skin.SetString(TabSettings,2)" )
                self.returnTabSettings = 2
    
    
    
        ##Update Account        
        if controlID == self.modCalendar_update_account :
            #Find the current item position
            self.modAccountTitle = self.accountsInfo[self.modCalendar_accountId]['title']
            self.modAccountLogin = self.accountsInfo[self.modCalendar_accountId]['login']
            self.modAccountPassword = self.accountsInfo[self.modCalendar_accountId]['password']
            ##Change modEvent label
            #Title
            labelTitle = self.Language.getLocalizedString(1220)
            labelTitle_colored = "[COLOR=%s]%s[/COLOR]" % ( "ff555555", self.modAccountTitle )
            self.getControl( self.modAccount_title ).setLabel( labelTitle , label2=labelTitle_colored )
            #Login
            labelLogin = self.Language.getLocalizedString(1321)
            labelLogin_colored = "[COLOR=%s]%s[/COLOR]" % ( "ff555555", self.modAccountLogin )
            self.getControl( self.modAccount_login ).setLabel( labelLogin , label2=labelLogin_colored )
            #Password
            labelPass = self.Language.getLocalizedString(1322)
            if self.modAccountPassword != "" :
                txtPass = "******"
            else :
                txtPass = ""
            labelPass_colored = "[COLOR=%s]%s[/COLOR]" % ( "ff555555", txtPass )
            self.getControl( self.modAccount_password ).setLabel( labelPass , label2=labelPass_colored )
            
            xbmc.executebuiltin( "Skin.SetString(TabSettings,6)" )
            self.returnTabSettings = 6
            
            self.setFocusId(9201)
    
    
        if controlID == self.modAccount_title :
            self.modAccountTitle = self.show_keyboard (self.modAccountTitle, self.Language.getLocalizedString(2101))
            labelTitle = self.Language.getLocalizedString(1220)
            labelTitle_colored = "[COLOR=%s]%s[/COLOR]" % ( "ff555555", self.modAccountTitle )
            self.getControl( self.modAccount_title ).setLabel( labelTitle , label2=labelTitle_colored )
    
        if controlID == self.modAccount_login :
            self.modAccountLogin = self.show_keyboard (self.modAccountLogin, self.Language.getLocalizedString(1301))
            #Login
            labelLogin = self.Language.getLocalizedString(1321)
            labelLogin_colored = "[COLOR=%s]%s[/COLOR]" % ( "ff555555", self.modAccountLogin )
            self.getControl( self.modAccount_login ).setLabel( labelLogin , label2=labelLogin_colored )
    
        if controlID == self.modAccount_password :
            self.modAccountPassword = self.show_keyboard ("", self.Language.getLocalizedString(1301))
            #Password
            labelPass = self.Language.getLocalizedString(1322)
            if self.modAccountPassword != "" :
                txtPass = "******"
            else :
                txtPass = ""
            labelPass_colored = "[COLOR=%s]%s[/COLOR]" % ( "ff555555", txtPass )
            self.getControl( self.modAccount_password ).setLabel( labelPass , label2=labelPass_colored )
    
        if controlID == self.modCalendar_validate_account :
            yesno = xbmcgui.Dialog().yesno(self.Language.getLocalizedString(2104), self.Language.getLocalizedString(2106))
            if yesno == True :
                xbmc.executebuiltin( "Skin.SetString(showcalendar,0)" )
                time.sleep(1)
                self.pDialog = xbmcgui.DialogProgress()
                self.pDialog.update(0)
                self.pDialog.create(self.Language.getLocalizedString(30))
                #Find the current item position
                self.XmlCalendar.xml_update_account(self.modCalendar_accountId,self.modAccountTitle,self.modAccountLogin,self.modAccountPassword)
            
                #Call the XML Class
                self.getControl( 150 ).reset()
                #Days in the calendar
                self.dayList = self.calendar.set_container_days()
                self.view_calendars() 
                self.pDialog.update(50)           
                #Events in the Google Calendars
                self.eventsGoogle = self.googleCalendar.DateRangeQuery(self.accountsInfo, self.calendarsInfo, self.eventsDateRange["start"], self.eventsDateRange["end"])
                #Populate the Calendar
                self.populate_calendar()
                #Populate the list events
                self.returnListEvents()
                self.pDialog.update(100)
                self.pDialog.close()
                xbmc.executebuiltin( "Skin.SetString(showcalendar,2)" )
    
    
    
        ##Calendar Action            
        if controlID == self.calendarMonthView :
            xbmc.executebuiltin( "Skin.SetString(TabSettings,0)" )
            self.returnTabSettings = 0
            time.sleep(1)
            self.returnListEvents()
            xbmc.executebuiltin( "Skin.SetString(TabSettings,1)" )
            self.returnTabSettings = 1
            
            self.setFocusId(8801)
 
  
    def onFocus(self, controlID):
        pass

if  __name__ == "__main__":
  
  w = AgendaGUI("default.xml", ROOTDIR, "Default.HD")
  w.doModal()
  del w
