import numpy as np
arr = []#存储256组输入值对应的输出值的异或值

S_box_enc = np.array(
    [[0x63, 0x7c, 0x99, 0x30, 0x1e, 0xad, 0xca, 0xb5, 0xdd, 0x77, 0x4, 0x78, 0xb7, 0xcd, 0x8, 0x7f], 
     [0x49, 0x31, 0x1c, 0x9f, 0xd0, 0x40, 0xee, 0x5f, 0x9, 0xbc, 0x41, 0x6f, 0xa3, 0x6a, 0x18, 0x12], 
     [0x3, 0xb3, 0x4a, 0xe5, 0xdc, 0xb0, 0x68, 0x9b, 0xba, 0x1b, 0x87, 0x8f, 0xa5, 0x67, 0x7d, 0xe0], 
     [0x23, 0x9e, 0x8c, 0xb, 0x7, 0x37, 0x10, 0xc5, 0x76, 0x88, 0xe7, 0xd2, 0xab, 0xf3, 0xae, 0xdb], 
     [0x26, 0xf4, 0x7e, 0x32, 0x82, 0x73, 0x20, 0x13, 0xc9, 0x47, 0xff, 0x3a, 0xe6, 0xc, 0x1f, 0xb2], 
     [0xfa, 0xbe, 0x2a, 0x91, 0x64, 0x1d, 0x60, 0xd9, 0x0, 0x1, 0x14, 0x4f, 0x19, 0x34, 0xd7, 0xf6], 
     [0x43, 0xd6, 0xe8, 0x8a, 0xe1, 0xb8, 0x22, 0x4d, 0x51, 0x6d, 0x3c, 0x6e, 0xaf, 0xfc, 0x45, 0x8b], 
     [0x9c, 0x44, 0x96, 0x69, 0x21, 0xaa, 0xbb, 0x39, 0x72, 0xbf, 0x5e, 0x4b, 0x85, 0x61, 0x3f, 0xf9], 
     [0xb4, 0xea, 0xa8, 0xf8, 0x98, 0x59, 0xcb, 0xc4, 0x93, 0x50, 0x6b, 0x8e, 0xc2, 0x84, 0x2e, 0x92], 
     [0x36, 0x7b, 0x71, 0x81, 0x2d, 0x9a, 0xcf, 0xf1, 0xa1, 0x55, 0xd4, 0xb1, 0x5d, 0x2f, 0xfe, 0x24], 
     [0xda, 0x33, 0x8d, 0x56, 0xc7, 0x9d, 0x1a, 0x3d, 0x95, 0x79, 0x5c, 0x58, 0xe2, 0x5a, 0x3e, 0xd5], 
     [0xa7, 0x3b, 0x27, 0xa2, 0xd8, 0x6c, 0x75, 0x16, 0x2b, 0xd1, 0xbd, 0xc0, 0x4c, 0xc1, 0xa9, 0x83], 
     [0x6, 0xce, 0xcc, 0x48, 0xd3, 0xa, 0x97, 0x89, 0x57, 0x15, 0xfb, 0xe, 0xc3, 0xe3, 0x74, 0x35], 
     [0xf, 0x2c, 0x11, 0xed, 0xb9, 0xa6, 0x90, 0x46, 0x5, 0x52, 0xac, 0x80, 0x70, 0x54, 0x17, 0xc6], 
     [0xe9, 0xef, 0xf0, 0xc8, 0xec, 0xf5, 0x66, 0xf7, 0x42, 0x86, 0xf2, 0xe4, 0x7a, 0xde, 0x4e, 0xa0], 
     [0xeb, 0xa4, 0xd, 0x28, 0xfd, 0x94, 0x2, 0x29, 0x65, 0x53, 0x62, 0x25, 0x38, 0xdf, 0x5b, 0xb6]]
)
# S_box_dec = np.array(
#     [[0x58, 0x59, 0xf6, 0x20, 0xa, 0xd8, 0xc0, 0x34, 0xe, 0x18, 0xc5, 0x33, 0x4d, 0xf2, 0xcb, 0xd0], 
#      [0x36, 0xd2, 0x1f, 0x47, 0x5a, 0xc9, 0xb7, 0xde, 0x1e, 0x5c, 0xa6, 0x29, 0x12, 0x55, 0x4, 0x4e], 
#      [0x46, 0x74, 0x66, 0x30, 0x9f, 0xfb, 0x40, 0xb2, 0xf3, 0xf7, 0x52, 0xb8, 0xd1, 0x94, 0x8e, 0x9d], 
#      [0x3, 0x11, 0x43, 0xa1, 0x5d, 0xcf, 0x90, 0x35, 0xfc, 0x77, 0x4b, 0xb1, 0x6a, 0xa7, 0xae, 0x7e], 
#      [0x15, 0x1a, 0xe8, 0x60, 0x71, 0x6e, 0xd7, 0x49, 0xc3, 0x10, 0x22, 0x7b, 0xbc, 0x67, 0xee, 0x5b], 
#      [0x89, 0x68, 0xd9, 0xf9, 0xdd, 0x99, 0xa3, 0xc8, 0xab, 0x85, 0xad, 0xfe, 0xaa, 0x9c, 0x7a, 0x17], 
#      [0x56, 0x7d, 0xfa, 0x0, 0x54, 0xf8, 0xe6, 0x2d, 0x26, 0x73, 0x1d, 0x8a, 0xb5, 0x69, 0x6b, 0x1b], 
#      [0xdc, 0x92, 0x78, 0x45, 0xce, 0xb6, 0x38, 0x9, 0xb, 0xa9, 0xec, 0x91, 0x1, 0x2e, 0x42, 0xf], 
#      [0xdb, 0x93, 0x44, 0xbf, 0x8d, 0x7c, 0xe9, 0x2a, 0x39, 0xc7, 0x63, 0x6f, 0x32, 0xa2, 0x8b, 0x2b], 
#      [0xd6, 0x53, 0x8f, 0x88, 0xf5, 0xa8, 0x72, 0xc6, 0x84, 0x2, 0x95, 0x27, 0x70, 0xa5, 0x31, 0x13], 
#      [0xef, 0x98, 0xb3, 0x1c, 0xf1, 0x2c, 0xd5, 0xb0, 0x82, 0xbe, 0x75, 0x3c, 0xda, 0x5, 0x3e, 0x6c], 
#      [0x25, 0x9b, 0x4f, 0x21, 0x80, 0x7, 0xff, 0xc, 0x65, 0xd4, 0x28, 0x76, 0x19, 0xba, 0x51, 0x79], 
#      [0xbb, 0xbd, 0x8c, 0xcc, 0x87, 0x37, 0xdf, 0xa4, 0xe3, 0x48, 0x6, 0x86, 0xc2, 0xd, 0xc1, 0x96], 
#      [0x14, 0xb9, 0x3b, 0xc4, 0x9a, 0xaf, 0x61, 0x5e, 0xb4, 0x57, 0xa0, 0x3f, 0x24, 0x8, 0xed, 0xfd], 
#      [0x2f, 0x64, 0xac, 0xcd, 0xeb, 0x23, 0x4c, 0x3a, 0x62, 0xe0, 0x81, 0xf0, 0xe4, 0xd3, 0x16, 0xe1], 
#      [0xe2, 0x97, 0xea, 0x3d, 0x41, 0xe5, 0x5f, 0xe7, 0x83, 0x7f, 0x50, 0xca, 0x6d, 0xf4, 0x9e, 0x4a]]
# )

def Sub(num):#过s盒，传入的参数是一个数
        numChanged = 0#存储过S盒之后的结果
        row = num // 16
        column = num % 16
        numChanged = S_box_enc[row][column]
        return numChanged

def Get_Xor_List():
        for num1 in range(0,256):
            num2 = num1 ^ 1 #与num1异或值为1的数，对于不用的异或值可以直接在此修改
            num1_S = Sub(num1)
            num2_S = Sub(num2)
            #num1和num2对应的S盒中的数的异或值
            xor_result = num1_S ^ num2_S
            arr.append(xor_result)
            print('(',num1,',',num2,'):',xor_result)


if __name__ == '__main__':
        Get_Xor_List()
        arr_count = [] #统计arr中每一个异或值出现的次数
        print(arr)
        for i in range(0,256):
                arr_count.append(arr.count(arr[i]))
        print(arr_count)


