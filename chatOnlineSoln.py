import pandas as pd
import re

def parse_file(text_file):
    file = open(text_file, 'r')
    sender = []; message = []; datetime = []
    for eachLine in file:
        if (re.search("^\d+/\d+/\d+, \d+:\d+ \w+ - ", eachLine)):
            data = eachLine
        else:
            data += eachLine

        datetime.append(data.split(' - ')[0])
        if(len(data.split('-')[1].split(':'))>1):
            s = data.split('-')[1].split(':')[0].strip()
            sender.append(s)
        else:
            sender.append('')
        try:
            message.append(data.split(': ', 1)[1].replace('\n',' '))
        except:
            message.append('')
    df = pd.DataFrame(zip(datetime, sender, message), columns=['timestamp', 'sender', 'message'])
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # remove events not associated with a sender
    df = df[df.sender != ''].reset_index(drop=True)
    
    return df

dataDf = parse_file(raw_input("Enter the filename: "))
print dataDf