import matplotlib
from matplotlib import pyplot as plt 
import pandas as pd 
import numpy as np

class simple_plotter:
    ''' Plots versus date, i.e. assumes time as x-axis 
    '''
    
    def __init__(self, columns, data, time_format='%Y-%m-%d %H:%M:%S'):
        self.load_data(columns, data, time_format)

    def load_data(self, columns, data, time_format='%Y-%m-%d %H:%M:%S'):
        self.columns = list(columns.values()) 
        xcolumn = str(columns[0])
        self.dataframe = pd.DataFrame( [[ij for ij in i] for i in data] )
        self.dataframe.rename(columns=columns, inplace=True)
        self.dataframe[xcolumn] = pd.to_datetime(self.dataframe[xcolumn], format=time_format) 

    def plot_it(self, xlabel="Date [YYYY-mm-dd]", ylabel="Current [uA]", filename=""):
        self.dataframe.set_index([self.columns[0]], inplace=True)
        self.dataframe.plot(legend=True, xlabel=xlabel, ylabel=ylabel, use_index=True)
        if filename == "":
            plt.show()
        else:
            plt.savefig(filename) 

    def plot_diff(self, xlabel="Date [YYYY-mm-dd]", ylabel="CurrentDifference [uA]", filename=""):
        difference = self.dataframe[self.columns[2]] - self.dataframe[self.columns[1]]
        xcolumn = str(self.columns[0])
        x = self.dataframe[xcolumn]
        fig, (sp1, sp2) = plt.subplots(1,2,gridspec_kw={'width_ratios':[5, 2]})
        sp1.plot(x, difference)
        sp2.hist(difference, bins=50, orientation="horizontal")
        if filename == "":
            plt.show()
        else:
            plt.savefig(filename) 

    def plot_run_avg(self, xlabel="Date [YYYY-mm-dd]", ylabel="CurrentDiffRunAvg [uA]", filename=""):
        difference = self.dataframe[self.columns[2]] - self.dataframe[self.columns[1]]
        self.dataframe['difference'] = difference
        newdataframe = self.dataframe[['predicted_for', 'difference']].copy()
        self.dataframe.drop(['difference'], axis=1)
        newdataframe.set_index(['predicted_for'], inplace=True)
        rolling = newdataframe.rolling(100).mean()
        newdataframe['rolling'] = rolling 
        newdataframe  = newdataframe.drop(['difference'], axis=1)
        newdataframe.plot(legend=True, xlabel=xlabel, ylabel=ylabel, use_index=True)
        if filename == "":
            plt.show()
        else:
            plt.savefig(filename)




class simple_plotter_opt:
    ''' Plots versus date, i.e. assumes time as x-axis 
    '''
    
    def __init__(self, columns, data, time_format='%Y-%m-%d %H:%M:%S'):
        self.load_data(columns, data, time_format)

    def load_data(self, columns, data, time_format='%Y-%m-%d %H:%M:%S'):
        self.columns = list(columns.values()) 
        ncols = len(self.columns)
        nrows = len(data)
        xcolumn = str(columns[0])
        self.date = list() #np.zeros(nrows, dtype=np.float)
        self.pred = list() #np.zeros(nrows, dtype=np.float)
        self.meas = list() #np.zeros(nrows, dtype=np.float)
        i = 0 
        for row in data:
            self.date.append(row[0])
            self.pred.append(row[1])
            self.meas.append(row[2])
            #self.date[i] = matplotlib.dates.date2num(row[0])
            #self.pred[i] = row[1]
            #self.meas[i] = row[2]
            i = i + 1
        
    def plot_it(self, xlabel="Date [YYYY-mm-dd]", ylabel="Current [uA]", filename=""):
        plt.gcf().autofmt_xdate() 
        plt.ylabel("Current [uA]") 
        plt.plot(self.date,self.pred,'.-',label="predicted", alpha=0.5)
        plt.plot(self.date,self.meas,'.-',label="measured",alpha=0.5) 
        plt.legend()
        if filename == "":
            plt.show()
        else:
            plt.savefig(filename) 

