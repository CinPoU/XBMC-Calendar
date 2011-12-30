# -*- coding: utf-8 -*-

from icalendar import Calendar
import os


class IcsCalendar :

    def __init__(self):
        pass
        
    def DateRangeQuery(self, accountsInfo, calendarsInfo, start_date, end_date, tempDir):
        """Return the list of calendar's events.
        List elements contains the title, description, startdate, stopdate, starttime, stoptime of the event, in a dico"""  
        print  accountsInfo, calendarsInfo, start_date, end_date, tempDir
        listEvents = []
        
        for accountNumber, accountInfo in enumerate(accountsInfo) :
            if accountInfo['type'] == "Local" or  accountInfo['type'] == "Web" :
    
                for calendarNumber, calendarFeed in enumerate(calendarsInfo[accountNumber]) :
                        
                  if calendarFeed['activate'] == "true" :
    
                    print '\t\tDate range query for events on %s Calendar: %s to %s' % (calendarFeed['title'], start_date, end_date,)
                  
                    #Print Calendar Info
                    print '\n\n\t\t\tCalendrier %s :' % (calendarFeed['title'])
                    print  '\n\t\t\tID : %s' % (calendarFeed['id'])
            
                    if accountInfo['type'] == "Web" :
                        localPath = os.path.join(tempDir , calendarFeed['id'].strip("/")[-1])
                        try : 
                            urllib.urlretrieve( calendarFeed['id'] , localPath)
                            calendarFeed['id'] = os.path.join(tempDir , calendarFeed['id'].strip("/")[-1])
                        except : "can't download the file"
                    
                    cal = Calendar.from_string(open(str(calendarFeed['id']),'rb').read())
                    
                    for component in cal.walk('vevent'):
                        
                          calendarEvent = {"title" : "" , "startdate" : 0 , "enddate" : 0 , "starttime" : 0 , "endtime" : 0 , "description" : "" , "accountnumber" : accountNumber, "calendarnumber" : calendarNumber}
                          print '\t\t\t%s' % (component['dtstart'])
                          title = component['summary']
                          
                          try : 
                              calendarEvent["title"] = title
                              print calendarEvent["title"]
                          except :
                              pass

                        
                          print '\t\t\t\tStart time: %s' % ( component['dtstart'])
                          print '\t\t\t\tEnd time:   %s' % ( component['dtend'])
                          
                          calendarEvent['startdate'] = str(component['dtstart']).split('T')[0]
                          calendarEvent['startdate'] = calendarEvent['startdate'][:4] + "-" + calendarEvent['startdate'][4:6] + "-" + calendarEvent['startdate'][6:8]
                          calendarEvent['enddate'] = str(component['dtend']).split('T')[0]
                          calendarEvent['enddate'] = calendarEvent['enddate'][:4] + "-" + calendarEvent['enddate'][4:6] + "-" + calendarEvent['enddate'][6:8]
                          print '\t\t\t\tStart time: %s' % (calendarEvent['startdate'])
                          print '\t\t\t\tEnd time:   %s' % (calendarEvent['enddate'])
                          try :
                              calendarEvent['starttime'] = str(component['dtstart']).split('T')[1][:4]
                              calendarEvent['starttime'] = calendarEvent['starttime'][:2] + ":" + calendarEvent['starttime'][2:]
                              calendarEvent['endtime'] = str(component['dtend']).split('T')[1][:4]
                              calendarEvent['endtime'] = calendarEvent['endtime'][:2] + ":" + calendarEvent['endtime'][2:]
                          except : 
                              calendarEvent['starttime'] = "00:00"
                              calendarEvent['endtime'] = "00:00"
                          
                          listEvents.append(calendarEvent)
                          
        return listEvents