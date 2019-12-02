#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 13:59:33 2019

@author: tommy
"""

import numpy as np
import matplotlib.pyplot as plt
import random
import sys

sys.path.append("..")

from solution_parsing.solution_parser import Schedule


def main():

    np.random.seed(42)
    random.seed(42)

    # Constants
    people = 100
    tracks = 3
    times = 15
    filename = f"preferences-{people}-ppl.txt"
    num_presentations = times * tracks

    # Number the presentations
    presentations = np.arange(1, num_presentations + 1)

    # Create some (latent) groups of presentations. Each person will be assigned to one group,
    # and presentations in that group will have a higher probability.
    # Groups could be e.g. "Java-Programmer", "DevOps person", "Data Scientist" in real life
    presentations_shuffled = list(presentations)
    random.shuffle(presentations_shuffled)

    print(presentations_shuffled)
    group_lengths = [0] + [random.randint(int(times * 0.8), times) for pres in presentations]
    group_lengths = np.cumsum(group_lengths)
    groups = []
    for start, end in zip(group_lengths, group_lengths[1:]):
        if start > len(presentations):
            break

        groups.append(np.array(presentations_shuffled[start:end]))

    for group in groups:
        print(f"Group ({len(group)} presentations): {group}")

    groups_probs = 3 + np.random.rand(len(groups))
    groups_probs = groups_probs / np.sum(groups_probs)
    print(f"groups_probs: {groups_probs}")

    # Populartiy - for plotting
    popularity = np.zeros_like(presentations)

    with open(filename, "w") as file:

        file.write(f"{tracks}, {times}\n")

        # Baseline probabilities for every person
        probs = np.random.rand(num_presentations) * 0.15 + 0.05
        assert np.all((probs <= 1) & ((probs >= 0))), "probs must be in range [0, 1]"

        num_chosen = []
        for person in range(1, people + 1):

            # Choose a latent group which the person belongs to
            latent_group = np.random.choice(np.arange(len(groups)), size=1, p=groups_probs)[0]

            # Update baseline probabilties with group information
            probs_person = probs.copy()
            probs_person[groups[latent_group] - 1] = probs_person[groups[latent_group] - 1] + 0.8
            assert np.all((probs_person <= 1) & ((probs_person >= 0))), "probs must be in range [0, 1]"

            # Sample presentations that the person is interested in
            interested_in = [pres for pres, prob in zip(presentations, probs_person) if random.random() <= prob]
            for presentation in interested_in:
                popularity[presentation - 1] += 1

            print(f"{person}: {repr(interested_in)}", file=file)
            if person < 10:
                print(f"{person}: {repr(interested_in)}")
            num_chosen.append(len(interested_in))

    plt.title("Popularity per presentation")
    plt.bar(presentations, popularity)
    plt.show()

    plt.title("Number of presentations people are interested in")
    plt.hist(num_chosen, bins=50)
    plt.show()

    schedule = Schedule.random_from_preferences(filename)
    schedule.schedule = [set(g) for g in np.array(presentations_shuffled).reshape(tracks, times).T.tolist()]
    assert schedule._is_feasible()
    print(f"Score is at least: {schedule.evaluate_score()}")
    print(schedule)


if __name__ == "__main__":
    main()
