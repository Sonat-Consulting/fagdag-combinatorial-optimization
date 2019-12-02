#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 17:06:39 2019

@author: tommy
"""

import sys
import itertools
import random
import time
import numpy as np
import os

sys.path.append("..")

random.seed(123)
np.random.seed(123)

from solution_parsing.solution_parser import Schedule


def swap_one(list_one, list_two):
    """A heuristics that swaps two elements from two lists."""
    i = random.choice(list_one)
    j = random.choice(list_two)

    list_one.remove(i)
    list_two.remove(j)

    list_one.append(j)
    list_two.append(i)


# Read the schedule
filename = os.path.join("..", "problem_generation", "preferences-4000-ppl.txt")
schedule = Schedule.random_from_preferences(filename)
assert schedule._is_feasible()

# Keep track of time
start_time = time.time()

to_plot = []

for iteration in itertools.count(1):

    # Create a list for indexing when swapping
    schedule_list = [list(p) for p in schedule.schedule]

    # Higher probability of chosing tracks with low scores
    if (iteration == 1) or iteration % 10 == 0:
        p = 1 / (1 + np.array(schedule.scores_by_time()))
        p = p / np.sum(p)

    # Choose indices based on scores (lower scores => higher probabilities)
    i, j = np.random.choice(list(range(len(schedule.schedule))), 2, replace=False, p=p)
    swap_one(schedule_list[i], schedule_list[j])

    # Make a copy and evaluate the objective function on the swapped list
    possible_schedule = schedule.copy()
    possible_schedule.schedule = [set(p) for p in schedule_list]
    assert possible_schedule._is_feasible()

    time_so_far = time.time() - start_time
    score = possible_schedule.evaluate_score()
    prob = np.exp(-iteration / 25)

    # If the score is better or a drawn number is likely enough => update schedule
    if score > schedule.evaluate_score() or (random.random() < prob):
        print(f"Iteration: {iteration}. Time: {round(time_so_far, 1)}: Score: {score} (prob: {round(prob, 2)})")
        schedule = possible_schedule

        to_plot.append((iteration, score, prob))

    if time_so_far > 60 * 3:
        break

print(schedule)

# %%
import matplotlib.pyplot as plt

plt.title("Simulated annealing")
plt.plot([i for (i, s, p) in to_plot], [s for (i, s, p) in to_plot], label="Score")
# plt.plot([i for (i, s, p) in to_plot], [p * max([s for (i, s, p) in to_plot]) for (i, s, p) in to_plot], label="Probability")
plt.legend()
plt.xlabel("Scores")
plt.xlabel("Iterations")
plt.grid(True, alpha=0.75)

plt.savefig("simulated_annealing.pdf")
plt.show()
