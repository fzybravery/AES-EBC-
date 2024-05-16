# AES-EBC

利用python实现AES-EBC加解密。并利用查表法进行优化并比较两者的效率。

文件说明：
1. AES.py文件通过编程实现AES的加解密（不采用查找表）
2. AES_lookup.py采用查找表快速实现的方法实现AES加密算法。
3. Gen_S.py生成S盒
4. mod_inverse.py为有限域上的模逆算法,为生成S盒算法的一个组件
