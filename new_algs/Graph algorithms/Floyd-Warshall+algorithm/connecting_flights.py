from . import Database
# import time


class ConnectingFlights:
    """Class to calculate ConnectingFlights"""

    def __init__(self, database):
        """Constructor. Takes Database object"""

        self.db = database

    def add_one_flight(self, orig, dest, **kwargs):
        """Add one flight to database. Accept multiple weights as kwrags"""
        print(kwargs)
        self.db.add_flight(orig, dest, **kwargs)
        self.calc_all()  # calculate shortest path

    def add_many_flights(self, arr):
        """Accept list of list, format: [orig, dest, **weight]"""
        for new_flight in arr:
            orig = new_flight[0]
            dest = new_flight[1]
            self.db.add_flight(orig, dest, **new_flight[2])

        self.calc_all()  # calculate shortest path

    def calc_all(self):
        """Calculate adjency table for all critera"""

        self.db.clear_adj()
        print("Calculating shortest paths...")
        # calculate shortest path for each criterion
        for cri in Database.Criterion:
            print("Calculating for {}...".format(cri.name))
            # t1 = time.time()
            self.floyd_warshal(cri)
            # t2 = time.time()
            # print("used {}s.\n".format(t2-t1))  # print time took for calculation

    def floyd_warshal(self, criterion):
        """Generate shortest path data in db using floyd warshal algorithm"""

        all_airports = self.db.all_airports

        # init adjacency list
        self.make_adj(criterion)

        for thru in all_airports:   # thru = intermediate vertex to consider
            for orig in all_airports:
                if orig == thru:
                    continue  # continue if intermediate is same as origin
                for dest in all_airports:
                    if dest == thru or dest == orig:
                        # continue if intermediate or destination is origin
                        continue

                    # origin->intermediate, intermediate->destination
                    orig_to_thru = self.db.get_adj(criterion, orig, thru)
                    thru_to_dest = self.db.get_adj(criterion, thru, dest)

                    if orig_to_thru is None or thru_to_dest is None:
                        # do nothing when not accessable thrugh intermediate
                        continue

                    # calculate new weight when going through intermediate "thru" vertex
                    new_weight = float(orig_to_thru["weight"]) + float(thru_to_dest["weight"])

                    last_path = thru_to_dest["thru"]
                    last_flight = thru_to_dest["last_flight"]

                    # get existing adjency entry
                    orig_adj = self.db.get_adj(criterion, orig, dest)

                    if orig_adj is None:  # if no path was discovered before, add.
                        self.db.add_to_adj(criterion, orig, dest, last_path,
                                           new_weight, last_flight)
                    else:
                        # if new weight total is shorter,
                        # use intermediate vertex as part of shortest path
                        old_weight = float(orig_adj["weight"])
                        if new_weight < old_weight:
                            self.db.update_adj(criterion, orig, dest,
                                               last_path, new_weight, last_flight)

    def print_floyd_warshal(self, criterion):
        """Print shortest path for each origin and destination pair"""

        # get string list of all airports
        all_airports = self.db.all_airports

        for orig in all_airports:
            for dest in all_airports:
                print("\n{} to {}:".format(orig, dest))

                # get shortest path info
                result = self.get_shortest_floyd_warshal(criterion, orig, dest)

                if len(result["path"]) != 0:
                    for o, d, w, f in result["path"]:
                        if f is None:
                            f = ""
                        weight = self.get_str_from_cri(criterion, w)
                        print("{} {}->{}: {}".format(f, o, d, weight))

                    total = self.get_str_from_cri(criterion,
                                                  result["total_weight"])

                    print("Total {}: {}".format(criterion.name, total))

                else:
                    print("No data")

    def get_shortest_floyd_warshal(self, criterion, orig, dest):
        """Take criterion, origin, and destination and return shortest path info"""

        output = {}
        shortest = []

        start = orig
        end = dest
        total = 0.0
        while start != end:  # backtrack to find shortest path
            # get shortest from start to end
            adj = self.db.get_adj(criterion, start, end)

            if adj is None:  # break if no data found
                break

            mid = adj["thru"]  # get the last vertex before the end in shortest path
            weight = float(self.db.get_weight(criterion, mid, end))
            airline_id = adj["last_flight"]
            shortest.append((mid, end, weight, airline_id))
            total += weight
            end = mid   # backtracking by using intermediate point as end point

        output["path"] = shortest[::-1]  # reverse list
        output["total_weight"] = total
        return output

    @staticmethod
    def get_str_from_cri(criterion, target):
        """Return formatted string with associated unit"""

        if criterion == Database.Criterion.price:
            return "${}".format('%.2f' % target)
        elif criterion == Database.Criterion.duration:
            return "{}h {}m".format(int(target // 60), int(target % 60))
        elif criterion == Database.Criterion.distance:
            return "{} miles".format(target)

    def make_adj(self, criterion):
        """Initialize adj with flights"""

        weight_name = criterion.name
        for flight in self.db.all_flights:
            orig = flight["orig"]
            dest = flight["dest"]
            try:
                last_flight_info = (flight["airline"], flight["no"])
            except KeyError:  # if no info
                last_flight_info = None
            try:
                weight = float(flight[weight_name])
                find_existing = self.db.get_adj(criterion, orig, dest)
                if find_existing is None:
                    # add to adj if none existing for this origin destination pair
                    self.db.add_to_adj(criterion, orig, dest, orig, weight,
                                       last_flight_info)
                    continue

                if weight < float(find_existing["weight"]):
                    # update adjency with new weight and last fight if adj info
                    # exists but new weight is smaller
                    self.db.update_adj(criterion, orig, dest, orig, weight,
                                       last_flight_info)

            except KeyError:
                pass  # ignore if the specified weight attribute does not exist
