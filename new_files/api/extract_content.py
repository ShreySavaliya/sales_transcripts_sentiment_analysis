import re


def extract_conversations(file_content):
    lines = file_content.split('\n')

    sales_agent_conversations = []
    customer_conversations = []
    
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

        elif line.startswith('[Customer'):
            customer_line = line  # Start with the timestamp line
            i += 1
            while i < len(lines) and lines[i].strip() != '':
                customer_line += ' ' + lines[i].strip()
                i += 1
            customer_conversations.append(customer_line)

        i += 1

    return sales_agent_conversations, customer_conversations


def extract_customer_timestamps(file_content):
    lines = file_content.split('\n')

    customer_timestamps = []
    for line in lines:
        if line.startswith("[Customer"):

            match = re.search(r'\[\w+ (\d{2}:\d{2})]', line)
            if match:
                customer_timestamps.append(match.group(1))

    return customer_timestamps


# # Function to extract the sales_agent_timestamps
def extract_sales_agent_timestamps(file_content):
    lines = file_content.split('\n')

    sales_agent_timestamps = []
    for line in lines:
        match = re.search(r'\[\w+ \w+ (\d{2}:\d{2})]', line)
        if match:
            sales_agent_timestamps.append(match.group(1))

    return sales_agent_timestamps


def extract_customer_dialogues(file_content):
    customer_dialogues = []
    for line in file_content:
        customer_dialogue = line[17:].strip()
        customer_dialogues.append(customer_dialogue)

    return customer_dialogues


def extract_sales_agent_dialogues(file_content):
    sales_agent_dialogues = []
    for line in file_content:
        sales_agent_dialogue = line[20:].strip()
        sales_agent_dialogues.append(sales_agent_dialogue)

    return sales_agent_dialogues
