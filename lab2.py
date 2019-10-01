# Shania Ie and Pooja Pathak
# lab 2
# CIS 41B

# Description:
# Lab2.py handles all the GUI. It is responsible for the interaction between the user and the application.
# There are 3 main windows, a main window, a dialog window and a plot window. It plots what ever data the
# user wants to see

# Extra Credit:
# We believe that it is best to live in Cupertino, judging from the percentage increase over the years. 
# Although it is pricier than Gilroy, however the increase has always been very steady. However, if we
# were looking for something that is really cheap, Gilroy would be the best solution. Yet, this also comes
# with the fact that you are far from the center of Silicon Valley and commute would be a hassle. 

import matplotlib
matplotlib.use('TkAgg')
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import tkinter.messagebox as tkmb

from rent import Rent

class MainWindow(tk.Tk):
    def __init__ (self, *args, **kwargs):
        '''
        Consturctor:
        The constructor inherits the tkinter class. It checks whether the input file is correct, if not then it will
        prompt the error message box. Creates 2 buttons, 1 for plotting the trend and the other for plotting the percent
        increase.
        '''
        super().__init__(*args, **kwargs)
        
        self.FileError = False
        try:
            self.r = Rent()
            self.cities = self.r.cityList
            self.cities.append("All")
            self.title('Rent Data')
            
            tk.Label(self,text='Rent Data for Santa Clara Country',fg = 'blue',font = ('Calibri',20)).grid(row = 0, columnspan = 2)
            tk.Button(self,text='Trend over Time', command=self._plotTrend).grid(row = 1, column = 0)
            tk.Button(self,text='Percent Change', command=self._plotChange).grid(row = 1, column = 1)
        
        except FileNotFoundError as c:
            state = tkmb.showerror("Error", "can't open " + str(c), parent=self)
            self.FileError = True
                
        except IOError as e:
            tkmb.showerror("Error", "can't open " + str(e), parent=self)
            self.FileError = True
            
    def _plotTrend(self):
        '''_plotTrend: Prompts the radio dialog window and passes the trend graph to the plot window'''
        dialog = RadioDialogWindow(self.cities)
        self.wait_window(dialog)
        returnVal = dialog.getControlVar()
        if returnVal != -1:
            pwin = PlotWin(self.r.plotRentalPrice, returnVal)
    
    def _plotChange(self):
        '''_plotChange: Passes the percent change graph to the plot window'''
        pwin = PlotWin(self.r.plotPercentIncrease, -1)
    
class RadioDialogWindow(tk.Toplevel):
    def __init__(self, cities, *args, **kwargs):
        '''
        Constructor:
        Creates radio buttons for each of the cities in the data file.
        The radio buttons are in one column. 
        Pre-select the first button for the user.
        '''
        super().__init__(*args, **kwargs)
        self.title("Choose City")
        self.geometry("400x400")
        self.focus_set()
        self.grab_set()
        self.transient(*args,**kwargs)
        self.choice = tk.StringVar()
        self.choice.set(cities[0])
        self.controlVar = -1 
        self.radioButtons = [tk.Radiobutton(self, text = city, variable = self.choice, value = city)for city in cities]
        for rb in self.radioButtons:
            rb.grid(sticky='w')
        tk.Button(self, text='Plot', command= lambda:self._chosenCity(cities)).grid() 
    
    def _chosenCity(self, cities):
        '''_chosenCity: finds the index of the city in the list'''
        self.controlVar = cities.index(self.choice.get())
        self.destroy()
    
    def getControlVar(self):
        '''getControlVar: Returns the index of the city'''
        return self.controlVar

class PlotWin(tk.Toplevel):
    def __init__(self, func, returnVal, *args, **kwargs):
        super().__init__(*args, **kwargs)
        '''
        Constructor: 
        Plots the appropriate graph according to the function passed in from main window class
        '''
        if returnVal == -1:
            fig = plt.figure(figsize=(7,8.5))
            func()
        else:
            fig = plt.figure(figsize=(6,8))
            func(returnVal)
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.get_tk_widget().grid()
        canvas.draw()

def main():
    win = MainWindow()
    if not win.FileError:
        win.mainloop()

main()
