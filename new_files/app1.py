from flask import Flask, request, jsonify
from extract_content import (extract_conversations, extract_sales_agent_timestamps, extract_customer_timestamps,
                             extract_customer_dialogues, extract_sales_agent_dialogues)
from sentiment_analysis import analyze_sentiment
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

        analyze_sentiment(customer_dialogues)

        return jsonify({"message": "File received",
                       "content_1": content,
                        "content_2": sales_agent_conversations,
                        "content_3": customer_conversations,
                        "content_4": sales_agent_timestamps,
                        "content_5": customer_timestamps,
                        "content_6": sales_agent_dialogues,
                        "content_7": customer_dialogues
                        }), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)
