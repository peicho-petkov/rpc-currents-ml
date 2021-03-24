import matplotlib.pyplot as plt 
import pandas as pd 

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

    def plot_it(self, xlabel="Date [YYYY-mm-dd]", ylabel="Current [uA]", filename=None):
        self.dataframe.set_index([self.columns[0]], inplace=True)
        self.dataframe.plot(legend=True, xlabel=xlabel, ylabel=ylabel, use_index=True)
        if filename is None:
            plt.show()
        else:
            plt.savefig(filename)
