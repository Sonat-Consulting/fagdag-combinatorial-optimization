#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 14:25:36 2019

@author: tommy
"""

import functools
import random
import copy


class Schedule:
    """Representation, scoring and I/O with schedules (a list of sets)."""

    def __init__(self, schedule):
        """Initialize an instance of a schedule.
        
        Examples
        --------
        >>> # Initialize a schedule with 3 tracks, 2 time segments and 6 presentations
        >>> Schedule([{1, 2, 3}, {4, 5, 6}])
        """
        self.schedule = schedule

    def _is_feasible(self):
        """Verify that the schedule is feasible."""

        # Every set must be of equal length
        equal_length = all(len(s) == len(self.schedule[0]) for s in self.schedule)

        # No duplicates are allowed
        num_presentations = sum(len(s) for s in self.schedule)
        unique_presentations = len(functools.reduce(set.union, self.schedule))
        no_duplicates = num_presentations == unique_presentations

        # The schedule must contain numbers from 1 to `num_presentations`
        presentations = [int(pres) for group in self.schedule for pres in group]
        contains_all = set(range(1, max(presentations) + 1)) == set(presentations)

        return equal_length and no_duplicates and contains_all

    def write_to_file(self, filename):
        """Write the schedule to a file."""
        assert self._is_feasible()
        with open(filename, "w") as file:
            file.write(repr(self.schedule))

    @classmethod
    def read_from_file(cls, filename):
        """Read the schedule from a file.
        
        The format must be:
            
            [{TIME1_PRES1, TIME1_PRES2, ...}, {TIME2_PRES1, TIME2_PRES2, ...}, ...]
            
        """
        with open(filename, "r") as file:
            new_instance = cls(eval(file.read()))
            return new_instance

    def load_preferences(self, filename):
        """Load preferences from a file.
        
        The format must be:
            
            TRACKS, TIMES
            PERSON_1 : [PREF1, PREF2, PREF3, ...]
            PERSON_2 : [PREF1, PREF2, PREF3, ...]
            PERSON_3 : [PREF1, PREF2, PREF3, ...]
            ...
            PERSON_K : [PREF1, PREF2, PREF3, ...]
            
        """
        self.preferences = []
        with open(filename, "r") as file:
            for i, line in enumerate(file):

                # Special handling of first line
                if i == 0:
                    self.tracks, self.times = line.strip("\n").split(",")
                    self.tracks, self.times = int(self.tracks), int(self.times)
                else:
                    person, prefs = line.strip("\n").split(":")
                    self.preferences.append(set(eval(prefs)))

    def scores_by_time(self):
        """Return a list of the objective function score per time."""
        if not hasattr(self, "preferences"):
            raise AttributeError("Run `load_preferences` before scoring.")
        score = [0 for _ in self.schedule]

        # Loop over ever persons preferences
        for person_preferences in self.preferences:
            for j, time_segment in enumerate(self.schedule):
                time_segment = set(time_segment)

                # If at least one presentation is interesting, the score is incraesed
                if len(time_segment.intersection(person_preferences)) > 0:
                    score[j] += 1

        return score

    def evaluate_score(self):
        """Evaluate the objective function score."""
        # Get the score for each time and sum over times to obtain the score
        return sum(self.scores_by_time())

    def copy(self):
        """Copy the object."""
        new_instance = type(self)(copy.deepcopy(self.schedule))
        new_instance.preferences = copy.deepcopy(self.preferences)
        return new_instance

    def __repr__(self):
        return type(self).__name__ + "(" + repr(self.schedule) + ")"

    def __eq__(self, other):
        return self.schedule == other.schedule

    @classmethod
    def random_from_preferences(cls, filename, random_seed=123):
        """Create a random schedule from preferences."""

        # Create a new instance and load the preferences
        new_instance = cls([])
        new_instance.load_preferences(filename)

        # Create a list of presentations
        num_presentations = new_instance.tracks * new_instance.times
        schedule = list(range(1, num_presentations + 1))

        # Shuffle the list (but seed random generator)
        random.Random(x=random_seed).shuffle(schedule)

        # Set the random schedule and return the instance
        schedule = [
            set(schedule[i * new_instance.tracks : (i + 1) * new_instance.tracks]) for i in range(new_instance.times)
        ]
        new_instance.schedule = schedule
        return new_instance

    def pprint(self):
        """Put into a canonical (sorted) form and print the schedule with scores."""
        prefs = [list(time) for time in self.schedule]

        # Sort within each time slot
        prefs = [list(sorted(time)) for time in self.schedule]

        # Sort the time tracks
        prefs = sorted(prefs, key=lambda t: min(t))

        print(*(f"Time {j+1}".rjust(8) for j in range(len(prefs))))
        for i in range(len(prefs[0])):
            for j in range(len(prefs)):
                print(str(prefs[j][i]).rjust(8), end=" ")
            print("\n", end="")

        print(*["-" * 8 for s in self.scores_by_time()])
        print(*[str(s).rjust(8) for s in self.scores_by_time()])


if __name__ == "__main__":

    # =============================================================================
    #     HOW TO USE THE CLASS
    # =============================================================================

    import os

    # Create a schedule manually
    schedule = Schedule(schedule=[{1, 2, 3}, {4, 5, 6}, {7, 8, 9}, {10, 11, 12}])

    # Create a random schedule from preferences
    filename = os.path.join("..", "problem_generation", "preferences-100-ppl.txt")
    schedule = Schedule.random_from_preferences(filename)
    print(f"The score is {schedule.evaluate_score()}")

    # Write it to a file
    schedule.write_to_file("schedule.txt")

    # The instance created with `read_from_file` is the same as the written one
    assert schedule == Schedule.read_from_file("schedule.txt")

    # Simple printing
    print(schedule)

    # Pretty printing
    # schedule.pprint()

    # =============================================================================
    #     AN ALGORITHM THAT TRIES 10 DIFFERENT RANDOM SCHEDULES
    # =============================================================================
    print("An algorithm that tries 10 different random schedules")

    best_score = 0
    best_schedule = Schedule.random_from_preferences(filename)

    for i in range(10):

        # Create a new random schedule
        schedule = Schedule.random_from_preferences(filename, random_seed=i)

        if schedule.evaluate_score() > best_score:
            best_score = schedule.evaluate_score()
            print(f"The best score so far is {schedule.evaluate_score()}")
            # print(f"Achieved with: {schedule}\n")
