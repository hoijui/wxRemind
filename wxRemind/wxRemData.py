#!/usr/bin/python
# $Id: wxRemData.py 14 2006-05-09 12:20:50Z dag $ 

import sys, datetime, re, commands
from wxRemConfig import zerominutes, twelvehour, reminders, remind

class RemData:

    leadingzero = re.compile(r'^0')

    nummonths = 4
    if twelvehour:
        timefmt = "%I:%M%p"
        indent1 = 9
        indent2 = 17
    else:
        indent1 = 7
        indent2 = 13
        timefmt = "%H:%M"

    datefmt = "%a %d %b %Y"
    regat = re.compile(r'\s+at.*$')
    data = {}
    nextdate = ''
    searchstr = ''
    oneday = datetime.timedelta(days=1)

    def _init__(self):
        self.getMonths()

    def getMonths(self):
        self.data = {}
        today = datetime.date.today()
        year, month = map(int, today.strftime("%Y %m").split())
        if month == 1:
            startmonth = 12
            startyear = year - 1
        else:
            startmonth = month - 1
            startyear = year
        self.slurp(startyear, startmonth, self.nummonths)

    def getDay(self, y, m, d):
        year, month, day = map(int, (y,m,d))
        requesteddate = datetime.date(year,month,day)
        self.shortremdate = requesteddate.strftime("%d %m")
        if not self.data.has_key(year) or not self.data[year].has_key(month):
            # print "getting data for %s-%s" % (year, month)
            self.slurp(y,m,1)
        # print "showing data for %d-%d-%d" % (year, month, day)
        try:
            retval = self.data[year][month][day]
        except:
            retval = [["", "", "", "Nothing scheduled", "", ""]]
        return retval

    def getMonthlyDurations(self, y, m):
        year, month = map(int, (y, m))
        busy = {}
        if not self.data.has_key(year) or not self.data[year].has_key(month):
            self.slurp(y,m,1)
        if self.data.has_key(year) and self.data[year].has_key(month):
            for day in self.data[year][month].keys():
                minutes = 0
                for event in self.data[year][month][day]:
                    minutes += event[6]
                busy.setdefault(day, minutes)
        return busy

    def slurp(self, y, m, n):
        startyear, startmonth, months = map(int, (y, m, n))
        # Slurp remind output for the relevant date and number of months
        startdate = datetime.date(startyear,startmonth,1).strftime("%b %Y")
        command = "%s -b2 -rls%s %s %s" % (remind, months, reminders, startdate)
        lines = commands.getoutput(command).split('\n')
        linenum = 0 
        filename = ''
        for line in lines:
            parts = line.split()
            if len(parts) == 0:
                continue
            if parts[1] == "fileinfo":
                linenum, filename = parts[2:4]
                # go to the next line for the item details
                continue
            year, month, day = map(int, parts[0].split('/'))
            date = datetime.date(year, month, day).strftime(self.datefmt)
            durationminutes, startminutes = parts[3:5]
            if startminutes != "*":
                startminutes = int(startminutes)
                starttime = datetime.datetime(year,month,day,
                        startminutes/60,startminutes%60)
                if durationminutes != "*":
                    durationminutes = int(durationminutes)
                    durationdelta = datetime.timedelta(hours=durationminutes/60,
                            minutes=durationminutes%60)
                    end = starttime + durationdelta
                    endtime = end.strftime(self.timefmt)
                    if twelvehour:
                        endtime = self.leadingzero.sub(' ', endtime)
                else:
                    endtime = ''
                    durationminutes = zerominutes
                starttime = starttime.strftime(self.timefmt)
                if twelvehour:
                    starttime = self.leadingzero.sub(' ', starttime)
            else:
                starttime = ''
                endtime = ''
                durationminutes = zerominutes
            if starttime and endtime:
                interval = "-"
            else:
                interval = ""
            msg = " ".join(parts[5:])

            # The following creates a value for data[year][month][day] creating
            # year, month and day keys when necessary.  Is this cool or what?
            self.data.setdefault(year,{}).setdefault(month,{}).setdefault(day,
                    []).append([starttime,  # 0
                        interval,           # 1
                        endtime,            # 2
                        msg,                # 3
                        filename,           # 4
                        linenum,            # 5
                        durationminutes,    # 6
                        ])

    def firstOccurance(self, str):
        if not self.nextdate:
            next = datetime.date.today().strftime("%d %b %Y")
            self.nextdate = self.leadingzero.sub('', next)
        self.searchstr = str
        command = "%s -b2 -n %s | grep -i %s | sort" % (remind, reminders, str)
        return self.nextOccurance()

    def nextOccurance(self):
        if self.nextdate and self.searchstr:
            command = "%s -b2 -n %s %s | grep -i %s | sort" % \
                    (remind, reminders, self.nextdate, self.searchstr)
            line = commands.getoutput(command)
            if len(line) > 0:
                parts = line.split()
                year, month, day = map(int, parts[0].split('/'))
                date = datetime.date(year, month, day)
                next = (date + self.oneday).strftime("%d %b %Y")
                self.nextdate = self.leadingzero.sub('', next) 
                msg = "%s" % self.regat.sub('', " ".join(parts[1:]))
                return (year, month, day, msg)
            else:
                return None
        else:
            return None

if __name__ == "__main__":
    if len(sys.argv) == 4:
        y,m,d = sys.argv[1:4]
    else:
        today = datetime.date.today()
        y, m, d = today.strftime("%Y %m %d").split()
    mydata = RemData()
    y,m,d = map(int, (y,m,d))
    fmt = "%%a %s %%b %%Y" % d
    print "%s:" % datetime.date(y,m,d).strftime(fmt)
    for event in mydata.getDay(y,m,d):
        str = " ".join(event[:-3])
        print "  %s" % str
