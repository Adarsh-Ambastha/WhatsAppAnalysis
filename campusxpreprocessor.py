import re # re library stands for regular expression 
import pandas as pd
def preprocess(data):
    '''
    this function is Devloped by CampusX Youtube
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
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'User_Message': messages, 'message_date': dates})
    # convert message_date type
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %H:%M - ')

    df.rename(columns={'message_date': 'Date'}, inplace=True)

    users = []
    messages = []
    for message in df['User_Message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])
    df['Names'] = users
    df['message'] = messages
    df.drop(columns=['User_Message'], inplace=True)
    df['year'] = df['Date'].dt.year
    df['month_num'] = df['Date'].dt.month
    df['month'] = df['Date'].dt.month_name()
    df['day'] = df['Date'].dt.day
    df['day_name'] = df['Date'].dt.day_name()
    df['hour'] = df['Date'].dt.hour
    df['minute'] = df['Date'].dt.minute
    return df