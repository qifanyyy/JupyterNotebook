"""
@author: David Lei
@since: 7/11/2017

https://www.hackerrank.com/challenges/minimum-average-waiting-time/problem

1. Sort input by arrival time.
2. Use min heap to keep track of people in the shop, sort by cook time so you can minimize the waiting time.

This makes sense as we can only process the people in the shop.
Out of everyone in the shop we want to reduce the time they all wait as much as possible
so sorting the min heap by cook time makes sense.

This approach was outlined in the forums: https://www.hackerrank.com/challenges/minimum-average-waiting-time/forum
It makes sense but I need to spend some time to figure out how to come up with it during an interview.
TODO: Spend some time thinking about formulating such a solution.

Passes :)
"""
from collections import deque
import heapq

customers = int(input())

jobs = []

for _ in range(customers):
    arrival_time, cook_time = [int(x) for x in input().split()]
    jobs.append((arrival_time, cook_time))

jobs.sort(key=lambda t:t[0])
jobs = deque(jobs)

time = 0
waiting_time = 0
min_heap = []

while jobs or min_heap:

    while jobs and jobs[0][0] <= time:
        # A customer comes to shop, at this time, add their job to the pq.
        job = jobs.popleft()
        heapq.heappush(min_heap, (job[1], job))
    if min_heap:
        # Process the jobs we have to serve.
        shortest_task = heapq.heappop(min_heap)
        time += shortest_task[1][1]
        waiting_time += time - shortest_task[1][0]
    else:
        # No tasks to do.
        # Add a task directly from the jobs and make the current time the arrival time.
        if jobs:
            # Need this otherwise TLE.
            job = jobs.popleft()
            time = job[0] # Arrival time.
            heapq.heappush(min_heap, (job[1], job))

print(waiting_time // customers)


