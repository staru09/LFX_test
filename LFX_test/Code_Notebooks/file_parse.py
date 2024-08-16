import requests
import openai
import csv
import base64
import json

def get_default_branch(api_token, owner, repo):
    headers = {
        'Authorization': f'token {api_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    url = f'https://api.github.com/repos/{owner}/{repo}'
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()['default_branch']
    else:
        print(f"Failed to retrieve repository information: {response.status_code}")
        return None

def fetch_github_files(api_token, owner, repo, branch):
    headers = {
        'Authorization': f'token {api_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    url = f'https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1'
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()['tree']
    else:
        print(f"Failed to retrieve files: {response.status_code}")
        return []

def get_file_content(api_token, owner, repo, path):
    headers = {
        'Authorization': f'token {api_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}'
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()['content']
    else:
        print(f"Failed to retrieve file content: {response.status_code}")
        return ""

def extract_code_from_notebook(decoded_content):
    notebook = json.loads(decoded_content)
    code_cells = []

    for cell in notebook['cells']:
        if cell['cell_type'] == 'code':
            code = ''.join(cell['source'])
            code_cells.append(code)

    return '\n'.join(code_cells)

def summarize_text(api_key, text):
    openai.api_key = api_key
    try:
        response = openai.ChatCompletion.create(
            messages=[
                {"role": "system", "content": "You are an expert Github repo analyser who reads jupyter notebooks and summarizes them."},
                {"role": "user", "content": f"Summarize the following code:\n\n{text}"}
            ],
            max_tokens=2000
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Failed to summarize text: {e}")
        return ""

def summarize_repository(api_token, api_key, owner, repo, output_csv):
    branch = get_default_branch(api_token, owner, repo)
    if branch is None:
        print("Could not determine the default branch. Exiting.")
        return
    
    files = fetch_github_files(api_token, owner, repo, branch)
    if not files:
        return

    with open(output_csv, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['File Name', 'File Path', 'Summary'])

        for file in files:
            if file['type'] == 'blob' and file['path'].endswith('.ipynb'):
                file_name = file['path'].split('/')[-1]
                file_path = file['path']
                
                # Fetch the content of the file
                content = get_file_content(api_token, owner, repo, file_path)
                if content:
                    try:
                        decoded_content = base64.b64decode(content).decode('utf-8')
                        code_cells = extract_code_from_notebook(decoded_content)
                        
                        if code_cells:
                            summary = summarize_text(api_key, code_cells)
                            print(f"Summary for {file_name}: {summary}")
                        else:
                            summary = "No code cells found."
                        
                    except (UnicodeDecodeError, base64.binascii.Error, json.JSONDecodeError) as e:
                        print(f"Error processing {file_name}: {e}")
                        summary = "Error processing file."
                    
                    csvwriter.writerow([file_name, file_path, summary])
                else:
                    print(f"Content for {file_name} is empty or could not be retrieved.")
                    csvwriter.writerow([file_name, file_path, "No content retrieved"])

def main():
    combined_input = input("Enter your GitHub API token, OpenAI API key, repository owner, and repository name (comma-separated): ")
    github_api_token, openai_api_key, owner, repo = [item.strip() for item in combined_input.split(',')]
    output_csv = input("Enter the name of the output CSV file: ")

    summarize_repository(github_api_token, openai_api_key, owner, repo, output_csv)
    print(f"CSV file '{output_csv}' created successfully.")

if __name__ == "__main__":
    main()
