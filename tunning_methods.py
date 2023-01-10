def model_pid_first_order(delay,time_const,const,p_const,i_const,d_const):
    kp = p_const*time_const/(const*delay)
    ki = i_const*delay
    kd = d_const*delay
    return kp,kd,ki

#WIP def model_pid_second_order():
    pass

tunning_methods_table_first_order = {
    'ziegle_pi': lambda delay,time_const,const,den: model_pid_first_order(delay,time_const,const,0.9,3.3,0),
    'chr_pi': lambda delay,time_const,const,den: model_pid_first_order(delay,time_const,const,0.35,1.16/delay*time_const,0),
    'chr20_pi': lambda delay,time_const,const,den: model_pid_first_order(delay,time_const,const,0.6,1/delay*time_const,0),
    'ziegle_pid': lambda delay,time_const,const,den: model_pid_first_order(delay,time_const,const,1.2,2,1/2),
    'chr_pid': lambda delay,time_const,const,den: model_pid_first_order(delay,time_const,const,0.6,1/delay*time_const,1/2),
    'chr20_pid': lambda delay,time_const,const,den: model_pid_first_order(delay,time_const,const,0.95,1.357/delay*time_const,0.473)
    #NOT WORKING'jon-mor_pid': lambda delay,time_const,const,den: model_pid_second_order(delay,time_const,const,0.95,1.357/delay*time_const,0.473)
}

def skogestad_first_case(num,den): #needs to be checked the constant can be a issue due to one being related to other
    const = num[-1]
    time_const = den[-2]
    k1 = 4
    tc = 0.7*time_const
    kp = 1/(const*tc)
    ki = k1*tc
    kd = 0
    return kp,ki,kd

def skogestad_second_case(num,den):
    const = num[-1]
    time_const = 1/den[-1]
    k1 = 4
    tc = 0.7*time_const
    kp = 1/(const*tc)
    ki = min(time_const,k1*tc)
    kd = 0
    return kp,ki,kd

def skogestad_third_case(num,den):
    const = num[-1]
    time_const = 1/den[-1]
    k1 = 4
    tc = 0.7*time_const
    kp = 1/(const*tc)
    ki = min(time_const,k1*tc)
    kd = 0
    return kp,ki,kd


def skogestad_method(num,den):
    pass

