def split_into_sentences(text, words_per_sentence=10):
    words = text.split()
    sentences = []

    for i in range(0, len(words), words_per_sentence):
        sentence = ' '.join(words[i:i + words_per_sentence])
        sentences.append(sentence)
        
    return '\n\n'.join(sentences)

with open('path_to_your_input_file', 'r') as file:
    content = file.read()

modified_content = split_into_sentences(content)

with open('path_to_your_output_file', 'w') as file:
    file.write(modified_content)

print("Text has been split into sentences with 10 words each, and blank lines have been added.")
