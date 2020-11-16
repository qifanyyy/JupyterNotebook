import argparse
import time
import hungarian
import brute_force

#TODO args for solver selection and data path
parser = argparse.ArgumentParser(description='main program to test hungarian and baseline on people-bike matching problem')
parser.add_argument('--data_file', type=str, help='path to the data file')
parser.add_argument('--method', type=str, nargs='?', const="hungarian", help='method to use')
args = parser.parse_args()

# distance measure
def cal_dist(p,b):
    return abs(p[0]-b[0])+abs(p[1]-b[1])

# fetch data
data=[list(map(int,line.strip().split(" "))) for line in open(args.data_file).readlines() if (line.startswith("#")==False and len(line)>0)]

# visualization
m,n=data[0]
people=data[1:m+1]
bikes=data[m+1:]
max_x=max([d[0] for d in data[1:]])
max_y=max([d[1] for d in data[1:]])

vis=[["O" for _ in range(max_y+1)] for __ in range(max_x+1)]
dist_mat=[[0 for _ in range(n)] for __ in range(m)]

for p in people:
    vis[p[0]][p[1]]="P"
for b in bikes:
    vis[b[0]][b[1]]="B"

for p_i, p in enumerate(people):
    for b_i, b in enumerate(bikes):
        dist_mat[p_i][b_i]=cal_dist(p,b)

print("MAP:")
print("."+"-"*len(vis[0])+">(y)")
[print("|"+"".join(line)) for line in vis]
print("v(x)\n")

print("DIST:")
[print(" ".join(["%2d"%(x) for x in line])) for line in dist_mat]
print()

print("SOLUTION:")
# algorithm (metrics, {(p_i, b_i)})
t0=time.time()
if args.method=="hungarian":
    solution = hungarian.solve(dist_mat, people, bikes)
elif args.method=="brute_force":
    solution = brute_force.solve(dist_mat, people, bikes)
else:
    print("Havn't implemented %s, please use %s or %s for --method"%(args.method, "hungarian","brute_force"))
t1=time.time()
print("algorithm took %.4f sec"%(t1-t0))
print("optimal distance is %d"%(solution[0]))
for (p,b) in solution[1]:
    print("person[%d](%d,%d) -> bike[%d](%d,%d) = %d"%(p,people[p][0],people[p][1],b,bikes[b][0],bikes[b][1],cal_dist(people[p],bikes[b])))
