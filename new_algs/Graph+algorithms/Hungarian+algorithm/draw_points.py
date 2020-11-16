import argparse
import matplotlib.pyplot as plt
import matplotlib.ticker as tck
import numpy as np
import shapely.geometry as sg
import json
import itertools
import functools

def parse_commandline_args():
  parser = argparse.ArgumentParser(
      description = "Draw points for the test Hungarian algorithm implementation"
      )

  parser.add_argument("-i", "--in-file", type=str, help="The input file")
  parser.add_argument("-o", "--out-file", type=str, help="Where to write the plot")
  parser.add_argument("-g", "--draw-groups", action="store_true", dest="draw_groups", help="Draw the groups")
  parser.add_argument("-G", "--no-draw-groups", action="store_false", dest="draw_groups", help="Do not draw the groups")
  parser.add_argument("-s", "--draw-sparse", action="store_true", dest="draw_sparse", help="Draw the sparse matching")
  parser.add_argument("-S", "--no-draw-sparse", action="store_false", dest="draw_sparse", help="Do not draw the sparse matching")
  parser.add_argument("-m", "--draw-hungarian", action="store_true", dest="draw_hungarian", help="Draw the hungarian matching")
  parser.add_argument("-M", "--no-draw-hungarian", action="store_false", dest="draw_hungarian", help="Do not draw the hungarian matching")
  parser.set_defaults(
      draw_groups = False,
      draw_sparse = False,
      draw_hungarian = False
      )

  return parser.parse_args()

def get_bounds(point, radius):
  bound = sg.Point(point).buffer(radius)
  bounds = [bound]
  if point[0]+radius > 2*np.pi:
    bounds.append(sg.Point(point[0] - 2*np.pi, point[1]).buffer(radius) )
  if point[0]-radius < 0:
    bounds.append(sg.Point(point[0] + 2*np.pi, point[1]).buffer(radius) )
  return bounds

def get_union_boundary(point_list, radius):
  bounds = list(itertools.chain(*(get_bounds(p, radius) for p in point_list)))
  return functools.reduce(lambda x, y: x.union(y), bounds)

def get_coords(poly):
  return poly.boundary.coords.xy

def plot_points(points_a, points_b):
  plt.plot([p/np.pi for p in zip(*points_a)[0]], zip(*points_a)[1], 'ro')
  plt.plot([p/np.pi for p in zip(*points_b)[0]], zip(*points_b)[1], 'bo')

def plot_groups(group_indices, points_a, points_b, max_radius):
  group_points = [points_a[i] for i in group_indices[0]] + [points_b[i] for i in group_indices[1]]
  boundary = get_union_boundary(group_points, max_radius)
  if isinstance(boundary, sg.multipolygon.MultiPolygon):
    for geo in boundary:
      coords = get_coords(geo)
      plt.plot([p/np.pi for p in coords[0]], coords[1], '--', color='black')
  else:
    coords = get_coords(boundary)
    plt.plot([p/np.pi for p in coords[0]], coords[1], '--', color='black')

def plot_matching(matching, points_a, points_b, color='black', **kwargs):
  for ia, ib in matching:
    a = points_a[ia]
    b = points_b[ib]
    if abs(a[0] - b[0]) < np.pi:
      plt.plot([a[0]/np.pi, b[0]/np.pi], [a[1], b[1]], color=color, **kwargs)
    else:
      # Work out the intersection with the axes
      if a[0] > b[0]:
        left = b
        right = a
      else:
        left = a
        right = b
      slope = (right[1]-left[1])/(right[0]-left[1])
      intercept = right[1] - right[0]*slope
      plt.plot([right[0]/np.pi, 2], [right[1], intercept + slope*2*np.pi], color=color, **kwargs)
      plt.plot([0, left[0]/np.pi], [intercept, left[1]], color=color, **kwargs)
        

if __name__ == "__main__":
  args = parse_commandline_args()

  if args.in_file is None:
    raise RuntimeError("No input file provided!")
  if args.out_file is None:
    raise RuntimeError("No output file provided!")
  with open(args.in_file) as fp:
    conf = json.load(fp)
  plot_points(conf["PointsA"], conf["PointsB"])
  if args.draw_groups:
    for group in conf["Groups"]:
      plot_groups(group, conf["PointsA"], conf["PointsB"], conf["MaxDR"])
  if args.draw_sparse:
    plot_matching(conf["SparseMatches"], conf["PointsA"], conf["PointsB"], color = 'black')
  if args.draw_hungarian:
    plot_matching(conf["HungarianMatches"], conf["PointsA"], conf["PointsB"], color = 'gray', dashes=(1,1))
  plt.gca().xaxis.set_major_formatter(tck.FormatStrFormatter('%g $\pi$'))
  plt.gca().xaxis.set_major_locator(tck.MultipleLocator(base=0.5))
  plt.gca().set_xlim(0, 2)
  plt.grid(b=True, which='major', axis='both', linestyle='--', color= 'gray', linewidth=0.5)
  plt.xlabel("$\phi$")
  plt.ylabel("$\eta$")
  plt.savefig(args.out_file)
