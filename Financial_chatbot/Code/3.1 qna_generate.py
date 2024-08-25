import openai
import csv
import sys
import os

API_BASE_URL = "https://llama.us.gaianet.network/v1"
MODEL_NAME = "llama"
API_KEY = "GAIA"

def qgen(source_text):
    client = openai.OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Respond with a list of 5 to 10 questions. The text in the user message must contain specific answers to each question. Each question must be complete without references to unclear context such as \"this team\" or \"that lab\". Each question must be on its own line. Just list the questions without any introductory text or numbers.",
            },
            {
                "role": "user",
                "content": source_text,
            }
        ],
        model=MODEL_NAME,
        stream=False,
    )
    return chat_completion.choices[0].message.content

def agen(source_text, question):
    client = openai.OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Give a comprehensive and well-reasoned answer to the user question strictly based on the context below.\n" + source_text,
            },
            {
                "role": "user",
                "content": question,
            }
        ],
        model=MODEL_NAME,
        stream=False,
    )
    return chat_completion.choices[0].message.content

def main():
    # Input and output file paths
    input_file_path = '/home/aru/Desktop/LFX_test/Financial_chatbot/Dataset/CSV/test.csv'
    output_file_path = '/home/aru/Desktop/LFX_test/Financial_chatbot/Dataset/CSV/qna_test.csv'
    
    results = []

    with open(input_file_path, 'r', newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            page_content = row['Content']

            qs = qgen(page_content)
            for q in qs.splitlines():
                if len(q.strip()) == 0:
                    continue

                answer = agen(page_content, q)
                result = {
                    'Question': q,
                    'Answer': answer
                }
                results.append(result)

    with open(output_file_path, 'w', newline='') as csvfile:
        fieldnames = ['Question', 'Answer']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in results:
            writer.writerow(row)

if __name__ == "__main__":
    main()
