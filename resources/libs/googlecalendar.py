# Generate and manipulate the main calendar 

import os
import re
import sys
import urllib
from xbmcaddon import Addon

__addonID__      = "script.calendar"
__settings__     = Addon(id=__addonID__)
__string__       = __settings__.getLocalizedString
__language__     = __settings__

# INITIALISATION CHEMIN RACINE
ROOTDIR = __settings__.getAddonInfo('path')
# Shared resources
BASE_RESOURCE_PATH = os.path.join( ROOTDIR, "resources" )

# append the proper gdata folder to our path
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "libs", "gdata" ) )
# append the proper libs folder to our path
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "libs" ) )

#Google modules
from elementtree import ElementTree
import gdata.calendar.service
import gdata.service
import atom.service
import gdata.calendar
import atom
import getopt
import string
import time


class GoogleCalendar :

    def __init__(self):

        #Init the google calendar
        self.calendar_service = gdata.calendar.service.CalendarService()
        self.calendar_service.email = ''
        self.calendar_service.password = ''
        self.calendar_service.source = 'Google-Calendar_Python_Sample-1.0'
        try : 
          self.calendar_service.ProgrammaticLogin()
        except : pass
        
    ##Google def
    def googleAccountConnect(self , login , password) :
        self.calendar_service = gdata.calendar.service.CalendarService()
        self.calendar_service.email = login
        self.calendar_service.password = password
        self.calendar_service.source = 'Google-Calendar_Python_Sample-1.0'
        try : 
          self.calendar_service.ProgrammaticLogin()
          return True
        except :
          return False
        
    def printUserCalendars(self , calendar_service):
        feed = calendar_service.GetAllCalendarsFeed()
        for i, a_calendar in enumerate(feed.entry):
          pass
          #print '\t%s. %s' % (i, a_calendar.title.text,)
    ##End of google def
        
    def list_calendar_title(self, xml_return_account):
    
        accounts_calendars_title = []
        account_calendars_title = []
        for a in xml_return_account :
          try :
            account_calendars_title = []
            if a['type'] == "Google" :
                
                #connection to the account
                if not self.googleAccountConnect(a['login'] , a['password']) == False :
                    feed = self.calendar_service.GetAllCalendarsFeed()
                    for i, a_calendar in enumerate(feed.entry):
                        #print '\t%s. %s' % (i, a_calendar.title.text,)
                        account_calendars_title.append(a_calendar.title.text)
                        
                accounts_calendars_title.append(account_calendars_title)
          except :
              print "error on loading calendar, check login and password!!!"
            
        return accounts_calendars_title
        
    def return_calendar_id(self, select_calendar_num, login, pwd):
        
        if not self.googleAccountConnect(login , password) == False :
            feed = self.calendar_service.GetAllCalendarsFeed()
            a_calendar = feed.entry[select_calendar_num]
            id = a_calendar.id.text
                
            return id
        else: 
            print "can't connect"
        
    def return_calendar_timezone(self, calendar_id):
                
        #connection to the account
        feed = self.calendar_service.GetAllCalendarsFeed()
        for a_calendar in feed.entry :
            #Extract Calendar ID
            a_calendarId = a_calendar.GetEditLink().href.split('/')[-1].replace('%40','@')
            if a_calendarId == calendar_id :
                timezone = a_calendar.timezone.value
                break
            
        return timezone
        
    def return_calendar_rule(self, select_calendar_num, login, pwd):
        
        if not self.googleAccountConnect(login , password) == False :
            feed = self.calendar_service.GetCalendarAclFeed()
            a_rule = feed.entry[select_calendar_num]
            rule = a_rule.title.text
                
            return rule
        else: 
            print "can't connect"
        
    
    def return_calendar_events(self, login, pwd, calendar, start_date, end_date) :
        
        if not self.googleAccountConnect(login , password) == False :
        
            return_events = []
            
            query = gdata.calendar.service.CalendarEventQuery('default', 'private', 'full')
            query.start_min = start_date
            query.start_max = end_date 
            feed = self.calendar_service.CalendarQuery(query)
            for i, an_event in enumerate(feed.entry):
              #print '\t%s. %s' % (i, an_event.title.text,)
              for a_when in an_event.when:
                e = a_when.start_time [0:10]
                evt = e.split("-")
                evt_code = '%04s%02s%02s' % (evt[0],evt[1],evt[2])
                return_events.append(evt_code)
                  
            return return_events
        else: 
            print "can't connect"
        
    def add_google_calendar(self, title, login, password, color) :
        #Init var
        color = "#" + color[2:]
        if not self.googleAccountConnect(login , password) == False :
            calendar = gdata.calendar.CalendarListEntry()
            calendar.title = atom.Title(text = title)
            calendar.summary = atom.Summary(text='')
            calendar.where  = gdata.calendar.Where(value_string='')
            calendar.color = gdata.calendar.Color(value=color)
            calendar.timezone = gdata.calendar.Timezone(value='UTC')
            calendar.hidden = gdata.calendar.Hidden(value='false')
            #Create the Calendar
            new_calendar = self.calendar_service.InsertCalendar(new_calendar=calendar)
        else: 
            print "can't connect"
 
 
 
 
    def getUserCalendars(self, accountsInfo):
      """Return the list of all calendar in an account.
      List elements contains the title, id, and accesslevel of the calendar, in a dico"""
      
      listCalendars = []
      
      for accountNumber, accountInfo in enumerate(accountsInfo) :
          accountCalendars = []
          
          if accountInfo['type'] == "Google" :
              if not self.googleAccountConnect(accountInfo['login'] , accountInfo['password']) == False :
    
                  #Init string
                  feed = self.calendar_service.GetAllCalendarsFeed()
                
                  for i, a_calendar in enumerate(feed.entry):
                    #Extract Calendar ID
                    userCalendarId = urllib.unquote(a_calendar.GetEditLink().href.split('/')[-1])
                
                    ##Print Calendar Info
                    #print '\tCalendrier #%s :' % (i,)
                    #print '\t\tTitle : %s' % (a_calendar.title.text,)
                    #print  '\t\tID : %s' % (userCalendarId,)
                    #print '\t\tAcessLevel : %s' % (a_calendar.access_level.value,)
                    
                    #Add Calendar Info in the list
                    calendarInfo = {'title' : a_calendar.title.text , 'id' : userCalendarId, 'accesslevel' : a_calendar.access_level.value}
                    accountCalendars.append(calendarInfo)
                    
          listCalendars.append(accountCalendars)
            
      return listCalendars
    
    
    def DateRangeQuery(self, accountsInfo, calendarsInfo, start_date, end_date):
      """Return the list of calendar's events.
      List elements contains the title, description, startdate, stopdate, starttime, stoptime of the event, in a dico"""
      
      listEvents = []
      
      for accountNumber, accountInfo in enumerate(accountsInfo) :
          if accountInfo['type'] == "Google" :
              if not self.googleAccountConnect(accountInfo['login'] , accountInfo['password']) == False :
                  
                      for calendarNumber, calendarFeed in enumerate(calendarsInfo[accountNumber]) :
          
                          #print '\t\tDate range query for events on %s Calendar: %s to %s' % (calendarFeed['title'], start_date, end_date,)
                        
                          if not calendarFeed['accesslevel'] == "freebusy" and calendarFeed['activate'] == "true" :
                        
                            #Print Calendar Info
                            #print '\n\n\tCalendrier %s :' % (calendarFeed['title'],)
                            #print  '\n\t\tID : %s' % (calendarFeed['id'],)
                            #print '\t\tAcessLevel : %s\n' % (calendarFeed['accesslevel'],)
                            
                            query = gdata.calendar.service.CalendarEventQuery(calendarFeed['id'], 'private', 'full')
                            query.start_min = start_date
                            query.start_max = end_date 
                            feed = self.calendar_service.CalendarQuery(query)
                            for i, an_event in enumerate(feed.entry):
                                recurInfo = {}
                                for where in an_event.where:
                                  whereTitle = where.value_string
                                
                                try :
                                    recurrenceText = an_event.recurrence.text
                                except : 
                                    recurrenceText = ""
                                    
                                if recurrenceText != "" :
                                    recurrenceInfos = re.split("\n",recurrenceText)
                                    for recurrenceInfo in recurrenceInfos :
                                        recurrenceInfoArray = re.split(":",recurrenceInfo)
                                        if recurrenceInfoArray[0] == "DTSTART" :
                                            if len(recurrenceInfoArray) > 1 :
                                                recurInfo["startDate"] =  recurrenceInfoArray[1][0:8]
                                                recurInfo["startTime"] =  recurrenceInfoArray[1][9:15]
                                        elif recurrenceInfoArray[0] == "DTEND" :
                                            if len(recurrenceInfoArray) > 1 :
                                                recurInfo["endDate"] =  recurrenceInfoArray[1][0:8]
                                                recurInfo["endTime"] =  recurrenceInfoArray[1][9:15]
                                        elif recurrenceInfoArray[0] == "RRULE" :
                                            if len(recurrenceInfoArray) > 1 :
                                                rrules = recurrenceInfoArray[1]
                                                rruleInfos = re.split(";",rrules)
                                                for rruleInfo in rruleInfos :
                                                    rruleInfoArray = re.split("=",rruleInfo)
                                                    if rruleInfoArray[0] == "FREQ" :
                                                        if len(rruleInfoArray) > 1 :
                                                            recurInfo["freq"] =  rruleInfoArray[1]
                                                    elif rruleInfoArray[0] == "UNTIL" :
                                                        if len(rruleInfoArray) > 1 :
                                                            recurInfo["until"] =  rruleInfoArray[1]
                                    
                                    #print recurInfo     
                                
                                for a_when in an_event.when:
                                
                                  calendarEvent = {"title" : "" , "startdate" : 0 , "enddate" : 0 , "starttime" : 0 , "endtime" : 0 , "description" : "" , "accountnumber" : accountNumber, "calendarnumber" : calendarNumber}
                                  #print '\t\t\t%s. %s' % (i, an_event.title.text,)
                                  calendarEvent['title'] = an_event.title.text
                                  if recurrenceText != "" :
                                      calendarEvent['recurrence'] = recurInfo
                                  
                                  if not an_event.content.text is None :
                                      calendarEvent['comment'] = an_event.content.text
                                  else :
                                      calendarEvent['comment'] = ""
                                  
                                  if calendarFeed['accesslevel'] == "owner" :
                                      calendarEvent['url'] = an_event.GetEditLink().href
                                      calendarEvent['event'] = an_event
                                  
                                  if not whereTitle is None :
                                      calendarEvent['where'] = whereTitle
                                  else :
                                      calendarEvent['where'] = ""
                                
                                  #print '\t\t\t\tStart time: %s' % (a_when.start_time,)
                                  #print '\t\t\t\tEnd time:   %s' % (a_when.end_time,)
                                  
                                  calendarEvent['startdate'] = a_when.start_time.split('T')[0]
                                  calendarEvent['enddate'] = a_when.end_time.split('T')[0]
                                  #print '\t\t\t\tStart time: %s' % (calendarEvent['startdate'])
                                  #print '\t\t\t\tEnd time:   %s' % (calendarEvent['enddate'])
                                  try :
                                      calendarEvent['starttime'] = a_when.start_time.split('T')[1][:5]
                                      calendarEvent['endtime'] = a_when.end_time.split('T')[1][:5]
                                  except : 
                                      calendarEvent['starttime'] = "00:00"
                                      calendarEvent['endtime'] = "00:00"
                                  
                                  listEvents.append(calendarEvent)
                              
              else : 
                  print 'Impossible de se connecter a %s' % (accountInfo['title'])
                  
      return listEvents
    
    
    #Add an Event
    def InsertRecurringEvent(self, calendarInfo, startDate, endDate, title='',
                             content='', where='',
                             recurrence=False, recurDate=""):
                             
        if not self.googleAccountConnect(calendarInfo['login'] , calendarInfo['password']) == False :
        
            event = gdata.calendar.CalendarEventEntry()
            event.title = atom.Title(text=title)
            event.content = atom.Content(text=content)
            event.where.append(gdata.calendar.Where(value_string=where))
        
                  
            if recurrence == 0:
                start_time = time.strftime("%Y-%m-%dT%H:%M:%S.000Z",time.gmtime(time.mktime(time.strptime(startDate,"%Y%m%d%H%M"))))
                end_time = time.strftime("%Y-%m-%dT%H:%M:%S.000Z",time.gmtime(time.mktime(time.strptime(endDate,"%Y%m%d%H%M"))))
                event.when.append(gdata.calendar.When(start_time=start_time, end_time=end_time))
            else :
                recurData = ["","DAILY","WEEKLY","MONTHLY","YEARLY"]
                recurrence_data = ('DTSTART:%s\r\n' % (time.strftime("%Y%m%dT%H%M%S000Z",time.gmtime(time.mktime(time.strptime(startDate,"%Y%m%d%H%M")))))
                  + 'DTEND:%s\r\n' % (time.strftime("%Y%m%dT%H%M%S000Z",time.gmtime(time.mktime(time.strptime(endDate,"%Y%m%d%H%M")))))
                  + 'RRULE:FREQ=%s;UNTIL=%s\r\n') % (recurData[recurrence] , time.strftime("%Y%m%d",time.gmtime(time.mktime(time.strptime(recurDate,"%Y%m%d")))))
                event.recurrence = gdata.calendar.Recurrence(text=recurrence_data)
                
            # Add the event
            feed = '/calendar/feeds/%s/private/full' % (calendarInfo['id'])
            new_event = self.calendar_service.InsertEvent(event, feed)
            
            #print 'New recurring event inserted: %s' % (new_event.id.text,)
            #print '\tEvent edit URL: %s' % (new_event.GetEditLink().href,)
            #print '\tEvent HTML URL: %s' % (new_event.GetHtmlLink().href,)
          
            #return new_event
            return True
            
            
    def UpdateTitle(self, event, calendarInfo, startDate, endDate, title='',
                             content='', where='',
                             recurrence=False, recurDate=""):
                             
        if not self.googleAccountConnect(calendarInfo['login'] , calendarInfo['password']) == False :
        
            event.title = atom.Title(text=title)
            event.content = atom.Content(text=content)
            event.where[0] = gdata.calendar.Where(value_string=where)
        
                  
            if recurrence == 0:
                start_time = time.strftime("%Y-%m-%dT%H:%M:%S.000Z",time.gmtime(time.mktime(time.strptime(startDate,"%Y%m%d%H%M"))))
                end_time = time.strftime("%Y-%m-%dT%H:%M:%S.000Z",time.gmtime(time.mktime(time.strptime(endDate,"%Y%m%d%H%M"))))
                event.when.append(gdata.calendar.When(start_time=start_time, end_time=end_time))
            #else :
            #    recurData = ["","DAILY","WEEKLY","MONTHLY","YEARLY"]
            #    recurrence_data = ('DTSTART:%s\r\n' % (time.strftime("%Y%m%dT%H%M%S000Z",time.gmtime(time.mktime(time.strptime(startDate,"%Y%m%d%H%M")))))
            #      + 'DTEND:%s\r\n' % (time.strftime("%Y%m%dT%H%M%S000Z",time.gmtime(time.mktime(time.strptime(endDate,"%Y%m%d%H%M")))))
            #      + 'RRULE:FREQ=%s;UNTIL=%s\r\n') % (recurData[recurrence] , time.strftime("%Y%m%d",time.gmtime(time.mktime(time.strptime(recurDate,"%Y%m%d")))))
            #    event.recurrence = gdata.calendar.Recurrence(text=recurrence_data)
            
            self.calendar_service.UpdateEvent(event.GetEditLink().href, event)
            
            print 'Updating event' 
            return True
            
            
    
    def DeleteEvent(self, calendarInfo, event):
        if not self.googleAccountConnect(calendarInfo['login'] , calendarInfo['password']) == False :
            self.calendar_service.DeleteEvent(event.GetEditLink().href)
            return True
