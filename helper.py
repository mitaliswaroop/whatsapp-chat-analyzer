from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
import emoji
from collections import Counter
extractor = URLExtract()

import matplotlib.pyplot as plt
from matplotlib import font_manager
emoji_font = font_manager.FontProperties(
    fname="C:/Windows/Fonts/seguiemj.ttf")
plt.rcParams["font.family"] = emoji_font.get_name()

def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    if selected_user == 'Overall':
        #fetch number of messages
        num_messages = df.shape[0]

        #fetch number of words
        words = []
        for message in df['message']:
            words.extend(message.split())

        #fetch number of media messages
        num_media_messages = df['message'].str.contains('<Media omitted>').sum()

        #fetch number of links
        links = []
        for message in df['message']:
            links.extend(extractor.find_urls(message))

        return num_messages, len(words), num_media_messages, len(links)
    else:
        new_df = df[df['user'] == selected_user]
        num_messages = new_df.shape[0]

        words = []
        for message in df['message']:
            words.extend(message.split())

        num_media_messages = df['message'].str.contains('<Media omitted>').sum()

        links = []
        for message in df['message']:
            links.extend(extractor.find_urls(message))

        return num_messages, len(words), num_media_messages, len(links)

def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts().head()/df.shape[0])*100, 2).reset_index().rename(columns = {'user': 'name', 'count': 'percent'})
    return x, df

def create_word_cloud(selected_user, df):
    with open("stop_hinglish.txt", "r") as f:
        stop_words = set(f.read().splitlines())
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'group_notification']
    temp = temp[~temp["message"].str.contains(
        r"media omitted|edited|deleted",
        case=False,
        regex=True,
        na=False
    )]

    def remove_stopword(message):
        words = []
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
        return " ".join(words)
    temp['message'] = temp['message'].apply(remove_stopword)
    wordcloud = WordCloud(width = 500, height = 500, min_font_size= 10, background_color= 'white').generate(temp['message'].str.cat(sep=" "))
    return wordcloud

def most_common_words(selected_user, df):
    with open("stop_hinglish.txt", "r") as f:
        stop_words = set(f.read().splitlines())
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'group_notification']
    temp = temp[~temp['message'].str.contains('<Media omitted>', na=False)]
    temp = temp[~temp['message'].str.contains('<This message was edited>', na=False)]
    temp = temp[~temp['message'].str.contains('<This message was deleted>', na=False)]
    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    emojis = []
    for message in df['message']:
        emojis.extend([e["emoji"] for e in emoji.emoji_list(message)])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    day_timeline = df.groupby('only_date').count()['message'].reset_index()
    return day_timeline

def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()

def monthly_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return user_heatmap
