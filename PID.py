import control as ct
from ast import literal_eval
import numpy as np
import math
from sympy import Symbol,limit

class PID:
    def __init__(self, **kwargs):
        self.kp = kwargs["kp"]
        self.ki = kwargs["ki"]
        self.kd = kwargs["kd"]
        self.ft = kwargs["ft"]
        self.I = 0
        self.D = 0
        self.P = 0
        self.ti = 0
        self.td = 0
        self.time = 10**-4 # arbitrary value to the sample time on the low order filter
        self.tune = kwargs["tune"] if "tune" in kwargs else 0 
        self.filter = []
        self.pid = []
        self.error = 0
    def get_pid(self):
        if self.kp and self.kd and self.ki:
            self.pid = [[self.kd,self.kp,self.ki],[1,0]]
        if self.ki and self.kp and self.kd == 0:
            self.pid = 1 # WIP
        if self.kp and self.kd == 0 and self.ki == 0:
            self.pid = [[0,self.kp],[0,1]]
    def low_filter(self):
        den = [self.time/2,1]
        num = [1]
        self.filter = [num,den]
    def simple_conv(self):
        pid = self.pid
        num_pid = pid[0]
        filter = self.filter
        den_filter = filter[1]
        den_filter.append(0)
        self.pid = [num_pid,den_filter] 

    def true_conv(self,first_ft,second_ft):
        reference_ft = first_ft
        inv_count1 = len(first_ft)-1
        inv_count2 = len(second_ft)-1
        ind_dict = {}
        for i in first_ft:
            for j in second_ft:
                ind_dict[inv_count1+inv_count2] = i*j if inv_count1+inv_count2 not in ind_dict else ind_dict[inv_count1+inv_count2]+i*j
                inv_count2-=1
            inv_count2 = len(second_ft)-1
            inv_count1-=1
        max_value = max(ind_dict.keys())
        list_values = [0 for i in range(len(first_ft)+len(second_ft)-1)]
        for key in ind_dict :
            list_values[key] += ind_dict[key]
        res_conv = list_values.reverse()
        return list_values

## Only works for a step signal WIP
    def tune_pid_auto(self):
        x = Symbol("x")
        temp_ft = self.ft.copy()
        num = self.pid[0].copy()
        den1 = self.pid[0].copy()
        den2 = temp_ft
        den_f = self.true_conv(den1,den2)
        count = 0
        y_num = 0
        y_den = 0
        for j in den_f:
            y_den += x**count*i
            count+=1
        count = 0
        for i in num:
            y_num += x**count*i
            count+=1
        kp = limit(y_num/y_den,x,0)
        self.error = 1/(1+kp)
if __name__ == "__main__":
    test = PID(kp = 1,ki = 1,kd = 1,ft =[1,0])
    test.tune_pid()

