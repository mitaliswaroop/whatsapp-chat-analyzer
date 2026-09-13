import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("WhatsApp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a WhatsApp .txt export", type=["txt"])

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8", errors="ignore")

    df = preprocessor.preprocess(data)
    st.header("Analysis:")

    user_list = df['user'].unique().tolist()
    try:
        user_list.remove('group_notification')
    except ValueError:
        pass
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):

        # Stats Area
        st.title("Top Statistics")
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_links)

        # monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color = 'green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map
        st.title('Activity Map')
        col1, col2 = st.columns(2)
        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color= 'pink')
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)
        with col2:
            st.header("Most Busy Month")
            busy_month = helper.monthly_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation = 'vertical' )
            st.pyplot(fig)

        # heatmap
        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)



        # finding most busy users in the group
        if selected_user == "Overall":
            st.title('Most Busy Users')
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots(figsize = (12,8))
            col1, col2 = st.columns(2)
            with col1:
                ax.bar(x.index, x.values, color = 'purple')
                plt.xticks(rotation = 45)
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # word Cloud
        st.title('Word Cloud')
        df_wc = helper.create_word_cloud(selected_user, df)
        fig, ax = plt.subplots(figsize = (12,8))
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        st.title("Most Common Words")
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots(figsize=(12, 8))
<<<<<<< HEAD
        ax.barh(most_common_df[0], most_common_df[1])
=======
        ax.barh(most_common_df['word'], most_common_df['count'])
>>>>>>> cef88523e2c65bdf9c8914abd55d13c0ff11098b
        plt.xticks(rotation = 45)
        st.pyplot(fig)

        # emoji analysis
        st.title("Most Common Emojis")
        emoji_df = helper.emoji_helper(selected_user, df)
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots(figsize = (12,8))
<<<<<<< HEAD
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)

        # sentiment analysis
        st.title("Sentiment Analysis")

        if selected_user == "Overall":

            # Overall sentiment
            sentiment_counts = df['sentiment'].value_counts()

            st.subheader("Overall Sentiment")

            st.bar_chart(sentiment_counts)

            st.dataframe(
                sentiment_counts.to_frame(name="Count"),
                use_container_width=True
            )

            # Sentiment by user
            st.subheader("Sentiment by User")

            user_sentiment = (
                df.groupby(['user', 'sentiment'])
                .size()
                .unstack(fill_value=0)
                .reindex(
                    columns=['Positive', 'Neutral', 'Negative'],
                    fill_value=0
                )
            )

            st.dataframe(
                user_sentiment,
                use_container_width=True
            )

        else:

            # Filter messages for selected user
            user_df = df[df['user'] == selected_user]

            # Sentiment counts for selected user
            sentiment_counts = (
                user_df['sentiment']
                .value_counts()
                .reindex(
                    ['Positive', 'Neutral', 'Negative'],
                    fill_value=0
                )
            )

            st.subheader(f"Sentiment Analysis - {selected_user}")

            st.bar_chart(sentiment_counts)

            st.dataframe(
                sentiment_counts.to_frame(name="Count"),
                use_container_width=True
            )
=======
            ax.pie(emoji_df['count'].head(), labels=emoji_df['emoji'].head(), autopct="%0.2f")
            st.pyplot(fig)
>>>>>>> cef88523e2c65bdf9c8914abd55d13c0ff11098b
