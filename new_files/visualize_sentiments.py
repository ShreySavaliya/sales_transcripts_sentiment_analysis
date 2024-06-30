import plotly.express as px


def merge_sentiment_scores(sentiment_scores):
    merged_scores = {}
    for score in sentiment_scores:
        for sentiment, value in score.items():
            if sentiment in merged_scores:
                merged_scores[sentiment] += value
            else:
                merged_scores[sentiment] = value
    return merged_scores


def create_piechart(sales_agent_sentiments):
    merged_scores = merge_sentiment_scores(sales_agent_sentiments)
    labels = list(merged_scores.keys())
    values = list(merged_scores.values())

    # Create a pie chart using Plotly
    fig = px.pie(values=values, names=labels, title='Sentiment Analysis')

    return fig
