import RSM_class as RSM_class
import numpy as np;
import eel
eel.init('gui_app')

class RSM_solve(RSM_class.RSM):
    def __init__(self , equ) -> None:
        super().__init__()
        rsm_equ = np.array(equ).tolist()
        self.Cn = rsm_equ[0]
        self.An = rsm_equ[1]
        self.B = rsm_equ[2]
        self.basic_var = rsm_equ[4]
        self.non_basic_var = rsm_equ[3]

    def sol(self):
        num_itrations = 1
        pieb = np.zeros(len(self.basic_var))
        Ab = np.identity(len(self.basic_var))
        Xb = self.B
        Cb = np.zeros(len(self.basic_var))
        Cn = self.Cn
        An = self.An
        B = self.B
        basic_var = self.basic_var
        non_basic_var = self.non_basic_var
        C_ = self.step3(pieb, An, Cn)
        
        initials = 0
        num_negative = sum(n < 0 for n in C_[0])
        while(num_negative > initials):
            A1_position = ((num_itrations)%len(non_basic_var))-1
            A1_initials = 0
            A1 = []
            while(A1_initials < len(An)):
                A1_data = An[A1_initials][A1_position]
                A1.append([A1_data])
                A1_initials+=1
            J1 = self.step4(Ab, A1, Xb)

            basic_position = J1.index([min(i for i in sum(J1,[]) if i > 0)])
            non_basic_position = ((num_itrations)%len(non_basic_var))-1

            basic_exit_value = basic_var[basic_position]
            non_basic_exit_value = non_basic_var[non_basic_position]
            basic_var[basic_position] = non_basic_exit_value
            non_basic_var[non_basic_position] = basic_exit_value

            Cb_exit_value = Cb[basic_position]
            Cn_exit_value = Cn[non_basic_position]
            Cb[basic_position] = Cn_exit_value
            Cn[non_basic_position] = Cb_exit_value

            swap_initails = 0
            while(len(Ab) > swap_initails):
                Ab_exit_value = Ab[swap_initails][basic_position]
                An_exit_value = An[swap_initails][non_basic_position]
                Ab[swap_initails][basic_position] = An_exit_value
                An[swap_initails][non_basic_position] = Ab_exit_value
                swap_initails+=1
            Xb = self.step1(Ab, Cb, B)[0]
            Z = self.step1(Ab, Cb, B)[1]
            pieb = self.step2(Ab, Cb)
            C_ = self.step3(pieb, An, Cn)
            num_itrations+=1
            num_negative = sum(n < 0 for n in C_[0])
        num_non_basic = len(non_basic_var)
        final_value_initials = 1
        final_value = []
        while(num_non_basic >= final_value_initials):
            if(final_value_initials in basic_var):
                value_X = Xb[basic_var.index(final_value_initials)]
            else:value_X = [0]
            final_value.append(value_X)
            final_value_initials+=1
        return([sum(final_value,[]) , Z[0] , C_[0], num_itrations])

@eel.expose
def calculate(equ): 
    return RSM_solve(equ).sol()
    


# equ_data = [[10, 20, 30, 50] , [[0.25, 0.62, 1, 2] , [5, 8, 8, 10]] , [[175] ,[30]] , [1 , 2, 3 , 4] , [5, 6]]
# equ_data = [[4 , 3] , [[1 , 4] , [14 , 4] , [1 , 0]] , [[52] , [156] , [10]] , [1 , 2] , [3 , 4 , 5]]
# equ = js.dumps(equ_data)
# RSM_solve = RSM_solve(equ)
# print (RSM_solve.sol())
# print(calculate(equ))
eel.start('index.html')