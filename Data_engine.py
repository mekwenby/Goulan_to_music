# 数据引擎
# 负责伤害计算、静态数据存储、基本类型管理、负责伤害计算

import tool
import random
import csv
from log_system import Log
import os

log = Log()


def read_csv(file):  # 读取csv文件返回列表
    with open(file, 'r', newline='', encoding='gbk') as file:
        Data = csv.reader(file)
        lis = []
        for i in Data:
            lis.append(i)
        lis = lis[1::]
        return lis


# 副本标识管理,复杂副本机制处理
class Replica_manage():
    def __init__(self):
        self.ID = None
        self.SD_label = None  # 用于宿敌奖励翻倍处理
        self.LL_plan = 0  # 用于处理莉莉崽副本隐藏关
        self.LL_now = 0

    def set_ID(self, list):
        print(list)
        # SD = 宿敌 ，DF = 斗法 ，DMW = 大魔王 ，LL = 莉莉崽 ，HZJ = 花朝节
        # SD = ['SD',Code]
        # DF = ['DF']
        # DMW = ['DMW']

        self.ID = list[0]
        #print(list[0])
        #print(self.ID)

        if self.ID == 'SD':

            self.SD_label = list[1]
            print('处理SD', self.SD_label)

        elif self.ID == 'DF':
            pass

        elif self.ID == 'DMW':
            pass

        elif self.ID == 'LL':
            #print('处理LL')
            sp = list[1]
            #print('sp:', sp)
            if sp == 1:
                self.LL_now = sp

            elif sp != 1:
                if (sp - self.LL_plan) == 1:
                    self.LL_now = sp
            else: # 非顺序挑战时还原当前进度
                self.LL_now = 0

            #print('LL_plan', self.LL_plan)

        elif self.ID == 'HZJ':
            pass

        else:
            self.ID = None
            #print('重置ID')

    def ll(self):
        self.LL_plan = self.LL_now

    def complex_replica_mechanism_judgment(self, G_id=None):  # 复杂副本机制处理
        # print(G_id)

        if self.ID == 'SD' and G_id == self.SD_label:  # 处理宿敌相同元神加成
            global 收益修正
            # print('已触发宿敌挑战奖励')
            收益修正 = 收益修正 * 2

        elif self.ID == 'LL':
            self.LL_plan = self.LL_now


class Reward():  # 奖励、收益、掉落等原始数据处理
    def __init__(self):
        self.state = False  # 用于判断处理是否触发奖励

        # 原始数据
        self.Y = 1
        self.G = 1
        self.T = 1
        self.Exp = 1
        self.init_Magnification = 100  # 奖励倍率设置该数值
        self.Magnification = self.init_Magnification / 100  # 真实倍率 可以是浮点数
        self.data = {'Y': int(self.Y * self.Magnification), 'G': int(self.G * self.Magnification),
                     'T': int(self.T * self.Magnification), 'Exp': int(self.Exp * self.Magnification)}

    # 设置奖励数据
    def sets(self, data):
        self.Magnification = self.init_Magnification / 100

        # data = {'Y': 1, 'G': 1, 'T': 1, 'Exp': 1}

        # self.state = True
        self.Y = data.get('Y')
        self.G = data.get('G')
        self.T = data.get('T')
        self.Exp = data.get('Exp')

        # 真实奖励数值 整数类型
        self.data = {'Y': int(self.Y * self.Magnification), 'G': int(self.G * self.Magnification),
                     'T': int(self.T * self.Magnification), 'Exp': int(self.Exp * self.Magnification)}


class Battlefield_service():  # 战场服务系统

    def 伤害计算(A, B):  # 伤害计算
        ''''''
        '''物理攻击始终拥有10%强制命中率,且命中率增幅10%'''
        '''法术攻击伤害加10%'''
        '''混合伤害附带10% x 命中基数的真实伤害'''

        if A.伤害类型 == '物理':
            ''''''
            MZL = ((A.命中 * 1.1) / B.闪避) - 1  # 命中增幅10%
            if MZL > 1:
                MZL = MZL

            elif MZL < 0:  # 处理10%强制命中率
                MZL = 0.1

            if MZL > 3:
                MZL = 3

            C = int(A.物理攻击 * MZL) + random.randint(50, 200)

        elif A.伤害类型 == '法术':  # 伤害加10% 附加80-1000
            MZL = (A.命中 / B.闪避) - 1
            if MZL > 1:
                MZL = MZL

            elif MZL < 0:
                MZL = 0

            if MZL > 3:
                MZL = 3

            C = int((A.法术攻击 * MZL) * 1.1) + random.randint(80, 100)  # random用于处理浮动伤害

        elif A.伤害类型 == '混合':  # 10%真实伤害 附加100
            MZL = (A.命中 / B.闪避) - 1
            if MZL > 1:
                MZL = MZL

            elif MZL < 0:
                MZL = 0

            if MZL > 3:
                MZL = 3
                # 注意此处的（MZL + 1）
            C = int(((A.物理攻击 + A.法术攻击) * MZL) * 0.5 + (A.物理攻击 + A.法术攻击) * 0.1 * (MZL + 1)) + 100

        elif A.伤害类型 == '血怒':  # 造成 HP的百分之十*1000命中的倍数
            Magnification = (A.命中 / 1000) + 1  # 倍率
            C = int(A.HP * 0.1 * Magnification) + random.randint(80, 100)

        elif A.伤害类型 == '法术穿透':  # 造成 法术攻击的百分之十*1000命中的倍数
            Magnification = (A.命中 / 1000) + 1

            R = random.randint(int(A.法术攻击 / 10), int(A.法术攻击 / 3))

            C = int(A.法术攻击 * 0.1 * Magnification) + random.randint(80, 100) + R

        else:
            C = 0

        log.start(f'计算伤害,{A.name}攻击{B.name}-{C}')

        return C

    def 计算阵容积分():
        dic = {
            'B': 8,
            'A': 9,
            'S': 10,
            'S1': 11,
            'SS': 12
        }

        总积分 = 0.1
        for g in 阵容:
            总积分 += dic.get(g.等级)

        if len(阵容) != 0:

            阵容积分 = int(总积分 / len(阵容))
        else:
            阵容积分 = 0

        log.start(f'计算阵容积分:{阵容积分}')

        return 阵容积分

    def 计算阵容增益():
        log.start(f'计算阵容增益:{阵容积分}')
        if 阵容积分 == 8:
            return [2, 1.1]

        elif 阵容积分 == 9:
            return [1.3, 1.05]

        elif 阵容积分 == 10:
            return [1.1, 1.02]

        elif 阵容积分 == 12:
            return [0.8, 1]

        else:
            return [1, 1]

    def HP恢复计算(I):

        log.start(f'{I.name},计算恢复HP')

        if 战斗HP恢复率 > 1:
            C = 战斗HP恢复率 - 1
            log.start(f'{I.name},计算恢复HP为{int(I.HP * C)}')

            return int(I.HP * C)+random.randint(0,200)
        else:
            return 0

    def 字体坐标计算(tup):
        x = tup[0]
        y = tup[1]

        x +=random.randint(-80,80)
        y += random.randint(-20, 30)

        return (x,y)
# 以下类型已弃用

class Player():
    def __init__(self):
        self.name = tool.随机名字生成()
        self.exp = 10000000
        self.Lv = 1
        self.玉 = 600
        self.金 = 40000
        self.铜 = 1000000
        self.召唤符 = 10
        # self.初始化等级()
        # self.背包 = []
        self.元神组 = []
        self.装备组 = []

    def 初始化等级(self):
        while True:
            if self.Lv < 40:
                self.目标等级 = self.Lv + 1
                self.升级所需经验 = self.目标等级 ** 2 * 1000
                if self.exp > self.升级所需经验:
                    self.Lv = self.目标等级
                    self.exp = self.exp - self.升级所需经验
                else:
                    break

    def Save(self):

        b = tool.二进制化对象(self)
        return b

    def info(self):
        text = f'''
{self.玉}
{self.金}
{self.铜}
{self.exp}
        '''
        print(text)


# 以下类型已弃用
class Role_SW():
    def __init__(self, Lv):
        self.Lv = Lv
        self.职业 = '素问'
        self.力量资质 = 76
        self.智慧资质 = 129
        self.体力资质 = 209
        self.敏捷资质 = 86
        self.初始化基础属性()
        self.初始化战斗属性()

    def 初始化基础属性(self):
        self.力量 = int((self.力量资质 * self.Lv) * 0.3)
        self.智慧 = int((self.智慧资质 * self.Lv) * 0.3)
        self.体力 = int((self.体力资质 * self.Lv) * 0.3)
        self.敏捷 = int((self.敏捷资质 * self.Lv) * 0.3)

    def 初始化战斗属性(self):
        self.HP = self.体力 * self.体力资质 * 12
        # self.MP = self.智慧 * self.敏捷资质 * 12
        self.物理攻击 = int(self.力量 * self.力量资质 * 1.1)
        self.法术攻击 = int(self.智慧 * self.智慧资质 * 1.1)
        self.闪避 = int(self.敏捷 * 0.6 * self.敏捷资质) + self.敏捷
        self.命中 = self.敏捷 * 1 * self.敏捷资质 + self.敏捷


# 以下类型已弃用
class Role_LY():
    def __init__(self, Lv):
        self.Lv = Lv
        self.职业 = '龙吟'
        self.力量资质 = 277
        self.智慧资质 = 33
        self.体力资质 = 97
        self.敏捷资质 = 113
        self.初始化基础属性()
        self.初始化战斗属性()

    def 初始化基础属性(self):
        self.力量 = int((self.力量资质 * self.Lv) * 0.3)
        self.智慧 = int((self.智慧资质 * self.Lv) * 0.3)
        self.体力 = int((self.体力资质 * self.Lv) * 0.3)
        self.敏捷 = int((self.敏捷资质 * self.Lv) * 0.3)

    def 初始化战斗属性(self):
        self.HP = self.体力 * self.体力资质 * 12
        # self.MP = self.智慧 * self.敏捷资质 * 12
        self.物理攻击 = int(self.力量 * self.力量资质 * 1.1)
        self.法术攻击 = int(self.智慧 * self.智慧资质 * 1.1)
        self.闪避 = int(self.敏捷 * 0.6 * self.敏捷资质) + self.敏捷
        self.命中 = self.敏捷 * 1 * self.敏捷资质 + self.敏捷


# 以下类型已弃用
class Role_JL():
    def __init__(self, Lv):
        self.Lv = Lv
        self.职业 = '九灵'
        self.力量资质 = 57
        self.智慧资质 = 245
        self.体力资质 = 88
        self.敏捷资质 = 110
        self.初始化基础属性()
        self.初始化战斗属性()

    def 初始化基础属性(self):
        self.力量 = int((self.力量资质 * self.Lv) * 0.3)
        self.智慧 = int((self.智慧资质 * self.Lv) * 0.3)
        self.体力 = int((self.体力资质 * self.Lv) * 0.3)
        self.敏捷 = int((self.敏捷资质 * self.Lv) * 0.3)

    def 初始化战斗属性(self):
        self.HP = self.体力 * self.体力资质 * 12
        # self.MP = self.智慧 * self.敏捷资质 * 12
        self.物理攻击 = int(self.力量 * self.力量资质 * 1.1)
        self.法术攻击 = int(self.智慧 * self.智慧资质 * 1.1)
        self.闪避 = int(self.敏捷 * 0.6 * self.敏捷资质) + self.敏捷
        self.命中 = self.敏捷 * 1 * self.敏捷资质 + self.敏捷


# 装备类型
class Equipment():
    def __init__(self, data):
        '''品级由创建装备时生成'''
        # data=[Code,name,力量,智慧,体力,敏捷,品级]
        # 固定属性位

        self.data = data
        self.ID = tool.S随机生成字母ID_8()
        self.Code = self.data[0]
        self.name = self.data[1]
        self.品级 = self.data[-1]
        self.强化等级 = 0
        self.分配隐藏属性()
        self.设置固定属性()

    def 分配隐藏属性(self):
        # 150 - 135 - 120 - 95 - 60
        品级隐藏属性表 = {'传承': 150, '史诗': 135, '神器': 120, '稀有': 90}
        L = 品级隐藏属性表.get(self.品级)
        # print(self.品级,L,self.data)
        a = random.randint(5, int((L / 2.5)))
        b = random.randint(5, int((L / 2.5)))
        c = random.randint(5, int((L - a - b) * 0.7))
        if a + b + c >= L:
            d = 1
        else:
            d = random.randint(5, int(L - a - b - c))
        self.力量资质 = a
        self.智慧资质 = b
        self.体力资质 = c
        self.敏捷资质 = d

        self.原始力量资质 = a
        self.原始智慧资质 = b
        self.原始体力资质 = c
        self.原始敏捷资质 = d

        self.完美程度 = int(((a + b + c + d) / L) * 100)

    def 设置固定属性(self):
        self.力量 = self.data[2]
        self.智慧 = self.data[3]
        self.体力 = self.data[4]
        self.敏捷 = self.data[5]

    def 获得装备属性(self):
        self.TEXT = f'''力量+{self.力量}
智慧+{self.智慧}
体力+{self.体力}
敏捷+{self.敏捷}
完美程度:{self.完美程度}
力量加强+{self.力量资质}
智慧加强+{self.智慧资质}
体力加强+{self.体力资质}
敏捷加强+{self.敏捷资质}'''

        return self.TEXT

    def 装备强化(self):
        self.力量资质 = int(self.原始力量资质 * (1 + (self.强化等级 * 0.05)))
        self.智慧资质 = int(self.原始智慧资质 * (1 + (self.强化等级 * 0.05)))
        self.敏捷资质 = int(self.原始敏捷资质 * (1 + (self.强化等级 * 0.05)))
        self.体力资质 = int(self.原始体力资质 * (1 + (self.强化等级 * 0.05)))


# 元神类型
class Genshin():
    def __init__(self, data):
        self.Lv = 1
        self.exp = 0
        self.data = data
        self.Code = data[0]
        self.name = data[1]
        self.等级 = data[2]
        self.力量资质 = int(data[3])
        self.智慧资质 = int(data[4])
        self.体力资质 = int(data[5])
        self.敏捷资质 = int(data[6])
        self.生成随机属性()
        self.初始化基础属性()
        self.初始化战斗属性()
        # self.初始化等级()
        if self.力量资质 > self.智慧资质:
            self.伤害类型 = '物理'

        elif self.力量资质 < self.智慧资质:
            self.伤害类型 = '法术'
        else:
            self.伤害类型 = '混合'

    def 转换伤害类型(self):
        C = random.randint(1, 5)
        if C == 1:
            self.伤害类型 = '法术'
        elif C == 2:
            self.伤害类型 = '物理'
        elif C == 3:
            self.伤害类型 = '混合'
        elif C == 4:
            self.伤害类型 = '血怒'
        elif C == 5:
            self.伤害类型 = '法术穿透'

    def 初始化等级(self):
        while True:
            if self.Lv < 40:
                self.目标等级 = self.Lv + 1
                self.升级所需经验 = self.目标等级 ** 2 * 1000
                if self.exp > self.升级所需经验:
                    self.Lv = self.目标等级
                    self.exp = self.exp - self.升级所需经验
                else:
                    break

    def 生成随机属性(self):
        随机属性值 = {'B': 60, 'A': 60, 'S': 60, 'S1': 80, 'SS': 100}
        S属性值 = 随机属性值.get(self.等级)
        W位置 = random.randint(1, 4) - 1
        SS = random.randint(int(S属性值 / 3), S属性值)

        if W位置 == 0:
            self.智慧资质 = self.智慧资质 + SS
            self.后天属性 = f'智慧资质 +{SS}'
        elif W位置 == 1:
            self.力量资质 = self.力量资质 + SS
            self.后天属性 = f'力量资质 +{SS}'
        elif W位置 == 2:
            self.体力资质 = self.体力资质 + SS
            self.后天属性 = f'体力资质 +{SS}'
        elif W位置 == 3:
            self.敏捷资质 = self.敏捷资质 + SS
            self.后天属性 = f'敏捷资质 +{SS}'

        self.ID = tool.S随机生成字母ID_8()

    def 初始化基础属性(self):
        self.力量 = int(((1 + (self.力量资质 / 90)) * self.Lv) * 1.3)
        self.智慧 = int(((1 + (self.智慧资质 / 90)) * self.Lv) * 1.3)
        self.体力 = int(((1 + (self.体力资质 / 90)) * self.Lv) * 1.3)
        self.敏捷 = int(((1 + (self.敏捷资质 / 90)) * self.Lv) * 1.3)

    def 初始化战斗属性(self):
        if hasattr(self, '装备') == False:  # 判断对象该属性是否存在
            self.装备 = None

        if self.装备 == None:
            self.HP = int(self.体力 * (1 + (self.体力资质 / 100)) * 120)
            # self.MP = self.智慧 * self.敏捷资质 * 12
            self.物理攻击 = int(self.力量 * (1 + (self.力量资质 / 100)) * 60)
            self.法术攻击 = int(self.智慧 * (1 + (self.智慧资质 / 100)) * 60)
            self.闪避 = int(self.敏捷 * 0.03 * (self.敏捷资质)) + self.敏捷 + self.体力 * 8 + self.力量 + self.智慧
            self.命中 = int(self.敏捷 * 0.1 * self.敏捷资质 + self.敏捷)
        else:
            self.装备.力量 = int(self.装备.力量)
            self.装备.智慧 = int(self.装备.智慧)
            self.装备.体力 = int(self.装备.体力)
            self.装备.敏捷 = int(self.装备.敏捷)
            self.HP = int((self.体力 + self.装备.体力) * (1 + ((self.体力资质 + self.装备.体力资质) / 100)) * 120)
            # self.MP = self.智慧 * self.敏捷资质 * 12
            self.物理攻击 = int((self.力量 + self.装备.力量) * (1 + ((self.力量资质 + self.装备.力量资质) / 100)) * 60)
            self.法术攻击 = int((self.智慧 + self.装备.智慧) * (1 + ((self.智慧资质 + self.装备.智慧资质) / 100)) * 60)
            self.闪避 = int((self.敏捷 + self.装备.敏捷) * 0.03 * (
                    self.敏捷资质 + self.装备.敏捷资质)) + self.敏捷 + self.装备.敏捷 + self.体力 * 8 + self.力量 + self.智慧
            self.命中 = int((self.敏捷 + self.装备.敏捷) * 0.1 * (self.敏捷资质 + self.装备.敏捷资质)) + self.敏捷 + self.装备.敏捷


Player_Mian = Player()

当前场景 = None

# 用处未知 忘记了
幻境 = None

# 已启用
Player_Role = None

# 弹出字体
资源font = ('Arial', 22)

提示font = ('System', 21)

Exp_font = ('Arial', 18)

战斗字体 = ('System',18)

fight_colour = {'物理':'yellow','法术':'blue','混合':'green','血怒':'red','法术穿透':'cyan'}

装备字体颜色 = {'传承': 'red', '史诗': 'gold', '神器': 'magenta', '稀有': 'cyan'}

元神字体颜色 = {}

强化装备花费倍数 = {'传承': 4, '史诗': 3, '神器': 2, '稀有': 1}

阵容 = []

敌人阵容 = []

阵容积分 = 0

阵容数量 = 5

收益修正 = 1

战斗HP恢复率 = 0

当前回合数 = 0

副本标识 = None


def 阵容删除成员(G):  # 选择阵容时删除已添加成员用
    阵容.remove(G)
    刷新阵容()


# 用处未知 忘记了，
刷新阵容 = None

# 卡池初始化
# Y元神列表 = read_csv('Resource/data/Genshin.csv')
Y元神列表 = read_csv(os.path.join('Resource', 'data', 'Genshin.csv'))
# log.start(f'元神池初始化成功！{len(Y元神列表)}')
Z装备列表 = read_csv(os.path.join('Resource', 'data', 'Equipment.csv'))

# log.start(f'准备池初始化成功！{len(Z装备列表)}')

if __name__ == '__main__':
    # print(Z装备列表)
    # for i in range(100):
    #     # G = Genshin(Y元神列表[random.randint(0,len(Y元神列表)-1)])
    #     # print(G.__dict__)
    #     abc = Z装备列表[random.randint(0, len(Z装备列表) - 1)]
    #     # print(i)
    #     abc.append('史诗')
    #     E = Equipment(abc[0:7])
    #     # print(G.智慧资质)
    #     print(E.__dict__)
    #
    # abc = Z装备列表[2]
    # abc.append('传承')
    # Q = Equipment(abc[0:7])
    # print(Q.__dict__)

    for i in Y元神列表:
        print(i)
    print(len(Y元神列表))
