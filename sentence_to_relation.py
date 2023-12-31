#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to process and correct StepGame data for spatial reasoning.
Created on Mon Jul 10 15:27:34 2023
@author: fangjun
"""

sentence_to_relation = {
   
r"What is the relation of the agent (?P<obj1>[A-Z]) to the agent (?P<obj2>[^\s?]+)\?": r"\1_query_\2",

# left
r"(?P<obj1>[A-Z]) is to the left of (?P<obj2>[A-Z]).": r"\1_left_\2",
r"(?P<obj1>[A-Z]) is at (?P<obj2>[A-Z])’s 9 o'clock.": r"\1_left_\2",
r"(?P<obj1>[A-Z]) is positioned left to (?P<obj2>[A-Z]).": r"\1_left_\2",
r"(?P<obj1>[A-Z]) is on the left side to (?P<obj2>[A-Z]).": r"\1_left_\2",
r"(?P<obj1>[A-Z]) and (?P<obj2>[A-Z]) are parallel, and \1 on the left of \2.": r"\1_left_\2",
r"(?P<obj1>[A-Z]) is to the left of (?P<obj2>[A-Z]) horizontally.": r"\1_left_\2",
r"The object labeled (?P<obj1>[A-Z]) is positioned to the left of the object labeled (?P<obj2>[A-Z]).": r"\1_left_\2",
r"(?P<obj1>[A-Z]) is over there and (?P<obj2>[A-Z]) is on the left.": r"\2_left_\1",
r"(?P<obj1>[A-Z]) is placed in the left direction of (?P<obj2>[A-Z]).": r"\1_left_\2",
r"(?P<obj1>[A-Z]) is on the left and (?P<obj2>[A-Z]) is on the right.": r"\1_left_\2",
r"(?P<obj1>[A-Z]) is sitting at the 9:00 position of (?P<obj2>[A-Z]).": r"\1_left_\2",
r"(?P<obj1>[A-Z]) is sitting in the left direction of (?P<obj2>[A-Z]).": r"\1_left_\2",
r"(?P<obj1>[A-Z]) is over there and (?P<obj2>[A-Z]) is on the left of it.": r"\2_left_\1",
r"(?P<obj1>[A-Z]) is at the 9 o'clock position relative to (?P<obj2>[A-Z]).": r"\1_left_\2",
r"(?P<obj1>[A-Z]) and (?P<obj2>[A-Z]) are parallel, and \1 is to the left of \2.": r"\1_left_\2",
r"(?P<obj1>[A-Z]) and (?P<obj2>[A-Z]) are horizontal and \1 is to the left of \2.": r"\1_left_\2",
r"(?P<obj1>[A-Z]) and (?P<obj2>[A-Z]) are in a horizontal line with \1 on the left.": r"\1_left_\2",
r"(?P<obj1>[A-Z]) is to the left of (?P<obj2>[A-Z]) with a small gap between them.": r"\1_left_\2",
r"(?P<obj1>[A-Z]) is on the same horizontal plane directly left to (?P<obj2>[A-Z]).": r"\1_left_\2",
r"(?P<obj1>[A-Z]) is to the left of (?P<obj2>[A-Z]) and is on the same horizontal plane.": r"\1_left_\2",
r"(?P<obj1>[A-Z]) and (?P<obj2>[A-Z]) are side by side with \1 to the right and \2 to the left.": r"\2_left_\1",
r"(?P<obj1>[A-Z]) and (?P<obj2>[A-Z]) are both there with the object \1 is to the left of object \2.": r"\1_left_\2",
r"(?P<obj1>[A-Z]) and (?P<obj2>[A-Z]) are next to each other with \2 on the right and \1 on the left.": r"\1_left_\2",
r"(?P<obj1>[A-Z]) presents left to (?P<obj2>[A-Z]).": r"\1_left_\2",

# right
r"(?P<obj1>[A-Z]) is to the right of (?P<obj2>[A-Z]).": r"\1_right_\2",
r"(?P<obj1>[A-Z]) is at (?P<obj2>[A-Z])'s 3 o'clock.": r"\1_right_\2",
r"(?P<obj1>[A-Z]) is positioned right to (?P<obj2>[A-Z]).": r"\1_right_\2",
r"(?P<obj1>[A-Z]) is on the right side to (?P<obj2>[A-Z]).": r"\1_right_\2",
# r"(?P<obj1>[A-Z]) and (?P<obj2>[A-Z]) are parallel, and \1 on the right of \2.": r"\1_right_\2",
r"(?P<obj1>[A-Z]) is to the right of (?P<obj2>[A-Z]) horizontally.": r"\1_right_\2",
r"The object labeled (?P<obj1>[A-Z]) is positioned to the right of the object labeled (?P<obj2>[A-Z]).": r"\1_right_\2",
r"(?P<obj1>[A-Z]) is over there and (?P<obj2>[A-Z]) is on the right.": r"\2_right_\1",
r"(?P<obj1>[A-Z]) is placed in the right direction of (?P<obj2>[A-Z]).": r"\1_right_\2",
r"(?P<obj1>[A-Z]) is on the right and (?P<obj2>[A-Z]) is on the left.": r"\1_right_\2",
r"(?P<obj1>[A-Z]) is sitting at the 3:00 position to (?P<obj2>[A-Z]).": r"\1_right_\2",
r"(?P<obj1>[A-Z]) is sitting in the right direction of (?P<obj2>[A-Z]).": r"\1_right_\2",
r"(?P<obj1>[A-Z]) is over there and (?P<obj2>[A-Z]) is on the right of it.": r"\2_right_\1",
r"(?P<obj1>[A-Z]) is at the 3 o'clock position relative to (?P<obj2>[A-Z]).": r"\1_right_\2",
# r"(?P<obj1>[A-Z]) and (?P<obj2>[A-Z]) are parallel, and \1 is to the right of \2": r"\1_right_\2",
# r"(?P<obj1>[A-Z]) and (?P<obj2>[A-Z]) are horizontal and \1 is to the right of \2.": r"\1_right_\2",
r"(?P<obj1>[A-Z]) and (?P<obj2>[A-Z]) are in a horizontal line with \2 on the right.": r"\2_right_\1",
r"(?P<obj1>[A-Z]) is to the right of (?P<obj2>[A-Z]) with a small gap between them.": r"\1_right_\2",
r"(?P<obj1>[A-Z]) is on the same horizontal plane directly right to (?P<obj2>[A-Z]).": r"\1_right_\2",
r"(?P<obj1>[A-Z]) is to the right of (?P<obj2>[A-Z]) and is on the same horizontal plane.": r"\1_right_\2",
r"(?P<obj1>[A-Z]) and (?P<obj2>[A-Z]) are side by side with \1 to the left and \2 to the right.": r"\2_right_\1",
r"(?P<obj1>[A-Z]) and (?P<obj2>[A-Z]) are both there with the object \2 is to the right of object \1.": r"\2_right_\1",
r"(?P<obj1>[A-Z]) and (?P<obj2>[A-Z]) are next to each other with \1 on the left and \2 on the right.": r"\2_right_\1",
r"(?P<obj1>[A-Z]) presents right to (?P<obj2>[A-Z]).": r"\1_right_\2",

# over
r"(?P<obj1>[A-Z]) is over (?P<obj2>[A-Z]).": r"\1_over_\2",
r"(?P<obj1>[A-Z]) is above (?P<obj2>[A-Z]).": r"\1_over_\2",
r"(?P<obj1>[A-Z]) is directly above (?P<obj2>[A-Z]).": r"\1_over_\2",
r"(?P<obj1>[A-Z]) is on top of (?P<obj2>[A-Z]).": r"\1_over_\2",
r"(?P<obj1>[A-Z]) is at (?P<obj2>[A-Z])'s 12 o'clock.": r"\1_over_\2",
r"(?P<obj1>[A-Z]) is positioned above (?P<obj2>[A-Z]).": r"\1_over_\2",
r"(?P<obj1>[A-Z]) is on the top side to (?P<obj2>[A-Z]).": r"\1_over_\2",
r"(?P<obj1>[A-Z]) and (?P<obj2>[A-Z]) are parallel, and \1 is over \2.": r"\1_over_\2",
r"(?P<obj1>[A-Z]) is to the top of (?P<obj2>[A-Z]) vertically.": r"\1_over_\2",
r"(?P<obj1>[A-Z]) is over there with (?P<obj2>[A-Z]) below.": r"\1_over_\2",
r"The object (?P<obj1>[A-Z]) is positioned directly above the object (?P<obj2>[A-Z]).": r"\1_over_\2",
r"(?P<obj1>[A-Z]) is over there and (?P<obj2>[A-Z]) is directly above it.": r"\2_over_\1",
r"(?P<obj1>[A-Z]) is placed on the top of (?P<obj2>[A-Z]).": r"\1_over_\2",
r"(?P<obj1>[A-Z]) is on the top and (?P<obj2>[A-Z]) is at the bottom.": r"\1_over_\2",
r"(?P<obj1>[A-Z]) is sitting at the 12:00 position to (?P<obj2>[A-Z]).": r"\1_over_\2",
r"(?P<obj1>[A-Z]) is sitting at the top position to (?P<obj2>[A-Z]).": r"\1_over_\2",
r"(?P<obj1>[A-Z]) is over there and (?P<obj2>[A-Z]) is on the top of it.": r"\2_over_\1",
r"(?P<obj1>[A-Z]) is at the 12 o'clock position relative to (?P<obj2>[A-Z]).": r"\1_over_\2",
r"(?P<obj1>[A-Z]) and (?P<obj2>[A-Z]) are parallel, and \1 is on top of \2.": r"\1_over_\2",
r"(?P<obj1>[A-Z]) and (?P<obj2>[A-Z]) are vertical and \1 is above \2.": r"\1_over_\2",
r"(?P<obj1>[A-Z]) and (?P<obj2>[A-Z]) are in a vertical line with \1 on top.": r"\1_over_\2",
r"(?P<obj1>[A-Z]) is above (?P<obj2>[A-Z]) with a small gap between them.": r"\1_over_\2",
r"(?P<obj1>[A-Z]) is on the same vertical plane directly above (?P<obj2>[A-Z]).": r"\1_over_\2",
r"(?P<obj1>[A-Z]) is on the top of (?P<obj2>[A-Z]) and is on the same vertical plane.": r"\1_over_\2",
r"(?P<obj1>[A-Z]) and (?P<obj2>[A-Z]) are side by side with \1 on the top and \2 at the bottom.": r"\1_over_\2",
r"(?P<obj1>[A-Z]) and (?P<obj2>[A-Z]) are both there with the object \1 above the object \2.": r"\1_over_\2",
r"(?P<obj1>[A-Z]) and (?P<obj2>[A-Z]) are next to each other with \1 on the top and \2 at the bottom.": r"\1_over_\2",
r"(?P<obj1>[A-Z]) presents over (?P<obj2>[A-Z]).": r"\1_over_\2",

# below
r"(?P<obj1>[A-Z]) is under (?P<obj2>[A-Z]).": r"\1_below_\2",
r"(?P<obj1>[A-Z]) is below (?P<obj2>[A-Z]).": r"\1_below_\2",
r"(?P<obj1>[A-Z]) is directly below (?P<obj2>[A-Z]).": r"\1_below_\2",
r"(?P<obj1>[A-Z]) is at the bottom of (?P<obj2>[A-Z]).": r"\1_below_\2",
r"(?P<obj1>[A-Z]) is at (?P<obj2>[A-Z])'s 6 o'clock.": r"\1_below_\2",
r"(?P<obj1>[A-Z]) is positioned below (?P<obj2>[A-Z]).": r"\1_below_\2",
r"(?P<obj1>[A-Z]) is at the lower side of (?P<obj2>[A-Z]).": r"\1_below_\2",
r"(?P<obj1>[A-Z]) and (?P<obj2>[A-Z]) are parallel, and \1 is under \2.": r"\1_below_\2",
r"(?P<obj1>[A-Z]) is at the bottom of (?P<obj2>[A-Z]) vertically.": r"\1_below_\2",
r"(?P<obj1>[A-Z]) is over there with (?P<obj2>[A-Z]) above.": r"\1_below_\2",
r"The object (?P<obj1>[A-Z]) is positioned directly below the object (?P<obj2>[A-Z]).": r"\1_below_\2",
r"(?P<obj1>[A-Z]) is over there and (?P<obj2>[A-Z]) is directly below it.": r"\2_below_\1",
# r"(?P<obj2>[A-Z]) is placed at the bottom of (?P<obj1>[A-Z]).": r"\1_below_\2", ##AA is placed at the bottom of BB.
r"(?P<obj1>[A-Z]) is at the bottom and (?P<obj2>[A-Z]) is on the top.": r"\1_below_\2",
r"(?P<obj1>[A-Z]) is sitting at the 6:00 position to (?P<obj2>[A-Z]).": r"\1_below_\2",
r"(?P<obj1>[A-Z]) is sitting at the lower position to (?P<obj2>[A-Z]).": r"\1_below_\2",
r"(?P<obj1>[A-Z]) is over there and (?P<obj2>[A-Z]) is at the bottom of it.": r"\2_below_\1",
r"(?P<obj1>[A-Z]) is at the 6 o'clock position relative to (?P<obj2>[A-Z]).": r"\1_below_\2",
r"(?P<obj1>[A-Z]) and (?P<obj2>[A-Z]) are parallel, and \2 is below \1.": r"\2_below_\1",
r"(?P<obj1>[A-Z]) and (?P<obj2>[A-Z]) are vertical and \1 is below \2.": r"\1_below_\2",
r"(?P<obj1>[A-Z]) and (?P<obj2>[A-Z]) are in a vertical line with \2 below \1.": r"\2_below_\1",
r"(?P<obj1>[A-Z]) is below (?P<obj2>[A-Z]) with a small gap between them.": r"\1_below_\2",
r"(?P<obj1>[A-Z]) is on the same vertical plane directly below (?P<obj2>[A-Z]).": r"\1_below_\2",
# r"(?P<obj2>[A-Z]) is at the bottom of (?P<obj1>[A-Z]) and is on the same vertical plane.": r"\1_below_\2", #AA is at the bottom of BB and is on the same vertical plane.
r"(?P<obj1>[A-Z]) and (?P<obj2>[A-Z]) are side by side with \2 at the bottom and \1 on the top.": r"\2_below_\1",
r"(?P<obj1>[A-Z]) and (?P<obj2>[A-Z]) are both there with the object \2 below the object \1.": r"\2_below_\1",
r"(?P<obj1>[A-Z]) and (?P<obj2>[A-Z]) are next to each other with \2 at the bottom \1 on the top.": r"\2_below_\1",
# r"(?P<obj2>[A-Z]) presents below (?P<obj1>[A-Z]).": r"\1_below_\2",  ##AA presents below BB.



# lowerleft
r"(?P<obj1>[A-Z]) is on the lower left of (?P<obj2>[A-Z]).": r"\1_lowerleft_\2",
r"(?P<obj1>[A-Z]) is to the bottom left of (?P<obj2>[A-Z]).": r"\1_lowerleft_\2",
r"The object (?P<obj1>[A-Z]) is lower and slightly to the left of the object (?P<obj2>[A-Z]).": r"\1_lowerleft_\2",
r"(?P<obj1>[A-Z]) is on the left side of and below (?P<obj2>[A-Z]).": r"\1_lowerleft_\2",
r"(?P<obj1>[A-Z]) is positioned in the lower left corner of (?P<obj2>[A-Z]).": r"\1_lowerleft_\2",
r"(?P<obj1>[A-Z]) is lower left to (?P<obj2>[A-Z]).": r"\1_lowerleft_\2",
r"(?P<obj1>[A-Z]) is to the bottom-left of (?P<obj2>[A-Z]).": r"\1_lowerleft_\2",
r"(?P<obj1>[A-Z]) is below (?P<obj2>[A-Z]) at 7 o'clock.": r"\1_lowerleft_\2",
r"(?P<obj1>[A-Z]) is positioned down and to the left of (?P<obj2>[A-Z]).": r"\1_lowerleft_\2",
r"The object (?P<obj1>[A-Z]) is positioned below and to the left of the object (?P<obj2>[A-Z]).": r"\1_lowerleft_\2",
r"(?P<obj1>[A-Z]) is diagonally left and below (?P<obj2>[A-Z]).": r"\1_lowerleft_\2",
r"(?P<obj1>[A-Z]) is placed at the lower left of (?P<obj2>[A-Z]).": r"\1_lowerleft_\2",
r"(?P<obj1>[A-Z]) is sitting at the lower left position to (?P<obj2>[A-Z]).": r"\1_lowerleft_\2",
# r"(?P<obj1>[A-Z]) is there and (?P<obj2>[A-Z]) is at the 10 position of a clock face.": r"\1_lowerleft_\2", # Special case for clock face position.
r"(?P<obj1>[A-Z]) is to the left of (?P<obj2>[A-Z]) and below \2 at approximately a 45 degree angle.": r"\1_lowerleft_\2",
r"(?P<obj1>[A-Z]) is south west of (?P<obj2>[A-Z]).": r"\1_lowerleft_\2",
r"(?P<obj1>[A-Z]) is below and to the left of (?P<obj2>[A-Z]).": r"\1_lowerleft_\2",
r"The objects (?P<obj1>[A-Z]) and (?P<obj2>[A-Z]) are over there. The object \1 is lower and slightly to the left of the object \2.": r"\1_lowerleft_\2",
r"(?P<obj1>[A-Z]) is directly south west of (?P<obj2>[A-Z]).": r"\1_lowerleft_\2",
# r"(?P<obj2>[A-Z]) is positioned below (?P<obj1>[A-Z]) and to the left.": r"\2_lowerleft_\1", # Inverted objects in sentence.
r"(?P<obj1>[A-Z]) is at a 45 degree angle to (?P<obj2>[A-Z]), in the lower lefthand corner.": r"\1_lowerleft_\2",
r"(?P<obj1>[A-Z]) is diagonally below (?P<obj2>[A-Z]) to the left at a 45 degree angle.": r"\1_lowerleft_\2",
r"Object (?P<obj1>[A-Z]) is below object (?P<obj2>[A-Z]) and to the left of it, too.": r"\1_lowerleft_\2",
r"(?P<obj1>[A-Z]) is diagonally to the bottom left of (?P<obj2>[A-Z]).": r"\1_lowerleft_\2",
r"(?P<obj1>[A-Z]) presents lower left to (?P<obj2>[A-Z]).": r"\1_lowerleft_\2",
r"If (?P<obj1>[A-Z]) is the center of a clock face, (?P<obj2>[A-Z]) is located between 7 and 8.": r"\2_lowerleft_\1", # Special case for clock face center.
r"(?P<obj1>[A-Z]) is below (?P<obj2>[A-Z]) and to the left of \2.": r"\1_lowerleft_\2",

# upperright
r"(?P<obj1>[A-Z]) is on the upper right of (?P<obj2>[A-Z]).": r"\1_upperright_\2",
r"(?P<obj1>[A-Z]) is to the top right of (?P<obj2>[A-Z]).": r"\1_upperright_\2",
r"The object (?P<obj1>[A-Z]) is upper and slightly to the right of the object (?P<obj2>[A-Z]).": r"\1_upperright_\2",
r"(?P<obj1>[A-Z]) is on the right side and top of (?P<obj2>[A-Z]).": r"\1_upperright_\2",
r"(?P<obj1>[A-Z]) is positioned in the front right corner of (?P<obj2>[A-Z]).": r"\1_upperright_\2",
r"(?P<obj1>[A-Z]) is upper right to (?P<obj2>[A-Z]).": r"\1_upperright_\2",
r"(?P<obj1>[A-Z]) is to the top-right of (?P<obj2>[A-Z]).": r"\1_upperright_\2",
r"(?P<obj1>[A-Z]) is above (?P<obj2>[A-Z]) at 2 o'clock.": r"\1_upperright_\2",
r"(?P<obj1>[A-Z]) is positioned up and to the right of (?P<obj2>[A-Z]).": r"\1_upperright_\2",
r"The object (?P<obj1>[A-Z]) is positioned above and to the right of the object (?P<obj2>[A-Z]).": r"\1_upperright_\2",
r"(?P<obj1>[A-Z]) is diagonally right and above (?P<obj2>[A-Z]).": r"\1_upperright_\2",
r"(?P<obj1>[A-Z]) is placed at the upper right of (?P<obj2>[A-Z]).": r"\1_upperright_\2",
r"(?P<obj1>[A-Z]) is sitting at the upper right position to (?P<obj2>[A-Z]).": r"\1_upperright_\2",
r"(?P<obj1>[A-Z]) is there and (?P<obj2>[A-Z]) is at the 2 position of a clock face.": r"\2_upperright_\1",
r"(?P<obj1>[A-Z]) is to the right and above (?P<obj2>[A-Z]) at an angle of about 45 degrees.": r"\1_upperright_\2",
r"(?P<obj1>[A-Z]) is north east of (?P<obj2>[A-Z]).": r"\1_upperright_\2",
r"(?P<obj1>[A-Z]) is above and to the right of (?P<obj2>[A-Z]).": r"\1_upperright_\2",
r"The objects (?P<obj1>[A-Z]) and (?P<obj2>[A-Z]) are over there. The object \1 is above and slightly to the right of the object \2.": r"\1_upperright_\2",
r"(?P<obj1>[A-Z]) is directly north east of (?P<obj2>[A-Z]).": r"\1_upperright_\2",
r"(?P<obj1>[A-Z]) is positioned above (?P<obj2>[A-Z]) and to the right.": r"\1_upperright_\2",
r"(?P<obj1>[A-Z]) is at a 45 degree angle to (?P<obj2>[A-Z]), in the upper righthand corner.": r"\1_upperright_\2",
r"(?P<obj1>[A-Z]) is diagonally above (?P<obj2>[A-Z]) to the right at a 45 degree.": r"\1_upperright_\2",
# r"Object (?P<obj2>[A-Z]) is above object (?P<obj1>[A-Z]) and to the right of it, too.": r"\1_upperright_\2", # Object A is above object BB and to the right of it, too.
# r"(?P<obj2>[A-Z]) is diagonally to the upper right of (?P<obj1>[A-Z]).": r"\1_upperright_\2", # AA is diagonally to the upper right of BB.
r"(?P<obj1>[A-Z]) presents upper right to (?P<obj2>[A-Z]).": r"\1_upperright_\2",
r"If (?P<obj1>[A-Z]) is the center of a clock face, (?P<obj2>[A-Z]) is located between 2 and 3.": r"\2_upperright_\1",
r"(?P<obj1>[A-Z]) is above (?P<obj2>[A-Z]) and to the right of \2.": r"\1_upperright_\2",



# lowerright
r"(?P<obj1>[A-Z]) is on the lower right of (?P<obj2>[A-Z]).": r"\1_lowerright_\2",
r"(?P<obj1>[A-Z]) is to the bottom right of (?P<obj2>[A-Z]).": r"\1_lowerright_\2",
r"The object (?P<obj1>[A-Z]) is lower and slightly to the right of the object (?P<obj2>[A-Z]).": r"\1_lowerright_\2",
r"(?P<obj1>[A-Z]) is on the right side and below (?P<obj2>[A-Z]).": r"\1_lowerright_\2",
r"(?P<obj1>[A-Z]) is slightly off center to the top left and (?P<obj2>[A-Z]) is slightly off center to the bottom right.": r"\2_lowerright_\1", # Inverted objects in sentence.
r"(?P<obj1>[A-Z]) is positioned in the lower right corner of (?P<obj2>[A-Z]).": r"\1_lowerright_\2",
r"(?P<obj1>[A-Z]) is lower right of (?P<obj2>[A-Z]).": r"\1_lowerright_\2",
r"(?P<obj1>[A-Z]) is to the bottom-right of (?P<obj2>[A-Z]).": r"\1_lowerright_\2",
r"(?P<obj1>[A-Z]) is below (?P<obj2>[A-Z]) at 4 o'clock.": r"\1_lowerright_\2",
r"(?P<obj1>[A-Z]) is positioned below and to the right of (?P<obj2>[A-Z]).": r"\1_lowerright_\2",
r"The object (?P<obj1>[A-Z]) is positioned below and to the right of the object (?P<obj2>[A-Z]).": r"\1_lowerright_\2",
r"(?P<obj1>[A-Z]) is diagonally right and below (?P<obj2>[A-Z]).": r"\1_lowerright_\2",
r"(?P<obj1>[A-Z]) is placed at the lower right of (?P<obj2>[A-Z]).": r"\1_lowerright_\2",
r"(?P<obj1>[A-Z]) is sitting at the lower right position to (?P<obj2>[A-Z]).": r"\1_lowerright_\2",
r"(?P<obj1>[A-Z]) is there and (?P<obj2>[A-Z]) is at the 5 position of a clock face.": r"\2_lowerright_\1", 
# r"(?P<obj1>[A-Z]) is to the right and above (?P<obj2>[A-Z]) at an angle of about 45 degrees.": r"\1_lowerright_\2", # Inverted objects in sentence.
r"(?P<obj1>[A-Z]) is south east of (?P<obj2>[A-Z]).": r"\1_lowerright_\2",
r"(?P<obj1>[A-Z]) is below and to the right of (?P<obj2>[A-Z]).": r"\1_lowerright_\2",
r"The object (?P<obj1>[A-Z]) and (?P<obj2>[A-Z]) are there. The object \1 is below and slightly to the right of the object \2.": r"\1_lowerright_\2",
r"(?P<obj1>[A-Z]) is directly south east of (?P<obj2>[A-Z]).": r"\1_lowerright_\2",
r"(?P<obj1>[A-Z]) is positioned below (?P<obj2>[A-Z]) and to the right.": r"\1_lowerright_\2",
r"(?P<obj1>[A-Z]) is at a 45 degree angle to (?P<obj2>[A-Z]), in the lower righthand corner.": r"\1_lowerright_\2",
r"(?P<obj1>[A-Z]) is diagonally below (?P<obj2>[A-Z]) to the right at a 45 degree angle.": r"\1_lowerright_\2",
r"Object (?P<obj1>[A-Z]) is below object (?P<obj2>[A-Z]) and to the right of it, too.": r"\1_lowerright_\2",
r"(?P<obj1>[A-Z]) is diagonally to the bottom right of (?P<obj2>[A-Z]).": r"\1_lowerright_\2",
r"(?P<obj1>[A-Z]) presents lower right to (?P<obj2>[A-Z]).": r"\1_lowerright_\2",
r"If (?P<obj1>[A-Z]) is the center of a clock face, (?P<obj2>[A-Z]) is located between 10 and 11.": r"\1_lowerright_\2",
r"(?P<obj1>[A-Z]) is below (?P<obj2>[A-Z]) and to the right of \2.": r"\1_lowerright_\2",


# upperleft
r"(?P<obj1>[A-Z]) is to the upper left of (?P<obj2>[A-Z]).": r"\1_upperleft_\2",
r"The object (?P<obj1>[A-Z]) is upper and slightly to the left of the object (?P<obj2>[A-Z]).": r"\1_upperleft_\2",
r"(?P<obj1>[A-Z]) is on the left side and above (?P<obj2>[A-Z]).": r"\1_upperleft_\2",
r"(?P<obj1>[A-Z]) is slightly off center to the top left and (?P<obj2>[A-Z]) is slightly off center to the bottom right.": r"\1_upperleft_\2",
r"(?P<obj1>[A-Z]) is positioned in the top left corner of (?P<obj2>[A-Z]).": r"\1_upperleft_\2",
r"(?P<obj1>[A-Z]) is upper left of (?P<obj2>[A-Z]).": r"\1_upperleft_\2",
r"(?P<obj1>[A-Z]) is to the top-left of (?P<obj2>[A-Z]).": r"\1_upperleft_\2",
r"(?P<obj1>[A-Z]) is above (?P<obj2>[A-Z]) at 10 o'clock.": r"\1_upperleft_\2",
r"(?P<obj1>[A-Z]) is positioned above and to the left of (?P<obj2>[A-Z]).": r"\1_upperleft_\2",
r"The object (?P<obj1>[A-Z]) is positioned above and to the left of object (?P<obj2>[A-Z]).": r"\1_upperleft_\2",
# r"(?P<obj1>[A-Z]) is diagonally left and above (?P<obj1>[A-Z]).": r"\1_upperleft_\2",  ##BB is diagonally left and above BB.
r"(?P<obj1>[A-Z]) is placed at the upper left of (?P<obj2>[A-Z]).": r"\1_upperleft_\2",
r"(?P<obj1>[A-Z]) is sitting at the upper left position to (?P<obj2>[A-Z]).": r"\1_upperleft_\2",
r"(?P<obj2>[A-Z]) is there and (?P<obj1>[A-Z]) is at the 10 position of a clock face.": r"\1_upperleft_\2",
# r"(?P<obj1>[A-Z]) is to the right and above (?P<obj2>[A-Z]) at an angle of about 45 degrees.": r"\1_upperleft_\2", #BB is to the right and above AA at an angle of about 45 degrees.
r"(?P<obj1>[A-Z]) is north west of (?P<obj2>[A-Z]).": r"\1_upperleft_\2",
r"(?P<obj1>[A-Z]) is above and to the left of (?P<obj2>[A-Z]).": r"\1_upperleft_\2",
r"The object (?P<obj1>[A-Z]) and (?P<obj2>[A-Z]) are there. The object \2 is above and slightly to the left of the object \1.": r"\2_upperleft_\1",
r"(?P<obj1>[A-Z]) is directly north west of (?P<obj2>[A-Z]).": r"\1_upperleft_\2",
r"(?P<obj1>[A-Z]) is positioned above (?P<obj2>[A-Z]) and to the left.": r"\1_upperleft_\2",
r"(?P<obj1>[A-Z]) is at a 45 degree angle to (?P<obj2>[A-Z]), in the upper lefthand corner.": r"\1_upperleft_\2",
r"(?P<obj1>[A-Z]) is diagonally above (?P<obj2>[A-Z]) to the left at a 45 degree angle.": r"\1_upperleft_\2",
r"Object (?P<obj1>[A-Z]) is above object (?P<obj2>[A-Z]) and to the left of it, too.": r"\1_upperleft_\2",
r"(?P<obj1>[A-Z]) is diagonally to the upper left of (?P<obj2>[A-Z]).": r"\1_upperleft_\2",
r"(?P<obj1>[A-Z]) presents upper left to (?P<obj2>[A-Z]).": r"\1_upperleft_\2",
r"If (?P<obj1>[A-Z]) is the center of a clock face, (?P<obj2>[A-Z]) is located between 4 and 5.": r"\1_upperleft_\2",
r"(?P<obj1>[A-Z]) is above (?P<obj2>[A-Z]) and to the left of \2.": r"\1_upperleft_\2",

}

