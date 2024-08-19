import pandas as pd
import openai

API_BASE_URL = "https://llama.us.gaianet.network/v1"
MODEL_NAME = "llama"
API_KEY = "GAIA"
client = openai.OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

def summarize_text(text):
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
    return response.choices[0].message.content

def summarize_csv_Content(input_csv_file, output_csv_file):
    df = pd.read_csv(input_csv_file)
    if 'Content' not in df.columns:
        raise ValueError("'Content' column not found in the input CSV file.")

    df['summary'] = df['Content'].apply(lambda x: summarize_text(x) if pd.notnull(x) else "")

    df.to_csv(output_csv_file, index=False)

    print(f"Summaries have been generated and saved to {output_csv_file}")

if __name__ == "__main__":
    input_csv_file = r'Financial_chatbot\Dataset\CSV\output_pages.csv'  
    output_csv_file = r'Financial_chatbot\Dataset\CSV\output_summary.csv' 

    summarize_csv_Content(input_csv_file, output_csv_file)
