import control as ct
import matplotlib.pyplot as plt
from . import tunning_methods


class PID:
    def __init__(self, **kwargs):
        """ O construtor dessa função é bastante leniente, apesar de existir vários parâmetros
        só é necessário o numerador e denominador para funcionar, entretanto o construtor iŕa 
        supor parâmetros, os valores padrões são: filtro: 0, type: paralelo, delay:0, tune :0, e 1 para
        os valores de kp,ki e kd se não forem passados"""
        self.kp = 1 if "kp" not in kwargs else float(kwargs["kp"])
        self.ki = 1 if "ki" not in kwargs else float(kwargs["ki"])
        self.kd = 1 if "kd" not in kwargs else float(kwargs["kd"])
        self.type = "parallel" if "type" not in kwargs else kwargs["type"]
        self.kf = 0 if "filter" not in kwargs else int(kwargs["filter"])
        self.pid_den = []
        self.pid_num = []
        self.num = kwargs["num"]
        self.den = kwargs["den"]
        self.tune = 0 if "tune" not in kwargs else kwargs["tune"]
        self.delay = 0 if "delay" not in kwargs else float(kwargs["delay"])
        self.aproximation_pade()
        self.tune_method()

    def delay_representation(self, delay):
        #delay: (2-s*td)/(2+s*td)
        num_delay = [-delay, 2]
        den_delay = [delay, 2]
        return num_delay, den_delay

    def aproximation_pade(self):  # always run this function
        if self.delay:
            num_delay, den_delay = self.delay_representation(self.delay)
            self.num = self.true_conv(self.num, num_delay)
            self.den = self.true_conv(self.den, den_delay)

    def tune_method(self):
        if self.tune == "IMC":
            self.kp, self.ki, self.kd = tunning_methods.IMC_method(
                self.num, self.den)
        if self.tune == "skogestad":
            self.kp, self.ki, self.kd = tunning_methods.skogestad_method(
                self.num, self.den)
        list_names = ["ziegle_pi", "ziegle,pid",
                      "chr_pi", "chr_pid", "chr20_pi", "chr20_pid"]
        if self.tune == "auto":
            self.kp = 1.275
            self.ki = 0.603
            self.kd = 0
        if self.tune in list_names:
            time_const, const = tunning_methods.calcule_parameters(
                self.num, self.den)
            self.kp, self.kd, self.ki = tunning_methods.tunning_methods_table_first_order[self.tune](
                self.delay, time_const, const, self.den)

    def plot_graphs(self):
        sys = ct.tf(self.num, self.den)
        sys = ct.feedback(sys, sign=-1)
        t1, y1 = ct.step_response(sys)
        sys_pid_alone = ct.tf(self.pid_num, self.pid_den)
        sys_pid = ct.tf(self.true_conv(self.pid_num, self.num),
                        self.true_conv(self.pid_den, self.den))
        sys_pid = ct.feedback(sys_pid, sign=-1)
        t2, y2 = ct.step_response(sys_pid)
        plt.plot(t2, y2)
        plt.plot(t1, y1)
        plt.show()

    def pid_calc_serie(self):
        integrate_term_num = [self.ki, 1]  # (1+Tis)
        integrate_term_den = [self.ki, 0]  # (Tis)
        derivative_term_num = [self.kd+self.kf, 1]  # Tds+1+Tfs
        derivative_term_den = [self.kf, 1]  # 1+Tfs
        id_num = self.true_conv(integrate_term_num, derivative_term_num)
        self.pid_den = self.true_conv(integrate_term_den, derivative_term_den)
        self.pid_num = [i*self.kp for i in id_num]

    def pid_calc_paralel(self):
        N = 3
        #eq = kp*(1+td*s+1/(ti*s))
        derivative_term_num = [self.kp*self.kd, 0]  # (kp*td*s)
        derivative_term_den = [self.kf/N, 1]
        integrative_term_num = [0, self.kp]  # kp/(ti*s)
        integrative_term_den = [self.ki, 0]
        proportional_term_num = [0, self.kp]  # kp/1
        proportional_term_den = [0, 1]
        self.id_num, self.id_den = self.sum_frac(
            derivative_term_num, derivative_term_den, integrative_term_num, integrative_term_den)
        self.pid_num, self.pid_den = self.sum_frac(
            self.id_num, self.id_den, proportional_term_num, proportional_term_den)

    def sum_frac(self, num1, den1, num2, den2):
        num1_conv = self.true_conv(num1, den2)
        den1_conv = self.true_conv(den1, den2)
        num2_conv = self.true_conv(num2, den1)
        den2_conv = den1_conv
        num_res = self.sum_terms(num1_conv, num2_conv)
        den_res = den2_conv
        return num_res, den_res

    def true_conv(self, first_term, second_term):
        inv_count1 = len(first_term)-1
        inv_count2 = len(second_term)-1
        ind_dict = {}
        for i in first_term:
            for j in second_term:
                ind_dict[inv_count1+inv_count2] = i*j if inv_count1 + \
                    inv_count2 not in ind_dict else ind_dict[inv_count1+inv_count2]+i*j
                inv_count2 -= 1
            inv_count2 = len(second_term)-1
            inv_count1 -= 1
        list_values = [0 for i in range(len(first_term)+len(second_term)-1)]
        for key in ind_dict:
            list_values[key] += ind_dict[key]
        list_values.reverse()
        return list_values

    def sum_terms(self, first_term, second_term):
        if len(first_term) >= len(second_term):
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

    def run_pid_paralel(self):
        self.tune_method()
        self.pid_calc_paralel()
        final_pid_num = self.true_conv(self.pid_num, self.num)
        final_pid_den = self.true_conv(self.pid_den, self.den)
        return final_pid_num, final_pid_den

    def get_pid_serie(self):
        self.tune_method()
        self.pid_calc_serie()
        final_pid_num = self.true_conv(self.pid_num, self.num)
        final_pid_den = self.true_conv(self.pid_den, self.den)
        return final_pid_num, final_pid_den

    def get_pid_parameters(self):
        self.run_pid()
        return self.kp, self.ki, self.kd

    def get_pid_only(self):
        if self.type == "parallel":
            self.pid_calc_paralel()
        elif self.type == "series":
            self.pid_calc_serie()
        else:
            raise SystemError(
                "Tipo de PID inexistente, cheque o nome passado, somente series ou parallel.")
        return self.pid_num, self.pid_den
    def get_pid_with_tf(self):
        pidd_num,pidd_den = self.get_pid_only()
        self.num_final = self.true_conv(pidd_num,self.num)
        self.den_final = self.true_conv(pidd_den,self.den)
        return self.num_final,self.den_final


if __name__ == "__main__":
    test = PID(num=[1], den=[0.603, 1], tune = "skogestad", filter = 0, )
    num,den = test.get_pid_with_tf()
    print(num,den)