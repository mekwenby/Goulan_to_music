# 奖励控制及配置管理
import Mek_master as Mek

file = 'config.json'

def construct_reward_list():  # 创建奖励配置文件及定向召唤标识
    GLv = 45
    data = {
        'R0': {'Y': 0 * GLv, 'G': int(0.1 * GLv), 'T': 200 * GLv, 'Exp': 300 * GLv},  # 宿敌   ！好像未实装
        'R1': {'Y': 0.4, 'G': 30, 'T': 1234, 'Exp': 10666},  # 斗技 掉落
        'R2': {'Y': 1, 'G': 20, 'T': 7888, 'Exp': 19887},  # 大魔王、莉莉崽 掉落
        'R3': {'Y': 0.1, 'G': 0.1, 'T': 100, 'Exp': 1000},  # 训练场 掉落
        'R4': {'Y': 18, 'G': 400, 'T': 0, 'Exp': 0},  # 莉莉崽隐藏关卡 掉落
        'R5':{'Y': 50, 'G': 1000, 'T': 0, 'Exp': 0}, # 花朝节
        'G_pool': None,  # 元神标记定向召唤 填入元神在 Data_engine.py.Y元神列表 中的index
        'E_pool': None,  # 准备标记定向召唤 同上
        'log_print': False,  # 日志打印
        'log_write': False,  # 日志写入
        'log_file': None,  # 日志存储文件
        'sleep_time':0.6 # 回合时间
    }

    Mek.write_json(file, data)

try:
    Config_Config = Mek.read_json(file)
except:
    print('Config_Config配置文件损坏,已重置!')
    construct_reward_list()
    Config_Config = Mek.read_json(file)



if __name__ == '__main__':
    construct_reward_list()
    # print(Config_Config.get('G_pool'))
    # print(type(Config_Config.get('G_pool')))
    # print(Config_Config)
    #print(Config_Config)
