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
import ambiguity
from ltlf2dfa.parser.ltlf import LTLfParser
import ast


def parse_LTL_formulas(options):
    # Parse LTL formulas using LTLfParser and store the results
    # LTLf2DFA is a tool that transforms an LTLf formula into a minimal Deterministic Finite state Automaton (DFA)
    parser = LTLfParser()
    parsed_LTL_formulas = []

    for option in options:
        try:
            formula_str = option.split("The final LTL translation is:")[1].strip(".")

        except IndexError:
            raise Exception
            #continue

        try:
            parsed_LTL_formula = parser(formula_str)
            parsed_LTL_formulas.append(parsed_LTL_formula)
        except:
            parsed_LTL_formulas.append(formula_str)
    
    return parsed_LTL_formulas


def parse_explanation_dictionary(options, nl):
    parsed_explanation_results = []

    for option in options:
        try:
            dict_string = "{" + option.split("Dictionary")[1].split("{")[1].split("}")[0] + "}"

            # Convert a string representation of a dictionary into an actual dictionary object safely.
            parsed_dict = ast.literal_eval(dict_string)
            
             # Filter out dictionary entries with keys matching the input NL
            parsed_dict = {key: value for key, value in parsed_dict.items() if key != nl}

            if parsed_dict:
                parsed_explanation_results.append(parsed_dict)
        except:
            #raise Exception
            pass

    return parsed_explanation_results

#  Takes a list of translation tuples, extracts information from each tuple, and organizes 
#  that information into separate lists for natural language inputs, LTL forms, certainty scores, and locking statuses
def generate_intermediate_output(intermediate_translation):
    nl_input= []
    ltl_output = []
    certainty_output = []
    locked_output = []

    for translation_tuple in intermediate_translation:
        nl_input.append(translation_tuple[0])
        ltl_output.append(translation_tuple[1])
        certainty_output.append(translation_tuple[2])
        locked_output.append(translation_tuple[3])
 
    intermediate_output = [nl_input, ltl_output, certainty_output, locked_output]
    return intermediate_output



def prompt(args):
    # Takes the natural language input from the command line argument. For example
    # "The brake should not be engaged for more than a certain duration without driver intervention."
    input = args.nl
    prompt_dir = os.path.join("..", "prompts")   

    # Maps the specifics prompt options with their filenames
    prompt_mapping = {
    "basic": "basic.txt"
    }

    # Checks if the prompt value exists in mapping dictionary
    if args.prompt in prompt_mapping:
        prompt_file_path = os.path.join(prompt_dir, prompt_mapping[args.prompt])
        with open(prompt_file_path, 'r') as fixed_prompt_file:
            fixed_prompt = fixed_prompt_file.read()
    else:
        fixed_prompt = args.prompt

    # Checks whether to include the provided translations 
    provided_translations_section = f"Provided translations: {args.provided_translations}" if args.provided_translations != "" else "Provided translations: {}"
    final_prompt = f"{fixed_prompt}\nNatural Language Utterance: {input}\n{provided_translations_section}\nElaboration:"
  
    print("FINAL PROMPT:")
    print(final_prompt)

    return final_prompt


def extract_subinfo(options, args, n):
    parsed_result_formulas = parse_LTL_formulas(options)

    print("Results of multiple runs:")
    print(parsed_result_formulas)

    # Outputs the most freq LTL form and confidence score. Done
    final_translation = ambiguity.ambiguity_final_translation(parsed_result_formulas, n)

    # Outputs a list of dictionaries for each attempt that contains the NL and corresponding AP.
    parse_explain = parse_explanation_dictionary(options, args.nl)
    
    # Generates the intermediate translations(sub-translations)
    intermediate_translation = ambiguity.ambiguity_detection_translations(
        parse_explain,
        n,
        ast.literal_eval(args.locked_translations)
        if "locked_translations" in args
        else {},
    )

    # Returns a list of lists with each list containing the nl, ltl, certainity score and locked transaltion output(boolean) in this order.
    intermediate_output = generate_intermediate_output(intermediate_translation)

    return final_translation, intermediate_output
