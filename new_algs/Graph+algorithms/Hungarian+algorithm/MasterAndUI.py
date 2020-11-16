# -*- coding: utf-8 -*-
#coding:utf8

from tkinter.filedialog import *
from tkinter import ttk;
import ExcelHandler
import DataHandler


def InitializeRoot():
    global tabStuScrollable, tabActScrollable, stuSearchVar, actSearchVar, stuCountVar, actCountVar, statsVar, mainframe, nb

    root = Tk ()
    root.geometry ("800x600")
    root.minsize = (800, 600);
    root.title ("Meslek Atölyeleri Öğrenci Yerleştiricisi")
    # root.iconbitmap ('icon.ico')

    # Add a grid
    mainframe = Frame (root)
    mainframe.config (width = 800, height = 800);
    mainframe.pack (side = "top", fill = "both", expand = True, padx = 10, pady = 10);

    Label (mainframe, text = "Meslek Atölyeleri Öğrenci Yerleştirici", font = ("TkDefaultFont", 15, "bold")).pack (side = "top", anchor = "w", padx = 20);
    Frame (mainframe, height = 5).pack (side = "top", anchor = "w");

    # -------------------------------General Tab Setup
    nb = ttk.Notebook (mainframe)
    tabStudents = Frame (nb)  # first page, which would get widgets gridded into it
    tabActivities = Frame (nb)  # second page
    nb.add (tabStudents, text = 'Students')
    nb.add (tabActivities, text = 'Activities')
    nb.pack (side = "top", fill = "both", expand = True);

    statsVar = StringVar ()
    statsVar.set ("Average Choice: -     Worst Choice: -" + "      " +  "Average Fill: -     Least Fill: -     Max Fill: -")

    # -------------------------------Tab Student stuff
    stuTopStuff = Frame (tabStudents, bg = "#f9f9f9")
    stuTopStuff.pack (fill = "x", ipadx = 5, ipady = 10)

    addStuButton = Button (stuTopStuff, text = "Import from Excel", command = ExcelHandler.LoadFromExternalExcelFile, bg = "#f9f9f9");
    addStuButton.pack (side = "left", padx = 5)

    stuCountVar = StringVar()
    stuCountVar.set("Total Students: 0    Currently Visible: 0")
    Label(stuTopStuff, textvariable=stuCountVar, bg = "#f9f9f9").pack(side="left", padx=5)

    Label(stuTopStuff, textvariable=statsVar, bg = "#f9f9f9").pack(side="left", padx=5)

    stuSearchBar = Frame (stuTopStuff, bg = "#f9f9f9")
    stuSearchBar.pack (side = "right", padx = 5)

    stuSearchVar = StringVar()
    stuSearchVar.trace_add ("write", DataHandler.StuSearchBarUpdate)
    stuSearchEntry = Entry (stuSearchBar, textvariable=stuSearchVar);
    Label (stuSearchBar, text = "Search:", bg = "#f9f9f9").pack (side = "left")
    stuSearchEntry.pack (side = "left");

    Frame (tabStudents, background = "#d6d6d6", height = 1).pack (fill = "x")
    Frame (tabStudents, height = 3).pack (fill = "x")

    tabStuScrollable = VerticalScrolledFrame (tabStudents, "Students", bg = "purple");
    tabStuScrollable.pack (fill = "both", expand = True)

    # -------------------------------Tab Activities stuff
    actTopStuff = Frame (tabActivities, bg = "#f9f9f9")
    actTopStuff.pack (fill = "x", ipadx = 5, ipady = 10)

    addActButton = Button (actTopStuff, text = "Import from Excel", command = ExcelHandler.LoadFromExternalExcelFile, bg = "#f9f9f9");
    addActButton.pack (side = "left", padx = 5)

    actCountVar = StringVar ()
    actCountVar.set ("Total Activities: 0    Currently Visible: 0")
    Label (actTopStuff, textvariable = actCountVar, bg = "#f9f9f9").pack (side = "left", padx = 5)

    Label (actTopStuff, textvariable = statsVar, bg = "#f9f9f9").pack (side = "left", padx = 5)

    actSearchBar = Frame (actTopStuff, bg = "#f9f9f9")
    actSearchBar.pack (side = "right", padx = 5)

    actSearchVar = StringVar ()
    actSearchVar.trace_add ("write", DataHandler.ActSearchBarUpdate)
    actSearchEntry = Entry (actSearchBar, textvariable = actSearchVar);
    Label (actSearchBar, text = "Search:", bg = "#f9f9f9").pack (side = "left")
    actSearchEntry.pack (side = "left");

    Frame (tabActivities, background = "#d6d6d6", height = 1).pack (fill = "x")
    Frame (tabActivities, height = 3).pack (fill = "x")

    tabActScrollable = VerticalScrolledFrame (tabActivities, "Activities", bg = "purple");
    tabActScrollable.pack (fill = "both", expand = True)
    # -------------------------------End of Tab stuff


    Label (mainframe, height = 1).pack (fill = "x");  # spacer
    bottomButtonFrame = Frame(mainframe)
    bottomButtonFrame.pack(fill = "x", ipady=2)
    Button (bottomButtonFrame, text = "Assign Students", command = lambda : DataHandler.AssignStudents()).pack (side="left", fill = "x", expand=1, padx=5);
    Button (bottomButtonFrame, text = "Export Results", command = lambda: ExcelHandler.ExporttoExcelFile()).pack (side = "left", fill = "x", expand=1, padx=5);

    return root;

def ok ():
    print("ok");


def UIAddStudent (stu):
    if(stu.myFrame != None):
        return ;

    stu.myFrame = Frame (tabStuScrollable.interior)
    stu.myFrame.pack(side="top", fill="x", ipadx=10, ipady=3, pady=2);

    Frame (stu.myFrame, background = "#d6d6d6", height = 1).pack (side="top", fill = "x")
    inFrame = Frame (stu.myFrame)
    inFrame.pack(side="top", expand=True,fill="both")
    Frame (stu.myFrame, background = "#d6d6d6", height = 1).pack (side="top", fill = "x")

    Label(inFrame, text = str(stu.grade), width=3, anchor=E).pack(side="left", padx=5, pady=5);
    Label(inFrame, text = stu.name, width=15, anchor=W).pack(side="left", padx=5, pady=5);

    choiceFrame = Frame(inFrame);
    choiceFrame.pack(side="left", padx=5, pady=5);

    #------- Choice Stuff
    stu.myButtons = []
    for n in range (DataHandler.periodCount):
        stu.myButtons.append ([]);
    p = 0
    for period in stu.choices:
        n = 0
        if(len(period) > 0):
            Label(choiceFrame, text = str(p+1) + ". Period: ").grid(row = p, column = 0);
        for act in period:
            myBut = Button(choiceFrame, text = str(n+1) + ". " + act.name, command = lambda stu=stu, p=p, n=n: ToggleActivityForcedStatus(stu, p, n), width = 25, background = "#93ff80");
            myBut.grid(row = p, column = n + 1, padx = 2);
            stu.myButtons[p].append(myBut);
            n += 1;
            if n >= 5:
                break;
        p += 1;

#Button colors:
#def color = "#f0f0f0"
#green = #93ff80
#yellow = #fffd80
#orange =  ##ffaa80
#red = #ff8080
def ToggleActivityForcedStatus (stu : DataHandler.Student, period, index):
    if stu.choices[period][index].isForced == True:
        stu.choices[period][index].isForced = False
        stu.myButtons[period][index].configure(font = "arial 9 normal")
        DataHandler.UpdateButtonColors()
        print("Student: " + stu.name + "  Period: " + str(period) + "  Activity: " + stu.choices[period][index].name + " is unforced")
    else:
        stu.choices[period][index].isForced = True
        stu.myButtons[period][index].configure(font = "arial 9 bold")
        print("Student: " + stu.name + "  Period: " + str(period) + "  Activity: " + stu.choices[period][index].name + " is FORCED")

        DataHandler.AssignStudentToActivity(stu, period, index, True, "DUMMY NAME");
        DataHandler.UpdateActivityAssignmentsUI();
        DataHandler.CalculateAverages();

        n = 0
        for act in stu.choices[period]:
            if(act.isForced) and (n != index):
                ToggleActivityForcedStatus(stu,period,n);
            n += 1;

def UIAddActivity (act):
    if(act.myFrame == None):
        act.myFrame = Frame (tabActScrollable.interior)
        act.myFrame.pack(side="top", fill="x",ipadx=10,ipady=3,pady=2);

        Frame (act.myFrame, background = "#d6d6d6", height = 1).pack (side="top", fill = "x")
        inFrame = Frame (act.myFrame)
        inFrame.pack(side="top", expand=True,fill="both")
        Frame (act.myFrame, background = "#d6d6d6", height = 1).pack (side="top", fill = "x")

        Label(inFrame, text = str(act.period+1), width=3,anchor=E).pack(side="left",padx=5,pady=5);
        Label(inFrame, text = act.name,width=15,anchor=W).pack(side="left", padx=5,pady=5);

        act.stuNameParentFrame = Frame(inFrame, bg="pink")
        act.stuNameParentFrame.pack(side="left", padx=10, pady=5);
        act.stuNameFrame = Frame(act.stuNameParentFrame, bg="blue");
        act.stuNameFrame.pack();


def HideStudent (stu):
    stu.myFrame.pack_forget();
def ShowStudent (stu):
    stu.myFrame.pack (side = "top", fill = "x", ipadx = 10, ipady = 3, pady = 2);

def HideActivity (act):
    act.myFrame.pack_forget();
def ShowActivity (act):
    act.myFrame.pack (side = "top", fill = "x", ipadx = 10, ipady = 3, pady = 2);


# http://tkinter.unpythonic.net/wiki/VerticalScrolledFrame
class VerticalScrolledFrame (Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling
    """

    canvas = None;
    name = "";

    def __init__ (self, parent, _name, *args, **kw):
        Frame.__init__ (self, parent, *args, **kw)
        self.name = _name;

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar (self, orient = VERTICAL)
        vscrollbar.pack (fill = Y, side = RIGHT, expand = FALSE)
        canvas = Canvas (self, bd = 0, highlightthickness = 0,
                         yscrollcommand = vscrollbar.set)
        canvas.pack (side = LEFT, fill = BOTH, expand = TRUE)
        vscrollbar.config (command = canvas.yview)

        # reset the view
        canvas.xview_moveto (0)
        canvas.yview_moveto (0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame (canvas)
        interior_id = canvas.create_window (0, 0, window = interior,
                                            anchor = NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior (event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth (), interior.winfo_reqheight ())
            canvas.config (scrollregion = "0 0 %s %s" % size)
            if interior.winfo_reqwidth () != canvas.winfo_width ():
                # update the canvas's width to fit the inner frame
                canvas.config (width = interior.winfo_reqwidth ())

        interior.bind ('<Configure>', _configure_interior)

        def _configure_canvas (event):
            if interior.winfo_reqwidth () != canvas.winfo_width ():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure (interior_id, width = canvas.winfo_width ())

        canvas.bind ('<Configure>', _configure_canvas)

        self.canvas = canvas;
        scrollable.append(self)


scrollable = []
def _on_mousewheel (event):
    for vertScroll in scrollable:
        if (nb.tab(nb.select(), "text") == vertScroll.name):
            vertScroll.canvas.yview_scroll (int(-1 * (event.delta / 120)), "units")


root = InitializeRoot();
root.bind ("<MouseWheel>", _on_mousewheel)
DataHandler.SetUp(UIAddStudent, UIAddActivity, stuSearchVar, actSearchVar, HideStudent, HideActivity, ShowStudent, ShowActivity, stuCountVar, actCountVar, statsVar)
ExcelHandler.SetUp(DataHandler)
print("reached loop")
mainloop()
print("main loop ended")