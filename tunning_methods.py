import cmath

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
    const = num[-1]/den[-2]
    new_den = [x/den[-2] for x in den]
    time_const = 1/new_den[-1]
    k1 = 4
    tc = 0.7*time_const
    kp = 1/(const*tc)
    ki = k1*tc
    kd = 0
    return kp,ki,kd

def skogestad_second_case(num,den):
    const = num[-1]/den[-2]
    new_den = [x/den[-2] for x in den]
    time_const = 1/new_den[-1]
    k1 = 4
    tc = 0.7*time_const
    kp = time_const/(const*tc)
    ki = min(time_const,k1*tc)
    kd = 0
    return kp,ki,kd

def skogestad_third_case(num,den):
    const = num[-1]/den[-3]
    new_den = [x/den[-3] for x in den]
    time_const = 1/new_den[-2]
    k1 = 4
    tc = 0.7*time_const
    kp = 1/(const*tc)
    ki = k1*tc
    kd = time_const
    return kp,ki,kd

def solve_second_order(den):
    c = den[-1]
    b = den[-2]
    a = den[-3]
    delta = b**2-4*a*c
    x1 = (-b+cmath.sqrt(delta))/(2*a)
    x2 = (-b-cmath.sqrt(delta))/(2*a)
    return x1,x2

def skogestad_fourth_case(num,den):
    const = num[-1]/den[-3]
    new_den = [x/den[-3] for x in den]
    x1,x2 = solve_second_order(new_den)
    t1 = 1/x1
    t2 = 1/x2
    k1 = 4
    tc = 0.7*t1
    kp = t1/(const*tc)
    try:
        ki = min(k1*tc,t1)
    except:
        ki = k1*tc
    kd = t2
    return kp,ki,kd

def skogestad_last_case(num,den):
    const = num[-1]/den[-3]
    tc = 0.7*const
    kp = 1/(4*const*tc**2)
    ki = 4*tc
    kd = ki
    return kp,ki,kd

def test_special_case1(term):
    if term[-1] == 0:
        return False
    state = 0
    for i in range(len(term)-1):
        if term[i] !=0:
            return False
    return True

def test_special_case2(term):
    for i in term:
        if i !=0:
            return False
    return True


def remove_left_zeros(term):
    if len(term) <3:
        return term
    new_term = []
    state = 0
    if test_special_case1(term):
        return [0,1]
    if test_special_case2(term):
        return [0,0]
    for i in term:
        if state == 1:
            new_term.append(i)
        if state == 0 and i != 0:
            new_term.append(i)
            state = 1
    return new_term
            

def skogestad_method(num,den):
    num = remove_left_zeros(num)
    den = remove_left_zeros(den)
    kp = 0
    ki = 0
    kd = 0
    if len(den) == 2:
        if den[-1] == 0 and den[-2] != 0:
            kp,ki,kd = skogestad_first_case(num,den)
        if den[-1] != 0 and den[-2] != 0:
            kp,ki,kd = skogestad_second_case(num,den)
    if len(den) == 3:
        if den[-1] == 0 and den[-2]!=0 and den[-3]!=0:
            kp,ki,kd = skogestad_third_case(num,den)
        if den[-1] != 0 and den[-2]!=0 and den[-3]!=0:
            kp,ki,kd = skogestad_fourth_case(num,den)
        if den[-1] != 0 and den[-2]==0 and den[-3]!=0:
            kp,ki,kd = skogestad_fourth_case(num,den)
        if den[-1] == 0 and den[-2]==0 and den[-3]!=0:
            kp,ki,kd = skogestad_last_case(num,den)
    return kp,ki,kd

if __name__ == "__main__":
    kp,ki,kd = skogestad_method([1],[0.603,1])
    print(kp,ki,kd)
