import re
import pandas as pd

def preprocess(chat_text):

    # Decode bytes if needed
    if isinstance(chat_text, bytes):
        chat_text = chat_text.decode("utf-8", errors="ignore")

    # Clean weird Unicode
    chat_text = chat_text.replace("\u202f", " ").replace("\ufeff", "")

    # Universal WhatsApp timestamp
    pattern = r'(\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}(?:\s?[APap][Mm])?)\s-\s'

    parts = re.split(pattern, chat_text)

    if len(parts) < 3:
        raise ValueError("Chat format not recognized")

    dates = parts[1::2]
    messages = parts[2::2]

    df = pd.DataFrame({
        "raw_date": dates,
        "raw_message": messages
    })

    # Let pandas handle ALL formats
    df["date"] = pd.to_datetime(
        df["raw_date"],
        errors="coerce",
        dayfirst=True
    )

    users = []
    messages_clean = []

    for msg in df["raw_message"]:
        match = re.match(r"([^:]+?):\s(.*)", msg)

        if match:
            users.append(match.group(1))
            messages_clean.append(match.group(2))
        else:
            users.append("notification")
            messages_clean.append(msg)

    df["user"] = users
    df["message"] = messages_clean
    df.drop(columns=["raw_date", "raw_message"], inplace=True)

    # Time features
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month_name()
    df["day"] = df["date"].dt.day
    df["hour"] = df["date"].dt.hour
    df["minute"] = df["date"].dt.minute
    df['month_num'] = df['date'].dt.month
    df['only_date'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))
    df['period'] = period

    return df
