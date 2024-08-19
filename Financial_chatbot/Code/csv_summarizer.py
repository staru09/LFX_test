import pandas as pd
import openai
import logging
import time

# Setup logging
logging.basicConfig(level=logging.INFO)

API_BASE_URL = "https://llama.us.gaianet.network/v1"
MODEL_NAME = "llama"
API_KEY = "GAIA"

client = openai.OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

def summarize_text(text):
    try:
        start_time = time.time()
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Summarize the given Content.",
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
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"Error in summarizing text: {e}")
        return "Error: Could not summarize"

def summarize_csv_content(input_csv_file, output_csv_file):
    try:
        df = pd.read_csv(input_csv_file)
        if 'Content' not in df.columns:
            raise ValueError("'Content' column not found in the input CSV file.")

        logging.info("Starting summarization...")
        df['summary'] = df['Content'].apply(lambda x: summarize_text(x) if pd.notnull(x) else "")

        df.to_csv(output_csv_file, index=False)
        logging.info(f"Summaries have been generated and saved to {output_csv_file}")
    except Exception as e:
        logging.error(f"Error processing CSV: {e}")

if __name__ == "__main__":
    input_csv_file = 'Enter_path_to_input_file'  
    output_csv_file = 'Enter_path_to_output_file' 

    summarize_csv_content(input_csv_file, output_csv_file)
