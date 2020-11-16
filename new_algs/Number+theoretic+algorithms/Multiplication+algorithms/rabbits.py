# Rabbits multiplication algorithm
# The rabbits which were born 5 months ago they all die
# A variation on the Fibonacci's number calculation

def rabbits(n):
    history = [0, 0, 0, 0, 1]  
    for i in range(n-1):
        history.append(history[3] + history[4] - history.pop(0))

    return history[4]
