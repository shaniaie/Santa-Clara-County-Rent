# Shania Ie and Pooja Pathak
# Lab 2
# CIS 41B

# Description:
# Rent.py reads in the data from the file, sorts it out and stores it in the appropriate data structure.
# It also calculates the mean of the rental price over the years and the percentage increase from year
# to year. Then it plots the appropriate graph for each specification.

import csv
import numpy as np
import matplotlib.pyplot as plt

fname = 'lab2cities.txt'
csvfname = 'lab2prices.csv'

def showNums(f):
    '''ShowNums: Prints to the output screen the return value of the function.'''
    def wrapper(*args,**kwargs):
        result = f(*args,**kwargs)
        print(result)
        return result
    return wrapper

class Rent:
    def __init__(self):
        '''
        Contructor: 
        Read the city names into a list and read the rental prices into a numpy array.
        Check for file open error and raise an appropriate exception. Create 2 class variables: 
        a start year of 2011 and an end year of 2018. Create a numpy array to store the mean values
        '''
        try:
            with open(fname) as inFile:
                self.cityList = [line.rstrip() for line in inFile]
        except FileNotFoundError:
            raise FileNotFoundError(fname)
        
        try:     
            self.rentalPrice = np.loadtxt(csvfname,dtype=int,delimiter=',',usecols=range(2,97))
            self.rentArr = np.zeros((13,8))
            self.startYear = 2011
            self.endYear = 2018
            self._calcMean()
        except IOError:
            raise IOError(csvfname)
    
    def _calcMean(self):
        '''_calcMean: Calculate the mean rental price for each year, starting at 2011 and ending at 2018, for each city.'''
        for col in range(0,96,12):
            view = self.rentalPrice[:,col:col+12].mean(1)
            i = int(col/12)
            self.rentArr[:, i] = view
   
    @showNums
    def _calcPercentIncrease(self) :
        '''_calcPercentIncrease: Calculate the percent increase between the mean rental prices of 2011 and 2018, for all cities.'''     
        mean_2011 = self.rentArr[:,0]
        mean_2018 = self.rentArr[:,-1]
        percInc = ((mean_2018 - mean_2011)/mean_2011 *100)
        return percInc
        
    
    def plotRentalPrice(self, value):
        '''plotRentalPrice: Plot the rental price trend for one city as price vs year.'''
        plt.title("Rental prices over time")
        plt.xlabel("Year")
        plt.ylabel("Rental prices (in dollars)")
        plt.xticks(np.arange(0,self.endYear- self.startYear + 1),range(self.startYear, self.endYear+1,1))
        if value == len(self.cityList) - 1:
            for i in range(value):
                plt.plot(self.rentArr[i,:],label=self.cityList[i])
        else:
            plt.plot(self.rentArr[value,:],label=self.cityList[value])
        plt.legend(loc="best", prop = {'size':9})
    
    def plotPercentIncrease(self):
        '''plotPercentIncrease: Plot the percent rent increase between 2011 and 2018 for all cities.'''
        plt.title("Percentage rent increase per year")
        plt.ylim((43,61))
        plt.xlabel("City")
        plt.ylabel("Percent increase(%)")
        plt.bar(range(len(self.cityList)-1),self._calcPercentIncrease(), align='center')
        plt.xticks(range(len(self.cityList)-1),self.cityList, rotation ='vertical', fontsize = 7)
