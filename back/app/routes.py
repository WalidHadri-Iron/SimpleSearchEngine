from flask import request, jsonify
from app import app
from app.services import return_response_sentence, return_details
from uuid import uuid4
from app.middlewares import check_token
import json
import datetime
import sqlite3


#state_dictionnary = dict()
input_sentences_cache = dict()
relevance_cache = dict()
sent_answers = dict()

@app.route("/generate-token", methods=["GET"])
def generate_token():
    #global state_dictionnary

    token = str(uuid4())
    #state_dictionnary[token] = None
    input_sentences_cache[token] = ""
    return jsonify({ 'token': token })

@app.route("/suggestion", methods=["POST"])
def make_suggestions():
    #global state_dictionnary, input_sentences_cache
    global input_sentences_cache

    token = check_token(input_sentences_cache)

    input_sentence = dict(request.get_json()).get('input_sentence', None)
    result = return_response_sentence(input_sentence)
    sent_answers[token] = [element['index'] for element in result]
    input_sentences_cache[token] = input_sentence

    return jsonify(result)

@app.route("/details", methods=["GET"])
def get_details():
    #(state_dictionnary)
    token = check_token(input_sentences_cache)
    index = int(request.args.get("index"))
    result = return_details(index)
    return jsonify(result)

@app.route("/relevance", methods=["POST"])
def is_satisfied():
    #global state_dictionnary, relevance_cache
    global input_sentences_cache, relevance_cache

    token = check_token(input_sentences_cache)

    relevant_suggestions = dict(request.get_json()).get('relevant_suggestions', None)
    relevance_cache[token] = relevant_suggestions

    conn = sqlite3.connect('control.sqlite')
    cur = conn.cursor()

    sqlite_insert_query = f"""INSERT INTO feedbacks
                          (time, token, input, sent, picked)
                           VALUES 
                          ('{str(datetime.datetime.now())}', '{token}', '{input_sentences_cache[token]}', '{", ".join([str(i) for i in sent_answers[token]])}', '{", ".join([str(i) for i in relevant_suggestions])}')"""

    
    count = cur.execute(sqlite_insert_query)
    conn.commit()
    cur.close()
    # with open('feedback.txt', 'a') as file:
    #     write_to_file = str(datetime.datetime.now()) + " " + token + " " + input_sentences_cache[token] + " "+ ', '.join(map(str, relevant_suggestions)) + "\n"
    #     file.write(write_to_file)
    
    return jsonify()

@app.route("/contact", methods=["POST"])
def send_mail():
    global input_sentences_cache

    token = check_token(input_sentences_cache)

    

    return jsonify()
