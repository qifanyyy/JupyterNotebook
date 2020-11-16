"""
@author: David Lei
@since: 21/10/2017

http://www.geeksforgeeks.org/convert-ternary-expression-binary-tree/

Given a string containing ternary expressions 'condition ? if_true: if_false' which may be nested
convert the expression into a binary tree.

Sample input 2:

a?b?c:d:e

The root is a, it's first child is b, and it's right child is e.
b has two children c and d.

So since my input is always a ternary expression which is composed of 3 components we must always have a left, root, right triplet to work with.

If we have something like a?b?c:d:e?q:r then I assume we would result in a tree like

            a
          /  \
        b     e   
      /  \    / \
     c    d   q   r

So there looks like there is an element of recursion and joining pointers.

My first thought is I can push everything onto a stack until I encounter a `a:b' pair, then I can process that triplet as it's root is the last item on the 
stack after the 'a:b' pair resulting in a subtree st.

 a? st :e?q:r

repeating this process I can do it for e?q:r resulting in a? st: st at which I can complete the tree.

"""

class Node:
    def __init__(self, char):
        self.char = char
        self.left = None
        self.right = None

def ternary_to_binary_tree_aux(string):
    stack = []
    ternary_to_binary_tree(string, 0, stack)  # Python is pass by reference so will mutate stack.
    while len(stack) >= 3:
        # Should be able to pop 3 items off as ternary expressions will come in three.
        right = stack.pop()
        left = stack.pop()
        root = stack.pop()
        root.left = left
        root.right = right
        stack.append(root)
    # Should only have 1 item left in the stack.
    print("items left in stack: " + str(len(stack)))
    return stack[0]

# Sample input 1:
# indexes: 01234
# string:  a?b:c
# i = 4

# Sample input 2:
# indexes: 012345678
# string:  a?b?c:d:e
# i = 8 (base case)
# stack = [(a), (b: c-b-d), (e)], base case join all and return (a).

# Made up input 1:
# indexes: 0 1 2 3 4 5 6 7 8 9 10 11 12
# string:  a ? b ? c : d : e ? q  :  r
# i = 12
# stack = [(a), (b: c-b-d), (e: q-e-r)] 

def ternary_to_binary_tree(string, i, stack):  # O(n/2 + 1) = O(n) as recursive calls bounded by n/2 as we skip over the ':' and '?' chars.    # Base case, end of the string.
    print('called')
    if i >= len(string) - 1:  # Last element in the string.
        right_child = Node(string[i])
        left_child = stack.pop()
        root = stack.pop()
        root.left = left_child
        root.right = right_child
        stack.append(root)
        return
    # Index won't be out of bounds of len(string) -1.
    # i += 2 to skip the '?' and ':'.
    if string[i + 1] == "?":  # Handle root.
        new_root = Node(string[i])
        stack.append(new_root)
        i += 2
    elif string[i - 1] == "?":  # Handle left child.
        new_left_child = Node(string[i])
        stack.append(new_left_child)
        i += 2
    else:
        # Will be another expression after this, need to join subtree here.
        new_right_child = Node(string[i])
        left_child = stack.pop()
        root = stack.pop()
        root.left = left_child
        root.right = new_right_child
        stack.append(root)
        i += 2
    return ternary_to_binary_tree(string, i, stack)

def in_order_print(root): # O(n) where n is the number of nodes in the tree.
    if root.left:
        in_order_print(root.left)
    print(root.char, end="")
    if root.right:
        in_order_print(root.right)

if __name__ == "__main__":
    # Sample input 1.
    sample_1 = "a?b:c"
    print("\nSample 1: %s" % sample_1)
    root = ternary_to_binary_tree_aux(sample_1)
    print("In order traversal")
    in_order_print(root)
    print()

    # Sample input 2.
    sample_2 = "a?b?c:d:e"
    print("\nSample 2: %s" % sample_2)
    root = ternary_to_binary_tree_aux(sample_2)
    print("In order traversal")
    in_order_print(root)
    print()

    # Made up input 1.  
    made_up_1 = "a?b?c:d:e?q:r"
    print("\nMade up 1: %s" % made_up_1)
    root = ternary_to_binary_tree_aux(made_up_1)
    print("In order traversal")
    in_order_print(root)
    print()



