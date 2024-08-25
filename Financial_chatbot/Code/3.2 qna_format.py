import csv

def convert_csv_to_output(input_file, output_file):
    with open(input_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)

        with open(output_file, 'w') as outfile:
            for row in reader:
                column_1 = row[0]
                column_2 = row[1]
                outfile.write(f"<SFT><s>[INST] <<SYS>>\n You are a financial assistant. Provide detailed, clear, and professional financial insights, and ensure that your responses are easy to understand. \n<</SYS>>\n\n {column_1} [/INST] {column_2} \n")

# Testing the function
input_file = '/home/aru/Desktop/LFX_test/Financial_chatbot/Dataset/CSV/qna_test.csv'  
output_file = '/home/aru/Desktop/LFX_test/Financial_chatbot/Dataset/Text/test.txt' 
convert_csv_to_output(input_file, output_file)
