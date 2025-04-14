import re
import pandas as pd

def preprocess(data):
    pattern = '(\d{2}/\d{2}/\d{2}, \d{1,2}:\d{2}\u202f?[apm]{2}) - (.+)'
    messages = re.split(pattern, data)[1:]
    dates = []
    msgs = []
    for i in range(1, len(messages) + 1, 3):
        m = messages[i]
        d = messages[i - 1]
        msgs.append(m)
        dates.append(d)
    df = pd.DataFrame({'user_message': msgs, 'message_date': dates})
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M %p')
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # separate user and msg

    user = []
    message = []
    for msg in df['user_message']:
        entry = re.split('([\w\W]+?): ', msg)
        if entry[1:]:
            user.append(entry[1])
            message.append(entry[2])
        else:
            user.append('Group notification')
            message.append(entry[0])
    df['user'] = user
    df['message'] = message
    df.drop(columns=['user_message'], inplace=True)
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num']=df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['day_name']=df['date'].dt.day_name()
    df['only_date'] = df['date'].dt.date
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    return df