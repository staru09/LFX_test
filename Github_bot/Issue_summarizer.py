import csv
import logging
import time
from github import Github
from urllib.parse import urlparse
import openai

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
                    "content": "You are an expert in summarizing and understanding various types of code and documentation. Summarize the given text in a concise and coherent manner.",
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

def get_repo_issues(repo_url):
    parsed_url = urlparse(repo_url)
    path_parts = parsed_url.path.strip('/').split('/')
    owner, repo_name = path_parts[0], path_parts[1]

    # Initialize GitHub client
    g = Github() 

    # Get the repository
    repo = g.get_repo(f"{owner}/{repo_name}")

    # Get all issues
    issues = repo.get_issues(state="all")
    issue_list = []
    for issue in issues:
        issue_list.append({
            "title": issue.title,
            "body": issue.body
        })

    return issue_list

def process_issues(repo_url, output_csv_file):
    try:
        issues = get_repo_issues(repo_url)
        
        with open(output_csv_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Issue Title", "Summary"])  
            
            for issue in issues:
                title = issue["title"]
                body = issue["body"]
                logging.info(f"Processing issue: {title}")
                
                # Summarize the issue body
                summary = summarize_text(body)
                writer.writerow([title, summary])
                
                logging.info(f"Summary for issue '{title}' added to CSV.")

    except Exception as e:
        logging.error(f"Error processing issues: {e}")

if __name__ == "__main__":
    repo_url = input("Enter the GitHub repository URL: ")
    output_csv_file = "repo_issues_summaries.csv"

    process_issues(repo_url, output_csv_file)
    print(f"Issue summaries have been saved to {output_csv_file}")
