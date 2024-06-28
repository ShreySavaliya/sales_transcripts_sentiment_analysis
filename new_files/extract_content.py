import re


def extract_conversations(file_content):
    lines = file_content.split('\n')

    sales_agent_conversations = []
    customer_conversations = []
    sales_agent_timestamps = []
    customer_timestamps = []
    sales_agent_dialogues = []
    customer_dialogues = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        if line.startswith('[Sales Agent'):
            sales_agent_line = line  # Start with the timestamp line
            i += 1
            while i < len(lines) and lines[i].strip() != '':
                sales_agent_line += ' ' + lines[i].strip()
                i += 1
            sales_agent_conversations.append(sales_agent_line)
            match = re.search(r'\[\w+ \w+ (\d{2}:\d{2})]', line)
            if match:
                sales_agent_timestamps.append(match.group(1))

            sales_agent_dialogue = line[20:].strip()
            sales_agent_dialogues.append(sales_agent_dialogue)

        elif line.startswith('[Customer'):
            customer_line = line  # Start with the timestamp line
            i += 1
            while i < len(lines) and lines[i].strip() != '':
                customer_line += ' ' + lines[i].strip()
                i += 1
            customer_conversations.append(customer_line)

            match = re.search(r'\[\w+ (\d{2}:\d{2})]', line)
            if match:
                customer_timestamps.append(match.group(1))

            customer_dialogue = line[17:].strip()
            customer_dialogues.append(customer_dialogue)

        i += 1

    return (sales_agent_conversations, sales_agent_timestamps, sales_agent_dialogues, customer_conversations,
            customer_timestamps, customer_dialogues)


# def save_conversations(sales_agent_conversations, customer_conversations, sales_file, customer_file):
#     with open(sales_file, 'w', encoding='utf-8') as file:
#         for convo in sales_agent_conversations:
#             file.write(convo + '\n')
#
#     with open(customer_file, 'w', encoding='utf-8') as file:
#         for convo in customer_conversations:
#             file.write(convo + '\n')


# def extract_customer_timestamps(file_path):
#     with open(file_path, 'r', encoding='utf-8') as file:
#         lines = file.readlines()
#
#     customer_timestamps = []
#     for line in lines:
#         if line.startswith("[Customer"):
#
#             match = re.search(r'\[\w+ (\d{2}:\d{2})\]', line)
#             if match:
#                 customer_timestamps.append(match.group(1))
#
#
#     return customer_timestamps
#
#
# # Function to extract the sales_agent_timestamps
# def extract_sales_agent_timestamps(file_path):
#     with open(file_path, 'r', encoding='utf-8') as file:
#         lines = file.readlines()
#
#     timestamps = []
#     for line in lines:
#         match = re.search(r'\[\w+ \w+ (\d{2}:\d{2})\]', line)
#         if match:
#             timestamps.append(match.group(1))
#
#     return timestamps


# Function to extract the sales agent dialogues
# def extract_customer_dialogue(file_path):
#     with open(file_path, 'r', encoding='utf-8') as file:
#         lines = file.readlines()
#         sentences = []
#         for line in lines:
#             # print(line.strip())
#             sentence = line[17:].strip()
#             sentences.append(sentence)
#
#     return sentences
#
#
# def extract_sales_agent_dialogue(file_path):
#     with open(file_path, 'r', encoding='utf-8') as file:
#         lines = file.readlines()
#         sentences = []
#         for line in lines:
#             sentence = line[20:].strip()
#             sentences.append(sentence)
#
#     return sentences
