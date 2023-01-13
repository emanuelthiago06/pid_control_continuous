import tunning_methods
import control as ct
import matplotlib.pyplot as plt

class PID:
    def __init__(self,**kwargs):
        self.kp = 0
        self.ki = 0
        self.kd = 0
        self.pid_den = []
        self.pid_num = []
        self.tune = 0
        self.num = kwargs["num"]
        self.den = kwargs["den"]
        if "tune" not in kwargs:
            self.kp = kwargs["kp"]
            self.ki = kwargs["ki"]
            self.kd = kwargs["kd"] 
        else:
            self.tune = kwargs["tune"]
        self.delay = kwargs["delay"]

    def tune_method(self):
        if self.tune == "skogestad":
            self.kp,self.ki,self.kd = tunning_methods.skogestad_method(self.num,self.den)
        list_names = ["ziegle_pi","ziegle,pid","chr_pi","chr_pid","chr20_pi","chr20_pid"]
        if self.tune == "auto":
            self.kp = 1.275
            self.ki = 0.603
            self.kd = 0
        if self.tune in list_names:
            delay,time_const,const = tunning_methods.calcule_parameters(self.num,self.den)
            self.kp,self.kd,self.ki = tunning_methods.tunning_methods_table_first_order[self.tune](delay,time_const,const,self.den)

    def plot_graphs(self):
        sys = ct.tf(self.num,self.den)
        sys = ct.feedback(sys,sign = -1)
        print(sys)
        t1,y1 = ct.step_response(sys)
        sys_pid_alone =  ct.tf(self.pid_num,self.pid_den)
        print(sys_pid_alone)
        sys_pid = ct.tf(self.true_conv(self.pid_num,self.num),self.true_conv(self.pid_den,self.den))
        sys_pid = ct.feedback(sys_pid,sign=-1)
        print(sys_pid)
        t2,y2 = ct.step_response(sys_pid)
        t3,y3 = ct.step_response(sys_pid_alone)
        plt.plot(t2,y2)
        plt.plot(t1,y1)
        print(t3)
        plt.show()

    def pid_calc_serie(self):
        integrate_term_num = [self.ki,1] #(1+Tis)
        integrate_term_den = [self.ki,0] #(Tis)
        derivative_term_num = [self.kd,1] #Tds+1
        derivative_term_den = [0,1]
        id_num = self.true_conv(integrate_term_num,derivative_term_num)
        self.pid_den = self.true_conv(integrate_term_den,derivative_term_den)
        self.pid_num = [i*self.kp for i in id_num]

    def pid_calc_paralel(self):
        #eq = kp*(1+td*s+1/(ti*s))
        first_term_num = [self.kp*self.kd,self.kp]   #(kp+kp*td*s)
        first_term_den = [0,1]
        second_term_num = [0,self.kp] #1/(ti*s)
        second_term_den = [self.ki,0]
        self.pid_num,self.pid_den = self.sum_frac(first_term_num,first_term_den,second_term_num,second_term_den)
    
    def sum_frac(self,num1,den1,num2,den2):
        num1_conv = self.true_conv(num1,den2)
        den1_conv = self.true_conv(den1,den2)
        num2_conv = self.true_conv(num2,den1)
        den2_conv = den1_conv
        num_res = self.sum_terms(num1_conv,num2_conv)
        den_res = den2_conv
        return num_res,den_res

    def true_conv(self,first_term,second_term):
        inv_count1 = len(first_term)-1
        inv_count2 = len(second_term)-1
        ind_dict = {}
        for i in first_term:
            for j in second_term:
                ind_dict[inv_count1+inv_count2] = i*j if inv_count1+inv_count2 not in ind_dict else ind_dict[inv_count1+inv_count2]+i*j
                inv_count2-=1
            inv_count2 = len(second_term)-1
            inv_count1-=1
        list_values = [0 for i in range(len(first_term)+len(second_term)-1)]
        for key in ind_dict :
            list_values[key] += ind_dict[key]
        list_values.reverse()
        return list_values

    def sum_terms(self,first_term,second_term):
        if len(first_term)>=len(second_term):
            more_term = first_term
            less_term = second_term
        else:
            more_term = second_term
            less_term = first_term
        more_term.reverse()
        less_term.reverse()
        sum_result = more_term
        for i in range(len(less_term)):
            sum_result[i] = more_term[i]+less_term[i]
        sum_result.reverse()
        return sum_result

    def get_pid(self):
        self.tune_method()
        self.pid_calc_paralel()
        self.plot_graphs()

if __name__ == "__main__":
    test = PID(delay = 0,tune = "auto",num = [1],den = [0.603,1])
    test.get_pid()
