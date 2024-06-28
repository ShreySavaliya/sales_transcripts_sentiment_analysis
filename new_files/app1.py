from flask import Flask, request, jsonify
from new_files.extract_content import extract_conversations
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

        print("File content:", content)

        (sales_agent_conversations, sales_agent_timestamps, sales_agent_dialogues, customer_conversations,
         customer_timestamps, customer_dialogues) = extract_conversations(content)

        return jsonify({"message": "File received", "content_1": content,
                       "content_2": sales_agent_conversations,
                        "content_3": customer_conversations,
                        "content_4": sales_agent_timestamps,
                        "content_5": customer_timestamps,
                        "content_6": sales_agent_dialogues,
                        "content_7": customer_dialogues}), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)
