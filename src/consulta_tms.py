from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import os
import re
import time

import pandas as pd
from src.aut_tms_ux import AutomacaoTmsUX
from utils.func_aux import FuncoesAux


fnc = FuncoesAux()
dir_download_temp = os.path.join(os.getcwd(), 'temp')

def consulta_tms_docs(dados: dict):
    """executa processo de consulta"""
    pasta_aux = f'pasta_aux_{dados["num_lista"]}'
    nova_pasta = fnc.criar_pasta(dir_download_temp, pasta_aux)
    contador = 0
    # type: ignore
    web = AutomacaoTmsUX(nova_pasta)
    while True:
        
        resultado = web.tela_consulta_documento(dados)
        if resultado['status'] ==  'sucesso':
            return resultado
        if contador > 3:
            return resultado
        contador += 1

def dados_consulta_doc(lista_documentos: list = [], max_doc: int = 0):
    """prepara os dados para consulta"""
    
    # dire = r'C:\Users\2103896595\Documents\BACKUP PYTHON\base_ciclo\saida.xlsx'
    # df = pd.DataFrame(pd.read_excel(dire))  
    # lista_pedidos = df['Documento_tms'].to_list()
    fnc = FuncoesAux()   
    lista = fnc.formatacao_numero_doc(lista_documentos, max_doc)
    return lista

def executar_processo_consulta(dados_dict: dict):
    """executa o processo de consulta dos documentos"""
    try:
        dados: list = dados_consulta_doc(dados_dict['lista_pedidos'], int(dados_dict['max_volumes'])) # type: ignore
        resultados: list = []

        fnc.remover_arquivo(dir_download_temp,'entregas_consulta')
        fnc.remover_pastas(dir_download_temp)
        print('#'*100)
        print(f'Total de Execuções: {len(dados)}')
        print('#'*100)

        # cria a thread para execução
        executor = ThreadPoolExecutor(max_workers=len(dados))

        # executa as threads
        for dado in dados:
            time.sleep(2)
            resultados.append(executor.submit(consulta_tms_docs, dado))

        # lista o resultado das consultas
        with open('teste.txt','w') as log:  
            for resultado in resultados:
                for dct in resultado.result():
                    if dct != 'volumes':
                        texto = f'{dct}: {resultado.result()[dct]}\n'
                        print(texto)
                        log.write(texto)

        # aguarda todas as execuções serem concluidas
        executor.shutdown(wait=True)

        # cria o arquivo de saida
        dire = dados_dict['dir_saida']
        df_tms: pd.DataFrame = fnc.concatenar_arquivos_csv(dir_download_temp, nome_arquivo='entregas_consulta') # type: ignore
        df_tms['N° Pedido'] = df_tms['N° Pedido'].apply(lambda x: re.sub("\\=|\"", "", str(x)) if str(x)[0] == "=" else x)
        retorno_tms: pd.DataFrame = df_tms[['N° Pedido', 'Sigla Unidade Entrega', 'Status', 'Ult. Romaneio', 'Sigla Unidade Atual']]
        retorno_tms = retorno_tms.drop_duplicates('N° Pedido')
        #         .to_csv(dire, sep=';', encoding='latin-1', index=False)
        # retorno_tms.to_excel('saida_tms.xlsx')
        return retorno_tms
    except Exception as e:
        print('Erro ao gerar arquivo de saída.', e)
        raise Exception('Erro ao gerar o arquivo')
    

if __name__ == '__main__':

    dados_dict = {
        'dir_saida': r'C:\\Users\\2103896595\\Desktop\\pedidos_tms_ux.csv',
        'max_volumes': 1500,
        'lista_pedidos': []
    }

    executar_processo_consulta(dados_dict)