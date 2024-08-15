import requests
import csv

def fetch_github_files(api_token, owner, repo):
    headers = {
        'Authorization': f'token {api_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    url = f'https://api.github.com/repos/{owner}/{repo}/git/trees/main?recursive=1'
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()['tree']
    else:
        print(f"Failed to retrieve files: {response.status_code}")
        return []

def save_files_to_csv(files, output_csv):
    with open(output_csv, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['File Name', 'File Path'])
        
        for file in files:
            if file['type'] == 'blob':  
                file_name = file['path'].split('/')[-1]
                file_path = file['path']
                csvwriter.writerow([file_name, file_path])

def main():
    api_token = input("Enter your GitHub API token: ")
    owner = input("Enter the owner of the repository (e.g., username): ")
    repo = input("Enter the repository name: ")
    output_csv = input("Enter the name of the output CSV file: ")

    files = fetch_github_files(api_token, owner, repo)
    if files:
        save_files_to_csv(files, output_csv)
        print(f"CSV file '{output_csv}' created successfully.")

if __name__ == "__main__":
    main()
