import os
import csv
import requests
import logging
import time
from github import Github
from urllib.parse import urlparse
import openai

# Setup logging
logging.basicConfig(level=logging.INFO)

# Constants
API_BASE_URL = "https://llama.us.gaianet.network/v1"
MODEL_NAME = "llama"
API_KEY = "GAIA"

# Initialize OpenAI client
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

def get_repo_files(repo_url):
    # Extract owner and repo name from the URL
    parsed_url = urlparse(repo_url)
    path_parts = parsed_url.path.strip('/').split('/')
    owner, repo_name = path_parts[0], path_parts[1]

    # Initialize GitHub client
    g = Github()  # If you have a token, use: g = Github("your_access_token")

    # Get the repository
    repo = g.get_repo(f"{owner}/{repo_name}")

    # Get all files in the repository
    files = []
    contents = repo.get_contents("")
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        else:
            files.append(file_content.path)

    return files

def fetch_file_content(repo_url, file_path):
    # Extract owner and repo name from the URL
    parsed_url = urlparse(repo_url)
    path_parts = parsed_url.path.strip('/').split('/')
    owner, repo_name = path_parts[0], path_parts[1]

    # Initialize GitHub client
    g = Github()  # If you have a token, use: g = Github("your_access_token")

    # Get the repository
    repo = g.get_repo(f"{owner}/{repo_name}")

    # Get file content
    file_content = repo.get_contents(file_path).decoded_content.decode()
    return file_content

def process_files(repo_url, output_csv_file):
    try:
        file_paths = get_repo_files(repo_url)
        
        with open(output_csv_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["File Path", "Summary"])  # Header
            
            for path in file_paths:
                logging.info(f"Processing file: {path}")
                file_content = fetch_file_content(repo_url, path)
                
                # Summarize file content
                summary = summarize_text(file_content)
                writer.writerow([path, summary])
                
                logging.info(f"Summary for {path} added to CSV.")

    except Exception as e:
        logging.error(f"Error processing files: {e}")

if __name__ == "__main__":
    repo_url = input("Enter the GitHub repository URL: ")
    output_csv_file = "repo_file_summaries.csv"

    process_files(repo_url, output_csv_file)
    print(f"File summaries have been saved to {output_csv_file}")
