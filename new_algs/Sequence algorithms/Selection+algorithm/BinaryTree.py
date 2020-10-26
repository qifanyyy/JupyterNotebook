'''
    A binary tree is a tree data structure where each node has at most two children
    referred to as left and right children.
    Binary trees are used for efficient searching and sorting.
'''
class BinaryTree:
    '''
        Constructor for the BinaryTree
        :param rootObj The object to define as the root node of the BinaryTree
    '''
    def __init__(self, rootObj):
        self.key = rootObj
        self.leftChild = None
        self.rightChild = None

    '''
        Returns the left child
        :return BinaryTree
    '''
    def getLeftChild(self):
        return self.leftChild

    '''
        Returns the right child
        :return BinaryTree
    '''
    def getRightChild(self):
        return self.rightChild

    '''
        Returns the root object
        :return object
    '''
    def getRootVal(self):
        return self.key

    '''
        Set the root value of the tree
        :param rootObj The object to define as the root node of the BinaryTree
    '''
    def setRootVal(self, rootObj):
        self.key = rootObj

    '''
        Insert a left node in to the tree, if the node is already occupied, move it
        down a level
        :param leftObj The object to insert
    '''
    def insertLeft(self, leftObj):
        # When there is no child, simply add a node
        if self.leftChild == None:
            self.leftChild = BinaryTree(leftObj)
        # If there is a child, we insert our new node, and push the
        # existing node down a level
        else:
            t = BinaryTree(leftObj)
            t.left = self.leftChild
            self.leftChild = t

    '''
        Insert a right node in to the tree, if the node is already occupied, move it
        down a level
        :param leftObj The object to insert
    '''
    def insertRight(self, rightObj):
        if self.rightChild == None:
            self.rightChild = BinaryTree(rightObj)
        else:
            t = BinaryTree(rightObj)
            t.right = self.rightChild
            self.rightChild = t
