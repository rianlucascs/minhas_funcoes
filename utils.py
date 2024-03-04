
from os import name, sep, path
from os import getcwd, remove
from pandas import read_csv, read_excel
from datetime import datetime
from subprocess import Popen, run
from time import sleep
from tkinter import filedialog

def get_funcion_name():
    from inspect import currentframe, getouterframes
    frame = currentframe()
    function_name = getouterframes(frame)[1].function
    return function_name

def get_operating_system_name():
    systems = {'nt': 'windows', 'posix': 'mac'}
    if name not in systems.keys():
        raise SystemError(f'*Erro {get_funcion_name()}')    
    else:
        return systems[name]

def detect_folder_separator():
    _system_name = get_operating_system_name()
    if _system_name == 'windows':
        row_sep = len(sep)
        match row_sep:
            case 0:
                raise SystemError(f'*Erro {get_funcion_name()}')
            case 1:
                _sep = sep
                __sep = _sep + _sep
            case 2:
                _sep = sep[0]
                __sep = sep
        return _sep, __sep, row_sep
    elif _system_name == 'mac':
        return '/', '/', 1

def get_path_folder():
    _system_name = get_operating_system_name()
    _separator = detect_folder_separator()
    current_path = getcwd()
    match _system_name:
        case 'windows':
            return current_path.replace(_separator[0], _separator[1]) + _separator[1]
        case 'mac':
            return current_path + _separator[0]
    
def get_encoding():
    _system_name = get_operating_system_name()
    match _system_name:
        case 'windows':
            return 'UTF-8'
        case 'mac':
            return 'ISO-8859-15'

def get_parent_directory_path(levels_back=1):
    current_path = getcwd()
    parent_path = current_path
    for _ in range(levels_back):
        parent_path = path.dirname(parent_path)
    return parent_path

def add_path(list_archives=[], bar_last=False):
    _path_folder = get_path_folder()
    _separator = detect_folder_separator()
    for i, archive in enumerate(list_archives):
        _path_folder += archive
        if i != len(list_archives) - 1:
            _path_folder += _separator[1]
    if bar_last:
        _path_folder += _separator[1]
    return _path_folder

def add_bar_last(_path):
    _separator = detect_folder_separator()
    return f'{_path}{_separator[1]}'

def update_bar(_path, update):
    _separator = detect_folder_separator()
    _system_name = get_operating_system_name()
    match _system_name:
        case 'windows':
            match update:
                case 'de duas para uma':
                    return _path.replace(_separator[1], _separator[0])
        case 'mac':
            pass

def detect_path(_path):
    if path.exists(_path):
        return True
    return False

def simple_writing(_path, message):
    _encoding = get_encoding()
    with open(_path, 'a', encoding=_encoding) as archive:
        archive.write(message)
    return None

def complex_writing(_path, message, update=False, skip_the_line=False, skip_execution=False):
    if skip_execution:
        return None
    if update:
        if detect_path(_path):
            remove(_path)
    if skip_the_line:
        message = message + '\n'
    simple_writing(_path, message)
    return None

def complex_reading(_path, type):
    import json
    types = {'read': lambda arquivo: arquivo.read(), 
             'readlines': lambda arquivo: arquivo.readlines(),
             'json': lambda arquivo: json.load(arquivo)}
    _encoding = get_encoding()
    with open(_path, 'r', encoding=_encoding) as archive:
        if type in types:
            return types[type](archive)
        
def detect_info(_path, info):
    archive = complex_reading(_path, 'readlines')
    for row in archive:
        for i in range(len(row)):
            if info == row[i:i+len(info)]:
                return True
    return False

def logmy(_path, message, type, update=False, skip_the_line=False, skip_execution=False):
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    types = {'INFO': f'[{time}] [INFO]', 'AVISO': f'[{time}] [AVISO]', 'ERRO': f'[{time}] [ERRO]'}
    message = f'{types[type]} {message}'
    complex_writing(_path, message, update, skip_the_line, skip_execution)
    
def shell_execution(_path, type):
    _system_name = get_operating_system_name()
    match _system_name:
        case 'windows':
            match type:
                case 'popen':
                    Popen(['start', _path], shell=True)
                case 'run':
                    run(['cmd', '/c', 'start', _path], shell=True)
        case 'mac':
            run(f'osascript -e \'tell application "Terminal" to do script "sh {_path}"\'', shell=True)

# import ctypes
# # Constantes para as cores do console
# STD_OUTPUT_HANDLE = -11
# FOREGROUND_RED = 0x0004 | 0x0008  # Vermelho
# FOREGROUND_GREEN = 0x0002 | 0x0008  # Verde
# FOREGROUND_BLUE = 0x0001 | 0x0008  # Azul
# FOREGROUND_ROXO = FOREGROUND_RED | FOREGROUND_BLUE | 0x0008

# def set_color(color):
#     ctypes.windll.kernel32.SetConsoleTextAttribute(ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE), color)
# set_color(FOREGROUND_ROXO)
            
def dynamic_shell_execution(
        path_py = None,
        path_bat = None,
        path_sh = None,
        update = False,
        skip_execution = False,
        run_after_creation = False,
        delete_after_execution = False,
        path_log_execution_txt = None,
        path_background_vbs = None,
        path_background_mac = None,
        color_shell = 'F1',
        ):
    
    _system_name = get_operating_system_name()
    _separator = detect_folder_separator()
    _last_archive = path_py.split(_separator[0])[-1]
    _path_folder = path_py.replace(_last_archive, '') # [:-1] 
    match _system_name:
        case 'windows':
            text_windows_bat = f'color {color_shell}\ncd {_path_folder}\npython {_last_archive}'
            complex_writing(path_bat, text_windows_bat, update, False, skip_execution)
            if path_background_vbs != None and path_background_vbs != False:
                text_windows_vbs = f'Set WshShell = CreateObject("WScript.shell")\nWshShell.Run "{path_bat}", 0'
                complex_writing(path_background_vbs, text_windows_vbs, update, False, skip_execution)
            if run_after_creation:
                if path_background_vbs != None and path_background_vbs != False:
                    shell_execution(path_background_vbs, 'run')
                else:
                    shell_execution(path_bat, 'run')
                if path_log_execution_txt != None and path_log_execution_txt != False:
                    text_windows_log_execution_txt = f'start {_last_archive}' 
                    logmy(path_log_execution_txt, text_windows_log_execution_txt, 'INFO', skip_the_line=True)
            if delete_after_execution:
                sleep(0.3)
                remove(path_bat)
                if path_background_vbs != None and path_background_vbs != False:
                    remove(path_background_vbs)
        case 'mac':
            text_mac_sh = f'cd {_path_folder}\npython {_last_archive}'
            complex_writing(path_sh, text_mac_sh, update, False, skip_execution)           
            if path_background_mac != None and path_background_mac != False:
                raise TypeError('*Erro background MAC nao adicionado!')
            if run_after_creation:
                if path_background_mac != None and path_background_mac != False:
                    raise TypeError('*Erro background MAC nao adicionado!')
                else:
                    shell_execution(path_sh, 'run')
                    
    return None

# dynamic_shell_execution(path_py = r'X:\Users\teste.py',
#                         path_bat = r'X:\Users\teste_exec.bat',
#                         update=True,
#                         # path_background_vbs=r'X:\Users\teste_exec_bg.vbs',
#                         path_background_vbs=None,
#                         run_after_creation=True,
#                         path_log_execution_txt=r'X:\Users\log_exec_teste.txt',
#                         delete_after_execution=True)


def update_separator_path(_path):
    _system_name = get_operating_system_name()
    _separator = detect_folder_separator()
    match _system_name:
        case 'windows':
            updated_path = _path.replace(_separator[0], _separator[1])
            updated_path = _path.replace(_separator[0]+_separator[1], _separator[1])
            updated_path = _path.replace((_separator[1]*2), _separator[1])
            updated_path = _path.replace((_separator[1]*2) + _separator[0], _separator[1])
            return updated_path
        case 'mac':
            raise ValueError(f'*Erro {get_funcion_name()}')

def read_table_data(_path=None, path_popup=False, _sep=';', register_path_popup_txt=None, fillna=None):
    if not path_popup and _path is None:
        raise TypeError('*Erro _path nao informado') 
    if path_popup:
        _path = filedialog.askopenfilename()
    _path = update_separator_path(_path)
    _encoding = get_encoding()
    file_type = {'xlsx': lambda _path: read_excel(_path),
                 'csv': lambda _path: read_csv(_path, encoding=_encoding, sep=_sep)}
    type = _path.split('.')[-1]
    if type in file_type:
        if register_path_popup_txt != None:
            complex_writing(register_path_popup_txt, _path, True)
        if fillna != None:
            df_data = file_type[type](_path).fillna(fillna)
        else:
            df_data = file_type[type](_path)
        return df_data
    else:
        raise TypeError(f'*Erro {get_funcion_name()}')


def remove_specific_characters(
        string,
        remove_accents_from_letters=False,
        remove_characters=False,
        remove_numbers=False,
        replace_with='',
        replace_except='',
        ):
        string = str(string)
        if remove_accents_from_letters:
            tuple_with_uppercase_accents = {'á': 'a', 'à': 'a', 'â': 'a', 'ã': 'a', 'é': 'e', 'ê': 'e', 
                                            'í': 'i', 'ó': 'o', 'ô': 'o', 'õ': 'o', 'ú': 'u', 'ü': 'u', 
                                            'ç': 'c'}
            tuple_with_lowercase_accents = {'Á': 'A', 'À': 'A', 'Â': 'A', 'Ã': 'A', 'É': 'E', 'Ê': 'E', 
                                            'Í': 'I', 'Ó': 'O', 'Ô': 'O', 'Õ': 'O', 'Ú': 'U', 'Ü': 'U', 
                                            'Ç': 'C'}
            for accent in tuple_with_uppercase_accents.keys():
                if accent in string and not accent in replace_except:
                    string = string.replace(accent, tuple_with_uppercase_accents[accent])
            for accent in tuple_with_lowercase_accents.keys():
                if accent in string and not accent in replace_except:
                    string = string.replace(accent, tuple_with_lowercase_accents[accent])
        if remove_characters:
            list_characters = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '-', '=', 
                               '{', '}', '[', ']', '|', '\\', ':', ';', '"', "'", '<', '>', ',', '.', 
                               '?', '/', '\t', '\n', '\r']
            for character in list_characters:
                if character in string and not character in replace_except:
                    string = string.replace(character, replace_with)
        if remove_numbers:
            list_numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
            for number in list_numbers:
                if number in string and not number in replace_except:
                    string = string.replace(number, replace_except)
        return string

def compute_similarity(string1, string2):
    from difflib import SequenceMatcher
    return SequenceMatcher(None, str(string1).lower(), str(string2).lower()).ratio()




            
                    

    