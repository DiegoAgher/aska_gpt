import os
import json
import openai

import pandas as pd

from constants import EXAMPLE_DB_NAME


openai.organization = os.getenv("OPENAI_ORG")
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_latest_model(for_chat=True):
	# TODO add functionality to select fine tuned model
	if for_chat:
		return "gpt-3.5-turbo"
	return "text-davinci-003"

def ask_question(question, model=None, add_suffix=False):
	if model is None:
		model = get_latest_model()

	# TODO move this question processing outside of ask_question
	if add_suffix:
		question = question + " ->"

	if model == "gpt-3.5-turbo":
		response = openai.ChatCompletion.create(model=model,
												messages = [{"role": "user",
															 "content": question}])
		text_response = response["choices"][0]["message"]["content"]
	else:
		response = openai.Completion.create(prompt=question, temperature=0.65,
											max_tokens=240, top_p=1, frequency_penalty=0.1,
											presence_penalty=0,
											model=model)
		text_response = response["choices"][0]["text"].strip(" \n")
	
	return text_response

def get_example_db():
	return pd.read_csv(EXAMPLE_DB_NAME)


def validate_filename(filename):
    base_name, ext = os.path.splitext(filename)
    suffix = ""
    count = 1
    new_filename = filename
    
    while os.path.exists(new_filename):
        new_filename = f"{base_name}_{count}{ext}"
        count += 1
    
    return new_filename

# Tell me about disentangled representations in the context of ML