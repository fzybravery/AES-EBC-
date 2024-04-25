import AES_lookup as aesl
import AES as aes

def Trans(list):#将列表转换为128位二进制字符串
    string = ''
    for i in range(0,4):
        for j in range(0,4):
            string += "{:0>8}".format(bin(list[i][j])[2:])
            string += ' '
    return string


def Enc_AES(plainText,key,round,control):#加密函数
    #当control=0时，有列混合，反之无列混合

    roundKey = aesl.KeyExpansion(key)#生成轮密钥
    #异或主密钥
    temp_Cipher = []#存储中间的加密结果
    for i in range(0,4):
        temp_Cipher.append(aes.Xor(plainText[i],key[i]))
    #前九轮和第十轮的过程不同，第十轮加密不需要列混合
    for i in range(0,round):#加密的轮数
        #过S盒
        for j in range(0,4):
            temp_Cipher[j] = aesl.Sub(temp_Cipher[j],0)
        #左移位
        for j in range(0,4):
            temp_Cipher[j] = aes.ShiftRows(temp_Cipher[j],j,0)
        if control == 0:
            #列混合
            temp_Cipher = aesl.Mul_Columns(temp_Cipher,0)
        #异或轮密钥
        for j in range(0,4):
            temp_Cipher[j] = aes.Xor(temp_Cipher[j],roundKey[i+1][j])
    return temp_Cipher

def Gen_Plaintext():
    Plain_Arr = []#存储256个明文字符串
    Head = '0x680x650x6c0x6c'#前四个块对应的十六进制字符串
    Tail = '0x200x770x6f0x720x6c0x640x200x730x640x750x71'#后11个块对应的十六进制字符串
    Mid = ''#中间会发生改变的一块对应的十六进制字符串
    for i in range(0,256):#遍历256种情况
        Mid = hex(i)
        Plain_Arr.append(Head+Mid+Tail)
    return Plain_Arr

def xor_cipher(cipher1,cipher2):#将两个列表的中的对应位置的元素异或，并返回一个新的列表
    for i in range(0,4):
        for j in range(0,4):
            cipher1[i][j]=cipher1[i][j]^cipher2[i][j]
    return cipher1

def Test(round,control):
    key = '1234567123456789'#密钥
    plain = Gen_Plaintext()#获取满足题目要求的256个明文组成的列表
    cipher = []#256个密文组成的列表
    for i in range(0,256):
        cipher.append(Enc_AES(aes.Trans(plain[i],2),aes.Trans(key,1),round,control))
    #一个空的列表，存储256个密文的异或值
    Empty_arr = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    #进行异或操作
    for i in range(0,256):
        Empty_arr = xor_cipher(Empty_arr,cipher[i])
    print(round,"轮：",Trans(Empty_arr))

if __name__ == "__main__":
    print("有列混合：")
    Test(3,0)
    Test(4,0)
    print("无列混合：")
    for i in range(3,10):
        Test(i,1)
    #若删除MC变换，9轮变换结果仍然是0，超出9轮之后由于轮密钥长度不够，因此若需要继续验证还需要扩展轮密钥的长度

