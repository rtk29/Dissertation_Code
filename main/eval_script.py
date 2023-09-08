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

import server
import numpy as np
import argparse
from tabulate import tabulate
from ltlf2dfa.parser.ltlf import LTLfParser


def parse_args():
    parser = argparse.ArgumentParser(
        prog="nl2spec",
        description="Translates natural language to LTL formulas.",
    )

    parser.add_argument(
        "--model",
        required=False,
        default="gpt-3.5-turbo",
        help="chose the deep learning model",
    )
    parser.add_argument(
        "--keyfile",
        required=False,
        default="",
        help="provide open ai key (for codex or gpt usage)",
    )
    parser.add_argument(
        "--keydir",
        required=False,
        default="../keys/",
        help="if not specify keyfile, specify directory",
    )
    parser.add_argument(
        "--prompt",
        required=False,
        default="basic",
        help="specifies the name of the promptfile",
    )
    parser.add_argument(
        "--num_tries",
        required=False,
        default=3,
        type=int,
        help="Number of runs the underlying language model attempts a translation.",
    )
    parser.add_argument(
        "--temperature",
        required=False,
        default=0.2,
        type=float,
        help="Model temperature.",
    )
    parser.add_argument(
        "--subtrans_model",
        required=False,
        default="",
        help="chose the deep learning model to render the subtranslations for the student model (see teacher student experiment in the nl2spec paper)",
    )
    parser.add_argument(
        "--datafile",
        required=False,
        default="",
        help="specify dataset file",
    )
    
    parser.add_argument(
        "--smoke",
        required=False,
        default=False,
        action="store_true",
        help="set to run smoke test",
    )
    args = parser.parse_args()
    return args

# This code is referenced from github repository https://github.com/realChrisHahn2/nl2spec
def get_dataset(datafile):
    if datafile == "":        
        f = open("../datasets/requirements_LTL_dataset.txt")
        f.readline()
        NL_list = []
        label_list = []
        for line in f:
            NL_data, label = line.split(";")
            NL_list.append(NL_data)
            
            parser = LTLfParser()
            label_list.append(str(parser(label)))
            
        return NL_list, label_list, None
    else:
        raise

def get_next_provided_translations(server_res):
    final_translation = server_res[0]
    intermediate_output = server_res[1]  # NL, F, confidence
    NL_list = intermediate_output[0]
    T_list = intermediate_output[1]
    confidence_list = intermediate_output[2]
    next_provided_translations = {}
    for i in range(len(NL_list)):
        NL_key = NL_list[i]
        formal_translation = T_list[i][np.argmax(confidence_list[i])]
        next_provided_translations[NL_key] = formal_translation
    return next_provided_translations


def get_final_translation(server_res):
    return str(server_res[0][0]).strip("\n")

# This code is referenced from github repository https://github.com/realChrisHahn2/nl2spec
def call_server(
    nl,
    model,
    prompt,
    num_tries,
    temperature,
    keyfile="",
    keydir="",
    provided_translations="",
    **kwargs
):
    call_args = {
        "model": model,
        "nl": nl,
        "fewshots": "",
        "keyfile": keyfile,
        "keydir": keydir,
        "prompt": prompt,
        "maxtokens": 64,
        "provided_translations": provided_translations,
        "num_tries": num_tries,
        "temperature": temperature,
    }
    call_args = argparse.Namespace(**call_args)
    res = server.call_model(call_args)

    return res


def display_results(NL_list, label_list, predictions, correct_list):
    tab_dict = {
        "input": NL_list,
        "label": label_list,
        "predictions": predictions,
        "correct": correct_list,
    }
    print(tabulate(tab_dict, headers="keys"))


def main():
    args = parse_args()
    
    NL_list, label_list,subtranslation_list = get_dataset(args.datafile)

    predictions = []
    if not args.smoke:
        num_examples = len(NL_list)
    else:
        num_examples = 2
    
    for i in range(num_examples):
        nl = NL_list[i]
        
        if subtranslation_list is not None:
            given_sub_translations = subtranslation_list[i]
        elif args.subtrans_model != "":
            
            teacher_dict = vars(args).copy()
            teacher_dict["model"] = args.subtrans_model
            
            res = call_server(nl,**teacher_dict)
            given_sub_translations = str(get_next_provided_translations(res))
            print("The SUB TRANSLATIONS")
            print(given_sub_translations)
        else:
            
            given_sub_translations = ""
        
        res = call_server(
            nl, **vars(args), provided_translations=given_sub_translations
        )
        predictions.append(get_final_translation(res))

    parser = LTLfParser()
    correct_list = []
    for i in range(len(predictions)):
        try:
            label = parser(label_list[i])
            pred = parser(predictions[i])
            if label == pred:
                correct_list.append(1)
            else:
                correct_list.append(0)
        except Exception as e:
            correct_list.append(0)

    display_results(NL_list, label_list, predictions, correct_list)
    accuracy = np.mean(correct_list)
    print("ACCURACY:", accuracy)
    if args.smoke:
        print("server smoke test success")
    if args.datafile != "":
        save_name = (
            "results-nl2spec_subtranslation-"
            + args.datafile
            + "_model-"
            + args.model
            + "_prompt-"
            + args.prompt
        )
    elif args.subtrans_model != "":
        save_name = (
            "results-nl2spec_teacher-"
            + args.subtrans_model
            + "_student-"
            + args.model
            + "_prompt-"
            + args.prompt
        )
    else:
        save_name = (
            "results-nl2spec_model-"
            + args.model
            + "_prompt-"
            + args.prompt
            + "_initial"
        )

    NL_list.insert(0, "input")
    label_list.insert(0, "label")
    predictions.insert(0, "prediction")
    correct_list.insert(0, "correct")
    np.savetxt(
        save_name + ".txt",
        [p for p in zip(NL_list, label_list, predictions, correct_list)],
        delimiter=";",
        fmt="%s",
    )
    np.savetxt(save_name + ".accuracy", [accuracy])


if __name__ == "__main__":
    main()
