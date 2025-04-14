import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt

from helper import common_emojis

#from helper import most_common_words

st.sidebar.title('Whatsapp Chat Analyzer')

uploaded_file=st.sidebar.file_uploader('choose a file')
if uploaded_file is not None:
    bytes_data=uploaded_file.getvalue()
    data=bytes_data.decode('utf-8')
    #st.text(data)
    df=preprocessor.preprocess(data)

    #st.dataframe(df)

    #fetch unique users

    user_list=df['user'].unique().tolist()
    user_list.remove('Group notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user=st.sidebar.selectbox("Show Analysis with respect to",user_list)

    if st.sidebar.button('Show Analysis'):
        num_msg,words,num_media,num_links=helper.fetch_stats(selected_user,df)
        st.title('TOP STATISTICS')
        col1,col2,col3,col4=st.columns(4)

        with col1:
            st.header("Messages")
            st.title(num_msg)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header('Media Shared')
            st.title(num_media)

        with col4:
            st.header("Links Shared")
            st.title(num_links)

        #monthly timeline
        st.title('Monthly Timeline')
        timeline=helper.month_timeline(selected_user,df)
        fig,ax=plt.subplots()
        plt.plot(timeline['time'], timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #daily timeline
        st.title('Daily Timeline')
        d_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        plt.plot(d_timeline['only_date'], d_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #activity map
        st.title('Weekly Timeline')
        col1,col2=st.columns(2)
        with col1:
            st.header('Most Busy Day')
            busy_day=helper.week_activity(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            st.pyplot(fig)

        with col2:
            st.header('Most Busy Month')
            busy_month = helper.month_activity(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='orange')
            #plt.xticks(rotation='vertical')
            st.pyplot(fig)


        #finding busiest person in the group(group level)
        if selected_user=='Overall':
            st.title('Most Busy Users')
            x,y=helper.fetch_most_busy(df)
            fig,ax=plt.subplots()

            col1,col2=st.columns(2)
            with col1:
                ax.bar(x.index, x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(y)

        #wordcloud
        st.title('Wordcloud Analysis')
        df_wc=helper.create_wordcloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #most common words
        st.title('Most Common Words')
        most_common=helper.common_words(selected_user,df)
        fig,ax=plt.subplots()
        ax.barh(most_common['word'],most_common['frequency'])
        #plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #emoji analysis
        common_emoji=helper.common_emojis(selected_user, df)
        st.title('Emojis Analysis')

        col1,col2=st.columns(2)
        with col1:
            st.dataframe(common_emoji)
        with col2:
            fig,ax=plt.subplots()
            #ax.barh(common_emoji[0],common_emoji[1])
            ax.pie(common_emoji[1].head(6),labels=common_emoji[0].head(6),autopct='%0.2f')
            st.pyplot(fig)
        #st.dataframe(common_emoji)


