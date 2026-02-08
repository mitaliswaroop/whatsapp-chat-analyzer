from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
import emoji
from collections import Counter
import matplotlib.pyplot as plt

extractor = URLExtract()


def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]

    words = []
    for message in df['message']:
        if isinstance(message, str):
            words.extend(message.split())

    num_media_messages = df['message'].str.contains(
        '<Media omitted>', na=False
    ).sum()

    links = []
    for message in df['message']:
        if isinstance(message, str):
            links.extend(extractor.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)


def most_busy_users(df):
    x = df['user'].value_counts().head()
    percent_df = (
        (df['user'].value_counts().head() / df.shape[0]) * 100
    ).round(2).reset_index()
    percent_df.columns = ['name', 'percent']
    return x, percent_df


def create_word_cloud(selected_user, df):
    with open("stop_hinglish.txt", "r") as f:
        stop_words = set(f.read().splitlines())

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[~temp['message'].str.contains(
        r"media omitted|edited|deleted",
        case=False,
        regex=True,
        na=False
    )]

    def remove_stopword(message):
        return " ".join(
            word for word in message.lower().split()
            if word not in stop_words
        )

    temp['message'] = temp['message'].apply(remove_stopword)

    wc = WordCloud(
        width=500,
        height=500,
        min_font_size=10,
        background_color='white'
    )

    return wc.generate(temp['message'].str.cat(sep=" "))


def most_common_words(selected_user, df):
    with open("stop_hinglish.txt", "r") as f:
        stop_words = set(f.read().splitlines())

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[~temp['message'].str.contains(
        r'media omitted|edited|deleted',
        case=False,
        regex=True,
        na=False
    )]

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    return pd.DataFrame(Counter(words).most_common(20),
                        columns=['word', 'count'])


def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        if isinstance(message, str):
            for e in emoji.emoji_list(message):
                emojis.append(e['emoji'])

    return pd.DataFrame(
        Counter(emojis).most_common(),
        columns=['emoji', 'count']
    )


def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = (
        df.groupby(['year', 'month_num', 'month'])
        .count()['message']
        .reset_index()
    )

    timeline['time'] = (
        timeline['month'] + "-" + timeline['year'].astype(str)
    )
    return timeline


def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df.groupby('only_date').count()['message'].reset_index()


def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()


def monthly_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()


def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return (
        df.pivot_table(
            index='day_name',
            columns='period',
            values='message',
            aggfunc='count'
        )
        .fillna(0)
    )

