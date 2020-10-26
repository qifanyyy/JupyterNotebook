from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
@csrf_exempt
def home(request):
	if request.method == 'GET':
		return render(request, 'graph.html')
    	elif request.method == 'POST':
        	adj = request.POST['adj_data']
        	adj_list = json.loads(adj)
   		not_colored = sorted(adj_list.items(), key=lambda k: len(k[1]), reverse=True)
		check = len(not_colored) *[0]
		color_data = {}
		color_list = [ i for i in range(0, len(not_colored))]
		for node in not_colored:
			color_list_dup = []
			color_list_dup.extend(color_list)
			for j in node[1]:
				if check[j-1]:
					try:
						color_list_dup[color_data[j]] = None
					except:
						pass
			for color in color_list_dup:
				if color != None:
					color_data[int(node[0])] = color
					break
			check[int(node[0])-1] = 1
		return HttpResponse(json.dumps(color_data))


