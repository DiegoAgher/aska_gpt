import openai

def ask_question(question):
	fine_tuned_model = get_latest_model()
	question = question + " ->"
	response = openai.Completion.create(prompt=question, temperature=0.65,
									max_tokens=240, top_p=1, frequency_penalty=0.1,
									presence_penalty=0,
									model=fine_tuned_model)["choices"][0]["text"].strip(" \n")
	return response