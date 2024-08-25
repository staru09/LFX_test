import pandas as pd
import openai
import logging
import time

logging.basicConfig(level=logging.INFO)

API_BASE_URL = "https://llama.us.gaianet.network/v1"
MODEL_NAME = "llama"
API_KEY = "GAIA"

client = openai.OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

def generate_qna(text):
    try:
        start_time = time.time()
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert financial analyst. Your task is to generate 3-5 insightful questions and provide brief, informative answers based on the provided text. The questions and answers should help stakeholders further explore key issues, risks, or trends mentioned in the text. Provide the output in the following format: For each question, provide the corresponding answer.",
                },
                {
                    "role": "user",
                    "content": text,
                }
            ],
            model=MODEL_NAME,
            stream=False,
        )
        logging.info(f"API call took {time.time() - start_time} seconds.")
        
        raw_content = response.choices[0].message['content'].strip()
        logging.info(f"Raw response content: {raw_content}")
        
        qna_pairs = []
        for line in raw_content.split('\n'):
            if 'Answer: ' in line:
                question_part = line.split('Answer: ')[0].strip()
                answer_part = line.split('Answer: ')[1].strip()
                if 'Question: ' in question_part:
                    question = question_part.replace('Question: ', '').strip()
                    qna_pairs.append((question, answer_part))
        
        questions, answers = zip(*qna_pairs) if qna_pairs else ([], [])
        
        return list(questions), list(answers)
    except Exception as e:
        logging.error(f"Error in generating Q&A: {e}")
        return [], []

def generate_qna_csv(input_csv_file, output_csv_file):
    try:
        df = pd.read_csv(input_csv_file)
        if 'Content' not in df.columns:
            raise ValueError("'Content' column not found in the input CSV file.")

        questions_list = []
        answers_list = []

        logging.info("Starting Q&A generation...")
        for index, row in df.iterrows():
            if pd.notnull(row['Content']):
                questions, answers = generate_qna(row['Content'])
                for q, a in zip(questions, answers):
                    questions_list.append(q)
                    answers_list.append(a)

        qna_df = pd.DataFrame({
            'Question': questions_list,
            'Answer': answers_list
        })

        qna_df.to_csv(output_csv_file, index=False)
        logging.info(f"Q&A have been generated and saved to {output_csv_file}")
    except Exception as e:
        logging.error(f"Error processing CSV: {e}")

if __name__ == "__main__":
    input_csv_file = '/home/aru/Desktop/LFX_test/Financial_chatbot/Dataset/CSV/test_summary.csv'  
    output_csv_file = '/home/aru/Desktop/LFX_test/Financial_chatbot/Dataset/CSV/qna.csv' 

    generate_qna_csv(input_csv_file, output_csv_file)
