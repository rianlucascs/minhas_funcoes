
"""
# S1RT6
28/12/23
https://www.linkedin.com/in/rian-lucas
"""

from os import getcwd, remove, mkdir, path, sep, name
from datetime import datetime
from subprocess import Popen, run
from time import sleep
from tkinter import filedialog
from pandas import read_csv, read_excel
from platform import system, version, platform
import json
from difflib import SequenceMatcher


def sistema_operacional():
    """Retorna o so."""
    sistemas = {'nt': 'windows', 'posix': 'mac'}
    if name in sistemas:
        return sistemas[name]
    if name not in sistemas.keys():
        raise ValueError('Sistema operacional diferente do esperado')

def sistema_parametros():
    """Retorna o caminho ate a pasta atual, encoding de arquivos e barra do so."""
    if len(sep) == 1:
        _sep = sep
        __sep = sep + sep
    if len(sep) == 2:
        _sep = sep[0]
        __sep = sep + sep
    if sistema_operacional() == 'windows':
        return getcwd().replace(_sep, __sep) + __sep, 'UTF-8', __sep
    elif sistema_operacional() == 'mac':
        return getcwd() + '/', 'ISO-8859-15', '/'

def get_parent_directory_path(levels_back=1):
    current_path = getcwd()
    parent_path = current_path
    for _ in range(levels_back):
        parent_path = path.dirname(parent_path)
    return parent_path

def encoding_sistema():
    if sistema_operacional() == 'windows':
        return 'UTF-8'
    if sistema_operacional() == 'mac':
        return 'ISO-8859-15'

def path_raiz(caminho=[]):
    """Retorna o caminho ate a pasta atual mais o arquivo ou pasta informado."""
    _str_caminho, _, barra = sistema_parametros()
    for i, elementos in enumerate(caminho):
        _str_caminho += elementos
        if i != len(caminho) -1:
            _str_caminho += barra
    return _str_caminho
    
# print(caminho_raiz(['logs']))

def existe(caminho):
    if path.exists(caminho):
        return True
    return False

def escrita(caminho, mensagem, atualizar=None, pular_linha=False, pular_escrita=False):
    if pular_escrita:
        return None
    if atualizar:
        if path.exists(caminho):
            remove(caminho)
    with open(caminho, 'a', encoding=sistema_parametros()[1]) as arquivo:
        if pular_linha:
            arquivo.write(mensagem + '\n')
        else:
            arquivo.write(mensagem)
    return None

def leitura(caminho, tipo):
    """Retorna a informacao do arquivo."""
    tipos = {'read': lambda arquivo: arquivo.read(), 'readlines': lambda arquivo: arquivo.readlines(),
             'json': lambda arquivo: json.load(arquivo)}
    with open(caminho, 'r', encoding=sistema_parametros()[1]) as arquivo:
        if tipo in tipos:
            return tipos[tipo](arquivo)

def leitura_simples(caminho, tipo):
    tipos = {'read': lambda arquivo: arquivo.read(), 'readlines': lambda arquivo: arquivo.readlines()}
    with open(caminho, 'r', encoding_sistema()) as arquivo:
        if tipo in tipos:
            return tipos[tipo](arquivo)
        
        
def informacao_existe(caminho, info):
    """Verifica se a informacao esta no arquivo."""
    arquivo = leitura(caminho, 'readlines')
    for linha in arquivo:
        for i in range(len(linha)):
            if info == linha[i:i+len(info)]:
                return True
    return False

def log_my(caminho, mensagem, tipo_log='INFO', atualizar=False, pular_linha=True, pular_escrita=False):
    """Escreve em arquivo de texto no formato log."""
    tempo = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    tup_log = {'INFO': f'[{tempo}] [INFO]', 'AVISO': f'[{tempo}] [AVISO]', 'ERRO': f'[{tempo}] [ERRO]'}
    if tipo_log in tup_log:
        escrita(caminho, f'{tup_log[tipo_log]} {mensagem}', atualizar, pular_linha, pular_escrita)
    else:
        raise TypeError('tipo_log tipo diferente do esperado')
    return None

from logging import basicConfig, getLogger, DEBUG
def log(caminho, mensagem):
    basicConfig(filename=caminho, level=DEBUG)
    log = getLogger()
    log.error(f'{mensagem}')
    return None

def terminal_exec(caminho, tipo_exec):
    """Executa python em um terminal."""
    if sistema_operacional() == 'windows':
        if tipo_exec == 'popen':
            Popen(['start', caminho], shell=True)
        elif tipo_exec == 'run':
            run(['cmd', '/c', 'start', caminho], shell=True)
    elif sistema_operacional() == 'mac':
        run(f'osascript -e \'tell application "Terminal" to do script "sh {caminho}"\'', shell=True)

def terminal_exec_dinamico(caminho_loc_py, caminho_loc_bat=None, caminho_loc_sh=None, atualizar=False, pular_escrita=False,
                   executar_em_seguida=False, excluir_em_seguida=False, local_log_execucao=None,
                   local_background=None):
    """Se 'so' for mac então informar caminho_loc_sh e local_background deve ser None."""
    so = sistema_operacional()
    if so == 'windows':
        escrita(caminho_loc_bat, f'cd {caminho_loc_py.replace(caminho_loc_py.split(sistema_parametros()[2])[-1], "")[:-1]}', atualizar, True, pular_escrita)
        escrita(caminho_loc_bat, f'python {caminho_loc_py.split(sistema_parametros()[2])[-1]}', False, False, pular_escrita)
    elif so == 'mac':
        escrita(caminho_loc_sh, f'cd {caminho_loc_py.replace(caminho_loc_py.split(sistema_parametros()[2])[-1], "")[:-1]}', atualizar, True, pular_escrita)
        escrita(caminho_loc_sh, f'python {caminho_loc_py.split(sistema_parametros()[2])[-1]}', False, False, pular_escrita)     
    if local_background != None:
        if so == 'windows':
            escrita(local_background, 'Set WshShell = CreateObject("WScript.shell")', atualizar, True, pular_escrita)
            escrita(local_background, f'WshShell.Run "{caminho_loc_bat}", 0', False, False, pular_escrita)
        elif so == 'mac':
            raise ValueError('background mac nao adicionado') from None
    if executar_em_seguida:
        if so == 'windows':
            if local_background != None:
                terminal_exec(local_background, 'run')
            else:
                terminal_exec(caminho_loc_bat, 'run')
        elif so == 'mac':
            if local_background != None:
                pass
            else:
                terminal_exec(caminho_loc_sh, 'run')
    sleep(0.2)
    if excluir_em_seguida:
        if local_background != None:
            remove(local_background)
        remove(caminho_loc_bat)
    if local_log_execucao != None: 
        log(local_log_execucao,
             f'{caminho_loc_py}, Atualizar: {atualizar}, Executar em seguida: {executar_em_seguida}, Excluir em seguida: {excluir_em_seguida}', 'INFO')

    return None

# if __name__ == '__main__':
#     terminal_exec_dinamico(caminho_raiz(['teste.py']), 
#                            caminho_raiz(['exec_teste.bat']), 
#                            atualizar=True, 
#                            executar_em_seguida=True, 
#                            excluir_em_seguida=True, 
#                            local_log_execucao=caminho_raiz(['log_teste.txt']), 
#                            local_background=caminho_raiz(['background.vbs']))

def atualiza_caminho_barra(caminho):
    if sistema_operacional() == 'windows':
        return caminho.replace(sep, sep+sep)
    return caminho

def leitura_dados(caminho=None, caixa_de_escolha=False, _sep=';', log_caminho=None, fillna=None):
    """Retorna o dataframe do arquivo .xlsx ou .csv"""
    # log_caminho informar o caminho onde vai ficar o registro do caminho selecionado ou escolhido
    if caixa_de_escolha:
        caminho = filedialog.askopenfilename()
    caminho = atualiza_caminho_barra(caminho)
    if not caixa_de_escolha and caminho is None:
        raise TypeError('Não informou o caminho')
    tup_tipo = {'xlsx': lambda caminho: read_excel(caminho),
                    'csv': lambda caminho: read_csv(caminho, encoding=sistema_parametros()[1], sep=_sep)}
    tipo_arquivo = caminho.split('.')[-1]
    if tipo_arquivo in tup_tipo:
        if log_caminho != None:
            escrita(atualiza_caminho_barra(log_caminho), caminho, True)
        if fillna != None:
            df = tup_tipo[tipo_arquivo](caminho).fillna(fillna)
        return df
    else:
        raise ValueError('Tipo arquivo diferente do esperado') from None


def remover_caracteries(string, letras=True, caracteries=False, numeros=False, novo_valor='', excecao='None'):
    # novo_valor e o que sera subistituido caso tenha o caracteries que sera removido
    # execao e o mesmo contendo sera permitido
    if type(string) != str:
        raise ValueError('Valor informado diferente de str.') from None
    if letras:
        tupla_acentos_minusculo = {'á': 'a', 'à': 'a', 'â': 'a', 'ã': 'a', 'é': 'e', 'ê': 'e', 'í': 'i', 'ó': 'o',
                                   'ô': 'o', 'õ': 'o', 'ú': 'u', 'ü': 'u', 'ç': 'c'}
        tupla_acentos_maiusculo = {'Á': 'A', 'À': 'A', 'Â': 'A', 'Ã': 'A', 'É': 'E', 'Ê': 'E', 'Í': 'I', 'Ó': 'O',
                                   'Ô': 'O', 'Õ': 'O', 'Ú': 'U', 'Ü': 'U', 'Ç': 'C'}
        for acentos in tupla_acentos_minusculo.keys():
            if acentos in string and not acentos in excecao:
                string = string.replace(acentos, tupla_acentos_minusculo[acentos])
        for acentos in tupla_acentos_maiusculo.keys():
            if acentos in string and not acentos in excecao:
                string = string.replace(acentos, tupla_acentos_maiusculo[acentos])
    if caracteries:
        caracteres = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '-', '=', '{', '}', '[', ']', '|',
                     '\\', ':', ';', '"', "'", '<', '>', ',', '.', '?', '/', '\t', '\n', '\r']
        for carac in caracteres:
            if carac in string and not carac in excecao:
                string = string.replace(carac, novo_valor)
    if numeros:
        lista_numeros = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        for num in lista_numeros:
            if num in string and not num in excecao:
                string = string.replace(num, novo_valor)
    return string

# print(remover_caracteries('avcsdefââasdasd & ', letras=True, caracteries=True, excecao='&'))

def calcular_semelhanca(string1, string2):
    return SequenceMatcher(None, str(string1).lower(), str(string2).lower()).ratio()

def registrar_info_sistema(caminho):
    """
    Cria um arquivo .txt contendo as informacoes do sistema operacional e, 
    caso ja exista, realiza uma verificacao de alteracoes.
    
    Return:
        bool: True = nao mudou
        bool: False  = mudou

    Obs:
        Verificar essa função em outro sistema operacional.
    """
    mensagem = f'{system()}\n{platform()}\n{version()}\n'
    if existe(caminho) is False:
        escrita(caminho, mensagem, False)
    else:
        arquivo = leitura(caminho, 'readlines')
        for linha in arquivo:
            if not linha[:-1] in [system(), platform(), version()]:
                return True
        remove(caminho)
        sleep(0.1)
        registrar_info_sistema(caminho)
        return False
    return None

def estabelecer_caminho_inteligente_script(caminho_arquivos_temporarios ):
    """
    Cria arquivo txt com o caminho da maquina ate o arquivo.

    Args:
        diretorio_temporario_path: caminho onde os arquivos temporários são 
        armazenados por este sistema.
    
    Obs:
        core_path: O conteudo sera sempre atualizado ao iniciar o algoritmo, 
        pois o cliente pode mover o arquivo para outro diretorio.
    """

    if '.' in caminho_arquivos_temporarios:
        raise TypeError('Nao informar o nome do arquivo que sera escrito.')
    
    bar = sistema_parametros()[2]
    caminho = caminho_arquivos_temporarios + bar + 'core_path'
    if existe(caminho) is False:
        mkdir(caminho_arquivos_temporarios + bar + 'core_path')
    sleep(0.1)
    if existe(caminho) is True:
        caminho = caminho_arquivos_temporarios + bar + 'core_path' + bar
        info_syst = registrar_info_sistema(caminho + 'so.txt')
        if info_syst == None:
            estabelecer_caminho_inteligente_script(caminho_arquivos_temporarios)
        if info_syst == False:
            escrita(caminho + 'core_path.txt', path_raiz([]), True)
    return None

# estabelecer_path_inteligente_script(path_raiz(['temp']))

# print(path_raiz([]))


    



    
    

    
