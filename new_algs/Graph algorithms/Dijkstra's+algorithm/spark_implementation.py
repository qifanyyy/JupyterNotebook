def transformer(x):
    """
    This function will be used inside of one of our maps. We use this instead of a lambda because the
    output is relatively complex (three possible outcomes, instead of the usual two with an if ... else structure).
    We loop over each arc:
        - If the source vertex is 1 (starting vertex) and the destination is the vertex defined in our search: we remove the first node in the key.
        - If the source vertex is the vertex defined in our search: we remove the second node in the key.
        - Otherwise, we make no change.
        
    The aim is to get a common key between the vertex searched and its antecedent. 
    """
    if x[0].split(',')[0] == '1' and x[0].split(',')[1] == vertex: # If the source vertex is 1 and the destination is the vertex searched
        return(x[0].split(',')[1], x[1])  
    elif x[0].split(',')[0] == vertex: # If the source vertex is the vertex we search
        return((x[0].split(',')[0], (x[1][0] + distance, path + ',' + x[1][1].split(',')[-1]))) 
    else: 
        return(x[0], (x[1][0], x[1][1])) # No transformation

# Get the initial document
document = sc.textFile("hdfs:///user/hadoop/wc/input/sparse_matrix.txt")
document = document.map(lambda x: x.split(";"))
# Transform the document to get the following output:
# (node1, node2, distance, node1, node2) (the last two elements are here to keep track of the path)
matrix = document.map(lambda x: (x[0] + ',' + x[1], (int(x[2]), x[0] + ',' + x[1])))
# Keep track of the last distance in the algorithm, along with the current vertex and corresponding path
vertex = '1'
distance = 0
path = '1'
length = matrix.filter(lambda x: x[0].split(',')[0] == '1').count()
while matrix.count() > length:
    # Weird transformation
    trans_matrix = matrix.map(lambda x: transformer(x))
    # Retrieve the proper key
    map_matrix = trans_matrix.map(lambda x: (x[0], x[1]) if len(x[0].split(',')) > 1 else ('1,' + x[1][1].split(',')[-1], x[1]))
    # Merge everything
    reduce_matrix = map_matrix.reduceByKey(lambda x, y: (x[0], x[1]) if x[0] < y[0] else (y[0], y[1]))
    # Update the current node
    current_node = reduce_matrix.filter(lambda x: x[0].split(',')[0] == '1').filter(lambda x: x[1][0] > distance).sortBy(lambda x: x[1][0]).first()
    vertex = current_node[0].split(',')[-1]
    distance = current_node[1][0]
    path = current_node[1][1]
    matrix = reduce_matrix
