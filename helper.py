from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
import emoji
<<<<<<< HEAD
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
from collections import Counter
extractor = URLExtract()

import matplotlib.pyplot as plt
from matplotlib import font_manager
emoji_font = font_manager.FontProperties(
    fname="C:/Windows/Fonts/seguiemj.ttf")
plt.rcParams["font.family"] = emoji_font.get_name()
=======
from collections import Counter
import matplotlib.pyplot as plt

extractor = URLExtract()

>>>>>>> cef88523e2c65bdf9c8914abd55d13c0ff11098b

def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

<<<<<<< HEAD
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
=======
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

>>>>>>> cef88523e2c65bdf9c8914abd55d13c0ff11098b

def create_word_cloud(selected_user, df):
    with open("stop_hinglish.txt", "r") as f:
        stop_words = set(f.read().splitlines())
<<<<<<< HEAD
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'group_notification']
    temp = temp[~temp["message"].str.contains(
=======

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[~temp['message'].str.contains(
>>>>>>> cef88523e2c65bdf9c8914abd55d13c0ff11098b
        r"media omitted|edited|deleted",
        case=False,
        regex=True,
        na=False
    )]

    def remove_stopword(message):
<<<<<<< HEAD
        words = []
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
        return " ".join(words)
    temp['message'] = temp['message'].apply(remove_stopword)
    wordcloud = WordCloud(width = 500, height = 500, min_font_size= 10, background_color= 'white').generate(temp['message'].str.cat(sep=" "))
    return wordcloud
=======
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

>>>>>>> cef88523e2c65bdf9c8914abd55d13c0ff11098b

def most_common_words(selected_user, df):
    with open("stop_hinglish.txt", "r") as f:
        stop_words = set(f.read().splitlines())
<<<<<<< HEAD
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'group_notification']
    temp = temp[~temp['message'].str.contains('<Media omitted>', na=False)]
    temp = temp[~temp['message'].str.contains('<This message was edited>', na=False)]
    temp = temp[~temp['message'].str.contains('<This message was deleted>', na=False)]
=======

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[~temp['message'].str.contains(
        r'media omitted|edited|deleted',
        case=False,
        regex=True,
        na=False
    )]

>>>>>>> cef88523e2c65bdf9c8914abd55d13c0ff11098b
    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
<<<<<<< HEAD
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df
=======

    return pd.DataFrame(Counter(words).most_common(20),
                        columns=['word', 'count'])

>>>>>>> cef88523e2c65bdf9c8914abd55d13c0ff11098b

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
<<<<<<< HEAD
    emojis = []
    for message in df['message']:
        emojis.extend([e["emoji"] for e in emoji.emoji_list(message)])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df
=======

    emojis = []
    for message in df['message']:
        if isinstance(message, str):
            for e in emoji.emoji_list(message):
                emojis.append(e['emoji'])

    return pd.DataFrame(
        Counter(emojis).most_common(),
        columns=['emoji', 'count']
    )

>>>>>>> cef88523e2c65bdf9c8914abd55d13c0ff11098b

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
<<<<<<< HEAD
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
=======

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

>>>>>>> cef88523e2c65bdf9c8914abd55d13c0ff11098b

def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
<<<<<<< HEAD
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

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Download VADER lexicon
nltk.download('vader_lexicon', quiet=True)

sia = SentimentIntensityAnalyzer()


def analyze_sentiment(message):
    """
    Analyze the sentiment of a single message.
    Returns: Positive, Negative, or Neutral
    """
    if not isinstance(message, str) or not message.strip():
        return "Neutral"

    score = sia.polarity_scores(message)['compound']

    if score >= 0.05:
        return "Positive"
    elif score <= -0.05:
        return "Negative"
    else:
        return "Neutral"


def add_sentiment(df):
    """
    Add sentiment column to the dataframe.
    """
    df = df.copy()

    # Remove empty messages
    df = df[df['message'].notna()]
    df['message'] = df['message'].astype(str)

    # Calculate sentiment
    df['sentiment'] = df['message'].apply(analyze_sentiment)

    return df


def get_user_sentiment(df, user):
    """
    Get sentiment counts for a specific user.
    """
    user_df = df[df['user'] == user]

    sentiment_counts = (
        user_df['sentiment']
        .value_counts()
        .reindex(['Positive', 'Neutral', 'Negative'], fill_value=0)
    )

    return sentiment_counts


def get_overall_sentiment(df):
    """
    Get sentiment counts for all users.
    """
    overall = (
        df.groupby(['user', 'sentiment'])
        .size()
        .unstack(fill_value=0)
        .reindex(columns=['Positive', 'Neutral', 'Negative'], fill_value=0)
    )

    return overall

=======

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

>>>>>>> cef88523e2c65bdf9c8914abd55d13c0ff11098b
