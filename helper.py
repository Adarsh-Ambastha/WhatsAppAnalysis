import emoji
import matplotlib.pyplot as plt
from wordcloud import WordCloud,STOPWORDS  
from urlextract import URLExtract
import pandas as pd
from collections import Counter
extractor=URLExtract()
def fetch_stats(selected_user,df):
    if selected_user != 'OverAll':
        #1 Number of Words 
        df=df[df['Names']== selected_user]
        
        #1 fetching Number oF Messages
    num_messages=df.shape[0]
    words=[]
    for message in df['message']:
        words.extend(message.split())
    
    num_media_message=df[df['message'] == '<Media omitted>\n'].shape[0]

    links=[]
    for message in df['message']:
        
        links.extend(extractor.find_urls(message))
    

    return num_messages,len(words),num_media_message,len(links)
    
def fetch_most_busy_user(df):
    x=df['Names'].value_counts().head()
    df=round((df['Names'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':"Name",'Names':'Percentage'})

    return x,df

def create_word_cloud(selected_user,df):
    f=open('hinglish.txt','r')
    stop_word=f.read()
    if selected_user!='OverAll':
        df=df[df['Names']==selected_user]

    temp=df[df['Names']!='group_notification']
    temp=temp[temp['message']!='<Media omitted>\n']

    def remove_stop_words(message):
        y=[]
        for word in message.lower().split():
            if word not in stop_word:
                y.append(word)
            return " ".join(y)
    messgae_list=[]
    messgae_list.extend(temp['message'])
    message_string=" ".join([str(elem) for elem in messgae_list])
    wc= WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['message']=temp['message'].apply(remove_stop_words)
    df_wc=wc.generate(message_string)
    return df_wc

def most_common_words(selected_user,df):
    f=open('A:\Krish_nayak\WhatsApp Chat Analysis\hinglish.txt','r')
    stop_word=f.read()
    if selected_user!='OverAll':
        df=df[df['Names']==selected_user]

    temp=df[df['Names']!='group_notification']
    temp=temp[temp['message']!='<Media omitted>\n']
    words=[]
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_word:
                words.append(word) 
    
    most_common_df= pd.DataFrame(Counter(words).most_common(10))
    # most_common_df.columns['Word','Frequency']

    return most_common_df

def emoji_helper(selected_user,df):
    if selected_user!='OverAll':
        df=df[df['Names']==selected_user]
    emojis=[]
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user!='OverAll':
        df=df[df['Names']==selected_user]
    timeline=df.groupby(['year','month_num','month']).count()['message'].reset_index()
    time=[]
    for i in range(len(timeline)):
        time.append(timeline.loc[i,'month']+ "-" + str(timeline.loc[i,'year']))

    timeline['time']=time
    return timeline

def week_activity_map(selected_user,df):
    if selected_user!='OverAll':
        df=df[df['Names']==selected_user]
    return df['day_name'].value_counts()


def month_activity_map(selected_user,df):
    if selected_user!='OverAll':
        df=df[df['Names']==selected_user]
    return df['month'].value_counts()
    
