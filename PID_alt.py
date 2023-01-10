

class PID:
    def __init__(self,**kwargs):
        self.kp = 0
        self.ki = 0
        self.kd = 0
        self.tune = 0
        if "tune" not in kwargs:
            self.kp = kwargs["kp"]
            self.ki = kwargs["ki"]
            self.kd = kwargs["kd"] 
        else:
            self.tune = kwargs["tune"]
        self.delay = kwargs["delay"]

    def tune_method(self):
        if self.tune == "teste":
            

    def pid_calc(self):
        #eq = kp*(1+td*s+1/(ti*s))
        first_term_num = [self.kp*self.td,self.kp]   #(kp+kp*td*s)
        first_term_den = [0,1]
        second_term_num = [0,self.kp] #1/(ti*s)
        second_term_den = [self.ti,0]
        pid_num,pid_den = self.sum_frac(first_term_num,first_term_den,second_term_num,second_term_den)
        return pid_num,pid_den
    
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


if __name__ == "__main__":
    test = PID(delay = 1,tune = "teste")
    value = test.true_conv([0,1],[5,1])
    print(value)
