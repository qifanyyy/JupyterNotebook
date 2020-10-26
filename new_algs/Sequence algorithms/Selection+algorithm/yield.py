"""
@author: David Lei
@since: 23/08/2016
@modified: 

http://stackoverflow.com/questions/231767/what-does-the-yield-keyword-do-in-python

Exploring what the key word yield does

need to understand
    1. iterators
    2. generators
in that order

Iterables
Things that are iterable are things that you can use "for... in...." (strings, lists, files, etc)

Generators
Are iterators, but you can only iterate over them once because they do not store the value in memory
--> generate values on the fly

below example, generator calculate 0 then forgets about it then calculates 1 then 4 one by one

Yield
is a keyword used like return except the function will return a generator
"""

myGenerator = (x*x for x in range(3))
for i in myGenerator:
    print("first try: " + str(i))
    print(myGenerator)

for j in myGenerator:               # wont print anything
    print("second try: " + str(j))

print("Playing with yield")

def createGenerator():
    myList = range(3)
    for i in myList:
        yield i*i

anotherGenerator = createGenerator()
print(anotherGenerator)
for i in anotherGenerator:
    print(i)

"""
above example is kinda useless, but generators are good when you know your function will
return a huge set of values that you will only need to read once

when you call the function, the code you have in the function body doesn't run, the function only return the generator
object

then your code will be run each time the for uses the generator. The first time the for calls the
generator object created in your function, it will run the code in your function from beginning until it hits yeild, then
it will return the first value of the loop, Each other call will run the loop in the function once more and return the
next value until there is no value to return

refer to stack overflow link to learn more.
"""

"""
http://stackoverflow.com/questions/7883962/where-to-use-yield-in-py

yield is best used when you have a function that returns a sequence and you want to iterate over that sequence, but you do not need to have every value in memory at once.

For example, I have a python script that parses a large list of CSV files, and I want to return each line to be processed in another function. I don't want to store the megabytes of data in memory all at once, so I yield each line in a python data structure. So the function to get lines from the file might look something like:

def get_lines(files):
    for f in files:
        for line in f:
            #preprocess line
            yield line
I can then use the same syntax as with lists to access the output of this function:

for line in get_lines(files):
    #process line

but I save a lot of memory usage.

~~~
Instead of using

arr = []
for line in file:
    arr.append(line)

pipe arr somewhere else to iterate over.
better to yield each line as needed
"""