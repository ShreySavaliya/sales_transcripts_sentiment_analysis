from transformers import (pipeline, AutoTokenizer, AutoModelForSequenceClassification,
                          LongformerTokenizer, LongformerForSequenceClassification, BigBirdTokenizer,
                          BigBirdForSequenceClassification,
                          DistilBertTokenizer, DistilBertForSequenceClassification)
import torch
from textblob import TextBlob

# def analyze_sentiment(file_content):
#     model_name = "google/bigbird-roberta-base"
#     tokenizer = BigBirdTokenizer.from_pretrained(model_name)
#     model = BigBirdForSequenceClassification.from_pretrained(model_name)
#
#     for line in file_content:
#
#         inputs = tokenizer(line, return_tensors='pt', max_length=4096, truncation=True)
#
#         with torch.no_grad():
#             outputs = model(**inputs)
#             logits = outputs.logits
#             predicted_class = torch.argmax(logits).item()
#
#         labels = ['negative', 'neutral', 'positive']  # Assuming 3-class sentiment analysis
#         print(f"Predicted class: {labels[predicted_class]}",
#               f"Line: {line}")


# def analyze_sentiment(file_content):
#
#     max_length = 1024
#     sentiments = []
#     for line in file_content:
#         text = line[:max_length]
#         blob = TextBlob(text)
#         sentiment = blob.sentiment
#         sentiments.append(sentiment.polarity)
#     print(len(sentiments))
#     return sentiments


def analyze_sentiment(file_content):

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

    print(sentiments)

    answers = []
    for value in sentiments:
        key = max(value, key=value.get)
        value = value[key]
        answers.append({key: value})
    print(answers)

    return sentiments
