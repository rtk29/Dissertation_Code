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

from argparse import Namespace
from flask import Flask, render_template, request, url_for
import server
import pandas as pd
import os
import json
from dotenv import load_dotenv

# # Load the environment variable from .env file
load_dotenv()

# Fetch the API key from environment variables
#api_key = os.environ["OPENAI_SECRET_KEY"]
api_key = os.environ.get("OPENAI_API_KEY")

# Initializes a Flask web application
app = Flask(__name__, template_folder="../templates", static_folder="../static")

# This code is referenced from github repository https://github.com/realChrisHahn2/nl2spec
# Defines the route for the home page of the web application. It handles both GET and POST requests
@app.route("/", methods=["POST", "GET"])
@app.route("/home/", methods=["POST", "GET"])
@app.route("/nl2ltl/", methods=["POST", "GET"])
def home():
    # Retrieving data from a form submitted via a web request
    form_data = request.form
    if request.method == "POST":
        subtranslation_map, locked_subtranslation_map = subtranslation_gen(form_data)
  
        prompt = form_data["prompts"]
        input = form_data["nl"]
        num_tries = int(form_data["num_tries"])
        temperature = float(form_data["temperature"]) * 0.1
        ground_truth = form_data["ground_truth"] if "ground_truth" in form_data else ""
        
        # If the model is davinci or GTP 3.5
        keyfile = ""
        if (
            form_data["models"] == "gpt-3.5-turbo"
            or form_data["models"] == "code-davinci-edit-001"
        ):
            #keyfile = os.path.join("keys", "oai_key.txt")
            keyfile = api_key

        if form_data["models"] == "text-bison@001":
            keyfile = os.path.join("keys", "google_project_id.txt")
        ns = Namespace(
            keyfile=keyfile,
            maxtokens=150,
            model=form_data["models"],
            nl=input,
            prompt=prompt,
            provided_translations=str(subtranslation_map),
            locked_translations=str(locked_subtranslation_map),
            num_tries=num_tries,
            temperature=temperature,
        )
        
        res = server.call_model(ns)
        final_formula = res[0][0]
        certainty = res[0][1]
        subtranslations = res[1]
        subtranslations_1 = res[1][0]
        subtranslations_2 = res[1][1]
        #examples = load_sample_requirements()
     
        return render_template(
            "home.html",
            examples=load_sample_requirements(),
            ground_truth=ground_truth,
            final_output=final_formula,
            certainty=str(round(certainty * 100, 2)) + "%",
            input=input,
            subnl="",
            subltl="",
            num_tries=num_tries,
            subtranslations=subtranslations,
            models=form_data["models"],
            prompts=prompt,
            temperature=form_data["temperature"],
        )
    return render_template(
        "home.html",
        examples=load_sample_requirements(),
        ground_truth="",
        num_tries=3,
        models="gpt-3.5-turbo",
        prompts="basic",
        temperature=2,
        input="The vehicle should always brake when an obstacle is detected within a critical distance.",
    )

# This code is referenced from github repository https://github.com/realChrisHahn2/nl2spec
# Retrieve data from a CSV file, convert it into JSON format, and provide it as output
def load_sample_requirements():

    #csv_file_path = os.path.join("..", "examples.csv")
    csv_file_path = "examples.csv"
    data_frame = pd.read_csv(csv_file_path, delimiter=";")
    examples_list = data_frame.values.tolist()   
    json_data = json.dumps(examples_list)
    
    return json_data

# This code is referenced from github repository https://github.com/realChrisHahn2/nl2spec
def subtranslation_gen(form_data):
    # number of fixed inputs: nl, prompt, model, temperature, runs = 5
    print(f"The key values of form data are {form_data.keys()}")
    # Hold example natural language sentences
    sub_nl = []
    # Hold corresponding linear temporal logic translations
    sub_ltl = []
    # Store the locking status for each example
    sub_lock = []
    # Extract numeric identifiers from keys in form_data dictionary
    sub_ids = [int(key[len("examplenl"):]) for key in form_data.keys() if key.startswith("examplenl")]
    
    for i in sub_ids:
        nl = form_data["examplenl" + str(i)]        
        ltl = form_data["exampleltl" + str(i)]        
        locked = "lock" + str(i) in form_data
        
        if nl != "" and ltl != "":
            sub_nl.append(nl)
            sub_ltl.append(ltl)
            sub_lock.append(locked)

    # Store translation mappings
    subtranslation_map = {}
    # Store locked mappings
    locked_subtranslation_map = {}

    for i in range(len(sub_nl)):
        subtranslation_map[sub_nl[i]] = sub_ltl[i]
        if sub_lock[i]:
            locked_subtranslation_map[sub_nl[i]] = sub_ltl[i]
 
    return subtranslation_map, locked_subtranslation_map



#print(f"The Open API key stored in Github is {api_key}")
if api_key is None:
    print("Open AI API key not found in environment variables")
else:
    print("Open AI API Key is:", api_key)
