import sys

root = 'C:/Users/temp-admin/Desktop/ove/xeme'
sys.argv = ['',\
			'--root={}/libs/closure-library/'.format(root),\
            '--root={}/js/'.format(root),\
            '--namespace=xeme.ui.GraphViewer',\
            '--namespace=xeme.coloring.Graph',\
            '--namespace=xeme.draw.Canvas',\
            '--output_mode=compiled',\
            '--compiler_jar={}/compiler.jar'.format(root)]

sys.path.append('{}/libs/closure-library/closure/bin/build/'.format(root))

output_location = 'C:/Users/temp-admin/Desktop/ove/webcode/static/js'
x = open('{}/xm_compiled.js'.format(output_location),'w')

save = sys.stdout
sys.stdout=x
execfile("{}/libs/closure-library/closure/bin/build/closurebuilder.py".format(root))
sys.stdout=save
x.close()
