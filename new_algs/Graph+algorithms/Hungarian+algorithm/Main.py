from tkinter import *
from tkinter import messagebox
from hungarian_algorithm.main import Munkres

tk = Tk()

matrixInputs = []

def updateMatrixInputs():
    global matrixInputs

    for row in matrixInputs:
        for item in row:
            item.grid_forget()

    matrixInputs = []

    if(len(sizeXInput.get()) == 0 and len(sizeYInput.get()) == 0):
        messagebox.showerror("Warning", "Matrix size cannot be null")
    elif(sizeXInput.get().isdigit() == False or sizeYInput.get().isdigit() == False):
        messagebox.showerror("Warning", "Matrix size must be number")
    else:
        sizeX = int(sizeXInput.get())
        sizeY = int(sizeYInput.get())

        for i in range(sizeY):
            matrixInputs.append([])
            for j in range(sizeX):
                matrixInputs[i].append(Entry(tk))
                matrixInputs[i][j].grid(row = i + 2, column = j)

def calculateOptimalCost():
    costs = []

    for i, row in enumerate(matrixInputs):
        
        costs.append([])
        for item in row:
            if(len(item.get()) == 0 or item.get().isdigit() == False):
                costs[i].append(0)
                item.delete(0, len(item.get()))
                item.insert(0, 0)
            else:
                costs[i].append(float(item.get()))

    costs = Munkres(costs)
    costs.calculate()

    sum, values = costs.getResult()
    messagebox.showinfo("Information", "The optimal value equals: " + str(sum) + "\nValues: " + str(values))
    
    del costs
    tk.destroy()

Label(text = "Matrix size (X x Y):").grid(row = 0, column = 0)
sizeXInput = Entry(tk)
sizeXInput.grid(row = 0, column = 1)
Label(text = "x").grid(row = 0, column = 2)
sizeYInput = Entry(tk)
sizeYInput.grid(row = 0, column = 3)

createMatrixBtn = Button(text = "Create matrix / Clear", command = updateMatrixInputs)
createMatrixBtn.grid(row = 0, column = 4)

calculateBtn = Button(text = "Calculate", command = calculateOptimalCost)
calculateBtn.grid(row = 0, column = 5)

Label(text = "").grid(row = 1, column = 0)

tk.mainloop()