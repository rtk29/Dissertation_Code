# Translating Natural Language requirements to Linear Temporal Logic
This project aims at translating unstructured natural language requirements to Linear Temporal Logic using Large Language Models with a well-designed few shot prompt. For the implementation of __client__ design and its __layout__, the __server__ design, and the style of __basic prompt__, the following github source has been utilised/referenced. The copyright information along with github link is cited in each of the code files that has referenced this source.  
[nl2spec](https://github.com/realChrisHahn2/nl2spec/tree/main)
# Dependencies
* [Flask](https://flask.palletsprojects.com/en/2.2.x/)  
* [LTLf2DFA](https://github.com/whitemech/LTLf2DFA)  
* [Open AI](https://openai.com/blog/openai-api)  
* [Google Cloud AI Platform](https://cloud.google.com/python/docs/reference/aiplatform/latest/index.html)  
# Installation instructions
* pip install flask  
* pip install ltlf2dfa  
* pip install openai  
* pip install google-cloud-aiplatform  

1. Access to Open AI API keys in mandatory. This should be purchased.  
2. To access Google PaLM model, Vertex AI should be enabled.  

# Run from Client
From the main folder:  
* In the keys folder within the main folder, paste your open ai or google project id into: keys/oai_key.txt or keys/google_project_id.txt respectively  
* python3 -m flask --app client.py run  
* Then open web-based tool at http://127.0.0.1:5000  
  
# Run from Server  
* Go to main folder and on the command line interface run the command __python nl2ltl.py --help__  
* __GPT 3.5 Turbo__: python3 nl2ltl.py --model gpt-3.5-turbo --keyfile PATH/TO/YOUR/OPENAIKEY --nl "The vehicle should always brake when an obstacle is detected within a critical distance." --num_tries 3 --temperature 0.2 --prompt basic  
* __Google PaLM__: python3 nl2ltl.py --model text-bison@001 --keyfile PATH/TO/YOUR/GOOGLE_PROJECT-ID --nl "The vehicle should always brake when an obstacle is detected within a critical distance." --num_tries 3 --temperature 0.2 --prompt basic
* The pre-processing is done on the __latex_formulas.txt__ file, and stored in the __modified_formulas.txt__ file
