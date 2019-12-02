#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 17:06:39 2019

@author: tommy
"""

import sys
import time
import os

sys.path.append("..")

from solution_parsing.solution_parser import Schedule


filename = os.path.join("..", "problem_generation", "preferences-4000-ppl.txt")
schedule = Schedule.random_from_preferences(filename)
assert schedule._is_feasible()
start_time = time.time()

schedule.schedule = [[None] * schedule.tracks for j in range(schedule.times)]
not_chosen_presentations = list(range(1, schedule.times * schedule.tracks + 1))


track_by_track = True
if track_by_track:
    generator = ((i, j) for i in range(schedule.tracks) for j in range(schedule.times))
else:
    generator = ((i, j) for j in range(schedule.times) for i in range(schedule.tracks))

for (i, j) in generator:

    best_score = 0
    best_presentation = None

    for presentation in not_chosen_presentations:
        schedule.schedule[j][i] = presentation
        score = schedule.evaluate_score()
        if score > best_score:
            best_score = score
            best_presentation = presentation

    print(f"Best found for ({i}, {j}) was {best_presentation} (score: {best_score})")
    schedule.schedule[j][i] = best_presentation
    not_chosen_presentations.remove(best_presentation)

print(schedule)
