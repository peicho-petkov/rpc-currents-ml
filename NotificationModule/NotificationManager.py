from db_tools import table_predicted_current
import time

def datetime2unix(dt):
    return time.mktime(dt.timetuple())

class NotificationManager:
    def __init__(self, db_conn, prediction_table, rolling_average_window):
        self.db_conn = db_conn
        self.prediction_table = prediction_table
        self.set_rolling_average_window(rolling_average_window)

    def set_rolling_average_window(self, npoints):
        self.rolling_average_window = npoints

    def set_soft_limit(self, soft_limit = 3):
        ''' soft limit in uA - for warnings raising '''
        self.soft_limit = soft_limit

    def set_hard_limit(self, hard_limit = 5):
        ''' hard limit in uA - for errors raising '''
        self.hard_limit = hard_limit

    def load_data(self, data, time_format='%Y-%m-%d %H:%M:%'):
        self.timestamp=list()
        self.prediction=list()
        self.mon=list()
        for row in data:
            self.timestamp.append(row[0])
            self.prediction.append(row[1])
            self.mon.append(row[2])

    def set_persistence_time(self, persistence_time = 8192):
        ''' time period [s] above soft/hard limit to encounter warning/error '''
        self.persistence_time = persistence_time

    def analyse(self):
        lt = len(self.timestamp)
        lp = len(self.prediction)
        lm = len(self.mon)
        
        if not (lt == lp and lp == lm):
            raise "datasets len does not match..."

        npoints = lm

        k_raised_soft = -1
        k_raised_hard = -1
        soft_acc = 0.0
        hard_acc = 0.0
        soft_acc_n = 0
        hard_acc_n = 0

        diff = []
        for kk in range(self.rolling_average_window - 1):
            diff.append(self.mon[kk]-self.prediction[kk])

        for kk in range(self.rolling_average_window - 1, npoints):
            diff.append(self.mon[kk]-self.prediction[kk])
            rav = sum(diff)/self.rolling_average_window
            diff.pop(0)
            
            if rav >= self.hard_limit and k_raised_hard < 0:
                k_raised_hard = kk

            if k_raised_hard > -1 and rav < self.hard_limit:
                k_raised_hard = -1
                hard_acc = 0.0
                hard_acc_n = 0

            if k_raised_hard > -1:
                hard_acc = hard_acc + rav
                hard_acc_n = hard_acc_n + 1

            if rav >= self.soft_limit and k_raised_soft < 0:
                k_raised_soft = kk

            if k_raised_soft > -1 and rav < self.soft_limit:
                k_raised_soft = -1
                soft_acc = 0.0
                soft_acc_n = 0

            if k_raised_soft > -1:
                soft_acc = soft_acc + rav
                soft_acc_n = soft_acc_n + 1

            if k_raised_hard > -1 and rav >= self.hard_limit:
                if datetime2unix(self.timestamp[kk]) - datetime2unix(self.timestamp[k_raised_soft]) >= self.persistence_time: 
                    yield "ERROR", self.timestamp[kk], hard_acc/hard_acc_n
                    k_raised_hard = -1
                    hard_acc = 0.0
                    hard_acc_n = 0
            elif k_raised_soft > -1 and rav >= self.soft_limit:
                if datetime2unix(self.timestamp[kk]) - datetime2unix(self.timestamp[k_raised_soft]) >= self.persistence_time: 
                    yield "WARNING", self.timestamp[kk], soft_acc/soft_acc_n
                    k_raised_soft = -1
                    soft_acc = 0.0
                    soft_acc_n = 0
