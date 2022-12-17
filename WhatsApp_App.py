# Importing all the Important Libraries 
from tkinter import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import streamlit as st
import preprocessor,helper
import re
import campusxpreprocessor
#The Main Heading of the project on Side bar 
st.sidebar.title("WhatsApp Char Analyzer")
pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
#Uploding the chat from the device in txt formate only
uploaded_file = st.sidebar.file_uploader("Choose a file",type=['txt'])
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode('utf-8')
    # checking which formate data is passsed in the text box if the timeline is in am or pm then  preproecessor will run else campusxpreprocessor will run
    if re.match(pattern,data):
        df=campusxpreprocessor.preprocess(data) 
    else:   
        df=preprocessor.preprocess(data)
    

    #Fetching All the Users
    name_list=df['Names'].unique().tolist()
    name_list.remove('group_notification')
    name_list.sort()
    name_list.insert(0,"OverAll")
    #making a sideBar selctbox to select the user in whcih we want to perform the analysis
    selected_user=st.sidebar.selectbox("Show Analysis With Respect To, Names",name_list)
    
    #A button on clicking whihc analysis will start
    if st.sidebar.button("Show Analysis"):

        #Fetch_stats function which will return the total number of messages, media ,words and links shared
        num_messages,words,num_media_messages,links=helper.fetch_stats(selected_user,df)
        
        #putting title to the Top Statistics value
        st.title('Top Statistics')
        #deviding the page in 4 columns
        col1,col2,col3,col4=st.columns(4)
        
        #col1 showing total Number of messages in the chat
        
        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        #col2 showing total Number of Words in the chat

        with col2:
            st.header("Total Word")
            st.title(words)

        #col3 showing total Number of media File Shared in the chat

        with col3:
            st.header("Total Media File")
            st.title(num_media_messages)

        #col4 showing total Number of Links in the chat

        with col4:
            st.header("Total Links")
            st.title(links)


        #Monthly_TimeLine
        #setting the header to monthly timeline
        st.title("Monthly TimeLine")

        #calling monthly_timeline Function 
        timeline=helper.monthly_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color='purple')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

    #Activity map
        st.title('Activity Map')
        col1,col2=st.columns(2)
        with col1:
            st.header('Most Busy Day:')
            busy_day=helper.week_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        
        with col2:
            st.header('Most Busy Month:')
            busy_month=helper.month_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        if selected_user=='OverAll':
            st.title('Busy User')
            x,new_df=helper.fetch_most_busy_user(df)
            fig,ax=plt.subplots()
            # ax=plt.bar()
            col1,col2=st.columns(2)
            with col1:
                ax.bar(x.index,x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

            # st.title(x)

    #Word Cloud
        st.title("Word Cloud")
        df_wc=helper.create_word_cloud(selected_user,df)
        # plt.savefig("mygraph.png")
        matplotlib.use('TkAgg')
        # plt.axis("off")
        plt.imshow(df_wc)
        plt.show()

    #Finding the most common word
        st.title("Most common words")
        most_common_df=helper.most_common_words(selected_user,df)
        fig,ax = plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        st.pyplot(fig)
        plt.xticks(rotation='vertical')
        
    #Finding Numeber of emojies 
        st.title('Emoji Analysis')
        emoji_df=helper.emoji_helper(selected_user,df)
        

        col1,col2=st.columns(2)
        with col1:
            st.dataframe(emoji_df.head(5))
        with col2:
            fig,ax=plt.subplots()
            ax.pie(emoji_df[1].head(5),labels=emoji_df[0].head(5))
            st.pyplot(fig)
            plt.close()