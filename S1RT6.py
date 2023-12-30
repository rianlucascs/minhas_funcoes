
"""
28/12/23
https://www.linkedin.com/in/rian-lucas
"""

from os import getcwd, remove, listdir, rename, path, sep, name
from datetime import datetime
from subprocess import Popen, run
from time import sleep
from tkinter import filedialog
from pandas import read_csv, read_excel
from platform import system, version, platform
from zipfile import ZipFile

def _sistema():
    """Retorna o so."""
    sistemas = {'nt': 'windows', 'posix': 'mac'}
    if name in sistemas:
        return sistemas[name]
    if name not in sistemas.keys():
        raise ValueError('Sistema operacional diferente do esperado')

def _local() -> list:
    """Retorna o caminho ate a pasta atual, encoding de arquivos e barra do so."""
    if _sistema() == 'windows':
        return getcwd().replace('/', sep) + sep, 'UTF-8', sep
    elif _sistema == 'mac':
        return getcwd() + '/', 'ISO-8859-15', '/'

def _get_pasta(caminho:list=[]) -> str:
    """Retorna o caminho ate a pasta atual mais o arquivo ou pasta informado."""
    _str_caminho, _, barra = _local()
    for i, elementos in enumerate(caminho):
        _str_caminho += elementos
        if i != len(caminho) -1:
            _str_caminho += barra
    return _str_caminho
    
def _existe(caminho:list=[]) -> bool:
    """Verifica se o arquivo existe."""
    if path.exists(_get_pasta(caminho)):
        return True
    return False

def _escrita(caminho:list, mensagem:str, atualizar:bool=None, pular_linha:bool=False, pular_escrita:bool=False) -> None:
    """Escreve arquivos de texto."""
    _caminho_arquivo = _get_pasta(caminho)
    if pular_escrita:
        return None
    if atualizar:
        if path.exists(_caminho_arquivo):
            remove(_caminho_arquivo)
    with open(_caminho_arquivo, 'a', encoding=_local()[1]) as arquivo:
        if pular_linha:
            arquivo.write(mensagem + '\n')
        else:
            arquivo.write(mensagem)
    return None

def _leitura(caminho:list=[], tipo='read | readlines'):
    """Retorna a informação do arquivo."""
    tipos = {'read': lambda arquivo: arquivo.read(), 'readlines': lambda arquivo: arquivo.readlines()}
    with open(_get_pasta(caminho), 'r', encoding=_local()[1]) as arquivo:
        if tipo in tipos:
            return tipos[tipo](arquivo)

def _log(caminho:list, mensagem:str, tipo_log:str='INFO', atualizar:bool=False, pular_linha:bool=True, pular_escrita:bool=False) -> None:
    """Escreve em arquivo de texto no formato log."""
    tempo = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    tup_log = {'INFO': f'[{tempo}] [INFO]', 'AVISO': f'[{tempo}] [AVISO]', 'ERRO': f'[{tempo}] [ERRO]'}
    if tipo_log in tup_log:
        _escrita(caminho, f'{tup_log[tipo_log]} {mensagem}', atualizar, pular_linha, pular_escrita)
    else:
        raise TypeError('tipo_log tipo diferente do esperado')
    return None

def _terminal_exec(caminho:list, tipo_exec='popen | run'):
    """Executa python em um terminal."""
    if _sistema() == 'windows':
        if tipo_exec == 'popen':
            Popen(['start', _get_pasta(caminho)], shell=True)
        elif tipo_exec == 'run':
            run(['cmd', '/c', 'start', _get_pasta(caminho)], shell=True)
    elif _sistema() == 'mac': # <---!!! Testar no mac
        # chmod +x *
        run(f'osascript -e \'tell application "Terminal" to do script "sh {_get_pasta(caminho)}"')

def _dir_dell_arquivos(caminho:list=[]) -> None:
    """Deleta todos os arquivos do diretório."""
    if not(len(caminho)):
        raise NotADirectoryError('Não informou o diretório')
    for arquivo in listdir(_get_pasta(caminho)):
        remove(_get_pasta(caminho + [arquivo]))
    return None

def _info_loc(caminho:list, info:str) -> bool:
    """Verifica se a informação esta no arquivo."""
    arquivo = _leitura(caminho, 'readlines')
    for linha in arquivo:
        for i in range(len(linha)):
            if info == linha[i:i+len(info)]:
                return True
    return False

def _ultima_pasta(caminho:list, bar:str):
    return caminho.split(bar)[-1]

def _cria_exec_bat(caminho_loc_py:list, caminho_loc_bat:list, atualizar:bool=False, pular_escrita:bool=False,
                   executar_em_seguida:bool=False, excluir_em_seguida:bool=False, local_log_execucao:list=None,
                   local_background:list=None):
    """Cria arquivo .bat para executar um arquivo .py, parametros processos."""
    if caminho_loc_bat[-1].split('.')[-1] != 'bat':
        raise ValueError('Exteção do arquivo incorreta ".bat"')
    if local_background != None and local_background[-1].split('.')[-1] != 'vbs':
        raise ValueError('Execução do arquivo incorreta ".vbs"')
    _escrita(caminho_loc_bat, f'cd {_get_pasta(caminho_loc_py).replace(caminho_loc_py[-1], "")[:-1]}', atualizar, True, pular_escrita)
    _escrita(caminho_loc_bat, f'python {caminho_loc_py[-1]}', False, False, pular_escrita)
    if local_background != None:
        _escrita(local_background, 'Set WshShell = CreateObject("WScript.shell")', atualizar, True, pular_escrita)
        _escrita(local_background, f'WshShell.Run "{_get_pasta(caminho_loc_bat)}", 0', False, False, pular_escrita)
    if executar_em_seguida:
        if local_background != None:
            _terminal_exec(local_background, 'run')
        else:
            _terminal_exec(caminho_loc_bat, 'run')
    sleep(0.2)
    if excluir_em_seguida:
        if local_background != None:
            remove(_get_pasta(local_background))
        remove(_get_pasta(caminho_loc_bat))
    if local_log_execucao != None: 
        _log(local_log_execucao, f'{caminho_loc_py}, {atualizar}, {executar_em_seguida}, {excluir_em_seguida}', 'INFO')

# if __name__ == '__main__':
#     _cria_exec_bat(['teste.py'], ['exec_teste.bat'], atualizar=True, executar_em_seguida=True, excluir_em_seguida=True, local_log_execucao=['log_teste.txt'], local_background=['background.vbs'])

def _leitura_dados(caminho:list=None, caixa_de_escolha=False, _sep:str=';'):
    """Retorna o dataframe do arquivo .xlsx ou .csv"""
    if caixa_de_escolha:
        caminho = filedialog.askopenfilename()
        bar = '/'
    else:
        caminho = _get_pasta(caminho)
        bar = _local()[2]
    if not caixa_de_escolha and caminho is None:
        raise TypeError('Não informou o caminho')
    tipo_arquivo = _ultima_pasta(caminho, bar).split('.')[-1]
    tup_tipo = {'xlsx': lambda caminho: read_excel(caminho),
                    'csv': lambda caminho: read_csv(caminho, encoding=_local()[1], sep=_sep)}
    if tipo_arquivo in tup_tipo:
        return tup_tipo[tipo_arquivo](caminho)
    else:
        raise ValueError('Tipo arquivo diferente do esperado')

def _info_pc(caminho:list):
    """Cria arquivo .txt com as informações do sistema operacional, se criado, então
    verificac se mudou."""
    mensagem = f'{system()}\n{platform()}\n{version()}\n'
    if _existe(caminho) is False:
        _escrita(caminho, mensagem, False)
    else:
        arquivo = _leitura(caminho, 'readlines')
        for linha in arquivo:
            if not linha[:-1] in [system(), platform(), version()]:
                return False
        return True
    return None

def _remover_caracteries(string:str, letras:bool=True, caracteries:bool=False, numeros:bool=False, novo_valor:str='') -> str:
    if type(string) != str:
        raise ValueError('valor informado diferente de str.')
    if letras:
        tupla_acentos_minusculo = {'á': 'a', 'à': 'a', 'â': 'a', 'ã': 'a', 'é': 'e', 'ê': 'e', 'í': 'i', 'ó': 'o',
                                   'ô': 'o', 'õ': 'o', 'ú': 'u', 'ü': 'u', 'ç': 'c'}
        tupla_acentos_maiusculo = {'Á': 'A', 'À': 'A', 'Â': 'A', 'Ã': 'A', 'É': 'E', 'Ê': 'E', 'Í': 'I', 'Ó': 'O',
                                   'Ô': 'O', 'Õ': 'O', 'Ú': 'U', 'Ü': 'U', 'Ç': 'C'}
        for acentos in tupla_acentos_minusculo.keys():
            if acentos in string:
                string = string.replace(acentos, tupla_acentos_minusculo[acentos])
        for acentos in tupla_acentos_maiusculo.keys():
            if acentos in string:
                string = string.replace(acentos, tupla_acentos_maiusculo[acentos])
    if caracteries:
        caracteres = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '-', '=', '{', '}', '[', ']', '|',
                     '\\', ':', ';', '"', "'", '<', '>', ',', '.', '?', '/', '\t', '\n', '\r']
        for carac in caracteres:
            if carac in string:
                string = string.replace(carac, novo_valor)
    if numeros:
        lista_numeros = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        for num in lista_numeros:
            if num in string:
                string = string.replace(num, novo_valor)
    return string

def _extrair_zip(caminho_entrada:str, caminho_saida:str, novo_nome:str=None, atualizar:bool=False) -> None:
    """Novo nome sem a extenção."""
    if '.' in novo_nome:
        raise ValueError('Novo nome contem . ou a extenção precisa remover')
    with ZipFile(_get_pasta(caminho_entrada), 'r') as arquivo_zip:
        arquivo_zip.extractall(_get_pasta(caminho_saida))
    if not novo_nome is None:
        novo_arquivo = novo_nome + f'.{arquivo_zip.namelist()[0].split(".")[-1]}'
        if not _existe(caminho_saida + [novo_arquivo]):
            rename(_get_pasta(caminho_saida + ['files'] + [arquivo_zip.namelist()[0].split('/')[1]]), 
                _get_pasta(caminho_saida + [novo_arquivo]))
        else:
            if atualizar:
                print(_get_pasta(caminho_saida + [novo_arquivo]))
                remove(_get_pasta(caminho_saida + [novo_arquivo]))
                sleep(0.2)
                _extrair_zip(caminho_entrada, caminho_saida, novo_nome, False)
    remove(_get_pasta(caminho_saida + ['files']))

# _extrair_zip(['agfa_embalagens.zip'], ['saida_zip'], novo_nome='arquivo_123', atualizar=True)
    





    



    
    

    
