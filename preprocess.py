import pandas as pd
import re

def preprocess(data):

    # Regular expression pattern
    pattern = r"^(\d{2}/\d{2}/\d{2}), (\d{1,2}:\d{2}\s?[ap]m) - (.*?): (.+)$"

    # Split chat into lines
    lines = data.split("\n")

    # Store extracted data
    structured_data = []

    # Process each line
    for line in lines:
        match = re.match(pattern, line)

        if match:
            date = match.group(1)
            time = match.group(2).replace("\u202f", " ")  # Fix the space issue
            user = match.group(3)
            message = match.group(4)

            structured_data.append([date, time, user, message])
        else:
            # Handling system messages (no user mentioned)
            sys_pattern = r"^(\d{2}/\d{2}/\d{2}), (\d{1,2}:\d{2}\s?[ap]m) - (.+)$"
            sys_match = re.match(sys_pattern, line)

            if sys_match:
                date = sys_match.group(1)
                time = sys_match.group(2).replace("\u202f", " ")  # Fix the space issue
                message = sys_match.group(3)
                structured_data.append([date, time, "System", message])

    # Convert to DataFrame
    df = pd.DataFrame(structured_data, columns=["Date", "Time", "User", "Message"])

    df["word_count"] = df["Message"].apply(lambda x: len(str(x).split()))

    # Convert "Date" column from object (string) to datetime format
    df["DateTime"] = pd.to_datetime(df["Date"] + " " + df["Time"], format="%d/%m/%y %I:%M %p")
    df["Time"] = pd.to_datetime(df["Time"], format="%I:%M %p")

    df["year"] = df["DateTime"].dt.year
    df["month"] = df["DateTime"].dt.month_name()
    df["day"] = df["DateTime"].dt.day_name()

    # Combine columns into one
    df["time_m"] = df["year"].astype(str) + "-" + df["month"]
    df["time_d"] = df["year"].astype(str).str[-2:] + "-" + df["day"].str[:3]

    df["hour"] = df["DateTime"].dt.hour
    df["min"] = df["DateTime"].dt.minute
    df['period'] = df["Time"].dt.strftime("%I %p")

    # Function to detect links and replace them with "Link"
    def replace_links(text):
        # Regex pattern to detect URLs
        url_pattern = r"http[s]?://|www\."
        if re.search(url_pattern, text):
            return "Link"
        return text

    # # Define media-related patterns
    # media_patterns = ['<Media omitted>', '.jpg', '.png', '.gif', '.mp3', '.mp4', '.ogg', 'voice_', 'video.mp4']
    #
    # # Function to replace media & links
    # def replace_media(message):
    #     # Check for media
    #     if any(media in str(message).lower() for media in media_patterns):
    #         return 'Media'
    #
    #     return message
    #
    # Apply function to "Message" column
    df['Message'] = df['Message'].apply(replace_links)


    return df[['User', 'Message','month', 'time_m','time_d', 'day', 'period' ,'word_count']]
