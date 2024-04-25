import numpy as np
import time
import random
import Gen_S as gen_s
#传入求模逆的函数

#声明全局变量
Enc_time = 0 #加密时间
Dec_time = 0 #解密时间

def Trans(text,control):
    #将字母和数字互换,control为0的时候对密文结果进行转换，转换为十六进制数构成的字符串；
    #为1时，字母转数字;
    #为2时，将十六进制字符串转换为数字列表;
    #为3时，将数字转为字符串
    result = []#转换为数字之后的明文
    temp = []#存储一行四个元素
    if control == 1:
        if len(text) < 16:
            text = "{:>16}".format(text)#如果传入的文本长度小于16个字节,那么就在左侧用空格填充
        for i in range(0,16):
            if i % 4 == 0:
                result.append(temp)
                temp = []
                temp.append(ord(text[i]))
            else:
                temp.append(ord(text[i]))
        result.append(temp)
        return result[1:]
    
    elif control == 0:
        text = [item for sublist in text for item in sublist]#使用列表推导式将二维列表转换为一维列表
        string = ''#用来存储字符串
        #将加密后的结果表示为十六进制字符串
        for item in text:
            string += hex(item)
        return string
    
    elif control == 2:
        # 去掉 "0x"，然后将字符串分割成每个十六进制数
        hex_values = text.split("0x")[1:]      
        # 将十六进制字符串转换为整数
        int_values = [int(value, 16) for value in hex_values]
        # 创建一个 4x4 的二维列表
        result = [int_values[i:i+4] for i in range(0, len(int_values), 4)]
        return result
    
    elif control == 3:
        result = ''#存储最终字符串
        for i in range(0,4):
            for j in range(0,4):
                result += hex(text[i][j])
        return result
    elif control == 4:#将结果表示为二进制字符串
        text = [item for sublist in text for item in sublist]#使用列表推导式将二维列表转换为一维列表
        string = ''#用来存储字符串
        #将加密后的结果表示为十六进制字符串
        for item in text:
            string += '{:0>8}'.format(bin(item)[2:])#去除'0b'
            #string += bin(item)
        return string



def SubBytes(alist,control):#过S盒运算,传入的参数是一个列表，即按照一列一列进行查找替换
    arrChanged = []#查S盒后的列表
    for i in range(0,4):
        arrChanged.append(gen_s.Generate_S(alist[i],control))
    return arrChanged

def ShiftRows(lie,n,control): #传入明文的一行和所需偏移的位数
    lie_temp=lie.copy()
    i=0
    #当control==0时，为左移；当control==1时，为右移
    if control == 0:
        while(i<4):
            lie[i]=lie_temp[(i+n)%4]
            i=i+1
    else:
        while(i<4):
            lie[i]=lie_temp[(i-n)%4]
            i=i+1
    return lie

def Mix_Multi(a,b):#计算在域上的乘法
    module = 0b100011011#模数是多项式x^8+x^4+x^3+1,对应的二进制数就是0b100011001
    result = 0 #0异或任何一个数，都等于该数本身
    #乘法的思想是，将乘法转换为移位加法
    for i in range(8):
        #如果b的最低位为1，那么就让结果加上当前的a，注意这里的加法其实是异或操作
        if b & 1 == 1:
            result ^= a
        #由于b是右移的(即右移之后，b&1就可以判断当前b参与运算的数是否为1)，因此为了保持结果不变，需要将a左移
        a <<= 1
        #由于模数的最高次为x^8，因此，需要判断移位后的a是否最高次为8次。
        #若a的最高次为1，那么对a进行取模运算,即a减去模数，就是a异或模数
        if a & 0b100000000 != 0:
            a ^= module
        b >>= 1
    return result

def MixColumns(PlainText,control):#列混合
    #列混合的矩阵
    #[[0x02,0x03,0x01,0x01],[0x01,0x02,0x03,0x01],[0x01,0x01,0x02,0x03],[0x03,0x01,0x01,0x02]]
    Left_array_enc = [[0x02,0x03,0x01,0x01],[0x01,0x02,0x03,0x01],[0x01,0x01,0x02,0x03],[0x03,0x01,0x01,0x02]]
    Left_array_dec = [[0x0e,0x0b,0x0d,0x09],[0x09,0x0e,0x0b,0x0d],[0x0d,0x09,0x0e,0x0b],[0x0b,0x0d,0x09,0x0e]]
    MixPlain = []
    #根据上面的列混合矩阵，对传入的列表进行列混合
    #由于整个计算在模2上，因此所有的加法替换为异或操作
    #列混合其实就是列混合矩阵左乘cipher矩阵
    #当control==0时，为加密；当control==1时，为解密
    if control == 0:
        Left_array = Left_array_enc
    else:
        Left_array = Left_array_dec
    for i in range(0,4):
        Lie_re = []#记录一行的结果
        temp_1 = Mix_Multi(PlainText[0][0],Left_array[i][0]) ^ Mix_Multi(PlainText[1][0],Left_array[i][1]) ^ Mix_Multi(PlainText[2][0],Left_array[i][2]) ^ Mix_Multi(PlainText[3][0],Left_array[i][3])
        Lie_re.append(temp_1)
        temp_2 = Mix_Multi(PlainText[0][1],Left_array[i][0]) ^ Mix_Multi(PlainText[1][1],Left_array[i][1]) ^ Mix_Multi(PlainText[2][1],Left_array[i][2]) ^ Mix_Multi(PlainText[3][1],Left_array[i][3])
        Lie_re.append(temp_2)
        temp_3 = Mix_Multi(PlainText[0][2],Left_array[i][0]) ^ Mix_Multi(PlainText[1][2],Left_array[i][1]) ^ Mix_Multi(PlainText[2][2],Left_array[i][2]) ^ Mix_Multi(PlainText[3][2],Left_array[i][3])
        Lie_re.append(temp_3)
        temp_4 = Mix_Multi(PlainText[0][3],Left_array[i][0]) ^ Mix_Multi(PlainText[1][3],Left_array[i][1]) ^ Mix_Multi(PlainText[2][3],Left_array[i][2]) ^ Mix_Multi(PlainText[3][3],Left_array[i][3])
        Lie_re.append(temp_4)
        MixPlain.append(Lie_re)
    return MixPlain

def Xor(list1,list2):
    result = [] #存储异或的结果
    for i in range(0,4):
        result.append(list1[i]^list2[i])
    return result

def KeyExpansion(plainText):
    #该函数将生成的轮密钥按照列存放
    #XorArr存储异或的列表
    XorArr = [[0x01,0,0,0],[0x02,0,0,0],[0x04,0,0,0],[0x08,0,0,0],[0x10,0,0,0],[0x20,0,0,0],[0x40,0,0,0],[0x80,0,0,0],[0x1b,0,0,0],[0x36,0,0,0]]
    list_key = [] #将密钥按列存储
    for i in range(0,4):
        sub_list_key = [plainText[0][i],plainText[1][i],plainText[2][i],plainText[3][i]] #一列
        list_key.append(sub_list_key)
    for i in range(4,44):
        temp = list_key[i-1]#存储当前列的前一列信息
        #如果当前列数是4的整数倍
        #那么就先将当前列的前一列进行移位操作，然后再与异或列表进行异或操作，赋值给temp列
        if i % 4 == 0: 
            #由于不希望前一列的移位将前一列信息打乱，即我们只需要移位后的列而原列保持不变，因此这里采用浅复制
            temp = Xor(SubBytes(ShiftRows(temp.copy(),1,0),0),XorArr[i//4-1])
        list_key.append(Xor(list_key[i-4],temp))
    #这里得到的密钥是按列存储的，而且是存储在一起的
    #将轮密钥分割
    roundKey = []#存储轮密钥
    i = 0
    while i <= 40:
        temp = []
        for j in range(0,4):
            temp.append(list_key[i+j])
        temp =  [[row[i] for row in temp] for i in range(len(temp[0]))]#使用列表推导式将二维数组转置
        roundKey.append(temp)
        i = i + 4
    return roundKey

def Enc_AES(plainText,key):#加密函数
    global Enc_time #使用global声明Enc_time以修改全局变量
    time_start = time.time()#记录开始时间

    roundKey = KeyExpansion(key)#生成轮密钥
    #异或主密钥
    temp_Cipher = []#存储中间的加密结果
    for i in range(0,4):
        temp_Cipher.append(Xor(plainText[i],key[i]))
    #前九轮和第十轮的过程不同，第十轮加密不需要列混合
    for i in range(0,10):
        #过S盒
        for j in range(0,4):
            temp_Cipher[j] = SubBytes(temp_Cipher[j],0)
        #左移位
        for j in range(0,4):
            temp_Cipher[j] = ShiftRows(temp_Cipher[j],j,0)
        #列混合，只有前九轮进行列混合
        if i <= 8:
            temp_Cipher = MixColumns(temp_Cipher,0)
        #异或轮密钥
        for j in range(0,4):
            temp_Cipher[j] = Xor(temp_Cipher[j],roundKey[i+1][j])
    time_end = time.time()#记录一次加密结束时间
    Enc_time += time_end - time_start #将一次加密的时间累加到总的加密时间中
    return Trans(temp_Cipher,0)

def Dec_AES(CipherText,key):
    global Dec_time #使用global声明Dec_time以修改全局变量
    time_start = time.time()#记录开始时间

    roundKey = KeyExpansion(key)#生成轮密钥
    temp_plain = []#存储中间的解密结果
    #解密过程轮密钥逆用
    #与轮密钥异或
    for i in range(0,4):
        temp_plain.append(Xor(CipherText[i],roundKey[10][i]))
    #前九轮和第十轮的过程不同，第十轮加密不需要列混合
    for i in range(0,10):
        #过S盒
        for j in range(0,4):
            temp_plain[j] = SubBytes(temp_plain[j],1)
        #左移位
        for j in range(0,4):
            temp_plain[j] = ShiftRows(temp_plain[j],j,1)
                #异或轮密钥
        for j in range(0,4):
            temp_plain[j] = Xor(temp_plain[j],roundKey[9-i][j])
        #列混合，只有前九轮进行列混合
        if i <= 8:
            temp_plain = MixColumns(temp_plain,1)

    time_end = time.time()#记录一次加密结束时间
    Dec_time += time_end - time_start #将一次解密的时间累加到总的加密时间中
    return Trans(temp_plain,3)

def Generate_text():
    text = ''#存储生成的十六进制数组成的字符串，长16个字节
    #生成一个随机数，将其转换为十六进制之后存储到text中
    for i in range(0,16):
        num = random.randint(0,255)
        text += hex(num)
    return text

def test():#单次测试
    plaintext = '0x680x650x6c0x6c0x6f0x200x770x6f0x720x6c0x640x200x730x640x750x71'
    key = '1234567891234567'
    ciphertext = '0x940x3a0x230x5c0xb60xcc0xa40x770x290x540x2b0x7d0x750x3f0xb40x4a'
    cipher = Enc_AES(Trans(plaintext,2),Trans(key,1))
    plain = Dec_AES(Trans(ciphertext,2),Trans(key,1))
    print('既定明文：',plaintext)
    print('加密后的密文：',cipher)
    print('解密后的明文：',plain)
    print('加密时间：',Enc_time)
    print('解密时间：',Dec_time)


def timetest():#加解密时间测试
    key = '1234567891234567'#确定密钥
    for i in range(0,1000):
        plaintext = Generate_text()#生成明文
        ciphertext = Enc_AES(Trans(plaintext,2),Trans(key,1))#完成一次加密，并获取密文
        Dec_AES(Trans(ciphertext,2),Trans(key,1))#完成一次解密
    print('加密时间：',Enc_time)
    print('解密时间：',Dec_time)

if __name__ == '__main__':
    print("===============加解密算法正确性验证===============")
    test()#加解密测试，测试加解密算法是否正确
    print("===============1000次加解密所需时间===============")
    timetest()#测试1000次加密和解密的时间        