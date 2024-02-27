import csv
import string
import sys
import unicodedata
from greek_stemmer import GreekStemmer
import pandas as pd


maxInt = sys.maxsize
stemmer = GreekStemmer()

while True:
    # decrease the maxInt value by factor 10 
    # as long as the OverflowError occurs.

    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)

def remove_null_speeches():
    df = pd.read_csv('stemmed.csv')
    df_null = df[df['speech'].isnull()]
    df_clean = df.dropna(subset=['speech'])
    df_clean.to_csv('stemmed.csv', index=False)

def remove_whitespaces():
    # Open the CSV file and read the contents into a list of rows
    with open('stemmed.csv', 'r', encoding='utf8') as f:
        reader = csv.reader(f)
        rows = list(reader)

    for i, row in enumerate(rows):
        for j, cell in enumerate(row):
            words = cell.split()
            # Iterate over the words and remove excess white spaces
            for k, word in enumerate(words):
                words[k] = word.strip()
            # Join the modified words back into a single string
            rows[i][j] = ' '.join(words)

    # Write the modified rows back to the CSV file
    with open('stemmed.csv', 'w', newline='', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerows(rows)


def remove_stopwords():
    with open('stopwords.txt', 'r', encoding='utf8') as f:
        stopwords = set(f.read().split(','))
    
    with open('stemmed.csv', 'r', encoding='utf8') as f:
        reader = csv.reader(f)
        rows = list(reader)

    # Iterate over the rows and split the cell values into words
    for i, row in enumerate(rows):
        cell_value = row[10]
        words = cell_value.split()
        # Iterate over the words and decapitalize them
        for k, word in enumerate(words):
            if word in stopwords:
                words[k] = ''
        # Join the modified words back into a single string
        rows[i][10] = ' '.join(words)

    # Write the modified rows back to the CSV file
    with open('stemmed.csv', 'w', newline='', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

def stem():
    with open('stemmed.csv', 'r', encoding='utf8') as f:
        reader = csv.reader(f)
        rows = list(reader)

    # Iterate over the rows and split the cell values into words
    for i, row in enumerate(rows):
        cell_value = row[10]
        words = cell_value.split()
        # Iterate over the words and decapitalize them
        for k, word in enumerate(words):
            words[k] = stemmer.stem(word)
        # Join the modified words back into a single string
        rows[i][10] = ' '.join(words)

    # Write the modified rows back to the CSV file
    with open('stemmed.csv', 'w', newline='', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

def capitalize():
    with open('stemmed.csv', 'r', encoding='utf8') as f:
        reader = csv.reader(f)
        rows = list(reader)

    # Iterate over the rows and split the cell values into words
    for i, row in enumerate(rows):
        for j, cell in enumerate(row):
            words = cell.split()
            # Iterate over the words and decapitalize them
            for k, word in enumerate(words):
                words[k] = word.upper()
            # Join the modified words back into a single string
            rows[i][j] = ' '.join(words)

    # Write the modified rows back to the CSV file
    with open('stemmed.csv', 'w', newline='', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

def remove_accents():
    with open('stemmed.csv', 'r', encoding='utf8') as f:
        reader = csv.reader(f)
        rows = list(reader)

    # Iterate over the rows and split the cell values into words
    for i, row in enumerate(rows):
        for j, cell in enumerate(row):
            words = cell.split()
            # Iterate over the words and decapitalize them
            for k, word in enumerate(words):
                # Normalize the text using the NFD form
                normalized_text = unicodedata.normalize('NFD', word)
                # Keep only characters that are not accents or diacritics
                unaccented_text = ''.join(c for c in normalized_text if not unicodedata.combining(c))
                words[k] = unaccented_text
            # Join the modified words back into a single string
            rows[i][j] = ' '.join(words)

    # Write the modified rows back to the CSV file
    with open('stemmed.csv', 'w', newline='', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerows(rows)


def decapitilize():
    with open('stemmed.csv', 'r', encoding='utf8') as f:
        reader = csv.reader(f)
        rows = list(reader)

    # Iterate over the rows and split the cell values into words
    for i, row in enumerate(rows):
        for j, cell in enumerate(row):
            words = cell.split()
            # Iterate over the words and decapitalize them
            for k, word in enumerate(words):
                words[k] = word.lower()
            # Join the modified words back into a single string
            rows[i][j] = ' '.join(words)

    # Write the modified rows back to the CSV file
    with open('stemmed.csv', 'w', newline='', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerows(rows)


# Function that removes punctuation marks
def remove_punctuation():
    # Open the CSV file and read the contents into a list of rows
    with open('test.csv', 'r', encoding='utf8') as f:
        reader = csv.reader(f)
        rows = list(reader)

    # Create a translation table to remove punctuation marks
    translator = str.maketrans('', '', string.punctuation)

    # Iterate over the rows and remove the punctuation marks
    for i, row in enumerate(rows):
        rows[i] = [cell.translate(translator) for cell in row]

    # Write the modified rows back to the CSV file
    with open('stemmed.csv', 'w', newline='', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerows(rows)


if __name__ == '__main__':
    remove_punctuation()
    decapitilize()
    remove_accents()
    remove_stopwords()
    capitalize()
    stem()
    decapitilize()
    remove_whitespaces()
    remove_null_speeches()


