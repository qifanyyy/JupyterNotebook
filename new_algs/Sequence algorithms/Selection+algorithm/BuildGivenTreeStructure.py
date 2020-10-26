# Below is an implementation of the following tree:

#                   a
#               /       \
#           b               c
#            \             / \
#             d           e   f


from Common import BinaryTree


def buildTree():

    #   Create a new tree and set the root value to a.
    b = BinaryTree('a')
    print(b.getRootVal() + " is the root value of the tree")

    #   Starting from the left, inset b.
    b.insertLeft('b')
    print(b.getLeftChild().getRootVal() + " is a's left child")

    #   Next set b's right child to be d.
    b.getLeftChild().insertRight('d')
    print(b.getLeftChild().getRightChild().getRootVal() + " is b's right child")

    #   Next go back to the root a and set its right child to c.
    b.insertRight('c')
    print(b.getRightChild().getRootVal() + " is a's right child")

    # Next set c's left child to e
    b.getRightChild().insertLeft('e')
    print(b.getRightChild().getLeftChild().getRootVal() + " is c's left child")

    # Finally set c's right child to f
    b.getRightChild().insertRight('f')
    print(b.getRightChild().getRightChild().getRootVal() + " is c's right child")


if __name__ == "__main__":
    buildTree()