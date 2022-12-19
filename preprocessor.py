
import re # re library stands for regular expression 
import pandas as pd
def preprocess(data):
    '''
    this function is Devloped by Adarsh Ambastha 
    the function takes the exported caht data in 25 hours formate and 
    extract all the important information from the chats and arrange it 
    in a proper DataFrame usnig pandas
    the pattern matching is ond eusing RegEx
    and information like message_date
                         message_time
                         User Name   
                         User Message
                         Message_Time
                         Message_month
                         Message_day
                         Hour
                         Minute 
    are stored in a proper columns and then extracted to analyse the data 

    hence the function returns a proper dataframe with all the usefull information extracted from the chats
    '''
    pattern= '\d{1,2}\/\d{1,2}\/\d{1,2},\s\d{1,2}:\d{1,2}\s(?:AM|am|PM|pm)\s-\s'

    message = re.split(pattern,data)[1:]
    dates=re.findall(pattern,data)

    df=pd.DataFrame({'User_Message':message,'message_date':dates})
    # convert message_date type
    df['message_date'] = df['message_date'].str.replace(" ", "")
    df[['Date', 'time']] = df["message_date"].apply(lambda x: pd.Series(str(x).split(",")))
    df['time'] = df['time'].str.replace("-", "")
    df=df.drop(['message_date'],axis=1)

    users=[]
    messages=[]
    for message in df['User_Message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['message']=messages
    df['Names']=users
    df=df.drop(['User_Message'],axis=1)
    
    df['Date']=pd.to_datetime(df['Date'])
    df['year']=df['Date'].dt.year
    df['month']=df['Date'].dt.month_name()
    df['month_num']=df['Date'].dt.month
    df['day']=df['Date'].dt.day
    df['day_name']=df['Date'].dt.day_name()
    
    df=df.drop(['Date'],axis=1)
    time_list=[]
    time_pattern="\d{1,2}:\d{1,2}"
    for message in df['time']:
        time_list.append(re.findall(time_pattern,message))
    df['_time']=time_list
    df['_time'] = [''.join(ele) for ele in df['_time']]
    df['_time']=pd.to_datetime(df['_time'])
    df['Names'] = [''.join(ele) for ele in df['Names']]
    df['hour']=df['_time'].dt.hour
    df['min']=df['_time'].dt.minute
    df=df.drop(['_time'],axis=1)
    
    return df



