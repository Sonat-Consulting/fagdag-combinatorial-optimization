#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 17:06:39 2019

@author: tommy
"""

import sys
import time
import random
import itertools
import os
from scipy import special

sys.path.append("..")

from solution_parsing.solution_parser import Schedule


filename = os.path.join("..", "problem_generation", "preferences-100-ppl.txt")
schedule = Schedule.random_from_preferences(filename)
assert schedule._is_feasible()
start_time = time.time()

schedule.schedule = [[None] * schedule.tracks for j in range(schedule.times)]
not_chosen_presentations = list(range(1, schedule.times * schedule.tracks + 1))

for j in range(schedule.times):

    # Choose a first presentation, any will do
    choice = random.choice(not_chosen_presentations)
    # not_chosen_presentations.remove(choice)

    best_score = 0
    best_schedule = None

    print(f"Number of combinations: {special.comb(len(not_chosen_presentations), schedule.tracks-1)}")

    combinations = enumerate(itertools.combinations(not_chosen_presentations, r=schedule.tracks - 1))

    for i, combination in combinations:

        schedule_proposed = set([choice] + list(combination))
        new_schedule = schedule.copy()
        new_schedule.schedule = [schedule_proposed]
        score = new_schedule.evaluate_score()
        if score > best_score:
            best_score = score
            best_schedule = schedule_proposed

    print(f"For track {j} the best combination is {best_schedule}")
    schedule.schedule[j] = best_schedule
    score = schedule.evaluate_score()

    print(f"Score: {score}")

    for chosen in best_schedule:
        not_chosen_presentations.remove(chosen)

    print(schedule)

print(schedule)
assert schedule._is_feasible()
print(f"Score: {schedule.evaluate_score()}")
