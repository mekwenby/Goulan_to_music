import gc
import os
import pickle
import random
import time
import tkinter.messagebox
from threading import Thread
from tkinter import *
from tkinter.ttk import Combobox
# from tkinter import font
from PIL import ImageTk

import Data_engine as DE
import ancient_engine
from Config import Config_Config
from log_system import Log

log = Log()
print = log.start
reward = DE.Reward()
r_manage = DE.Replica_manage()


def 普通弹窗(标题, 内容):
    result = tkinter.messagebox.askokcancel(title=f'{标题}', message=f'{内容}')


# Jpg 图像资源处理模块
def Open_Jpg(file):
    '''用PIL模块处理JPG格式图像'''
    print(f'处理图像：{file}')
    image = ImageTk.Image.open(file)  # 用Image模块打开图像
    image2 = ImageTk.PhotoImage(image)
    # print(image2.width())
    # print(image2.height())
    # 处理为Tkimage格式
    return image2


def showMenu(event):
    # print('yunx!')
    Main_menubar.post(event.x_root, event.y_root)


def Save():
    保存窗口(DE.当前场景.frame)


def 自动保存():
    for i in DE.Player_Mian.元神组:  # 删除战斗场景附加的额外属性，否则无法保存
        try:
            del i.text
        except:
            pass

    file = str(DE.Player_Mian.name)
    avefile = os.path.join('Save', file + '.Player')
    with open(avefile, 'wb') as file:  # 持久化对象需要使用二进制写入
        pickle.dump(DE.Player_Mian, file)
    # 普通弹窗('保存完成', f'{avefile}存档已保存！')
    # self.fm.destroy()
    print('已自动保存游戏！')


def 进入游戏():
    大地图()


def 切换角色():
    # DE.Player_Mian.初始化等级()
    角色切换()


def 退出游戏():
    自动保存()
    win.destroy()


def load():
    开始()

    def New():
        DE.Player_Mian = DE.Player()
        角色切换()
        存档窗口.destroy()
        print(DE.Player_Mian.name)

    Save_list = os.listdir('Save')
    print(Save_list)
    存档窗口 = Frame(DE.当前场景.frame)
    关闭按钮(存档窗口)
    L = Label(存档窗口, text='存档管理').pack()
    for i in Save_list:
        i = 存档加载按钮(存档窗口, os.path.join('Save', i))

    Button(存档窗口, text='新建存档', command=New).pack()
    存档窗口.place(x=0, y=500)


def New_存档加载界面():
    def New():
        DE.Player_Mian = DE.Player()
        角色切换()
        print(f'新建存档成功{DE.Player_Mian}')
        print(DE.Player_Mian.name)

    def Load():
        filename = var.get()
        file = os.path.join('Save', filename)
        with open(file, 'rb') as file:
            DE.Player_Mian = pickle.load(file)
            # 普通弹窗('存档管理', f'{file}已加载！')
            切换角色()

    开始()
    Save_list = os.listdir('Save')
    heigth = 150
    存档加载界面 = LabelFrame(DE.当前场景.frame, text='加载存档', height=heigth, width=700)
    存档加载界面.place(x=(1366 - 700) / 2, y=768 - heigth)
    L1 = Label(存档加载界面, text='存档文件名：').place(x=10, y=10)
    var = StringVar()
    C1 = Combobox(存档加载界面, width=60, textvariable=var)
    C1['value'] = Save_list
    try:  # 用于处理存档为空的情况
        C1.current(0)
    except:
        pass

    C1.place(x=130, y=30)
    B1 = Button(存档加载界面, text='加载存档', width=60, command=Load, relief=FLAT)
    B1.place(x=130, y=70)
    B2 = Button(存档加载界面, text='新游戏', width=60, command=New, relief=FLAT)
    B2.place(x=130, y=100)


# 场景切换函数
def 角色切换():
    DE.当前场景.off()
    DE.当前场景 = Home(win)


def 打开背包():
    DE.当前场景.off()
    DE.当前场景 = Backpack(win)


def 大地图():
    DE.当前场景.off()
    DE.当前场景 = Map(win)


def 开始():
    DE.当前场景.off()
    DE.当前场景 = Start(win)


def 切换场景(OBJ):  # 万能切换场景，将场景对象传进来，关闭旧场景，场景新场景
    print(text=f'场景关闭：{DE.当前场景}')
    DE.当前场景.frame.destroy()

    del DE.当前场景
    gc.collect()  # 清理内存
    DE.当前场景 = OBJ(win)
    print(text=f'场景切换成功！{str(DE.当前场景)}')
    if reward.state:  # 切换场景触发奖励
        # reward.Magnification = reward.Magnification * DE.收益修正 #
        DE.当前场景.LL掉落弹窗 = 掉落弹窗(list=reward.data)
        reward.state = False

        # 初始化奖励倍率
        reward.init_Magnification = 100


def 出征():  # 开始战斗场景切换 阵容控制 复杂机制控制
    # for i in DE.敌人阵容:
    # print('敌人', i.__dict__)

    # for i in DE.阵容:
    # print('我方', i.__dict__)
    if len(DE.阵容) != 0:
        if DE.阵容数量 == 1:
            DE.阵容 = [DE.阵容[0]]

        切换场景(战斗场景)


def DEUBG():
    DeBUG()


class 战斗场景():
    def __init__(self, root):
        self.frame = Frame(root, width=1366, height=768)
        self.frame.place(x=0, y=0)

        self.伤害计算 = DE.Battlefield_service.伤害计算

        self.我方阵容 = DE.阵容
        self.敌方阵容 = DE.敌人阵容

        self.create = Canvas(self.frame, width=1366, height=768)
        self.create.place(x=0, y=0)
        self.BG = Open_Jpg(os.path.join('Resource', 'picture', 'MapTT', f'ZDCJ.jpg'))
        self.BG_img = self.create.create_image(0, 0, anchor=NW, image=self.BG)
        self.战场信息 = LabelFrame(self.frame, text='战场信息', width=150, height=760)
        self.战场信息.place(x=1210, y=5)

        self.HP信息面板()
        self.显示阵容窗口()

        self.kill_image = Open_Jpg(os.path.join('Resource', 'picture', 'ui', 'kill.jpg'))
        self.auto_image = Open_Jpg(os.path.join('Resource', 'picture', 'ui', 'auto.jpg'))
        self.exit_image = Open_Jpg(os.path.join('Resource', 'picture', 'ui', 'quit.jpg'))

        self.开始按钮 = Button(self.frame, image=self.kill_image, relief=FLAT, command=self.战斗开始).place(x=1, y=720)
        self.auto_lab = False  # 用于标识自动战斗是否开启
        self.auto_Button = Button(self.frame, image=self.auto_image, relief=FLAT, command=self.start_auto_fight).place(
            x=52, y=720)
        self.exit_fight_Button = Button(self.frame, image=self.exit_image, relief=FLAT, command=self.exit_fight).place(
            x=103, y=720)
        self.line_list = []  # 用于存储线条
        self.战场动态 = []
        self.HP_list = []

        self.rounds = 1  # 用于回合计数

    def start_auto_fight(self):  # 开始自动战斗
        t = Thread(target=self.auto_fight)
        t.start()

    def exit_fight(self):  # 退出战斗
        self.off()
        DE.当前场景 = Map(win)

    def auto_fight(self):  # 自动战斗
        self.auto_lab = True
        while self.auto_lab:
            self.战斗开始()
            time.sleep(Config_Config.get('sleep_time'))

    def 显示阵容窗口(self):

        '''该函数用于处理战斗场景显示角色信息'''
        '''注意阵容数量的判断渲染和出场阵容'''

        py = 468
        px = 583

        dx = 583
        dy = 0
        # 我方阵容
        if len(self.我方阵容) < 3 or len(self.我方阵容) == 2:
            self.p1 = self.我方阵容[0]
            self.p1_P = Open_Jpg(os.path.join('Resource', 'picture', 'Genshin', f'{self.p1.Code}-x.jpg'))
            self.p1_img = self.create.create_image(px, py, anchor=NW, image=self.p1_P)
            self.p1.当前HP = self.p1.HP
            self.p1.text = StringVar()
            self.p1.text.set(f'{self.p1.name}\n{self.p1.当前HP}/{self.p1.HP}')
            self.p1_l = Label(self.我方_HP, textvariable=self.p1.text).pack()
            self.p1.c = (px + 100, py)
            self.出场阵容 = [self.p1]

            if len(self.我方阵容) == 2:
                '''判断一下是否为2,不是2则不渲染p2'''

                self.p2 = self.我方阵容[1]
                self.p2_P = Open_Jpg(os.path.join('Resource', 'picture', 'Genshin', f'{self.p2.Code}-x.jpg'))
                self.p2_img = self.create.create_image(px - 210, py, anchor=NW, image=self.p2_P)
                self.p2.当前HP = self.p2.HP
                self.p2.text = StringVar()
                self.p2.text.set(f'{self.p2.name}\n{self.p2.当前HP}/{self.p2.HP}')
                self.p2_l = Label(self.我方_HP, textvariable=self.p2.text).pack()
                self.p2.c = (px - 210 + 100, py)
                self.出场阵容 = [self.p1, self.p2]

        elif len(self.我方阵容) == 3 or len(self.我方阵容) == 4:
            self.p1 = self.我方阵容[0]
            self.p1_P = Open_Jpg(os.path.join('Resource', 'picture', 'Genshin', f'{self.p1.Code}-x.jpg'))
            self.p1_img = self.create.create_image(px, py, anchor=NW, image=self.p1_P)
            self.p1.当前HP = self.p1.HP
            self.p1.text = StringVar()
            self.p1.text.set(f'{self.p1.name}\n{self.p1.当前HP}/{self.p1.HP}')
            self.p1_l = Label(self.我方_HP, textvariable=self.p1.text).pack()
            self.p1.c = (px + 100, py)

            self.p2 = self.我方阵容[1]
            self.p2_P = Open_Jpg(os.path.join('Resource', 'picture', 'Genshin', f'{self.p2.Code}-x.jpg'))
            self.p2_img = self.create.create_image(px - 210, py, anchor=NW, image=self.p2_P)
            self.p2.当前HP = self.p2.HP
            self.p2.text = StringVar()
            self.p2.text.set(f'{self.p2.name}\n{self.p2.当前HP}/{self.p2.HP}')
            self.p2_l = Label(self.我方_HP, textvariable=self.p2.text).pack()
            self.p2.c = (px - 210 + 100, py)

            self.p3 = self.我方阵容[2]
            self.p3_P = Open_Jpg(os.path.join('Resource', 'picture', 'Genshin', f'{self.p3.Code}-x.jpg'))
            self.p3_img = self.create.create_image(px + 210, py, anchor=NW, image=self.p3_P)
            self.p3.当前HP = self.p3.HP
            self.p3.text = StringVar()
            self.p3.text.set(f'{self.p3.name}\n{self.p3.当前HP}/{self.p3.HP}')
            self.p3_l = Label(self.我方_HP, textvariable=self.p3.text).pack()
            self.p3.c = (px + 210 + 100, py)
            self.出场阵容 = [self.p1, self.p2, self.p3]

            if len(self.我方阵容) == 4:
                '''判断一下是否为4,不是4则不渲染p4'''
                self.p4 = self.我方阵容[3]
                self.p4_P = Open_Jpg(os.path.join('Resource', 'picture', 'Genshin', f'{self.p4.Code}-x.jpg'))
                self.p4_img = self.create.create_image(px - 420, py, anchor=NW, image=self.p4_P)
                self.p4.当前HP = self.p4.HP
                self.p4.text = StringVar()
                self.p4.text.set(f'{self.p4.name}\n{self.p4.当前HP}/{self.p4.HP}')
                self.p4_l = Label(self.我方_HP, textvariable=self.p4.text).pack()
                self.p4.c = (px - 420 + 100, py)
                self.出场阵容 = [self.p1, self.p2, self.p3, self.p4]

        elif len(self.我方阵容) == 5:
            self.p1 = self.我方阵容[0]
            self.p1_P = Open_Jpg(os.path.join('Resource', 'picture', 'Genshin', f'{self.p1.Code}-x.jpg'))
            self.p1_img = self.create.create_image(px, py, anchor=NW, image=self.p1_P)
            self.p1.当前HP = self.p1.HP
            self.p1.text = StringVar()
            self.p1.text.set(f'{self.p1.name}\n{self.p1.当前HP}/{self.p1.HP}')
            self.p1_l = Label(self.我方_HP, textvariable=self.p1.text).pack()
            self.p1.c = (px + 100, py)

            self.p2 = self.我方阵容[1]
            self.p2_P = Open_Jpg(os.path.join('Resource', 'picture', 'Genshin', f'{self.p2.Code}-x.jpg'))
            self.p2_img = self.create.create_image(px - 210, py, anchor=NW, image=self.p2_P)
            self.p2.当前HP = self.p2.HP
            self.p2.text = StringVar()
            self.p2.text.set(f'{self.p2.name}\n{self.p2.当前HP}/{self.p2.HP}')
            self.p2_l = Label(self.我方_HP, textvariable=self.p2.text).pack()
            self.p2.c = (px - 210 + 100, py)

            self.p3 = self.我方阵容[2]
            self.p3_P = Open_Jpg(os.path.join('Resource', 'picture', 'Genshin', f'{self.p3.Code}-x.jpg'))
            self.p3_img = self.create.create_image(px + 210, py, anchor=NW, image=self.p3_P)
            self.p3.当前HP = self.p3.HP
            self.p3.text = StringVar()
            self.p3.text.set(f'{self.p3.name}\n{self.p3.当前HP}/{self.p3.HP}')
            self.p3_l = Label(self.我方_HP, textvariable=self.p3.text).pack()
            self.p3.c = (px + 210 + 100, py)

            self.p4 = self.我方阵容[3]
            self.p4_P = Open_Jpg(os.path.join('Resource', 'picture', 'Genshin', f'{self.p4.Code}-x.jpg'))
            self.p4_img = self.create.create_image(px - 420, py, anchor=NW, image=self.p4_P)
            self.p4.当前HP = self.p4.HP
            self.p4.text = StringVar()
            self.p4.text.set(f'{self.p4.name}\n{self.p4.当前HP}/{self.p4.HP}')
            self.p4_l = Label(self.我方_HP, textvariable=self.p4.text).pack()
            self.p4.c = (px - 420 + 100, py)

            self.p5 = self.我方阵容[4]
            self.p5_P = Open_Jpg(os.path.join('Resource', 'picture', 'Genshin', f'{self.p5.Code}-x.jpg'))
            self.p5_img = self.create.create_image(px + 420, py, anchor=NW, image=self.p5_P)
            self.p5.当前HP = self.p5.HP
            self.p5.text = StringVar()
            self.p5.text.set(f'{self.p5.name}\n{self.p5.当前HP}/{self.p5.HP}')
            self.p1_5 = Label(self.我方_HP, textvariable=self.p5.text).pack()
            self.p5.c = (px + 420 + 100, py)
            self.出场阵容 = [self.p1, self.p2, self.p3, self.p4, self.p5]

        # 敌方阵容
        if len(self.敌方阵容) == 1:
            self.d1 = self.敌方阵容[0]
            self.d1_P = Open_Jpg(os.path.join('Resource', 'picture', 'Genshin', f'{self.d1.Code}-x.jpg'))
            self.d1_img = self.create.create_image(dx, dy, anchor=NW, image=self.d1_P)
            self.d1.当前HP = self.d1.HP
            self.d1.text = StringVar()
            self.d1.text.set(f'{self.d1.name}\n{self.d1.当前HP}/{self.d1.HP}')
            self.d1_l = Label(self.敌方_HP, textvariable=self.d1.text).pack()
            self.d1.c = (dx + 100, dy + 300)
            self.敌出场阵容 = [self.d1]

        elif len(self.敌方阵容) == 3 or len(self.敌方阵容) == 4:
            self.d1 = self.敌方阵容[0]
            self.d1_P = Open_Jpg(os.path.join('Resource', 'picture', 'Genshin', f'{self.d1.Code}-x.jpg'))
            self.d1_img = self.create.create_image(dx, dy, anchor=NW, image=self.d1_P)
            self.d1.当前HP = self.d1.HP
            self.d1.text = StringVar()
            self.d1.text.set(f'{self.d1.name}\n{self.d1.当前HP}/{self.d1.HP}')
            self.d1_l = Label(self.敌方_HP, textvariable=self.d1.text).pack()
            self.d1.c = (dx + 100, dy + 300)

            self.d2 = self.敌方阵容[1]
            self.d2_P = Open_Jpg(os.path.join('Resource', 'picture', 'Genshin', f'{self.d2.Code}-x.jpg'))
            self.d2_img = self.create.create_image(dx - 210, dy, anchor=NW, image=self.d2_P)
            self.d2.当前HP = self.d2.HP
            self.d2.text = StringVar()
            self.d2.text.set(f'{self.d2.name}\n{self.d2.当前HP}/{self.d2.HP}')
            self.d2_l = Label(self.敌方_HP, textvariable=self.d2.text).pack()
            self.d2.c = (dx - 210 + 100, dy + 300)

            self.d3 = self.敌方阵容[2]
            self.d3_P = Open_Jpg(os.path.join('Resource', 'picture', 'Genshin', f'{self.d3.Code}-x.jpg'))
            self.d3_img = self.create.create_image(dx + 210, dy, anchor=NW, image=self.d3_P)
            self.d3.当前HP = self.d3.HP
            self.d3.text = StringVar()
            self.d3.text.set(f'{self.d3.name}\n{self.d3.当前HP}/{self.d3.HP}')
            self.d3_l = Label(self.敌方_HP, textvariable=self.d3.text).pack()
            self.d3.c = (dx + 210 + 100, dy + 300)
            self.敌出场阵容 = [self.d1, self.d2, self.d3]

        elif len(self.敌方阵容) == 5:
            self.d1 = self.敌方阵容[0]
            self.d1_P = Open_Jpg(os.path.join('Resource', 'picture', 'Genshin', f'{self.d1.Code}-x.jpg'))
            self.d1_img = self.create.create_image(dx, dy, anchor=NW, image=self.d1_P)
            self.d1.当前HP = self.d1.HP
            self.d1.text = StringVar()
            self.d1.text.set(f'{self.d1.name}\n{self.d1.当前HP}/{self.d1.HP}')
            self.d1_l = Label(self.敌方_HP, textvariable=self.d1.text).pack()
            self.d1.c = (dx + 100, dy + 300)

            self.d2 = self.敌方阵容[1]
            self.d2_P = Open_Jpg(os.path.join('Resource', 'picture', 'Genshin', f'{self.d2.Code}-x.jpg'))
            self.d2_img = self.create.create_image(dx - 210, dy, anchor=NW, image=self.d2_P)
            self.d2.当前HP = self.d2.HP
            self.d2.text = StringVar()
            self.d2.text.set(f'{self.d2.name}\n{self.d2.当前HP}/{self.d2.HP}')
            self.d2_l = Label(self.敌方_HP, textvariable=self.d2.text).pack()
            self.d2.c = (dx - 210 + 100, dy + 300)

            self.d3 = self.敌方阵容[2]
            self.d3_P = Open_Jpg(os.path.join('Resource', 'picture', 'Genshin', f'{self.d3.Code}-x.jpg'))
            self.d3_img = self.create.create_image(dx + 210, dy, anchor=NW, image=self.d3_P)
            self.d3.当前HP = self.d3.HP
            self.d3.text = StringVar()
            self.d3.text.set(f'{self.d3.name}\n{self.d3.当前HP}/{self.d3.HP}')
            self.d3_l = Label(self.敌方_HP, textvariable=self.d3.text).pack()
            self.d3.c = (dx + 210 + 100, dy + 300)

            self.d4 = self.敌方阵容[3]
            self.d4_P = Open_Jpg(os.path.join('Resource', 'picture', 'Genshin', f'{self.d4.Code}-x.jpg'))
            self.d4_img = self.create.create_image(dx - 420, dy, anchor=NW, image=self.d4_P)
            self.d4.当前HP = self.d4.HP
            self.d4.text = StringVar()
            self.d4.text.set(f'{self.d4.name}\n{self.d4.当前HP}/{self.d4.HP}')
            self.d4_l = Label(self.敌方_HP, textvariable=self.d4.text).pack()
            self.d4.c = (dx - 420 + 100, dy + 300)

            self.d5 = self.敌方阵容[4]
            self.d5_P = Open_Jpg(os.path.join('Resource', 'picture', 'Genshin', f'{self.d5.Code}-x.jpg'))
            self.d5_img = self.create.create_image(dx + 420, dy, anchor=NW, image=self.d5_P)
            self.d5.当前HP = self.d5.HP
            self.d5.text = StringVar()
            self.d5.text.set(f'{self.d5.name}\n{self.d5.当前HP}/{self.d5.HP}')
            self.d1_5 = Label(self.敌方_HP, textvariable=self.d5.text).pack()
            self.d5.c = (dx + 420 + 100, dy + 300)
            self.敌出场阵容 = [self.d1, self.d2, self.d3, self.d4, self.d5]

    def HP信息面板(self):
        self.敌方_HP = LabelFrame(self.frame, text='敌方信息', width=150, height=280)
        self.敌方_HP.place(x=3, y=0)
        self.我方_HP = LabelFrame(self.frame, text='我方信息', width=150, height=280)
        self.我方_HP.place(x=3, y=428)

    def 战斗开始(self):

        def OK():
            切换场景(Map)

        def move(ID, x, y):
            pass
            # for i in range(0,random.randint(60,100)):
            #     i = i * -1
            #     print(f'开始移动:{ID}-{x}-{y}')
            #     self.create.move(ID,0,i)
            #     self.create.update()
            #     time.sleep(0.00000001)
            # time.sleep(0.002)

        try:

            for i in self.line_list:  # 清除线条
                self.create.delete(i)
        except:
            pass

        try:
        # 初始化列表
            self.line_list = []
            self.战场动态 = []
            self.战场动态.append(f'---第{DE.当前回合数}回合---')
            ##########################################################
            self.战场动态.append('#我方回合#')

            for i in self.出场阵容:
                # 处理阵容只有一人的情况
                if len(self.敌出场阵容) == 1:
                    D = self.敌出场阵容[0]
                else:
                    try:
                        D = self.敌出场阵容[random.randint(1, len(self.敌出场阵容)) - 1]
                    except:
                        D = (0, 0)

                line = self.create.create_line(i.c, D.c, arrow=LAST, width=3, fill='red')
                self.line_list.append(line)
                C = self.伤害计算(i, D)
                伤害数值 = f'-{C}'
                坐标 = DE.Battlefield_service.字体坐标计算(D.c)
                伤害文本 = self.create.create_text(坐标, text=伤害数值, fill='red', font=DE.战斗字体)

                move(伤害文本, 坐标[0], 坐标[1])

                self.line_list.append(伤害文本)
                text = f'{i.name}攻击{D.name}\n造成{C}伤害。'
                self.战场动态.append(text)
                D.当前HP -= C
                HP = DE.Battlefield_service.HP恢复计算(i)

                if HP > 0:
                    恢复数值 = f'+{HP}'
                    恢复文本 = self.create.create_text(i.c[0], i.c[1] + 290, text=恢复数值, fill='green', font=DE.战斗字体)
                    move(恢复文本, i.c[0], i.c[1] + 290)
                    self.line_list.append(恢复文本)
                    i.当前HP += HP
                    text = f'{i.name}恢复了\n{HP}点生命值。'
                    self.战场动态.append(text)

                if i.当前HP > i.HP:  # 恢复满处理,防止当前HP 溢出
                    i.当前HP = i.HP

                if D.当前HP < 0:
                    tex = f'{D.name}被{i.name}击杀！'
                    self.战场动态.append(tex)
                    D.text.set(f'{D.name}\n败北')
                    try:
                        self.敌出场阵容.remove(D)
                    except:
                        pass
                if len(self.敌出场阵容) == 0:
                    print('胜利！')
                    判断弹窗(OK=OK, text='胜利！')

                    # 触发奖励
                    reward.state = True  # 处理回合收益相关计算
                    if DE.当前回合数 >= 200:
                        DE.收益修正 = DE.收益修正 * 0.25
                    elif DE.当前回合数 >= 100:

                        DE.收益修正 = DE.收益修正 * 0.5

                    if DE.当前回合数 > 300:
                        DE.收益修正 = 0

                    r_manage.complex_replica_mechanism_judgment(G_id=DE.阵容[0].Code)

            ########################################################
            self.战场动态.append('----------\n#敌方回合#')
            for i in self.敌出场阵容:
                if len(self.出场阵容) == 1:
                    D = self.出场阵容[0]
                elif len(self.出场阵容) == 0:
                    pass

                else:
                    try:
                        D = self.出场阵容[random.randint(1, len(self.出场阵容)) - 1]
                    except:
                        D = self.出场阵容[0]

                line = self.create.create_line(i.c, D.c, arrow=LAST, width=2, fill='blue')
                self.line_list.append(line)
                C = self.伤害计算(i, D)
                text = f'{i.name}攻击{D.name}\n造成{C}伤害。'
                self.战场动态.append(text)
                伤害数值 = f'-{C}'
                坐标 = DE.Battlefield_service.字体坐标计算(D.c)
                伤害文本 = self.create.create_text(坐标, text=伤害数值, fill='blue', font=DE.战斗字体)
                move(伤害文本, 坐标[0], 坐标[1])
                self.line_list.append(伤害文本)
                D.当前HP -= C
                if D.当前HP < 0:
                    tex = f'{D.name}被{i.name}击杀！'
                    self.战场动态.append(tex)
                    D.text.set(f'{D.name}\n败北')
                    self.出场阵容.remove(D)
                if len(self.出场阵容) == 0:
                    print('失败！')
                    判断弹窗(OK=OK, text='失败！')
            try:
                self.刷新战场动态()
            except:
                pass
            self.rounds = self.rounds + 1

            DE.当前回合数 = self.rounds
        except:
            pass

    '''def 伤害计算(self, A, B): # 伤害计算
        if A.伤害类型 == '物理':  # 命中率加10% 附加300-500
            MZL = (A.命中 / B.闪避) - 0.9
            if MZL > 1:
                MZL = MZL
            elif MZL < 0:
                MZL = 0
            C = int(A.物理攻击 * MZL) + random.randint(200,500)

        elif A.伤害类型 == '法术':  # 伤害加10% 附加1-1000
            MZL = (A.命中 / B.闪避) - 1
            if MZL > 1:
                MZL = MZL
            elif MZL < 0:
                MZL = 0
            C = int((A.法术攻击 * MZL) * 1.1) + random.randint(1,800)

        elif A.伤害类型 == '混合':  # 8%真实伤害 附加100
            MZL = (A.命中 / B.闪避) - 1
            if MZL > 1:
                MZL = MZL
            elif MZL < 0:
                MZL = 0
            C = int(((A.物理攻击 + A.法术攻击) * MZL) * 0.5 + (A.物理攻击 + A.法术攻击) * 0.08) + 100

        return C'''

    def 刷新战场动态(self):
        for i in self.战场信息.winfo_children():  # 清空Frame
            # print('清空', i)
            i.place_forget()

        x = 3
        y = 3
        # self.战场信息.destroy()
        self.战场信息 = LabelFrame(self.frame, text='战场信息', width=150, height=760)
        self.战场信息.place(x=1210, y=5)
        for i in self.战场动态:
            self.BCBCBL = Label(self.战场信息, text=i, justify=LEFT, font=('Aridl', 8))
            self.BCBCBL.place(x=x, y=y)
            y += 35

        for i in self.出场阵容:
            i.text.set(f'{i.name}\n{i.当前HP}/{i.HP}')
        for i in self.敌出场阵容:
            i.text.set(f'{i.name}\n{i.当前HP}/{i.HP}')

    def off(self):
        self.frame.destroy()


class 保存窗口():
    def __init__(self, win):
        self.fm = Frame(win)
        self.L = Label(self.fm, text='存档文件名你')
        self.存档文件名 = Entry(self.fm)
        self.存档文件名.insert(0, DE.Player_Mian.name)
        self.存档文件名.pack()
        self.保存按钮 = Button(self.fm, text='保存', command=self.ave).pack()
        self.关闭按钮 = 关闭按钮(self.fm)
        self.fm.place(x=500, y=300)

    def ave(self):
        file = self.存档文件名.get()
        avefile = os.path.join('Save', file + '.Player')
        with open(avefile, 'wb') as file:  # 持久化对象需要使用二进制写入
            pickle.dump(DE.Player_Mian, file)
        普通弹窗('保存完成', f'{avefile}存档已保存！')
        self.fm.destroy()


class 关闭按钮():
    def __init__(self, win):
        self.FFM = win
        self.BU = Button(win, text='关闭', command=self.off)
        self.BU.pack(side=BOTTOM)

    def off(self):
        self.FFM.destroy()


class 存档加载按钮():
    def __init__(self, win, file):
        self.file = file
        self.BU = Button(win, text=f'{file}', command=self.Load)
        self.BU.pack()

    def Load(self):
        with open(self.file, 'rb') as file:
            DE.Player_Mian = pickle.load(file)
            普通弹窗('存档管理', f'{file}已加载！')
            角色切换()


# 修改器
class DeBUG():

    def __init__(self):
        print('尝试打开修改器！')
        self.root = Toplevel()
        self.EXP = Button(self.root, text='经验+980000', command=lambda: self.修改器(['EXP', 980000])).pack()
        self.TQ = Button(self.root, text='铜钱+980000', command=lambda: self.修改器(['TQ', 9880000])).pack()
        self.HG = Button(self.root, text='黄金+80000', command=lambda: self.修改器(['HG', 80000])).pack()
        self.GY = Button(self.root, text='勾玉+2000', command=lambda: self.修改器(['GY', 2000])).pack()

        self.EXP0 = Button(self.root, text='经验=0', command=lambda: self.归零(['EXP', 980000])).pack()
        self.TQ0 = Button(self.root, text='铜钱=0', command=lambda: self.归零(['TQ', 9880000])).pack()
        self.HG0 = Button(self.root, text='黄金=0', command=lambda: self.归零(['HG', 80000])).pack()
        self.GY0 = Button(self.root, text='勾玉=0', command=lambda: self.归零(['GY', 2000])).pack()
        self.name_l = Label(self.root, text='新昵称:').pack()
        self.name = Entry(self.root)
        self.name.pack()
        self.nameB = Button(self.root, text='修改', command=lambda: self.修改器(['name', self.name.get()])).pack()
        self.root.mainloop()

    def 修改器(self, cmd):
        cmd1 = cmd[0]
        data = cmd[1]
        if cmd1 == 'EXP':
            DE.Player_Mian.exp = DE.Player_Mian.exp + data
        elif cmd1 == 'TQ':
            DE.Player_Mian.铜 = DE.Player_Mian.铜 + data
        elif cmd1 == 'HG':
            DE.Player_Mian.金 = DE.Player_Mian.金 + data
        elif cmd1 == 'GY':
            DE.Player_Mian.玉 = DE.Player_Mian.玉 + data
        elif cmd1 == 'name':
            DE.Player_Mian.name = data
            普通弹窗('昵称修改成功', data)

    def 归零(self, cmd):

        cmd = cmd[0]

        if cmd == 'EXP':
            DE.Player_Mian.exp = 0
        elif cmd == 'TQ':
            DE.Player_Mian.铜 = 0
        elif cmd == 'HG':
            DE.Player_Mian.金 = 0
        elif cmd == 'GY':
            DE.Player_Mian.玉 = 0


def 弹出提示弹窗():  # 测试用函数
    T提示弹窗()


def 触发掉落():  # 测试函数
    DL = 掉落弹窗(list={'Y': 1, 'G': 1, 'T': 1, 'Exp': 1})


class 判断弹窗():
    def __init__(self, OK, text='提示弹窗'):
        # print('判断弹窗建立完成', text, OK)
        self.OK = OK

        self.FM = LabelFrame(DE.当前场景.frame, text='确认', fg='SkyBlue', height=200, width=604, bg='white')
        self.FM.place(x=383, y=0)
        # bg = 'white' 背景白色，fg='SkyBlue' 字体天蓝色

        self.提示文本 = Label(self.FM, text=text, font=DE.提示font, bg='white', wraplength=580, justify=LEFT)
        # wraplength = 580,文本宽度达到580换行， justify = LEFT 最后一排靠左。
        self.提示文本.place(x=10, y=10)

        self.NO_P = Open_Jpg(os.path.join('Resource', 'picture', 'ui', f'PD_NO.jpg'))
        self.OFFBUUT = Button(self.FM, image=self.NO_P, command=self.FM.destroy, relief=FLAT, bg='white')
        self.OFFBUUT.place(y=130, x=508)

        self.YES_P = Open_Jpg(os.path.join('Resource', 'picture', 'ui', f'PD_OK.jpg'))
        '''注意这里的OK，是将业务流封装后绑定给确定按钮'''
        self.OKBUUT = Button(self.FM, image=self.YES_P, relief=FLAT, bg='white', command=self.OKC)
        self.OKBUUT.place(x=1, y=130)

    def OKC(self):
        self.OK()
        self.FM.destroy()

        # print('提示弹窗创建完成！')


class T提示弹窗():
    def __init__(self, text='警告'):  # text = 窗口内提示语
        self.FM = LabelFrame(DE.当前场景.frame, text='提示', fg='SkyBlue', height=200, width=604, bg='white')
        # bg = 'white' 背景白色，fg='SkyBlue' 字体天蓝色
        self.FM.place(x=383, y=0)
        self.NO_P = Open_Jpg(os.path.join('Resource', 'picture', 'ui', f'PD_OK.jpg'))
        # 确定按钮只是为了关闭窗口
        self.OFFBUUT = Button(self.FM, image=self.NO_P, command=self.FM.destroy, relief=FLAT, bg='white')
        self.OFFBUUT.place(y=130, x=282)
        self.提示文本 = Label(self.FM, text=text, font=DE.提示font, bg='white', wraplength=580, justify=LEFT)
        # wraplength = 580,文本宽度达到580换行， justify = LEFT 最后一排靠左。
        self.提示文本.place(x=10, y=10)


class 掉落弹窗():
    '''用一个字典类型的数据创建掉落窗口对象实现掉落，调用时注意数据刷新顺序'''

    def __init__(self, list):
        # 掉落数据样式
        # list={'Y':0,'G':0,'T':0,'Exp':0}
        self.list = list
        print(f'掉落原始数据{list}')
        self.FM = LabelFrame(DE.当前场景.frame, text='获得资源', fg='SkyBlue', height=200, width=1100, bg='black')
        self.FM.place(x=133, y=280)
        self.NO_P = Open_Jpg(os.path.join('Resource', 'picture', 'ui', f'PD_OK_DL.jpg'))
        self.OFFBUUT = Button(self.FM, image=self.NO_P, command=self.FM.destroy, relief=FLAT, bg='white', bd=0)
        self.OFFBUUT.place(y=130, x=510)
        self.FM2 = Frame(self.FM, bg='white', height=100, width=1100)
        self.FM2.place(x=0, y=50)
        self.创建掉落数据()
        # print('掉落数据',self.list)

    def 创建掉落数据(self):
        self.资源UIX = 70
        self.资源UIY = 728
        '''根据字典内的数据创建对应的游戏资源图标，图标创建完成后将执行资源变更'''
        if self.list.get('Y') != 0:  # 为0时不创建
            # print('Y')
            self.勾玉FM = Frame(self.FM2, bg='black', height=40, width=250)
            self.勾玉P_P = Open_Jpg(os.path.join('Resource', 'picture', 'ui', f'P_UI_Y.jpg'))
            self.勾玉_P = Label(self.勾玉FM, image=self.勾玉P_P, relief='solid')
            self.勾玉_P.place(x=0, y=0)
            self.勾玉S = StringVar()
            self.勾玉S.set(str(self.list.get('Y')))
            self.勾玉L = Label(self.勾玉FM, textvariable=self.勾玉S, font=DE.资源font, fg='SkyBlue', bg='black')
            self.勾玉L.place(x=120, y=0)
            self.勾玉FM.pack(side=LEFT)
            # 执行数据变更，已实装

            DE.Player_Mian.info()
            DE.Player_Mian.玉 = DE.Player_Mian.玉 + self.list.get('Y')

        if self.list.get('G') != 0:
            # print('G')
            self.黄金FM = Frame(self.FM2, bg='black', height=40, width=250)
            self.黄金P_P = Open_Jpg(os.path.join('Resource', 'picture', 'ui', f'P_UI_G.jpg'))
            self.黄金_P = Label(self.黄金FM, image=self.黄金P_P, relief='solid')
            self.黄金_P.place(x=0, y=0)
            self.黄金S = StringVar()
            self.黄金S.set(str(int(self.list.get('G') * DE.收益修正)))
            self.黄金L = Label(self.黄金FM, textvariable=self.黄金S, font=DE.资源font, fg='SkyBlue', bg='black').place(x=120,
                                                                                                               y=0)
            self.黄金FM.pack(side=LEFT)
            # 执行数据变更
            DE.Player_Mian.金 = DE.Player_Mian.金 + int((self.list.get('G') * DE.收益修正))

        if self.list.get('T') != 0:
            # print('T')
            self.铜钱FM = Frame(self.FM2, bg='black', height=40, width=250)
            self.铜钱P_P = Open_Jpg(os.path.join('Resource', 'picture', 'ui', f'P_UI_T.jpg'))
            self.铜钱_P = Label(self.铜钱FM, image=self.铜钱P_P, relief='solid')
            self.铜钱_P.place(x=0, y=0)
            self.铜钱S = StringVar()
            self.铜钱S.set(str(int(self.list.get('T') * DE.收益修正)))
            self.铜钱L = Label(self.铜钱FM, textvariable=self.铜钱S, font=DE.Exp_font, fg='SkyBlue', bg='black').place(x=120,
                                                                                                                 y=8)
            self.铜钱FM.pack(side=LEFT)
            # 执行数据变更
            DE.Player_Mian.铜 = DE.Player_Mian.铜 + int((self.list.get('T') * DE.收益修正))

        if self.list.get('Exp') != 0:
            print('Exp')
            self.ExpFM = Frame(self.FM2, bg='black', height=40, width=250)
            self.ExpP_P = Open_Jpg(os.path.join('Resource', 'picture', 'ui', f'P_UI_EXP.jpg'))
            self.Exp_P = Label(self.ExpFM, image=self.ExpP_P, relief='solid')
            self.Exp_P.place(x=0, y=0)
            self.ExpS = StringVar()
            self.ExpS.set(str(int(self.list.get('Exp') * DE.收益修正)))
            self.ExpL = Label(self.ExpFM, textvariable=self.ExpS, font=DE.Exp_font, fg='SkyBlue', bg='black').place(
                x=120,
                y=8)
            self.ExpFM.pack(side=LEFT)
            # 执行数据变更
            DE.Player_Mian.exp = DE.Player_Mian.exp + int((self.list.get('Exp') * DE.收益修正))

        DE.Player_Mian.info()
        DE.收益修正 = 1


def 创建元神大图(name, Code):
    元神大图(name, Code)


# 穿戴装备用，用于元神操作界面显示装备信息界面，用于执行穿戴装备和替换装备回收流程
class 装备小图标():
    def __init__(self, win, E, x, y, G, CMD):
        self.CMD = CMD
        self.目标G = G
        self.win = win
        self.E = E
        self.Buut_P = Open_Jpg(os.path.join('Resource', 'picture', 'Equipment', f'{self.E.Code}-c.jpg'))
        self.Buut = Button(self.win, image=self.Buut_P, relief=FLAT, command=self.打开装备详细面板)
        self.Buut.place(x=x, y=y)

    def destroy(self):
        self.Buut.destroy()

    def 打开装备详细面板(self):
        try:
            self.装备显示容器.destroy()
        except:
            pass
        self.装备名称文本 = StringVar()
        try:
            if self.E.强化等级 == 0:
                self.装备名称文本.set(self.E.name)

            else:
                self.装备名称文本.set('+' + str(self.E.强化等级) + self.E.name)
        except:
            self.E.强化等级 = 0
            self.装备名称文本.set(self.E.name)

        self.装备显示容器 = LabelFrame(self.win, text=self.E.name + ' ' + self.E.ID, height=250, width=300, bg='white')
        self.装备图标_P = Open_Jpg(os.path.join('Resource', 'picture', 'Equipment', f'{self.E.Code}.jpg'))
        self.装备图标 = Label(self.装备显示容器, image=self.装备图标_P)
        self.装备图标.place(x=0, y=0)
        self.装备名称 = Label(self.装备显示容器, textvariable=self.装备名称文本, font=('Aridl', 10), bg='white',
                          fg=DE.装备字体颜色.get(self.E.品级)).place(x=160, y=0)
        # self.装备品级 = Label(self.装备显示容器, text=self.E.品级, bg='white').place(x=240, y=0)
        self.装备属性 = Label(self.装备显示容器, text=self.E.获得装备属性(), justify=LEFT, bg='white').place(x=160, y=20)
        self.装备 = Button(self.装备显示容器, text='装备', relief=FLAT, bg='white', fg='red', command=self.穿戴装备).place(x=255,
                                                                                                             y=125)
        self.取消 = Button(self.装备显示容器, text='取消', relief=FLAT, bg='white', command=self.装备显示容器.destroy).place(x=255,
                                                                                                             y=155)
        self.装备显示容器.place(x=135, y=100)

    def 穿戴装备(self):
        '''用于给对象属性赋值'''
        if self.目标G.装备 != None:
            DE.Player_Mian.装备组.append(self.目标G.装备)
        self.目标G.装备 = self.E
        # print(self.目标G.name, self.E.ID)
        DE.Player_Mian.装备组.remove(self.E)
        # self.装备显示容器.destroy()
        self.CMD()
        切换场景(Genshin_view)


# 用于阵容显示元神头像
class 元神信息卡片():
    def __init__(self, G, FM, x, y):
        self.G = G
        self.G_ICO_P = Open_Jpg(os.path.join('Resource', 'picture', 'Genshin', f'{self.G.Code}-c.jpg'))
        self.G_ICO = Button(FM, image=self.G_ICO_P, command=lambda: self.弹出信息(FM))
        self.G_ICO.place(x=x, y=y)

    def destroy(self):
        self.G_ICO.destroy()

    def 弹出信息(self, FM):
        self.元神_FM = LabelFrame(FM, text=self.G.name + '  *  ' + self.G.ID + '*' + self.G.等级, height=370,
                                width=604, bg='white', )
        # bg='white' 白色背景
        self.元神_FM.place(x=0, y=70)
        # self.宿敌_FM.config(bg='red')
        # 立绘
        self.LH_P = Open_Jpg(os.path.join('Resource', 'picture', 'Genshin', f'{self.G.Code}-x.jpg'))  # 元神小立绘
        self.LH = Label(self.元神_FM, image=self.LH_P)
        self.LH.place(x=5, y=0)
        # 装备图标
        if self.G.装备 == None:
            self.ZBLH_P = Open_Jpg(os.path.join('Resource', 'picture', 'Equipment', f'O.jpg'))
        else:
            self.ZBLH_P = Open_Jpg(os.path.join('Resource', 'picture', 'Equipment', f'{self.G.装备.Code}.jpg'))
            if self.G.装备.强化等级 != 0:
                self.ENAMEL = Label(self.元神_FM, text='+' + str(self.G.装备.强化等级) + self.G.装备.name + '-' + self.G.装备.ID,
                                    bg='white', fg=DE.装备字体颜色.get(self.G.装备.品级)).place(x=220, y=185)
            else:
                self.ENAMEL = Label(self.元神_FM, text=self.G.装备.name + '-' + self.G.装备.ID,
                                    bg='white', fg=DE.装备字体颜色.get(self.G.装备.品级)).place(x=220, y=185)
            self.ELL = Label(self.元神_FM, text='力量+' + str(self.G.装备.力量), bg='white').place(x=220, y=205)
            self.EZH = Label(self.元神_FM, text='智慧+' + str(self.G.装备.智慧), bg='white').place(x=310, y=205)
            self.ETL = Label(self.元神_FM, text='体力+' + str(self.G.装备.体力), bg='white').place(x=220, y=225)
            self.EMJ = Label(self.元神_FM, text='敏捷+' + str(self.G.装备.敏捷), bg='white').place(x=310, y=225)

            self.ELLZ = Label(self.元神_FM, text='力量强化+' + str(self.G.装备.力量资质), bg='white').place(x=220, y=245)
            self.EZZH = Label(self.元神_FM, text='智慧强化+' + str(self.G.装备.智慧资质), bg='white').place(x=220, y=265)
            self.ETLZ = Label(self.元神_FM, text='体力强化+' + str(self.G.装备.体力资质), bg='white').place(x=220, y=285)
            self.ETLZ = Label(self.元神_FM, text='敏捷强化+' + str(self.G.装备.敏捷资质), bg='white').place(x=220, y=305)
            self.ETLZ = Label(self.元神_FM, text='成色；' + str(self.G.装备.完美程度), bg='white').place(x=310, y=305)
        self.ZBLH = Label(self.元神_FM, image=self.ZBLH_P, relief=FLAT)
        self.ZBLH.place(x=215, y=3)
        # 属性
        self.属性词条 = []  # 该变量未使用
        x = 385
        self.昵称 = Label(self.元神_FM, text=self.G.name, font=('Aridl', 13), bg='white').place(x=x, y=0)

        self.S_LV = StringVar()
        self.S_LV.set('Lv: ' + str(self.G.Lv))
        self.Lv = Label(self.元神_FM, textvariable=self.S_LV, bg='white').place(x=x, y=25)

        self.S_伤害类型 = StringVar()
        try:
            self.S_伤害类型.set('伤害类型：' + self.G.伤害类型)
        except:
            self.S_伤害类型.set('无')
        self.伤害类型 = Label(self.元神_FM, textvariable=self.S_伤害类型, bg='white').place(x=x + 100, y=25)

        self.S_HP = StringVar()
        self.S_HP.set('HP: ' + str(self.G.HP))
        self.HP = Label(self.元神_FM, textvariable=self.S_HP, bg='white').place(x=x, y=45)
        # 基础属性
        self.S_力量 = StringVar()
        self.S_力量.set('力量: ' + str(self.G.力量) + '    ')
        self.力量 = Label(self.元神_FM, textvariable=self.S_力量, bg='white').place(x=x, y=65)

        self.S_智慧 = StringVar()
        self.S_智慧.set('智慧: ' + str(self.G.智慧))
        self.智慧 = Label(self.元神_FM, textvariable=self.S_智慧, bg='white').place(x=x + 100, y=65)

        self.S_体力 = StringVar()
        self.S_体力.set('体力: ' + str(self.G.体力))
        self.体力 = Label(self.元神_FM, textvariable=self.S_体力, bg='white').place(x=x, y=85)

        self.S_敏捷 = StringVar()
        self.S_敏捷.set('敏捷: ' + str(self.G.敏捷))
        self.敏捷 = Label(self.元神_FM, textvariable=self.S_敏捷, bg='white').place(x=x + 100, y=85)

        # 属性资质
        self.S_力量资质 = StringVar()
        self.S_力量资质.set('力量资质: ' + str(self.G.力量资质))
        self.力量资质 = Label(self.元神_FM, textvariable=self.S_力量资质, bg='white').place(x=x, y=125)

        self.S_智慧资质 = StringVar()
        self.S_智慧资质.set('' + '智慧资质: ' + str(self.G.智慧资质))
        self.智慧资质 = Label(self.元神_FM, textvariable=self.S_智慧资质, bg='white').place(x=x + 100, y=125)

        self.S_体力资质 = StringVar()
        self.S_体力资质.set('体力资质: ' + str(self.G.体力资质))
        self.体力资质 = Label(self.元神_FM, textvariable=self.S_体力资质, bg='white').place(x=x, y=105)

        self.S_敏捷资质 = StringVar()
        self.S_敏捷资质.set('敏捷资质: ' + str(self.G.敏捷资质))
        self.敏捷资质 = Label(self.元神_FM, textvariable=self.S_敏捷资质, bg='white').place(x=x + 100, y=105)

        # 后天属性
        self.S_后天属性 = StringVar()
        self.S_后天属性.set('后天属性：' + self.G.后天属性)
        self.后天属性 = Label(self.元神_FM, textvariable=self.S_后天属性, bg='white').place(x=x, y=145)

        # 战斗属性
        self.S_物理攻击 = StringVar()
        self.S_物理攻击.set('物理攻击: ' + str(self.G.物理攻击))
        self.物理攻击 = Label(self.元神_FM, textvariable=self.S_物理攻击, bg='white').place(x=x, y=165)

        self.S_法术攻击 = StringVar()
        self.S_法术攻击.set('法术攻击: ' + str(self.G.法术攻击))
        self.法术攻击 = Label(self.元神_FM, textvariable=self.S_法术攻击, bg='white').place(x=x, y=185)

        self.S_命中 = StringVar()
        self.S_命中.set('命中: ' + str(self.G.命中))
        self.命中 = Label(self.元神_FM, textvariable=self.S_命中, bg='white').place(x=x, y=205)

        self.S_闪避 = StringVar()
        self.S_闪避.set('闪避: ' + str(self.G.闪避))
        self.闪避 = Label(self.元神_FM, textvariable=self.S_闪避, bg='white').place(x=x + 100, y=205)

        self.加入按钮 = Button(self.元神_FM, text='加入', bg='white', fg='red', command=self.加入)
        self.加入按钮.place(x=x, y=250)

        self.关闭按钮 = Button(self.元神_FM, text='关闭', bg='white', fg='red', command=self.元神_FM.destroy)
        self.关闭按钮.place(x=x + 100, y=250)

    def 加入(self):
        if self.G in DE.阵容:  # 判断是否已在阵容内
            pass
        else:
            if len(DE.阵容) < DE.阵容数量:
                DE.阵容.append(self.G)
                DE.当前场景.刷新阵容()
                self.元神_FM.destroy()


# 用于阵容团队管理
class 阵容按钮():
    def __init__(self, G, FM, x, y):
        self.G = G
        self.ICO_P = Open_Jpg(os.path.join('Resource', 'picture', 'Genshin', f'{self.G.Code}-c.jpg'))
        self.ICO = Button(FM, image=self.ICO_P, command=self.删除)
        self.ICO.place(x=x, y=y)

    def 删除(self):
        DE.阵容.remove(self.G)
        DE.刷新阵容()

    def destroy(self):
        self.ICO.destroy()


class 元神大图():
    def __init__(self, name, Code, PJ):
        self.root = Toplevel()
        self.root.title(f'{name} {PJ}')
        self.P = Open_Jpg(os.path.join('Resource', 'picture', 'Genshin', f'{Code}-d.jpg'))
        self.L = Label(self.root, image=self.P).pack()
        self.root.mainloop()


# 用于元神单独小窗口呼出，元神各种操作
class 元神操作视图():
    def __init__(self, G):
        self.G = G
        # print(G.__dict__)
        self.FM = LabelFrame(DE.当前场景.frame, text=self.G.name + '  *  ' + self.G.ID + '*' + self.G.等级, height=380,
                             width=604, bg='white')
        # bg='white' 白色背景
        self.FM.place(x=383, y=232)
        self.LH_P = Open_Jpg(os.path.join('Resource', 'picture', 'Genshin', f'{self.G.Code}-x.jpg'))  # 元神小立绘
        self.LH = Label(self.FM, image=self.LH_P)
        self.LH.place(x=5, y=0)
        self.X_B = Button(self.FM, text='X', command=self.用于关闭)
        self.X_B.place(x=580, y=0)
        self.创建装备图标()
        self.创建属性词条()
        self.创建操作按钮()

    def 用于关闭(self):
        self.FM.destroy()
        try:
            self.显示装备列表面板.destroy()
        except:
            pass

    def 创建装备图标(self):  # 临时用，装备功能尚未实装
        if self.G.装备 == None:
            self.ZBLH_P = Open_Jpg(os.path.join('Resource', 'picture', 'Equipment', f'O.jpg'))
        else:
            self.ZBLH_P = Open_Jpg(os.path.join('Resource', 'picture', 'Equipment', f'{self.G.装备.Code}.jpg'))
            if self.G.装备.强化等级 != 0:
                self.ENAMEL = Label(self.FM, text='+' + str(self.G.装备.强化等级) + self.G.装备.name + '-' + self.G.装备.ID,
                                    bg='white', fg=DE.装备字体颜色.get(self.G.装备.品级)).place(x=220, y=185)
            else:
                self.ENAMEL = Label(self.FM, text=self.G.装备.name + '-' + self.G.装备.ID,
                                    bg='white', fg=DE.装备字体颜色.get(self.G.装备.品级)).place(x=220, y=185)
            self.ELL = Label(self.FM, text='力量+' + str(self.G.装备.力量), bg='white').place(x=220, y=205)
            self.EZH = Label(self.FM, text='智慧+' + str(self.G.装备.智慧), bg='white').place(x=310, y=205)
            self.ETL = Label(self.FM, text='体力+' + str(self.G.装备.体力), bg='white').place(x=220, y=225)
            self.EMJ = Label(self.FM, text='敏捷+' + str(self.G.装备.敏捷), bg='white').place(x=310, y=225)

            self.ELLZ = Label(self.FM, text='力量强化+' + str(self.G.装备.力量资质), bg='white').place(x=220, y=245)
            self.EZZH = Label(self.FM, text='智慧强化+' + str(self.G.装备.智慧资质), bg='white').place(x=220, y=265)
            self.ETLZ = Label(self.FM, text='体力强化+' + str(self.G.装备.体力资质), bg='white').place(x=220, y=285)
            self.ETLZ = Label(self.FM, text='敏捷强化+' + str(self.G.装备.敏捷资质), bg='white').place(x=220, y=305)
            self.ETLZ = Label(self.FM, text='成色；' + str(self.G.装备.完美程度), bg='white').place(x=310, y=305)
        self.ZBLH = Button(self.FM, image=self.ZBLH_P, relief=FLAT, command=self.创建装备穿戴面板)
        self.ZBLH.place(x=215, y=3)

    def 创建装备穿戴面板(self):
        try:
            self.显示装备列表面板.destroy()
        except:
            pass

        def 翻页(页码=1):
            self.页码 = 页码
            if self.页码 > 1:
                self.上一页 = Button(self.显示装备列表面板, text='上一页', command=lambda: 翻页(self.页码 - 1), relief=FLAT).place(x=380,
                                                                                                                 y=排序按钮y)
            elif self.页码 == 1:
                self.上一页 = Button(self.显示装备列表面板, text='上一页', relief=FLAT).place(x=380, y=排序按钮y)

            if len(DE.Player_Mian.装备组) < self.页码 * 25:
                self.下一页 = Button(self.显示装备列表面板, text='下一页', relief=FLAT).place(x=320, y=排序按钮y)
            else:
                self.下一页 = Button(self.显示装备列表面板, text='下一页', command=lambda: 翻页(self.页码 + 1), relief=FLAT).place(x=320,
                                                                                                                 y=排序按钮y)

            for i in self.E_ICO_C:
                i.destroy()
            x = 0
            y = 0
            if len(DE.Player_Mian.装备组) > 页码 * 25:  # 大于60个将进行分页

                for i in DE.Player_Mian.装备组[(页码 * 25 - 25):(页码 * 25)]:
                    self.E_B = 装备小图标(self.显示装备列表面板, i, x, y, self.G, self.创建装备穿戴面板)
                    self.E_ICO_C.append(self.E_B)
                    x = x + 110
                    if x > 500:
                        y = y + 110
                        x = 0
            else:
                for i in DE.Player_Mian.装备组[(页码 * 24 - 24)::]:
                    self.E_B = 装备小图标(self.显示装备列表面板, i, x, y, self.G, self.创建装备穿戴面板)
                    self.E_ICO_C.append(self.E_B)
                    x = x + 110
                    if x > 500:
                        y = y + 110
                        x = 0

        def 关闭():
            self.显示装备列表面板.destroy()
            try:
                self.FM.place(x=383, y=232)
            except:
                pass

        排序按钮y = 630
        self.FM.place(x=183, y=232)
        self.显示装备列表面板 = LabelFrame(DE.当前场景.frame, text=f'{self.G.name}-{self.G.ID}' + '更换装备', height=710, width=570,
                                   bg='white')
        self.显示装备列表面板.place(x=790, y=10)
        self.关闭按钮 = Button(self.显示装备列表面板, text='X', command=关闭).place(y=0, x=550)
        self.E_ICO_C = []
        # self.排序_HP_P = Open_Jpg(os.path.join('Resource','picture','ui',f'G_PX_MP.jpg'))
        self.排序_HP = Button(self.显示装备列表面板, text='力量加强', command=self.E_LIST_L, relief=FLAT).place(x=10, y=排序按钮y)

        # self.排序_WL_P = Open_Jpg(os.path.join('Resource','picture','ui',f'G_PX_WL.jpg'))
        self.排序_WL = Button(self.显示装备列表面板, text='智力加强', command=self.E_LIST_ZL, relief=FLAT).place(x=100, y=排序按钮y)

        # self.排序_FS_P = Open_Jpg(os.path.join('Resource','picture','ui',f'G_PX_FS.jpg'))
        self.排序_FS = Button(self.显示装备列表面板, text='体力加强', command=self.E_LIST_TL, relief=FLAT).place(x=190, y=排序按钮y)

        # self.排序_MZ_P = Open_Jpg(os.path.join('Resource','picture','ui',f'G_PX_MZ.jpg'))
        self.排序_MZ = Button(self.显示装备列表面板, text='敏捷加强', command=self.E_LIST_MJ, relief=FLAT).place(x=280, y=排序按钮y)

        # self.排序_S_P = Open_Jpg(os.path.join('Resource','picture','ui',f'G_PX_SB.jpg'))
        self.排序_S = Button(self.显示装备列表面板, text='完美程度', command=self.E_LIST_WM, relief=FLAT).place(x=370, y=排序按钮y)
        翻页()
        if self.页码 > 1:
            self.上一页 = Button(self.显示装备列表面板, text='上一页', command=lambda: 翻页(self.页码 - 1), relief=FLAT).place(x=380,
                                                                                                             y=排序按钮y)
        else:
            self.上一页 = Button(self.显示装备列表面板, text='上一页', relief=FLAT).place(x=380, y=排序按钮y)
        if len(DE.Player_Mian.装备组) > self.页码 * 25:
            self.下一页 = Button(self.显示装备列表面板, text='下一页', command=lambda: 翻页(self.页码 + 1), relief=FLAT).place(x=320,
                                                                                                             y=排序按钮y)
        else:
            self.下一页 = Button(self.显示装备列表面板, text='下一页', relief=FLAT).place(x=320, y=排序按钮y)

        '''显示字符 '排序方式' '''
        self.排序_L = Label(self.显示装备列表面板, text=f'排序方式' + f'   共计装备:{len(DE.Player_Mian.装备组)} 件') \
            .place(x=11, y=排序按钮y - 25)

    def E_LIST_MJ(self):
        # 列表排序 #x 对象属性
        DE.Player_Mian.装备组 = sorted(DE.Player_Mian.装备组, key=lambda x: x.敏捷资质, reverse=True)
        # for i in list:
        # print(i.HP)
        self.显示装备列表面板.destroy()
        self.创建装备穿戴面板()

    def E_LIST_WM(self):
        # 列表排序 #x 对象属性
        DE.Player_Mian.装备组 = sorted(DE.Player_Mian.装备组, key=lambda x: x.完美程度, reverse=True)
        # for i in list:
        # print(i.HP)
        self.显示装备列表面板.destroy()
        self.创建装备穿戴面板()

    def E_LIST_TL(self):
        # 列表排序 #x 对象属性
        DE.Player_Mian.装备组 = sorted(DE.Player_Mian.装备组, key=lambda x: x.体力资质, reverse=True)
        # for i in list:
        # print(i.HP)
        self.显示装备列表面板.destroy()
        self.创建装备穿戴面板()

    def E_LIST_L(self):

        DE.Player_Mian.装备组 = sorted(DE.Player_Mian.装备组, key=lambda x: x.力量资质, reverse=True)
        # for i in list:
        # print(i.HP)
        self.显示装备列表面板.destroy()
        self.创建装备穿戴面板()

    def E_LIST_ZL(self):
        DE.Player_Mian.装备组 = sorted(DE.Player_Mian.装备组, key=lambda x: x.智慧资质, reverse=True)
        # for i in list:
        # print(i.HP)
        self.显示装备列表面板.destroy()
        self.创建装备穿戴面板()

        #

    # 其他窗口弹出方法封装
    def 创建判断弹窗(self, OK, text):
        # 将业务流封装绑定给判断窗口，判断窗口确认后才会继续执行
        self.判断弹窗 = 判断弹窗(OK, text=text)

    def 创建提示弹窗(self, text):
        '''将弹出提示窗口封装成类方法，而不是在按钮触发函数内创建提示窗口对象'''
        self.提示弹窗 = T提示弹窗(text)

    def 删除后获得资源(self, list):
        '''将元神放逐后获得资源的过程封装成类方法'''
        '''用掉落数据创建掉落窗口'''
        self.LL掉落弹窗 = 掉落弹窗(list)

    # 以上全是弹出其他窗口的函数

    def 创建操作按钮(self):
        # 操作面板内按钮方法函数封装
        def 删除元神(G):
            # 触发掉落()
            # self.创建提示弹窗(OK)

            def OK():  # 业务流封装到判断窗口的确认按钮上
                '''下面是根据元神品级分级判断获得资源'''
                if self.G.等级 == 'B':
                    list = {'Y': 0, 'G': 0, 'T': 0, 'Exp': (1000 + (self.G.Lv * 100))}
                    # self.删除后获得资源(list)
                elif self.G.等级 == 'A':
                    list = {'Y': 0, 'G': 0, 'T': 5000, 'Exp': (1000 + (self.G.Lv * 100))}
                    # self.删除后获得资源(list)
                    # text = f'   请确认是否要放逐{self.G.name},放逐后你将获得5000 铜币和{(1000 + (self.G.Lv * 100))} Exp。'

                elif self.G.等级 == 'S':
                    list = {'Y': 0, 'G': 100, 'T': 20000, 'Exp': (1000 + (self.G.Lv * 100))}
                    # self.删除后获得资源(list)
                    # text = f'   请确认是否要放逐{self.G.name},放逐后你将获得100 黄金、20000 铜币和{(1000 + (self.G.Lv * 100))} Exp。'
                elif self.G.等级 == 'S1':
                    list = {'Y': 10, 'G': 200, 'T': 50000, 'Exp': (1000 + (self.G.Lv * 100))}
                    # self.删除后获得资源(list)
                    # text = f'   请确认是否要放逐{self.G.name},放逐后你将获得10勾玉、200 黄金、50000 铜币和{(1000 + (self.G.Lv * 100))} Exp。'
                elif self.G.等级 == 'SS':
                    list = {'Y': 30, 'G': 600, 'T': 60000, 'Exp': (1000 + (self.G.Lv * 100))}
                    # self.删除后获得资源(list)
                    # text = f'   请确认是否要放逐{self.G.name},放逐后你将获得30勾玉、600 黄金、60000 铜币和{(1000 + (self.G.Lv * 100))} Exp。'
                # DE.Player_Mian.exp = DE.Player_Mian.exp + (1000 + (self.G.Lv*100)) #收回经验
                '''把当前元神从列表中删除，关闭元神操作面板，刷新元神视图'''
                if G.装备 != None:
                    DE.Player_Mian.装备组.append(G.装备)  # 回收装备
                DE.Player_Mian.元神组.remove(G)
                '''注意此处业务流程，先执行删除，然后关闭操作面板，刷新元神视图场景，弹出资源页面，在刷新资源UI'''
                '''若先弹出资源页面在刷新场景会出现资源页面消失'''
                '''先刷新UI资源显示在弹出资源页面会UI资源更新不及时'''
                self.FM.destroy()
                # 切换场景(Genshin_view)
                DE.当前场景.翻页(DE.当前场景.ABCD)
                self.删除后获得资源(list)
                DE.当前场景.刷新资源UI()

            if self.G.等级 == 'B':
                text = f'   请确认是否要放逐{self.G.name},放逐后你将获得{(1000 + (self.G.Lv * 100))} Exp。'
            elif self.G.等级 == 'A':
                text = f'   请确认是否要放逐{self.G.name},放逐后你将获得5000 铜币和{(1000 + (self.G.Lv * 100))} Exp。'

            elif self.G.等级 == 'S':
                text = f'   请确认是否要放逐{self.G.name},放逐后你将获得100 黄金、20000 铜币和{(1000 + (self.G.Lv * 100))} Exp。'
            elif self.G.等级 == 'S1':
                text = f'   请确认是否要放逐{self.G.name},放逐后你将获得10勾玉、200 黄金、50000 铜币和{(1000 + (self.G.Lv * 100))} Exp。'
            elif self.G.等级 == 'SS':
                text = f'   请确认是否要放逐{self.G.name},放逐后你将获得30勾玉、600 黄金、60000 铜币和{(1000 + (self.G.Lv * 100))} Exp。'

            self.创建判断弹窗(OK, text)

        def 转换伤害类型():
            '''调用对象方法重新设置属性，然后刷新词条'''

            # 转换开销
            Overhead = {'B': 800, 'A': 1500, 'S': 2000, 'S1': 2500, 'SS': 3000}

            if DE.Player_Mian.金 >= Overhead.get(self.G.等级):  # 判断金是否够使用
                DE.Player_Mian.金 = DE.Player_Mian.金 - Overhead.get(self.G.等级)  # 向Overhead获取各品级所需开销
                self.G.转换伤害类型()  # 执行元神类方法
                self.刷新属性词条()  # 执行元神操作面板词条属性刷新
                DE.当前场景.刷新资源UI()  # 执行UI资源显示刷新
            else:  # 开销不足时弹窗提示
                # self.创建提示弹窗(f'资源不足，{self.G.等级}级元神转换伤害类型需要{Overhead.get(self.G.等级)}黄金。')
                pass

        def 元神升级():
            '''等级加一，初始化后天属性，刷新词条'''
            Overhead = {'B': 5000, 'A': 6000, 'S': 7000, 'S1': 8000, 'SS': 10000}
            '''扣除经验，已实装'''
            DE.Player_Mian.exp = DE.Player_Mian.exp - int((1 + (1 + self.G.Lv * 1.130)) * Overhead.get(self.G.等级))
            '''执行升级'''
            self.G.Lv = self.G.Lv + 1
            self.G.初始化基础属性()
            self.G.初始化战斗属性()
            self.刷新属性词条()
            '''判断按钮是否需要关闭'''
            if self.G.Lv >= 40:  # 40级后关闭升级按钮
                self.元神升级按钮.config(state=DISABLED)
            if DE.Player_Mian.exp < int((1 + (1 + self.G.Lv * 1.130)) * Overhead.get(self.G.等级)):  # 所需经验不足关闭升级按钮
                self.元神升级按钮.config(state=DISABLED)

            DE.当前场景.刷新资源UI()  # 刷新UI资源显示

        def 鉴赏():
            self.GB_P = Open_Jpg(os.path.join('Resource', 'picture', 'Genshin', f'{self.G.Code}-d.jpg'))
            大图宽 = self.GB_P.width()
            if 大图宽 < 1366:
                放置位置 = (1366 - 大图宽) / 2
            else:
                放置位置 = 0
            self.GB = Label(DE.当前场景.frame, image=self.GB_P)
            self.GB.place(x=放置位置, y=0)
            # self.GB_C = Button(self.GB_FM, text='查看')

            颜色 = {'B': 'chartreuse', 'A': 'cyan', 'S': '', 'S1': '', 'SS': ''}

            def off():
                self.GB.destroy()
                self.GLFM.destroy()

            self.GLFM = Frame(DE.当前场景.frame)
            self.GLFM.place(x=1230, y=660)
            self.GL_name = Label(self.GLFM, text=self.G.name, font=('Aridl', 13))
            self.GL_name.pack()
            # self.GL_等级 = Label(self.GLFM, text=self.G.等级, font=('Aridl', 13))
            # self.GL_等级.pack()
            self.GBB = Button(self.GLFM, text='关闭', command=off)
            self.GBB.pack()

        # 创建操作按钮
        # self.操作按钮区域 = Frame(self.FM,height=60, width=200).place(x=385,y=245)
        self.转换伤害类型_P = Open_Jpg(os.path.join('Resource', 'picture', 'ui', f'G_CZ_ZH.jpg'))
        self.元神升级按钮_P = Open_Jpg(os.path.join('Resource', 'picture', 'ui', f'G_CZ_UP.jpg'))
        self.删除元神按钮_P = Open_Jpg(os.path.join('Resource', 'picture', 'ui', f'G_CZ_FZ.jpg'))
        self.鉴赏功能_P = Open_Jpg(os.path.join('Resource', 'picture', 'ui', f'G_CZ_JS.jpg'))

        self.转换伤害类型 = Button(self.FM, image=self.转换伤害类型_P, command=转换伤害类型, relief=FLAT)
        self.转换伤害类型.place(x=385 + 50, y=228)

        self.删除元神按钮 = Button(self.FM, image=self.删除元神按钮_P, command=lambda: 删除元神(self.G), relief=FLAT)
        self.删除元神按钮.place(x=385 + 100, y=228)
        Overhead = {'B': 1000, 'A': 2000, 'S': 3000, 'S1': 5000, 'SS': 10000}
        '''判断是否激活升级按钮，所需经验不足时将停用升级按钮'''
        '''等级超过40级时也将停用升级按钮'''
        if self.G.Lv < 40 and DE.Player_Mian.exp >= int(int((1 + (1 + self.G.Lv * 1.130)) * Overhead.get(self.G.等级))):
            self.元神升级按钮 = Button(self.FM, image=self.元神升级按钮_P, command=元神升级, relief=FLAT)
        else:
            self.元神升级按钮 = Button(self.FM, image=self.元神升级按钮_P, command=元神升级, relief=FLAT, state=DISABLED)
        self.元神升级按钮.place(x=385, y=228)

        self.鉴赏功能 = Button(self.FM, image=self.鉴赏功能_P, command=鉴赏, relief=FLAT)
        self.鉴赏功能.place(x=386 + 150, y=228)

    def 刷新属性词条(self):
        '''通过set刷新属性词条'''
        self.S_LV.set('Lv: ' + str(self.G.Lv))
        self.S_伤害类型.set('伤害类型：' + self.G.伤害类型)
        self.S_HP.set('HP: ' + str(self.G.HP))
        self.S_力量.set('力量: ' + str(self.G.力量))
        self.S_智慧.set('智慧: ' + str(self.G.智慧))
        self.S_体力.set('体力: ' + str(self.G.体力))
        self.S_敏捷.set('敏捷: ' + str(self.G.敏捷))

        self.S_力量资质.set('力量资质: ' + str(self.G.力量资质))
        self.S_智慧资质.set('智慧资质: ' + str(self.G.智慧资质))
        self.S_体力资质.set('体力资质: ' + str(self.G.体力资质))
        self.S_敏捷资质.set('敏捷资质: ' + str(self.G.敏捷资质))
        # 后天属性
        self.S_后天属性.set('后天属性：' + self.G.后天属性)
        # 战斗属性
        self.S_物理攻击.set('物理攻击: ' + str(self.G.物理攻击))
        self.S_法术攻击.set('法术攻击: ' + str(self.G.法术攻击))
        self.S_命中.set('命中: ' + str(self.G.命中))
        self.S_闪避.set('闪避: ' + str(self.G.闪避))
        Overhead = {'B': 1000, 'A': 2000, 'S': 3000, 'S1': 5000, 'SS': 10000}
        self.升级经验L_S.set(f'升级所需经验：{int((1 + (1 + self.G.Lv * 1.130)) * Overhead.get(self.G.等级))}')

    def 创建属性词条(self):
        Overhead = {'B': 1000, 'A': 2000, 'S': 3000, 'S1': 5000, 'SS': 10000}
        self.升级经验L_S = StringVar()
        self.升级经验L_S.set(f'升级所需经验：{int((1 + (1 + self.G.Lv * 1.130)) * Overhead.get(self.G.等级))}')
        self.升级经验L = Label(self.FM, textvariable=self.升级经验L_S, bg='white')

        if self.G.Lv < 40:  # 判断升级所需经验是否需要显示
            self.升级经验L.place(x=5, y=310)

        self.属性词条 = []  # 该变量未使用
        x = 385
        self.昵称 = Label(self.FM, text=self.G.name, font=('Aridl', 13), bg='white').place(x=x, y=0)

        self.S_LV = StringVar()
        self.S_LV.set('Lv: ' + str(self.G.Lv))
        self.Lv = Label(self.FM, textvariable=self.S_LV, bg='white').place(x=x, y=25)

        self.S_伤害类型 = StringVar()
        try:
            self.S_伤害类型.set('伤害类型：' + self.G.伤害类型)
        except:
            self.S_伤害类型.set('无')
        self.伤害类型 = Label(self.FM, textvariable=self.S_伤害类型, bg='white').place(x=x + 100, y=25)

        self.S_HP = StringVar()
        self.S_HP.set('HP: ' + str(self.G.HP))
        self.HP = Label(self.FM, textvariable=self.S_HP, bg='white').place(x=x, y=45)
        # 基础属性
        self.S_力量 = StringVar()
        self.S_力量.set('力量: ' + str(self.G.力量) + '    ')
        self.力量 = Label(self.FM, textvariable=self.S_力量, bg='white').place(x=x, y=65)

        self.S_智慧 = StringVar()
        self.S_智慧.set('智慧: ' + str(self.G.智慧))
        self.智慧 = Label(self.FM, textvariable=self.S_智慧, bg='white').place(x=x + 100, y=65)

        self.S_体力 = StringVar()
        self.S_体力.set('体力: ' + str(self.G.体力))
        self.体力 = Label(self.FM, textvariable=self.S_体力, bg='white').place(x=x, y=85)

        self.S_敏捷 = StringVar()
        self.S_敏捷.set('敏捷: ' + str(self.G.敏捷))
        self.敏捷 = Label(self.FM, textvariable=self.S_敏捷, bg='white').place(x=x + 100, y=85)

        # 属性资质
        self.S_力量资质 = StringVar()
        self.S_力量资质.set('力量资质: ' + str(self.G.力量资质))
        self.力量资质 = Label(self.FM, textvariable=self.S_力量资质, bg='white').place(x=x, y=125)

        self.S_智慧资质 = StringVar()
        self.S_智慧资质.set('' + '智慧资质: ' + str(self.G.智慧资质))
        self.智慧资质 = Label(self.FM, textvariable=self.S_智慧资质, bg='white').place(x=x + 100, y=125)

        self.S_体力资质 = StringVar()
        self.S_体力资质.set('体力资质: ' + str(self.G.体力资质))
        self.体力资质 = Label(self.FM, textvariable=self.S_体力资质, bg='white').place(x=x, y=105)

        self.S_敏捷资质 = StringVar()
        self.S_敏捷资质.set('敏捷资质: ' + str(self.G.敏捷资质))
        self.敏捷资质 = Label(self.FM, textvariable=self.S_敏捷资质, bg='white').place(x=x + 100, y=105)

        # 后天属性
        self.S_后天属性 = StringVar()
        self.S_后天属性.set('后天属性：' + self.G.后天属性)
        self.后天属性 = Label(self.FM, textvariable=self.S_后天属性, bg='white').place(x=x, y=145)

        # 战斗属性
        self.S_物理攻击 = StringVar()
        self.S_物理攻击.set('物理攻击: ' + str(self.G.物理攻击))
        self.物理攻击 = Label(self.FM, textvariable=self.S_物理攻击, bg='white').place(x=x, y=165)

        self.S_法术攻击 = StringVar()
        self.S_法术攻击.set('法术攻击: ' + str(self.G.法术攻击))
        self.法术攻击 = Label(self.FM, textvariable=self.S_法术攻击, bg='white').place(x=x, y=185)

        self.S_命中 = StringVar()
        self.S_命中.set('命中: ' + str(self.G.命中))
        self.命中 = Label(self.FM, textvariable=self.S_命中, bg='white').place(x=x, y=205)

        self.S_闪避 = StringVar()
        self.S_闪避.set('闪避: ' + str(self.G.闪避))
        self.闪避 = Label(self.FM, textvariable=self.S_闪避, bg='white').place(x=x + 100, y=205)


class 元神操作视图_斗法():
    def __init__(self, G):
        self.G = G
        print(G.__dict__)
        self.FM = LabelFrame(DE.当前场景.frame, text=self.G.name + '  *  ' + self.G.ID + '*' + self.G.等级, height=380,
                             width=604, bg='white')
        # bg='white' 白色背景
        self.FM.place(x=383, y=232)
        self.LH_P = Open_Jpg(os.path.join('Resource', 'picture', 'Genshin', f'{self.G.Code}-x.jpg'))  # 元神小立绘
        self.LH = Label(self.FM, image=self.LH_P)
        self.LH.place(x=5, y=0)
        self.X_B = Button(self.FM, text='X', command=self.用于关闭)
        self.X_B.place(x=580, y=0)
        self.创建装备图标()
        self.创建属性词条()

    def 用于关闭(self):
        self.FM.destroy()
        try:
            self.显示装备列表面板.destroy()
        except:
            pass

    def 创建装备图标(self):  # 临时用，装备功能尚未实装
        if self.G.装备 == None:
            self.ZBLH_P = Open_Jpg(os.path.join('Resource', 'picture', 'Equipment', f'O.jpg'))
        else:
            self.ZBLH_P = Open_Jpg(os.path.join('Resource', 'picture', 'Equipment', f'{self.G.装备.Code}.jpg'))
            if self.G.装备.强化等级 != 0:
                self.ENAMEL = Label(self.FM, text='+' + str(self.G.装备.强化等级) + self.G.装备.name + '-' + self.G.装备.ID,
                                    bg='white', fg=DE.装备字体颜色.get(self.G.装备.品级)).place(x=220, y=185)
            else:
                self.ENAMEL = Label(self.FM, text=self.G.装备.name + '-' + self.G.装备.ID,
                                    bg='white', fg=DE.装备字体颜色.get(self.G.装备.品级)).place(x=220, y=185)
            self.ELL = Label(self.FM, text='力量+' + str(self.G.装备.力量), bg='white').place(x=220, y=205)
            self.EZH = Label(self.FM, text='智慧+' + str(self.G.装备.智慧), bg='white').place(x=310, y=205)
            self.ETL = Label(self.FM, text='体力+' + str(self.G.装备.体力), bg='white').place(x=220, y=225)
            self.EMJ = Label(self.FM, text='敏捷+' + str(self.G.装备.敏捷), bg='white').place(x=310, y=225)

            self.ELLZ = Label(self.FM, text='力量强化+' + str(self.G.装备.力量资质), bg='white').place(x=220, y=245)
            self.EZZH = Label(self.FM, text='智慧强化+' + str(self.G.装备.智慧资质), bg='white').place(x=220, y=265)
            self.ETLZ = Label(self.FM, text='体力强化+' + str(self.G.装备.体力资质), bg='white').place(x=220, y=285)
            self.ETLZ = Label(self.FM, text='敏捷强化+' + str(self.G.装备.敏捷资质), bg='white').place(x=220, y=305)
            self.ETLZ = Label(self.FM, text='成色；' + str(self.G.装备.完美程度), bg='white').place(x=310, y=305)
        self.ZBLH = Button(self.FM, image=self.ZBLH_P, relief=FLAT)
        self.ZBLH.place(x=215, y=3)

    # 其他窗口弹出方法封装

    def 创建操作按钮(self):
        # 操作面板内按钮方法函数封装
        def 删除元神(G):
            # 触发掉落()
            # self.创建提示弹窗(OK)

            def OK():  # 业务流封装到判断窗口的确认按钮上
                '''下面是根据元神品级分级判断获得资源'''
                if self.G.等级 == 'B':
                    list = {'Y': 0, 'G': 0, 'T': 0, 'Exp': (1000 + (self.G.Lv * 100))}
                    # self.删除后获得资源(list)
                elif self.G.等级 == 'A':
                    list = {'Y': 0, 'G': 0, 'T': 5000, 'Exp': (1000 + (self.G.Lv * 100))}
                    # self.删除后获得资源(list)
                    # text = f'   请确认是否要放逐{self.G.name},放逐后你将获得5000 铜币和{(1000 + (self.G.Lv * 100))} Exp。'

                elif self.G.等级 == 'S':
                    list = {'Y': 0, 'G': 100, 'T': 20000, 'Exp': (1000 + (self.G.Lv * 100))}
                    # self.删除后获得资源(list)
                    # text = f'   请确认是否要放逐{self.G.name},放逐后你将获得100 黄金、20000 铜币和{(1000 + (self.G.Lv * 100))} Exp。'
                elif self.G.等级 == 'S1':
                    list = {'Y': 10, 'G': 200, 'T': 50000, 'Exp': (1000 + (self.G.Lv * 100))}
                    # self.删除后获得资源(list)
                    # text = f'   请确认是否要放逐{self.G.name},放逐后你将获得10勾玉、200 黄金、50000 铜币和{(1000 + (self.G.Lv * 100))} Exp。'
                elif self.G.等级 == 'SS':
                    list = {'Y': 30, 'G': 600, 'T': 60000, 'Exp': (1000 + (self.G.Lv * 100))}
                    # self.删除后获得资源(list)
                    # text = f'   请确认是否要放逐{self.G.name},放逐后你将获得30勾玉、600 黄金、60000 铜币和{(1000 + (self.G.Lv * 100))} Exp。'
                # DE.Player_Mian.exp = DE.Player_Mian.exp + (1000 + (self.G.Lv*100)) #收回经验
                '''把当前元神从列表中删除，关闭元神操作面板，刷新元神视图'''
                if G.装备 != None:
                    DE.Player_Mian.装备组.append(G.装备)  # 回收装备
                DE.Player_Mian.元神组.remove(G)
                '''注意此处业务流程，先执行删除，然后关闭操作面板，刷新元神视图场景，弹出资源页面，在刷新资源UI'''
                '''若先弹出资源页面在刷新场景会出现资源页面消失'''
                '''先刷新UI资源显示在弹出资源页面会UI资源更新不及时'''
                self.FM.destroy()
                # 切换场景(Genshin_view)
                DE.当前场景.翻页(DE.当前场景.ABCD)
                self.删除后获得资源(list)
                DE.当前场景.刷新资源UI()

            if self.G.等级 == 'B':
                text = f'   请确认是否要放逐{self.G.name},放逐后你将获得{(1000 + (self.G.Lv * 100))} Exp。'
            elif self.G.等级 == 'A':
                text = f'   请确认是否要放逐{self.G.name},放逐后你将获得5000 铜币和{(1000 + (self.G.Lv * 100))} Exp。'

            elif self.G.等级 == 'S':
                text = f'   请确认是否要放逐{self.G.name},放逐后你将获得100 黄金、20000 铜币和{(1000 + (self.G.Lv * 100))} Exp。'
            elif self.G.等级 == 'S1':
                text = f'   请确认是否要放逐{self.G.name},放逐后你将获得10勾玉、200 黄金、50000 铜币和{(1000 + (self.G.Lv * 100))} Exp。'
            elif self.G.等级 == 'SS':
                text = f'   请确认是否要放逐{self.G.name},放逐后你将获得30勾玉、600 黄金、60000 铜币和{(1000 + (self.G.Lv * 100))} Exp。'

            self.创建判断弹窗(OK, text)

        def 转换伤害类型():
            '''调用对象方法重新设置属性，然后刷新词条'''

            # 升级开销
            Overhead = {'B': 300, 'A': 800, 'S': 1200, 'S1': 1800, 'SS': 3000}

            if DE.Player_Mian.金 >= Overhead.get(self.G.等级):  # 判断金是否够使用
                DE.Player_Mian.金 = DE.Player_Mian.金 - Overhead.get(self.G.等级)  # 向Overhead获取各品级所需开销
                self.G.转换伤害类型()  # 执行元神类方法
                self.刷新属性词条()  # 执行元神操作面板词条属性刷新
                DE.当前场景.刷新资源UI()  # 执行UI资源显示刷新
            else:  # 开销不足时弹窗提示
                self.创建提示弹窗(f'资源不足，{self.G.等级}级元神转换伤害类型需要{Overhead.get(self.G.等级)}黄金。')

        def 元神升级():
            '''等级加一，初始化后天属性，刷新词条'''
            Overhead = {'B': 1000, 'A': 2000, 'S': 3000, 'S1': 5000, 'SS': 10000}
            '''扣除经验，已实装'''
            DE.Player_Mian.exp = DE.Player_Mian.exp - int((1 + (1 + self.G.Lv * 1.130)) * Overhead.get(self.G.等级))
            '''执行升级'''
            self.G.Lv = self.G.Lv + 1
            self.G.初始化基础属性()
            self.G.初始化战斗属性()
            self.刷新属性词条()
            '''判断按钮是否需要关闭'''
            if self.G.Lv >= 40:  # 40级后关闭升级按钮
                self.元神升级按钮.config(state=DISABLED)
            if DE.Player_Mian.exp < int((1 + (1 + self.G.Lv * 1.130)) * Overhead.get(self.G.等级)):  # 所需经验不足关闭升级按钮
                self.元神升级按钮.config(state=DISABLED)

            DE.当前场景.刷新资源UI()  # 刷新UI资源显示

        def 鉴赏():
            self.GB_P = Open_Jpg(os.path.join('Resource', 'picture', 'Genshin', f'{self.G.Code}-d.jpg'))
            大图宽 = self.GB_P.width()
            if 大图宽 < 1366:
                放置位置 = (1366 - 大图宽) / 2
            else:
                放置位置 = 0
            self.GB = Label(DE.当前场景.frame, image=self.GB_P)
            self.GB.place(x=放置位置, y=0)
            # self.GB_C = Button(self.GB_FM, text='查看')

            颜色 = {'B': 'chartreuse', 'A': 'cyan', 'S': '', 'S1': '', 'SS': ''}

            def off():
                self.GB.destroy()
                self.GLFM.destroy()

            self.GLFM = Frame(DE.当前场景.frame)
            self.GLFM.place(x=1230, y=660)
            self.GL_name = Label(self.GLFM, text=self.G.name, font=('Aridl', 13))
            self.GL_name.pack()
            # self.GL_等级 = Label(self.GLFM, text=self.G.等级, font=('Aridl', 13))
            # self.GL_等级.pack()
            self.GBB = Button(self.GLFM, text='关闭', command=off)
            self.GBB.pack()

        # 创建操作按钮
        # self.操作按钮区域 = Frame(self.FM,height=60, width=200).place(x=385,y=245)
        self.转换伤害类型_P = Open_Jpg(os.path.join('Resource', 'picture', 'ui', f'G_CZ_ZH.jpg'))
        self.元神升级按钮_P = Open_Jpg(os.path.join('Resource', 'picture', 'ui', f'G_CZ_UP.jpg'))
        self.删除元神按钮_P = Open_Jpg(os.path.join('Resource', 'picture', 'ui', f'G_CZ_FZ.jpg'))
        self.鉴赏功能_P = Open_Jpg(os.path.join('Resource', 'picture', 'ui', f'G_CZ_JS.jpg'))

        self.转换伤害类型 = Button(self.FM, image=self.转换伤害类型_P, command=转换伤害类型, relief=FLAT)
        self.转换伤害类型.place(x=385 + 50, y=228)

        self.删除元神按钮 = Button(self.FM, image=self.删除元神按钮_P, command=lambda: 删除元神(self.G), relief=FLAT)
        self.删除元神按钮.place(x=385 + 100, y=228)
        Overhead = {'B': 1000, 'A': 2000, 'S': 3000, 'S1': 5000, 'SS': 10000}
        '''判断是否激活升级按钮，所需经验不足时将停用升级按钮'''
        '''等级超过40级时也将停用升级按钮'''
        if self.G.Lv < 40 and DE.Player_Mian.exp >= int(int((1 + (1 + self.G.Lv * 1.130)) * Overhead.get(self.G.等级))):
            self.元神升级按钮 = Button(self.FM, image=self.元神升级按钮_P, command=元神升级, relief=FLAT)
        else:
            self.元神升级按钮 = Button(self.FM, image=self.元神升级按钮_P, command=元神升级, relief=FLAT, state=DISABLED)
        self.元神升级按钮.place(x=385, y=228)

        self.鉴赏功能 = Button(self.FM, image=self.鉴赏功能_P, command=鉴赏, relief=FLAT)
        self.鉴赏功能.place(x=386 + 150, y=228)

    def 刷新属性词条(self):
        '''通过set刷新属性词条'''
        self.S_LV.set('Lv: ' + str(self.G.Lv))
        self.S_伤害类型.set('伤害类型：' + self.G.伤害类型)
        self.S_HP.set('HP: ' + str(self.G.HP))
        self.S_力量.set('力量: ' + str(self.G.力量))
        self.S_智慧.set('智慧: ' + str(self.G.智慧))
        self.S_体力.set('体力: ' + str(self.G.体力))
        self.S_敏捷.set('敏捷: ' + str(self.G.敏捷))

        self.S_力量资质.set('力量资质: ' + str(self.G.力量资质))
        self.S_智慧资质.set('智慧资质: ' + str(self.G.智慧资质))
        self.S_体力资质.set('体力资质: ' + str(self.G.体力资质))
        self.S_敏捷资质.set('敏捷资质: ' + str(self.G.敏捷资质))
        # 后天属性
        self.S_后天属性.set('后天属性：' + self.G.后天属性)
        # 战斗属性
        self.S_物理攻击.set('物理攻击: ' + str(self.G.物理攻击))
        self.S_法术攻击.set('法术攻击: ' + str(self.G.法术攻击))
        self.S_命中.set('命中: ' + str(self.G.命中))
        self.S_闪避.set('闪避: ' + str(self.G.闪避))
        Overhead = {'B': 1000, 'A': 2000, 'S': 3000, 'S1': 5000, 'SS': 10000}
        self.升级经验L_S.set(f'升级所需经验：{int((1 + (1 + self.G.Lv * 1.130)) * Overhead.get(self.G.等级))}')

    def 创建属性词条(self):
        Overhead = {'B': 1000, 'A': 2000, 'S': 3000, 'S1': 5000, 'SS': 10000}
        self.升级经验L_S = StringVar()
        self.升级经验L_S.set(f'升级所需经验：{int((1 + (1 + self.G.Lv * 1.130)) * Overhead.get(self.G.等级))}')
        self.升级经验L = Label(self.FM, textvariable=self.升级经验L_S, bg='white')

        if self.G.Lv < 40:  # 判断升级所需经验是否需要显示
            self.升级经验L.place(x=5, y=310)

        self.属性词条 = []  # 该变量未使用
        x = 385
        self.昵称 = Label(self.FM, text=self.G.name, font=('Aridl', 13), bg='white').place(x=x, y=0)

        self.S_LV = StringVar()
        self.S_LV.set('Lv: ' + str(self.G.Lv))
        self.Lv = Label(self.FM, textvariable=self.S_LV, bg='white').place(x=x, y=25)

        self.S_伤害类型 = StringVar()
        try:
            self.S_伤害类型.set('伤害类型：' + self.G.伤害类型)
        except:
            self.S_伤害类型.set('无')
        self.伤害类型 = Label(self.FM, textvariable=self.S_伤害类型, bg='white').place(x=x + 100, y=25)

        self.S_HP = StringVar()
        self.S_HP.set('HP: ' + str(self.G.HP))
        self.HP = Label(self.FM, textvariable=self.S_HP, bg='white').place(x=x, y=45)
        # 基础属性
        self.S_力量 = StringVar()
        self.S_力量.set('力量: ' + str(self.G.力量) + '    ')
        self.力量 = Label(self.FM, textvariable=self.S_力量, bg='white').place(x=x, y=65)

        self.S_智慧 = StringVar()
        self.S_智慧.set('智慧: ' + str(self.G.智慧))
        self.智慧 = Label(self.FM, textvariable=self.S_智慧, bg='white').place(x=x + 100, y=65)

        self.S_体力 = StringVar()
        self.S_体力.set('体力: ' + str(self.G.体力))
        self.体力 = Label(self.FM, textvariable=self.S_体力, bg='white').place(x=x, y=85)

        self.S_敏捷 = StringVar()
        self.S_敏捷.set('敏捷: ' + str(self.G.敏捷))
        self.敏捷 = Label(self.FM, textvariable=self.S_敏捷, bg='white').place(x=x + 100, y=85)

        # 属性资质
        self.S_力量资质 = StringVar()
        self.S_力量资质.set('力量资质: ' + str(self.G.力量资质))
        self.力量资质 = Label(self.FM, textvariable=self.S_力量资质, bg='white').place(x=x, y=125)

        self.S_智慧资质 = StringVar()
        self.S_智慧资质.set('' + '智慧资质: ' + str(self.G.智慧资质))
        self.智慧资质 = Label(self.FM, textvariable=self.S_智慧资质, bg='white').place(x=x + 100, y=125)

        self.S_体力资质 = StringVar()
        self.S_体力资质.set('体力资质: ' + str(self.G.体力资质))
        self.体力资质 = Label(self.FM, textvariable=self.S_体力资质, bg='white').place(x=x, y=105)

        self.S_敏捷资质 = StringVar()
        self.S_敏捷资质.set('敏捷资质: ' + str(self.G.敏捷资质))
        self.敏捷资质 = Label(self.FM, textvariable=self.S_敏捷资质, bg='white').place(x=x + 100, y=105)

        # 后天属性
        self.S_后天属性 = StringVar()
        self.S_后天属性.set('后天属性：' + self.G.后天属性)
        self.后天属性 = Label(self.FM, textvariable=self.S_后天属性, bg='white').place(x=x, y=145)

        # 战斗属性
        self.S_物理攻击 = StringVar()
        self.S_物理攻击.set('物理攻击: ' + str(self.G.物理攻击))
        self.物理攻击 = Label(self.FM, textvariable=self.S_物理攻击, bg='white').place(x=x, y=165)

        self.S_法术攻击 = StringVar()
        self.S_法术攻击.set('法术攻击: ' + str(self.G.法术攻击))
        self.法术攻击 = Label(self.FM, textvariable=self.S_法术攻击, bg='white').place(x=x, y=185)

        self.S_命中 = StringVar()
        self.S_命中.set('命中: ' + str(self.G.命中))
        self.命中 = Label(self.FM, textvariable=self.S_命中, bg='white').place(x=x, y=205)

        self.S_闪避 = StringVar()
        self.S_闪避.set('闪避: ' + str(self.G.闪避))
        self.闪避 = Label(self.FM, textvariable=self.S_闪避, bg='white').place(x=x + 100, y=205)


# 用于装备视图小窗口呼出，装备强化和分解
class 装备操作视图():
    def __init__(self, E):
        self.E = E
        self.装备显示容器 = LabelFrame(DE.当前场景.frame, text=E.name + ' ' + E.ID, height=260, width=300, bg='white')
        self.抽装备关闭按钮 = Button(self.装备显示容器, text='X', command=self.装备显示容器.destroy, relief=FLAT, bg='white')
        self.抽装备关闭按钮.place(x=275, y=0)
        self.装备图标_P = Open_Jpg(os.path.join('Resource', 'picture', 'Equipment', f'{E.Code}.jpg'))
        self.装备图标 = Label(self.装备显示容器, image=self.装备图标_P)
        self.装备图标.place(x=0, y=0)
        self.装备属性文本 = StringVar()
        self.装备属性文本.set(E.获得装备属性())
        self.装备名称文本 = StringVar()
        try:
            if self.E.强化等级 == 0:
                self.装备名称文本.set(self.E.name)

            else:
                self.装备名称文本.set('+' + str(self.E.强化等级) + self.E.name)
        except:
            self.E.强化等级 = 0
            self.装备名称文本.set(self.E.name)

        self.装备名称 = Label(self.装备显示容器, textvariable=self.装备名称文本, font=('Aridl', 11), bg='white',
                          fg=DE.装备字体颜色.get(self.E.品级)).place(x=160, y=0)
        # self.装备品级 = Label(self.装备显示容器, text=E.品级, bg='white').place(x=240, y=0)
        self.装备属性 = Label(self.装备显示容器, textvariable=self.装备属性文本, justify=LEFT, bg='white').place(x=160, y=20)

        self.装备显示容器.place(x=533, y=180)

        self.创建按钮()

    def 创建按钮(self):
        self.分解按钮 = Button(self.装备显示容器, text='分解', relief=FLAT, bg='white', command=self.分解装备)
        self.分解按钮.place(x=10, y=200)
        self.强化消费 = StringVar()
        self.强化消费.set(f'强化 -{((self.E.强化等级 + 1) * 500 + 1000) * DE.强化装备花费倍数.get(self.E.品级)}铜币')
        self.强化钮 = Button(self.装备显示容器, textvariable=self.强化消费, relief=FLAT, bg='white', command=self.强化装备)
        self.强化钮.place(x=107, y=200)

    def 分解装备(self):

        def OK():  # 业务流封装到判断窗口的确认按钮上
            print('开始装备分解')
            '''下面是根据装备品级分级判断获得资源'''
            # 传承-史诗-神器-稀有
            if self.E.品级 == '稀有':
                list = {'Y': 0, 'G': 0, 'T': 5000, 'Exp': 0}
                # self.删除后获得资源(list)
            elif self.E.品级 == '神器':
                list = {'Y': 0, 'G': 30, 'T': 10000, 'Exp': 0}
                # self.删除后获得资源(list)
                # text = f'   请确认是否要放逐{self.G.name},放逐后你将获得5000 铜币和{(1000 + (self.G.Lv * 100))} Exp。'
            elif self.E.品级 == '史诗':
                list = {'Y': 3, 'G': 100, 'T': 50000, 'Exp': 10000}
                # self.删除后获得资源(list)
                # text = f'   请确认是否要放逐{self.G.name},放逐后你将获得100 黄金、20000 铜币和{(1000 + (self.G.Lv * 100))} Exp。'
            elif self.E.品级 == '传承':
                list = {'Y': 10, 'G': 500, 'T': 50000, 'Exp': 60000}
                # self.删除后获得资源(list)
                # text = f'   请确认是否要放逐{self.G.name},放逐后你将获得10勾玉、200 黄金、50000 铜币和{(1000 + (self.G.Lv * 100))} Exp。'

            DE.Player_Mian.装备组.remove(self.E)
            页码 = DE.当前场景.当前页码
            self.装备显示容器.destroy()
            切换场景(Equipment_view)
            # DE.当前场景.显示所有(页码=DE.当前场景.当前页码)
            DE.当前场景.翻页(页码)
            self.删除后获得资源(list)
            DE.当前场景.刷新资源UI()
            print('分解完成！')

        if self.E.品级 == '稀有':
            # list = {'Y': 0, 'G': 0, 'T': 5000, 'Exp': 0}
            # self.删除后获得资源(list)
            text = f'   请确认是否要分解{self.E.name},分解后你将获得5000 铜币。'
        elif self.E.品级 == '神器':
            # list = {'Y': 0, 'G': 30, 'T': 10000, 'Exp': 0}
            # self.删除后获得资源(list)
            text = f'   请确认是否要分解{self.E.name},分解后你将获得30 黄金和10000 铜币。'

        elif self.E.品级 == '史诗':
            # list = {'Y': 3, 'G': 100, 'T': 50000, 'Exp': 10000}
            # self.删除后获得资源(list)
            text = f'   请确认是否要分解{self.E.name},分解后你将获得3 勾玉、100 黄金、50000 铜币和10000 Exp。'
        elif self.E.品级 == '传承':
            # list = {'Y': 10, 'G': 500, 'T': 50000, 'Exp': 60000}
            # self.删除后获得资源(list)
            text = f'   请确认是否要分解{self.E.name},分解后你将获得10 勾玉、500 黄金、50000 铜币和60000 Exp。'

        self.创建判断弹窗(OK, text)
        # DE.当前场景.刷新资源UI()

    def 强化装备(self):
        # if hasattr(self, '强化等级') == False:#判断对象该属性是否存在。
        # self.E.强化等级=0
        # 判断对象该属性是否存在
        目标等级 = self.E.强化等级 + 1
        强化花费 = 目标等级 * 500 + 1000
        if DE.Player_Mian.铜 >= 强化花费 * DE.强化装备花费倍数.get(self.E.品级) and self.E.强化等级 < 20:
            print(f'消耗{强化花费 * DE.强化装备花费倍数.get(self.E.品级)}强化{self.E.name},目标等级{目标等级}')
            DE.Player_Mian.铜 -= 强化花费 * DE.强化装备花费倍数.get(self.E.品级)
            v = random.randint(0, 100)  # 抽取概率
            C = 100 - (目标等级 * 4.8)  # 成功概率
            if v < C:
                print(True)
                self.E.强化等级 = 目标等级
                self.E.装备强化()
                self.装备属性文本.set(self.E.获得装备属性())
                self.装备名称文本.set('+' + str(self.E.强化等级) + self.E.name)
                self.强化消费.set(f'强化 -{((self.E.强化等级 + 1) * 500 + 1000) * DE.强化装备花费倍数.get(self.E.品级)}铜币')
                DE.当前场景.刷新资源UI()
            else:
                print(False)
                DE.当前场景.刷新资源UI()

    def 创建判断弹窗(self, OK, text):
        # 将业务流封装绑定给判断窗口，判断窗口确认后才会继续执行
        self.判断弹窗 = 判断弹窗(OK, text=text)

    def 创建提示弹窗(self, text):
        '''将弹出提示窗口封装成类方法，而不是在按钮触发函数内创建提示窗口对象'''
        self.提示弹窗 = T提示弹窗(text)

    def 删除后获得资源(self, list):
        '''将元神放逐后获得资源的过程封装成类方法'''
        '''用掉落数据创建掉落窗口'''
        self.LL掉落弹窗 = 掉落弹窗(list)


# 未使用
class 抽出按钮():  # 用于显示抽出的元神，临时用
    def __init__(self, root, Code):
        self.GB_P = Open_Jpg(os.path.join('Resource', 'picture', 'Genshin', f'{Code}-x.jpg'))
        self.GB = Button(root, image=self.GB_P)
        self.GB.place(x=0, y=0)


# 未使用
class UI():  # 未使用的界面UI类
    def __init__(self):
        self.root = Tk()
        self.root.geometry('1366x768')
        self.Game_UI = Frame(self.root)
        self.Game_UI.pack()
        # 菜单条
        self.menubar = Menu(self.Game_UI)
        self.menu = Menu(self.menubar, tearoff=False)
        self.menu.add_command(label='退出', command=self.root.quit)
        self.menubar.add_cascade(label="菜单", menu=self.menu)
        self.Game_UI.bind("<Button-3>", self.showMenu)

    def run(self):
        self.root.mainloop()


# 阵容选择视图
class Lineup():

    def __init__(self):
        self.G_list = []
        self.阵容列表 = []
        self.GFM = LabelFrame(DE.当前场景.frame, text='神社', height=750, width=740, bg='white')
        self.GFM.place(y=5, x=620)

        self.当前阵容标签文本 = StringVar()
        self.当前阵容标签文本.set('当前阵容积分:')
        self.LFM = LabelFrame(DE.当前场景.frame, text='当前阵容', height=170, width=600, bg='white')
        self.LFM.place(x=5, y=550)
        self.显示所有()
        self.显示阵容()

        self.出征_l_m = Open_Jpg(os.path.join('Resource', 'picture', 'ui', 'go.jpg'))

        self.出征 = Button(self.LFM, image=self.出征_l_m, relief=FLAT, command=出征, bg='white').place(x=510, y=112)
        # self.挑战按钮 = Button(self.LFM, image=self.出征_l_m, relief=FLAT, bg='white', fg='red').place(x=400,y=110)

        self.当前阵容标签 = Label(self.LFM, textvariable=self.当前阵容标签文本).place(x=0, y=120)
        DE.当前场景.刷新阵容 = self.显示阵容

        DE.刷新阵容 = self.显示阵容

    def 显示阵容(self):
        for i in self.阵容列表:
            try:
                i.ICO.destroy()
            except:
                pass

        # self.LFM.place_forget()
        self.LFM.place(x=5, y=550)
        x = 5
        y = 5
        for i in DE.阵容:
            self.Car = 阵容按钮(i, self.LFM, x, y)
            self.阵容列表.append(self.Car)
            x += 110

        DE.阵容积分 = DE.Battlefield_service.计算阵容积分()
        阵容增益 = DE.Battlefield_service.计算阵容增益()
        print(str(阵容增益))
        DE.收益修正 = 阵容增益[0]
        DE.战斗HP恢复率 = 阵容增益[1]
        self.当前阵容标签文本.set(f'当前阵容积分:{DE.阵容积分} 收益率:{DE.收益修正} HP恢复率:{DE.战斗HP恢复率}')

    def 显示所有(self, 页码=1):
        for i in self.G_list:
            try:
                i.destroy()
            except:
                pass

        self.G_list = []

        self.ABC = 页码
        x = 40
        y = 5
        for i in DE.Player_Mian.元神组[页码 * 36 - 36:页码 * 36]:
            # self.i = i
            # self.G_ICO_P = Open_Jpg(os.path.join('Resource','picture','Genshin',f'{i.Code}-c.jpg'))
            # self.G_ICO = Button(self.GFM, image=self.G_ICO_P,command=lambda :元神信息卡片(i,self.GFM))
            # self.G_list.append(self.i)
            # self.G_ICO.place(x=x, y=y)
            self.But = 元神信息卡片(i, self.GFM, x, y)
            self.G_list.append(self.But)
            x += 110
            if x > 600:
                y += 110
                x = 40

        if len(DE.Player_Mian.元神组) > self.ABC * 36:
            self.下一页 = Button(self.GFM, text='下一页', bg='white', command=lambda: self.显示所有(页码=self.ABC + 1))
        else:
            self.下一页 = Button(self.GFM, text='下一页', bg='white')
        if self.ABC > 1:
            self.上一页 = Button(self.GFM, text='上一页', bg='white', command=lambda: self.显示所有(页码=self.ABC - 1))
        else:
            self.上一页 = Button(self.GFM, text='上一页', bg='white')

        self.上一页.place(x=5, y=670)
        self.下一页.place(x=5, y=700)

        按钮间隙 = 90

        self.排序_HP = Button(self.GFM, text='HP', width=7, command=self.G_LIST_HP).place(x=66, y=670)
        self.排序_WL = Button(self.GFM, text='物攻攻击', width=6, command=self.G_LIST_WL).place(x=66 + 按钮间隙 * 1, y=670)
        self.排序_MF = Button(self.GFM, text='法术攻击', width=6, command=self.G_LIST_MF).place(x=66 + 按钮间隙 * 2, y=670)
        self.排序_MZ = Button(self.GFM, text='命中', width=6, command=self.G_LIST_MZ).place(x=66 + 按钮间隙 * 3, y=670)
        self.排序_SB = Button(self.GFM, text='闪避', width=6, command=self.G_LIST_SB).place(x=66 + 按钮间隙 * 4, y=670)

    def 元神信息卡片(self, G):
        G = G
        self.元神_FM = LabelFrame(self.GFM, text=G.name + '  *  ' + G.ID + '*' + G.等级, height=370,
                                width=604, bg='white', )
        # bg='white' 白色背景
        self.元神_FM.place(x=0, y=70)
        # self.宿敌_FM.config(bg='red')
        # 立绘
        self.LH_P = Open_Jpg(os.path.join('Resource', 'picture', 'Genshin', f'{G.Code}-x.jpg'))  # 元神小立绘
        self.LH = Label(self.元神_FM, image=self.LH_P)
        self.LH.place(x=5, y=0)
        # 装备图标
        if G.装备 == None:
            self.ZBLH_P = Open_Jpg(os.path.join('Resource', 'picture', 'Equipment', f'O.jpg'))
        else:
            self.ZBLH_P = Open_Jpg(os.path.join('Resource', 'picture', 'Equipment', f'{G.装备.Code}.jpg'))
            if G.装备.强化等级 != 0:
                self.ENAMEL = Label(self.元神_FM, text='+' + str(G.装备.强化等级) + G.装备.name + '-' + G.装备.ID,
                                    bg='white', fg=DE.装备字体颜色.get(G.装备.品级)).place(x=220, y=185)
            else:
                self.ENAMEL = Label(self.元神_FM, text=G.装备.name + '-' + G.装备.ID,
                                    bg='white', fg=DE.装备字体颜色.get(G.装备.品级)).place(x=220, y=185)
            self.ELL = Label(self.元神_FM, text='力量+' + str(G.装备.力量), bg='white').place(x=220, y=205)
            self.EZH = Label(self.元神_FM, text='智慧+' + str(G.装备.智慧), bg='white').place(x=310, y=205)
            self.ETL = Label(self.元神_FM, text='体力+' + str(G.装备.体力), bg='white').place(x=220, y=225)
            self.EMJ = Label(self.元神_FM, text='敏捷+' + str(G.装备.敏捷), bg='white').place(x=310, y=225)

            self.ELLZ = Label(self.元神_FM, text='力量强化+' + str(G.装备.力量资质), bg='white').place(x=220, y=245)
            self.EZZH = Label(self.元神_FM, text='智慧强化+' + str(G.装备.智慧资质), bg='white').place(x=220, y=265)
            self.ETLZ = Label(self.元神_FM, text='体力强化+' + str(G.装备.体力资质), bg='white').place(x=220, y=285)
            self.ETLZ = Label(self.元神_FM, text='敏捷强化+' + str(G.装备.敏捷资质), bg='white').place(x=220, y=305)
            self.ETLZ = Label(self.元神_FM, text='成色；' + str(G.装备.完美程度), bg='white').place(x=310, y=305)
        self.ZBLH = Label(self.元神_FM, image=self.ZBLH_P, relief=FLAT)
        self.ZBLH.place(x=215, y=3)
        # 属性
        self.属性词条 = []  # 该变量未使用
        x = 385
        self.昵称 = Label(self.元神_FM, text=G.name, font=('Aridl', 13), bg='white').place(x=x, y=0)

        self.S_LV = StringVar()
        self.S_LV.set('Lv: ' + str(G.Lv))
        self.Lv = Label(self.元神_FM, textvariable=self.S_LV, bg='white').place(x=x, y=25)

        self.S_伤害类型 = StringVar()
        try:
            self.S_伤害类型.set('伤害类型：' + G.伤害类型)
        except:
            self.S_伤害类型.set('无')
        self.伤害类型 = Label(self.元神_FM, textvariable=self.S_伤害类型, bg='white').place(x=x + 100, y=25)

        self.S_HP = StringVar()
        self.S_HP.set('HP: ' + str(G.HP))
        self.HP = Label(self.元神_FM, textvariable=self.S_HP, bg='white').place(x=x, y=45)
        # 基础属性
        self.S_力量 = StringVar()
        self.S_力量.set('力量: ' + str(G.力量) + '    ')
        self.力量 = Label(self.元神_FM, textvariable=self.S_力量, bg='white').place(x=x, y=65)

        self.S_智慧 = StringVar()
        self.S_智慧.set('智慧: ' + str(G.智慧))
        self.智慧 = Label(self.元神_FM, textvariable=self.S_智慧, bg='white').place(x=x + 100, y=65)

        self.S_体力 = StringVar()
        self.S_体力.set('体力: ' + str(G.体力))
        self.体力 = Label(self.元神_FM, textvariable=self.S_体力, bg='white').place(x=x, y=85)

        self.S_敏捷 = StringVar()
        self.S_敏捷.set('敏捷: ' + str(G.敏捷))
        self.敏捷 = Label(self.元神_FM, textvariable=self.S_敏捷, bg='white').place(x=x + 100, y=85)

        # 属性资质
        self.S_力量资质 = StringVar()
        self.S_力量资质.set('力量资质: ' + str(G.力量资质))
        self.力量资质 = Label(self.元神_FM, textvariable=self.S_力量资质, bg='white').place(x=x, y=125)

        self.S_智慧资质 = StringVar()
        self.S_智慧资质.set('' + '智慧资质: ' + str(G.智慧资质))
        self.智慧资质 = Label(self.元神_FM, textvariable=self.S_智慧资质, bg='white').place(x=x + 100, y=125)

        self.S_体力资质 = StringVar()
        self.S_体力资质.set('体力资质: ' + str(G.体力资质))
        self.体力资质 = Label(self.元神_FM, textvariable=self.S_体力资质, bg='white').place(x=x, y=105)

        self.S_敏捷资质 = StringVar()
        self.S_敏捷资质.set('敏捷资质: ' + str(G.敏捷资质))
        self.敏捷资质 = Label(self.元神_FM, textvariable=self.S_敏捷资质, bg='white').place(x=x + 100, y=105)

        # 后天属性
        self.S_后天属性 = StringVar()
        self.S_后天属性.set('后天属性：' + G.后天属性)
        self.后天属性 = Label(self.元神_FM, textvariable=self.S_后天属性, bg='white').place(x=x, y=145)

        # 战斗属性
        self.S_物理攻击 = StringVar()
        self.S_物理攻击.set('物理攻击: ' + str(G.物理攻击))
        self.物理攻击 = Label(self.元神_FM, textvariable=self.S_物理攻击, bg='white').place(x=x, y=165)

        self.S_法术攻击 = StringVar()
        self.S_法术攻击.set('法术攻击: ' + str(G.法术攻击))
        self.法术攻击 = Label(self.元神_FM, textvariable=self.S_法术攻击, bg='white').place(x=x, y=185)

        self.S_命中 = StringVar()
        self.S_命中.set('命中: ' + str(G.命中))
        self.命中 = Label(self.元神_FM, textvariable=self.S_命中, bg='white').place(x=x, y=205)

        self.S_闪避 = StringVar()
        self.S_闪避.set('闪避: ' + str(G.闪避))
        self.闪避 = Label(self.元神_FM, textvariable=self.S_闪避, bg='white').place(x=x + 100, y=205)

        self.挑战按钮 = Button(self.元神_FM, text='加入', bg='white', fg='red')
        self.挑战按钮.place(x=x, y=250)

        self.关闭按钮 = Button(self.元神_FM, text='关闭', bg='white', fg='red', command=self.元神_FM.destroy)
        self.关闭按钮.place(x=x + 100, y=250)

    def G_LIST_MZ(self):
        # 列表排序 #x 对象属性
        DE.Player_Mian.元神组 = sorted(DE.Player_Mian.元神组, key=lambda x: x.命中, reverse=True)
        # for i in list:
        # print(i.HP)
        self.显示所有(页码=self.ABC)

    def G_LIST_S(self):
        # 列表排序 #x 对象属性
        DE.Player_Mian.元神组 = sorted(DE.Player_Mian.元神组, key=lambda x: x.闪避, reverse=True)
        # for i in list:
        # print(i.HP)
        self.显示所有(页码=self.ABC)

    def G_LIST_MF(self):
        # 列表排序 #x 对象属性
        DE.Player_Mian.元神组 = sorted(DE.Player_Mian.元神组, key=lambda x: x.法术攻击, reverse=True)
        # for i in list:
        # print(i.HP)
        self.显示所有(页码=self.ABC)

    def G_LIST_HP(self):

        DE.Player_Mian.元神组 = sorted(DE.Player_Mian.元神组, key=lambda x: x.HP, reverse=True)
        # for i in list:
        # print(i.HP)
        self.显示所有(页码=self.ABC)

    def G_LIST_SB(self):

        DE.Player_Mian.元神组 = sorted(DE.Player_Mian.元神组, key=lambda x: x.闪避, reverse=True)
        # for i in list:
        # print(i.HP)
        self.显示所有(页码=self.ABC)

    def G_LIST_WL(self):
        DE.Player_Mian.元神组 = sorted(DE.Player_Mian.元神组, key=lambda x: x.物理攻击, reverse=True)
        # for i in list:
        # print(i.HP)
        self.显示所有(页码=self.ABC)

        #


# 元神视图内每个元神的按钮
class Genshin_But():
    '''神社内展示每个元神头像的按钮封装'''

    def __init__(self, root, i, x, y):  # 创建时将提供放置坐标
        self.G = i
        self.G.初始化战斗属性()
        # Resource\picture\Genshin\VUGXQ-x.jpg
        self.BUT_P = Open_Jpg(os.path.join('Resource', 'picture', 'Genshin', f'{self.G.Code}-c.jpg'))
        self.BUT = Button(root, image=self.BUT_P, command=self.创建元神信息面板, relief=FLAT)
        self.BUT.place(x=x, y=y)

    def 创建元神信息面板(self):
        '''创建元神操作面板'''
        self.原画 = 元神操作视图(self.G)

    def destroy(self):
        # 未使用的函数
        self.BUT.destroy()


class Genshin_But_斗法():
    '''神社内展示每个元神头像的按钮封装'''

    def __init__(self, root, i, x, y):  # 创建时将提供放置坐标
        self.G = i
        self.G.初始化战斗属性()
        # Resource\picture\Genshin\VUGXQ-x.jpg
        self.BUT_P = Open_Jpg(os.path.join('Resource', 'picture', 'Genshin', f'{self.G.Code}-c.jpg'))
        self.BUT = Button(root, image=self.BUT_P, command=self.创建元神信息面板, relief=FLAT)
        self.BUT.place(x=x, y=y)

    def 创建元神信息面板(self):
        '''创建元神操作面板'''
        self.原画 = 元神操作视图_斗法(self.G)

    def destroy(self):
        # 未使用的函数
        self.BUT.destroy()


class Genshin_But_莉莉崽():
    '''神社内展示每个元神头像的按钮封装'''

    def __init__(self, root, i, x, y):  # 创建时将提供放置坐标
        self.G = i
        # self.G.初始化战斗属性()
        # Resource\picture\Genshin\VUGXQ-x.jpg
        self.BUT_P = Open_Jpg(os.path.join('Resource', 'picture', 'Genshin', f'{self.G.Code}-c.jpg'))
        self.BUT = Button(root, image=self.BUT_P, command=self.创建元神信息面板, relief=FLAT)
        self.BUT.place(x=x, y=y)

    def 创建元神信息面板(self):
        '''创建元神操作面板'''
        self.原画 = 元神操作视图_莉莉崽(self.G)

    def destroy(self):
        # 未使用的函数
        self.BUT.destroy()


class 元神操作视图_莉莉崽():
    def __init__(self, G):
        self.G = G
        print(G.__dict__)
        self.FM = LabelFrame(DE.当前场景.frame, text=self.G.name + '  *  ' + self.G.ID + '*' + self.G.等级, height=360,
                             width=604, bg='white')
        # bg='white' 白色背景
        self.FM.place(x=383, y=232)
        self.LH_P = Open_Jpg(os.path.join('Resource', 'picture', 'Genshin', f'{self.G.Code}-x.jpg'))  # 元神小立绘
        self.LH = Label(self.FM, image=self.LH_P)
        self.LH.place(x=5, y=0)
        self.X_B = Button(self.FM, text='X', command=self.用于关闭)
        self.X_B.place(x=580, y=0)
        self.创建装备图标()
        self.创建属性词条()

    def 用于关闭(self):
        self.FM.destroy()
        try:
            self.显示装备列表面板.destroy()
        except:
            pass

    def 创建装备图标(self):  # 临时用，装备功能尚未实装
        if self.G.装备 == None:
            self.ZBLH_P = Open_Jpg(os.path.join('Resource', 'picture', 'Equipment', f'O.jpg'))
        else:
            self.ZBLH_P = Open_Jpg(os.path.join('Resource', 'picture', 'Equipment', f'{self.G.装备.Code}.jpg'))
            if self.G.装备.强化等级 != 0:
                self.ENAMEL = Label(self.FM, text='+' + str(self.G.装备.强化等级) + self.G.装备.name + '-' + self.G.装备.ID,
                                    bg='white', fg=DE.装备字体颜色.get(self.G.装备.品级)).place(x=220, y=185)
            else:
                self.ENAMEL = Label(self.FM, text=self.G.装备.name + '-' + self.G.装备.ID,
                                    bg='white', fg=DE.装备字体颜色.get(self.G.装备.品级)).place(x=220, y=185)
            self.ELL = Label(self.FM, text='力量+' + str(self.G.装备.力量), bg='white').place(x=220, y=205)
            self.EZH = Label(self.FM, text='智慧+' + str(self.G.装备.智慧), bg='white').place(x=310, y=205)
            self.ETL = Label(self.FM, text='体力+' + str(self.G.装备.体力), bg='white').place(x=220, y=225)
            self.EMJ = Label(self.FM, text='敏捷+' + str(self.G.装备.敏捷), bg='white').place(x=310, y=225)

            self.ELLZ = Label(self.FM, text='力量强化+' + str(self.G.装备.力量资质), bg='white').place(x=220, y=245)
            self.EZZH = Label(self.FM, text='智慧强化+' + str(self.G.装备.智慧资质), bg='white').place(x=220, y=265)
            self.ETLZ = Label(self.FM, text='体力强化+' + str(self.G.装备.体力资质), bg='white').place(x=220, y=285)
            self.ETLZ = Label(self.FM, text='敏捷强化+' + str(self.G.装备.敏捷资质), bg='white').place(x=220, y=305)
            self.ETLZ = Label(self.FM, text='成色；' + str(self.G.装备.完美程度), bg='white').place(x=310, y=305)
        self.ZBLH = Button(self.FM, image=self.ZBLH_P, relief=FLAT)
        self.ZBLH.place(x=215, y=3)

    # 其他窗口弹出方法封装

    def 创建操作按钮(self):
        # 操作面板内按钮方法函数封装
        def 删除元神(G):
            # 触发掉落()
            # self.创建提示弹窗(OK)

            def OK():  # 业务流封装到判断窗口的确认按钮上
                '''下面是根据元神品级分级判断获得资源'''
                if self.G.等级 == 'B':
                    list = {'Y': 0, 'G': 0, 'T': 0, 'Exp': (1000 + (self.G.Lv * 100))}
                    # self.删除后获得资源(list)
                elif self.G.等级 == 'A':
                    list = {'Y': 0, 'G': 0, 'T': 5000, 'Exp': (1000 + (self.G.Lv * 100))}
                    # self.删除后获得资源(list)
                    # text = f'   请确认是否要放逐{self.G.name},放逐后你将获得5000 铜币和{(1000 + (self.G.Lv * 100))} Exp。'

                elif self.G.等级 == 'S':
                    list = {'Y': 0, 'G': 100, 'T': 20000, 'Exp': (1000 + (self.G.Lv * 100))}
                    # self.删除后获得资源(list)
                    # text = f'   请确认是否要放逐{self.G.name},放逐后你将获得100 黄金、20000 铜币和{(1000 + (self.G.Lv * 100))} Exp。'
                elif self.G.等级 == 'S1':
                    list = {'Y': 10, 'G': 200, 'T': 50000, 'Exp': (1000 + (self.G.Lv * 100))}
                    # self.删除后获得资源(list)
                    # text = f'   请确认是否要放逐{self.G.name},放逐后你将获得10勾玉、200 黄金、50000 铜币和{(1000 + (self.G.Lv * 100))} Exp。'
                elif self.G.等级 == 'SS':
                    list = {'Y': 30, 'G': 600, 'T': 60000, 'Exp': (1000 + (self.G.Lv * 100))}
                    # self.删除后获得资源(list)
                    # text = f'   请确认是否要放逐{self.G.name},放逐后你将获得30勾玉、600 黄金、60000 铜币和{(1000 + (self.G.Lv * 100))} Exp。'
                # DE.Player_Mian.exp = DE.Player_Mian.exp + (1000 + (self.G.Lv*100)) #收回经验
                '''把当前元神从列表中删除，关闭元神操作面板，刷新元神视图'''
                if G.装备 != None:
                    DE.Player_Mian.装备组.append(G.装备)  # 回收装备
                DE.Player_Mian.元神组.remove(G)
                '''注意此处业务流程，先执行删除，然后关闭操作面板，刷新元神视图场景，弹出资源页面，在刷新资源UI'''
                '''若先弹出资源页面在刷新场景会出现资源页面消失'''
                '''先刷新UI资源显示在弹出资源页面会UI资源更新不及时'''
                self.FM.destroy()
                # 切换场景(Genshin_view)
                DE.当前场景.翻页(DE.当前场景.ABCD)
                self.删除后获得资源(list)
                DE.当前场景.刷新资源UI()

            if self.G.等级 == 'B':
                text = f'   请确认是否要放逐{self.G.name},放逐后你将获得{(1000 + (self.G.Lv * 100))} Exp。'
            elif self.G.等级 == 'A':
                text = f'   请确认是否要放逐{self.G.name},放逐后你将获得5000 铜币和{(1000 + (self.G.Lv * 100))} Exp。'

            elif self.G.等级 == 'S':
                text = f'   请确认是否要放逐{self.G.name},放逐后你将获得100 黄金、20000 铜币和{(1000 + (self.G.Lv * 100))} Exp。'
            elif self.G.等级 == 'S1':
                text = f'   请确认是否要放逐{self.G.name},放逐后你将获得10勾玉、200 黄金、50000 铜币和{(1000 + (self.G.Lv * 100))} Exp。'
            elif self.G.等级 == 'SS':
                text = f'   请确认是否要放逐{self.G.name},放逐后你将获得30勾玉、600 黄金、60000 铜币和{(1000 + (self.G.Lv * 100))} Exp。'

            self.创建判断弹窗(OK, text)

        def 转换伤害类型():
            '''调用对象方法重新设置属性，然后刷新词条'''

            # 升级开销
            Overhead = {'B': 300, 'A': 800, 'S': 1200, 'S1': 1800, 'SS': 3000}

            if DE.Player_Mian.金 >= Overhead.get(self.G.等级):  # 判断金是否够使用
                DE.Player_Mian.金 = DE.Player_Mian.金 - Overhead.get(self.G.等级)  # 向Overhead获取各品级所需开销
                self.G.转换伤害类型()  # 执行元神类方法
                self.刷新属性词条()  # 执行元神操作面板词条属性刷新
                DE.当前场景.刷新资源UI()  # 执行UI资源显示刷新
            else:  # 开销不足时弹窗提示
                self.创建提示弹窗(f'资源不足，{self.G.等级}级元神转换伤害类型需要{Overhead.get(self.G.等级)}黄金。')

        def 元神升级():
            '''等级加一，初始化后天属性，刷新词条'''
            Overhead = {'B': 1000, 'A': 2000, 'S': 3000, 'S1': 5000, 'SS': 10000}
            '''扣除经验，已实装'''
            DE.Player_Mian.exp = DE.Player_Mian.exp - int((1 + (1 + self.G.Lv * 1.130)) * Overhead.get(self.G.等级))
            '''执行升级'''
            self.G.Lv = self.G.Lv + 1
            self.G.初始化基础属性()
            self.G.初始化战斗属性()
            self.刷新属性词条()
            '''判断按钮是否需要关闭'''
            if self.G.Lv >= 40:  # 40级后关闭升级按钮
                self.元神升级按钮.config(state=DISABLED)
            if DE.Player_Mian.exp < int((1 + (1 + self.G.Lv * 1.130)) * Overhead.get(self.G.等级)):  # 所需经验不足关闭升级按钮
                self.元神升级按钮.config(state=DISABLED)

            DE.当前场景.刷新资源UI()  # 刷新UI资源显示

        def 鉴赏():
            self.GB_P = Open_Jpg(os.path.join('Resource', 'picture', 'Genshin', f'{self.G.Code}-d.jpg'))
            大图宽 = self.GB_P.width()
            if 大图宽 < 1366:
                放置位置 = (1366 - 大图宽) / 2
            else:
                放置位置 = 0
            self.GB = Label(DE.当前场景.frame, image=self.GB_P)
            self.GB.place(x=放置位置, y=0)
            # self.GB_C = Button(self.GB_FM, text='查看')

            颜色 = {'B': 'chartreuse', 'A': 'cyan', 'S': '', 'S1': '', 'SS': ''}

            def off():
                self.GB.destroy()
                self.GLFM.destroy()

            self.GLFM = Frame(DE.当前场景.frame)
            self.GLFM.place(x=1230, y=660)
            self.GL_name = Label(self.GLFM, text=self.G.name, font=('Aridl', 13))
            self.GL_name.pack()
            # self.GL_等级 = Label(self.GLFM, text=self.G.等级, font=('Aridl', 13))
            # self.GL_等级.pack()
            self.GBB = Button(self.GLFM, text='关闭', command=off)
            self.GBB.pack()

        # 创建操作按钮
        # self.操作按钮区域 = Frame(self.FM,height=60, width=200).place(x=385,y=245)
        self.转换伤害类型_P = Open_Jpg(os.path.join('Resource', 'picture', 'ui', f'G_CZ_ZH.jpg'))
        self.元神升级按钮_P = Open_Jpg(os.path.join('Resource', 'picture', 'ui', f'G_CZ_UP.jpg'))
        self.删除元神按钮_P = Open_Jpg(os.path.join('Resource', 'picture', 'ui', f'G_CZ_FZ.jpg'))
        self.鉴赏功能_P = Open_Jpg(os.path.join('Resource', 'picture', 'ui', f'G_CZ_JS.jpg'))

        self.转换伤害类型 = Button(self.FM, image=self.转换伤害类型_P, command=转换伤害类型, relief=FLAT)
        self.转换伤害类型.place(x=385 + 50, y=228)

        self.删除元神按钮 = Button(self.FM, image=self.删除元神按钮_P, command=lambda: 删除元神(self.G), relief=FLAT)
        self.删除元神按钮.place(x=385 + 100, y=228)
        Overhead = {'B': 1000, 'A': 2000, 'S': 3000, 'S1': 5000, 'SS': 10000}
        '''判断是否激活升级按钮，所需经验不足时将停用升级按钮'''
        '''等级超过40级时也将停用升级按钮'''
        if self.G.Lv < 40 and DE.Player_Mian.exp >= int(int((1 + (1 + self.G.Lv * 1.130)) * Overhead.get(self.G.等级))):
            self.元神升级按钮 = Button(self.FM, image=self.元神升级按钮_P, command=元神升级, relief=FLAT)
        else:
            self.元神升级按钮 = Button(self.FM, image=self.元神升级按钮_P, command=元神升级, relief=FLAT, state=DISABLED)
        self.元神升级按钮.place(x=385, y=228)

        self.鉴赏功能 = Button(self.FM, image=self.鉴赏功能_P, command=鉴赏, relief=FLAT)
        self.鉴赏功能.place(x=386 + 150, y=228)

    def 刷新属性词条(self):
        '''通过set刷新属性词条'''
        self.S_LV.set('Lv: ' + str(self.G.Lv))
        self.S_伤害类型.set('伤害类型：' + self.G.伤害类型)
        self.S_HP.set('HP: ' + str(self.G.HP))
        self.S_力量.set('力量: ' + str(self.G.力量))
        self.S_智慧.set('智慧: ' + str(self.G.智慧))
        self.S_体力.set('体力: ' + str(self.G.体力))
        self.S_敏捷.set('敏捷: ' + str(self.G.敏捷))

        self.S_力量资质.set('力量资质: ' + str(self.G.力量资质))
        self.S_智慧资质.set('智慧资质: ' + str(self.G.智慧资质))
        self.S_体力资质.set('体力资质: ' + str(self.G.体力资质))
        self.S_敏捷资质.set('敏捷资质: ' + str(self.G.敏捷资质))
        # 后天属性
        self.S_后天属性.set('后天属性：' + self.G.后天属性)
        # 战斗属性
        self.S_物理攻击.set('物理攻击: ' + str(self.G.物理攻击))
        self.S_法术攻击.set('法术攻击: ' + str(self.G.法术攻击))
        self.S_命中.set('命中: ' + str(self.G.命中))
        self.S_闪避.set('闪避: ' + str(self.G.闪避))
        Overhead = {'B': 1000, 'A': 2000, 'S': 3000, 'S1': 5000, 'SS': 10000}
        self.升级经验L_S.set(f'升级所需经验：{int((1 + (1 + self.G.Lv * 1.130)) * Overhead.get(self.G.等级))}')

    def 创建属性词条(self):
        Overhead = {'B': 1000, 'A': 2000, 'S': 3000, 'S1': 5000, 'SS': 10000}
        self.升级经验L_S = StringVar()
        self.升级经验L_S.set(f'升级所需经验：{int((1 + (1 + self.G.Lv * 1.130)) * Overhead.get(self.G.等级))}')
        self.升级经验L = Label(self.FM, textvariable=self.升级经验L_S, bg='white')

        if self.G.Lv < 40:  # 判断升级所需经验是否需要显示
            self.升级经验L.place(x=5, y=310)

        self.属性词条 = []  # 该变量未使用
        x = 385
        self.昵称 = Label(self.FM, text=self.G.name, font=('Aridl', 13), bg='white').place(x=x, y=0)

        self.S_LV = StringVar()
        self.S_LV.set('Lv: ' + str(self.G.Lv))
        self.Lv = Label(self.FM, textvariable=self.S_LV, bg='white').place(x=x, y=25)

        self.S_伤害类型 = StringVar()
        try:
            self.S_伤害类型.set('伤害类型：' + self.G.伤害类型)
        except:
            self.S_伤害类型.set('无')
        self.伤害类型 = Label(self.FM, textvariable=self.S_伤害类型, bg='white').place(x=x + 100, y=25)

        self.S_HP = StringVar()
        self.S_HP.set('HP: ' + str(self.G.HP))
        self.HP = Label(self.FM, textvariable=self.S_HP, bg='white').place(x=x, y=45)
        # 基础属性
        self.S_力量 = StringVar()
        self.S_力量.set('力量: ' + str(self.G.力量) + '    ')
        self.力量 = Label(self.FM, textvariable=self.S_力量, bg='white').place(x=x, y=65)

        self.S_智慧 = StringVar()
        self.S_智慧.set('智慧: ' + str(self.G.智慧))
        self.智慧 = Label(self.FM, textvariable=self.S_智慧, bg='white').place(x=x + 100, y=65)

        self.S_体力 = StringVar()
        self.S_体力.set('体力: ' + str(self.G.体力))
        self.体力 = Label(self.FM, textvariable=self.S_体力, bg='white').place(x=x, y=85)

        self.S_敏捷 = StringVar()
        self.S_敏捷.set('敏捷: ' + str(self.G.敏捷))
        self.敏捷 = Label(self.FM, textvariable=self.S_敏捷, bg='white').place(x=x + 100, y=85)

        # 属性资质
        self.S_力量资质 = StringVar()
        self.S_力量资质.set('力量资质: ' + str(self.G.力量资质))
        self.力量资质 = Label(self.FM, textvariable=self.S_力量资质, bg='white').place(x=x, y=125)

        self.S_智慧资质 = StringVar()
        self.S_智慧资质.set('' + '智慧资质: ' + str(self.G.智慧资质))
        self.智慧资质 = Label(self.FM, textvariable=self.S_智慧资质, bg='white').place(x=x + 100, y=125)

        self.S_体力资质 = StringVar()
        self.S_体力资质.set('体力资质: ' + str(self.G.体力资质))
        self.体力资质 = Label(self.FM, textvariable=self.S_体力资质, bg='white').place(x=x, y=105)

        self.S_敏捷资质 = StringVar()
        self.S_敏捷资质.set('敏捷资质: ' + str(self.G.敏捷资质))
        self.敏捷资质 = Label(self.FM, textvariable=self.S_敏捷资质, bg='white').place(x=x + 100, y=105)

        # 后天属性
        self.S_后天属性 = StringVar()
        self.S_后天属性.set('后天属性：' + self.G.后天属性)
        self.后天属性 = Label(self.FM, textvariable=self.S_后天属性, bg='white').place(x=x, y=145)

        # 战斗属性
        self.S_物理攻击 = StringVar()
        self.S_物理攻击.set('物理攻击: ' + str(self.G.物理攻击))
        self.物理攻击 = Label(self.FM, textvariable=self.S_物理攻击, bg='white').place(x=x, y=165)

        self.S_法术攻击 = StringVar()
        self.S_法术攻击.set('法术攻击: ' + str(self.G.法术攻击))
        self.法术攻击 = Label(self.FM, textvariable=self.S_法术攻击, bg='white').place(x=x, y=185)

        self.S_命中 = StringVar()
        self.S_命中.set('命中: ' + str(self.G.命中))
        self.命中 = Label(self.FM, textvariable=self.S_命中, bg='white').place(x=x, y=205)

        self.S_闪避 = StringVar()
        self.S_闪避.set('闪避: ' + str(self.G.闪避))
        self.闪避 = Label(self.FM, textvariable=self.S_闪避, bg='white').place(x=x + 100, y=205)


# 显示所有元神
class Genshin_view():

    def __init__(self, root):
        self.name = '元神视图'
        # self.L_image_open = Image.open(os.path.join('Resource','picture',f'BG.png')
        # self.L_image = ImageTk.PhotoImage(self.L_image_open)
        self.L_image = Open_Jpg(os.path.join('Resource', 'picture', 'BIG', f'JUSE.jpg'))
        self.frame = Frame(root, height=768, width=1366)
        self.L = Label(self.frame, image=self.L_image)
        self.L.place(x=0, y=0)
        self.frame.place(x=0, y=0)
        self.显示所有()
        # self.G_LIST_DJ()
        '''在该界面UI上显示资源'''
        self.资源UIX = 70
        self.资源UIY = 728
        self.勾玉FM = Frame(self.frame, bg='black', height=40, width=250)
        self.勾玉P_P = Open_Jpg(os.path.join('Resource', 'picture', 'ui', f'P_UI_Y.jpg'))
        self.勾玉_P = Label(self.勾玉FM, image=self.勾玉P_P, relief='solid')
        self.勾玉_P.place(x=0, y=0)
        self.勾玉S = StringVar()
        self.勾玉S.set(str(DE.Player_Mian.玉))
        self.勾玉L = Label(self.勾玉FM, textvariable=self.勾玉S, font=DE.资源font, fg='SkyBlue', bg='black').place(x=120, y=0)
        self.勾玉FM.place(x=self.资源UIX, y=self.资源UIY)

        self.黄金FM = Frame(self.frame, bg='black', height=40, width=250)
        self.黄金P_P = Open_Jpg(os.path.join('Resource', 'picture', 'ui', f'P_UI_G.jpg'))
        self.黄金_P = Label(self.黄金FM, image=self.黄金P_P, relief='solid')
        self.黄金_P.place(x=0, y=0)
        self.黄金S = StringVar()
        self.黄金S.set(str(DE.Player_Mian.金))
        self.黄金L = Label(self.黄金FM, textvariable=self.黄金S, font=DE.资源font, fg='SkyBlue', bg='black').place(x=120, y=0)
        self.黄金FM.place(x=self.资源UIX + 250, y=self.资源UIY)

        self.铜钱FM = Frame(self.frame, bg='black', height=40, width=250)
        self.铜钱P_P = Open_Jpg(os.path.join('Resource', 'picture', 'ui', f'P_UI_T.jpg'))
        self.铜钱_P = Label(self.铜钱FM, image=self.铜钱P_P, relief='solid')
        self.铜钱_P.place(x=0, y=0)
        self.铜钱S = StringVar()
        self.铜钱S.set(str(DE.Player_Mian.铜))
        self.铜钱L = Label(self.铜钱FM, textvariable=self.铜钱S, font=DE.Exp_font, fg='SkyBlue', bg='black').place(x=120, y=8)
        self.铜钱FM.place(x=self.资源UIX + 500, y=self.资源UIY)

        self.ExpFM = Frame(self.frame, bg='black', height=40, width=250)
        self.ExpP_P = Open_Jpg(os.path.join('Resource', 'picture', 'ui', f'P_UI_EXP.jpg'))
        self.Exp_P = Label(self.ExpFM, image=self.ExpP_P, relief='solid')
        self.Exp_P.place(x=0, y=0)
        self.ExpS = StringVar()
        self.ExpS.set(str(DE.Player_Mian.exp))
        self.ExpL = Label(self.ExpFM, textvariable=self.ExpS, font=DE.Exp_font, fg='SkyBlue', bg='black').place(x=120,
                                                                                                                y=8)
        self.ExpFM.place(x=self.资源UIX + 750, y=self.资源UIY)

    def 刷新资源UI(self):
        '''用于刷新UI资源'''
        self.勾玉S.set(str(DE.Player_Mian.玉))
        self.黄金S.set(str(DE.Player_Mian.金))
        self.铜钱S.set(str(DE.Player_Mian.铜))
        self.ExpS.set(str(DE.Player_Mian.exp))

    def 显示所有(self, 页码=1):
        self.ABCD = 页码
        '''页面码用于截取显示该页面需要展示的元神'''
        排序按钮y = 670  # 更变排序按钮的y坐标

        self.G_ICO = []  # 用来保存元神图标，否则会按钮对象会被覆盖，将无法正常使用
        x = 23
        y = 10
        # print(len(DE.Player_Mian.元神组))
        '''这里的if函数用来截取本页应该显示的元神数量'''
        if len(DE.Player_Mian.元神组) > 页码 * 60:  # 大于60个将进行分页

            for i in DE.Player_Mian.元神组[(页码 * 60 - 60):(页码 * 60)]:
                self.But = Genshin_But(self.frame, i, x=x, y=y)
                self.G_ICO.append(self.But)  # 将新创建的Genshin_But添加到列表
                x = x + 110
                if x > 1320:
                    y = y + 110
                    x = 23
        else:  # 小于60个不进行分页
            # print('不足')
            for i in DE.Player_Mian.元神组[(页码 * 60 - 60)::]:  # 用页码*60 主要是用来分页时判断数量使用
                self.But = Genshin_But(self.frame, i, x=x, y=y)
                self.G_ICO.append(self.But)  # 将新创建的Genshin_But添加到列表
                x = x + 110  # 放置坐标
                if x > 1320:  # 每排超过10个以后将换排摆放
                    y = y + 110
                    x = 23

        '''排序转换按钮'''
        self.排序_HP_P = Open_Jpg(os.path.join('Resource', 'picture', 'ui', f'G_PX_MP.jpg'))
        self.排序_HP = Button(self.frame, image=self.排序_HP_P, command=self.G_LIST_HP, relief=FLAT).place(x=10, y=排序按钮y)

        self.排序_WL_P = Open_Jpg(os.path.join('Resource', 'picture', 'ui', f'G_PX_WL.jpg'))
        self.排序_WL = Button(self.frame, image=self.排序_WL_P, command=self.G_LIST_WL, relief=FLAT).place(x=70, y=排序按钮y)

        self.排序_FS_P = Open_Jpg(os.path.join('Resource', 'picture', 'ui', f'G_PX_FS.jpg'))
        self.排序_FS = Button(self.frame, image=self.排序_FS_P, command=self.G_LIST_MF, relief=FLAT).place(x=130, y=排序按钮y)

        self.排序_MZ_P = Open_Jpg(os.path.join('Resource', 'picture', 'ui', f'G_PX_MZ.jpg'))
        self.排序_MZ = Button(self.frame, image=self.排序_MZ_P, command=self.G_LIST_MZ, relief=FLAT).place(x=190, y=排序按钮y)

        self.排序_S_P = Open_Jpg(os.path.join('Resource', 'picture', 'ui', f'G_PX_SB.jpg'))
        self.排序_S = Button(self.frame, image=self.排序_S_P, command=self.G_LIST_S, relief=FLAT).place(x=250, y=排序按钮y)

        '''显示字符 '排序方式' '''
        self.排序_L = Label(self.frame, text='排序方式').place(x=11, y=排序按钮y - 25)

        # 翻页按钮
        self.UP_Bu_P = Open_Jpg(os.path.join('Resource', 'picture', 'ui', f'UP.jpg'))
        if 页码 == 1:  # 页码=1时，上翻页无效
            self.UP_Bu = Button(self.frame, image=self.UP_Bu_P)
            self.UP_Bu.place(x=1, y=排序按钮y + 60)
        else:
            self.UP_Bu = Button(self.frame, image=self.UP_Bu_P, command=lambda: self.翻页(Y=页码 - 1))
            self.UP_Bu.place(x=1, y=排序按钮y + 60)

        self.Don_Bu_P = Open_Jpg(os.path.join('Resource', 'picture', 'ui', f'DON.jpg'))
        if len(DE.Player_Mian.元神组) > 页码 * 60:  # 元神数量大于60时下翻页生效
            self.Don_Bu = Button(self.frame, image=self.Don_Bu_P, command=lambda: self.翻页(Y=页码 + 1))
        else:
            self.Don_Bu = Button(self.frame, image=self.Don_Bu_P)

        self.Don_Bu.place(x=1334, y=排序按钮y + 60)

        # self.排序_LV = Button(self.frame, text='LV', command=self.G_LIST_Lv).place(x=30, y=700)
        # self.排序_WL = Button(self.frame, text='物理攻击', command=self.G_LIST_WL).place(x=100, y=700)
        # self.排序_FS = Button(self.frame, text='法术攻击', command=self.G_LIST_MF).place(x=150, y=700)

    def 翻页(self, Y):
        '''for循环用来批量关闭已创建的元神图标按钮'''
        for i in self.G_ICO:
            i.destroy()
        self.显示所有(页码=Y)  # 创建新页码

    def run(self):
        self.frame.place(x=0, y=0)

    def off(self):
        self.frame.place_forget()
        del self.G_ICO

    '''排序方法执行函数'''

    def G_LIST_MZ(self):
        # 列表排序 #x 对象属性
        DE.Player_Mian.元神组 = sorted(DE.Player_Mian.元神组, key=lambda x: x.命中, reverse=True)
        # for i in list:
        # print(i.HP)
        切换场景(Genshin_view)

    def G_LIST_S(self):
        # 列表排序 #x 对象属性
        DE.Player_Mian.元神组 = sorted(DE.Player_Mian.元神组, key=lambda x: x.闪避, reverse=True)
        # for i in list:
        # print(i.HP)
        切换场景(Genshin_view)

    def G_LIST_MF(self):
        # 列表排序 #x 对象属性
        DE.Player_Mian.元神组 = sorted(DE.Player_Mian.元神组, key=lambda x: x.法术攻击, reverse=True)
        # for i in list:
        # print(i.HP)
        切换场景(Genshin_view)

    def G_LIST_HP(self):

        DE.Player_Mian.元神组 = sorted(DE.Player_Mian.元神组, key=lambda x: x.HP, reverse=True)
        # for i in list:
        # print(i.HP)
        切换场景(Genshin_view)

    def G_LIST_Lv(self):

        DE.Player_Mian.元神组 = sorted(DE.Player_Mian.元神组, key=lambda x: x.Lv, reverse=True)
        # for i in list:
        # print(i.HP)
        切换场景(Genshin_view)

    def G_LIST_WL(self):
        DE.Player_Mian.元神组 = sorted(DE.Player_Mian.元神组, key=lambda x: x.物理攻击, reverse=True)
        # for i in list:
        # print(i.HP)
        切换场景(Genshin_view)

        #


# 装备操作按钮
class Equipment_But():

    def __init__(self, root, i, x, y):  # 创建时将提供放置坐标
        self.E = i
        # Resource\picture\Genshin\VUGXQ-x.jpg
        self.BUT_P = Open_Jpg(os.path.join('Resource', 'picture', 'Equipment', f'{self.E.Code}.jpg'))
        self.BUT = Button(root, image=self.BUT_P, command=self.创建装备信息面板, relief=FLAT)
        self.BUT.place(x=x, y=y)

    def 创建装备信息面板(self):
        self.操作视图 = 装备操作视图(self.E)

    def destroy(self):
        # 未使用的函数
        self.BUT.destroy()


# 显示所有装备
class Equipment_view():
    def __init__(self, root):
        self.name = '装备视图'
        # self.L_image_open = Image.open(os.path.join('Resource','picture',f'BG.png')
        # self.L_image = ImageTk.PhotoImage(self.L_image_open)
        self.L_image = Open_Jpg(os.path.join('Resource', 'picture', 'BIG', f'JUSE.jpg'))
        self.frame = Frame(root, height=768, width=1366)
        self.L = Label(self.frame, image=self.L_image)
        self.L.place(x=0, y=0)
        self.frame.place(x=0, y=0)
        # self.G_LIST_DJ()
        '''在该界面UI上显示资源'''
        self.资源UIX = 70
        self.资源UIY = 728
        self.勾玉FM = Frame(self.frame, bg='black', height=40, width=250)
        self.勾玉P_P = Open_Jpg(os.path.join('Resource', 'picture', 'ui', f'P_UI_Y.jpg'))
        self.勾玉_P = Label(self.勾玉FM, image=self.勾玉P_P, relief='solid')
        self.勾玉_P.place(x=0, y=0)
        self.勾玉S = StringVar()
        self.勾玉S.set(str(DE.Player_Mian.玉))
        self.勾玉L = Label(self.勾玉FM, textvariable=self.勾玉S, font=DE.资源font, fg='SkyBlue', bg='black').place(x=120, y=0)
        self.勾玉FM.place(x=self.资源UIX, y=self.资源UIY)

        self.黄金FM = Frame(self.frame, bg='black', height=40, width=250)
        self.黄金P_P = Open_Jpg(os.path.join('Resource', 'picture', 'ui', f'P_UI_G.jpg'))
        self.黄金_P = Label(self.黄金FM, image=self.黄金P_P, relief='solid')
        self.黄金_P.place(x=0, y=0)
        self.黄金S = StringVar()
        self.黄金S.set(str(DE.Player_Mian.金))
        self.黄金L = Label(self.黄金FM, textvariable=self.黄金S, font=DE.资源font, fg='SkyBlue', bg='black').place(x=120, y=0)
        self.黄金FM.place(x=self.资源UIX + 250, y=self.资源UIY)

        self.铜钱FM = Frame(self.frame, bg='black', height=40, width=250)
        self.铜钱P_P = Open_Jpg(os.path.join('Resource', 'picture', 'ui', f'P_UI_T.jpg'))
        self.铜钱_P = Label(self.铜钱FM, image=self.铜钱P_P, relief='solid')
        self.铜钱_P.place(x=0, y=0)
        self.铜钱S = StringVar()
        self.铜钱S.set(str(DE.Player_Mian.铜))
        self.铜钱L = Label(self.铜钱FM, textvariable=self.铜钱S, font=DE.Exp_font, fg='SkyBlue', bg='black').place(x=120, y=8)
        self.铜钱FM.place(x=self.资源UIX + 500, y=self.资源UIY)

        self.ExpFM = Frame(self.frame, bg='black', height=40, width=250)
        self.ExpP_P = Open_Jpg(os.path.join('Resource', 'picture', 'ui', f'P_UI_EXP.jpg'))
        self.Exp_P = Label(self.ExpFM, image=self.ExpP_P, relief='solid')
        self.Exp_P.place(x=0, y=0)
        self.ExpS = StringVar()
        self.ExpS.set(str(DE.Player_Mian.exp))
        self.ExpL = Label(self.ExpFM, textvariable=self.ExpS, font=DE.Exp_font, fg='SkyBlue', bg='black').place(x=120,
                                                                                                                y=8)
        self.ExpFM.place(x=self.资源UIX + 750, y=self.资源UIY)

        self.显示所有()

    def 刷新资源UI(self):
        '''用于刷新UI资源'''
        self.勾玉S.set(str(DE.Player_Mian.玉))
        self.黄金S.set(str(DE.Player_Mian.金))
        self.铜钱S.set(str(DE.Player_Mian.铜))
        self.ExpS.set(str(DE.Player_Mian.exp))

    def 显示所有(self, 页码=1):
        self.当前页码 = 页码
        '''页面码用于截取显示该页面需要展示的元神'''
        排序按钮y = 670  # 更变排序按钮的y坐标

        self.G_ICO = []  # 用来保存元神图标，否则会按钮对象会被覆盖，将无法正常使用
        x = 48
        y = 10
        # print(len(DE.Player_Mian.元神组))
        '''这里的if函数用来截取本页应该显示的元神数量'''
        if len(DE.Player_Mian.装备组) > 页码 * 24:  # 大于60个将进行分页

            for i in DE.Player_Mian.装备组[(页码 * 24 - 24):(页码 * 24)]:
                self.But = Equipment_But(self.frame, i, x=x, y=y)
                self.G_ICO.append(self.But)  # 将新创建的Genshin_But添加到列表
                x = x + 160
                if x > 1280:
                    y = y + 190
                    x = 48
        else:  # 小于60个不进行分页
            # print('不足')
            for i in DE.Player_Mian.装备组[(页码 * 24 - 24)::]:  # 用页码*60 主要是用来分页时判断数量使用
                self.But = Equipment_But(self.frame, i, x=x, y=y)
                self.G_ICO.append(self.But)  # 将新创建的Genshin_But添加到列表
                x = x + 160
                if x > 1280:
                    y = y + 190
                    x = 48

        '''排序转换按钮'''

        按钮开始位置 = 10
        按钮间隙 = 70

        # self.排序_HP_P = Open_Jpg(os.path.join('Resource','picture','ui',f'G_PX_MP.jpg'))
        self.排序_HP = Button(self.frame, text='力量加强', command=self.E_LIST_L, relief=FLAT).place(x=按钮开始位置, y=排序按钮y)

        # self.排序_WL_P = Open_Jpg(os.path.join('Resource','picture','ui',f'G_PX_WL.jpg'))
        self.排序_WL = Button(self.frame, text='智力加强', command=self.E_LIST_ZL, relief=FLAT).place(x=按钮开始位置 + 按钮间隙,
                                                                                                y=排序按钮y)

        # self.排序_FS_P = Open_Jpg(os.path.join('Resource','picture','ui',f'G_PX_FS.jpg'))
        self.排序_FS = Button(self.frame, text='体力加强', command=self.E_LIST_TL, relief=FLAT).place(x=按钮开始位置 + 按钮间隙 * 2,
                                                                                                y=排序按钮y)

        # self.排序_MZ_P = Open_Jpg(os.path.join('Resource','picture','ui',f'G_PX_MZ.jpg'))
        self.排序_MZ = Button(self.frame, text='敏捷加强', command=self.E_LIST_MJ, relief=FLAT).place(x=按钮开始位置 + 按钮间隙 * 3,
                                                                                                y=排序按钮y)

        # self.排序_S_P = Open_Jpg(os.path.join('Resource','picture','ui',f'G_PX_SB.jpg'))
        self.排序_S = Button(self.frame, text='完美程度', command=self.E_LIST_WM, relief=FLAT).place(x=按钮开始位置 + 按钮间隙 * 4,
                                                                                               y=排序按钮y)

        '''显示字符 '排序方式' '''
        self.排序_L = Label(self.frame, text=f'排序方式' + f'   共计装备:{len(DE.Player_Mian.装备组)} 件') \
            .place(x=11, y=排序按钮y - 25)

        # 翻页按钮
        self.UP_Bu_P = Open_Jpg(os.path.join('Resource', 'picture', 'ui', f'UP.jpg'))
        if 页码 == 1:  # 页码=1时，上翻页无效
            self.UP_Bu = Button(self.frame, image=self.UP_Bu_P)
            self.UP_Bu.place(x=1, y=排序按钮y + 60)
        else:
            self.UP_Bu = Button(self.frame, image=self.UP_Bu_P, command=lambda: self.翻页(Y=页码 - 1))
            self.UP_Bu.place(x=1, y=排序按钮y + 60)

        self.Don_Bu_P = Open_Jpg(os.path.join('Resource', 'picture', 'ui', f'DON.jpg'))
        if len(DE.Player_Mian.装备组) > 页码 * 24:  # 元神数量大于60时下翻页生效
            self.Don_Bu = Button(self.frame, image=self.Don_Bu_P, command=lambda: self.翻页(Y=页码 + 1))
        else:
            self.Don_Bu = Button(self.frame, image=self.Don_Bu_P)

        self.Don_Bu.place(x=1334, y=排序按钮y + 60)

        # self.排序_LV = Button(self.frame, text='LV', command=self.G_LIST_Lv).place(x=30, y=700)
        # self.排序_WL = Button(self.frame, text='物理攻击', command=self.G_LIST_WL).place(x=100, y=700)
        # self.排序_FS = Button(self.frame, text='法术攻击', command=self.G_LIST_MF).place(x=150, y=700)

    def 翻页(self, Y):
        '''for循环用来批量关闭已创建的元神图标按钮'''
        for i in self.G_ICO:
            i.destroy()
        self.显示所有(页码=Y)  # 创建新页码

    def run(self):
        self.frame.place(x=0, y=0)

    def off(self):
        self.frame.place_forget()
        del self.G_ICO

    '''排序方法执行函数'''

    def E_LIST_MJ(self):
        # 列表排序 #x 对象属性
        DE.Player_Mian.装备组 = sorted(DE.Player_Mian.装备组, key=lambda x: x.敏捷资质, reverse=True)
        # for i in list:
        # print(i.HP)
        切换场景(Equipment_view)

    def E_LIST_WM(self):
        # 列表排序 #x 对象属性
        DE.Player_Mian.装备组 = sorted(DE.Player_Mian.装备组, key=lambda x: x.完美程度, reverse=True)
        # for i in list:
        # print(i.HP)
        切换场景(Equipment_view)

    def E_LIST_TL(self):
        # 列表排序 #x 对象属性
        DE.Player_Mian.装备组 = sorted(DE.Player_Mian.装备组, key=lambda x: x.体力资质, reverse=True)
        # for i in list:
        # print(i.HP)
        切换场景(Equipment_view)

    def E_LIST_L(self):

        DE.Player_Mian.装备组 = sorted(DE.Player_Mian.装备组, key=lambda x: x.力量资质, reverse=True)
        # for i in list:
        # print(i.HP)
        切换场景(Equipment_view)

    def G_LIST_Lv(self):

        DE.Player_Mian.装备组 = sorted(DE.Player_Mian.装备组, key=lambda x: x.Lv, reverse=True)
        # for i in list:
        # print(i.HP)
        切换场景(Genshin_view)

    def E_LIST_ZL(self):
        DE.Player_Mian.装备组 = sorted(DE.Player_Mian.装备组, key=lambda x: x.智慧资质, reverse=True)
        # for i in list:
        # print(i.HP)
        切换场景(Equipment_view)

        #


# 好像未使用
class Game():  # 好像未使用
    def __init__(self, root):
        self.name = '游戏主界面'
        self.x = 1366
        self.y = 768
        # self.L_image_open = Image.open(os.path.join('Resource','picture',f'BG.png')
        # self.L_image = ImageTk.PhotoImage(self.L_image_open)
        self.L_image = Open_Jpg(os.path.join('Resource', 'picture', f'BG.jpg'))
        self.frame = Frame(root, height=768, width=1366)
        self.背景图标签 = Label(self.frame, image=self.L_image)
        self.背景图标签.pack()
        self.frame.place(x=0, y=0)

    def run(self):
        self.frame.place(x=0, y=0)

    def off(self):
        self.frame.place_forget()


# 背包视图 未用
class Backpack():
    def __init__(self, root):
        self.name = '背包'
        # self.L_image_open = Image.open(os.path.join('Resource','picture',f'BG.png')
        # self.L_image = ImageTk.PhotoImage(self.L_image_open)
        self.L_image = Open_Jpg(os.path.join('Resource', 'picture', f'BK.jpg'))
        self.frame = Frame(root, height=768, width=1366)
        self.L = Label(self.frame, image=self.L_image)
        self.L.place(x=0, y=0)
        self.frame.place(x=0, y=0)

    def run(self):
        self.frame.place(x=0, y=0)

    def off(self):
        self.frame.place_forget()


# 战斗场景选择
class Map():
    def __init__(self, root):
        self.name = '世界地图'
        # self.L_image_open = Image.open(os.path.join('Resource','picture',f'BG.png')
        # self.L_image = ImageTk.PhotoImage(self.L_image_open)
        self.L_image = Open_Jpg(os.path.join('Resource', 'picture', f'LG.jpg'))
        self.frame = Frame(root, height=768, width=1366)
        self.L = Label(self.frame, image=self.L_image)
        self.L.place(x=0, y=0)
        self.frame.place(x=0, y=0)
        self.创建UI按钮()
        self.start_b_l = Open_Jpg(os.path.join('Resource', 'picture', 'ui', 'start.jpg'))

        DE.敌人阵容 = []

    def 创建UI按钮(self):
        # 副本选择
        self.宿敌系统_P = Open_Jpg(os.path.join('Resource', 'picture', 'MapTT', f'SD.jpg'))
        self.宿敌系统 = Button(self.frame, image=self.宿敌系统_P, command=self.宿敌副本, relief=FLAT, bg='white')
        self.宿敌系统.place(x=1200, y=10)

        按钮间隔_y = 85

        self.斗法_P = Open_Jpg(os.path.join('Resource', 'picture', 'MapTT', f'DF.jpg'))
        self.斗法 = Button(self.frame, image=self.斗法_P, relief=FLAT, bg='white', command=self.斗法副本创建界面)
        self.斗法.place(x=1200, y=95)

        self.大魔王_P = Open_Jpg(os.path.join('Resource', 'picture', 'MapTT', f'DMW.jpg'))
        self.大魔王 = Button(self.frame, image=self.大魔王_P, relief=FLAT, bg='white', command=self.创建大魔王副本)
        self.大魔王.place(x=1200, y=180)

        self.莉莉崽_P = Open_Jpg(os.path.join('Resource', 'picture', 'MapTT', f'TZLLZ.jpg'))
        self.莉莉崽 = Button(self.frame, image=self.莉莉崽_P, relief=FLAT, bg='white', command=self.创建莉莉崽副本)
        self.莉莉崽.place(x=1200, y=10 + 按钮间隔_y * 3)

        self.训练场_P = Open_Jpg(os.path.join('Resource', 'picture', 'MapTT', f'XLC.jpg'))
        self.训练场 = Button(self.frame, image=self.训练场_P, relief=FLAT, bg='white', command=self.创建训练场副本)
        self.训练场.place(x=1200, y=10 + 按钮间隔_y * 7)

        self.花朝节_P = Open_Jpg(os.path.join('Resource', 'picture', 'MapTT', f'HZJ.jpg'))
        self.花朝节 = Button(self.frame, image=self.花朝节_P, relief=FLAT, bg='white', command=self.创建花朝节副本)
        self.花朝节.place(x=1200, y=10 + 按钮间隔_y * 4)

    # 宿敌副本处理
    def 宿敌副本(self):
        self.sync_()

        def 随机生成APC(GLv=40, ELv=20):
            G = DE.Genshin(DE.Y元神列表[random.randint(0, len(DE.Y元神列表)) - 1])
            # G = DE.Genshin(DE.Y元神列表[6])
            ABC = DE.Z装备列表[random.randint(0, len(DE.Z装备列表)) - 1]
            ABC.append('传承')
            G.装备 = DE.Equipment(ABC)
            G.装备.强化等级 = ELv
            G.装备.装备强化()
            G.Lv = GLv
            G.初始化基础属性()
            G.初始化战斗属性()
            # print(G.name, G.HP,
            # G.物理攻击, G.法术攻击, G.命中, G.闪避, G.伤害类型, G.装备.name)

            # 宿敌掉落奖励初始化
            reward.init_Magnification = 100
            reward.sets({'Y': 0 * GLv, 'G': int(0.5 * GLv), 'T': 800 * GLv, 'Exp': 1000 * GLv})
            DE.Player_Mian.铜 = DE.Player_Mian.铜 - 100
            return G

        def off():
            self.当前窗口.destroy()
            self.宿敌系统.place(x=1200, y=10)
            切换场景(Map)
            try:
                self.阵容选择界面.LFM.destroy()
                self.阵容选择界面.GFM.destroy()
            except:
                pass

        self.当前窗口 = LabelFrame(self.frame, text='宿敌', height=450, width=610, bg='white')
        self.当前窗口.place(x=1366 / 2 - 305, y=70)

        self.宿敌_普通 = Button(self.当前窗口, text='普通', relief=FLAT, bg='white',
                            command=lambda: self.创建宿敌面板(G=随机生成APC(GLv=20, ELv=3)))
        self.宿敌_普通.place(x=1, y=1)
        self.宿敌_冒险 = Button(self.当前窗口, text='冒险', relief=FLAT, bg='white',
                            command=lambda: self.创建宿敌面板(G=随机生成APC(GLv=40, ELv=10)))
        self.宿敌_冒险.place(x=100, y=1)
        self.宿敌_英雄 = Button(self.当前窗口, text='英雄', relief=FLAT, bg='white',
                            command=lambda: self.创建宿敌面板(G=随机生成APC(GLv=40, ELv=20)))
        self.宿敌_英雄.place(x=200, y=1)
        self.宿敌_王者 = Button(self.当前窗口, text='王者', relief=FLAT, bg='white',
                            command=lambda: self.创建宿敌面板(G=随机生成APC(GLv=45, ELv=25)))
        self.宿敌_王者.place(x=300, y=1)
        self.玩法介绍文本 = Label(self.当前窗口, text='*玩法：1v1\n*刷新费用：100 铜 \n*获得奖励：大量经验、铜币、黄金'
                            , bg='white', justify=LEFT).place(x=35, y=250)

        self.提示 = Label(self.当前窗口, text='*使用相同元神挑战宿敌奖励翻倍', bg='white', fg='red', font=('Aridl', 8))
        self.提示.place(x=0, y=405)

        self.关闭 = Button(self.当前窗口, text='关闭', relief=FLAT, bg='white', command=off).place(x=550, y=1)

        self.创建宿敌面板(G=随机生成APC(GLv=20, ELv=3))
        DE.Player_Mian.铜 = DE.Player_Mian.铜 + 100

    def 创建宿敌面板(self, G):

        try:
            self.阵容选择界面 = None
        except:
            pass

        try:
            self.大魔王_FM.destroy()
        except:
            pass
        self.宿敌G = G
        G = G
        self.大魔王_FM = LabelFrame(self.当前窗口, text=G.name + '  *  ' + G.ID + '*' + G.等级, height=365,
                                 width=604, bg='white', )
        # bg='white' 白色背景
        self.大魔王_FM.place(x=0, y=33)
        # self.宿敌_FM.config(bg='red')
        # 立绘
        self.LH_P = Open_Jpg(os.path.join('Resource', 'picture', 'Genshin', f'{G.Code}-x.jpg'))  # 元神小立绘
        self.LH = Label(self.大魔王_FM, image=self.LH_P)
        self.LH.place(x=5, y=0)
        # 装备图标
        if G.装备 == None:
            self.ZBLH_P = Open_Jpg(os.path.join('Resource', 'picture', 'Equipment', f'O.jpg'))
        else:
            self.ZBLH_P = Open_Jpg(os.path.join('Resource', 'picture', 'Equipment', f'{G.装备.Code}.jpg'))
            if G.装备.强化等级 != 0:
                self.ENAMEL = Label(self.大魔王_FM, text='+' + str(G.装备.强化等级) + G.装备.name + '-' + G.装备.ID,
                                    bg='white', fg=DE.装备字体颜色.get(G.装备.品级)).place(x=220, y=185)
            else:
                self.ENAMEL = Label(self.大魔王_FM, text=G.装备.name + '-' + G.装备.ID,
                                    bg='white', fg=DE.装备字体颜色.get(G.装备.品级)).place(x=220, y=185)
            self.ELL = Label(self.大魔王_FM, text='力量+' + str(G.装备.力量), bg='white').place(x=220, y=205)
            self.EZH = Label(self.大魔王_FM, text='智慧+' + str(G.装备.智慧), bg='white').place(x=310, y=205)
            self.ETL = Label(self.大魔王_FM, text='体力+' + str(G.装备.体力), bg='white').place(x=220, y=225)
            self.EMJ = Label(self.大魔王_FM, text='敏捷+' + str(G.装备.敏捷), bg='white').place(x=310, y=225)

            self.ELLZ = Label(self.大魔王_FM, text='力量强化+' + str(G.装备.力量资质), bg='white').place(x=220, y=245)
            self.EZZH = Label(self.大魔王_FM, text='智慧强化+' + str(G.装备.智慧资质), bg='white').place(x=220, y=265)
            self.ETLZ = Label(self.大魔王_FM, text='体力强化+' + str(G.装备.体力资质), bg='white').place(x=220, y=285)
            self.ETLZ = Label(self.大魔王_FM, text='敏捷强化+' + str(G.装备.敏捷资质), bg='white').place(x=220, y=305)
            self.ETLZ = Label(self.大魔王_FM, text='成色；' + str(G.装备.完美程度), bg='white').place(x=310, y=305)
        self.ZBLH = Label(self.大魔王_FM, image=self.ZBLH_P, relief=FLAT)
        self.ZBLH.place(x=215, y=3)
        # 属性
        self.属性词条 = []  # 该变量未使用
        x = 385
        self.昵称 = Label(self.大魔王_FM, text=G.name, font=('Aridl', 13), bg='white').place(x=x, y=0)

        self.S_LV = StringVar()
        self.S_LV.set('Lv: ' + str(G.Lv))
        self.Lv = Label(self.大魔王_FM, textvariable=self.S_LV, bg='white').place(x=x, y=25)

        self.S_伤害类型 = StringVar()
        try:
            self.S_伤害类型.set('伤害类型：' + G.伤害类型)
        except:
            self.S_伤害类型.set('无')
        self.伤害类型 = Label(self.大魔王_FM, textvariable=self.S_伤害类型, bg='white').place(x=x + 100, y=25)

        self.S_HP = StringVar()
        self.S_HP.set('HP: ' + str(G.HP))
        self.HP = Label(self.大魔王_FM, textvariable=self.S_HP, bg='white').place(x=x, y=45)
        # 基础属性
        self.S_力量 = StringVar()
        self.S_力量.set('力量: ' + str(G.力量) + '    ')
        self.力量 = Label(self.大魔王_FM, textvariable=self.S_力量, bg='white').place(x=x, y=65)

        self.S_智慧 = StringVar()
        self.S_智慧.set('智慧: ' + str(G.智慧))
        self.智慧 = Label(self.大魔王_FM, textvariable=self.S_智慧, bg='white').place(x=x + 100, y=65)

        self.S_体力 = StringVar()
        self.S_体力.set('体力: ' + str(G.体力))
        self.体力 = Label(self.大魔王_FM, textvariable=self.S_体力, bg='white').place(x=x, y=85)

        self.S_敏捷 = StringVar()
        self.S_敏捷.set('敏捷: ' + str(G.敏捷))
        self.敏捷 = Label(self.大魔王_FM, textvariable=self.S_敏捷, bg='white').place(x=x + 100, y=85)

        # 属性资质
        self.S_力量资质 = StringVar()
        self.S_力量资质.set('力量资质: ' + str(G.力量资质))
        self.力量资质 = Label(self.大魔王_FM, textvariable=self.S_力量资质, bg='white').place(x=x, y=125)

        self.S_智慧资质 = StringVar()
        self.S_智慧资质.set('' + '智慧资质: ' + str(G.智慧资质))
        self.智慧资质 = Label(self.大魔王_FM, textvariable=self.S_智慧资质, bg='white').place(x=x + 100, y=125)

        self.S_体力资质 = StringVar()
        self.S_体力资质.set('体力资质: ' + str(G.体力资质))
        self.体力资质 = Label(self.大魔王_FM, textvariable=self.S_体力资质, bg='white').place(x=x, y=105)

        self.S_敏捷资质 = StringVar()
        self.S_敏捷资质.set('敏捷资质: ' + str(G.敏捷资质))
        self.敏捷资质 = Label(self.大魔王_FM, textvariable=self.S_敏捷资质, bg='white').place(x=x + 100, y=105)

        # 后天属性
        self.S_后天属性 = StringVar()
        self.S_后天属性.set('后天属性：' + G.后天属性)
        self.后天属性 = Label(self.大魔王_FM, textvariable=self.S_后天属性, bg='white').place(x=x, y=145)

        # 战斗属性
        self.S_物理攻击 = StringVar()
        self.S_物理攻击.set('物理攻击: ' + str(G.物理攻击))
        self.物理攻击 = Label(self.大魔王_FM, textvariable=self.S_物理攻击, bg='white').place(x=x, y=165)

        self.S_法术攻击 = StringVar()
        self.S_法术攻击.set('法术攻击: ' + str(G.法术攻击))
        self.法术攻击 = Label(self.大魔王_FM, textvariable=self.S_法术攻击, bg='white').place(x=x, y=185)

        self.S_命中 = StringVar()
        self.S_命中.set('命中: ' + str(G.命中))
        self.命中 = Label(self.大魔王_FM, textvariable=self.S_命中, bg='white').place(x=x, y=205)

        self.S_闪避 = StringVar()
        self.S_闪避.set('闪避: ' + str(G.闪避))
        self.闪避 = Label(self.大魔王_FM, textvariable=self.S_闪避, bg='white').place(x=x + 100, y=205)

        self.挑战按钮 = Button(self.大魔王_FM, image=self.start_b_l, relief=FLAT, bg='white', fg='red', command=self.挑战宿敌)
        self.挑战按钮.place(x=x, y=250)

        r_manage.set_ID(['SD', G.Code])

    def 挑战宿敌(self):
        self.宿敌_普通.place_forget()
        self.宿敌_冒险.place_forget()
        self.宿敌_英雄.place_forget()
        self.宿敌_王者.place_forget()
        self.宿敌系统.place_forget()
        self.挑战按钮.place_forget()

        self.阵容选择界面 = Lineup()

        '''try:
            self.阵容选择界面.阵容列表 = []
            self.阵容选择界面.显示阵容()
            DE.刷新阵容()
        except:
            pass'''

        DE.阵容数量 = 1  # 用来控制该模式允许上阵的最大卡牌数
        DE.敌人阵容 = [self.宿敌G]
        # print(self.宿敌G.__dict__)
        self.当前窗口.place(x=5, y=5)

    # 斗法副本处理
    def 斗法副本创建界面(self):
        self.sync_()

        def 斗法用关闭():
            切换场景(Map)

        self.当前窗口 = LabelFrame(self.frame, text='协同斗法', height=420, width=610, bg='white')
        self.当前窗口.place(x=1366 / 2 - 305, y=70)

        self.宿敌_普通 = Button(self.当前窗口, text='普通', relief=FLAT, bg='white', command=lambda: self.创建斗法副本('普通'))
        self.宿敌_普通.place(x=1, y=1)
        self.宿敌_冒险 = Button(self.当前窗口, text='冒险', relief=FLAT, bg='white', command=lambda: self.创建斗法副本('冒险'))
        self.宿敌_冒险.place(x=100, y=1)
        self.宿敌_英雄 = Button(self.当前窗口, text='英雄', relief=FLAT, bg='white', command=lambda: self.创建斗法副本('英雄'))
        self.宿敌_英雄.place(x=200, y=1)
        self.宿敌_王者 = Button(self.当前窗口, text='王者', relief=FLAT, bg='white', command=lambda: self.创建斗法副本('王者'))
        self.宿敌_王者.place(x=300, y=1)
        self.关闭 = Button(self.当前窗口, text='关闭', relief=FLAT, bg='white', command=斗法用关闭).place(x=550, y=1)
        self.玩法介绍文本 = Label(self.当前窗口, text='*玩法：5v5\n*刷新费用：10000 铜 和 60 金\n*获得奖励：大量经验、铜币、黄金'
                            , bg='white', justify=LEFT).place(x=35, y=250)

        self.开始斗法 = Button(self.当前窗口, image=self.start_b_l, bg='white', fg='red', relief=FLAT, command=self.开始战斗)
        # self.开始斗法.config(statr=DISABLED) # 关闭该按钮
        x = 30
        y = 100
        self.开始斗法.place(x=x + 440, y=y + 120)

        self.创建斗法副本('普通')

        # 返还默认创建副本的消费
        DE.Player_Mian.金 = DE.Player_Mian.金 + 60
        DE.Player_Mian.铜 = DE.Player_Mian.铜 + 10000

    def 创建斗法副本(self, 难度):
        # try:
        # self.开始斗法.config(statr=NORMAL) # 开启开始按钮
        # except:
        # pass
        DE.Player_Mian.金 = DE.Player_Mian.金 - 60
        DE.Player_Mian.铜 = DE.Player_Mian.铜 - 10000

        def 随机生成APC(GLv=40, ELv=20):
            G = DE.Genshin(DE.Y元神列表[random.randint(0, len(DE.Y元神列表)) - 1])
            # G = DE.Genshin(DE.Y元神列表[6])
            ABC = DE.Z装备列表[random.randint(0, len(DE.Z装备列表)) - 1]
            ABC.append('传承')
            G.装备 = DE.Equipment(ABC)
            G.装备.强化等级 = ELv
            G.装备.装备强化()
            G.Lv = GLv
            G.初始化基础属性()
            G.初始化战斗属性()
            # print(G.name, G.HP,
            # G.物理攻击, G.法术攻击, G.命中, G.闪避, G.伤害类型, G.装备.name)
            return G

        r_manage.set_ID(['DF'])

        DE.阵容数量 = 5  # 用来控制该模式允许上阵的最大卡牌数
        if 难度 == '普通':
            DE.敌人阵容 = [随机生成APC(GLv=20, ELv=3), 随机生成APC(GLv=20, ELv=3), 随机生成APC(GLv=20, ELv=3),
                       随机生成APC(GLv=20, ELv=3), 随机生成APC(GLv=20, ELv=3)]
            reward.init_Magnification = 150
        elif 难度 == '冒险':
            DE.敌人阵容 = [随机生成APC(GLv=40, ELv=10), 随机生成APC(GLv=40, ELv=10), 随机生成APC(GLv=40, ELv=10),
                       随机生成APC(GLv=40, ELv=10), 随机生成APC(GLv=40, ELv=10)]
            reward.init_Magnification = 250
        elif 难度 == '英雄':
            DE.敌人阵容 = [随机生成APC(GLv=40, ELv=20), 随机生成APC(GLv=40, ELv=20), 随机生成APC(GLv=40, ELv=20),
                       随机生成APC(GLv=40, ELv=20), 随机生成APC(GLv=40, ELv=20)]
            reward.init_Magnification = 300
        elif 难度 == '王者':
            DE.敌人阵容 = [随机生成APC(GLv=45, ELv=20), 随机生成APC(GLv=45, ELv=20), 随机生成APC(GLv=45, ELv=20),
                       随机生成APC(GLv=45, ELv=20), 随机生成APC(GLv=45, ELv=20)]
            reward.init_Magnification = 400

        # 斗法掉落奖励初始化
        reward.sets(Config_Config.get('R1'))
        # print(reward.Magnification, reward.data)

        x = 30
        y = 100

        self.当前阵容显示文本 = Label(self.当前窗口, text='当前阵容：', bg='white').place(x=x, y=80)
        self.斗法阵容_ICO = []

        for i in DE.敌人阵容:
            self.But = Genshin_But_斗法(self.当前窗口, i, x, y)
            self.斗法阵容_ICO.append(self.But)
            x += 110

    def 开始战斗(self):
        # print('开始斗法', len(DE.敌人阵容))
        if len(DE.敌人阵容) == 5:
            self.阵容选择界面 = Lineup()
            # self.宿敌_普通.place_forget()
            # self.宿敌_冒险.place_forget()
            # self.宿敌_英雄.place_forget()
            # self.宿敌_王者.place_forget()
            # self.宿敌系统.place_forget()
            self.开始斗法.place_forget()
            self.当前窗口.place(x=5, y=5)

        elif len(DE.敌人阵容) == 3 or len(DE.敌人阵容) == 1:
            self.阵容选择界面 = Lineup()
            # self.宿敌_普通.place_forget()
            # self.宿敌_冒险.place_forget()
            # self.宿敌_英雄.place_forget()
            # self.宿敌_王者.place_forget()
            # self.宿敌系统.place_forget()
            self.开始斗法.place_forget()
            self.当前窗口.place(x=5, y=5)

    # 大魔王副本处理
    def 创建大魔王副本(self):
        self.sync_()

        def off():
            self.当前窗口.destroy()
            self.宿敌系统.place(x=1200, y=10)
            try:
                self.阵容选择界面.LFM.destroy()
                self.阵容选择界面.GFM.destroy()
            except:
                pass

        def 关闭():
            切换场景(Map)

        self.当前窗口 = LabelFrame(self.frame, text='大魔王', height=420, width=610, bg='white')
        self.当前窗口.place(x=1366 / 2 - 305, y=70)

        self.大魔王_普通 = Button(self.当前窗口, text='普通', relief=FLAT, bg='white', command=lambda: self.大魔王召唤('普通'))
        self.大魔王_普通.place(x=1, y=1)
        self.大魔王_冒险 = Button(self.当前窗口, text='冒险', relief=FLAT, bg='white', command=lambda: self.大魔王召唤('冒险'))
        self.大魔王_冒险.place(x=100, y=1)
        self.大魔王_英雄 = Button(self.当前窗口, text='英雄', relief=FLAT, bg='white', command=lambda: self.大魔王召唤('英雄'))
        self.大魔王_英雄.place(x=200, y=1)
        self.大魔王_王者 = Button(self.当前窗口, text='王者', relief=FLAT, bg='white', command=lambda: self.大魔王召唤('王者'))
        self.大魔王_王者.place(x=300, y=1)
        self.玩法介绍文本 = Label(self.当前窗口, text='*玩法：1v5\n*刷新费用：5000 铜 和 80 金\n*获得奖励：大量经验、铜币、黄金'
                            , bg='white', justify=LEFT).place(x=35, y=250)

        self.关闭 = Button(self.当前窗口, text='关闭', relief=FLAT, bg='white', command=关闭).place(x=550, y=1)

        self.大魔王召唤('普通')
        DE.Player_Mian.金 = DE.Player_Mian.金 + 80
        DE.Player_Mian.铜 = DE.Player_Mian.铜 + 5000

    def 大魔王召唤(self, 难度):

        DE.Player_Mian.金 = DE.Player_Mian.金 - 80
        DE.Player_Mian.铜 = DE.Player_Mian.铜 - 5000
        r_manage.set_ID(['DMW'])
        try:
            self.大魔王_FM.destroy()
        except:
            pass

        def 随机生成APC(GLv=40, ELv=20):
            G = DE.Genshin(DE.Y元神列表[random.randint(0, len(DE.Y元神列表)) - 1])
            # G = DE.Genshin(DE.Y元神列表[6])
            ABC = DE.Z装备列表[random.randint(0, len(DE.Z装备列表)) - 1]
            ABC.append('传承')
            G.装备 = DE.Equipment(ABC)
            G.装备.强化等级 = ELv
            G.装备.装备强化()
            G.Lv = GLv
            G.初始化基础属性()
            G.初始化战斗属性()
            # print(G.name, G.HP,
            # G.物理攻击, G.法术攻击, G.命中, G.闪避, G.伤害类型, G.装备.name)
            return G

        DE.阵容数量 = 5  # 用来控制该模式允许上阵的最大卡牌数
        if 难度 == '普通':
            G = 随机生成APC(GLv=20, ELv=3)
            G.HP = G.HP * 10
            G.命中 = 1200
            G.闪避 = 1500
            DE.敌人阵容 = [G]
            reward.init_Magnification = 200
        elif 难度 == '冒险':
            G = 随机生成APC(GLv=40, ELv=10)
            G.HP = G.HP * 15
            G.命中 = 1800
            G.闪避 = 2000
            DE.敌人阵容 = [G]
            reward.init_Magnification = 300
        elif 难度 == '英雄':
            G = 随机生成APC(GLv=40, ELv=20)
            G.HP = G.HP * 20
            G.命中 = 2500
            G.闪避 = 2800
            DE.敌人阵容 = [G]
            reward.init_Magnification = 400
        elif 难度 == '王者':
            G = 随机生成APC(GLv=45, ELv=20)
            G.HP = G.HP * 30
            G.命中 = 3300
            G.闪避 = 3900
            DE.敌人阵容 = [G]
            reward.init_Magnification = 500

        reward.sets(Config_Config.get('R2'))  # 设置奖励格式

        self.大魔王_FM = LabelFrame(self.当前窗口, text=G.name + '  *  ' + G.ID + '*' + G.等级, height=365,
                                 width=604, bg='white', )
        # bg='white' 白色背景
        self.大魔王_FM.place(x=0, y=33)
        # self.宿敌_FM.config(bg='red')
        # 立绘
        self.LH_P = Open_Jpg(os.path.join('Resource', 'picture', 'Genshin', f'{G.Code}-x.jpg'))  # 元神小立绘
        self.LH = Label(self.大魔王_FM, image=self.LH_P)
        self.LH.place(x=5, y=0)
        # 装备图标
        if G.装备 == None:
            self.ZBLH_P = Open_Jpg(os.path.join('Resource', 'picture', 'Equipment', f'O.jpg'))
        else:
            self.ZBLH_P = Open_Jpg(os.path.join('Resource', 'picture', 'Equipment', f'{G.装备.Code}.jpg'))
            if G.装备.强化等级 != 0:
                self.ENAMEL = Label(self.大魔王_FM, text='+' + str(G.装备.强化等级) + G.装备.name + '-' + G.装备.ID,
                                    bg='white', fg=DE.装备字体颜色.get(G.装备.品级)).place(x=220, y=185)
            else:
                self.ENAMEL = Label(self.大魔王_FM, text=G.装备.name + '-' + G.装备.ID,
                                    bg='white', fg=DE.装备字体颜色.get(G.装备.品级)).place(x=220, y=185)
            self.ELL = Label(self.大魔王_FM, text='力量+' + str(G.装备.力量), bg='white').place(x=220, y=205)
            self.EZH = Label(self.大魔王_FM, text='智慧+' + str(G.装备.智慧), bg='white').place(x=310, y=205)
            self.ETL = Label(self.大魔王_FM, text='体力+' + str(G.装备.体力), bg='white').place(x=220, y=225)
            self.EMJ = Label(self.大魔王_FM, text='敏捷+' + str(G.装备.敏捷), bg='white').place(x=310, y=225)

            self.ELLZ = Label(self.大魔王_FM, text='力量强化+' + str(G.装备.力量资质), bg='white').place(x=220, y=245)
            self.EZZH = Label(self.大魔王_FM, text='智慧强化+' + str(G.装备.智慧资质), bg='white').place(x=220, y=265)
            self.ETLZ = Label(self.大魔王_FM, text='体力强化+' + str(G.装备.体力资质), bg='white').place(x=220, y=285)
            self.ETLZ = Label(self.大魔王_FM, text='敏捷强化+' + str(G.装备.敏捷资质), bg='white').place(x=220, y=305)
            self.ETLZ = Label(self.大魔王_FM, text='成色；' + str(G.装备.完美程度), bg='white').place(x=310, y=305)
        self.ZBLH = Label(self.大魔王_FM, image=self.ZBLH_P, relief=FLAT)
        self.ZBLH.place(x=215, y=3)
        # 属性
        self.属性词条 = []  # 该变量未使用
        x = 385
        self.昵称 = Label(self.大魔王_FM, text=G.name, font=('Aridl', 13), bg='white').place(x=x, y=0)

        self.S_LV = StringVar()
        self.S_LV.set('Lv: ' + str(G.Lv))
        self.Lv = Label(self.大魔王_FM, textvariable=self.S_LV, bg='white').place(x=x, y=25)

        self.S_伤害类型 = StringVar()
        try:
            self.S_伤害类型.set('伤害类型：' + G.伤害类型)
        except:
            self.S_伤害类型.set('无')
        self.伤害类型 = Label(self.大魔王_FM, textvariable=self.S_伤害类型, bg='white').place(x=x + 100, y=25)

        self.S_HP = StringVar()
        self.S_HP.set('HP: ' + str(G.HP))
        self.HP = Label(self.大魔王_FM, textvariable=self.S_HP, bg='white').place(x=x, y=45)
        # 基础属性
        self.S_力量 = StringVar()
        self.S_力量.set('力量: ' + str(G.力量) + '    ')
        self.力量 = Label(self.大魔王_FM, textvariable=self.S_力量, bg='white').place(x=x, y=65)

        self.S_智慧 = StringVar()
        self.S_智慧.set('智慧: ' + str(G.智慧))
        self.智慧 = Label(self.大魔王_FM, textvariable=self.S_智慧, bg='white').place(x=x + 100, y=65)

        self.S_体力 = StringVar()
        self.S_体力.set('体力: ' + str(G.体力))
        self.体力 = Label(self.大魔王_FM, textvariable=self.S_体力, bg='white').place(x=x, y=85)

        self.S_敏捷 = StringVar()
        self.S_敏捷.set('敏捷: ' + str(G.敏捷))
        self.敏捷 = Label(self.大魔王_FM, textvariable=self.S_敏捷, bg='white').place(x=x + 100, y=85)

        # 属性资质
        self.S_力量资质 = StringVar()
        self.S_力量资质.set('力量资质: ' + str(G.力量资质))
        self.力量资质 = Label(self.大魔王_FM, textvariable=self.S_力量资质, bg='white').place(x=x, y=125)

        self.S_智慧资质 = StringVar()
        self.S_智慧资质.set('' + '智慧资质: ' + str(G.智慧资质))
        self.智慧资质 = Label(self.大魔王_FM, textvariable=self.S_智慧资质, bg='white').place(x=x + 100, y=125)

        self.S_体力资质 = StringVar()
        self.S_体力资质.set('体力资质: ' + str(G.体力资质))
        self.体力资质 = Label(self.大魔王_FM, textvariable=self.S_体力资质, bg='white').place(x=x, y=105)

        self.S_敏捷资质 = StringVar()
        self.S_敏捷资质.set('敏捷资质: ' + str(G.敏捷资质))
        self.敏捷资质 = Label(self.大魔王_FM, textvariable=self.S_敏捷资质, bg='white').place(x=x + 100, y=105)

        # 后天属性
        self.S_后天属性 = StringVar()
        self.S_后天属性.set('后天属性：' + G.后天属性)
        self.后天属性 = Label(self.大魔王_FM, textvariable=self.S_后天属性, bg='white').place(x=x, y=145)

        # 战斗属性
        self.S_物理攻击 = StringVar()
        self.S_物理攻击.set('物理攻击: ' + str(G.物理攻击))
        self.物理攻击 = Label(self.大魔王_FM, textvariable=self.S_物理攻击, bg='white').place(x=x, y=165)

        self.S_法术攻击 = StringVar()
        self.S_法术攻击.set('法术攻击: ' + str(G.法术攻击))
        self.法术攻击 = Label(self.大魔王_FM, textvariable=self.S_法术攻击, bg='white').place(x=x, y=185)

        self.S_命中 = StringVar()
        self.S_命中.set('命中: ' + str(G.命中))
        self.命中 = Label(self.大魔王_FM, textvariable=self.S_命中, bg='white').place(x=x, y=205)

        self.S_闪避 = StringVar()
        self.S_闪避.set('闪避: ' + str(G.闪避))
        self.闪避 = Label(self.大魔王_FM, textvariable=self.S_闪避, bg='white').place(x=x + 100, y=205)
        self.挑战按钮 = Button(self.大魔王_FM, image=self.start_b_l, relief=FLAT, bg='white', fg='red', command=self.挑战大魔王)
        self.挑战按钮.place(x=x, y=250)

    def 挑战大魔王(self):
        self.大魔王_普通.place_forget()
        self.大魔王_冒险.place_forget()
        self.大魔王_英雄.place_forget()
        self.大魔王_王者.place_forget()
        self.挑战按钮.place_forget()
        self.当前窗口.place(x=5, y=5)
        self.阵容选择界面 = Lineup()

    # 创建莉莉崽副本处理
    def 创建莉莉崽副本(self):
        self.sync_()

        def off():
            self.当前窗口.destroy()
            self.宿敌系统.place(x=1200, y=10)
            try:
                self.阵容选择界面.LFM.destroy()
                self.阵容选择界面.GFM.destroy()
            except:
                pass

        def 关闭():
            切换场景(Map)

        self.当前窗口 = LabelFrame(self.frame, text='挑战莉莉崽', height=420, width=610, bg='white')
        self.当前窗口.place(x=1366 / 2 - 305, y=70)
        x_add = 50  # 乾，坤，震，巽，坎，离，艮，兑
        self.挑战莉莉崽_普通 = Button(self.当前窗口, text='乾', relief=FLAT, bg='white', command=lambda: self.挑战莉莉崽召唤('乾'))
        self.挑战莉莉崽_普通.place(x=1, y=1)
        self.挑战莉莉崽_冒险 = Button(self.当前窗口, text='坤', relief=FLAT, bg='white', command=lambda: self.挑战莉莉崽召唤('坤'))
        self.挑战莉莉崽_冒险.place(x=1 + x_add * 1, y=1)
        self.挑战莉莉崽_英雄 = Button(self.当前窗口, text='震', relief=FLAT, bg='white', command=lambda: self.挑战莉莉崽召唤('震'))
        self.挑战莉莉崽_英雄.place(x=1 + x_add * 2, y=1)
        self.挑战莉莉崽_王者 = Button(self.当前窗口, text='巽', relief=FLAT, bg='white', command=lambda: self.挑战莉莉崽召唤('巽'))
        self.挑战莉莉崽_王者.place(x=1 + x_add * 3, y=1)
        self.挑战莉莉崽_噩梦 = Button(self.当前窗口, text='坎', relief=FLAT, bg='white', command=lambda: self.挑战莉莉崽召唤('坎'))
        self.挑战莉莉崽_噩梦.place(x=1 + x_add * 4, y=1)
        self.挑战莉莉崽_挑战 = Button(self.当前窗口, text='离', relief=FLAT, bg='white', command=lambda: self.挑战莉莉崽召唤('离'))
        self.挑战莉莉崽_挑战.place(x=1 + x_add * 5, y=1)
        self.挑战莉莉崽_1 = Button(self.当前窗口, text='艮', relief=FLAT, bg='white', command=lambda: self.挑战莉莉崽召唤('艮'))
        self.挑战莉莉崽_1.place(x=1 + x_add * 6, y=1)
        self.挑战莉莉崽_2 = Button(self.当前窗口, text='兑', relief=FLAT, bg='white', command=lambda: self.挑战莉莉崽召唤('兑'))
        self.挑战莉莉崽_2.place(x=1 + x_add * 7, y=1)
        self.挑战莉莉崽_3 = Button(self.当前窗口, text='破', relief=FLAT, bg='white', command=lambda: self.挑战莉莉崽召唤('破'))

        if r_manage.LL_plan == 8:
            self.挑战莉莉崽_3.place(x=1 + x_add * 8, y=1)

        self.玩法介绍文本 = Label(self.当前窗口, text='*刷新费用：8000 铜 和 12 金\n*获得奖励：大量经验、铜币、黄金、勾玉\n'
                                            f'特殊难度进度:{r_manage.LL_plan}/8'
                            , bg='white', justify=LEFT).place(x=35, y=250)
        self.关闭 = Button(self.当前窗口, text='关闭', relief=FLAT, bg='white', command=关闭).place(x=550, y=1)

        self.开始斗法 = Button(self.当前窗口, image=self.start_b_l, relief=FLAT, bg='white', fg='red', command=self.开始战斗)
        # self.开始斗法.config(statr=DISABLED) # 关闭该按钮
        x = 30
        y = 100
        self.开始斗法.place(x=x + 440, y=y + 120)

        self.挑战莉莉崽召唤('乾', 标识=True)

    def 挑战莉莉崽召唤(self, 难度, 标识=None):

        # 标识 用来判断和处理刷新阵容扣费
        if 标识 == None:
            DE.Player_Mian.金 = DE.Player_Mian.金 - 12
            DE.Player_Mian.铜 = DE.Player_Mian.铜 - 8000

        try:
            self.大魔王_FM.destroy()
        except:
            pass

        def 随机生成APC(GLv=40, ELv=20):
            G = DE.Genshin(DE.Y元神列表[random.randint(0, len(DE.Y元神列表)) - 1])
            # G = DE.Genshin(DE.Y元神列表[6])
            ABC = DE.Z装备列表[random.randint(0, len(DE.Z装备列表)) - 1]
            ABC.append('传承')
            G.装备 = DE.Equipment(ABC)
            G.装备.强化等级 = ELv
            G.装备.装备强化()
            G.Lv = GLv
            G.初始化基础属性()
            G.初始化战斗属性()
            # print(G.name, G.HP,
            # G.物理攻击, G.法术攻击, G.命中, G.闪避, G.伤害类型, G.装备.name)
            return G

        def 生成莉莉崽(难度):

            xulie = 67  # 序列 莉莉崽在卡池中的序列

            if 难度 == '普通':
                G = DE.Genshin(DE.Y元神列表[xulie])  # 68 为莉莉崽在元神池中的序号
                ABC = DE.Z装备列表[random.randint(0, len(DE.Z装备列表)) - 1]
                ABC.append('传承')
                G.装备 = DE.Equipment(ABC)
                G.装备.强化等级 = 3
                G.装备.装备强化()
                G.Lv = 10
                G.初始化基础属性()
                G.初始化战斗属性()
            elif 难度 == '冒险':
                G = DE.Genshin(DE.Y元神列表[xulie])  # 68 为莉莉崽在元神池中的序号
                ABC = DE.Z装备列表[random.randint(0, len(DE.Z装备列表)) - 1]
                ABC.append('传承')
                G.装备 = DE.Equipment(ABC)
                G.装备.强化等级 = 5
                G.装备.装备强化()
                G.Lv = 20
                G.初始化基础属性()
                G.初始化战斗属性()
            elif 难度 == '英雄':
                G = DE.Genshin(DE.Y元神列表[xulie])  # 68 为莉莉崽在元神池中的序号
                ABC = DE.Z装备列表[random.randint(0, len(DE.Z装备列表)) - 1]
                ABC.append('传承')
                G.装备 = DE.Equipment(ABC)
                G.装备.强化等级 = 10
                G.装备.装备强化()
                G.Lv = 30
                G.初始化基础属性()
                G.初始化战斗属性()
            elif 难度 == '王者':
                G = DE.Genshin(DE.Y元神列表[xulie])  # 68 为莉莉崽在元神池中的序号
                ABC = DE.Z装备列表[random.randint(0, len(DE.Z装备列表)) - 1]
                ABC.append('传承')
                G.装备 = DE.Equipment(ABC)
                G.装备.强化等级 = 20
                G.装备.装备强化()
                G.Lv = 40
                G.初始化基础属性()
                G.初始化战斗属性()
            elif 难度 == '噩梦':
                G = DE.Genshin(DE.Y元神列表[xulie])  # 68 为莉莉崽在元神池中的序号
                ABC = DE.Z装备列表[random.randint(0, len(DE.Z装备列表)) - 1]
                ABC.append('传承')
                G.装备 = DE.Equipment(ABC)
                G.装备.强化等级 = 20
                G.装备.装备强化()
                G.Lv = 45
                G.初始化基础属性()
                G.初始化战斗属性()
            else:
                G = DE.Genshin(DE.Y元神列表[xulie])  # 68 为莉莉崽在元神池中的序号
                ABC = DE.Z装备列表[random.randint(0, len(DE.Z装备列表)) - 1]
                ABC.append('传承')
                G.装备 = DE.Equipment(ABC)
                G.装备.强化等级 = 99
                G.装备.装备强化()
                G.Lv = 99
                G.初始化基础属性()
                G.初始化战斗属性()

            return G

        DE.阵容数量 = 5  # 用来控制该模式允许上阵的最大卡牌数
        # 创建APC
        # 乾，坤，震，巽，坎，离，艮，兑
        if 难度 == '乾':
            r_manage.set_ID(['LL', 1])
            LLZ = 生成莉莉崽('普通')
            LLZ.HP = LLZ.HP * 10
            LLZ.闪避 = 1600
            LLZ.命中 = 1300

            G1 = 随机生成APC(GLv=10, ELv=3)
            G1.HP = G1.HP * 5
            G1.命中 = 1200
            G1.闪避 = 1000

            G2 = 随机生成APC(GLv=10, ELv=3)
            G2.HP = G2.HP * 5
            G2.命中 = 1200
            G2.闪避 = 1000

            DE.敌人阵容 = [LLZ, G1, G2]

            reward.init_Magnification = 200

        elif 难度 == '坤':
            r_manage.set_ID(['LL', 2])
            LLZ = 生成莉莉崽('冒险')
            LLZ.HP = LLZ.HP * 15
            LLZ.闪避 = 2000
            LLZ.命中 = 1800

            G1 = 随机生成APC(GLv=20, ELv=10)
            G1.HP = G1.HP * 8
            G1.命中 = 1500
            G1.闪避 = 1600

            G2 = 随机生成APC(GLv=20, ELv=10)
            G2.HP = G2.HP * 8
            G2.命中 = 1500
            G2.闪避 = 1800

            DE.敌人阵容 = [LLZ, G1, G2]

            reward.init_Magnification = 300

        elif 难度 == '震':
            r_manage.set_ID(['LL', 3])
            LLZ = 生成莉莉崽('英雄')
            LLZ.HP = LLZ.HP * 20
            LLZ.闪避 = 2500
            LLZ.命中 = 2230

            G1 = 随机生成APC(GLv=30, ELv=18)
            G1.HP = G1.HP * 15
            G1.命中 = 3000
            G1.闪避 = 1000

            G2 = 随机生成APC(GLv=30, ELv=18)
            G2.HP = G2.HP * 15
            G2.命中 = 1000
            G2.闪避 = 3000

            DE.敌人阵容 = [LLZ, G1, G2]

            reward.init_Magnification = 400

        elif 难度 == '巽':
            r_manage.set_ID(['LL', 4])
            LLZ = 生成莉莉崽('王者')
            LLZ.HP = LLZ.HP * 25
            LLZ.闪避 = 3000
            LLZ.命中 = 2800

            G1 = 随机生成APC(GLv=40, ELv=20)
            G1.HP = G1.HP * 6
            G1.命中 = 1800
            G1.闪避 = 7000

            G2 = 随机生成APC(GLv=40, ELv=20)
            G2.HP = G2.HP * 100
            G2.命中 = 100
            G2.闪避 = 2000

            DE.敌人阵容 = [LLZ, G1, G2]
            reward.init_Magnification = 1000

        elif 难度 == '坎':
            r_manage.set_ID(['LL', 5])
            LLZ = 生成莉莉崽('噩梦')
            LLZ.HP = LLZ.HP * 30
            LLZ.闪避 = 4000
            LLZ.命中 = 3000

            G1 = 随机生成APC(GLv=40, ELv=20)
            G1.HP = G1.HP * 20
            G1.命中 = 3000
            G1.闪避 = 2500

            G2 = 随机生成APC(GLv=40, ELv=20)
            G2.HP = G2.HP * 25
            G2.命中 = 1299
            G2.闪避 = 3600

            DE.敌人阵容 = [LLZ, G1, G2]
            reward.init_Magnification = 1500

        elif 难度 == '离':
            r_manage.set_ID(['LL', 6])
            LLZ = 生成莉莉崽('噩梦')
            LLZ.HP = LLZ.HP * 30
            LLZ.闪避 = 4100
            LLZ.命中 = 3100

            G1 = 随机生成APC(GLv=40, ELv=20)
            G1.HP = G1.HP * 88
            G1.命中 = 1000
            G1.闪避 = 1000

            G2 = 随机生成APC(GLv=40, ELv=20)
            G2.HP = G2.HP * 15
            G2.命中 = 1299
            G2.闪避 = 7200

            G3 = 随机生成APC(GLv=40, ELv=30)
            G3.HP = G3.HP * 35
            G3.命中 = 1000
            G3.闪避 = 1456

            G4 = 随机生成APC(GLv=40, ELv=30)
            G4.HP = G4.HP * 35
            G4.命中 = 2699
            G4.闪避 = 2500

            DE.敌人阵容 = [LLZ, G1, G2, G3, G4]
            reward.init_Magnification = 1600

        elif 难度 == '艮':
            r_manage.set_ID(['LL', 7])
            LLZ = 生成莉莉崽('噩梦')
            LLZ.HP = LLZ.HP * 40
            LLZ.闪避 = 2600
            LLZ.命中 = 3300

            G1 = 随机生成APC(GLv=40, ELv=20)
            G1.HP = G1.HP * 100
            G1.命中 = 1000
            G1.闪避 = 2000

            G2 = 随机生成APC(GLv=40, ELv=20)
            G2.HP = G2.HP * 20
            G2.命中 = 800
            G2.闪避 = 7200

            G3 = 随机生成APC(GLv=40, ELv=30)
            G3.HP = G3.HP * 5
            G3.命中 = 4000
            G3.闪避 = 1456

            G4 = 随机生成APC(GLv=40, ELv=30)
            G4.HP = G4.HP * 40
            G4.命中 = 2699
            G4.闪避 = 2500

            DE.敌人阵容 = [LLZ, G1, G2, G3, G4]
            reward.init_Magnification = 1800

        elif 难度 == '兑':
            r_manage.set_ID(['LL', 8])
            LLZ = 生成莉莉崽('噩梦')
            LLZ.HP = LLZ.HP * 40
            LLZ.闪避 = 3000
            LLZ.命中 = 3300

            G1 = 生成莉莉崽('噩梦')
            G1.HP = G1.HP * 40
            G1.命中 = 3300
            G1.闪避 = 3000

            G2 = 生成莉莉崽('噩梦')
            G2.HP = G2.HP * 20
            G2.命中 = 800
            G2.闪避 = 9999

            G3 = 随机生成APC(GLv=40, ELv=30)
            G3.HP = G3.HP * 5
            G3.命中 = 4000
            G3.闪避 = 1456

            G4 = 随机生成APC(GLv=40, ELv=30)
            G4.HP = G4.HP * 10
            G4.命中 = 5000
            G4.闪避 = 100

            DE.敌人阵容 = [LLZ, G1, G2, G3, G4]
            reward.init_Magnification = 2000

        reward.sets(Config_Config.get('R2'))

        if 难度 == '破':
            r_manage.set_ID(['LL', 000])
            LLZ = 生成莉莉崽('噩梦')
            LLZ.HP = LLZ.HP * 80
            LLZ.闪避 = 7888
            # LLZ.命中 = 1000

            G3 = 随机生成APC(GLv=40, ELv=30)
            G3.HP = G3.HP * 3
            G3.命中 = 4000
            G3.闪避 = 8888

            G4 = 随机生成APC(GLv=40, ELv=30)
            G4.HP = G4.HP * 3
            G4.命中 = 5000
            G4.闪避 = 8888

            DE.敌人阵容 = [LLZ, G3, G4]
            reward.init_Magnification = 1000
            reward.sets(Config_Config.get('R4'))

        x = 30
        y = 100

        self.当前阵容显示文本 = Label(self.当前窗口, text='当前阵容：', bg='white').place(x=x, y=80)

        try:
            for but in self.莉莉崽阵容_ICO:  # 关闭全部头像
                but.destroy()
        except:
            pass

        self.莉莉崽阵容_ICO = []
        # print('莉莉崽 阵容', DE.敌人阵容)

        for i in DE.敌人阵容:
            # print(i.__dict__)
            self.But = Genshin_But_莉莉崽(self.当前窗口, i, x, y)
            self.莉莉崽阵容_ICO.append(self.But)
            x += 110

    # 创建训练场
    def 创建训练场副本(self):
        self.sync_()

        def off():
            self.当前窗口.destroy()
            self.宿敌系统.place(x=1200, y=10)
            try:
                self.阵容选择界面.LFM.destroy()
                self.阵容选择界面.GFM.destroy()
            except:
                pass

        def 关闭():
            切换场景(Map)

        self.当前窗口 = LabelFrame(self.frame, text='训练场', height=420, width=610, bg='white')
        self.当前窗口.place(x=1366 / 2 - 305, y=70)

        self.训练场_普通 = Button(self.当前窗口, text='普通', relief=FLAT, bg='white', command=lambda: self.训练场APC召唤('普通'))
        self.训练场_普通.place(x=1, y=1)
        self.训练场_冒险 = Button(self.当前窗口, text='冒险', relief=FLAT, bg='white', command=lambda: self.训练场APC召唤('冒险'))
        self.训练场_冒险.place(x=100, y=1)
        self.训练场_英雄 = Button(self.当前窗口, text='英雄', relief=FLAT, bg='white', command=lambda: self.训练场APC召唤('英雄'))
        self.训练场_英雄.place(x=200, y=1)
        self.训练场_王者 = Button(self.当前窗口, text='王者', relief=FLAT, bg='white', command=lambda: self.训练场APC召唤('王者'))
        self.训练场_王者.place(x=300, y=1)
        self.训练场_噩梦 = Button(self.当前窗口, text='噩梦', relief=FLAT, bg='white', command=lambda: self.训练场APC召唤('噩梦'))
        self.训练场_噩梦.place(x=400, y=1)

        self.玩法介绍文本 = Label(self.当前窗口, text='*玩法：伤害测试\n*刷新费用：100 铜\n*获得奖励：经验、铜币'
                            , bg='white', justify=LEFT).place(x=35, y=250)

        self.关闭 = Button(self.当前窗口, text='关闭', relief=FLAT, bg='white', command=关闭).place(x=550, y=1)

        self.训练场APC召唤('普通')
        DE.Player_Mian.铜 = DE.Player_Mian.铜 + 100

    def 训练场APC召唤(self, 难度):

        DE.Player_Mian.铜 = DE.Player_Mian.铜 - 100
        r_manage.set_ID([None])

        try:
            self.大魔王_FM.destroy()
        except:
            pass

        def 随机生成APC(GLv=40, ELv=20):
            G = DE.Genshin(DE.Y元神列表[random.randint(0, len(DE.Y元神列表)) - 1])
            # G = DE.Genshin(DE.Y元神列表[6])
            ABC = DE.Z装备列表[random.randint(0, len(DE.Z装备列表)) - 1]
            ABC.append('传承')
            G.装备 = DE.Equipment(ABC)
            G.装备.强化等级 = ELv
            G.装备.装备强化()
            G.Lv = GLv
            G.初始化基础属性()
            G.初始化战斗属性()
            # print(G.name, G.HP,
            # G.物理攻击, G.法术攻击, G.命中, G.闪避, G.伤害类型, G.装备.name)
            return G

        DE.阵容数量 = 5  # 用来控制该模式允许上阵的最大卡牌数
        if 难度 == '普通':
            G = 随机生成APC(GLv=20, ELv=3)
            G.HP = 10000000
            G.命中 = 10
            G.闪避 = 500
            DE.敌人阵容 = [G]
            reward.init_Magnification = 200
        elif 难度 == '冒险':
            G = 随机生成APC(GLv=40, ELv=10)
            G.HP = 10000000
            G.命中 = 10
            G.闪避 = 1000
            DE.敌人阵容 = [G]
            reward.init_Magnification = 300
        elif 难度 == '英雄':
            G = 随机生成APC(GLv=40, ELv=20)
            G.HP = 10000000
            G.命中 = 10
            G.闪避 = 2000
            DE.敌人阵容 = [G]
            reward.init_Magnification = 400
        elif 难度 == '王者':
            G = 随机生成APC(GLv=45, ELv=20)
            G.HP = 10000000
            G.命中 = 10
            G.闪避 = 3000
            DE.敌人阵容 = [G]
            reward.init_Magnification = 500
        elif 难度 == '噩梦':
            G = 随机生成APC(GLv=45, ELv=20)
            G.HP = 10000000
            G.命中 = 10
            G.闪避 = 4000
            DE.敌人阵容 = [G]
            reward.init_Magnification = 800

        reward.sets(Config_Config.get('R3'))  # 设置奖励格式

        self.大魔王_FM = LabelFrame(self.当前窗口, text=G.name + '  *  ' + G.ID + '*' + G.等级, height=365,
                                 width=604, bg='white', )
        # bg='white' 白色背景
        self.大魔王_FM.place(x=0, y=33)
        # self.宿敌_FM.config(bg='red')
        # 立绘
        self.LH_P = Open_Jpg(os.path.join('Resource', 'picture', 'Genshin', f'{G.Code}-x.jpg'))  # 元神小立绘
        self.LH = Label(self.大魔王_FM, image=self.LH_P)
        self.LH.place(x=5, y=0)
        # 装备图标
        if G.装备 == None:
            self.ZBLH_P = Open_Jpg(os.path.join('Resource', 'picture', 'Equipment', f'O.jpg'))
        else:
            self.ZBLH_P = Open_Jpg(os.path.join('Resource', 'picture', 'Equipment', f'{G.装备.Code}.jpg'))
            if G.装备.强化等级 != 0:
                self.ENAMEL = Label(self.大魔王_FM, text='+' + str(G.装备.强化等级) + G.装备.name + '-' + G.装备.ID,
                                    bg='white', fg=DE.装备字体颜色.get(G.装备.品级)).place(x=220, y=185)
            else:
                self.ENAMEL = Label(self.大魔王_FM, text=G.装备.name + '-' + G.装备.ID,
                                    bg='white', fg=DE.装备字体颜色.get(G.装备.品级)).place(x=220, y=185)
            self.ELL = Label(self.大魔王_FM, text='力量+' + str(G.装备.力量), bg='white').place(x=220, y=205)
            self.EZH = Label(self.大魔王_FM, text='智慧+' + str(G.装备.智慧), bg='white').place(x=310, y=205)
            self.ETL = Label(self.大魔王_FM, text='体力+' + str(G.装备.体力), bg='white').place(x=220, y=225)
            self.EMJ = Label(self.大魔王_FM, text='敏捷+' + str(G.装备.敏捷), bg='white').place(x=310, y=225)

            self.ELLZ = Label(self.大魔王_FM, text='力量强化+' + str(G.装备.力量资质), bg='white').place(x=220, y=245)
            self.EZZH = Label(self.大魔王_FM, text='智慧强化+' + str(G.装备.智慧资质), bg='white').place(x=220, y=265)
            self.ETLZ = Label(self.大魔王_FM, text='体力强化+' + str(G.装备.体力资质), bg='white').place(x=220, y=285)
            self.ETLZ = Label(self.大魔王_FM, text='敏捷强化+' + str(G.装备.敏捷资质), bg='white').place(x=220, y=305)
            self.ETLZ = Label(self.大魔王_FM, text='成色；' + str(G.装备.完美程度), bg='white').place(x=310, y=305)
        self.ZBLH = Label(self.大魔王_FM, image=self.ZBLH_P, relief=FLAT)
        self.ZBLH.place(x=215, y=3)
        # 属性
        self.属性词条 = []  # 该变量未使用
        x = 385
        self.昵称 = Label(self.大魔王_FM, text=G.name, font=('Aridl', 13), bg='white').place(x=x, y=0)

        self.S_LV = StringVar()
        self.S_LV.set('Lv: ' + str(G.Lv))
        self.Lv = Label(self.大魔王_FM, textvariable=self.S_LV, bg='white').place(x=x, y=25)

        self.S_伤害类型 = StringVar()
        try:
            self.S_伤害类型.set('伤害类型：' + G.伤害类型)
        except:
            self.S_伤害类型.set('无')
        self.伤害类型 = Label(self.大魔王_FM, textvariable=self.S_伤害类型, bg='white').place(x=x + 100, y=25)

        self.S_HP = StringVar()
        self.S_HP.set('HP: ' + str(G.HP))
        self.HP = Label(self.大魔王_FM, textvariable=self.S_HP, bg='white').place(x=x, y=45)
        # 基础属性
        self.S_力量 = StringVar()
        self.S_力量.set('力量: ' + str(G.力量) + '    ')
        self.力量 = Label(self.大魔王_FM, textvariable=self.S_力量, bg='white').place(x=x, y=65)

        self.S_智慧 = StringVar()
        self.S_智慧.set('智慧: ' + str(G.智慧))
        self.智慧 = Label(self.大魔王_FM, textvariable=self.S_智慧, bg='white').place(x=x + 100, y=65)

        self.S_体力 = StringVar()
        self.S_体力.set('体力: ' + str(G.体力))
        self.体力 = Label(self.大魔王_FM, textvariable=self.S_体力, bg='white').place(x=x, y=85)

        self.S_敏捷 = StringVar()
        self.S_敏捷.set('敏捷: ' + str(G.敏捷))
        self.敏捷 = Label(self.大魔王_FM, textvariable=self.S_敏捷, bg='white').place(x=x + 100, y=85)

        # 属性资质
        self.S_力量资质 = StringVar()
        self.S_力量资质.set('力量资质: ' + str(G.力量资质))
        self.力量资质 = Label(self.大魔王_FM, textvariable=self.S_力量资质, bg='white').place(x=x, y=125)

        self.S_智慧资质 = StringVar()
        self.S_智慧资质.set('' + '智慧资质: ' + str(G.智慧资质))
        self.智慧资质 = Label(self.大魔王_FM, textvariable=self.S_智慧资质, bg='white').place(x=x + 100, y=125)

        self.S_体力资质 = StringVar()
        self.S_体力资质.set('体力资质: ' + str(G.体力资质))
        self.体力资质 = Label(self.大魔王_FM, textvariable=self.S_体力资质, bg='white').place(x=x, y=105)

        self.S_敏捷资质 = StringVar()
        self.S_敏捷资质.set('敏捷资质: ' + str(G.敏捷资质))
        self.敏捷资质 = Label(self.大魔王_FM, textvariable=self.S_敏捷资质, bg='white').place(x=x + 100, y=105)

        # 后天属性
        self.S_后天属性 = StringVar()
        self.S_后天属性.set('后天属性：' + G.后天属性)
        self.后天属性 = Label(self.大魔王_FM, textvariable=self.S_后天属性, bg='white').place(x=x, y=145)

        # 战斗属性
        self.S_物理攻击 = StringVar()
        self.S_物理攻击.set('物理攻击: ' + str(G.物理攻击))
        self.物理攻击 = Label(self.大魔王_FM, textvariable=self.S_物理攻击, bg='white').place(x=x, y=165)

        self.S_法术攻击 = StringVar()
        self.S_法术攻击.set('法术攻击: ' + str(G.法术攻击))
        self.法术攻击 = Label(self.大魔王_FM, textvariable=self.S_法术攻击, bg='white').place(x=x, y=185)

        self.S_命中 = StringVar()
        self.S_命中.set('命中: ' + str(G.命中))
        self.命中 = Label(self.大魔王_FM, textvariable=self.S_命中, bg='white').place(x=x, y=205)

        self.S_闪避 = StringVar()
        self.S_闪避.set('闪避: ' + str(G.闪避))
        self.闪避 = Label(self.大魔王_FM, textvariable=self.S_闪避, bg='white').place(x=x + 100, y=205)
        self.挑战按钮 = Button(self.大魔王_FM, image=self.start_b_l, relief=FLAT, bg='white', fg='red', command=self.开始训练场)
        self.挑战按钮.place(x=x, y=250)

    def 开始训练场(self):
        self.训练场_普通.place_forget()
        self.训练场_冒险.place_forget()
        self.训练场_英雄.place_forget()
        self.训练场_王者.place_forget()
        self.训练场_噩梦.place_forget()
        self.挑战按钮.place_forget()
        self.当前窗口.place(x=5, y=5)
        self.阵容选择界面 = Lineup()

    def 创建花朝节副本(self):
        self.sync_()

        def 关闭():
            切换场景(Map)

        self.当前窗口 = LabelFrame(self.frame, text='花朝节', height=420, width=610, bg='white')
        self.当前窗口.place(x=1366 / 2 - 305, y=70)
        x_add = 45

        self.花朝节_1 = Button(self.当前窗口, text='梅', relief=FLAT, bg='white', command=lambda: self.花朝节召唤('梅'))
        self.花朝节_1.place(x=1, y=1)
        self.花朝节_2 = Button(self.当前窗口, text='杏', relief=FLAT, bg='white', command=lambda: self.花朝节召唤('杏'))
        self.花朝节_2.place(x=1 + x_add * 1, y=1)
        self.花朝节_3 = Button(self.当前窗口, text='桃', relief=FLAT, bg='white', command=lambda: self.花朝节召唤('桃'))
        self.花朝节_3.place(x=1 + x_add * 2, y=1)
        self.花朝节_4 = Button(self.当前窗口, text='牡丹', relief=FLAT, bg='white', command=lambda: self.花朝节召唤('牡丹'))
        self.花朝节_4.place(x=1 + x_add * 3, y=1)
        self.花朝节_5 = Button(self.当前窗口, text='石榴', relief=FLAT, bg='white', command=lambda: self.花朝节召唤('石榴'))
        self.花朝节_5.place(x=1 + x_add * 4, y=1)
        self.花朝节_6 = Button(self.当前窗口, text='莲', relief=FLAT, bg='white', command=lambda: self.花朝节召唤('莲'))
        self.花朝节_6.place(x=1 + x_add * 5, y=1)
        self.花朝节_7 = Button(self.当前窗口, text='玉簪', relief=FLAT, bg='white', command=lambda: self.花朝节召唤('玉簪'))
        self.花朝节_7.place(x=1 + x_add * 6, y=1)
        self.花朝节_8 = Button(self.当前窗口, text='桂', relief=FLAT, bg='white', command=lambda: self.花朝节召唤('桂'))
        self.花朝节_8.place(x=1 + x_add * 7, y=1)
        self.花朝节_9 = Button(self.当前窗口, text='菊', relief=FLAT, bg='white', command=lambda: self.花朝节召唤('菊'))
        self.花朝节_9.place(x=1 + x_add * 8, y=1)
        self.花朝节_10 = Button(self.当前窗口, text='茶', relief=FLAT, bg='white', command=lambda: self.花朝节召唤('茶'))
        self.花朝节_10.place(x=1 + x_add * 9, y=1)
        self.花朝节_11 = Button(self.当前窗口, text='芙蓉', relief=FLAT, bg='white', command=lambda: self.花朝节召唤('芙蓉'))
        self.花朝节_11.place(x=1 + x_add * 10, y=1)
        self.花朝节_12 = Button(self.当前窗口, text='水仙', relief=FLAT, bg='white', command=lambda: self.花朝节召唤('水仙'))
        self.花朝节_12.place(x=1 + x_add * 11, y=1)

        self.玩法介绍文本 = Label(self.当前窗口, text='*刷新费用：200000 铜 和 50 金\n*获得奖励：大量经验、勾玉\n'
                            , bg='white', justify=LEFT).place(x=35, y=250)
        self.关闭 = Button(self.当前窗口, text='关闭', relief=FLAT, bg='white', command=关闭).place(x=560, y=1)

        self.开始斗法 = Button(self.当前窗口, image=self.start_b_l, relief=FLAT, bg='white', fg='red', command=self.开始战斗)
        # self.开始斗法.config(statr=DISABLED) # 关闭该按钮
        x = 30
        y = 100
        self.开始斗法.place(x=x + 440, y=y + 120)

    def 花朝节召唤(self, data):

        print(data)

        DE.Player_Mian.铜 = DE.Player_Mian.铜 - 200000
        DE.Player_Mian.金 = DE.Player_Mian.金 - 50

        reward.init_Magnification = 100

        def 生成APC(GLv=40, ELv=20, Code=0):

            G = DE.Genshin(DE.Y元神列表[Code - 2])
            # G = DE.Genshin(DE.Y元神列表[6])
            ABC = DE.Z装备列表[random.randint(0, len(DE.Z装备列表)) - 1]
            ABC.append('传承')
            G.装备 = DE.Equipment(ABC)
            G.装备.强化等级 = ELv
            G.装备.装备强化()
            G.Lv = GLv
            G.初始化基础属性()
            G.初始化战斗属性()
            # print(G.name, G.HP,
            # G.物理攻击, G.法术攻击, G.命中, G.闪避, G.伤害类型, G.装备.name)
            return G

        DE.敌人阵容 = []

        reward.sets({'Y': 50, 'G': 50, 'T': 0, 'Exp': 0})

        # 开始花朝节构建敌人阵容
        if data == '梅':  # 判断
            reward.init_Magnification = 100
            for n in [10, 44, 70]:
                G = 生成APC(GLv=60, ELv=25, Code=n)
                G.HP = G.HP * 2
                DE.敌人阵容.append(G)

        elif data == '杏':
            reward.init_Magnification = 100
            for n in [73, 19, 58]:
                G = 生成APC(GLv=40, ELv=20, Code=n)
                G.HP = G.HP * 5
                G.命中 = 3000 + random.randint(-100, 100)
                G.物理攻击 = 38000 + random.randint(-100, 100)
                G.伤害类型 = '物理'
                DE.敌人阵容.append(G)

        elif data == '桃':
            reward.init_Magnification = 200
            for n in [64, 41, 39]:
                G = 生成APC(GLv=40, ELv=20, Code=n)
                G.HP = G.HP * 5
                G.命中 = 4000 + random.randint(-100, 100)
                G.法术攻击 = 35000 + random.randint(-100, 100)
                G.伤害类型 = '法术'
                DE.敌人阵容.append(G)

        elif data == '牡丹':
            reward.init_Magnification = 150
            for n in [47, 12, 24]:
                G = 生成APC(GLv=40, ELv=20, Code=n)
                G.HP = G.HP * 5
                G.命中 = 4000 + random.randint(-100, 100)
                G.法术攻击 = 35000 + random.randint(-100, 100)
                G.伤害类型 = '法术穿透'
                DE.敌人阵容.append(G)

        elif data == '石榴':
            reward.init_Magnification = 300
            for n in [5, 63, 6, 13, 4]:
                G = 生成APC(GLv=40, ELv=20, Code=n)
                G.HP = 40000 + random.randint(40000, 80000)
                G.命中 = 1000 + random.randint(100, 650)
                G.闪避 = 3000
                G.法术攻击 = 35000
                G.伤害类型 = '血怒'
                DE.敌人阵容.append(G)

        elif data == '莲':
            reward.init_Magnification = 150
            for n in [45, 8, 30]:
                G = 生成APC(GLv=45, ELv=20, Code=n)
                G.HP = G.HP * 5
                G.命中 = 7000 + random.randint(-100, 100)
                G.物理攻击 = 10000 + random.randint(-100, 6000)
                DE.敌人阵容.append(G)

        elif data == '玉簪':
            reward.init_Magnification = 300
            for n in [15, 36, 67, 58, 72]:
                G = 生成APC(GLv=45, ELv=20, Code=n)
                G.HP = G.HP * 20
                DE.敌人阵容.append(G)

        elif data == '桂':
            reward.init_Magnification = 300
            for n in [28]:
                G = 生成APC(GLv=45, ELv=20, Code=n)
                G.HP = G.HP * 20
                G.命中 = 8000 + random.randint(-10, 150)
                DE.敌人阵容.append(G)

        elif data == '菊':
            reward.init_Magnification = 300
            for n in [10, 44, 70]:
                G = 生成APC(GLv=45, ELv=20, Code=n)
                G.HP = G.HP * 100
                G.闪避 = 1000 + random.randint(-200, 150)
                DE.敌人阵容.append(G)

        elif data == '茶':
            reward.init_Magnification = 400
            for n in [46, 33, 35]:
                G = 生成APC(GLv=45, ELv=20, Code=n)
                G.HP = G.HP * 12
                G.闪避 = 9999 + random.randint(-200, 150)
                DE.敌人阵容.append(G)

        elif data == '芙蓉':
            reward.init_Magnification = 600
            for n in [69, 13, 66, 72, 32]:
                G = 生成APC(GLv=80, ELv=5, Code=n)
                G.HP = G.HP
                DE.敌人阵容.append(G)

        elif data == '水仙':
            reward.init_Magnification = 400
            for n in [71, 46, 61, 63, 38]:
                G = 生成APC(GLv=45, ELv=40, Code=n)
                G.HP = G.HP * 3
                DE.敌人阵容.append(G)

        x = 30
        y = 100

        self.当前阵容显示文本 = Label(self.当前窗口, text='当前阵容：', bg='white').place(x=x, y=80)

        try:
            for but in self.花朝节阵容_ICO:  # 关闭全部头像
                but.destroy()
        except:
            pass
        self.花朝节阵容_ICO = []

        # print('莉莉崽 阵容', DE.敌人阵容)

        for i in DE.敌人阵容:
            # print(i.__dict__)
            self.But = Genshin_But_莉莉崽(self.当前窗口, i, x, y)
            self.花朝节阵容_ICO.append(self.But)
            x += 110

    def run(self):
        self.frame.place(x=0, y=0)

    def off(self):
        self.frame.place_forget()

    def sync_(self):
        # 用于关闭上一个副本选择页面
        try:
            self.当前窗口.destroy()
        except:
            pass


# 用于元神召唤和装备抽奖的视图
class Call():  # 抽卡视图

    def __init__(self, root):
        n = 1
        for i in DE.Y元神列表:
            n += 1

        self.name = '拜月祠堂'
        # self.L_image_open = Image.open(os.path.join('Resource','picture',f'BG.png')
        # self.L_image = ImageTk.PhotoImage(self.L_image_open)
        self.L_image = Open_Jpg(os.path.join('Resource', 'picture', 'BIG', f'BYCT.jpg'))
        self.frame = Frame(root, height=768, width=1366)
        self.L = Label(self.frame, image=self.L_image)
        self.L.place(x=0, y=0)
        self.frame.place(x=0, y=0)
        self.召唤元神_P = Open_Jpg(os.path.join('Resource', 'picture', 'ui', f'CALL_YS.jpg'))
        self.召唤元神 = Button(self.frame, image=self.召唤元神_P, command=self.抽卡元神)
        self.召唤元神.place(x=59, y=514)

        self.召唤装备1_P = Open_Jpg(os.path.join('Resource', 'picture', 'ui', f'CALL_ZB1.jpg'))
        self.召唤装备1 = Button(self.frame, image=self.召唤装备1_P, command=self.抽装备)
        self.召唤装备1.place(x=203, y=514)

        self.召唤装备2_P = Open_Jpg(os.path.join('Resource', 'picture', 'ui', f'CALL_ZB2.jpg'))
        self.召唤装备2 = Button(self.frame, image=self.召唤装备2_P, command=self.高级抽装备)
        self.召唤装备2.place(x=347, y=514)

        self.符文礼包_P = Open_Jpg(os.path.join('Resource', 'picture', 'ui', f'CALL_FW11.jpg'))
        self.符文礼包按钮 = Button(self.frame, image=self.符文礼包_P, command=self.符文礼包)
        self.符文礼包按钮.place(x=491, y=514)

        self.符文大满贯_P = Open_Jpg(os.path.join('Resource', 'picture', 'ui', f'CALL_FW99.jpg'))
        self.符文大满贯按钮 = Button(self.frame, image=self.符文大满贯_P, command=self.符文大满贯)
        self.符文大满贯按钮.place(x=635, y=514)

        '''在该界面UI上显示资源'''
        self.资源UIX = 59
        self.资源UIY = 728

        self.召唤符FM = Frame(self.frame, bg='black', height=40, width=250)
        self.召唤符P_P = Open_Jpg(os.path.join('Resource', 'picture', 'ui', f'P_UI_FW.jpg'))
        self.召唤符_P = Label(self.召唤符FM, image=self.召唤符P_P, relief='solid')
        self.召唤符_P.place(x=0, y=0)
        self.召唤符S = StringVar()
        self.召唤符S.set(str(DE.Player_Mian.召唤符))
        self.召唤符L = Label(self.召唤符FM, textvariable=self.召唤符S, font=DE.资源font, fg='SkyBlue', bg='black').place(x=120,
                                                                                                              y=0)
        self.召唤符FM.place(x=self.资源UIX + 1000, y=self.资源UIY)

        self.勾玉FM = Frame(self.frame, bg='black', height=40, width=250)
        self.勾玉P_P = Open_Jpg(os.path.join('Resource', 'picture', 'ui', f'P_UI_Y.jpg'))
        self.勾玉_P = Label(self.勾玉FM, image=self.勾玉P_P, relief='solid')
        self.勾玉_P.place(x=0, y=0)
        self.勾玉S = StringVar()
        self.勾玉S.set(str(DE.Player_Mian.玉))
        self.勾玉L = Label(self.勾玉FM, textvariable=self.勾玉S, font=DE.资源font, fg='SkyBlue', bg='black').place(x=120, y=0)
        self.勾玉FM.place(x=self.资源UIX, y=self.资源UIY)

        self.黄金FM = Frame(self.frame, bg='black', height=40, width=250)
        self.黄金P_P = Open_Jpg(os.path.join('Resource', 'picture', 'ui', f'P_UI_G.jpg'))
        self.黄金_P = Label(self.黄金FM, image=self.黄金P_P, relief='solid')
        self.黄金_P.place(x=0, y=0)
        self.黄金S = StringVar()
        self.黄金S.set(str(DE.Player_Mian.金))
        self.黄金L = Label(self.黄金FM, textvariable=self.黄金S, font=DE.资源font, fg='SkyBlue', bg='black').place(x=120, y=0)
        self.黄金FM.place(x=self.资源UIX + 250, y=self.资源UIY)

        self.铜钱FM = Frame(self.frame, bg='black', height=40, width=250)
        self.铜钱P_P = Open_Jpg(os.path.join('Resource', 'picture', 'ui', f'P_UI_T.jpg'))
        self.铜钱_P = Label(self.铜钱FM, image=self.铜钱P_P, relief='solid')
        self.铜钱_P.place(x=0, y=0)
        self.铜钱S = StringVar()
        self.铜钱S.set(str(DE.Player_Mian.铜))
        self.铜钱L = Label(self.铜钱FM, textvariable=self.铜钱S, font=DE.Exp_font, fg='SkyBlue', bg='black').place(x=120, y=8)
        self.铜钱FM.place(x=self.资源UIX + 500, y=self.资源UIY)

        self.ExpFM = Frame(self.frame, bg='black', height=40, width=250)
        self.ExpP_P = Open_Jpg(os.path.join('Resource', 'picture', 'ui', f'P_UI_EXP.jpg'))
        self.Exp_P = Label(self.ExpFM, image=self.ExpP_P, relief='solid')
        self.Exp_P.place(x=0, y=0)
        self.ExpS = StringVar()
        self.ExpS.set(str(DE.Player_Mian.exp))
        self.ExpL = Label(self.ExpFM, textvariable=self.ExpS, font=DE.Exp_font, fg='SkyBlue', bg='black').place(x=120,
                                                                                                                y=8)
        self.ExpFM.place(x=self.资源UIX + 750, y=self.资源UIY)

    def 刷新资源UI(self):
        '''用于刷新UI资源'''
        self.召唤符S.set(str(DE.Player_Mian.召唤符))
        self.勾玉S.set(str(DE.Player_Mian.玉))
        self.黄金S.set(str(DE.Player_Mian.金))
        self.铜钱S.set(str(DE.Player_Mian.铜))
        self.ExpS.set(str(DE.Player_Mian.exp))

    def 抽卡元神(self):
        if DE.Player_Mian.召唤符 != 0:
            DE.Player_Mian.召唤符 = DE.Player_Mian.召唤符 - 1
            print('抽卡成功！')
            self.抽卡成功()
            自动保存()

        elif DE.Player_Mian.玉 >= 100:
            DE.Player_Mian.玉 = DE.Player_Mian.玉 - 100
            self.刷新资源UI()
            # print('抽卡成功！')
            self.抽卡成功()
            自动保存()
        else:
            普通弹窗('抽卡提示', '勾玉或召唤符不足！')

    def 抽装备(self):
        def off():
            self.装备显示容器.destroy()
            切换场景(Call)

        if DE.Player_Mian.铜 >= 30000:
            DE.Player_Mian.铜 = DE.Player_Mian.铜 - 30000
            # print('普通召唤装备！')
            等级 = random.randint(0, 1000)

            ABC = DE.Z装备列表[random.randint(0, len(DE.Z装备列表) - 1)]
            # print('等级',等级)
            if 等级 < 800:
                ABC.append('稀有')
            elif 等级 > 800 and 等级 < 900:
                ABC.append('神器')
            elif 等级 > 900:
                ABC.append('史诗')
            else:
                ABC.append('稀有')

            E = DE.Equipment(ABC)
            try:
                DE.Player_Mian.装备组.append(E)
            except:
                DE.Player_Mian.装备组 = []
                DE.Player_Mian.装备组.append(E)

            自动保存()

            self.装备显示容器 = LabelFrame(self.frame, text=E.name + ' ' + E.ID, height=210, width=300, bg='white')
            self.抽装备关闭按钮 = Button(self.装备显示容器, text='X', command=off, relief=FLAT, bg='white')
            self.抽装备关闭按钮.place(x=275, y=0)
            self.装备图标_P = Open_Jpg(os.path.join('Resource', 'picture', 'Equipment', f'{E.Code}.jpg'))
            self.装备图标 = Label(self.装备显示容器, image=self.装备图标_P)
            self.装备图标.place(x=0, y=0)
            self.装备名称 = Label(self.装备显示容器, text=E.name, font=('Aridl', 11), bg='white', fg=DE.装备字体颜色.get(E.品级)).place(
                x=160, y=0)
            self.装备品级 = Label(self.装备显示容器, text=E.品级, bg='white').place(x=240, y=0)
            self.装备属性 = Label(self.装备显示容器, text=E.获得装备属性(), justify=LEFT, bg='white').place(x=160, y=20)

            self.装备显示容器.place(x=533, y=280)
            print('成功抽取准备！')
            print(E.__dict__)
            self.刷新资源UI()

    def 高级抽装备(self):
        def off():
            self.装备显示容器.destroy()
            切换场景(Call)

        if DE.Player_Mian.金 >= 2000:
            DE.Player_Mian.金 = DE.Player_Mian.金 - 2000
            # print('普通召唤装备！')
            等级 = random.randint(0, 1000)

            if Config_Config.get('E_pool') == None:
                ABC = DE.Z装备列表[random.randint(0, len(DE.Z装备列表) - 1)]

            elif Config_Config.get('E_pool') <= len(DE.Z装备列表):
                ABC = DE.Z装备列表[Config_Config.get('E_pool') - 1]
                等级 = 999

            else:
                ABC = DE.Z装备列表[random.randint(0, len(DE.Z装备列表) - 1)]

            # print('等级', 等级)
            if 等级 < 800:
                ABC.append('史诗')
            else:
                ABC.append('传承')

            E = DE.Equipment(ABC)
            try:
                DE.Player_Mian.装备组.append(E)
            except:
                DE.Player_Mian.装备组 = []
                DE.Player_Mian.装备组.append(E)
            自动保存()
            self.装备显示容器 = LabelFrame(self.frame, text=E.name + ' ' + E.ID, height=210, width=300, bg='white')
            self.抽装备关闭按钮 = Button(self.装备显示容器, text='X', command=off, relief=FLAT, bg='white')
            self.抽装备关闭按钮.place(x=275, y=0)
            self.装备图标_P = Open_Jpg(os.path.join('Resource', 'picture', 'Equipment', f'{E.Code}.jpg'))
            self.装备图标 = Label(self.装备显示容器, image=self.装备图标_P)
            self.装备图标.place(x=0, y=0)
            self.装备名称 = Label(self.装备显示容器, text=E.name, font=('Aridl', 11), bg='white', fg=DE.装备字体颜色.get(E.品级)).place(
                x=160, y=0)
            self.装备品级 = Label(self.装备显示容器, text=E.品级, bg='white').place(x=240, y=0)
            self.装备属性 = Label(self.装备显示容器, text=E.获得装备属性(), justify=LEFT, bg='white').place(x=160, y=20)

            self.装备显示容器.place(x=533, y=280)
            print('成功抽取准备！')
            print(E.__dict__)
            self.刷新资源UI()

    def 抽卡成功(self):
        time.sleep(0.1)  # 抽卡成功等待1秒

        if Config_Config.get('G_pool') == None:
            OC = DE.Y元神列表[random.randint(0, len(DE.Y元神列表)) - 1]

        elif Config_Config.get('G_pool') <= len(DE.Y元神列表):  # 定向召唤
            OC = DE.Y元神列表[Config_Config.get('G_pool') - 1]

        else:
            OC = DE.Y元神列表[random.randint(0, len(DE.Y元神列表)) - 1]

        G = DE.Genshin(OC)
        print(G.__dict__)
        # self.GB_FM = Frame(self.frame, height=768, width=1366)

        self.GB_P = Open_Jpg(os.path.join('Resource', 'picture', 'Genshin', f'{G.Code}-d.jpg'))
        大图宽 = self.GB_P.width()
        if 大图宽 < 1366:
            放置位置 = (1366 - 大图宽) / 2
        else:
            放置位置 = 0
        self.GB = Label(self.frame, image=self.GB_P)
        self.GB.place(x=放置位置, y=0)
        # self.GB_C = Button(self.GB_FM, text='查看')

        颜色 = {'B': 'chartreuse', 'A': 'cyan', 'S': '', 'S1': '', 'SS': ''}

        self.GLFM = Frame(self.frame)
        self.GLFM.place(x=1230, y=660)
        self.GL_name = Label(self.GLFM, text=G.name, font=('Aridl', 13))
        self.GL_name.pack()
        self.GL_等级 = Label(self.GLFM, text=G.等级, font=('Aridl', 13))
        self.GL_等级.pack()
        self.GBB = Button(self.GLFM, text='关闭', command=self.关闭卡片)
        self.GBB.pack()
        # self.GB_FM.place(x=0, y=0)
        # self.GB_C.place(x=0,y=301)
        # self.召唤.place_forget()
        DE.Player_Mian.元神组.append(G)  # 把抽出来的卡片放入背包
        # print(DE.Player_Mian.元神组)
        self.刷新资源UI()
        print(f'成功抽取元神！{G}')

    def 关闭卡片(self):
        # self.召唤.place(x=610, y=468)
        self.GB.destroy()
        self.GLFM.destroy()
        切换场景(Call)

    def 符文礼包(self):
        if DE.Player_Mian.玉 > 1000:
            DE.Player_Mian.玉 = DE.Player_Mian.玉 - 1000
            DE.Player_Mian.召唤符 = DE.Player_Mian.召唤符 + 11
            self.刷新资源UI()
            自动保存()

    def 符文大满贯(self):
        if DE.Player_Mian.玉 > 6888:
            DE.Player_Mian.玉 = DE.Player_Mian.玉 - 6888
            DE.Player_Mian.召唤符 = DE.Player_Mian.召唤符 + 99
            self.刷新资源UI()
            自动保存()

    def run(self):
        self.frame.place(x=0, y=0)

    def off(self):
        self.frame.place_forget()


class Start():
    def __init__(self, root):
        self.name = '开始'
        # self.L_image_open = Image.open(os.path.join('Resource','picture',f'BG.png')
        # self.L_image = ImageTk.PhotoImage(self.L_image_open)
        self.L_image = Open_Jpg(os.path.join('Resource', 'picture', 'BIG', f'START.jpg'))
        self.frame = Frame(root, height=768, width=1366)
        self.L = Label(self.frame, image=self.L_image)
        self.L.place(x=0, y=0)
        self.frame.place(x=0, y=0)

    def run(self):
        self.frame.place(x=0, y=0)

    def off(self):
        self.frame.place_forget()


# 未使用
class Player_switching():  # 角色切换
    def __init__(self, root):
        # self.L_image_open = Image.open(os.path.join('Resource','picture',f'BG.png')
        # self.L_image = ImageTk.PhotoImage(self.L_image_open)
        self.L_image = Open_Jpg(os.path.join('Resource', 'picture', 'BIG', f'START.jpg'))
        self.frame = Frame(root, height=768, width=1366)
        self.L = Label(self.frame, image=self.L_image)
        self.L.place(x=0, y=0)
        self.frame.place(x=0, y=0)

    def run(self):
        self.frame.place(x=0, y=0)

    def off(self):
        self.frame.place_forget()


# 胧界幻境视图
class Home():
    def __init__(self, root):
        self.name = '开始'
        # self.L_image_open = Image.open(os.path.join('Resource','picture',f'BG.png')
        # self.L_image = ImageTk.PhotoImage(self.L_image_open)
        self.L_image = Open_Jpg(os.path.join('Resource', 'picture', 'BIG', f'SHHJ.jpg'))
        self.frame = Frame(root, height=768, width=1366)
        self.L = Label(self.frame, image=self.L_image)
        self.L.place(x=0, y=0)
        self.frame.place(x=0, y=0)
        self.create_UI()

    # 用于创建UI功能按钮
    def create_UI(self):
        '''用于创建UI功能按钮'''
        self.BTTX = 816
        self.BTTY = 710
        # self.人物_P = Open_Jpg(os.path.join('Resource','picture','ui',f'JS.jpg'))
        # self.人物 = Button(self.frame, image=self.人物_P, command=self.属性UI, relief=FLAT)
        # self.人物.place(x=self.BTTX, y=self.BTTY)

        self.背包_P = Open_Jpg(os.path.join('Resource', 'picture', 'ui', f'BB.jpg'))
        self.背包 = Button(self.frame, image=self.背包_P, relief=FLAT, command=lambda: 切换场景(Equipment_view))
        self.背包.place(x=self.BTTX + 110, y=self.BTTY)

        self.元神_P = Open_Jpg(os.path.join('Resource', 'picture', 'ui', f'YS.jpg'))
        self.元神 = Button(self.frame, image=self.元神_P, command=lambda: 切换场景(Genshin_view), relief=FLAT)
        self.元神.place(x=self.BTTX + 220, y=self.BTTY)

        self.世界_P = Open_Jpg(os.path.join('Resource', 'picture', 'ui', f'SJ.jpg'))
        self.世界 = Button(self.frame, image=self.世界_P, command=大地图, relief=FLAT)
        self.世界.place(x=self.BTTX + 330, y=self.BTTY)

        self.召唤_P = Open_Jpg(os.path.join('Resource', 'picture', 'ui', f'ZH.jpg'))
        self.召唤 = Button(self.frame, image=self.召唤_P, command=lambda: 切换场景(Call), relief=FLAT)
        self.召唤.place(x=self.BTTX + 440, y=self.BTTY)

        # 经济属性

        '''用于创建UI显示资源的按钮'''
        self.资源UIX = 1086
        self.资源UIY = 25

        self.召唤符FM = Frame(self.frame, bg='black', height=40, width=250)
        self.召唤符P_P = Open_Jpg(os.path.join('Resource', 'picture', 'ui', f'P_UI_FW.jpg'))
        self.召唤符_P = Label(self.召唤符FM, image=self.召唤符P_P, relief='solid')
        self.召唤符_P.place(x=0, y=0)
        self.召唤符S = StringVar()
        self.召唤符S.set(str(DE.Player_Mian.召唤符))
        self.召唤符L = Label(self.召唤符FM, textvariable=self.召唤符S, font=DE.资源font, fg='SkyBlue', bg='black').place(x=120,
                                                                                                              y=0)
        self.召唤符FM.place(x=self.资源UIX, y=self.资源UIY)

        self.勾玉FM = Frame(self.frame, bg='black', height=40, width=250)
        self.勾玉P_P = Open_Jpg(os.path.join('Resource', 'picture', 'ui', f'P_UI_Y.jpg'))
        self.勾玉_P = Label(self.勾玉FM, image=self.勾玉P_P, relief='solid')
        self.勾玉_P.place(x=0, y=0)
        self.勾玉S = StringVar()
        self.勾玉S.set(str(DE.Player_Mian.玉))
        self.勾玉L = Label(self.勾玉FM, textvariable=self.勾玉S, font=DE.资源font, fg='SkyBlue', bg='black').place(x=120, y=0)
        self.勾玉FM.place(x=self.资源UIX, y=self.资源UIY + 50)

        self.黄金FM = Frame(self.frame, bg='black', height=40, width=250)
        self.黄金P_P = Open_Jpg(os.path.join('Resource', 'picture', 'ui', f'P_UI_G.jpg'))
        self.黄金_P = Label(self.黄金FM, image=self.黄金P_P, relief='solid')
        self.黄金_P.place(x=0, y=0)
        self.黄金S = StringVar()
        self.黄金S.set(str(DE.Player_Mian.金))
        self.黄金L = Label(self.黄金FM, textvariable=self.黄金S, font=DE.资源font, fg='SkyBlue', bg='black').place(x=120, y=0)
        self.黄金FM.place(x=self.资源UIX, y=self.资源UIY + 100)

        self.铜钱FM = Frame(self.frame, bg='black', height=40, width=250)
        self.铜钱P_P = Open_Jpg(os.path.join('Resource', 'picture', 'ui', f'P_UI_T.jpg'))
        self.铜钱_P = Label(self.铜钱FM, image=self.铜钱P_P, relief='solid')
        self.铜钱_P.place(x=0, y=0)
        self.铜钱S = StringVar()
        self.铜钱S.set(str(DE.Player_Mian.铜))
        self.铜钱L = Label(self.铜钱FM, textvariable=self.铜钱S, font=DE.Exp_font, fg='SkyBlue', bg='black').place(x=120, y=8)
        self.铜钱FM.place(x=self.资源UIX, y=self.资源UIY + 150)

        self.ExpFM = Frame(self.frame, bg='black', height=40, width=250)
        self.ExpP_P = Open_Jpg(os.path.join('Resource', 'picture', 'ui', f'P_UI_EXP.jpg'))
        self.Exp_P = Label(self.ExpFM, image=self.ExpP_P, relief='solid')
        self.Exp_P.place(x=0, y=0)
        self.ExpS = StringVar()
        self.ExpS.set(str(DE.Player_Mian.exp))
        self.ExpL = Label(self.ExpFM, textvariable=self.ExpS, font=DE.Exp_font, fg='SkyBlue', bg='black').place(x=120,
                                                                                                                y=8)
        self.ExpFM.place(x=self.资源UIX, y=self.资源UIY + 200)

    def run(self):
        self.frame.place(x=0, y=0)

    def off(self):
        self.frame.place_forget()

    # 用于显示游戏角色属性
    def 属性UI(self):
        print('创建属性UI成功！')
        self.UI = Frame(self.frame, height=700, width=300)
        self.UI.place(x=50, y=50)
        self.头像 = Open_Jpg(os.path.join('Resource', 'picture', 'paly', f'{DE.Player_Mian.角色代码}.jpg'))
        self.L1 = Label(self.UI, image=self.头像).place(x=0, y=0)
        self.角色属性文本 = f'''
                    {DE.Player_Mian.name}
                    Lv {DE.Player_Role.Lv}
                    ###天赋属性###
                    力量资质:{DE.Player_Role.力量资质}
                    智慧资质:{DE.Player_Role.智慧资质}
                    体力资质:{DE.Player_Role.体力资质}
                    敏捷资质:{DE.Player_Role.敏捷资质}

                    ###基础属性###
                    力量:{DE.Player_Role.力量}
                    智慧:{DE.Player_Role.智慧}
                    体力:{DE.Player_Role.体力}
                    敏捷:{DE.Player_Role.敏捷}

                    ###战斗属性###
                    HP: {DE.Player_Role.HP}
                    物理攻击: {DE.Player_Role.物理攻击}
                    法术攻击: {DE.Player_Role.法术攻击}
                    闪避: {DE.Player_Role.闪避}
                    命中: {DE.Player_Role.命中}
        '''
        self.L2 = Label(self.UI, text=self.角色属性文本, justify=LEFT).place(x=0, y=301)
        self.关闭属性窗口 = Button(self.UI, text='X', command=self.UI.destroy, anchor='w').place(x=280, y=0)
        # self.关闭按钮 = 关闭按钮(self.UI)


# 切换主角视图
class C_P():
    def __init__(self, root):
        self.name = '角色切换'
        self.frame = Frame(root, height=768, width=1366)
        '''三个主角三个按钮'''
        self.No1_image = Open_Jpg(os.path.join('Resource', 'picture', 'paly', f'P1.jpg'))
        self.No1 = Button(self.frame, image=self.No1_image, command=self.SW, relief=FLAT)
        self.No1.pack(side=LEFT)

        self.No2_image = Open_Jpg(os.path.join('Resource', 'picture', 'paly', f'P2.jpg'))
        self.No2 = Button(self.frame, image=self.No2_image, command=self.LY, relief=FLAT)
        self.No2.pack(side=LEFT, padx=30)

        self.No3_image = Open_Jpg(os.path.join('Resource', 'picture', 'paly', f'P3.jpg'))
        self.No3 = Button(self.frame, image=self.No3_image, command=self.JL, relief=FLAT)
        self.No3.pack(side=LEFT)
        self.PL = Label(self.frame, text=ancient_engine.角色信息()).pack(side=LEFT, padx=30)
        self.L = Label(self.frame, text=ancient_engine.角色介绍)
        self.L.pack(side=LEFT, padx=30)
        # self.frame.pack()
        self.frame.place(x=0, y=0)

    def run(self):
        self.frame.place(x=0, y=0)

    def off(self):
        self.frame.pack_forget()

    def SW(self):
        '''通过改变主玩家的角色代码实现角色切换'''
        # print('素问！', DE.Player_Mian.name)
        DE.Player_Mian.角色代码 = 'SW'
        DE.Player_Role = DE.Role_SW(DE.Player_Mian.Lv)
        DE.幻境 = Home(win)

    def LY(self):
        '''通过改变主玩家的角色代码实现角色切换'''
        DE.Player_Mian.角色代码 = 'LY'
        DE.Player_Role = DE.Role_LY(DE.Player_Mian.Lv)
        # print('龙吟！', DE.Player_Mian.name)
        DE.幻境 = Home(win)

    def JL(self):
        '''通过改变主玩家的角色代码实现角色切换'''
        DE.Player_Mian.角色代码 = 'JL'
        DE.Player_Role = DE.Role_JL(DE.Player_Mian.Lv)
        # print('九灵！', DE.Player_Mian.name)
        DE.幻境 = Home(win)


# 场景切换测试
def VeTest():
    while True:
        切换场景(Equipment_view)
        time.sleep(1)
        切换场景(Genshin_view)


if __name__ == '__main__':
    print('正在启动。。。。。')
    # log.start('正在启动。。。。。')
    C_LIST = []
    win = Tk()
    win.geometry('1368x769')
    win.title(ancient_engine.Tite)
    win.resizable(width=False, height=False)  # 锁定窗口
    # 创建创建
    # Backpack_UI = Backpack(win)
    # Map_UI = Map(win)
    # Game_UI = Game(win)
    # Player_switching_UI = Player_switching(win)
    # C_P_UI = C_P(win)
    # Start_UI = Start(win)
    # 创建全局对象
    DE.当前场景 = Start(win)
    print('场景初始化完成！')
    # log.start('场景初始化完成！')
    # P1 = None
    # load()
    New_存档加载界面()

    Main_menubar = Menu(win, tearoff=False)  # tearoff=False 隐藏分割线
    Sys_menu = Menu(Main_menubar, tearoff=False)  # 系统菜单
    Sys_menu.add_command(label='加载游戏', command=New_存档加载界面)
    # Sys_menu.add_command(label='切换主角', command=切换角色)
    Sys_menu.add_command(label='游戏设置')
    # Sys_menu.add_command(label='游戏图鉴',command=VeTest)
    Sys_menu.add_command(label='保存游戏', command=自动保存)
    Sys_menu.add_command(label='修改器', command=DEUBG)
    Sys_menu.add_command(label='退出游戏', command=退出游戏)

    Paly_menu = Menu(Main_menubar, tearoff=False)  # 玩家菜单
    # Paly_menu.add_command(label='角色', command=Home.属性UI)
    # Paly_menu.add_command(label='技能')
    Paly_menu.add_command(label='神社', command=lambda: 切换场景(Genshin_view))
    Paly_menu.add_command(label='背包', command=lambda: 切换场景(Equipment_view))

    Game_menu = Menu(Main_menubar, tearoff=False)  # 游戏菜单
    Game_menu.add_command(label='胧界幻境', command=lambda: 切换场景(Home))
    Game_menu.add_command(label='拜月祠堂', command=lambda: 切换场景(Call))
    Game_menu.add_command(label='副本地图', command=大地图)
    # 向主菜单添加子菜单
    Main_menubar.add_cascade(label="玩家菜单", menu=Paly_menu)
    Main_menubar.add_cascade(label="游戏功能", menu=Game_menu)
    Main_menubar.add_cascade(label="系统设置", menu=Sys_menu)
    win.bind("<Button-3>", showMenu)
    win.mainloop()
