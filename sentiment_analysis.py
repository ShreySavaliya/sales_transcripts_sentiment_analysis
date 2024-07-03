from transformers import (AutoTokenizer, AutoModelForSequenceClassification)


def analyze_sentiment(file_content):
    """Calculating the sentiments for the transcripts"""

    try:
        model_name = "cardiffnlp/twitter-roberta-base-sentiment"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSequenceClassification.from_pretrained(model_name)
    except Exception as e:
        print("Error loading model: {e}")
        raise e

    sentiments = []

    for line in file_content:
        text = tokenizer(line[:1024], return_tensors='pt')
        output = model(**text)
        scores = output.logits.softmax(dim=1).tolist()[0]
        sentiment = {'Negative': scores[0], 'Neutral': scores[1], 'Positive': scores[2]}
        sentiments.append(sentiment)

    answers = []
    for value in sentiments:
        key = max(value, key=value.get)
        value = value[key]
        answers.append({key: value})

    return answers
