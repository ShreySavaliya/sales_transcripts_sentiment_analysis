from flask import Flask, request, jsonify
from extract_content import (extract_conversations, extract_sales_agent_timestamps, extract_customer_timestamps,
                             extract_customer_dialogues, extract_sales_agent_dialogues)
from sentiment_analysis import analyze_sentiment
import plotly.express as px
import streamlit as st
app = Flask(__name__)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file:
        content = file.read().decode("utf-8")
        # Process the file content here

        # print("File content:", content)

        sales_agent_conversations, customer_conversations = extract_conversations(content)
        sales_agent_timestamps = extract_sales_agent_timestamps(content)
        customer_timestamps = extract_customer_timestamps(content)
        sales_agent_dialogues = extract_sales_agent_dialogues(sales_agent_conversations)
        customer_dialogues = extract_customer_dialogues(customer_conversations)
        sales_agent_sentiments = analyze_sentiment(sales_agent_dialogues)
        customer_sentiments = analyze_sentiment(customer_dialogues)

        # return jsonify({"Transcript": content})

        # fig = create_piechart(sales_agent_sentiments)
        # st.plotly_chart(fig)
        # return fig

        return jsonify({"message": "File received",
                       "content": content,
                        "sales_agent_conversations": sales_agent_conversations,
                        "customer_conversations": customer_conversations,
                        "sales_agent_timestamps": sales_agent_timestamps,
                        "customer_timestamps": customer_timestamps,
                        "sales_agent_dialogues": sales_agent_dialogues,
                        "sales_agent_sentiments": sales_agent_sentiments,
                        "customer_dialogues": customer_dialogues,
                        "customer_sentiments": customer_sentiments
                        }), 200

#         visualize_sentiments(sales_agent_timestamps, sales_agent_sentiments,
#                              customer_timestamps, customer_sentiments)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
