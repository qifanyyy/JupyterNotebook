from distutils.core import setup


description = ("A dynamic plotter of the minimum spanning tree of a graph " 
               "using Dijkstra's, Kruskal's and Prim's algorithm")

with open('README.md', 'rb') as f:
    readme = f.read().decode('utf8')

setup(name='mstfind',
      version='1.0.0',
      author='Mario Sasko',
      author_email='mariosasko777@gmail.com',
      url='https://github.com/mariosasko/mstfind',
      packages=['mstfind'],
      entry_points={
        'console_scripts': ['mstfind = mstfind.runner:main'],
      }, 
      description=description,
      long_description=readme,
      license='MIT',
      install_requires=['matplotlib', 'networkx'],
     )