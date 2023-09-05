from textblob import TextBlob

def get_sentiment(word):
    analysis = TextBlob(word)
    if analysis.sentiment.polarity > 0:
        return "Positive"
    elif analysis.sentiment.polarity < 0:
        return "Negative"
    else:
        return "Neutral"