import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk import ngrams
import texthero as hero
from texthero import preprocessing
from collections import Counter
import math
import random
from datetime import datetime


w_tokenizer = nltk.tokenize.WhitespaceTokenizer()
lemmatizer = nltk.stem.WordNetLemmatizer()


custom_pipeline = [preprocessing.fillna, preprocessing.lowercase, preprocessing.remove_diacritics, preprocessing.remove_brackets, preprocessing.remove_stopwords,
                  preprocessing.remove_punctuation, preprocessing.stem, preprocessing.remove_whitespace]

def lemmatize_text(text):
    return ' '.join([lemmatizer.lemmatize(w) for w in w_tokenizer.tokenize(text)])


def count_common_words(listA, listB):
    """
    Return the percentage of common words between two lists
    
    listA: List
    listB: List
    
    Example:
    count_common_words(["machine","learning","homerun", "Shakespeare"],["learning","homerun","home","parents", "Teacher"])
    >>>0.2857142857142857
    """
    
    listA.sort()
    listB.sort()
    counterA = Counter(listA)
    counterB = Counter(listB)
    terms_union = set(counterA).union(counterB)
    terms_intersect = set(counterA).intersection(counterB)
    return len(terms_intersect)/len(terms_union)

def counter_cosine_similarity(listA, listB):
    """
    Return the cosine similarity between two lists
    
    listA: List
    listB: List
    
    Example:
    counter_cosine_similarity(["machine","complex","homerun", "Shakespeare"],["complexes","homerun","home","parents", "Teacher"])
    >>>0.22360679774997896
    """
    
    counterA = Counter(listA)
    counterB = Counter(listB)
    
    terms = set(counterA).union(counterB)
    dotprod = sum(counterA.get(k, 0) * counterB.get(k, 0) for k in terms)
    magA = math.sqrt(sum(counterA.get(k, 0)**2 for k in terms))
    magB = math.sqrt(sum(counterB.get(k, 0)**2 for k in terms))
    return dotprod / (magA * magB)

def compare_two_tokenized_sentences(first_tokenized_sentence, second_tokenized_sentence, similarity="Cosine"):
    """
    
    Cosine
    Common_words
    """
    if similarity == "Cosine":
        return counter_cosine_similarity(first_tokenized_sentence, second_tokenized_sentence)
    if similarity == "Common_words":
        return count_common_words(first_tokenized_sentence, second_tokenized_sentence)
    
def comparaison_ngrams(sentence1, sentence2):
    """
    """
    
    
    w_g = [1/6,2/6,3/6]
    grams_list = [1,2,3]
    final_score = 0
    for k in range(len(grams_list)) :
        n_grams_1 = list(ngrams(sentence1.split(), grams_list[k]))
        n_grams_2 = list(ngrams(sentence2.split(), grams_list[k]))
        scores_grams = []
        for i in range(len(n_grams_1)):
            max_for_gram_1 = -2
            for j in range(len(n_grams_2)):
                score_gram = compare_two_tokenized_sentences(list(n_grams_1[i]), list(n_grams_2[j]))
                if score_gram > max_for_gram_1:
                    max_for_gram_1 = score_gram
            scores_grams.append(max_for_gram_1)
        final_score += w_g[k]*sum(scores_grams)/len(n_grams_1)
    if final_score<0:
        return 0
    return final_score

def compare_with_column(sentence, row, column, split_columns, method="spacy"):
    sentence = pd.Series(sentence)
    sentence = hero.clean(sentence, custom_pipeline).values[0]
    if pd.isna(row[column]) or row[column]=='':
        return 0
    if column not in split_columns:
        if method == 'basic_cosine_similarity':
            return compare_two_tokenized_sentences(word_tokenize(sentence), word_tokenize(row[column]), similarity="Cosine")
        if method == 'basic_common_words':
            return compare_two_tokenized_sentences(word_tokenize(sentence), word_tokenize(row[column]), similarity="Common_words")
        if method == "n_grams":
            return comparaison_ngrams(sentence, row[column])
            
    else:
        sentence_2 = row[column]
        sentence_2 = sentence_2.replace(' |', ' ,')
        list_split = sentence_2.split(',')
        list_split = [i.strip() for i in list_split]
        score = []
        if method == 'basic_cosine_similarity':
            for sentence_ in list_split:
                if sentence_.strip()=='':
                    continue
                score.append(compare_two_tokenized_sentences(word_tokenize(sentence), word_tokenize(sentence_), similarity="Cosine"))
        if method == 'basic_common_words':
            for sentence_ in list_split:
                score.append(compare_two_tokenized_sentences(word_tokenize(sentence), word_tokenize(sentence_), similarity="Common_words"))
        if method == 'n_grams':
            for sentence_ in list_split:
                score.append(comparaison_ngrams(sentence,sentence_))
        score = sum(score)
        return score
    
def calculate_score(df, sentence, method, row, exclude, split_columns):
    total_score = 0
    for column in list(set(df.columns) - set(exclude)):
        score = compare_with_column(sentence, row, column, split_columns, method)
        total_score += score
    return total_score

def return_best_n(df, df_cleaned, sentence, method, exclude, split_columns, top=5):
    df_cleaned['total_score'] = df_cleaned.apply(lambda x: calculate_score(df, sentence, method, x, exclude, split_columns), axis=1)
    out = df_cleaned.sort_values(by='total_score', ascending=False)
    out = out[out.total_score>0]
    return list(out.index)[:top]

