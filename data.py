# data.py
# David Li
# Contains three classes that represent all of the data on call options and put options

import os
import matplotlib.pyplot
import matplotlib.dates

class Data(object):
    """An instance of Data corresponds to a file of quote data.
    Each instance stores the date of the trading, the number of call options
    traded that day, the number of put options traded that day, and the top 5
    traded call and put options."""
    
    """Instance attributes:
        _date [string]: the date of the trading
        _call [int]: the number of call options traded
        _put [int]: the number of put options traded
        _topcall [list of Option]: the top 5 traded call options
        _topput [list of Option]: the top 5 traded put options
    """
    
    def __init__(self, d, c, p, tc, tp):
        """Initializes an instance of class Data.
        Must provide the date, number of call options, and number of put options"""
        self._date = d
        self._call = c
        self._put = p
        self._topcall = tc
        self._topput = tp
    
    
    def getDate(self):
        """Returns the date of the trading."""
        return self._date
    
    
    def getCall(self):
        """Returns the number of call options."""
        return self._call
    
    
    def getPut(self):
        """Returns the number of put options."""
        return self._put
    
    
    def getTopCall(self):
        """Returns a list of the top 5 traded call options."""
        return self._topcall
    
    
    def getTopPut(self):
        """Returns a list of the top 5 traded put options."""
        return self._topput
    
    
    def _printOptions(self, options):
        """Returns the list of Option in printable format."""
        s = ''
        for op in options:
            s = s + op.getName() + ', '
        s = s.strip()
        s = s[:-1]
        return s
    
    
    def __str__(self):
        """Returns the string representation of a Data object in the form:
        _date; call: _call; put: _put"""
        return (self._date + '\ncall: ' + str(self._call) + '\nput:' + str(self._put) +
                '\ntop call: ' + self._printOptions(self._topcall) + '\ntop put: ' + self._printOptions(self._topput)) + '\n'
    

class Option(object):
    """An instance of Option is a call option or a put option."""
    
    """Instance Attributes:
        _name [string]: name of the option
        _amt [int]: amount of option traded
    """
    
    def __init__(self, name, amt):
        """Initializes _name and _amt for the option."""
        self._name = name
        self._amt = amt
    
    
    def getName(self):
        """Returns the name of the option."""
        return self._name
    
    
    def getAmt(self):
        """Returns the amount traded of the option."""
        return self._amt


class Dataset(object):
    """An instance of Dataset contains all of the data from all of the files of quote data."""
    
    """Instance Attributes:
        _datalist [list of directories]: contains all of the files of data
        _alldata [list of Data objects]: contains all of the data
        _option [string]: the option that is being analyzed
    """
    CALL_COMMAS = 5     #the number of commas in each line before the Vol of call options
    PUT_COMMAS = 12     #the number of commas in each line before the Vol of put options
    
    def __init__(self, folder, option):
        """Initializes _alldata and _datalist for the given folder"""
        self._option = option
        self._datalist = self.makeDatalist(folder)
        assert len(self._datalist) > 0, 'Not a valid option name'       # makes sure that the option name is valid
        self._alldata = self.readData()
    
    
    def getData(self):
        """Returns _alldata, the list of all the Data objects."""
        return self._alldata
    
    
    def getDatalist(self):
        """Returns _datalist, the list of data files."""
        return self._datalist
    
    
    def getOption(self):
        """Returns _option, the name of this option."""
        return self._option
    
    def clearData(self):
        """Clears all of the data and data files."""
        self._alldata = []
        self._datalist = []
    
    
    def makeDatalist(self, folder):
        """Returns the list of data files in the folder."""
        templist = os.listdir(folder)
        templist = self._removeNonData(templist)
        return templist
    
    
    def _removeNonData(self, templist):
        """Removes the files from templist that are not data files of _option."""
        n=0
        while n < len(templist):
            dataname = templist[n]
            if not (dataname[:9] == 'QuoteData'):
                templist.remove(dataname)
            else:
                data = open(dataname)
                line = data.readline()
                data.close()
                temp = line[:line.find(' ')]
                if not (temp == self._option):
                    templist.remove(dataname)
                else:
                    n+=1
        return templist
    
    
    def readData(self):
        """Reads each data file in the folder.
        Creates a Data object for each file.
        Puts all of the Data objects into _alldata"""
        tempdata = []
        for dataname in self._datalist:
            topcall = []
            topput = []
            data = open(dataname)
            #newdata = open('new' + dataname, 'w')
            lines = data.readlines()
            date = self._getDate(lines[1][:11])
            call = 0
            put = 0
            for i in range(3,len(lines)):
                thisline = lines[i]
                loc = thisline.find('-')
                aloc = thisline.find('ASHR')
                if (loc != aloc+11) and (loc != aloc+13):  
                    assert loc != 25                    #two assert checks in place for now because '-' is always at index 25 or 27...
                    assert loc != 27                    #...if this changes in the future then this will throw an AssertionError and I will fix it.
                    #newdata.write(thisline)
                    callName = self._findCallOptionName(thisline)
                    callCommas = self._findCommas(thisline, self.CALL_COMMAS)
                    thisCall = int(thisline[callCommas[0]+1 : callCommas[1]])
                    call += thisCall
                    callOption = Option(callName, thisCall)
                    if len(topcall) < 5:
                        topcall.append(callOption)
                        toppcall = self._sort(topcall)
                    elif (callOption.getAmt() > topcall[0].getAmt()):
                        topcall[0] = callOption
                        toppcall = self._sort(topcall)
                    
                    putName = self._findPutOptionName(thisline)
                    putCommas = self._findCommas(thisline, self.PUT_COMMAS)
                    thisPut = int(thisline[putCommas[0]+1 : putCommas[1]])
                    put += thisPut
                    putOption = Option(putName, thisPut)
                    if len(topput) < 5:
                        topput.append(putOption)
                        topput = self._sort(topput)
                    elif (putOption.getAmt() > topput[0].getAmt()):
                        topput[0] = putOption
                        topput = self._sort(topput)
            tempdata.append(Data(date, call, put, topcall, topput))
            data.close()
            #newdata.close()
        return tempdata
    
    
    def _getDate(self, old_date):
        """Returns the date in the format: month/day/year"""
        month = old_date[:3]
        monthdict = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06',
                     'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}
        new_date = monthdict[month] + '/' + old_date[4:6] + '/' + old_date[7:]
        return new_date

    
    def _findCallOptionName(self, thisline):
        """Find the name of the call option in thisline.
        This is done by finding the string between the 1st and 2nd parentheses"""
        first = thisline.find('(')
        second = thisline.find(')')
        return thisline[first+1: second]
    
    
    def _findPutOptionName(self, thisline):
        """Find the name of the put option in thisline.
        This is done by finding the string between the 3rd and 4th parentheses"""
        first = thisline.find('(')
        first = thisline.find('(', first+1)
        second = thisline.find(')')
        second = thisline.find(')', second+1)
        return thisline[first+1: second]
    
    
    def _findCommas(self, thisline, n):
        """Find the nth and (n+1)th comma in the string thisline.
        This is used to find the vol of call and put options in each line of data.
        first: the comma before the vol
        second: the comma after the vol"""
        
        first = thisline.find(',')
        while n > 1:
            first = thisline.find(',', first+1)
            n-=1
        second = thisline.find(',', first+1)
        return [first, second]
    
    
    def _sort(self, options):
        """Sorts a list of Option in ascending order according to traded amount."""
        for i in range(len(options)):
            j = i
            while(j>0) and (options[j].getAmt() < options[j-1].getAmt()):
                k = options[j]
                options[j] = options[j-1]
                options[j-1] = k
                j-=1
        return options
    
    
    def plotData(self):
        """Plots the data."""
        dates = []
        calls = []
        puts = []
        for data in self._alldata:
            tempdate = matplotlib.dates.datestr2num(data.getDate())
            dates.append(tempdate)
            calls.append(data.getCall())
            puts.append(data.getPut())
        matplotlib.pyplot.plot_date(dates, calls, 'b', label = 'Call Options')
        matplotlib.pyplot.plot_date(dates, puts, 'r', label = 'Put Options')
        matplotlib.pyplot.legend(loc = 2)
        matplotlib.pyplot.xlabel('Dates')
        matplotlib.pyplot.ylabel('Call Options & Put Options')
        matplotlib.pyplot.show()
    
    
    def __str__(self):
        """Returns the string representation of an instance of Dataset."""
        s = '\n'
        for data in self._alldata:
            s = s + data.__str__() + '\n'
        return s