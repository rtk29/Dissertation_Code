# MIT License
# 
# Copyright (c) 2023 Christoper Hahn
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# This code is referenced from github repository https://github.com/realChrisHahn2/nl2spec

import os
#from statistics import mode

import openai
import requests
import vertexai
from transformers import AutoModel, AutoModelForCausalLM, AutoTokenizer, pipeline
from vertexai.preview.language_models import TextGenerationModel

import prompting

from dotenv import load_dotenv

# # Load the environment variable from .env file
load_dotenv()

# Fetch the API key from environment variables
api_key = os.environ['OPENAI_API_KEY']
#api_key = os.environ.get('OPENAI_API_KEY')



def gpt_35_turbo(args):

    #Read the open AI key from the text file in keys folder and store it.
    #keyfile = args.keyfile if args.keyfile != "" else os.path.join(args.keydir, "oai_key.txt")
    #with open(keyfile, 'r') as file:
       #key = file.readline().rstrip("\n")

    if not api_key:
        raise Exception("No key provided in the file")    
    openai.api_key = api_key

    # Specify the number of times the model attempts a translation.
    n = 3 if args.num_tries == "" else min(int(args.num_tries), 5)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",                        # Specifies the model to be used
        messages=[{"role": "user", "content": prompting.prompt(args)}],    # Prime the model with a few-shot prompt
        n=n,                                          # Represents the number of responses to generate.
        temperature=args.temperature,                 # Sets the temperature parameter for controlling the randomness of the response. 
        stop="FINISH",                                # Stops generating text once it encounters the string "FINISH"
    )
    choices = []
    
    for i in range(0, n):
        output = response["choices"][i]["message"]["content"]
        print(f"OUTPUT {i}")
        print(output)
        choices.append(output)
        print()
        print(f" The choices list is {choices}")
    return prompting.extract_subinfo(choices, args, n)
    #return [[0,0],[1,1]]


def code_davinci_edit_001(args):
    
    # Read the open AI key from the text file in keys folder and store it.
    # keyfile = args.keyfile if args.keyfile != "" else os.path.join(args.keydir, "oai_key.txt")
    # with open(keyfile, 'r') as file:
    #     key = file.readline().rstrip("\n")
    if not openai.api_key:
        raise Exception("No key provided in the file")    
    openai.api_key = api_key

    # Specify the number of times the model attempts a translation.
    n = 3 if args.num_tries == "" else min(int(args.num_tries), 5)

    prompt = prompting.prompt(args) + " REPLACE"
    response = openai.Edit.create(
        model="code-davinci-edit-001",
        input=prompt,
        instruction="replace REPLACE with the explanation, an explanation dictionary and the final translation",
        temperature=args.temperature,
        top_p=1,
        n=n,
    )
    choices = []
    for i in range(0, n):
        output = response["choices"][i]["text"][len(prompt) - 8 :].split("FINISH")[0]
        choices.append(output)
    return prompting.extract_subinfo(choices, args, n)


def text_bison_001(args):

    # Access the google PaLM model via the google cloud platform project id with Vertex AI Enabled
    keyfile = args.keyfile if args.keyfile != "" else os.path.join(args.keydir, "google_project_id.txt")
    with open(keyfile, 'r') as file:
        key = file.readline().rstrip("\n")
    if not key:
        raise Exception("No key provided in the file")    
    
    # Initialize the vertex AI module from google cloud Ai platform 
    vertexai.init(project=key)
    model = TextGenerationModel.from_pretrained("text-bison@001")

    def query():
        return model.predict(
            prompting.prompt(args), temperature=args.temperature, max_output_tokens=300
        )

    choices = []
    for i in range(0, args.num_tries):
        repsonse = query()
        output = repsonse.text.split("FINISH")[0]
        choices.append(output)
    return prompting.extract_subinfo(choices, args, args.num_tries)

