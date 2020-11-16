import math
import binarytree as binarynode
import subprocess
import sys
# AUTHOR: Luis Enrique Neri Pérez
# Copyright 2019

# This is an algorithm that draws a binary tree

levels = 1

class BinaryNode:

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def hasLNode(self):
        return self.left!=None

    def hasRNode(self):
        return self.right!=None

    def addNode(self, value):

        if(value < self.value):

            if(self.hasLNode()):
                self.left.addNode(value)
            else:
                self.left = BinaryNode(value)

        elif(value > self.value):

            if (self.hasRNode()):
                self.right.addNode(value)
            else:
                self.right = BinaryNode(value)


    def print(self):
        current_level = [self]
        tree = list()
        global levels
        space = levels
        while current_level and space >= 1:
            for node in current_level:
                tree.append(node.value)

            next_level = list()
            for n in current_level:
                if n.left:
                    next_level.append(n.left)
                else:
                    next_level.append(BinaryNode(0))
                if n.right:
                    next_level.append(n.right)
                else:
                    next_level.append(BinaryNode(0))
                current_level = next_level
            space -= 1

        arbolInter = []
        for elemento in tree:
            if elemento == 0:
                arbolInter.append(None)
            else:
                arbolInter.append(elemento)

        tree = arbolInter
        root = binarynode.build(tree)
        print(root)

def TreeCreator(list):
    node = BinaryNode(list[0])
    for i in range(1,len(list)):
        node.addNode(list[i])

    node.print()


def install():
    if 'binarytree' not in sys.modules:
        subprocess.call([sys.executable, "-m", "pip", "install", 'binarytree'])

def main():
    install()
    print("Example:   11, 6, 8, 19, 4, 10, 5, 17, 43, 49, 31\n")
    lista = input("Write down the list of nodes to draw the Binary Tree:")
    nodos = lista.split(',')

    for i in range(0,len(nodos)):
        nodos[i] = int(nodos[i])

    global levels

    levels = int(math.ceil(math.log(len(nodos)+1)/math.log(2)))
    TreeCreator(nodos)

lista = [11, 6, 8, 19, 4, 10, 5, 17, 43, 49, 31]

main()

