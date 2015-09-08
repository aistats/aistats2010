#!/usr/bin/env python

# File for publishing workshop pages to the web.

import os
import sys
import re
import shutil
import time
import string
import httplib
import datetime
import posix

sys.path.append(os.path.join(posix.environ['HOME'], 'sh'))
import ndlfile
import ndlhtml


# arguments PACKAGENAME VRS AUTHORS
if len(sys.argv) < 2:
    raise "There should be an input argument (workshop short name)."
year = time.strftime('%Y')
timeStamp = time.strftime('%A %d %b %Y at %H:%M')
workshopName = sys.argv[1];
lowerWorkshop = workshopName.lower();
dirName = lowerWorkshop + 'Info'

#workshopHeader.txt contains the pages' headers
workshopHeader = ndlfile.readTxtFile('workshopHeader.txt', dirName)
#workshopFooter.txt contains the pages' footers
workshopFooter = ndlfile.readTxtFile('workshopFooter.txt', dirName)
#workshopStyle.txt contains the pages' style
workshopStyle = ndlfile.readTxtFile('workshopStyle.txt', dirName)

# schedule.txt contains schedule information
scheduleDetails = ndlfile.extractFileDetails('schedule.txt', '|', dirName)
# Write the schedule portion
startDateTuple = time.strptime('12/05/2010', '%d/%m/%Y')
startDate = datetime.datetime(startDateTuple[0], startDateTuple[1], startDateTuple[2])
#endDate = startDate + datetime.timedelta(int(dateDetails[0][1])-1)
curDate = startDate.date()
curTime = datetime.time(0, 0, 0)
scheduleString = '<h1>AISTATS Conference Schedule</h2>\n'
firstTime = True
for i in range(len(scheduleDetails)):
    print scheduleDetails[i][0]
    if scheduleDetails[i][0]=='day':
	oldDate = curDate
        curDate = startDate.date() + datetime.timedelta(int(scheduleDetails[i][1])-1)
        startTimeTuple = time.strptime(scheduleDetails[i][2], '%H:%M')
        curTime = datetime.time(startTimeTuple[3], startTimeTuple[4])
        curDateTime = datetime.datetime.combine(curDate, curTime)
	if not curDate == oldDate or firstTime:
            scheduleString += "<h3>" + curDateTime.strftime('%A') + ' ' + curDateTime.strftime('%d') + ' ' + ' ' + curDateTime.strftime('%B') + '</h3>\n'
            firstTime = False
    else:
        videoLink = scheduleDetails[i][6]
        if videoLink == 'none' or videoLink == 'video':
            videoLink = ''
        slidesFile = scheduleDetails[i][5]
        if slidesFile == 'none' or slidesFile == 'slides':
            slidesFile = ''
        abstractFile = scheduleDetails[i][4]
        if not abstractFile == 'none' and not abstractFile == '' and not abstractFile == 'abstract':
            abstractTxt = ndlfile.readTxtFile(os.path.join(dirName, abstractFile))
        else:
            abstractTxt = ''
        paperPDF = scheduleDetails[i][3]
        talkTitle = scheduleDetails[i][1]
        if talkTitle == 'none' or talkTitle == 'talktitle':
            talkTitle = ''
        if paperPDF == 'paperpdf' or paperPDF == '':
            paperPDF = ''
        authorlist = scheduleDetails[i][2]
        if authorlist == 'none' or authorlist == 'authorlist':
            authorlist = ''
        name = scheduleDetails[i][0]
        startTimeStr = curDateTime.strftime('%H:%M')
        talkLength = datetime.timedelta(0, 0, 0, 0, int(scheduleDetails[i][7]))
        endTime = curDateTime + talkLength
        curDateTime = endTime
        endTimeStr = endTime.strftime('%H:%M')
        scheduleString+='''
<table width="100%">
  <tr>'''
        if int(scheduleDetails[i][7])>0:
            scheduleString+='''
     <td width="20%" ><a name="'''

            scheduleString += scheduleDetails[i][0]
            scheduleString += '"></a>' + startTimeStr + ' - ' + endTimeStr + '</td>\n'
        else:
                        scheduleString+='''
     <td width="20%" ></td>'''

        if len(talkTitle)>0:
            if int(scheduleDetails[i][7])==0:
                talkTitle = '<b>' + talkTitle + '</b>'

            if paperPDF == '':
                scheduleString += '    <td width="90%">' + talkTitle + '\n'
            else:
                scheduleString += '    <td width="90%"><b><a href="./abstract/' + paperPDF + '">' + talkTitle + '</a></b>'
            if len(authorlist)>0:
                scheduleString += '<br><i>' + authorlist + '</i>\n'
            if len(videoLink)>0:
                scheduleString += '[<a href="' + videoLink + '">video</a>]\n'
            if len(slidesFile)>0:
                scheduleString += '[<a href="./slides/' + slidesFile + '">slides</a>]\n'
            scheduleString+= ' </td>\n </tr>\n'
        if len(abstractTxt)>0:
            scheduleString += '''
  <tr>
    <td width="10%" >&nbsp;</td>
    <td width="90%" >
    '''
            scheduleString += abstractTxt
            scheduleString += '</td>\n  </tr>\n'
        scheduleString += '</table>'

ndlhtml.writeToFile('schedule.php', scheduleString, workshopStyle, 'Conference Schedule', workshopHeader, workshopFooter, timeStamp)
