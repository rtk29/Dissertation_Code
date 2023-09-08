#! D:\Dissertation\Papers\nl2spec-main\nl2spec-main\myenv\Scripts\python.exe

# This code is referenced from github repository https://github.com/realChrisHahn2/nl2spec

import models


def call_model(args):
    model = args.model

    if model == "text-bison@001":
        return models.text_bison_001(args)
    
    if model == "code-davinci-edit-001":
        return models.code_davinci_edit_001(args)
    
    if model == "gpt-3.5-turbo":
        return models.gpt_35_turbo(args)
    
    raise Exception("Invalid model selected. Not in the list of models")
    
    
