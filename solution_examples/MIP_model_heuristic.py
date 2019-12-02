#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 17:06:39 2019

@author: tommy
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 17:06:39 2019

@author: tommy
"""

import sys
import collections
import os

sys.path.append("..")

from solution_parsing.solution_parser import Schedule
from ortools.linear_solver import pywraplp


filename = os.path.join("..", "problem_generation", "preferences-4000-ppl.txt")
schedule = Schedule.random_from_preferences(filename)


solver = pywraplp.Solver("solver", pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
INF = solver.infinity()

objective = 0

# Set up variables x_pj
x = dict()
for p in range(1, schedule.times * schedule.tracks + 1):
    for j in range(schedule.times):
        x[(p, j)] = solver.BoolVar(f"x_{p}_{j}")

        objective += x[(p, j)] / (p * (j + 1))

# Constraint: place each presentation in one time slot
for p in range(1, schedule.times * schedule.tracks + 1):
    solver.Add(sum(x[(p, j)] for j in range(schedule.times)) == 1)

# Constraint: exactly `tracks` presentations per time
for j in range(schedule.times):
    solver.Add(sum(x[(p, j)] for p in range(1, schedule.times * schedule.tracks + 1)) == schedule.tracks)


# Frequencies
frequencies = collections.Counter(p for person_prefs in schedule.preferences for p in person_prefs)

y = solver.NumVar(0, INF, "y")
for j in range(schedule.times):
    solver.Add(y <= sum(frequencies[p] * x[(p, j)] for p in range(1, schedule.times * schedule.tracks + 1)))


solver.Maximize(objective + y)

print(f"Number of variables: {solver.NumVariables()}")
print(f"Number of constraints: {solver.NumConstraints()}")

solver.SetTimeLimit(60 * 1000)
result_status = solver.Solve()

# assert result_status == pywraplp.Solver.OPTIMAL
assert solver.VerifySolution(1e-7, True)

schedule.schedule = [set() for _ in range(schedule.times)]

for p in range(1, schedule.times * schedule.tracks + 1):
    for j in range(schedule.times):
        if x[(p, j)].solution_value() > 0.5:
            schedule.schedule[j].add(p)

# assert solver.Objective().Value() == schedule.evaluate_score()
assert schedule._is_feasible()
print(solver.Objective().Value())
print(schedule.evaluate_score())
