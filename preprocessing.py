import io
import os
import re
import shutil
import string
import typing_extensions
from flask import jsonify

# import tensorflow as tf
# from tensorflow.python.keras import Sequential
# from tensorflow.python.keras.layers import Dense, Embedding, GlobalAveragePooling1D
# from tensorflow.python.keras.layers import TextVectorization

# The python library to implement the text preprocessing tasks is nltk

import nltk
from nltk import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords 
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer 
nltk.download('punkt')

nltk.download('words')
from nltk.corpus import words
from nltk.corpus import PlaintextCorpusReader
from fuzzywuzzy import process

from medical_lists import known_terms, normalization_dict



# Get the path to the words corpus
words_corpus_path = words.abspath('')

# Create a list of custom words
custom_words = ['wbc']

# Create a new corpus by extending the words corpus and the custom word list
all_words = words.words() + custom_words

# english_words = set(words.words())

from nltk.corpus import brown

# Load the NLTK stop words
nltk.download("stopwords")
stop_words = set(stopwords.words('english')) 

# Load the NLTK lemmatizer
nltk.download('wordnet')
lemmatizer = WordNetLemmatizer()

# Function to remove elements that are only symbols
def remove_symbols(words_list):
    # Create a new list to store the filtered words
    filtered_words = []
    # Define a regex pattern for matching symbols
    symbol_pattern = r'^\W+$'  # \W matches any non-word character
    for word in words_list:
        # Check if the word contains only symbols or is an empty string
        if not re.match(symbol_pattern, word) and word != "":
            filtered_words.append(word)
    return filtered_words

def expand_abbreviations(text, abbreviations_dict):
    """
    This function will expand abbreviations found in the text based on the provided dictionary.
    """
    # for abbr, full_form in abbreviations_dict.items():
    #     text = text.replace(abbr, full_form)
    # return text
    sorted_abbreviations = dict(sorted(abbreviations_dict.items(), key=lambda item: len(item[0]), reverse=True))
    for abbr, full_form in sorted_abbreviations.items():
        text = re.sub(r'\b' + abbr + r'\b', full_form, text)
    return text

def clean_tokens(tokens, known_terms, cutoff=80):
    """
    This function will clean up the tokens using fuzzy matching with the known terms.
    """
    cleaned_tokens = {}
    for token, value in tokens.items():
        best_match, score = process.extractOne(token, known_terms)
        if score > cutoff:
            cleaned_tokens[best_match] = value
        else:
            cleaned_tokens[token] = value
    return cleaned_tokens

def filter_known_terms(data, known_terms):
    return {term: value for term, value in data.items() if term in known_terms}


def normalize_terms(text, normalization_dict):
    """
    This function will normalize the medical terms found in the text based on the provided dictionary.
    """
    for term, standard_term in normalization_dict.items():
        text = text.replace(term, standard_term)
    return text

def generate_values(sentences):
    # Create a list to store the values
    extracted_terms_and_values = {}
    for sentence in sentences:
        # Extract term and value assuming first word is term and second word is value
        if len(sentence) >= 2:
            term_words = [sentence[0]]
            value = None

            # Loop through words in the sentence to find a word that can be converted to a float
            for word in sentence[1:]:
                try:
                    # Try converting the word to float
                    float_value = float(word)
                    # If conversion is successful, assign the float value as the value
                    value = float_value
                    break
                except ValueError:
                    # If the word cannot be converted to a float, check if it's an English word
                    if word.lower() in all_words and len(word.lower()) > 2:
                        # If it's an English word, add it to the term_words list
                        term_words.append(word)

            # If a value was found, add the term and value to the extracted_terms_and_values dictionary
            if value is not None:
                term = ' '.join(term_words)
                term = term.replace('.', '')
                # expanded_text = expand_abbreviations(term, abbreviations_dict)
                normalized_text = normalize_terms(term, normalization_dict)
                extracted_terms_and_values[normalized_text] = value
    
    return extracted_terms_and_values

# Preprocess text
def preprocess_text(text):
    # Tokenize the text into individual words
    tokens = word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word.lower() for word in tokens if word.lower() not in stop_words and word.isalpha()]
    
    return tokens


def generate_tokens(text):
    # lower casing
    lower_sents = text.lower().split('\n')

    # Create a list of lists to represent the grid
    sentences = []
    for sentence in lower_sents:
        # Tokenize each sentence into words
        words = word_tokenize(sentence)

        # Remove stop words
        words = [word for word in words if word not in stop_words]

        # Lemmatize words
        # words = [lemmatizer.lemmatize(word) for word in words]

        # Filter words that do not match the regex pattern
        words = [word for word in words if not re.match(r'^\W+$', word)]

        # Add the list of words as a row in the grid
        sentences.append(words)

    # Extract medical terms and their values from the grid
    # print("sentences are",sentences)
    tokens = generate_values(sentences)
    # print(values)
    cleaned_tokens = clean_tokens(tokens, known_terms)
    filtered_data = filter_known_terms(cleaned_tokens, known_terms)

    return filtered_data
