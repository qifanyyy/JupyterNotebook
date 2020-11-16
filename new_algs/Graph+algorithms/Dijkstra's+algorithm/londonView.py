# UID: 1901208601

import tkinter as tk
import londonController

# Create list of stations from dictionary
def getStationList():
    stations = []

    stationList = londonController.getStations()

    for x in stationList:
        stations.append(stationList[x]['name'])

    stations.sort()

    return stations

# Built around the Tkinter reference and exercise 1.10.8 in the 4th Python Practical:
# https://students.keele.ac.uk/bbcswebdav/pid-1765740-dt-content-rid-4678813_1/courses/CSC-40044-2019-SEM1-A/tkinter.pdf
# https://students.keele.ac.uk/bbcswebdav/pid-1765739-dt-content-rid-4680937_1/courses/CSC-40044-2019-SEM1-A/python4%281%29.pdf
class GUI(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)

        # Class Variables
        self.stationList = getStationList()
        self.startingStation = ''
        self.endingStation = ''
        self.unavailableStations = []

        # Initiate widgets
        self.grid()
        self.createWidgets()

    # Create the GUI here
    def createWidgets(self):
        # Label for error handling
        self.errorLabel = tk.Label(self, text="", width=90)
        self.errorLabel.grid(row = 0, column = 0, columnspan = 3)

        # Label for stations list box
        self.stationLabel = tk.Label(self, text="Stations", width=6)
        self.stationLabel.grid(row = 1, column = 0)

        # Initiate station list box widget
        self.stations = tk.Listbox(self, width = 40, height = 5)
        self.stations.grid(row = 2, column = 0)

        # Add stations to the station list box
        for station in self.stationList:
            self.stations.insert(tk.END, station)

        # Label for unavailable stations list box
        self.unavailableStationLabel = tk.Label(self, text="Unavailable Stations", width=20)
        self.unavailableStationLabel.grid(row = 1, column = 2)

        # Initiate station list box widget
        self.unavailableStationsListBox = tk.Listbox(self, width = 40, height = 5)
        self.unavailableStationsListBox.grid(row = 2, column = 2)

        # Button for setting the starting station
        self.startingStationButton = tk.Button(self, text = 'Set Start', command = self.setStart, width = 15, padx = 0)
        self.startingStationButton.grid(row = 2, column = 1, sticky = tk.N)

        # Button for setting the ending station
        self.endingStationButton = tk.Button(self, text = 'Set End', command = self.setEnd, width = 15, padx = 0)
        self.endingStationButton.grid(row = 2, column = 1)

        # Button for adding to the unavailable stations list box
        self.setUnavailable = tk.Button(self, text = 'Set Status', command = self.changeStatus, width = 15, padx = 0)
        self.setUnavailable.grid(row = 2, column = 1, sticky = tk.S)

        # Confirmation Label
        self.routeLabel = tk.Label(self, text="", width=50)
        self.routeLabel.grid(row = 3, column = 0, columnspan = 2, sticky = tk.W)

        # Confirmation Button
        self.confirmRoute = tk.Button(self, text = 'Confirm Route', command = self.findRoute, width = 15)
        self.confirmRoute.grid(row = 3, column = 2, sticky = tk.E)

        # Suggested Route
        self.routeText = tk.Text(self, height = 5, width = 80)
        self.routeText.grid(row = 4, column = 0, columnspan = 3, padx = 5)

    def setStart(self):
        # get selected index
        index = self.stations.curselection()[0]

        # get selected station
        self.startingStation = self.stations.get(index)

        # set label string
        if self.endingStation != '':
            updatedText = "From %s to %s" % (self.startingStation, self.endingStation)
        else:
            updatedText = "From %s" % (self.startingStation)

        # update route label
        self.routeLabel.config(text = updatedText)

    def setEnd(self):
        # get selected index
        index = self.stations.curselection()[0]

        # get selected station
        self.endingStation = self.stations.get(index)

        # set label string
        if self.startingStation != '':
            updatedText = "From %s to %s" % (self.startingStation, self.endingStation)
        else:
            updatedText = "%s to %s" % (self.routeLabel['text'], self.endingStation)

        # update route label
        self.routeLabel.config(text = updatedText)

    # Change the status of the station
    def changeStatus(self):
        # If in active stations list box move to unavailable stations
        if (self.stations.curselection()):
            station = self.changeStationStatus(self.stations, self.unavailableStationsListBox)
            self.unavailableStations.append(station)

        # If in unavailable stations list box move to active stations
        if (self.unavailableStationsListBox.curselection()):
            station = self.changeStationStatus(self.unavailableStationsListBox, self.stations)
            self.unavailableStations.remove(station)

    def changeStationStatus(self, moveFrom, moveTo):
        # get selected index
        index = moveFrom.curselection()[0]

        # get selected station
        station = moveFrom.get(index)

        # create a temp list of stations from target listbox
        tempList = list(moveTo.get(0, tk.END))
        tempList.append(station)
        tempList.sort()

        # clear current list of stations in target listbox
        moveTo.delete(0, tk.END)

        # insert all stations into target listbox
        for item in tempList:
            moveTo.insert(tk.END, item)

        # remove station from previous listbox
        moveFrom.delete(index)

        # return the moved station
        return station

    def findRoute(self):
        # Run the route algorithm
        route = londonController.findFastestRoute(self.startingStation, self.endingStation, self.unavailableStations)

        # If the route is a list calculation was successful, else error occurred
        if isinstance(route, list):
            # Show the suggested route
            self.setRouteText(route)

            # Display Success Message
            self.displayResponse({'error': False, 'msg': 'Route Calculated'})
        else:
            # Clear any current route
            self.setRouteText(None)

            # Display Error Message
            self.displayResponse(route)

    # Show the suggested route
    def setRouteText(self, route):
        # Clear current route text
        self.routeText.delete(1.0, tk.END)

        if route:
            # count of total stations in route to prevent '>' on last station
            stationCount = len(route)

            self.routeText.insert(tk.END, "Suggested Route: ")

            # Append each station to the route text
            for station in route:
                # If station is the last station in route, dont add '>' to end
                if str(station) == str(route[stationCount-1]):
                    station = "%s" % station
                else:
                    station = "%s > " % station

                self.routeText.insert(tk.END, station)

    # Set the success / error message
    def displayResponse(self, response):
        if response:
            background = 'Green'

            if response['error']:
                background = 'Red'

            self.errorLabel.config(background=background, text=response['msg'])

# Everything needed to create the view
def initiateView():
    app = GUI()
    app.master.title('London Underground Route Finder')
    app.mainloop()

# Display the view
initiateView()
