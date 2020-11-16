from tkinter import *
from operations import *
from register import Register


class AddForm:
    number_of_bits = 8

    def __init__(self, sw):
        self.sw = sw
        self.root = Tk()
        self.root.title("Addition" if sw == 1 else "Subtraction")
        self.txt1 = Entry(self.root)
        self.txt2 = Entry(self.root)
        self.calculate = Button(self.root, text="Calculate", command=self.calculate)
        self.resultLabel = Label(self.root, text="Result")

        self.txt1.pack()
        self.txt2.pack()
        self.calculate.pack()
        self.resultLabel.pack()
        self.root.mainloop()

    def calculate(self):
        n1 = int(self.txt1.get())
        n2 = int(self.txt2.get())

        if n1 > 255 or n2 > 255:
            self.resultLabel.config(text="INVALID NUMBER")
            return

        n1_binary = to_binary(n1, self.number_of_bits)
        n2_binary = to_binary(n2, self.number_of_bits)

        reg_a = Register("A", n1_binary)
        reg_b = Register("B", n2_binary)

        result, overflow = add_with_overflow(reg_a.value, reg_b.value if self.sw == 1 else comp(reg_b.value))
        # reg_a.value = result

        self.resultLabel.config(text=result)

        print('RESULT=' + result)
        reg_a.print_value()
        reg_b.print_value()
        print('OF=' + overflow)
