#from app import num_msg
from wordcloud import WordCloud
from urlextract import URLExtract
import pandas as pd
import emoji
from collections import Counter

extract=URLExtract()

def fetch_stats(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    # number of msgs
    num_msg = df.shape[0]

    # number of words
    words = []
    for i in df['message']:
        words.extend(i.split())

    #fetch number of media shared
    num_media=df[df['message']=='<Media omitted>'].shape[0]

    #fetch number of links
    links=[]
    for i in df['message']:
        links.extend(extract.find_urls(i))

    return num_msg, len(words), num_media, len(links)


def fetch_most_busy(df):
    x = df['user'].value_counts()[1:].head()
    y=round((df['user'].value_counts()[1:] / df.shape[0]) * 100, 2).reset_index().rename(columns={'count': 'percent'})
    return x, y

def create_wordcloud(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    wc=WordCloud(width=800, height=400,min_font_size=10,background_color='white')
    df_wc=wc.generate(df['message'].str.cat(sep=' '))
    return df_wc

def common_words(selected_user,df):
    f=open('stop_hinglish.txt','r')
    stop_words=f.read()
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    temp = df[df['user'] != 'Group notification']
    temp = temp[temp['message'] != '<Media omitted>']
    words = []
    for i in temp['message']:
        for j in i.lower().split():
            if j not in stop_words:
                words.append(j)
    from collections import Counter
    most_common=pd.DataFrame(Counter(words).most_common(20)).rename(columns={0: 'word', 1: 'frequency'})

    return most_common

def common_emojis(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]

    emojis = []
    for i in df['message']:
        emojis.extend([c for c in i if emoji.is_emoji(c)])

    common_emoji=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return common_emoji


def month_timeline(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append((timeline['month'][i]) + '-' + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

def daily_timeline(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    d_timeline = df.groupby(['only_date']).count()['message'].reset_index()

    return d_timeline

def week_activity(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    return df['day_name'].value_counts()

def month_activity(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]

    return df['month'].value_counts()




'''
    if selected_user=='Overall':
        #number of msgs
        num_msg=df.shape[0]

        #number of words
        words=[]
        for i in df['message']:
            words.extend(i.split())
        return num_msg,len(words)

        return df.shape[0]
    else:
        df1=df[df['user']==selected_user]
        num_msg=df1.shape[0]
        words=[]
        for j in df1['message']:
            words.extend(j.split())
        return num_msg,len(words)
        '''
