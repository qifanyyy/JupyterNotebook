__author__ = 'AlexLlamas'
from Tkinter import *
from samples import Samples
from CorrelationMesures import *
import matplotlib.pyplot as plt
import sympy as sym
from scipy.optimize import curve_fit

def colocar_scrollbar(listbox,scrollbar):
    scrollbar.config(command=listbox.yview)
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)
    listbox.pack(side=LEFT, fill=Y)


def cargarlistbox(lista,listbox):
    ind,largo=0,len(lista)
    while ind < largo:
        listbox.insert(END,lista[ind])
        ind += 1


def case_function(samples, obj):
    sam = Samples()
    print samples
    numBinx, numBiny = Binx.get(), Biny.get()
    #numBinx = 30
    #numBiny = 30
    print numBinx, numBiny
    print numBinx
    x, y = samples[:, 0], samples[:, 1]
    MI = mutual_info(x, y, numBinx, numBiny)
    ex = entropy(x, numBinx)
    ey = entropy(y, numBiny)
    R = norm_MI(x, y, numBinx, numBiny)
    rxy = pearson_corr(x, y)
    exy = entropyx_y(x, y, numBinx, numBiny)
    eyx = entropyx_y(y, x, numBinx, numBiny)
    MIE = MI_Entropy(x, y, numBinx, numBiny)
    Ixy = propuesta_Ixy(x, y, numBinx, numBiny)
    Iyx = propuesta_Iyx(x, y, numBinx, numBiny)
    Ixy2 = propuesta2_Ixy(x, y, numBinx, numBiny)
    Iyx2 = propuesta2_Iyx(x, y, numBinx, numBiny)
    PMD = propuesta_mutual_dependency(x, y, numBinx, numBiny)
    PMD2 = propuesta2_mutual_dependency(x,y, numBinx, numBiny)
    # d_cor = d_corr(x,y)
    # Mic = MIC(x,y)

    mitexto.set('Entropy of x: ' + str(ex) + '\n'+
                'Entropy of y: ' + str(ey) + '\n' +
                'Mutual information: ' + str(MI) + '\n' +
                'Mutual info with entropy: ' + str(MIE) + '\n' + '\n' +

                '(Max=1)Normalized Mutual info: '+ str(R) + '\n' +
                '(Max=1)Pearson Correlation: ' + str(rxy) + '\n' +
                # '(Max=1)Distance Correlation: ' + str(d_cor) + '\n' +
                # '(Max=1)MIC: ' + str(Mic) + '\n' +
                '(Max=1)Mutual Dependency: ' + str(PMD) + '\n'  +
                '(Max=1)Mutual Dependency2: ' + str(PMD2) + '\n' + '\n' +

                'Entropy of X|Y = ' + str(exy) + '\n' +
                'Entropy of Y|X = ' + str(eyx)+ '\n' +
                '(Max=1)Information in Y of X: ' + str(Ixy) + '\n' +
                '(Max=1)Information in X of Y: ' + str(Iyx) + '\n' +
                '(Max=1)Information2 in Y of X: ' + str(Ixy2) + '\n' +
                '(Max=1)Information2 in X of Y: ' + str(Iyx2))

    if plot_sample.get():
        sam.plot_sample(samples, numBinx, numBiny, step.get())
    if plot_compare.get():
        obj.plot_compare2(numBinx, numBiny, noise.get(), step.get())
    if plot_propuse.get():
        sam.plot_propose(samples, numBinx)
    if plot_partition.get():
        sam.plot_partition(samples, numBinx, numBiny)
    if plot_converge_in_samples.get():
        Converge_in_samples(numBinx, numBiny, obj)
    if samples_check.get():
        samples_grid(numBinx, numBiny)



def func(x,a,b,c,d):
    return (a/(b*x+c))+d


def invfunc(y,a,b,c,d):
    return (a/float(b*(y-d))) - (c/float(b))

def samples_grid(numBinx, numBiny):
        sig = 0.99  # significancia
        v = 10 # muestras por bloque deseadas 5 para squere
        samPerBlock =  (v*sig)/math.sqrt(1-math.pow(sig,2))
        numSamples = int(numBinx*numBiny*samPerBlock)
        print 'The number of samples needed for a significance of ' + str(sig) +  'with v = ' + str(v) + 'Binx = ' + str(numBinx) + 'Biny= ' + str(numBiny) + 'is...: ' + str(numSamples)


def Converge_in_samples(numBinx, numBiny, obj):

    # this function plot the measures with different number of samples
    # the objective of this function is find converge in the measures
    # this is, adding more samples does not change or change very litle the measur.

    converge_value_PMD = 0.631995917246
    converge_value_PMD2 = 0.346874335815
    converge_value_R = 0.0607182686559

    ini = 150 # initial number of samples
    end = numberSam.get()
    stepi = step.get()
    size = ((end - ini)/stepi)
    PMD = np.zeros(size)
    PMD2 = np.zeros(size)
    R = np.zeros(size)

    r_PMD = np.zeros(size)
    r_PMD2 = np.zeros(size)
    r_R = np.zeros(size)
    axis = np.zeros(size)
    k = 0
    for i in range(ini, end, stepi):
        samples = obj.get(i, noise.get())
        x, y = samples[:, 0], samples[:, 1]
        PMD[k] = propuesta_mutual_dependency(x, y, numBinx, numBiny)
        PMD2[k] = propuesta2_mutual_dependency(x, y, numBinx, numBiny)
        R[k] = norm_MI(x, y, numBinx, numBiny)
        axis[k] = i
        k += 1

    fig6 = plt.figure(6)
    plt.plot(axis, PMD, 'r-')
    plt.plot(axis, PMD2, 'g-')
    plt.plot(axis, R, 'b-')

    popt_PMD, pcov = curve_fit(func, axis, PMD)
    popt_PMD2, pcov = curve_fit(func, axis, PMD2)
    popt_R, pcov = curve_fit(func, axis, R)

    plt.plot(axis, func(axis,*popt_PMD), 'r-')
    plt.plot(axis, func(axis,*popt_PMD2), 'g-')
    plt.plot(axis, func(axis,*popt_R), 'b-')

    plt.xlabel('Number of samples')
    plt.ylabel('Mutual Dependency uniform (red) | Mutual Dependency p(x) (green) | mutual information (blue)' )
    plt.ylim((0,1))
    fig6.show()

    # ----------------- fin converge values --------------------------------------------------------
    a = popt_PMD[0]
    b = popt_PMD[1]
    c = popt_PMD[2]
    e = 1                 # variacion entre muestras i.e. X_2 = X_1 + e. Entre mayor sea e mas tarda en converger.
    eps = 0.00001         # si el resultado de evaluar f(X_2)- f(X_1) = eps, entonces converge. Entre menor se eps mas tarda en converger.

    PMDx = ((-(((pow(b,2))*e)+(2*b*c)) + pow(((((pow(b,2))*e)+(2*b*c)) - ((4*(pow(b,2)))*((b*c*e) + pow(c,2) - (a*b*e/eps)))),0.5))/float(2*pow(b,2)))

    a = popt_PMD2[0]
    b = popt_PMD2[1]
    c = popt_PMD2[2]

    PMD2x = ((-(((pow(b,2))*e)+(2*b*c)) + pow(((((pow(b,2))*e)+(2*b*c)) - ((4*(pow(b,2)))*((b*c*e) + pow(c,2) - (a*b*e/eps)))),0.5))/float(2*pow(b,2)))

    a = popt_R[0]
    b = popt_R[1]
    c = popt_R[2]

    Rx = ((-(((pow(b,2))*e)+(2*b*c)) + pow(((((pow(b,2))*e)+(2*b*c)) - ((4*(pow(b,2)))*((b*c*e) + pow(c,2) - (a*b*e/eps)))),0.5))/float(2*pow(b,2)))

    # ------------------------------------------------------------------------------------------------------------------

    print '----------------------------------------------------------------------'
    print 'Number of samples to converge in UMD (red): ' + str(PMDx)
    print 'value of converge for UMD: ' + str(func(PMDx,*popt_PMD))

    print 'Number of samples to converge in CMD (green): ' + str(PMD2x)
    print 'value of converge for CMD: ' + str(func(PMD2x,*popt_PMD2))

    print 'Number of samples to converge in MI (blue): ' + str(Rx)
    print 'value of converge for MI: ' + str(func(PMDx,*popt_R))

    print '----------------------------------------------------------------------'

    print 'Number of samples to get a converge value of ' + str(converge_value_PMD) + ' in UMD is: ' + str(invfunc(converge_value_PMD, *popt_PMD)) + 'ASB, ' + str(numBinx) + 'x' +str(numBiny) + ': '+ str(invfunc(converge_value_PMD, *popt_PMD)/float(numBinx*numBiny))

    print 'Number of samples to get a converge value of ' + str(converge_value_PMD2) + ' in CMD is: ' + str(invfunc(converge_value_PMD2, *popt_PMD2)) + 'ASB, ' + str(numBinx) + 'x' +str(numBiny) + ': '+ str(invfunc(converge_value_PMD2, *popt_PMD2)/float(numBinx*numBiny))

    print 'Number of samples to get a converge value of ' + str(converge_value_R) + ' in MI is: ' + str(invfunc(converge_value_R, *popt_R)) + 'ASB, ' + str(numBinx) + 'x' +str(numBiny) + ': '+ str(invfunc(converge_value_R, *popt_R)/float(numBinx*numBiny))

def plot_select():
    ind = list1.curselection()
    if list1.curselection() != ():

        if ind[0] == 0:
            sam = Samples(tipo=0)
            samples = sam.get_sin(numberSam.get(), noise.get())
            case_function(samples, sam)
        elif ind[0] == 1:
            sam = Samples(tipo=1)
            samples = sam.get_square(numberSam.get(), noise.get())
            case_function(samples, sam)
        elif ind[0] == 2:
            sam = Samples(tipo=2)
            samples = sam.get_blur(numberSam.get(), noise.get())
            case_function(samples, sam)
        elif ind[0] == 3:
            sam = Samples(tipo=3)
            samples = sam.get_cuadratic(numberSam.get(), noise.get())
            case_function(samples, sam)
        elif ind[0] == 4:
            sam = Samples(tipo=4)
            samples = sam.get_diagonal_line(numberSam.get(), noise.get())
            case_function(samples, sam)
        elif ind[0] == 5:
            sam = Samples(tipo=5)
            samples = sam.get_horizontal_line(numberSam.get(), noise.get())
            case_function(samples, sam)
        elif ind[0] == 6:
            sam = Samples(tipo=6)
            samples = sam.get_vertical_line(numberSam.get(), noise.get())
            case_function(samples, sam)
        elif ind[0] == 7:
            sam = Samples(tipo=7)
            samples = sam.get_x(numberSam.get(), noise.get())
            case_function(samples, sam)
        elif ind[0] == 8:
            sam = Samples(tipo=8)
            samples = sam.get_circle(numberSam.get(), noise.get())
            case_function(samples, sam)
        elif ind[0] == 9:
            sam = Samples(tipo=9)
            samples = sam.get_curve_x(numberSam.get(), noise.get())
            case_function(samples, sam)
        elif ind[0] == 10:
            sam = Samples(tipo=10)
            samples = sam.get_diagonal_line2(numberSam.get(), noise.get())
            case_function(samples, sam)
        elif ind[0] == 11:
            sam = Samples(tipo=11)
            samples = sam.get_dependent(numberSam.get())
            case_function(samples, sam)
        elif ind[0] == 12:
            sam = Samples(tipo=12)
            samples = sam.get_independent(numberSam.get())
            case_function(samples, sam)
        elif ind[0] == 13:
            sam = Samples(tipo=13)
            samples = sam.get_corr(numberSam.get(), noise.get())
            case_function(samples, sam)
        elif ind[0] == 14:
            sam = Samples(tipo=14)
            samples = sam.get_file()
            case_function(samples, sam)
        else:
            mitexto.set('Error')
    else:
        mitexto.set('Select a type')

# Constants

# Principal Window
v0=Tk()
v0.minsize(width=300, height=400)

# Listbox ---------------------------------
frame1=Frame(v0)
frame1.pack()
scroll1=Scrollbar(frame1)
list1=Listbox(frame1)
list1.pack()
colocar_scrollbar(list1,scroll1)
ListaNombres = ['Sinusoidal', 'Uniform', 'Blur', 'Quadratic', 'Diagonal line 1', 'Horizontal line', 'Vertical line', 'X line',
                'Circle', 'X curve', 'Diagonal line 2', 'Dependent', 'Independent', 'Correlated', 'File']
cargarlistbox(ListaNombres,list1)
# ------------------------------------------

# Other variables --------------------------
mitexto = StringVar()
label1 = Label(v0,textvar=mitexto).pack()

b1=Button(v0,text="Calculate",command=lambda: plot_select()).pack()


# Noise variable -------------------
noise = DoubleVar(value=0.2)
e1 = Entry(v0,textvar=noise).pack()

# Number of samples variable --------
numberSam = IntVar(value=10050)
e2 = Entry(v0,textvar=numberSam).pack()

binvalue = 30
Binx = IntVar(value=binvalue)
e3 = Entry(v0,textvar=Binx).pack()

Biny = IntVar(value=binvalue)
e4 = Entry(v0,textvar=Biny).pack()

step = IntVar(value=50)
e5 = Entry(v0,textvar=step).pack()

plot_sample = IntVar(value=0)
c1 = Checkbutton(v0, text="Plot Sample structure?", variable=plot_sample).pack()

plot_compare = IntVar(value=0)
c2 = Checkbutton(v0, text="Plot Comparative?", variable=plot_compare).pack()

plot_propuse = IntVar(value=0)
c3 = Checkbutton(v0, text="Plot UMD for Grids ixi?", variable=plot_propuse).pack()

plot_partition = IntVar(value=0)
c4 = Checkbutton(v0, text="Plot histogram of the structure?", variable=plot_partition).pack()

plot_converge_in_samples = IntVar(value=0)
c5 = Checkbutton(v0, text="Plot Converge in samples?", variable=plot_converge_in_samples).pack()

samples_check = IntVar(value=0)
c6 = Checkbutton(v0, text="Calculate samples for the grid?", variable=samples_check).pack()
# ----------------------------------------------

v0.mainloop()