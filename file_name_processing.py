import os
import Mek_master as Mek


def a100(dir):
    file_list = os.listdir(dir)
    for file in file_list:
        #print(file)
        #print()

        file_name = file[8::].replace('-d.png','-c.png')
        src_file_path = os.path.join(path, file)
        new_file_path = os.path.join(path, file_name)

        os.rename(src_file_path, new_file_path)


def a432(dir):
    file_list = os.listdir(dir)
    for file in file_list:
        # print(file)
        #print()

        file_name = file[8::].replace('-d.png', '-x.png')
        src_file_path = os.path.join(path,file)
        new_file_path = os.path.join(path,file_name)

        os.rename(src_file_path,new_file_path)

def bb():
    path1 = r'C:\Users\Mek\Desktop\J1'

    list = os.listdir(path1)
    for file in list:
        file_path = os.path.join(path1,file)
        print(file_path)
        new_file_path = os.path.join(path1,f'{Mek.get_random_letters(8)}.jpg')
        print(new_file_path)
        os.rename(file_path,new_file_path)




if __name__ == '__main__':
    path = None
    bb()

