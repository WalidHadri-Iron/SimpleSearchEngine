from flask import render_template, request, redirect, jsonify
from app import app
from app.controlname import *
import os, json

with open('config.json') as json_file:
    config = json.load(json_file)

split_columns = config["split_columns"]
exclude = config["exclude"]
path_excel_file = config["path_excel_file"]


in_sentences = []
reponse_keep = None
def formatting_control(dict_result):
    string_out = ""
    for key in dict_result.keys():
        string_out += f"{key}: {dict_result[key]}"
        string_out+='<br /> \u00A0'
    return string_out



def handle_user_input(user_input):
    
    global in_sentences, reponse_keep, feedbacks

    
    df = pd.read_excel(path_excel_file, sheet_name="ALL_ANONYMISED")
    reponse_result = return_response(path_excel_file, user_input, split_columns, exclude)
    if user_input == "restart":
        in_sentences = []
        reponse_keep = None
        return "You can start another search"
    if len(in_sentences) == 0:
        if len(reponse_result) == 0:
            return "Nothing Found, please try again"
        if len(reponse_result) > 1:
            reponse_keep = reponse_result
            in_sentences.append(user_input)
            string_out = "The found results are <br /> \u00A0"
            i = 1
            for key in reponse_result.keys():
                string_out+=f"{i}. {reponse_result[key]['Control name']}"
                string_out+='<br /> \u00A0'
                i += 1
            string_out = string_out[:-8]
            string_out+='<br /> \u00A0'
            string_out += "Choose the number of the control you want to explore (Type in -1, if none of the control names matches your search)"
            return string_out
    if len(in_sentences) == 1:
        #in_sentences.append("Step of choosing")
        if int(user_input) == -1:
            #Sending_mail_function()
            feedback = dict()
            feedback["request"] = in_sentences[0]
            feedback["result_picked"] = None
            feedback["status"] = -1
            
            feedbacks = json.load(open('feedbacks.json'))

            feedbacks.append(feedback)
            # write list to file
            with open('feedbacks.json', 'w') as outfile:
                json.dump(feedbacks, outfile)
            in_sentences = []
            reponse_keep = None
            return "A mail will be sent to the support to answer your request ASAP" + '<br /> \u00A0' + "You can start another search"
        else:
            try:
                in_sentences.append(list(reponse_keep.keys())[int(user_input)-1])
                string_out = formatting_control(reponse_keep[list(reponse_keep.keys())[int(user_input)-1]])
                string_out+='<br /> \u00A0'
                string_out+='<br /> \u00A0'
                string_out+="If you are statisfied with the result please enter 1 otherwise -1, a mail will be sent to the support to answer your request ASAP"
                return string_out
            except:
                return "Please give a correct index"
    if len(in_sentences) == 2:
        feedback = dict()
        feedback["request"] = in_sentences[0]
        if int(user_input) == 1:
            feedback["result_picked"] = in_sentences[1]
            feedback["status"] = 1
            feedbacks = json.load(open('feedbacks.json'))
            feedbacks.append(feedback)
            # write list to file
            with open('feedbacks.json', 'w') as outfile:
                json.dump(feedbacks, outfile)
        else:
            #Sending_mail_function()
            feedback["result_picked"] = in_sentences[1]
            feedback["status"] = 0
            feedbacks = json.load(open('feedbacks.json'))
            feedbacks.append(feedback)
            # write list to file
            with open('feedbacks.json', 'w') as outfile:
                json.dump(feedbacks, outfile)
        in_sentences = []
        reponse_keep = None
        return "You can start another search"

@app.route("/")
def home():
    return render_template("index.html")
 
@app.route("/get")
def bot_response():
    user_message = request.args.get('msg')
    return handle_user_input(user_message)

@app.route("/response")
def reponse():
    path_excel_file = "Controls_dictionnary_202110_A.xlsx"
    df = pd.read_excel(path_excel_file, sheet_name="ALL_ANONYMISED")
    user_message = in_sentences[0]
    return return_response(path_excel_file, user_message, split_columns, exclude)
