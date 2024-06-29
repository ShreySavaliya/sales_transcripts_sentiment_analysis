from transformers import (pipeline, AutoTokenizer, AutoModelForSequenceClassification,
                          LongformerTokenizer, LongformerForSequenceClassification, BigBirdTokenizer,
                          BigBirdForSequenceClassification)
import torch


# def analyze_sentiment(file_content):
#     results = []
#     sentiment_pipeline = pipeline("sentiment-analysis")
#
#     for line in file_content:
#         result = sentiment_pipeline(line)
#         results.append(result)
#         sentiments = [entry['score'] for entry in results]
#
#     return sentiments

def analyze_sentiment(file_content):
    model_name = "google/bigbird-roberta-base"
    tokenizer = BigBirdTokenizer.from_pretrained(model_name)
    model = BigBirdForSequenceClassification.from_pretrained(model_name)

    for line in file_content:

        inputs = tokenizer(line, return_tensors='pt', max_length=4096, truncation=True)

        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits
            predicted_class = torch.argmax(logits).item()

        labels = ['negative', 'neutral', 'positive']  # Assuming 3-class sentiment analysis
        print(f"Predicted class: {labels[predicted_class]}",
              f"Line: {line}")

