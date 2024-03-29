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

import models


def call_model(args):
    model = args.model
    
    # Select Bison model
    if model == "text-bison@001":
        return models.text_bison_001(args)
    
    # Select Davinci model
    if model == "code-davinci-edit-001":
        return models.code_davinci_edit_001(args)
    
    # Select GPT model
    if model == "gpt-3.5-turbo":
        return models.gpt_35_turbo(args)
    
    raise Exception("Invalid model selected. Not in the list of models")
    
    
