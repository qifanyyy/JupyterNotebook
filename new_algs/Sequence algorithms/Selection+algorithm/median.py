"""
Copyright (C) 2014-2017 cloudover.io ltd.
This file is part of the CloudOver.org project

Licensee holding a valid commercial license for this software may
use it in accordance with the terms of the license agreement
between cloudover.io ltd. and the licensee.

Alternatively you may use this software under following terms of
GNU Affero GPL v3 license:

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version. For details contact
with the cloudover.io company: https://cloudover.io/


This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.


You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


from corecluster.models.core.node import Node
from corecluster.utils.exception import CoreException


def select(template, image):
    """
    Method finds first (or with given id) Node that is sufficient enough
    for specified \c Image and \c Template and returns that Node.

    @parameter{template,Template} instance of the VM's Template to run on
    searched Node
    @parameter{image,Image} instance of the Image to run on searched Node
    @parameter{node_id,int} @optional{first suitable}

    @returns{Node} sufficient instance of the Node

    @raises{node_get,CoreException} cannot get sufficient Node
    """
    available_nodes = []

    # Get all nodes, which fit this VM
    for node in Node.objects.filter(state='ok'):
        if node.cpu_free >= template.cpu and node.memory_free >= template.memory and node.hdd_free >= template.hdd:
            available_nodes.append(node)

    if not available_nodes:
        raise CoreException('node_not_available')

    # Get best matching (miedian filled) node
    available_nodes.sort(key=lambda node: node.cpu_free)
    return available_nodes[int(len(available_nodes)/2)]
