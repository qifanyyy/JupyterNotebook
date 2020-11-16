# A RouteTrie will store our routes and their associated handlers
# import re


class RouteTrie:
    def __init__(self):
        # Initialize the trie with an root node and a handler, this is the root path or home page node
        self.root = RouteTrieNode()

    def insert(self, listpath, handler):
        # Similar to our previous example you will want to recursively add nodes
        # Make sure you assign the handler to only the leaf (deepest) node of this path
        current_node = self.root
        for item in listpath:
            if item not in current_node.before:
                current_node.insert(item)
            current_node = current_node.before[item]
        current_node.handler = handler

    def find(self, listpath):
        # Starting at the root, navigate the Trie to find a match for this path
        # Return the handler for a match, or None for no match
        current_node = self.root
        if listpath[0] is '/':
            return current_node.handler

        for item in listpath:
            if item not in current_node.before:
                return 'not found handler'
            current_node = current_node.before[item]

        return current_node.handler


# A RouteTrieNode will be similar to our autocomplete TrieNode... with one additional element, a handler.
class RouteTrieNode:
    def __init__(self):
        # Initialize the node with children as before, plus a handler

        self.handler = None
        self.before = {}

    def insert(self, item):
        # Insert the node as before
        self.before.update({item : RouteTrieNode()})


# The Router class will wrap the Trie and handle
class Router:
    def __init__(self, root_handler, not_found_handler):
        # Create a new RouteTrie for holding our routes
        # You could also add a handler for 404 page not found responses as well!
        self.newtrie = RouteTrie()
        self.root_handler = root_handler
        self.not_found_handler = not_found_handler

    def add_handler(self, path, handler):
        # Add a handler for a path
        # You will need to split the path and pass the pass parts
        # as a list to the RouteTrie
        listpath = self.split_path(path)
        self.newtrie.insert(listpath, handler)

    def lookup(self, path):
        # lookup path (by parts) and return the associated handler
        # you can return None if it's not found or
        # return the "not found" handler if you added one
        # bonus points if a path works with and without a trailing slash
        # e.g. /about and /about/ both return the /about handler
        if path is '/' or path is '':
            return self.root_handler

        listpath = self.split_path(path)
        # print(listpath)
        return self.newtrie.find(listpath)

    def split_path(self, path):
        # you need to split the path into parts for
        # both the add_handler and loopup functions,
        # so it should be placed in a function here
        str_list = path.split('/')
        if str_list[len(str_list) - 1] != "":
            str_list.append('/')
        else:
            str_list[len(str_list) - 1] = '/'
        str_list = filter(lambda item: item, str_list)
        # print(list(str_list))
        return list(str_list)

# Here are some test cases and expected outputs you can use to test your implementation

# create the router and add a route
router = Router("root handler", "not found handler")  # remove the 'not found handler' if you did not implement this
router.add_handler("/home/about", "about handler")  # add a route

# some lookups with the expected output
print(router.lookup("/"))  # should print 'root handler'
print(router.lookup("/home"))  # should print 'not found handler' or None if you did not implement one
print(router.lookup("/home/about"))  # should print 'about handler'
print(router.lookup("/home/about/"))  # should print 'about handler' or None if you did not handle trailing slashes
print(router.lookup("/home/about/me"))  # should print 'not found handler' or None if you did not implement one

print('************************************')
router = Router("root handler", "not found handler")  # remove the 'not found handler' if you did not implement this
router.add_handler("/blog/posts/", "posts handler")  # add a route

# some lookups with the expected output
print(router.lookup("/"))  # 'root handler'
print(router.lookup(""))  # 'root handler'
print(router.lookup("/blog"))  # 'not found handler'
print(router.lookup("/blog/posts"))  # 'posts handler'
print(router.lookup("/blog/posts/"))  # 'posts handler'
print(router.lookup("/blog/posts/1/"))  # 'not found handler'
print(router.lookup("/blog/posts//1/"))  # 'not found handler'

print('************************************')
router = Router("root handler", "not found handler")  # remove the 'not found handler' if you did not implement this
router.add_handler("", "posts handler")  # add a route

# some lookups with the expected output
print(router.lookup(""))  # 'root handler'
print(router.lookup("/blog"))  # 'not found handler'
print(router.lookup("/blog/posts"))  # 'not found handler'
print(router.lookup("/blog/posts/"))  # 'not found handler'
print(router.lookup("/blog/posts/1/"))  # 'not found handler'

