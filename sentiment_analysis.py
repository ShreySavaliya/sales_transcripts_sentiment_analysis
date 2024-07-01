from transformers import pipeline

# Function to perform sentiment analysis
def sentiment_analysis(dialogue):
    results = []
    sentiment_pipeline = pipeline("sentiment-analysis")

    for sentence in dialogue:
        result = sentiment_pipeline(sentence)
        results.append(result[0])  # result is a list of dicts, we want the first dict
        sentiments = [entry['score'] for entry in results]
    return sentiments