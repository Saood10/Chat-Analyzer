from  urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd

extract = URLExtract()

def fetch(user, df):
    if user != "Overall":
        df = df[df['User'] == user]

    # fetch media
    media = df[df["Message"] == "<Media omitted>"].shape[0]

    # # fetch links
    # links = []
    # for mes in df['Message']:
    #     links.extend(extract.find_urls(mes))
    links = df[df['Message'] == 'Link']


    return df.shape[0], df['word_count'].sum(),media,len(links)

def busy_user(df):
    x = df['User'].value_counts().head()
    df = round(df['User'].value_counts() / df.shape[0] * 100, 2).reset_index().rename(columns={"count": '%'})
    return x,df


def fetch_wordcloud(df,user):
    if user != "Overall":
        df = df[df["User"] == user]

    wc = WordCloud(width=500,height=300,background_color="white", colormap="viridis").generate(df["Message"].str.cat(sep=" "))

    return wc

def fetch_freq(df,user):

    with open("stop_hinglish.txt" , 'r') as f:
        stop_words = f.read()

    if user != "Overall":
        df = df[df["User"] == user]

    temp = df[df["Message"] != "<Media omitted>"]
    temp = temp[temp["User"] != "System"]

    words = []

    for m in temp["Message"]:
        for w in m.lower().split():
            if w not in stop_words:
                words.append(w)

    return pd.DataFrame(Counter(words).most_common(20))

def monthly_timeline(df,user):
    if user != "Overall":
        df = df[df["User"] == user]

    return df.groupby(['time_m']).count()["Message"].reset_index()


def daily_timeline(df,user):
    if user != "Overall":
        df = df[df["User"] == user]

    return df.groupby("time_d").count()["Message"].reset_index()

def busy_day(df,user):
    if user != "Overall":
        df = df[df["User"] == user]

    return df.groupby("day").count()["Message"].reset_index().set_index("day").reindex(
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]).reset_index()


def busy_month(df,user):
    if user != "Overall":
        df = df[df["User"] == user]

    return df.groupby("month").count()["Message"].reset_index()

def heatmap(df,user):
    if user != "Overall":
        df = df[df["User"] == user]

    # Create pivot table (heatmap data)
    heatmap_data = df.pivot_table(index="day", columns="period", values="Message", aggfunc="count").fillna(0)

    # Define correct AM-PM order
    ordered_hours = [f"{i:02d} AM" for i in range(1, 12)] + ["12 PM"] + [f"{i:02d} PM" for i in range(1, 12)] + [
        "12 AM"]

    # **Fix: Use `.reindex()` to include missing hours and fill with 0
    heatmap_data = heatmap_data.reindex(columns=ordered_hours, fill_value=0)

    # Sort days properly
    ordered_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    heatmap_data = heatmap_data.reindex(ordered_days)

    return heatmap_data


