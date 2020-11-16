from Common import Stack


def revString(my_string):

    # Define a new Stack
    s = Stack()

    # Iterate over the string and push each character to the Stack.
    for char in my_string:
        s.push(char)

    # Declare a string to hold our result.
    result = ""

    # Add the top character in the stack to the string, then pop() until its empty.
    while not s.isEmpty():
        result = result + s.peek()
        s.pop()

    return result


if __name__ == "__main__":
    print("The word hello in reverse is:")
    print(revString("hello"))
