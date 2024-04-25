import mod_inverse as iv

module = '100011011'#不可约多项式的二进制字符串表示

def Tran(text,control):
    if control == 0:#如果control为0，则为加密中的将列表转换为十进制数
        Dec = 0
        for i in range(0,8):
            Dec += text[i] * 2**i
        return Dec
    elif control == 1:#如果control为1，则为将十进制数转换为二进制列表
        string = "{:0>8}".format(bin(text)[2:])#先将十进制数转化为二进制字符串
        alist = [] #列表
        #将字符串转换为列表
        for i in range(0,8):
            alist.append(int(string[i]))
        return alist
    elif control == 2:#如果control为2，将字符串转换为十进制整数
        result = 0
        for i in range(0,8):
            result += int(text[i]) * 2**(7-i)
        return result
    elif control == 3:
        #在生成S盒的时候，将两个数分别为八位二进制的高四位和第四位，然后转变为该八位二进制数对应的十进制数
        High = "{:0>4}".format(bin(text[0])[2:])#获取高四位的四位二进制数
        Low = "{:0>4}".format(bin(text[1])[2:])#获取低四位的四位二进制数
        result_str = ''#构成的八位二进制字符串
        result_str = result_str + High + Low
        result = Tran(result_str,2)
        return result

def Xor(list1,list2):
    result = [] #存储异或的结果
    for i in range(0,8):
        result.append(list1[i]^list2[i])
    return result

def Mul_Matrix(inv_list,control):#模逆左乘矩阵
    #当control为0的时候，是加密左乘矩阵
    #当control为1的时候，是解密左乘逆矩阵
    #因为是模2运算，所以加法是异或操作
    Left_M = [[1,0,0,0,1,1,1,1],[1,1,0,0,0,1,1,1],[1,1,1,0,0,0,1,1],[1,1,1,1,0,0,0,1],[1,1,1,1,1,0,0,0],[0,1,1,1,1,1,0,0],[0,0,1,1,1,1,1,0],[0,0,0,1,1,1,1,1]]
    Left_M_in = [[0,0,1,0,0,1,0,1],[1,0,0,1,0,0,1,0],[0,1,0,0,1,0,0,1],[1,0,1,0,0,1,0,0],[0,1,0,1,0,0,1,0],[0,0,1,0,1,0,0,1],[1,0,0,1,0,1,0,0],[0,1,0,0,1,0,1,0]]
    result = []#inv_list左乘矩阵的结果
    if control == 0:
        Matrix = Left_M
    elif control == 1:
        Matrix = Left_M_in
    for i in range(0,8):
        temp_re = 0#一行的结果
        for j in range(0,8):
            temp_re ^= Matrix[i][j] * inv_list[j]
        result.append(temp_re)
    return result

def Generate_S(num,control):#生成num在S盒中对应的数
    #先获取num的模逆（模数为不可约多项式）
    Xor_list = [1,1,0,0,0,1,1,0]#异或列表
    if control == 0:#加密生成S盒
        num_inv = "{:0>8}".format(iv.inv(num,module))#这里的num_inv是一个字符串
        list_inv = []#存储num模逆的列表
        result_list = []
        for i in range(0,8):
            list_inv.append(int(num_inv[i]))
        list_inv.reverse()#将列表逆序
        result_list = Mul_Matrix(list_inv,0)
        result_list = Xor(result_list,Xor_list)#将左乘后的列表与Xor_list异或
        result = Tran(result_list,0)
        return result
    elif control == 1:#解密生成S盒
        num_list = Tran(num,1)#将数字转换为列表
        num_list.reverse()#列表逆序
        result_list = Xor(Xor_list,num_list)#先异或
        result_list = Mul_Matrix(result_list,1)#左乘逆矩阵得到目标数的逆列表
        result_num = Tran(result_list,0)#将列表转换为整数
        result_str = "{:0>8}".format(iv.inv(result_num,module))#得到结果的字符串
        result = Tran(result_str,2)
        return result

def Gen_Sbox(control):#生成S盒,
    #control为0的时候生成加密S盒，为1的时候生成解密S盒
    S_Box = []#S盒
    #通过循环，i为高四位，j为低四位，遍历从而生成对应的S盒
    for i in range(0,16):
        S_Box_Row = []#S盒的一行
        for j in range(0,16):
            num = Tran([i,j],3)
            S_Box_Row.append(hex(Generate_S(num,control)))
        S_Box.append(S_Box_Row)
    return S_Box