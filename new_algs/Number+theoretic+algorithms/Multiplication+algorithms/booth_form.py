from tkinter import *
from operations import *
from register import Register


class BoothForm:
    reg_a = Register('A')
    reg_q = Register('Q')
    reg_m = Register('M')
    count = 0
    q_1 = '0'

    cycle = 1

    def __init__(self):
        self.root = Tk()
        self.root.title("Booth")
        self.txt1 = Entry(self.root)
        self.txt2 = Entry(self.root)
        self.calculateBtn = Button(self.root, text="Start", command=self.calculate)
        self.nextBtn = Button(self.root, text="Next Step", command=self.cal_next_step)
        self.resultLabel = Label(self.root, text="A      Q     Q-1      M\n")

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

        sign = 1 if n1 + n2 > 0 else 0
        self.count = count(max(abs(n1), abs(n2)), sign)

        n1_binary = to_binary(n1, self.count)
        n2_binary = to_binary(n2, self.count)

        self.reg_q.value = n1_binary
        self.reg_m.value = n2_binary
        self.reg_a.value = '0'

        self.reg_a.value = self.reg_a.value.zfill(self.count)
        self.reg_q.value = self.reg_q.value.zfill(self.count)
        self.reg_m.value = self.reg_m.value.zfill(self.count)

        self.print_all()

    def cal_next_step(self):
        self.resultLabel.config(text=self.resultLabel.cget('text') + '--------------------- ')
        self.resultLabel.config(text=self.resultLabel.cget('text') + '\n      Cycle #' + str(self.cycle) + '\n')
        self.cycle += 1
        q0 = self.reg_q.value[-1]
        if q0 + self.q_1 == '01':
            self.reg_a.value = add_with_overflow(self.reg_a.value, self.reg_m.value)[0]
            self.print_all()
        elif q0 + self.q_1 == '10':
            self.reg_a.value = sub(self.reg_a.value, self.reg_m.value)
            self.print_all()
        self.reg_a.value, self.reg_q.value, self.q_1 = arith_shift_right(self.reg_a.value, self.reg_q.value)
        self.count -= 1

        self.print_all()
        if self.count == 0:
            self.nextBtn.config(state=DISABLED)

    def print_all(self):
        self.reg_a.print_value()
        self.reg_q.print_value()
        self.reg_m.print_value()
        print(self.q_1)
        result = self.reg_a.value + '    ' + self.reg_q.value + '     ' + self.q_1 + '     ' + self.reg_m.value + '\n'
        self.resultLabel.config(text=self.resultLabel.cget('text') + result)
