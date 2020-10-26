"""Tasks scheduler. The goal is to minimize the weighted sum of completion times.
We can achieve this by ordering tasks by their ratios (weight / length)."""

import operator

# [job_weight, job_length]
jobs = [[3, 6], [54, 2], [1, 500], [1000, 1], [3, 555], [27, 1111], [2, 1000]]


def schedule(tasks, alg=None):
    """Takes list of tasks (weight, length). Algorithm 'diff' or 'ratio'
    can be passed to determine the way of task comparison"""

    # Defines operator dynamically. Subtraction when algorithm
    # is based on weight and length difference, otherwise division is used
    # what reflects scheduling by ratio (optimal).
    operation = operator.sub if alg == 'diff' else operator.truediv

    # schedules jobs in decreasing order of the difference (weight - length)
    # or ratio (weight / length)
    tasks = sorted(tasks, key=lambda x: operation(x[0], x[1]), reverse=True)

    # handle ties so that bigger weights go first.
    difference = operation(tasks[0][0], tasks[0][1])
    temp = []
    for idx, i in enumerate(tasks):
        diff = operation(i[0], i[1])
        if diff == difference:
            temp.append(i)
        else:
            difference = diff
            if len(temp) > 1:
                temp.sort(reverse=True)
                tasks[idx - len(temp):idx] = temp
            temp = [i]

    if len(temp) > 1:
        temp.sort(reverse=True)
        tasks[len(tasks) - len(temp):len(tasks)] = temp

    return tasks


def weighted_completion_time(scheduled):
    comp_time = 0
    weighted_comp_time = 0
    for i in scheduled:
        comp_time += i[1]
        weighted_comp_time += i[0] * comp_time

    return weighted_comp_time


if __name__ == "__main__":
    ordered = schedule(jobs)
    print(ordered)
    print("Before scheduling:", weighted_completion_time(jobs))
    print("After scheduling:", weighted_completion_time(ordered))
