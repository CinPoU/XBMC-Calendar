"""Manipulate events"""

import os
import re
import sys
from xbmc import translatePath

# append the proper libs folder to our path
sys.path.append( os.path.join(sys.modules[ "__main__" ].BASE_RESOURCE_PATH, "libs" ) )

from traceback import print_exc

#For Ics Files
from icalendar import Calendar, vDatetime

from googlecalendar import *




class ReadEvents :

    def __init__(self):
        
        #Call the Google Class
        self.googleCalendar = GoogleCalendar()
        
    
    def findMonthEvts(self, dayList, listCalendar):
        
        #Define the start and end limit
        start = dayList[0]
        end = dayList[-1]
    
        month_evt={}
      
        for n,calendar in enumerate(listCalendar) :
        
            if calendar['activate'] == "true" :
                start_date = '%04d%02d%02d' % (start['year'],start['month'],start['number'])
                end_date = '%04d%02d%02d' % (end['year'],end['month'],end['number'])
        
                print n, calendar
                
                if calendar['typeaccount'] == "google" :
                    start_date = '%04d-%02d-%02d' % (start['year'],start['month'],start['number'])
                    end_date = '%04d-%02d-%02d' % (end['year'],end['month'],end['number'])
                    events = self.googleCalendar.return_calendar_events(calendar['login'], calendar['password'], calendar['url'], start_date, end_date)
                    
                    for e in events :
                        month_evt[e] = "event"
                
                elif calendar['typeaccount'] == "local" :
                    #Traitment of the local iCalendar File
                    url = translatePath ( calendar['url'] )
                    cal = Calendar.from_string(open(os.path.join(url),'rb').read())
                    
                    for evt in cal.walk('VEVENT'):
                        a = '%04d%02d%02d' % (vDatetime.from_ical(evt['dtstart'].ical()).year,vDatetime.from_ical(evt['dtstart'].ical()).month,vDatetime.from_ical(evt['dtstart'].ical()).day)
                        
                        if a >= start_date and a <= end_date:
                        
                            month_evt[a] = "event"
                
                elif calendar['typeaccount'] == "web" :
                    pass
              
        return month_evt