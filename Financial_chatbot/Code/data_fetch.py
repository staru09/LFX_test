import requests
import json
import os

# SEC-API Key
API_KEY = 'a21d00c9f744b30bf5c521841aaa4bdc5eca031811a5a0e185bdf2be65d34525'

# Function to fetch 10-Q reports for a public company
def fetch_10q_reports(ticker):
    url = "https://sec-api.com/api/v1/filings"
    params = {
        "token": API_KEY,
        "query": f"ticker:{ticker} AND formType:10-Q",
        "pageSize": 5
    }

    response = requests.get(url, params=params, allow_redirects=False)

    if response.status_code == 302:  # HTTP Redirect
        redirect_url = response.headers.get('Location')
        print("Following redirect to:", redirect_url)
        response = requests.get(redirect_url)
    
    # Check the final response
    print("Status Code:", response.status_code)
    print("Response Text:", response.text[:500])

    if response.status_code == 200:
        try:
            filings = response.json()
            return filings
        except json.decoder.JSONDecodeError as e:
            print("JSON Decode Error:", e)
            return None
    else:
        print("Failed to fetch data:", response.status_code)
        return None

# Function to download and save the filing text
def save_filing_text(filing, output_dir='filings'):
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Extract the URL for the full text
    filing_url = filing['linkToFilingDetails']
    
    # Fetch the filing text
    filing_response = requests.get(filing_url)
    
    if filing_response.status_code == 200:
        # Save the filing text to a .txt file
        filing_name = f"{filing['ticker']}_10Q_{filing['filedAt']}.txt"
        file_path = os.path.join(output_dir, filing_name)
        
        with open(file_path, 'w') as file:
            file.write(filing_response.text)
        
        print(f"Saved: {file_path}")
    else:
        print("Failed to fetch filing text:", filing_response.status_code)


ticker = "AAPL"  
filings = fetch_10q_reports(ticker)

if filings:
    for filing in filings['filings']:
        save_filing_text(filing)
