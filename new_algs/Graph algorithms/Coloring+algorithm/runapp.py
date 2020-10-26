from edge_coloring import do_edge_coloring
from vertex_coloring import do_vertex_coloring

input_path1 = 'test_cases/vertex/networkC.csv'  # necessary for both edge coloring and vertex coloring. for vertex
# coloring, put the address of graph in input_path1 and put the output of vertex coloring in java code ( result
# containing colors ) in input_path2. for edge coloring , put the output of edge coloring of java code in input_path1

# input_path1 = 'test_cases/edge/k3.csv'

input_path2 = 'test_cases/vertex/networkC_out.csv'  # necessary only for vertex coloring. put the output of vertex
# coloring in java code ( result containing colors ) in input_path2.

temp = int(input("Enter 0 for vertex coloring and 1 for edge coloring:"))
if temp == 0:
    input_path1 = input("Enter path of input-graph:")
    input_path2 = input("Enter output path of vertex coloring of graph entered in previous request:")
    do_vertex_coloring(input_path1, input_path2)
elif temp == 1:
    input_path1 = input("Enter output path of edge coloring:")
    do_edge_coloring(input_path1)
else:
    print("Illegal number entered.")
