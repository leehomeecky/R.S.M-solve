import numpy as np;


class RSM:
# FUNCTION TO CALCULATE THE INVERSE OF A MATRIX;
    def invers(self , value):
        # matrix =np.asmatrix(value)
        inverse = np.linalg.inv(value)
        return inverse
        
    def step1(self, Ab, Cb, B):
        MAb = np.asmatrix(Ab)
        MCb = np.asmatrix(Cb)
        MB = np.asmatrix(B)
        Xb = np.linalg.inv(MAb) * MB
        Z = MCb * Xb
        return [Xb.tolist() , Z.tolist()]

    def step2 (self , Ab , Cb):
        MCb = np.asmatrix(Cb)
        MAb = np.asmatrix(Ab)
        Pieb = MCb * np.linalg.inv(MAb)
        return Pieb.tolist()
           
    def step3 (self , Pieb , An , Cn):
        MCn = np.asmatrix(Cn)
        MAn = np.asmatrix(An)
        C_ = (Pieb * MAn) - MCn
        return C_.tolist()
               
    def step4 (self , Ab , A1 , Xb):
        MAb = np.asmatrix(Ab)
        MA1 = np.asmatrix(A1)
        Y1 = np.linalg.inv(MAb) * MA1
        J1 = Xb / Y1
        return J1.tolist()

