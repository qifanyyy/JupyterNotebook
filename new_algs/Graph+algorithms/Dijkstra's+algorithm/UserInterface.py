import tkinter as tk
import tkinter.messagebox


class SetupFrames(tk.Frame): # Class initialises all frames in application

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.frames = {}     # Dict that holds record of all frames

        # setup frames
        for new_frame in(LogInFrame, AdminPageFrame, EnterGraphFrame,RandomGraphFrame ,AlgorithmFrame):
            frame = new_frame(self)
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[new_frame] = frame
        self.change_frame(LogInFrame)  # Display Mainframe

    def change_frame(self, frame):   # Method to change between frames when called
        self.frames[frame].tkraise()


class LogInFrame(tk.Frame):  # first frame shown when application run

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        import Database as db

        self.database = db.Database()  # Composition used to access database class

        self.label_username = tk.Label(self, text="Enter username: ")  # label for username
        self.label_pass = tk.Label(self, text="Enter password: ")  # label for password

        self.label_username.grid(row=0, sticky=tk.E)  # Labels placed on frame
        self.label_pass.grid(row=1, sticky=tk.E)

        self.entry_user = tk.Entry(self)  # Entries for user input
        self.entry_pass = tk.Entry(self, show="*")

        self.entry_user.grid(row=0, column=1)  # Positions of entries on frame using
        self.entry_pass.grid(row=1, column=1)

        self.button_checkinputs_user = tk.Button(self, text="Press to log in", command=self.check_valid_user)

        self.button_checkinputs_user.grid(row=3, column=5) # Positioning buttons on frame

    def check_valid_user(self):  # Method validate userinput

        username = self.entry_user.get()  # User input is fetched
        password = self.entry_pass.get()

        username = username.strip()  # Remove any whitespace before/after entry
        password = password.strip()


        if (len(username)) == 0 or (len(password) == 0):
            tk.messagebox.showinfo("title", "Invalid username or password entered, please try again or register")

        else:

            # Validity checked from Method within database (method returns user if valid user or admin if valid admin)
            is_valid = self.database.check_login(username, password)

            if is_valid == "user":  # if valid user
                tk.messagebox.showinfo("title", "You are logged in")
                self.database.c.close()  # close connections to db if user log in
                self.database.conn.close()
                self.master.change_frame(EnterGraphFrame)

            elif is_valid == 'admin':
                tk.messagebox.showinfo('Admin', 'You have logged in as admin')
                self.database.c.close()  # close connections to db if user log in
                self.database.conn.close()
                self.master.change_frame(AdminPageFrame) # Change frame to admin one
                tk.messagebox.showinfo("note to admins", "If you wish to add another admin leave assigned adminid entry "
                                       "blank, otherwise add to it an exisitng adminid for the new user.")

            else:  # If incorrect user must re-enter.
                tk.messagebox.showinfo('Invalid input', 'Password or username not found in records')


class AdminPageFrame(tk.Frame):  # Admin class

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.new_user = ''  # variable that stores the username from entry
        self.new_pass = ''  # variable that stores password from entry
        self.login_adminid = '' # variable to hold adminid (if entered)
        self.login_adminname = ''  # varuabke to hold admin name (if entered)

        self.label_title_add = tk.Label(self, text ="ADD/REMOVE USER")  # title for adding user
        self.label_newuser = tk.Label(self, text="Enter new id: ")  # label for new userid
        self.label_pass = tk.Label(self, text="Enter id password: ")  # label for userid password
        self.label_adminname = tk.Label(self, text="Enter name of admin (if admin): ") # name of admin if admin
        self.label_addadminid = tk.Label(self, text="Enter assigned admin id (if user)")  #label for adding admin to userid
        self.label_viewusers = tk.Label(self, text="VIEW USERS AND ASSIGNED ADMINS")

        self.label_title_add.grid(row=0, sticky=tk.NSEW)
        self.label_newuser.grid(row=1, sticky=tk.NSEW)  # Labels placed on frame
        self.label_pass.grid(row=2, sticky=tk.NSEW)
        self.label_adminname.grid(row=3, sticky=tk.NSEW)
        self.label_addadminid.grid(row=4, sticky=tk.NSEW)
        self.label_viewusers.grid(row=7, sticky=tk.NSEW)

        self.entry_newuser = tk.Entry(self)  # Entries for user input
        self.entry_pass = tk.Entry(self, show="*")  # hide characters for password entry
        self.entry_getname = tk.Entry(self)  # entry for admin name
        self.entry_getid = tk.Entry(self)  # get adminid for the new userid (if user being added)

        self.entry_newuser.grid(row=1, column=2)  # Positions of entries on frame using
        self.entry_pass.grid(row=2, column=2)
        self.entry_getname.grid(row=3, column=2)
        self.entry_getid.grid(row=4, column=2)

        self.button_removeuser = tk.Button(self, text='Remove user', command = self.remove_user)
        self.button_adduser = tk.Button(self, text="Register user", command=self.add_user)
        self.button_view_users = tk.Button(self, text="View system details", command=self.view_users)

        self.button_removeuser.grid(row=4, column=10) # Positioning buttons on frame
        self.button_adduser.grid(row=4, column=7)
        self.button_view_users.grid(row=9)

    def get_info(self):
        self.new_user = self.entry_newuser.get()  # User input is fetched and assigned
        self.new_pass = self.entry_pass.get()  # user input for password fetched and assigned
        self.login_adminname = self.entry_getname.get()  # user input for admin name fetched
        self.login_adminid = self.entry_getid.get()  # admin id fetched

    def remove_user(self): # Method to remove user which can be user or admin
        self.get_info()  # fetch data from entries

        import Database as db  # importing my database module

        self.database = db.Database()
        isadminid = self.database.check_adminid(self.new_user)  # check if Id was admins

        if isadminid:  # Id was admins
            self.database.remove_admin(self.new_user)
            tk.messagebox.showinfo('Removed', 'Admin and associated users have been removed')

        else:
            notuserid = self.database.check_newuser(self.new_user)

            if not notuserid:  # if no invalid userid was found then admin must wish to remove userid
                self.database.remove_user(self.new_user)
                tk.messagebox.showinfo('Removed', 'User has been removed')

            else:
                tk.messagebox.showinfo('Invalid user/admin selected', 'Userid/adminid could not be found in records')

    def validate_info(self):
        import Database as db  # importing my database module
        self.database = db.Database()  # creating connections to database
        self.get_info()  #collect entry information and store in initalised variables

        x = self.database.check_adminid(self.login_adminid)

        if (len(self.new_pass)) == 0 or (len(self.new_user) == 0):  # if no data entered
            tk.messagebox.showinfo("title", "One or more required fields was left blank")
            return False  # invalid data entry

        elif (len(self.login_adminid) != 0) and (len(self.login_adminname) != 0):
            return False  # invalid data entry

        elif (len(self.login_adminid) == 0) and (len(self.login_adminname) == 0):
            return False  # invalid data entry

        elif x:  # if valid adminid added then user must want to add new person as user
            self.new_pass = self.new_pass.strip()  # Remove any whitespace before/after entry
            self.new_user = self.new_user.strip()
            self.login_adminid = self.login_adminid.strip()
            return 'user'

        elif (not x) and (len(self.login_adminid) == 0) and (len(self.login_adminname) != 0):
            # no adminid was given and an admin name was given so must be admin being entered
            self.new_pass = self.new_pass.strip()  # Remove any whitespace before/after entry
            self.new_user = self.new_user.strip()
            return 'admin'

        else:
            return False  # invalid data entry

    def add_user(self):  # Method to add users to system
        check_valid = self.validate_info() # check for valid data entry and type (admin/user)

        if check_valid == 'user' or check_valid == 'admin':
            import Database as db # importing my database module

            self.database = db.Database() # creating connections to database

            valid = self.database.check_newuser(self.new_user)  # check if valid user is being added

            if valid:
                if check_valid == 'admin':
                    self.database.enter_newadmin(self.new_user, self.login_adminname, self.new_pass)  # add admin data
                    self.database.c.close()  # close connections to db if user log in
                    self.database.conn.close()
                else:
                    self.database.enter_newuser(self.new_user, self.new_pass, self.login_adminid)  # add user data
                    self.database.c.close()  # close connections to db if user log in
                    self.database.conn.close()

            else:  # user data is invalid
                tk.messagebox.showinfo('Invalid input', 'Userid already exists please create another id')

        else:
            tk.messagebox.showinfo('Invalid input', 'Please check data was entered correctly')

    def view_users(self):  # Method to view users in system
        import Database as db  # importing my database module
        self.database = db.Database()  # creating connections to database
        tk.messagebox.showinfo('Users with assigned admins', self.database.get_joins())
        self.get_counts()
        self.get_mostfrequser()

    def get_counts(self): # Method to get sum of system users
        import Database as db  # importing my database module
        self.database = db.Database()  # creating connections to database
        tk.messagebox.showinfo("Total number of users in system including admins",
                               list(self.database.get_numusers())[0] + list(self.database.get_numadmins())[0])

    def get_mostfrequser(self): # Method get user with most logins
        import Database as db  # importing my database module
        self.database = db.Database()  # creating connections to database
        self.database.getmostlogin()

class RandomGraphFrame(tk.Frame):  # Class for random graph generation

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        # Button to 'create' random graph
        self.run_random = tk.Button(self, text="press to generate a random graph", command=self.setup_complex)
        self.run_random.grid(row=10, column=15)

    def setup_complex(self):
        import GraphGenerator as graphgen  # importing my random graph generator module
        random_graph = graphgen.ComplexGraph()  # compositon used to access random graph class
        random_graph.setup_nodes()  # random graph being set up
        random_graph.setup_neighbours()
        self.display_data(random_graph.graph)

    def display_data(self, graph):
        import AdjancencyMatrix as amatrix
        display_graph = amatrix.Matrix()
        display_graph.graph = graph
        tk.messagebox.showinfo('Adjacency Matrix for graph', display_graph.create_matrix())  # Complex graph displayed
        self.master.frames[EnterGraphFrame].graph_nodes = graph  # set graph in application to the random graph
        self.master.change_frame(AlgorithmFrame) # change frame to frame with alogrithm


class EnterGraphFrame(tk.Frame):  # Frame where user graph is collected

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.graph_nodes = {}  # Graph is stored as dictionary

        # Button for graph input
        self.run_alg = tk.Button(self, text="press to begin graph entry", command=self.setup_nodes)
        self.run_alg.grid(row=10, column=10)

        self.run_random = tk.Button(self, text="press to generate random graph", command=self.setup_random)
        self.run_random.grid(row=15, column=10)

        self.source_node = tk.StringVar()  # string variable to store source node
        self.neighbour = tk.StringVar()  # string variable to store neighbour node
        self.distance = tk.DoubleVar()  # Float/Double variable to store distance

        self.entry_source = tk.Entry(self, textvariable=self.source_node)   # Entry for source
        self.entry_neighbour = tk.Entry(self, textvariable=self.neighbour)  # Entry for neighbour
        self.entry_distance = tk.Entry(self, textvariable=self.distance)  # Entry for distance

        # Sends information to add_node function for error checking and storage
        self.button_addnode = tk.Button(self, text="Press to add source node and neighbours",
                                        command=self.validate_nodes)

        # Button that calls method that changes frame
        self.button_graphdone = tk.Button(text="Press when graph completed", command=self.graph_entered)

    def setup_random(self):
        self.master.change_frame(RandomGraphFrame)

    def setup_nodes(self):  # Method allows user input for nodes, neighbours and distances

        self.run_alg.grid_forget()  # Hide button that began graph entry
        self.run_random.grid_forget()  # # Hide button that gave option for random generation graph

        enter_source = tk.Label(self, text="Enter the source node: ")
        enter_neighbour = tk.Label(self, text="Enter its neighbour node: ")
        enter_distance = tk.Label(self, text="Enter int value for distance from source to neighbour: ")

        enter_source.grid(row=1)
        enter_neighbour.grid(row=3)
        enter_distance.grid(row=5)

        self.entry_source.grid(row=2, column=0)
        self.entry_neighbour.grid(row=4, column=0)
        self.entry_distance.grid(row=6)
        self.button_addnode.grid(row=0, column=1)
        self.button_graphdone.grid(row=5, column=5)

    def add_nodes(self, source, neighbour, distance):  # Method to add validated nodes to graph variable

        # Creates nested dict for both source and neighbour to add
        # As distance a-b = b-a so when one entered
        # Other can be automatically entered as well

        if source not in self.graph_nodes.keys():
            self.graph_nodes[source] = {}
            self.graph_nodes[source][neighbour] = distance
            self.graph_nodes[neighbour] = {}
            self.graph_nodes[neighbour][source] = distance

        elif neighbour not in self.graph_nodes.keys():
            self.graph_nodes[neighbour] = {}
            self.graph_nodes[source][neighbour] = distance
            self.graph_nodes[neighbour][source] = distance
        else:
            self.graph_nodes[source][neighbour] = distance
            self.graph_nodes[neighbour][source] = distance

        tk.messagebox.showinfo("Current graph", '{}'.format(self.graph_nodes))  # Displays graph user entered thus far

        self.entry_neighbour.delete(0, "end")  # Clear entry for neighbour
        self.entry_distance.delete(0, "end")   # Clear entry for distance

    def graph_entered(self):  # Method changes frame to DisplayAlgorithm Frame

        if len(self.graph_nodes) > 2:
            tk.messagebox.showinfo("Completed graph", '{}'.format(self.graph_nodes))  # display completed graph
            print(self.graph_nodes)
            self.master.change_frame(AlgorithmFrame)  # change frame
            self.button_graphdone.grid_forget()  # Hide button
        else:
            tk.messagebox.showerror('Graph Invalid', 'Please ensure it has at least two unique nodes')  # catch graph error

    def validate_nodes(self):  # Method to validate user inputs

        is_valid = False
        try:
            if (self.distance.get() >=0) and (len(self.source_node.get()) > 0) and (len(self.neighbour.get()) > 0):
                is_valid = True

        except tk.TclError:  # when non double data type entered error raised
            self.entry_distance.delete(0, 'end')

        if is_valid:
            self.add_nodes(self.source_node.get(), self.neighbour.get(), self.distance.get())

        else:
            tk.messagebox.showinfo("Invalid distance", "Invalid input detected, please ensure no fields are blank "
                                                       "and that distance is greater than or equal to 0")
            self.entry_distance.delete(0, 'end')


class AlgorithmFrame(tk.Frame):  # Frame to display results of algorithm

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        import Dijks as dk # Dijkstra module imported

        self.graph = dk.Dijkstra()  # Graph class called using composition

        self.button_display_sp = tk.Button(self, text="Press to apply Dijkstra's Algorithm to graph",
                                           command=self.check_startend)
        self.button_display_sp.grid(row=1, column=4)

        # Button closes application , only defined here but placed on frame after algorithm is run
        self.quitapp = tk.Button(self, text="Press to quit application", command=self.end_program)

        self.label_start_node = tk.Label(self, text="Enter start node: ")  # labels for start node
        self.label_end_node = tk.Label(self, text="Enter end node: ")  # labels for end node

        self.entry_start = tk.Entry(self)  # entry for start node
        self.entry_end = tk.Entry(self)  # entry for end node

        self.label_start_node.grid(row=0, sticky=tk.E)
        self.label_end_node.grid(row=1, sticky=tk.E)
        self.entry_start.grid(row=0, column=1)
        self.entry_end.grid(row=1, column=1)

    def display_data(self):  # Method displays result of algorithm and allows user to exit

        # Hide buttons previously on frame
        # Not destroyed as user may wish to restart program
        self.button_display_sp.grid_forget()
        self.label_end_node.grid_forget()
        self.label_start_node.grid_forget()
        self.entry_end.grid_forget()
        self.entry_start.grid_forget()

        # Displays user graph , shortest path and the distance of shortest path
        label_graph = tk.Label(self, text="User graph:     "
                                          ""+'{}'.format(self.master.frames[EnterGraphFrame].graph_nodes))
        label_sp = tk.Label(self, text="A shortest path is through : " + '{}'.format(self.graph.shortest_path))
        label_distance = tk.Label(self, text="With distance: "'{}'.format(self.graph.distance_node[self.graph.end]))

        label_graph.grid(row=0, sticky=tk.E)
        label_sp.grid(row=1, sticky=tk.E)
        label_distance.grid(row=2, sticky=tk.E)

        self.quitapp.grid(row=4, sticky=tk.NSEW)  # Adds button that exits program.

    def check_startend(self):  # Method to check userinputs for start end nodes

        # user entered graph is fetched from previous frame
        self.graph.nodes = self.master.frames[EnterGraphFrame].graph_nodes

        # checks to ensure start and end node are in user graph
        if (self.entry_start.get() not in self.graph.nodes.keys()) or \
                (self.entry_end.get() not in self.graph.nodes.keys()):    # if invalid

            tk.messagebox.showerror("Invalid start/end node","Please enter a valid start/end node")
            self.entry_start.delete(0, 'end')  # clear start node entry
            self.entry_end.delete(0, 'end')  # clear end node entry

        else:
            self.apply_algorithm()  # if valid then apply algorithm

    def apply_algorithm(self):  # Method apply Dijkstra algorithm to user graph

        self.graph.start = self.entry_start.get()  # user input fetched for start node
        self.graph.end = self.entry_end.get()  # user input fetched for end node

        self.graph.calc_shortest_path()  # apply algorithm given graph

        self.display_data()  # Call method to display result of algorithm

    def end_program(self):  # Method when called ends program
        root.destroy()

if __name__ == '__main__':
    root = tk.Tk()  # Initialising GUI and running it
    gui = SetupFrames(root).grid()
    root.mainloop()
