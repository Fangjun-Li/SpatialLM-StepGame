#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to process and correct StepGame data for spatial reasoning.
Created on Mon Jul 10 15:27:34 2023
@author: fangjun
"""
import os
import re


#https://github.com/ZhengxiangShi/StepGame/blob/main/Code/template.py

AA_left_BB = [
    "AA is to the left of BB.",
    "AA is at BB’s 9 o'clock.",
    "AA is positioned left to BB.",
    "AA is on the left side to BB.",
    "AA and BB are parallel, and AA on the left of BB.",
    "AA is to the left of BB horizontally.",
    "The object labeled AA is positioned to the left of the object labeled BB.",
    "BB is over there and AA is on the left.",
    "AA is placed in the left direction of BB.",
    "AA is on the left and BB is on the right.",
    "AA is sitting at the 9:00 position of BB.",
    "AA is sitting in the left direction of BB.",
    "BB is over there and AA is on the left of it.",
    "AA is at the 9 o'clock position relative to BB.",
    "AA and BB are parallel, and AA is to the left of BB.",
    "AA and BB are horizontal and AA is to the left of BB.",
    "AA and BB are in a horizontal line with AA on the left.",
    "AA is to the left of BB with a small gap between them.",
    "AA is on the same horizontal plane directly left to BB.",
    "AA is to the left of BB and is on the same horizontal plane.",
    "BB and AA are side by side with BB to the right and AA to the left.",
    "AA and BB are both there with the object AA is to the left of object BB.",
    "AA and BB are next to each other with BB on the right and AA on the left.",
    "AA presents left to BB.",
]


BB_right_AA = [
    "BB is to the right of AA.",
    "BB is at AA's 3 o'clock.",
    "BB is positioned right to AA.",
    "BB is on the right side to AA.",
    "AA and BB are parallel, and AA on the right of BB.", # AA and BB are parallel, and AA on the right of BB.
    "BB is to the right of AA horizontally.",
    "The object labeled BB is positioned to the right of the object labeled AA.",
    "AA is over there and BB is on the right.",
    "BB is placed in the right direction of AA.",
    "BB is on the right and AA is on the left.",
    "BB is sitting at the 3:00 position to AA.",
    "BB is sitting in the right direction of AA.",
    "AA is over there and BB is on the right of it.",
    "BB is at the 3 o'clock position relative to AA.",
    "AA and BB are parallel, and AA is to the right of BB.", # AA and BB are parallel, and AA is to the right of BB.
    "AA and BB are horizontal and AA is to the right of BB.",#AA and BB are horizontal and AA is to the right of BB.
    "AA and BB are in a horizontal line with BB on the right.",
    "BB is to the right of AA with a small gap between them.",
    "BB is on the same horizontal plane directly right to AA.",
    "BB is to the right of AA and is on the same horizontal plane.",
    "AA and BB are side by side with AA to the left and BB to the right.",
    "AA and BB are both there with the object AA is to the right of object BB.", #AA and BB are both there with the object AA is to the right of object BB.
    "AA and BB are next to each other with AA on the left and BB on the right.",
    "BB presents right to AA.",
]

AA_over_BB = [
    "AA is over BB.",
    "AA is above BB.",
    "AA is directly above BB.",
    "AA is on top of BB.",
    "AA is at BB's 12 o'clock.",
    "AA is positioned above BB.",
    "AA is on the top side to BB.",
    "AA and BB are parallel, and AA is over BB.",
    "AA is to the top of BB vertically.",
    "AA is over there with BB below.",
    "The object AA is positioned directly above the object BB.",
    "BB is over there and AA is directly above it.",
    "AA is placed on the top of BB.",
    "AA is on the top and BB is at the bottom.",
    "AA is sitting at the 12:00 position to BB.",
    "AA is sitting at the top position to BB.",
    "BB is over there and AA is on the top of it.",
    "AA is at the 12 o'clock position relative to BB.",
    "AA and BB are parallel, and AA is on top of BB.",
    "AA and BB are vertical and AA is above BB.",
    "AA and BB are in a vertical line with AA on top.",
    "AA is above BB with a small gap between them.",
    "AA is on the same vertical plane directly above BB.",
    "AA is on the top of BB and is on the same vertical plane.",
    "AA and BB are side by side with AA on the top and BB at the bottom.",
    "AA and BB are both there with the object AA above the object BB.",
    "AA and BB are next to each other with AA on the top and BB at the bottom.",
    "AA presents over BB.",
]

BB_below_AA =  [
    "BB is under AA.",
    "BB is below AA.",
    "BB is directly below AA.",
    "BB is at the bottom of AA.",
    "BB is at AA's 6 o'clock.",
    "BB is positioned below AA.",
    "BB is at the lower side of AA.",
    "BB and AA are parallel, and BB is under AA.",
    "BB is at the bottom of AA vertically.",
    "BB is over there with AA above.",
    "The object BB is positioned directly below the object AA.",
    "AA is over there and BB is directly below it.",
    "AA is placed at the bottom of BB.",   ##AA is placed at the bottom of BB.
    "BB is at the bottom and AA is on the top.",
    "BB is sitting at the 6:00 position to AA.",
    "BB is sitting at the lower position to AA.",
    "AA is over there and BB is at the bottom of it.",
    "BB is at the 6 o'clock position relative to AA.",
    "AA and BB are parallel, and BB is below AA.",
    "BB and AA are vertical and BB is below AA.",
    "AA and BB are in a vertical line with BB below AA.",
    "BB is below AA with a small gap between them.",
    "BB is on the same vertical plane directly below AA.",
    "AA is at the bottom of BB and is on the same vertical plane.", #AA is at the bottom of BB and is on the same vertical plane.
    "AA and BB are side by side with BB at the bottom and AA on the top.",
    "AA and BB are both there with the object BB below the object AA.",
    "AA and BB are next to each other with BB at the bottom AA on the top.",
    "AA presents below BB."  ##AA presents below BB.
]

AA_lowerleft_BB = [
    "AA is on the lower left of BB.",
    "AA is to the bottom left of BB.",
    "The object AA is lower and slightly to the left of the object BB.",
    "AA is on the left side of and below BB.",
    "AA is positioned in the lower left corner of BB.",
    "AA is lower left to BB.",
    "AA is to the bottom-left of BB.",
    "AA is below BB at 7 o'clock.",
    "AA is positioned down and to the left of BB.",
    "The object AA is positioned below and to the left of the object BB.",
    "AA is diagonally left and below BB.",
    "AA is placed at the lower left of BB.",
    "AA is sitting at the lower left position to BB.",
    "BB is there and AA is at the 10 position of a clock face.", # BB is there and AA is at the 10 position of a clock face.
    "AA is to the left of BB and below BB at approximately a 45 degree angle.",
    "AA is south west of BB.",
    "AA is below and to the left of BB.",
    "The objects AA and BB are over there. The object AA is lower and slightly to the left of the object BB.",
    "AA is directly south west of BB.",
    "BB is positioned below AA and to the left.", ## BB is positioned below AA and to the left.
    "AA is at a 45 degree angle to BB, in the lower lefthand corner.",
    "AA is diagonally below BB to the left at a 45 degree angle.",
    "Object AA is below object BB and to the left of it, too.",
    "AA is diagonally to the bottom left of BB.",
    "AA presents lower left to BB.",
    "If BB is the center of a clock face, AA is located between 7 and 8.",
    "AA is below BB and to the left of BB.",
]

BB_upperright_AA = [
    "BB is on the upper right of AA.",
    "BB is to the top right of AA.",
    "The object BB is upper and slightly to the right of the object AA.",
    "BB is on the right side and top of AA.",
    "BB is positioned in the front right corner of AA.",
    "BB is upper right to AA.",
    "BB is to the top-right of AA.",
    "BB is above AA at 2 o'clock.",
    "BB is positioned up and to the right of AA.",
    "The object BB is positioned above and to the right of the object AA.",
    "BB is diagonally right and above AA.",
    "BB is placed at the upper right of AA.",
    "BB is sitting at the upper right position to AA.",
    "AA is there and BB is at the 2 position of a clock face.",
    "BB is to the right and above AA at an angle of about 45 degrees.",
    "BB is north east of AA.",
    "BB is above and to the right of AA.",
    "The objects BB and AA are over there. The object BB is above and slightly to the right of the object AA.",
    "BB is directly north east of AA.",
    "BB is positioned above AA and to the right.",
    "BB is at a 45 degree angle to AA, in the upper righthand corner.",
    "BB is diagonally above AA to the right at a 45 degree.",
    "Object A is above object BB and to the right of it, too.", #Object A is above object BB and to the right of it, too.
    "AA is diagonally to the upper right of BB.", #AA is diagonally to the upper right of BB.
    "BB presents upper right to AA.",
    "If AA is the center of a clock face, BB is located between 2 and 3.",
    "BB is above AA and to the right of AA.", 
]

AA_lowerright_BB = [
    "AA is on the lower right of BB.",
    "AA is to the bottom right of BB.",
    "The object AA is lower and slightly to the right of the object BB.",
    "AA is on the right side and below BB.",
    "BB is slightly off center to the top left and AA is slightly off center to the bottom right.",
    "AA is positioned in the lower right corner of BB.",
    "AA is lower right of BB.",
    "AA is to the bottom-right of BB.",
    "AA is below BB at 4 o'clock.",
    "AA is positioned below and to the right of BB.",
    "The object AA is positioned below and to the right of the object BB.",
    "AA is diagonally right and below BB.",
    "AA is placed at the lower right of BB.",
    "AA is sitting at the lower right position to BB.",
    "BB is there and AA is at the 5 position of a clock face.",
    "AA is to the right and above BB at an angle of about 45 degrees.", #AA is to the right and above BB at an angle of about 45 degrees.
    "AA is south east of BB.",
    "AA is below and to the right of BB.",
    "The object AA and BB are there. The object AA is below and slightly to the right of the object BB.",
    "AA is directly south east of BB.",
    "AA is positioned below BB and to the right.",
    "AA is at a 45 degree angle to BB, in the lower righthand corner.",
    "AA is diagonally below BB to the right at a 45 degree angle.",
    "Object AA is below object BB and to the right of it, too.",
    "AA is diagonally to the bottom right of BB.",
    "AA presents lower right to BB.",
    "If AA is the center of a clock face, BB is located between 10 and 11.",
    "AA is below BB and to the right of BB.",
]

BB_upperleft_AA = [
    "BB is to the upper left of AA.",
    "BB is to the upper left of AA.",
    "The object BB is upper and slightly to the left of the object AA.",
    "BB is on the left side and above AA.",
    "BB is slightly off center to the top left and AA is slightly off center to the bottom right.",
    "BB is positioned in the top left corner of AA.",
    "BB is upper left of AA.",
    "BB is to the top-left of AA.",
    "BB is above AA at 10 o'clock.",
    "BB is positioned above and to the left of AA.",
    "The object BB is positioned above and to the left of object AA.",
    "BB is diagonally left and above BB.",  ##BB is diagonally left and above BB.
    "BB is placed at the upper left of AA.",
    "BB is sitting at the upper left position to AA.",
    "AA is there and BB is at the 10 position of a clock face.",
    "BB is to the right and above AA at an angle of about 45 degrees.", #BB is to the right and above AA at an angle of about 45 degrees.
    "BB is north west of AA.",
    "BB is above and to the left of AA.",
    "The object AA and BB are there. The object BB is above and slightly to the left of the object AA.",
    "BB is directly north west of AA.",
    "BB is positioned above AA and to the left.",
    "BB is at a 45 degree angle to AA, in the upper lefthand corner.",
    "BB is diagonally above AA to the left at a 45 degree angle.",
    "Object BB is above object AA and to the left of it, too.",
    "BB is diagonally to the upper left of AA.",
    "BB presents upper left to AA.",
    "If BB is the center of a clock face, AA is located between 4 and 5.",
    "BB is above AA and to the left of AA.",
]

# Combine all templates into one list
all_templates = AA_left_BB + BB_right_AA + AA_over_BB + BB_below_AA + AA_lowerleft_BB + BB_upperright_AA + AA_lowerright_BB + BB_upperleft_AA



# Incorrect to correct statement mapping based on the table
incorrect_to_correct_mapping = {
    r"(?P<obj1>\b\w+\b) and (?P<obj2>\b\w+\b) are parallel, and \1 on the right of \2": r"\1 and \2 are parallel, and \2 on the right of \1",
    r"(?P<obj1>\b\w+\b) and (?P<obj2>\b\w+\b) are parallel, and \1 is to the right of \2": r"\1 and \2 are parallel, and \2 is to the right of \1",
    r"(?P<obj1>\b\w+\b) and (?P<obj2>\b\w+\b) are horizontal and \1 is to the right of \2": r"\1 and \2 are horizontal and \2 is to the right of \1",
    r"(?P<obj1>\b\w+\b) and (?P<obj2>\b\w+\b) are both there with the object \1 is to the right of object \2": r"\1 and \2 are both there with the object \2 is to the right of object \1",
    r"(?P<obj1>\b\w+\b) is at the bottom of (?P<obj2>\b\w+\b) and is on the same vertical plane": r"\2 is at the bottom of \1 and is on the same vertical plane",
    r"(?P<obj1>\b\w+\b) presents below (?P<obj2>\b\w+\b)": r"\2 presents below \1",
    r"(?P<obj1>\b\w+\b) is placed at the bottom of (?P<obj2>\b\w+\b)": r"\2 is placed at the bottom of \1",    
    r"(?P<obj2>\b\w+\b) is there and (?P<obj1>\b\w+\b) is at the 10 position of a clock face": r"\2 is there and \1 is at the 8 position of a clock face",
    r"(?P<obj2>\b\w+\b) is positioned below (?P<obj1>\b\w+\b) and to the left": r"\2 is positioned below \1 iand to the left",
    r"Object (?P<obj1>\b\w+\b) is above object (?P<obj2>\b\w+\b) and to the right of it, too": r"Object \2 is above object \1 and to the right of it, too",
    r"(?P<obj1>\b\w+\b) is diagonally to the upper right of (?P<obj2>\b\w+\b)": r"\2 is diagonally to the upper right of  \1",
    r"(?P<obj1>\b\w+\b) is to the right and above (?P<obj2>\b\w+\b) at an angle of about 45 degrees": r"\1 is to the right and below \2 at an angle of about 45 degrees",
    r"(?P<obj2>\b\w+\b) is to the right and above (?P<obj1>\b\w+\b) at an angle of about 45 degrees": r"\2 is to the left and above \1 at an angle of about 45 degrees",
    r"(?P<obj1>\b\w+\b) is diagonally left and above (?P<obj2>\b\w+\b)": r"\1 is diagonally left and above \2",
}

    
# Read the text file
DATA_PATHS = (
    # [f'data/clean/qa{i}_train.txt' for i in range(1, 11)] +
    # [f'data/clean/qa{i}_valid.txt' for i in range(1, 11)] +
    [f'data/clean/qa{i}_test.txt' for i in range(1, 11)] +
    # [f'data/noise/qa{i}_train.txt' for i in range(1, 11)] +
    # [f'data/noise/qa{i}_valid.txt' for i in range(1, 11)] +
    [f'data/noise/qa{i}_test.txt' for i in range(1, 11)]
)


def process_file(path):
    print(path)
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    inp = ''
    
    data = []
    examples = []
    examples_correct = []
    example_in=[]
    original_text=[]
    for line in lines:   
        if line.strip().endswith('1'):
            inp += line
            original_text.append(inp)
            inp = ''
        else:
            inp += line
    
    for line in lines:   
        _, line = line.strip().split(' ', 1)
        if line.endswith('1'):
            line, target, _ = line.split('\t')
            inp += line
            data.append([[inp],[target]])
            example_in.append(line)  ###### note this when calculate the sentence number
            examples.append(example_in)
            example_in = []
            inp = ''
        else:
            inp += line + '\n'  
            example_in.append(line)

    
    
    # Initialize counts
    total_sentences = 0
    total_examples = 0
    incorrect_sentences = 0
    incorrect_examples = 0
    wrong_sentences = []
    
    # Go through each group of len(examples) lines in the file
    for i in range(len(examples)):
        example = examples[i]
        total_examples += 1
        example_incorrect = False
        for line in example:
            line = line.strip()  # remove trailing spaces and newline characters
            if line:  # if line is not empty
                total_sentences += 1
                # Check against each incorrect pattern
                # for incorrect_pattern, correct_pattern in list(incorrect_to_correct_mapping.items())[-2:]:  # Only the last two mappings
                for incorrect_pattern, correct_pattern in list(incorrect_to_correct_mapping.items()):
                    if re.search(incorrect_pattern, line):
                        incorrect_sentences += 1
                        example_incorrect = True
                        ###This part add for rectified_data#####
                        #corrected_sentence = re.sub(incorrect_pattern, correct_pattern, line)
                        ###This part add for rectified_data#####
                        break  # No need to check other patterns once a match is found
                    
        if example_incorrect:
            incorrect_examples += 1
        else:
            examples_correct.append(original_text[i])
    
# =============================================================================
#     if 'clean' in path:
#         path_write = path.replace("clean", "correct_clean")
#     elif 'noise' in path:
#         path_write = path.replace("noise", "correct_noise")
#     else:
#         path_write = path
# 
#     # Create the directory for correct data if it doesn't exist
#     directory = os.path.dirname(path_write)
#     if not os.path.exists(directory):
#         os.makedirs(directory)
# 
#     # Write the corrected data
#     with open(path_write, 'w', encoding='utf-8') as file:
#         for line in examples_correct:
#             file.write(line)
# =============================================================================
    
    return total_examples, incorrect_examples


    
def main():
    for path in DATA_PATHS:
        total_examples, incorrect_examples = process_file(path)  
        print("incorrect exmaple rate:", "{:.2f}".format(incorrect_examples/total_examples*100))
        print("Number of right examples:", total_examples-incorrect_examples)


if __name__ == "__main__":
    main()