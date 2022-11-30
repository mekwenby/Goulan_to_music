import Data_engine as DE

角色介绍 = '''
素问
擅长治疗和法术攻击

龙吟
擅长物理攻击

九灵
擅长法术和控制

'''

def 角色信息():
    text = f'''
昵称：{DE.Player_Mian.name}
等级：{DE.Player_Mian.Lv}
勾玉：{DE.Player_Mian.玉}
金条：{DE.Player_Mian.金}
铜钱：{DE.Player_Mian.铜}
累计经验：{DE.Player_Mian.exp}
    '''
    return text

Tite = '勾栏听曲 0.9.1'


if __name__ == '__main__':
    pass