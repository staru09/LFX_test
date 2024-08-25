import PyPDF2
import csv

def extract_text_from_pdf(pdf_file_path):
    pdf_reader = PyPDF2.PdfReader(pdf_file_path)
    pages_content = []

    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text = page.extract_text()
        pages_content.append(text)
    
    return pages_content

def save_pages_to_csv(pages_content, output_csv_file):
    with open(output_csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Page", "Content"]) 
        for i, content in enumerate(pages_content):
            writer.writerow([i + 1, content])

if __name__ == "__main__":
    input_pdf_file = '.pdf'  # Replace with your PDF file path
    output_csv_file = '.csv'  # Replace with your desired output CSV file path
    
    pages_content = extract_text_from_pdf(input_pdf_file)
    save_pages_to_csv(pages_content, output_csv_file)

    print(f"Content of each page has been extracted and saved to {output_csv_file}")
