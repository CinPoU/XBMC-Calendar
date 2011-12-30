# Generate and manipulate the main calendar 

import os
import re
import sys
import xbmc

#calendar modules
import time
import datetime
import calendar

from traceback import print_exc
from xbmcaddon import Addon

__addonID__      = "script.calendar"
__settings__     = Addon(id=__addonID__)
__string__       = __settings__.getLocalizedString
__language__     = __settings__

# INITIALISATION CHEMIN RACINE
ROOTDIR = __settings__.getAddonInfo('path')

try:
    from xbmcaddon import Addon

    __settings__ = Addon( id="script.calendar" )
    __language__ = __settings__.getLocalizedString
    print "Mode AddOn ON"


except : 
    __settings__ = xbmc.Settings(ROOTDIR)
    __language__ = xbmc.getLocalizedString
    print "Mode plugin ON"


firstWeekDay = __settings__.getSetting("fwday")
print firstWeekDay

if firstWeekDay == "true" :
    calendar.setfirstweekday(6)
else :
    calendar.setfirstweekday(0)


class Agenda :

    def __init__(self):
         
       
        self.monthName = calendar.month_name 
                
                
        #Today :
        self.today = datetime.date.today()
        #Break the data
        current = re.split('-', str(self.today))
        self.current_no = int(current[1])
        self.current_month = self.monthName[self.current_no]
        self.current_day = int(re.sub('\A0', '', current[2]))
        self.current_yr = int(current[0])
        #Display the today's date :
        self.today_text = '%s %s %s' %(self.current_day, self.current_month, self.current_yr)
        
        #Selected month
        self.year = self.current_yr
        self.month_no = self.current_no
        self.prev_year = 0
        self.next_year = 0
        self.prev_month_no = 0
        self.next_month_no = 0
        self.dayList = []
        
        #self.mainCalendar = self.set_container_days ()  
        
    def set_container_days (self) :
        
        try :
            self.dayList = []
        
            #Find prev year
            if self.month_no == 1 :
                self.prev_year = self.year-1
            else :
                self.prev_year = self.year
        
            #Find prev month
            if self.month_no == 1 :
                self.prev_month_no = 12
            else :
                self.prev_month_no = self.month_no-1
        
            #Display the number of weeks in the prev month
            prev_month = calendar.monthcalendar(self.prev_year, self.prev_month_no)
            prev_nweeks = len(prev_month)
            
        
            #Find next year
            if self.month_no == 12 :
                self.next_year = self.year+1
            else :
                self.next_year = self.year
        
            #Find next month
            if self.month_no == 12 :
                self.next_month_no = 1
            else :
                self.next_month_no = self.month_no+1
        
            #Display the number of weeks in the next month
            self.next_month = calendar.monthcalendar(self.next_year, self.next_month_no)
            
            #Display the month's information
            month = calendar.monthcalendar(self.year, self.month_no)
            nweeks = len(month)
            if month[-1][-1] == 0 :
                n = 1
            else :
                n = 0
            
            if nweeks < 6 :
              month.append(self.next_month[n])
            if nweeks < 5 :
              month.append(self.next_month[n+1])
            
            #Display the days of the current month
            item_pos = 0 
            for w in range(0,6):
                week = month[w]
                for x in xrange(0,7):
                    day = week[x]
                    today = 0
                    if x == 5 or x == 6:
                        daytype = 'weekend'
                    else:
                        daytype = 'day'
                    # Previous month days      
                    if day == 0 and w==0:
                        daytype = 'previous'
                        prev_week =  prev_month[prev_nweeks-1]
                        day = prev_week[x] 
                        daymonth = self.prev_month_no
                        year = self.prev_year
                    # Next month days then the month contain 5 weeks
                    elif w == 4 and nweeks == 4:
                        daytype = 'next'
                        day = week[x]
                        daymonth = self.next_month_no
                        year = self.next_year
                    # Next month days then the month contain 4 weeks
                    elif w == 5 and nweeks <= 5:
                        daytype = 'next'
                        day = week[x]
                        daymonth = self.next_month_no
                        year = self.next_year
                    # Next month days        
                    elif day == 0:
                        daytype = 'next'
                        next_week =  self.next_month[0]
                        day = next_week[x]
                        daymonth = self.next_month_no
                        year = self.next_year
                    # Today
                    elif day == self.current_day and self.month_no == self.current_no and self.year == self.current_yr :
                        daytype = "today"
                        daymonth = self.month_no
                        year = self.year
                    # Current days
                    else:
                        daytype = 'current'
                        daymonth = self.month_no
                        year = self.year
                        
                    self.dayList.append({'number' : day , 'month' : daymonth , 'year' : year , 'type' : daytype})
            
        except :
            print "err. month", type( month ), month
            print_exc()
            
        return self.dayList
        
    def get_month_name(self) :
        month_text = '%s %s' % (self.monthName[self.month_no], self.year)
        return month_text
        
    def get_month_parm(self) :
        return self.month_no ,  self.year
        
    def get_next_month(self) :
        self.year = self.next_year
        self.month_no = self.next_month_no
        self.set_container_days()
        
    def get_prev_month(self) :
        self.year = self.prev_year
        self.month_no = self.prev_month_no
        self.set_container_days()
        
    def get_next_day(self, eventDay) :
        print time.strptime(eventDay,"%Y%m%d")
        print time.mktime(time.strptime(eventDay,"%Y%m%d"))
        date1 = datetime.date.fromtimestamp(time.mktime(time.strptime(eventDay,"%Y%m%d")))
        timedelta = datetime.timedelta(1)
        date2 = date1 + timedelta
        print date2.strftime('%Y%m%d')
        return date2.strftime('%Y%m%d')
        
    def get_event_time_range(self) :
        startTime = '%04d-%02d-%02d' % (int(self.dayList[0]['year']) , int(self.dayList[0]['month']),int(self.dayList[0]['number'])  )
        stopTime = '%04d-%02d-%02d' % (int(self.dayList[-1]['year']) , int(self.dayList[-1]['month']),int(self.dayList[-1]['number'])  )
        eventRange = {'start' : startTime , 'end' : stopTime}
        return eventRange

    def returnDateTitle(self, dateNum, monthName, dayName) :
        dateNum = dateNum.split("-")
        #Today :
        todayInfo = re.split('-', str(self.today))
        if dateNum[0] == todayInfo[0] and dateNum[1] == todayInfo[1] and  dateNum[2] == todayInfo[2] :
            return "today"
        else :
            dayNum = calendar.weekday(int(dateNum[0]) , int(dateNum[1]) , int(dateNum[2]))
            dayTitle = dayName[dayNum]
            monthTitle = monthName[int(dateNum[1])]
            
            return dayTitle + " " + dateNum[2] + " " + monthTitle + " " + dateNum[0]
        

