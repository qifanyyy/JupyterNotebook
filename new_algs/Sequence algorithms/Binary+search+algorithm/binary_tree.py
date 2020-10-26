from tree_node import TreeNode


class BinarySearchTree:

    def __init__(self):
        self.root = None

    def insert(self, parent, left=None, right=None):

        if not self.root:
            self.root = TreeNode(parent)
            node = self.root
        else:
            node = self.bfs(parent)

        if node:
            node.left = TreeNode(left) if left else None
            node.right = TreeNode(right) if right else None
        else:
            raise LookupError("There is no such parent")

    # Search and return parent node (if exists; if not - return None)
    def bfs(self, parent):

        if not self.root:
            return

        queue = [self.root]

        while queue:

            node = queue.pop(0)

            if node.data == parent:
                return node

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        return None
