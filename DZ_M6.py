import sys
from pathlib import Path
import os
import shutil

#пошук файлів у вкладених папках
def search(path):    
#    print(os.getcwdb())
    list_dir_ = ['video', 'audio', 'documents', 'images', 'archives'] #перелік папок для работи скрипта (сервісні папки)
    list_dir = [path]
    all_dir = os.walk(path)
    for i in all_dir: #перебор папок
        #print(i)            
        if i[0] == str(path):
            list_name_file = i[2]
            if list_name_file != []:
                for f in list_name_file:                
                    move_file(fr'{path}/{f}', path) #виклик функції перенесення файлів        
        else:
            
            name_dir = i[0] #назва вкладеної папки
            one_dir = str(name_dir.split(path)[1]).split('/')[1] 
            
            if one_dir in list_dir_: # перевірка чи папка є сервісною для роботи
                pass
            else: # якщо ні то обробляємо
                #print(name_dir ,path + normalize(name_dir.split(path)[1]))
                os.rename(name_dir, path + normalize(name_dir.split(path)[1])) # переіменування папки в латиницю
                list_name_file = i[2]
                #print('додаємо папку до переліку',name_dir)
                list_dir.append(path + normalize(name_dir.split(path)[1]))    
                if list_name_file != []:
                    for f in list_name_file:                
                        move_file(fr'{name_dir}/{f}', path) #виклик функції перенесення файлів         
    return path, list_dir

#переміщення файлів до папок та перевод назви файлу у латиницю
def move_file(path_file, path):
    #print(path_file)
    
    list_dir_ = ['video', 'audio', 'documents', 'images', 'archives'] #перелік папок для работи скрипта(сервісні папки)
    dict_dir = {'images':['JPEG', 'PNG', 'JPG', 'SVG'], 
                'video': ['AVI', 'MP4', 'MOV', 'MKV'], 
                'audio': ['MP3', 'OGG', 'WAV', 'AMR'], 
                'documents': ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'], 
                'archives': ['ZIP', 'GZ', 'TAR']} # словник з розширеннями файлів
    
    file = os.path.basename(path_file) #відокремлюємо назву файлу
    
    suffix_file = str(Path(path_file).suffix).upper()[1:] #приведення розширення до вигляду як у словнику
    file = normalize(file.split('.')[0]) + str(Path(path_file).suffix) #переіменування файла у латиницю

    #фільтруваня файла по групах
    if suffix_file in dict_dir['video']:
        #print('video', fr'{path_file}')        
        os.rename(path_file, fr'{path}/video/{file}')
    elif suffix_file in dict_dir['images']:
        #print('images', fr'{path_file}')
        os.rename(path_file, fr'{path}/images/{file}')
    elif suffix_file in dict_dir['audio']:
        #print('audio', fr'{path_file}')
        os.rename(path_file, fr'{path}/audio/{file}')
    elif suffix_file in dict_dir['documents']:
        #print('documents', fr'{path_file}')
        os.rename(path_file, fr'{path}/documents/{file}')
    elif suffix_file in dict_dir['archives']:
        #print('archives', fr'{path_file}')
        file = file.split('.')[0]
        shutil.unpack_archive(path_file, fr'{path}/archives/{file}')
        os.remove(path_file)    
    else:
        print('Невідомий файл -->', fr'{path_file}')        

#Перевірка наявності папок для работи скрипта у вибраній дерікторії
def folder_project(path):
    list_dir_work = os.listdir(path) #отимання переліку папок та файлів у вибраній папці
    list_dir_ = ['video', 'audio', 'documents', 'images', 'archives'] #перелік папок для работи скрипта(сервісні папки)
    for i in list_dir_work: #перебираємо отриманий перелік
        if os.path.isdir(fr'{path}/{i}'): #перевіряємо чи то є папка 
            if i in list_dir_: #якщо так, то дивимось чи є ця папка в нашому робочому переліку
                #print(fr'this folder {i} exists')
                list_dir_.remove(i) #видаляємо існуючу папку з переліку папок для работи скрипта
    for d in list_dir_: #перебираєме перелік папок для работи скрипта щоб створити не існуючи папки 
        os.mkdir(fr'{path}/{d}') #створюємо папку
    print('перевірив')
                
#Функція переводу з кирилиці у латиницю назв
def normalize(name):    
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ "
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g", "_")

    TRANS = {}

    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()    

    return name.translate(TRANS)   

# Видалення пустих папок
def del_empty_dir(list_dir=[]):
    list_dir_ = ['video', 'audio', 'documents', 'images', 'archives'] #перелік папок для работи скрипта(сервісні папки)    

    for dir in sorted(list_dir, key=lambda x: len(x.split('/')), reverse=True):
        
        if dir in list_dir_: # перевірка чи входить папка у перелік сервісних папок
            pass
        else: 
            if os.listdir(dir) :
                #print(os.listdir(dir), dir)
                if os.listdir(dir) == ['.DS_Store']:
                    #print('пустая + DS_Store', dir)
                    shutil.rmtree(dir)
            else:
                #print('пустая', dir)
                shutil.rmtree(dir)
                
def main():

    try :        
        folder_project(sys.argv[1])
        #search(sys.argv[1])
        del_empty_dir(search(sys.argv[1])[1])    
    except IndexError as er:
        print(er)
        print('Ну і де посилання на дерікторію ?')

if __name__ == '__main__':
    main()



#зображення ('JPEG', 'PNG', 'JPG', 'SVG');
#відео файли ('AVI', 'MP4', 'MOV', 'MKV');
#документи ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX');
#музика ('MP3', 'OGG', 'WAV', 'AMR');
#архіви ('ZIP', 'GZ', 'TAR');
#невідомі розширення.

#зображення переносимо до папки images
#документи переносимо до папки documents
#аудіо файли переносимо до 'audio'
#відео файли до video
#архіви розпаковуються та їх вміст переноситься до папки archives
