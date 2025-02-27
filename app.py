import streamlit as st
from preprocess import preprocess  # Import the function
from fetch import fetch,busy_user,fetch_wordcloud,fetch_freq,monthly_timeline,daily_timeline,busy_day,busy_month,heatmap

import seaborn as sns
import matplotlib.pyplot as plt

st.sidebar.title('Chat Analyzer')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file :
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()

    data = bytes_data.decode("utf-8")

    df = preprocess(data)

    users = df['User'].unique().tolist()
    users.remove("System")
    users.sort()
    users.insert(0,"Overall")

    selected_user = st.sidebar.selectbox(
        "Show analysis with",
        users
    )

    if st.sidebar.button("Analyse"):
        st.title("Top Statistics")

        num_mes,words,media,links = fetch(selected_user,df)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.header(num_mes)

        with col2:
            st.header("Total Words")
            st.header(words)

        with col3:
            st.header("Media Shared")
            st.header(media)

        with col4:
            st.header("Links Shared")
            st.header(links)

        st.header("Monthly Timeline")

        timeline = monthly_timeline(df, selected_user)
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(timeline['time_m'],timeline['Message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.header("Daily Timeline")

        timeline = daily_timeline(df, selected_user)
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(timeline['time_d'], timeline['Message'])

        step = max(1, len(timeline) // 10)  # Adjust step size dynamically
        ax.set_xticks(timeline['time_d'][::step])

        # Rotate x-axis labels for better spacing
        plt.xticks(rotation=45, ha="right")
        st.pyplot(fig)

        st.header("Activity Map")

        col1,col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")

            b_day = busy_day(df, selected_user)
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.bar(b_day['day'], b_day['Message'])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")

            b_mon = busy_month(df, selected_user)
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.bar(b_mon['month'], b_mon['Message'])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        if selected_user == "Overall":
            st.title("Most Busy User")
            x,new_df = busy_user(df)

            fig, ax = plt.subplots(figsize=(5, 4))

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index,x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df, height=300)


        st.header("Word Cloud")

        # Display word cloud
        wc = fetch_wordcloud(df,selected_user)
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.imshow(wc, interpolation="bilinear")
        ax.axis("off")  # Hide axes
        st.pyplot(fig)

        st.header("Top Frequent Words")

        most_com_df = fetch_freq(df,selected_user)

        fig,ax = plt.subplots(figsize=(8, 8))

        ax.barh(most_com_df[0] , most_com_df[1])
        plt.xticks(rotation='vertical')

        st.pyplot(fig)

        st.header("Most Active Hour")

        heatmap_data = heatmap(df,selected_user)

        fig, ax = plt.subplots(figsize=(20, 10))
        sns.heatmap(heatmap_data, cmap="Blues", annot=True, fmt=".0f", linewidths=0.5, ax=ax)
        plt.yticks(rotation='horizontal')

        # Set labels
        plt.xlabel("Hour of the Day")
        plt.ylabel("Day of the Week")
        plt.title("Message Activity Heatmap")

        st.pyplot(fig)



