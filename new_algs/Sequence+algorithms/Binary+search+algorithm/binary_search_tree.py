#Author: Denis Karanja, P15/55431/2012
#Institution: The University of Nairobi, Kenya,
#Department: School of Computing and nodeInformatics,
#Email: dee.caranja@gmail.com,
#Task: Binary search tree inorder, preorder and postorder traversal in Python
#License type: MIT :)

class Node:
	#constructor--a little house keeping :)
	def __init__(self, nodeInfo):
		self.nodeInfo = nodeInfo
		self.left = None
		self.right = None

	#return as astring
	def __str__(self):
		return str(self.nodeInfo)


class BinarySearchTree:
	#constructor 
	def __init__(self):
		self.root = None

	#createTree binary tree nodes
	def createTree(self, value):
		if self.root == None:
			self.root = Node(value)
		else:
			now_node = self.root

			while True:
				#check if value is less than the current root node
				if value < now_node.nodeInfo:
					if now_node.left:
						now_node = now_node.left
					else:
						now_node.left = Node(value)
						break
				elif value > now_node.nodeInfo:
					if now_node.right:
						now_node = now_node.right
					else:
						now_node.right = Node(value)
						break

				else:
					break

	#Traversal methods
	def traverseInorder(self, node):
		if node is not None:
			self.traverseInorder(node.left)
			print (node.nodeInfo)
			self.traverseInorder(node.right)

	def traversePostorder(self, node):
		if node is not None:
			self.traversePostorder(node.left)
			self.traversePostorder(node.right)
			print (node.nodeInfo)


	def traversePreorder(self, node):
		if node is not None:
			print (node.nodeInfo)
			self.traversePreorder(node.left)
			self.traversePreorder(node.right)




tree = BinarySearchTree()

numbers = [8, 3, 2, 1, 6, 7, 9, 4, 25, 65, 23]

for number in numbers:
	tree.createTree(number)

print ("In-order traversal...\n")
tree.traverseInorder(tree.root)

print ("\nPre-Order traversal...\n")
tree.traversePreorder(tree.root)

print ("\nPost-Order traversal...\n")
tree.traversePostorder(tree.root)




