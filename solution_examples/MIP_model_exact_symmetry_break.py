#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 17:06:39 2019

@author: tommy
"""

import sys
import os

sys.path.append("..")

from solution_parsing.solution_parser import Schedule
from ortools.linear_solver import pywraplp


filename = os.path.join("..", "problem_generation", "preferences-100-ppl.txt")
schedule = Schedule.random_from_preferences(filename)


solver = pywraplp.Solver("solver", pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
INF = solver.infinity()


objective = 0


# Set up variables x_pj
x = dict()
for p in range(1, schedule.times * schedule.tracks + 1):
    for j in range(schedule.times):
        for i in range(schedule.tracks):
            x[(p, i, j)] = solver.BoolVar(f"x_{p}_{i}_{j}")
            objective += x[(p, i, j)]

# Constraint: place each presentation in one time slot
for p in range(1, schedule.times * schedule.tracks + 1):
    solver.Add(sum(x[(p, i, j)] for j in range(schedule.times) for i in range(schedule.tracks)) == 1)

# Constraint: exactly `tracks` presentations per time
for j in range(schedule.times):
    for i in range(schedule.tracks):
        solver.Add(sum(x[(p, i, j)] for p in range(1, schedule.times * schedule.tracks + 1)) == 1)

# Symmetry breaking constraints
for j in range(schedule.times - 1):
    left = sum(x[(p, 0, j)] * p for p in range(1, schedule.times * schedule.tracks + 1))
    right = sum(x[(p, 0, j + 1)] * p for p in range(1, schedule.times * schedule.tracks + 1))
    solver.Add(left <= right)

for j in range(schedule.times):
    for i in range(schedule.tracks - 1):
        top = sum(x[(p, i, j)] * p for p in range(1, schedule.times * schedule.tracks + 1))
        bottom = sum(x[(p, i + 1, j)] * p for p in range(1, schedule.times * schedule.tracks + 1))
        solver.Add(top <= bottom)


# Objective function and constraints
y = dict()

for k, preferences in enumerate(schedule.preferences[1:]):
    for j in range(schedule.times):
        # When this was boolean the code was too slow, but if it's a real number its fast enough
        y[(k, j)] = solver.NumVar(0, 1, f"y_{k}_{j}")
        solver.Add(
            y[(k, j)]
            <= sum(
                x[(p, i, j)]
                for i in range(schedule.tracks)
                for p in range(1, schedule.times * schedule.tracks + 1)
                if p in preferences
            )
        )
        objective += y[(k, j)]


solver.Maximize(objective)

print(f"Number of variables: {solver.NumVariables()}")
print(f"Number of constraints: {solver.NumConstraints()}")

solver.SetTimeLimit(60 * 1000 * 1)


result_status = solver.Solve()

# assert result_status == pywraplp.Solver.OPTIMAL
assert solver.VerifySolution(1e-7, True)

print(solver.Objective().Value())

schedule.schedule = [set() for _ in range(schedule.times)]

for i in range(schedule.tracks):
    for j in range(schedule.times):
        for p in range(1, schedule.times * schedule.tracks + 1):
            if x[(p, i, j)].solution_value() > 0.5:
                schedule.schedule[j].add(p)
                print(str(p).ljust(3), end=" ")
    print()

# assert solver.Objective().Value() == schedule.evaluate_score()
assert schedule._is_feasible()
print(schedule.evaluate_score())
print(schedule)

print(f"Ran in {solver.wall_time() / 1000}")
