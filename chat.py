import re
import time
from tabulate import tabulate


file = open('chatApooh.txt', 'r')
text = ""
line = ""
names = []
numOfTexts = []
convoInit = []
prevTime = 0
prevDate = ""

for eachLine in file:
    if (re.search("^\d+/\d+/\d+, \d+:\d+ \w+ - ", eachLine)):
        text = eachLine[eachLine.index('-')+2:]
        line = eachLine
    else:
        text += eachLine
        line += eachLine
    dateTexted = line.split('-')[0].split(',')[0].strip()
    timeTexted = line.split('-')[0].split(',')[1].strip()
    const = 0
    if (timeTexted.endswith("PM")):
        const = 12
    hrs = str(int(timeTexted.split()[0].split(":")[0] if timeTexted.split()[0].split(":")[0]!="12" else "0" ) + const)
    mins = timeTexted.split()[0].split(":")[1]
    dateTime = dateTexted+" "+hrs+" "+mins
    timeTxt = time.mktime(time.strptime(dateTime,"%m/%d/%y %H %M"))

    if(len(text.split(':')) > 1):
        if(text.split(':')[0] in names):
            numOfTexts[names.index(text.split(':')[0])] += 1
            if(timeTxt-prevTime >= 3600):
                convoInit[names.index(text.split(':')[0])] += 1
                print "Convo init by ",names[names.index(text.split(':')[0])]
        else:
            names.append(text.split(':')[0])
            numOfTexts.append(1)
            convoInit.append(0)

    print (prevTime,  timeTexted, prevDate, dateTexted,dateTime,timeTxt)
    prevDate = dateTexted
    prevTime = timeTxt

table = [names, numOfTexts, convoInit]
print(tabulate(table))
file.close()
