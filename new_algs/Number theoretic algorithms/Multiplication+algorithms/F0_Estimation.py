from PyQt5 import QtCore, QtGui, QtWidgets
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math


class Ui_MainWindow(object):
    def __init__(self):
        super().__init__()
        self.setFundamentalFreq = None
        self.EstimatedFundamentalFreq = None

    def loadFile(self):
        dialog = QtWidgets.QFileDialog()
        self.fpath, _ = dialog.getOpenFileName(None, "Open File", "",
                                               "Excel File (*.xlsx)")
        self.filename = self.fpath.split("/")[-1]
        self.label_select_status.setText(" {0} file selected".format
                                         (self.filename))
        self.label_read_status.setText("")
        self.lineEdit_F0.setText("")
        self.label_set_sampling_freq_status.setText("Not Set")
        self.lineEdit_sampling_freq.clear()

    def readFile(self):
        df = pd.read_excel(self.fpath, header=None)
        self.inputSignal = df.as_matrix().T
        self.label_read_status.setText("File Read Successfully")

    def setSamplingFrequency(self):
        self.samplingFrequency = int(self.lineEdit_sampling_freq.text())
        self.ub = self.samplingFrequency / 3
        self.pitchBounds = np.array([1, self.ub])
        self.f = self.ub
        self.label_set_sampling_freq_status.setText("Sampling Frequency Set:{0} Hz".format(self.samplingFrequency))

    def plotInputSignal(self):
        stepTime = 1 / self.samplingFrequency
        self.N = float(len(self.inputSignal))
        self.tIndex = np.arange(0, self.N) * stepTime
        self.tIndex = np.reshape(self.tIndex, (len(self.tIndex), 1))
        self.timeDuration = self.N * stepTime
        fig1 = plt.figure(figsize=(10, 5))
        axes1 = fig1.add_axes([.1, .1, .8, .8])
        axes1.axhline(0, color='black', linestyle='-', linewidth=3)
        axes1.plot(
            self.tIndex,
            self.inputSignal,
            color='green',
            linewidth=.05,
            linestyle=' ',
            marker='o',
            markersize=2)
        axes1.plot(
            self.tIndex,
            self.inputSignal,
            color='red',
            linewidth=.5,
            linestyle='-')
#        axes1.bar(self.tIndex,self.inputSignal,bottom=0,linewidth=.15,width=0.00002,color='blue')
        axes1.set_xlim([0, self.timeDuration])
        fig1.suptitle('Sampled Signal', fontsize=16)
        plt.xlabel('Time(s)', fontsize=14)
        plt.ylabel('Amplitude', fontsize=14)
        plt.show()

    def setFundamentalFrequency(self):
        self.setFundamentalFreq = int(self.lineEdit_frequency.text())
        self.label_frequency_status.setText(
            "Frequency Set: {0} Hz".format(
                self.setFundamentalFreq))
        self.lable_generatedSignal_status.setText(" ")
        self.label_save_status.setText(" ")
        self.label_genSamplingFrequency_status.setText(" ")
        self.lable_generated_sampled_Signal_status.setText(" ")
        self.lineEdit_genSamplingfrequency.clear()

    def setgenSamplingFrequency(self):
        self.setgenSamplingFreq = int(
            self.lineEdit_genSamplingfrequency.text())
        self.label_genSamplingFrequency_status.setText(
            "Fs Set: {0} Hz".format(self.setgenSamplingFreq))

    def generateNoisyAnalogSignal(self):
        # Generate analog signal and add noise
        time_period = 1 / self.setFundamentalFreq
        cycles = 140
        self.time = time_period * cycles
        amplitude = 2
        samples = 140000
        self.t = np.linspace(0, self.time, samples, endpoint=True)
        xcont = amplitude * \
            np.sin(2 * np.pi * self.setFundamentalFreq * self.t)

        target_noise_db = 10
        # Convert to linear Watt units
        target_noise_watts = 10 ** (target_noise_db / 10)
        # Generate noise samples
        mean_noise = 0
        noise_volts = np.random.normal(
            mean_noise, target_noise_watts, len(xcont))
        self.xnoisy = xcont + noise_volts
        self.lable_generatedSignal_status.setText("Signal Generated")
#        xnoisy=xcont+1.1*np.random.uniform(low=-.1, high=1, size=len(xcont))

    def generateNoisySampledSignal(self):
        # generate a sampled noisy signal
        fs = self.setgenSamplingFreq
        ts = 1 / fs
        tempIndex = np.arange(0, self.time + ts / 2, ts)
        scalingFactor = np.round(len(self.t) / len(tempIndex))
        index = np.arange(0, len(self.t), scalingFactor).astype('int')
        self.tSampled = self.t[index]
        self.xSampled = self.xnoisy[index]
        self.lable_generated_sampled_Signal_status.setText("Signal Generated")

    def saveSignalToExcel(self):
        df = pd.DataFrame(self.xSampled.flatten())
        df = df.T
        self.fileName = self.lineEdit_Filename.text()
        self.fileName = self.fileName + ".xlsx"
        df.to_excel(self.fileName, header=False, index=False)
        self.label_save_status.setText(
            "Signal Saved as: {0}".format(
                self.fileName))

    def estinmateFundamentalFrequency(self):
        self.label_F0_calulating_status.setText("Calculating....")
        F = len(self.inputSignal)
        nFftGrid = math.ceil(F)
        minFftIndex = math.ceil(nFftGrid * self.pitchBounds[0])
        maxFftIndex = math.floor(nFftGrid * self.pitchBounds[1])
        validFftIndices = np.arange(minFftIndex, maxFftIndex, self.f)
        fullPitchGrid = validFftIndices / nFftGrid
        costFunctionMatrix = np.full(
            [1, int(np.ceil((maxFftIndex - minFftIndex) / self.f))], np.nan)
        pitchGrid = np.arange(
            minFftIndex,
            maxFftIndex + self.f,
            self.f) / nFftGrid
        nPitches = len(pitchGrid)

        for jPitch in range(0, nPitches - 1):
            pitch = pitchGrid[jPitch]
            sinusoidalMat = np.exp(1j * 2 * np.pi * pitch * self.tIndex)
            sinusoidalMatrixrealimag = np.concatenate(
                (np.real(sinusoidalMat), np.imag(sinusoidalMat)), axis=1)
            costFunctionMatrix[0,
                               jPitch] = np.real(np.matmul((np.matmul(self.inputSignal.T,
                                                                      sinusoidalMatrixrealimag)),
                                                           (np.matmul(np.linalg.pinv(sinusoidalMatrixrealimag),
                                                                      self.inputSignal))))

        index = np.argmax(costFunctionMatrix, axis=1)
        estimatedFundamentalFreq = fullPitchGrid[index]
        result = "%.2f" % estimatedFundamentalFreq[0]
        self.label_F0_calulating_status.setText(" ")
        print(result)
        self.lineEdit_F0.setText(str(result))
        fig1 = plt.figure(figsize=(10, 5))
        axes1 = fig1.add_axes([.1, .1, .8, .8])
        axes1.plot(fullPitchGrid.flatten(), costFunctionMatrix.flatten())
#        plt.xticks(np.arange(0,25000,500),np.arange(0,25000,500))
#        axes1.set_xlim([0,200])
        fig1.suptitle('F0 Estimation', fontsize=16)
        plt.xlabel('Frequency(Hz)', fontsize=14)
        plt.ylabel('NLS Cost Function', fontsize=14)
        plt.show()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(970, 764)
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox_generate = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_generate.setGeometry(QtCore.QRect(350, 20, 591, 231))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_generate.setFont(font)
        self.groupBox_generate.setObjectName("groupBox_generate")

        self.btn_set_frequency = QtWidgets.QPushButton(self.groupBox_generate)
        self.btn_set_frequency.setGeometry(QtCore.QRect(20, 65, 93, 28))
        self.btn_set_frequency.clicked.connect(self.setFundamentalFrequency)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setBold(False)
        font.setWeight(50)
        self.btn_set_frequency.setFont(font)
        self.btn_set_frequency.setObjectName("btn_set_frequency")
        self.lineEdit_frequency = QtWidgets.QLineEdit(self.groupBox_generate)
        self.lineEdit_frequency.setGeometry(QtCore.QRect(20, 30, 121, 25))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setBold(False)
        font.setWeight(50)
        self.lineEdit_frequency.setFont(font)
        self.lineEdit_frequency.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.lineEdit_frequency.setClearButtonEnabled(True)
        self.lineEdit_frequency.setObjectName("lineEdit_frequency")
        self.label_Hz_3 = QtWidgets.QLabel(self.groupBox_generate)
        self.label_Hz_3.setGeometry(QtCore.QRect(150, 30, 31, 31))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setBold(True)
        font.setWeight(75)
        self.label_Hz_3.setFont(font)
        self.label_Hz_3.setObjectName("label_Hz_3")
        self.label_frequency_status = QtWidgets.QLabel(self.groupBox_generate)
        self.label_frequency_status.setGeometry(QtCore.QRect(25, 95, 231, 21))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setBold(False)
        font.setWeight(50)
        self.label_frequency_status.setFont(font)
        self.label_frequency_status.setText("")
        self.label_frequency_status.setObjectName("label_frequency_status")

        self.lineEdit_genSamplingfrequency = QtWidgets.QLineEdit(
            self.groupBox_generate)
        self.lineEdit_genSamplingfrequency.setGeometry(
            QtCore.QRect(20, 130, 121, 25))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setBold(False)
        font.setWeight(50)
        self.lineEdit_genSamplingfrequency.setFont(font)
        self.lineEdit_genSamplingfrequency.setInputMethodHints(
            QtCore.Qt.ImhDigitsOnly)
        self.lineEdit_genSamplingfrequency.setClearButtonEnabled(True)
        self.lineEdit_genSamplingfrequency.setObjectName(
            "lineEdit_genSamplingfrequency")
        self.label_Hz_5 = QtWidgets.QLabel(self.groupBox_generate)
        self.label_Hz_5.setGeometry(QtCore.QRect(150, 125, 31, 31))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setBold(True)
        font.setWeight(75)
        self.label_Hz_5.setFont(font)
        self.label_Hz_5.setObjectName("label_Hz_5")
        self.label_genSamplingFrequency_status = QtWidgets.QLabel(
            self.groupBox_generate)
        self.label_genSamplingFrequency_status.setGeometry(
            QtCore.QRect(20, 200, 171, 16))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setBold(False)
        font.setWeight(50)
        self.label_genSamplingFrequency_status.setFont(font)
        self.label_genSamplingFrequency_status.setText("")
        self.label_genSamplingFrequency_status.setObjectName(
            "label_genSamplingFrequency_status")
        self.btn_set_genSamplingFrequency = QtWidgets.QPushButton(
            self.groupBox_generate)
        self.btn_set_genSamplingFrequency.setGeometry(
            QtCore.QRect(20, 165, 93, 28))
        self.btn_set_genSamplingFrequency.clicked.connect(
            self.setgenSamplingFrequency)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setBold(False)
        font.setWeight(50)
        self.btn_set_genSamplingFrequency.setFont(font)
        self.btn_set_genSamplingFrequency.setObjectName(
            "btn_set_genSamplingFrequency")

        self.btn_generate_signal = QtWidgets.QPushButton(
            self.groupBox_generate)
        self.btn_generate_signal.setGeometry(QtCore.QRect(210, 30, 151, 28))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setBold(False)
        font.setWeight(50)
        self.btn_generate_signal.setFont(font)
        self.btn_generate_signal.setObjectName("btn_generate_signal")
        self.btn_generate_signal.clicked.connect(
            self.generateNoisyAnalogSignal)
        self.lable_generatedSignal_status = QtWidgets.QLabel(
            self.groupBox_generate)
        self.lable_generatedSignal_status.setGeometry(
            QtCore.QRect(210, 70, 191, 21))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setBold(False)
        font.setWeight(50)
        self.lable_generatedSignal_status.setFont(font)
        self.lable_generatedSignal_status.setText("")
        self.lable_generatedSignal_status.setObjectName(
            "lable_generatedSignal")

        self.btn_generate_sampled_signal = QtWidgets.QPushButton(
            self.groupBox_generate)
        self.btn_generate_sampled_signal.setGeometry(
            QtCore.QRect(210, 130, 161, 28))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setBold(False)
        font.setWeight(50)
        self.btn_generate_sampled_signal.setFont(font)
        self.btn_generate_sampled_signal.setObjectName(
            "btn_generate_sampled_signal")
        self.btn_generate_sampled_signal.clicked.connect(
            self.generateNoisySampledSignal)
        self.lable_generated_sampled_Signal_status = QtWidgets.QLabel(
            self.groupBox_generate)
        self.lable_generated_sampled_Signal_status.setGeometry(
            QtCore.QRect(210, 170, 181, 21))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setBold(False)
        font.setWeight(50)
        self.lable_generated_sampled_Signal_status.setFont(font)
        self.lable_generated_sampled_Signal_status.setText("")
        self.lable_generated_sampled_Signal_status.setObjectName(
            "lable_generated_sampled_Signal")

        self.btn_save_to_file = QtWidgets.QPushButton(self.groupBox_generate)
        self.btn_save_to_file.setGeometry(QtCore.QRect(400, 165, 111, 28))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setBold(False)
        font.setWeight(50)
        self.btn_save_to_file.setFont(font)
        self.btn_save_to_file.setObjectName("btn_save_to_file")
        self.btn_save_to_file.clicked.connect(self.saveSignalToExcel)
        self.label_save_status = QtWidgets.QLabel(self.groupBox_generate)
        self.label_save_status.setGeometry(QtCore.QRect(360, 200, 221, 16))
        self.label_save_status.setAlignment(QtCore.Qt.AlignHCenter)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setBold(False)
        font.setWeight(50)
        self.label_save_status.setFont(font)
        self.label_save_status.setText("")
        self.label_save_status.setObjectName("label_save_status")
        self.lineEdit_Filename = QtWidgets.QLineEdit(self.groupBox_generate)
        self.lineEdit_Filename.setGeometry(QtCore.QRect(400, 130, 141, 25))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setBold(False)
        font.setWeight(50)
        self.lineEdit_Filename.setFont(font)
        self.lineEdit_Filename.setClearButtonEnabled(True)
        self.lineEdit_Filename.setObjectName("lineEdit_Filename")

        self.groupBox_load = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_load.setGeometry(QtCore.QRect(60, 20, 241, 231))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_load.setFont(font)
        self.groupBox_load.setObjectName("groupBox_load")
        self.btn_select_file = QtWidgets.QPushButton(self.groupBox_load)
        self.btn_select_file.setGeometry(QtCore.QRect(10, 30, 101, 31))
        self.btn_select_file.clicked.connect(self.loadFile)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setBold(False)
        font.setWeight(50)
        self.btn_select_file.setFont(font)
        self.btn_select_file.setObjectName("btn_select_file")
        self.label_select_file = QtWidgets.QLabel(self.groupBox_load)
        self.label_select_file.setGeometry(QtCore.QRect(10, 60, 141, 21))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setBold(True)
        font.setWeight(75)
        self.label_select_file.setFont(font)
        self.label_select_file.setObjectName("label_select_file")
        self.label_select_status = QtWidgets.QLabel(self.groupBox_load)
        self.label_select_status.setGeometry(QtCore.QRect(10, 80, 211, 20))
        font.setFamily("MS Shell Dlg 2")
        font.setBold(False)
        font.setWeight(50)
        self.label_select_status.setFont(font)
        self.label_select_status.setObjectName("label_select_status")

        self.btn_read_file = QtWidgets.QPushButton(self.groupBox_load)
        self.btn_read_file.setGeometry(QtCore.QRect(10, 130, 101, 31))
        self.btn_read_file.clicked.connect(self.readFile)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setBold(False)
        font.setWeight(50)
        self.btn_read_file.setFont(font)
        self.btn_read_file.setAcceptDrops(False)
        self.btn_read_file.setInputMethodHints(QtCore.Qt.ImhNone)
        self.btn_read_file.setFlat(False)
        self.btn_read_file.setObjectName("btn_read_file")
        self.label_read = QtWidgets.QLabel(self.groupBox_load)
        self.label_read.setGeometry(QtCore.QRect(10, 170, 121, 16))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setBold(True)
        font.setWeight(75)
        self.label_read.setFont(font)
        self.label_read.setObjectName("label_read")
        self.label_read_status = QtWidgets.QLabel(self.groupBox_load)
        self.label_read_status.setGeometry(QtCore.QRect(10, 200, 211, 16))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setBold(False)
        font.setWeight(50)
        self.label_read_status.setFont(font)
        self.label_read_status.setText("")
        self.label_read_status.setObjectName("label_read_status")

        self.groupBox_estimation = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_estimation.setGeometry(QtCore.QRect(60, 300, 881, 391))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_estimation.setFont(font)
        self.groupBox_estimation.setObjectName("groupBox_estimation")
        self.lineEdit_sampling_freq = QtWidgets.QLineEdit(
            self.groupBox_estimation)
        self.lineEdit_sampling_freq.setGeometry(QtCore.QRect(10, 30, 161, 25))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setBold(False)
        font.setWeight(50)
        self.lineEdit_sampling_freq.setFont(font)
        self.lineEdit_sampling_freq.setInputMethodHints(
            QtCore.Qt.ImhDigitsOnly)
        self.lineEdit_sampling_freq.setClearButtonEnabled(True)
        self.lineEdit_sampling_freq.setObjectName("lineEdit_sampling_freq")
        self.btn_set_sampling_freq = QtWidgets.QPushButton(
            self.groupBox_estimation)
        self.btn_set_sampling_freq.setGeometry(QtCore.QRect(10, 70, 91, 28))
        self.btn_set_sampling_freq.clicked.connect(self.setSamplingFrequency)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setBold(False)
        font.setWeight(50)
        self.btn_set_sampling_freq.setFont(font)
        self.btn_set_sampling_freq.setObjectName("btn_set_sampling_freq")
        self.label_sampling_frequency = QtWidgets.QLabel(
            self.groupBox_estimation)
        self.label_sampling_frequency.setGeometry(
            QtCore.QRect(10, 100, 221, 31))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setBold(True)
        font.setWeight(75)
        self.label_sampling_frequency.setFont(font)
        self.label_sampling_frequency.setObjectName("label_sampling_frequency")
        self.label_set_sampling_freq_status = QtWidgets.QLabel(
            self.groupBox_estimation)
        self.label_set_sampling_freq_status.setGeometry(
            QtCore.QRect(110, 75, 300, 16))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setBold(False)
        font.setWeight(50)
        self.label_set_sampling_freq_status.setFont(font)
        self.label_set_sampling_freq_status.setObjectName(
            "label_set_sampling_freq_status")

        self.btn_plot = QtWidgets.QPushButton(self.groupBox_estimation)
        self.btn_plot.setGeometry(QtCore.QRect(10, 150, 101, 28))
        self.btn_plot.clicked.connect(self.plotInputSignal)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setBold(False)
        font.setWeight(50)
        self.btn_plot.setFont(font)
        self.btn_plot.setObjectName("btn_plot")
        self.label_plot = QtWidgets.QLabel(self.groupBox_estimation)
        self.label_plot.setGeometry(QtCore.QRect(10, 190, 191, 16))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setBold(True)
        font.setWeight(75)
        self.label_plot.setFont(font)
        self.label_plot.setObjectName("label_plot")

        self.btn_calculateFundamentalFrequency = QtWidgets.QPushButton(
            self.groupBox_estimation)
        self.btn_calculateFundamentalFrequency.setGeometry(
            QtCore.QRect(10, 240, 93, 28))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setBold(False)
        font.setWeight(50)
        self.btn_calculateFundamentalFrequency.setFont(font)
        self.btn_calculateFundamentalFrequency.setObjectName(
            "btn_calculateFundamentalFrequency")
        self.btn_calculateFundamentalFrequency.clicked.connect(
            self.estinmateFundamentalFrequency)
        self.label_calculate_fundamental = QtWidgets.QLabel(
            self.groupBox_estimation)
        self.label_calculate_fundamental.setGeometry(
            QtCore.QRect(10, 270, 331, 31))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setBold(True)
        font.setWeight(75)
        self.label_calculate_fundamental.setFont(font)
        self.label_calculate_fundamental.setObjectName(
            "label_calculate_fundamental")
        self.label_estimated_Fundamental = QtWidgets.QLabel(
            self.groupBox_estimation)
        self.label_estimated_Fundamental.setGeometry(
            QtCore.QRect(10, 320, 291, 31))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setBold(True)
        font.setWeight(75)
        self.label_estimated_Fundamental.setFont(font)
        self.label_estimated_Fundamental.setObjectName(
            "label_estimated_Fundamental")
        self.label_Hz = QtWidgets.QLabel(self.groupBox_estimation)
        self.label_Hz.setGeometry(QtCore.QRect(180, 27, 31, 31))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setBold(True)
        font.setWeight(75)
        self.label_Hz.setFont(font)
        self.label_Hz.setObjectName("label_Hz")
        self.label_F0_calulating_status = QtWidgets.QLabel(
            self.groupBox_estimation)
        self.label_F0_calulating_status.setGeometry(
            QtCore.QRect(130, 245, 161, 16))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setBold(False)
        font.setWeight(50)
        self.label_F0_calulating_status.setFont(font)
        self.label_F0_calulating_status.setObjectName(
            "label_F0_calulating_status")
        self.lineEdit_F0 = QtWidgets.QLineEdit(self.groupBox_estimation)
        self.lineEdit_F0.setGeometry(QtCore.QRect(300, 323, 91, 30))
        self.lineEdit_F0.setReadOnly(True)
        self.lineEdit_F0.setObjectName("lineEdit_F0")
        self.label_Hz_2 = QtWidgets.QLabel(self.groupBox_estimation)
        self.label_Hz_2.setGeometry(QtCore.QRect(400, 320, 31, 31))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setBold(True)
        font.setWeight(75)
        self.label_Hz_2.setFont(font)
        self.label_Hz_2.setObjectName("label_Hz_2")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 823, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(
            _translate(
                "MainWindow",
                "Fundamental Frequency Estimation"))
        self.groupBox_generate.setTitle(_translate(
            "MainWindow", "Generate Noisy Signal"))
        self.btn_set_frequency.setText(_translate("MainWindow", "Set"))
        self.lineEdit_frequency.setPlaceholderText(
            _translate("MainWindow", "Frequency F0"))
        self.label_Hz_3.setText(_translate("MainWindow", "Hz"))
        self.btn_generate_signal.setText(_translate(
            "MainWindow", "Generate Analog Signal"))
        self.btn_save_to_file.setText(
            _translate("MainWindow", "Save To Excel"))
        self.lineEdit_Filename.setPlaceholderText(
            _translate("MainWindow", "Filename"))
        self.groupBox_load.setTitle(
            _translate(
                "MainWindow",
                "Load Noisy Signal File"))
        self.btn_select_file.setText(_translate("MainWindow", "Select File"))
        self.label_select_file.setText(
            _translate("MainWindow", "Choose Excel File"))
        self.label_select_status.setText(
            _translate("MainWindow", "No file selected"))
        self.btn_read_file.setText(_translate("MainWindow", "Read File"))
        self.label_read.setText(_translate("MainWindow", "Read Excel File"))
        self.label_read_status.setText(_translate("MainWindow", " "))
        self.groupBox_estimation.setTitle(
            _translate("MainWindow", "Estimation"))
        self.lineEdit_sampling_freq.setPlaceholderText(
            _translate("MainWindow", "Sampling Frequency"))
        self.btn_set_sampling_freq.setText(_translate("MainWindow", "Set "))
        self.btn_plot.setText(_translate("MainWindow", "Plot"))
        self.label_plot.setText(
            _translate(
                "MainWindow",
                "Display Measured Signal"))
        self.label_sampling_frequency.setText(_translate(
            "MainWindow", "Enter the sampling frequency"))
        self.btn_calculateFundamentalFrequency.setText(
            _translate("MainWindow", "Calculate F0"))
        self.label_calculate_fundamental.setText(_translate(
            "MainWindow", "Calculate Estimated Fundamental Frequency"))
        self.label_estimated_Fundamental.setText(_translate(
            "MainWindow", "Estimated Fundamental frequency (F0):"))
        self.label_set_sampling_freq_status.setText(
            _translate("MainWindow", "Not Set"))
        self.label_Hz.setText(_translate("MainWindow", "Hz"))
        self.label_Hz_2.setText(_translate("MainWindow", "Hz"))
        self.lineEdit_genSamplingfrequency.setPlaceholderText(
            _translate("MainWindow", "Sampling Frequency"))
        self.label_Hz_5.setText(_translate("MainWindow", "Hz"))
        self.btn_set_genSamplingFrequency.setText(
            _translate("MainWindow", "Set "))
        self.btn_generate_sampled_signal.setText(
            _translate("MainWindow", "Generate Sampled Signal"))
        self.lable_generated_sampled_Signal_status.setText(
            _translate("MainWindow", " "))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    app.exec_()
    app.aboutToQuit.connect(app.deleteLater)
