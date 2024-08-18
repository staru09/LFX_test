from openai import OpenAI

client = OpenAI(api_key="your_openai_api_key_here")

def read_text_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def generate_summary(text, model="gpt-4o-mini", max_tokens=150):
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are an expert in analysing 10-Q reports and summarizes the content of those reports."},
            {"role": "user", "content": text},
        ]
    )
    
    summary = completion.choices[0].message['content'].strip()
    return summary


def main(file_path):
    text = read_text_file(file_path)
    summary = generate_summary(text)
    print("Summary:")
    print(summary)

if __name__ == "__main__":
    input_file_path = "your_text_file.txt" 
    main(input_file_path)

