from tkinter import *
from operations import *
from register import Register


class DivForm:
    reg_a = Register('A')
    reg_q = Register('Q')
    reg_m = Register('M')
    count = 0
    cycle = 1

    def __init__(self):
        self.root = Tk()
        self.root.title("Division")
        self.txt1 = Entry(self.root)
        self.txt2 = Entry(self.root)
        self.calculateBtn = Button(self.root, text="Start", command=self.calculate)
        self.nextBtn = Button(self.root, text="Next Cycle", command=self.cal_next_step)
        self.resultLabel = Label(self.root, text="A       Q       M\n")

        self.txt1.pack()
        self.txt2.pack()
        self.calculateBtn.pack()
        self.nextBtn.pack()
        self.resultLabel.pack()
        self.nextBtn.config(state=DISABLED)
        self.root.mainloop()

    def calculate(self):
        self.calculateBtn.config(state=DISABLED)
        self.nextBtn.config(state=NORMAL)
        n1 = int(self.txt1.get())
        n2 = int(self.txt2.get())

        self.count = count(max(abs(n1), abs(n2)), 1)

        n1_binary = to_binary(n1, self.count)
        n2_binary = to_binary(n2, self.count)
        self.reg_q.value = n1_binary
        self.reg_m.value = n2_binary
        self.reg_a.value = '0'

        self.printAll()

    def cal_next_step(self):
        self.resultLabel.config(text=self.resultLabel.cget('text') + '--------------------- ')
        self.resultLabel.config(text=self.resultLabel.cget('text') + '\n      Cycle #' + str(self.cycle) + '\n')
        self.cycle += 1

        self.reg_a.value, self.reg_q.value = shift_left(self.reg_a.value, self.reg_q.value)
        self.reg_a.print_value()
        self.reg_a.value = sub(self.reg_a.value, self.reg_m.value)
        self.reg_a.print_value()
        if is_less_than_zero(self.reg_a.value):
            self.reg_q.value = self.reg_q.value[:-1] + '0'  # Q0=0
            self.reg_a.value = add_with_overflow(self.reg_a.value, self.reg_m.value)[0]
        else:
            self.reg_q.value = self.reg_q.value[:-1] + '1'  # Q0 =1
        self.count -= 1

        self.printAll()

        if self.count == 0:
            self.nextBtn.config(state=DISABLED)

    def printAll(self):
        self.reg_a.print_value()
        self.reg_q.print_value()
        self.reg_m.print_value()
        result = self.reg_a.value + '    ' + self.reg_q.value + '     ' + self.reg_m.value + '\n'
        self.resultLabel.config(text=self.resultLabel.cget('text') + result)
