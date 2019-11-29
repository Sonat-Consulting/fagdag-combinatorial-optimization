# fagdag-combinatorial-optimization

Today we'll learn about combinatorial optimization problems and how to solve them.

- You will be presented with a real-world optimization problem.
- You will spend time trying to find a good solution to the problem.
- We'll discuss our approaches and talk about theory and solution approaches.

## Problem description

An conference organizer has contacted Sonat to help set up a conference *schedule* that consists of *tracks* and *times*.
For instance, if there are 3 tracks, then for each time (e.g. 10:00 to 10:25) 3 presentations will run simultaneously.
The total number of presentations is equal to the number of *tracks* multiplied by the number of *times*.
For instance, with 3 tracks are 15 times, there are 45 presentations to be scheduled in total.

To see why scheduling matters, consider a person attending the conference.
It would be unfortunate if she is interested in every presentation in a time (e.g. 10:00 to 10:25), but in the next time (e.g. 10:30 to 10:55) there's not a single presentation that is interesting to her.
For her, the conference experience would be better if the schedule was organized so that there was at least one interesting presentation in both times.

The conference organizer would like to create a schedule that *maximizes the sum of each persons happiness* with the schedule.
For each person, a unit of happiness (a point) is given for each time that the person has at least one interesting presentation to attend.
The total happiness of a single person is the number of times when there's at least one interesting presentation scheduled.

The attendees filled out a form where they chose the conferences that they prefer, and the conference organizer has this data.

## Practical information

- There are two instances:
  - Small instance: (3 tracks, 15 times, 100 people).
  - Large instance: (8 tracks, 15 times, 4000 people).
- Solve in whatever language you want. Use any resource you want.
  - A Python solution parser is written for your convenience, and you can build on it if you like.

## Example and input data

### Minimal example

The instance below consists of 2 tracks, 2 times and 4 presentations.
There are only 3 possible schedules, and one of them is optimal.

![](presentation/images/7.png)

### Input data format

The input consists of a file with the following format.

```text
TRACKS, TIMES
PERSON_1 : [PREF1, PREF2, PREF3, ...]
PERSON_2 : [PREF1, PREF2, PREF3, ...]
PERSON_3 : [PREF1, PREF2, PREF3, ...]
...
PERSON_K : [PREF1, PREF2, PREF3, ...]
```

The minimal example above would be represented as:

```text
2, 2
1: [1, 2]
2: [2, 3]
```

### Solution format

The solution must be in the following format:

```text
[{TIME1_PRES1, TIME1_PRES2, ...}, {TIME2_PRES1, TIME2_PRES2, ...}, ...]
```

The optimal solution to the minimal example above would be represented as:

```text
[{1, 3}, {2, 4}]
```
