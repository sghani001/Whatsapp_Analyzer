import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data =bytes_data.decode("utf-8")

    df =preprocessor.preprocess(data)

    # st.dataframe(df,height=600,width=1200)

    # fetch unique user
    user_list=df['user'].unique().tolist()
    try:
        user_list.remove("group_notification")
    except:
        pass
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user=st.sidebar.selectbox("Show Analysis with",user_list)



    # statsss
    if st.sidebar.button("show Analysis"):
        num_msg,num_words,num_media,num_links,num_emoji,most_common_word,m_word_count,least_common_word,l_word_count,most_common_emoji,m_emoji_count,least_common_emoji,l_emoji_count=helper.fetch_stats(selected_user,df)
        st.title("TOP STATISTICS")
        col1,col2,col3,col4=st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_msg)
        with col2:
            st.header("Total Words")
            st.title(num_words)
        with col3:
            st.header("Media Shared")
            st.title(num_media)
        with col4:
            st.header("Link Shared")
            st.title(num_links)
        with col1:
             st.header("Emoji Shared")
             st.title(num_emoji)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Most repeated Word")
            st.title(f"\"{most_common_word}\"")
            st.title(m_word_count)
        with col2:
            st.header("Least repeated Word")
            st.title(f"\"{least_common_word}\"")
            st.title(l_emoji_count)
        with col3:
            st.header("Most repeated Emoji")
            st.title(f"\"{most_common_emoji}\"")
            st.title(m_emoji_count)
        with col4:
            st.header("least repeated Emoji")
            st.title(f"\"{least_common_emoji}\"")
            st.title(l_emoji_count)

        col1, col2 = st.columns(2)
        # Timeline
        with col1:
            st.title("MONTHLY TIMELINE")
            timeline=helper.timeline(selected_user,df)
            fig, ax = plt.subplots(figsize=(8, 6))

            ax.plot(timeline['time'], timeline['message'],color='green')
            plt.xticks(rotation='vertical')
            ax.tick_params(axis='both', colors='white')
            ax.set_xlabel('Months-Years', color='white')
            ax.set_ylabel('Messages', color='white')
            ax.set_facecolor('black')
            fig.set_facecolor('black')
            st.pyplot(fig)

        with col2:
            # daily_timeline
            st.title("DAILY TIMELINE")
            daily_timeline = helper.daily_timeline(selected_user, df)
            fig, ax = plt.subplots(figsize=(8, 6))

            ax.plot(daily_timeline['date'],daily_timeline['message'], color='green')
            plt.xticks(rotation='vertical')
            ax.tick_params(axis='both', colors='white')
            ax.set_xlabel('Day', color='white')
            ax.set_ylabel('Messages', color='white')
            ax.set_facecolor('black')
            fig.set_facecolor('black')
            st.pyplot(fig)

        col1, col2 = st.columns(2)
        with col1:
            # activity map for week
            st.title("WEEKLY TIMELINE")
            weekly_timeline = helper.weekly_timeline(selected_user, df)
            fig, ax = plt.subplots(figsize=(8, 6))

            ax.bar(weekly_timeline['index'], weekly_timeline['day_name'], color='green')
            plt.xticks(rotation='vertical')
            ax.tick_params(axis='both', colors='white')
            ax.set_xlabel('Week Days', color='white')
            ax.set_ylabel('Messages', color='white')
            ax.set_facecolor('black')
            fig.set_facecolor('black')
            st.pyplot(fig)
        with col2:
            # activity map for month
            st.title("MONTHLY TIMELINE")
            monthly_timeline = helper.monthly_timeline(selected_user, df)
            fig, ax = plt.subplots(figsize=(8, 6))

            ax.bar(monthly_timeline['index'], monthly_timeline['month'], color='green')
            plt.xticks(rotation='vertical')
            ax.tick_params(axis='both', colors='white')
            ax.set_xlabel('Months', color='white')
            ax.set_ylabel('Messages', color='white')
            ax.set_facecolor('black')
            fig.set_facecolor('black')
            st.pyplot(fig)

        #  heatmap
        st.title('WEEKLY ACTIVITY MAP')
        user_heatmap=helper.user_heatmap(selected_user,df)
        fig, ax = plt.subplots(figsize=(20,6))
        ax=sns.heatmap(user_heatmap)
        plt.yticks(rotation='horizontal')
        plt.xticks(rotation='vertical')
        ax.tick_params(axis='both', colors='white')
        ax.set_xlabel('Hour Periods', color='white')
        ax.set_ylabel('Days', color='white')
        ax.set_facecolor('black')
        fig.set_facecolor('black')
        st.pyplot(fig)


        # finding most busy users
        if selected_user == 'Overall':
            x,new_df=helper.most_busy_user(df)
            col1, col2 = st.columns(2)
            fig, ax = plt.subplots(figsize=(8,6))
            with col1:
                st.title("Most Busy Users")
                ax.bar(x.index,x.values,color='green')
                plt.xticks(rotation='vertical')
                ax.tick_params(axis='both', colors='white')
                ax.set_xlabel('User', color='white')
                ax.set_ylabel('Messages', color='white')
                ax.set_facecolor('black')
                fig.set_facecolor('black')
                st.pyplot(fig)
            with col2:
                st.title("Active User Percentage")
                st.dataframe(new_df,width=400,height=400)

        col1, col2 = st.columns(2)
        common_word_df=helper.most_common_words(selected_user,df)
        fig, ax = plt.subplots(figsize=(8, 6))
        with col1:
            st.title("Word Cloud")
            df_wc=helper.create_wordcloud(selected_user,df)
            ax.imshow(df_wc)
            ax.tick_params(axis='both', colors='white')
            fig.set_facecolor('black')
            st.pyplot(fig)
        fig, ax = plt.subplots(figsize=(8,8.5))
        with col2:
            st.title('Most Common Words')
            ax.barh(common_word_df['Words'],common_word_df['Count'],color='green')
            plt.xticks(rotation='vertical')
            ax.tick_params(axis='both', colors='white')
            ax.set_xlabel('Count', color='white')
            ax.set_ylabel('Words', color='white')
            ax.set_facecolor('black')
            fig.set_facecolor('black')
            st.pyplot(fig)

        col1, col2 = st.columns(2)
        common_emoji_df=helper.most_common_emoji(selected_user,df)
        fig, ax = plt.subplots()
        with col1:
            st.title('Most Common Emoji')
            st.dataframe(common_emoji_df,height=400,width=600)
        with col2:
            st.title('Most Common Emoji Plot')
            ax.pie(common_emoji_df['Count'],labels=common_emoji_df['Emoji'],autopct="%0.2f",startangle=90,explode=[0.3,0,0,0,0,0,0,0,0,0],shadow=True)
            ax.set_facecolor('black')
            fig.set_facecolor('black')
            plt.rcParams['text.color'] = 'white'
            st.pyplot(fig)