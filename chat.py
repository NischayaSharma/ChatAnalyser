import re
import time
import numpy as np
from tabulate import tabulate
from matplotlib import pyplot as plt
from scipy.stats import gaussian_kde

fileName = raw_input("Enter the file name: ")
file = open(fileName, 'r')
text = ""
line = ""
names = []
numOfTexts = []
convoInit = []
xDays = []
yHrs = []
dictDays = {0: "Monday", 1: "Tuesday", 2: "Wednesday",
            3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}
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
    hrs = str(int(timeTexted.split()[0].split(":")[0] if timeTexted.split()[
              0].split(":")[0] != "12" else "0") + const)
    mins = timeTexted.split()[0].split(":")[1]
    dateTime = dateTexted+" "+hrs+" "+mins
    txtInfo = time.strptime(dateTime, "%m/%d/%y %H %M")
    timeTxt = time.mktime(txtInfo)
    xDays.append(dictDays[txtInfo[6]])
    yHrs.append((int(hrs)*60)+(int(mins)))

    if(len(text.split(':')) > 1):
        if(text.split(':')[0] in names):
            numOfTexts[names.index(text.split(':')[0])] += 1
            if(timeTxt-prevTime >= 3600):
                convoInit[names.index(text.split(':')[0])] += 1
        else:
            names.append(text.split(':')[0])
            numOfTexts.append(1)
            convoInit.append(0)

    prevDate = dateTexted
    prevTime = timeTxt

table = [names, numOfTexts, convoInit]
print(tabulate(table))
plt.scatter(yHrs,xDays)
plt.show()
file.close()
