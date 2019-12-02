#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 17:06:39 2019

@author: tommy
"""

import sys

import statistics
import numpy as np
import os

sys.path.append("..")

from solution_parsing.solution_parser import Schedule

# Read the schedule
filename = os.path.join("..", "problem_generation", "preferences-100-ppl.txt")
schedule = Schedule.random_from_preferences(filename)
assert schedule._is_feasible()

old_score = schedule.evaluate_score()

all_scores = [old_score]

for i in range(100):

    possible_new = Schedule.random_from_preferences(filename, random_seed=i)
    new_score = possible_new.evaluate_score()
    all_scores.append(new_score)

    if new_score > old_score:
        old_score = new_score
        print(f"Best solution found has score: {new_score}")

print(f"Mean: {int(statistics.mean(all_scores))}")
