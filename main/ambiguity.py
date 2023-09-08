# This code is referenced from github repository https://github.com/realChrisHahn2/nl2spec

from statistics import mode

# Takes a list of dictionaries, merges them into a single dictionary with case-insensitive keys,
# and returns the merged dictionary.
def merge_explanation_dicts(explanation_dict_list):
    merged_dict = {}

    for explanation_dict in explanation_dict_list:
        for key in explanation_dict:
            normalized_key = key.lower()
            if normalized_key not in merged_dict:
                merged_dict[normalized_key] = [explanation_dict[key]]
            else:
                merged_dict[normalized_key].append(explanation_dict[key])

    return merged_dict


# Fill each list value in the dictionary with the string "None" followed by an 
# incrementing number until the length of each list reaches at least n elements.
# Ensure consistency in list lengths and providing default filler values when necessary.
def fill_dict_with_none(dictionary, n):
    for key in dictionary:
        i = 0
        while len(dictionary[key]) < n:
            dictionary[key].append("None" + str(i))
            i += 1
    return dictionary



def most_freq(parsed_lst):
    if len(parsed_lst) == 0:
        return "No output. The parsed ltl formula list is empty."
    try:
        # Returns the most commonly parsed LTL formula
        most_common = mode(parsed_lst)
    except:
        most_common = parsed_lst[0]
    return most_common


def count_occurences(parsed_lst, parsed_element):
    occurrences_count = 0
    
    for e in parsed_lst:
        if e == parsed_element:
            occurrences_count += 1
    return occurrences_count


def calculate_certainty_score(parsed_lst, parsed_element, n):
    occurrences = count_occurences(parsed_lst, parsed_element)
    return occurrences / n

# Optimizes the input dictionary with certainty scores and reduce its contents
def add_certainty_and_reduce(merged_dict, n):
    # Initializes an empty dictionary to hold the reduced and enhanced results
    reduced_dict = {}
    
    # Iterates through each key-value pair in the input dictionary
    for key, value_list in merged_dict.items():
        # Initializes an empty list to store elements along with their associated certainty scores.
        certainty_list = []
        
        # Iterates through each element in the list associated with the current key.
        for element in value_list:
            # Calculate a certainty score for the current element based on the entire list and num of tries.
            score = calculate_certainty_score(value_list, element, n)
            if not element.startswith("None"):
                certainty_list.append((element, round(score * 100, 2)))
        
        # Removes duplicate entries while preserving the order
        certainty_list = list(set(certainty_list))

        # Sorts certainty_list based on the certainty score in descending order
        certainty_list = sorted(certainty_list, key=lambda x: x[1], reverse=True)

        # Assigns the certainty_list to the corresponding key in the reduced dictionarys
        reduced_dict[key] = certainty_list

    return reduced_dict



def ambiguity_detection_translations(explain_dict_list, n, locked_translations):
    # Takes a list of dictionaries, merges them into a single dictionary with case-insensitive keys,
    # and returns the merged dictionary.
    merge_d = merge_explanation_dicts(explain_dict_list)
 
    # Fill each list value in the dictionary with the string "None" till the last element of the list.
    merge_d = fill_dict_with_none(merge_d, n)
 
    # Optimizes the input dictionary with certainty scores and reduce its contents.
    reduced_d = add_certainty_and_reduce(merge_d, n)
 
    # Updates the subtransalations dcitionary based on the information of locked translations.
    reduced_d = add_locked_subtranslation(reduced_d, locked_translations)

    # Organize the above dictionary that includes three separate lists for each key in the dictionary containing 
    # subtranslations, certainity scores, locking status.
    certainty_triple_list = [
    (
        key,
        [entry[0] for entry in reduced_d[key]],
        [entry[1] for entry in reduced_d[key]],
        [entry[2] for entry in reduced_d[key]],
    )
    for key in reduced_d.keys()
    ]
    # Sorts the triple list based on the maximum locking status values within each certainty triple.
    return sorted(certainty_triple_list, key=lambda x: max(x[2]))


def add_locked_subtranslation(model_subtranslations, locked_subtranslations):
    # Creates a copy of the model_subt dictionary while setting the third element of each entry tuple to False. 
    # This indicates that the subtranslation is not locked.
    model_subtranslations = {
        key: [(entry[0], entry[1], False) for entry in model_subtranslations[key]]
        for key in model_subtranslations
    }
 
    # Iterates through the keys in the locked_subt dictionary
    for key in locked_subtranslations:
        # update the corresponding entry in model_subt if key is present
        if key in model_subtranslations:
            # Initializes a variable to hold the entry targeted for modification
            target_entry = None
            
            # Iterates through the entries for the current key in model_subt.
            for entry in model_subtranslations[key]:
                # Checks if the first element of the current entry matches the corresponding value from locked_subt.
                if entry[0] == locked_subtranslations[key]:
                    target_entry = entry

            if target_entry is None:
                model_subtranslations[key] = [(locked_subtranslations[key], 0.0, True)] + model_subtranslations[key]
            else:
                model_subtranslations[key].remove(target_entry)
                model_subtranslations[key] = [(locked_subtranslations[key], target_entry[1], True)] + model_subtranslations[key]
        else:
            model_subtranslations[key] = [(locked_subtranslations[key], 0.0, True)]
            
    return model_subtranslations



def ambiguity_final_translation(parsed_result_formulas, n):
    # Find out the most parsed LTL formula
    most_frequent_ltl = most_freq(parsed_result_formulas)

    # calculate the certainity score
    certainty_score = calculate_certainty_score(parsed_result_formulas, most_frequent_ltl, n)

    return most_frequent_ltl, certainty_score
