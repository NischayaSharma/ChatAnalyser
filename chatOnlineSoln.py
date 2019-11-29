from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import itertools
import sys
import re


def plot_bar(df):
    # this is for plotting purpose
    index = np.arange(len(df['sender']))
    plt.bar(index, df['numOfTxt'])
    plt.xlabel('Sender', fontsize=13)
    plt.ylabel('No of Texts', fontsize=13)
    plt.xticks(index, df['sender'], fontsize=10, rotation=15)
    plt.title('Texts sent by each sender in the convo')
    plt.show()


def parse_file(text_file):
    file = open(text_file, 'r')
    sender = []
    message = []
    datetime = []
    for eachLine in file:
        if (re.search("^\d+/\d+/\d+, \d+:\d+ \w+ - ", eachLine)):
            data = eachLine
        else:
            data += eachLine
        datetime.append(data.split(' - ')[0])
        if(len(data.split('-')[1].split(':')) > 1):
            s = data.split('-')[1].split(':')[0].strip()
            sender.append(s)
        else:
            sender.append('')
        try:
            message.append(data.split(': ', 1)[1].replace('\n', ' ').strip())
        except:
            message.append('')
    df = pd.DataFrame(zip(datetime, sender, message), columns=[
                      'timestamp', 'sender', 'message'])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df[df.sender != ''].reset_index(drop=True)
    for i in range(len(df.message)):
        if df.iloc[i]['message']== '<Media omitted>':
            df.drop(df.index[i])
            print "hey",df.index[i],i
    print df
    return df


def mssgPerUser(df):
    names = list(df['sender'].unique())
    numOfTxts = []
    for i in range(len(names)):
        numOfTxts.append(0)
    for name in df['sender']:
        numOfTxts[names.index(name)] += 1
    df = pd.DataFrame(zip(names, numOfTxts), columns=['sender', 'numOfTxt'])
    return df


dataDf = parse_file(sys.argv[1])
dataDf['characters'] = dataDf.message.apply(len)
dataDf['words'] = dataDf.message.apply(lambda x: len(x.split()))
dataDf['keywords'] = dataDf.message.apply(lambda x: (x.split()))
# print (dataDf)
stopwords = []
with open("stopwordsHinglish.txt") as file:
    data = file.read()
    stopwords = data

for arr in dataDf['keywords']:
    for keyword in stopwords:
        if (keyword in arr):
            arr.remove(keyword)
# print dataDf

# words = ''
# for i in dataDf.message.values:
#     words += '{} '.format(i.lower()) # make words lowercase

# print (pd.DataFrame(Counter(words.split()).most_common(), columns=['word', 'frequency']))

