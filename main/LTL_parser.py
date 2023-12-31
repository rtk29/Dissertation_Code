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

import argparse

def parse_args():
    parser = argparse.ArgumentParser(
                        prog = 'NL2LTL',
                        description = 'Translates natural language to LTL formulas',)

    parser.add_argument('--model', required=False, default="gpt-3.5-turbo", help='Choose the deep learning model')
    parser.add_argument('--nl', required=True, default="", help='Input NL requirement') 
    parser.add_argument('--fewshots', required=False, default="",  help='provide few shot examples')
    parser.add_argument('--keyfile', required=False, default="", help='provide open ai key (for codex usage), or a huggingface api key (for bloom usage)')
    parser.add_argument('--keydir', required=False, default="", help='if not specify keyfile, specify directory')
    parser.add_argument('--prompt', required=False, default="basic", help='Specify the name of the prompt')
    parser.add_argument('--maxtokens', required=False, default=64, help='Maximum number of tokens to compute')
    parser.add_argument('--provided_translations', required=False, default="", help='Provides given translations')
    parser.add_argument('--num_tries', type=int, required=False, default=3, help="Number of runs the underlying language model attempts a translation.")
    parser.add_argument('--temperature', required=False, default=0.2, type=float, help="Model temperature.")
    args = parser.parse_args()
    
    return args
