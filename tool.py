import time
import string
import random
import pickle

def S随机生成字母():
    s = string.ascii_uppercase
    r = random.choice(s)
    return r

def S随机生成字母ID_8():
    ID = S随机生成字母()+S随机生成字母()+S随机生成字母()+S随机生成字母()+\
         S随机生成字母()+S随机生成字母()+S随机生成字母()+S随机生成字母()
    return ID


def S生成等级():
    i = ['B','A','S','S1','SS']

    r = random.randint(0,len(i))

    return i[r-1]

def S属性分配(S):
    if S=='B':
        A = random.randint(30,100)
        B = random.randint(30,100)
        C = random.randint(50,250-A-B)
        D = 350-A-B-C
        return (A,B,C,D)

    elif S=='A':
        A = random.randint(80, 120)
        B = random.randint(80, 120)
        C = random.randint(60, 300 - A - B)
        D = 400 - A - B - C
        return (A, B, C, D)

    elif S=='S':
        A = random.randint(80, 135)
        B = random.randint(80, 135)
        C = random.randint(70, 350 - A - B)
        D = 450 - A - B - C
        return (A, B, C, D)

    elif S=='S1':
        A = random.randint(40, 180)
        B = random.randint(40, 180)
        C = random.randint(100, 420 - A - B)
        D = 500 - A - B - C
        return (A, B, C, D)

    elif S=='SS':
        D = random.randint(80, 180)
        C = random.randint(80, 180)
        A = random.randint(60, 450 - D - C)
        B = 550 - A - D - C
        return (A, B, C, D)

def 随机名字生成():
    int = random.randint(100000,900000) #生成随机数
    int2 = random.randint(1,1000)

    username = f'玩家_{int}{int2}'

    return username

def 二进制化对象(obj):
    b_obj = pickle.dumps(obj)
    return b_obj

def 还原对象(b):
    obj = pickle.loads(b)
    return obj


if __name__ == '__main__':
    DJ  = S生成等级()
    print(S随机生成字母() + S随机生成字母() + S随机生成字母() + S随机生成字母() + S随机生成字母())
    DJ = S生成等级()
    print(S属性分配("A"))
    A = S随机生成字母() + S随机生成字母() + S随机生成字母() + S随机生成字母() + S随机生成字母()
    c = 1
    for i in range(20):
        c = 1
        while True:
            B = S随机生成字母() + S随机生成字母() + S随机生成字母() + S随机生成字母() + S随机生成字母()
            c +=1

            if A==B:
                print(c)
                break



