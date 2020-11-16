# Top View Tree Traversal Algorithm: https://www.youtube.com/watch?v=c3SAvcjWb1E
# or https://www.geeksforgeeks.org/print-nodes-top-view-binary-tree/
def top_view(root):

    if not root:
        return

    result_top_view = {root.data: 0}
    queue = [root]

    while queue:

        node = queue.pop(0)

        if node.left and node.left.data not in result_top_view.keys():
            queue.append(node.left)
            result_top_view[node.left.data] = result_top_view[node.data] - 1

        if node.right and node.right.data not in result_top_view.keys():
            queue.append(node.right)
            result_top_view[node.right.data] = result_top_view[node.data] + 1

    temp = []
    result = []

    for item in sorted(result_top_view, key=result_top_view.get):

        if result_top_view[item] not in temp:
            result.append(item)
            temp.append(result_top_view[item])

    return result
