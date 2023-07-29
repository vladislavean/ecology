from tkinter import *
from tkinter import ttk
import tkinter
from getLinks import GetLinks
from tkinter import filedialog as fd
import writeToExcel
import parser_1
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class App:
    def __init__(self):
        self.root = Tk()
        self.root.title("Parser")
        self.root.geometry("270x180") 
        self.selectState = "Виктория"
        self.file_name = ""
        self.stationList = GetLinks().getStationsLinks()

    def _createLables(self):
        label1 = ttk.Label(text="Выберите штат: ").place(x=10, y=10)
        
    
    def _createCombobox(self):
        data = self.stationList
        
        def selectedStateE(event):
            self.selectState = comboboxStates.get()
        
        var = StringVar()
        states = list(data.keys())
        comboboxStates = ttk.Combobox(self.root, textvariable = var, values=states)
        comboboxStates['state'] = 'readonly'
        comboboxStates.pack(fill='x',padx= 5, pady=5)
        comboboxStates.current(1)
        comboboxStates.place(x=10, y=30)
        comboboxStates.bind("<<ComboboxSelected>>", selectedStateE)
        
    def _createButtons(self):
        def clickFunc():
            file_name = fd.askopenfilename()
            self.file_name = file_name
            fileNameLabel = ttk.Label(text=file_name).place(x=10, y=140)
            
        selectBtn = ttk.Button(text="Выбрать файл", command=clickFunc)
        selectBtn.place(x=100, y=110)
        
        def buildAPlot(getDict):
            plt.switch_backend('TkAgg')
            fig = plt.Figure(figsize=(15, 6), dpi=100)
            ax = fig.add_subplot(111)
            x = []
            y = []
            for year, value in getDict[self.selectState][0].items():
                x.append(year)
                y.append(value[1])
            ax.plot(x, y, label=f'{self.selectState}')
            ax.set_xticks(x)
            ax.set_xticklabels(x, rotation=45)
            ax.grid()
            ax.legend()
            
            graph = Tk()
            graph.title("Plot")
            canvas = FigureCanvasTkAgg(fig, master=graph)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
            
        
        def startFunc():
            getDict = parser_1.Parser(self.selectState, self.stationList).getStateTemps()
            #
            writeToExcel.WriteToExcel(getDict, self.file_name, self.selectState).write()
            print(getDict)
            buildAPlot(getDict)
            
        startBtn = ttk.Button(text="Построить", command = startFunc)
        startBtn.place(x=10, y=110)
        
    def startApp(self):
        self._createLables()
        self._createCombobox()
        self._createButtons()
        self.root.mainloop()
        
app = App()
app.startApp()