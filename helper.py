from urlextract import URLExtract
import emojis
import pandas as pd
from collections import Counter
from wordcloud import WordCloud


f=open('stopwords.txt','r')
stopwords=f.read()
def fetch_stats(selected_user,df):

    if selected_user!='Overall':
        df = df[df['user'] == selected_user]
    # num of messages
    num_msg = df.shape[0]
    # num of words
    words = []
    for message in df['message']:
        words.extend(message.split(" "))
        num_words = len(words)
    word_max = []

    temp= df[df['user']!='group_notification']
    temp=temp[temp['message']!='<Media omitted>']
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stopwords:
                word_max.append(word)
    count=Counter(word_max)
    most_common_word,m_word_count=count.most_common(1)[0]
    least_common_word,l_word_count = count.most_common()[-1]



    # num of media msg
    num_media=df[df['message']=='<Media omitted>'].shape[0]

    # num of links
    extractor=URLExtract()
    links=[]
    for message in df['message']:
        links.extend(extractor.find_urls(message))
        num_links=len(links)
    # num of emojis
    emoji=[]
    for message in df['message']:
        emoji.extend(emojis.get(message))
    num_emoji=len(emoji)
    count_e=Counter(emoji)
    most_common_emoji, m_emoji_count = count_e.most_common(1)[0]
    least_common_emoji, l_emoji_count = count_e.most_common()[-1]

    return num_msg,num_words,num_media,num_links,num_emoji,most_common_word,m_word_count,least_common_word,l_word_count,most_common_emoji,m_emoji_count,least_common_emoji,l_emoji_count

def most_busy_user(df):
    x = df['user'].value_counts().head()
    new_df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={'index':'Name','user': 'Percentage'})
    return x,new_df

def create_wordcloud(selected_user,df):

    if selected_user!='Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>']
    def remove_stop_words(message):
        y=[]
        for word in message.lower().split():
            if word not in stopwords:
                y.append(word)
        return " ".join(y)

    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='black',stopwords=stopwords)
    temp['message']=temp['message'].apply(remove_stop_words)
    df_wc=wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]
    common_word = []
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>']
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stopwords:
                common_word.append(word)
    return_df =pd.DataFrame(Counter(common_word).most_common(20))
    return_df=return_df.rename(columns={0:'Words',1:'Count'})
    return return_df

def most_common_emoji(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]

    emoji = []
    for message in df['message']:
        emoji.extend(emojis.get(message))

    return_df = pd.DataFrame(Counter(emoji).most_common(10))
    return_df = return_df.rename(columns={0: 'Emoji', 1: 'Count'})
    return return_df

def timeline(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]


    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))
    timeline['time'] = time

    return timeline
def daily_timeline(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]


    daily_timeline=df.groupby('date').count()['message'].reset_index()

    return daily_timeline

def weekly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    weekly_timeline=df['day_name'].value_counts().reset_index()

    return weekly_timeline

def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    monthly_timeline=df['month'].value_counts().reset_index()

    return monthly_timeline

def user_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    pivot = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return pivot