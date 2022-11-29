# 日志系统
import Mek_master as Mek
from threading import Thread

file = 'config.json'

Config_Config = Mek.read_json(file)

class Log():
    def __init__(self):
        self.print = Config_Config.get('log_print')
        self.write = Config_Config.get('log_write')

        if Config_Config.get('log_file') == None:
            self.file = 'default.log'
        else:
            self.file = Config_Config.get('log_file')

    def write_file(self,file, Data):  # 写入文件
        with open(file, 'a+', encoding='utf-8') as file:
            file.write(str(Data))

    def log(self,text):
        if self.print:
            print('---',Mek.get_localtime())
            print(text)

        if self.write:
            self.write_file(self.file,f'---{Mek.get_localtime()}\n{text}\n')
            #self.write_file(self.file, text)

    def start(self,text):
        self.t = Thread(target=self.log,args=(text,))
        self.t.start()



if __name__ == '__main__':
    log = Log()
    print(log.file)
    for i in range(100):
        text = '12312312321'
        log.start(text)

