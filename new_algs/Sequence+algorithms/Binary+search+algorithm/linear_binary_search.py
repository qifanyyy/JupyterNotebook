# read the data from the CSV
import csv
import time

with open('netflix2019.csv', mode='r') as f:
    reader = csv.reader(f)
    next(reader)
    titles = [row[1] for row in list(reader)]

# read target titles into a list
with open('target_titles.txt') as f:
    target_titles = [line.strip() for line in f.readlines()]


# linear search algorithm
def linear_lookup(titles, target_title):
    for title in titles:
        if title == target_title:
            return True
    return None


# binary search algorithm modified to return True or False
def binsearch_lookup(sorted_titles, target_title):
    range_start = 0
    range_end = len(sorted_titles) - 1
    while range_start < range_end:
        range_middle = (range_end + range_start) // 2
        title = sorted_titles[range_middle]
        if title == target_title:
            return True
        elif title < target_title:
            range_start = range_middle + 1
        else:
            range_end = range_middle - 1
    if sorted_titles[range_start] != target_title:
        return False
    return True


# titles is the list of all titles available on the CSV
# target_titles contains 5,000 titles that we want to lookup

# linear Search
start = time.time()
for title in target_titles:
    linear_lookup(titles, title)
end = time.time()
time_linear = end - start

# binary search
start = time.time()
sorted_titles = sorted(titles)
for title in sorted_titles:
    binsearch_lookup(title)
end = time.time()
time_binsearch = end - start

print(time_linear)
print(time_binsearch)

# titles is the list of all titles available on the CSV
# target_titles contains 5,000 titles that we want to lookup
