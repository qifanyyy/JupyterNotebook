import xml.dom.minidom as minidom

class RouteManager():
    def __init__(self, map_folder, 
    route_configs={
        "pattern":"fixed" #or "random"
        }):
        self.route_configs = route_configs

    def bind_simulator(self, sim):
        self.simulator = sim

    def init_routes(self):
        dom = minidom.getDOMImplementation().createDocument(None, 'routes', None)
        root = dom.documentElement
        vType = dom.createElement('vType')
        vType.setAttribute('id', "car")
        vType.setAttribute('accel', "0.8")
        vType.setAttribute('decel', "4.5")
        vType.setAttribute('sigma', "0.5")
        vType.setAttribute('length', "5")
        vType.setAttribute('maxSpeed', "40")
        root.appendChild(vType)
        for i in range(0, 20):
            vehicle = dom.createElement('vehicle')
            vehicle.setAttribute('id', str(i))
            vehicle.setAttribute('type', "car")
            vehicle.setAttribute('depart', "0")
            vehicle.setAttribute('color', "1, 0, 0")
            root.appendChild(vehicle)
            route = dom.createElement('route')
            route.setAttribute('edges', "west_in east_out")
            vehicle.appendChild(route)
        for i in range(20, 40):
            vehicle = dom.createElement('vehicle')
            vehicle.setAttribute('id', str(i))
            vehicle.setAttribute('type', "car")
            vehicle.setAttribute('depart', "0")
            vehicle.setAttribute('color', "0, 1, 0")
            root.appendChild(vehicle)
            route = dom.createElement('route')
            route.setAttribute('edges', "north_in south_out")
            vehicle.appendChild(route)
        for i in range(40, 60):
            vehicle = dom.createElement('vehicle')
            vehicle.setAttribute('id', str(i))
            vehicle.setAttribute('type', "car")
            vehicle.setAttribute('depart', "0")
            vehicle.setAttribute('color', "0, 0, 1")
            root.appendChild(vehicle)
            route = dom.createElement('route')
            route.setAttribute('edges', "east_in west_out")
            vehicle.appendChild(route)
        for i in range(60, 80):
            vehicle = dom.createElement('vehicle')
            vehicle.setAttribute('id', str(i))
            vehicle.setAttribute('type', "car")
            vehicle.setAttribute('depart', "0")
            vehicle.setAttribute('color', "1, 1, 0")
            root.appendChild(vehicle)
            route = dom.createElement('route')
            route.setAttribute('edges', "south_in north_out")
            vehicle.appendChild(route)
        with open("simulator/maps/simple/map.rou.xml", 'w', encoding='utf-8') as f:
            dom.writexml(f, addindent='\t', newl='\n', encoding='utf-8')

    def step(self):
        # print ("route manager stepped")
        a = 1