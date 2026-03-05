import csv
import json

def load_csv(filepath, target_language, target_difficulty):
    words = []
    #Open the file in read mode
    with open(filepath, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['language'] == target_language and row['difficulty'] == target_difficulty:
                words.append(row['word'])
    return words    

def load_json(filepath):
    with open(filepath, mode='r', encoding='utf-8') as file:
        return json.load(file)
    

'''
AI Assistance Disclaimer:
This project incorporates concepts and suggestions generated through NotebookLM. The Gemini AI model served as a technical consultant to ensure the desired architecture, specific libraries, and general best practices.
'''