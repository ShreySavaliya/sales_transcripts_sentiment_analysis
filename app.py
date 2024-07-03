from flask import Flask, request, jsonify
from extract_content import (extract_conversations, extract_sales_agent_timestamps, extract_customer_timestamps,
                             extract_customer_dialogues, extract_sales_agent_dialogues)
from sentiment_analysis import analyze_sentiment

app = Flask(__name__)


# Home Page Route
@app.route('/upload', methods=['POST'])
def upload_file():
    """Managing the file uploads"""

    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file:
        content = file.read().decode("utf-8")

        sales_agent_conversations, customer_conversations = extract_conversations(content)
        sales_agent_timestamps = extract_sales_agent_timestamps(content)
        customer_timestamps = extract_customer_timestamps(content)
        sales_agent_dialogues = extract_sales_agent_dialogues(sales_agent_conversations)
        customer_dialogues = extract_customer_dialogues(customer_conversations)
        sales_agent_sentiments = analyze_sentiment(sales_agent_dialogues)
        customer_sentiments = analyze_sentiment(customer_dialogues)

        # Returning the response to the request
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


if __name__ == "__main__":
    app.run(debug=True, port=5000)
