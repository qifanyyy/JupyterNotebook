from django.db import models

class Graph(models.Model):
	node_id=models.CharField(max_length=60)
	vertex_x=models.CharField(max_length=60)
        vertex_y=models.CharField(max_length=60)
