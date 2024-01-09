import csv
from datetime import datetime, timedelta
import os
from pathlib import Path
import re
import shutil
import time
from tkinter.filedialog import askdirectory, askopenfilename
#from typing import Dict, Type
from loguru import logger
#import pandas as pd
from tkinter import Tk, messagebox
#from tkinter import StringVar, Tk, messagebox
from PIL import Image, ImageTk
import glob
import pandas as pd
from unidecode import unidecode
from workadays import workdays as wd
import numpy as np


class FuncoesAux:

    def definicao_feriados(self):
        """cria lista de feriados para analise""" 


        # definição de feriados
        lista_datas = [date for date in wd.get_holidays(country='BR', state='SP', years=range(2020, (datetime.now().year + 1)))]
        # data = {'data': lista_datas}
        # df = pd.DataFrame(data)
        # df['data'] = pd.to_datetime(df['data']).dt.strftime('%d/%m/%Y')
        # df.to_excel('saida_feriado.xlsx')
        lista_datas = pd.to_datetime(lista_datas)
        df_feriados = np.array(lista_datas.values.astype('datetime64[D]'))

        return df_feriados 

    def concatenar_arquivos_csv_massivo(self, diretorio: str, salvar_em: str, nome_arquivo: str):

        try:

            # Localizar todos os arquivos .xls no diretório que contenham o nome específico
            arquivos_xls = [arquivo for arquivo in glob.glob(os.path.join(diretorio, f'*{nome_arquivo}*.csv'))]

            # Verificar se existem arquivos correspondentes
            if not arquivos_xls:

                print(f"Nenhum arquivo com o nome '{nome_arquivo}' encontrado.")

            else:
                # Criar uma lista para armazenar os DataFrames dos arquivos correspondentes
                dataframes = []

                # Loop para ler cada arquivo correspondente e armazená-lo na lista
                for arquivo in arquivos_xls:
                    df = pd.read_csv(arquivo, sep=';', encoding='latin-1', low_memory=False)
                    dataframes.append(df)

                # Combinar os DataFrames em um único DataFrame
                df_final = pd.concat(dataframes, ignore_index=True)
                return df_final

                # data_hora = datetime.now()
                # data_format = data_hora.strftime('%d%m%Y_%H%M%S')
                # # Salvar o DataFrame combinado em um novo arquivo .xls
                # arquivo_saida = salvar_em + '//' + f'consolidado_{nome_arquivo}_{data_format}.csv'
                # df_final.to_csv(arquivo_saida, sep=";", index=False, encoding='latin-1')


                #print(f"Arquivos com o nome '{nome_arquivo}' combinados e salvos como {arquivo_saida}")

        except Exception as e:
            raise Exception(f'Erro ao gerar arquivo {e}')

    def concatenar_arquivos_csv(self, dir_download, nome_arquivo):  # type: ignore
        """Concatena os arquivos gerados em csv"""
        df_arquivo = pd.DataFrame()
        df_arquivo_final = pd.DataFrame()

        try:
            directory = Path(dir_download)
            lista_df = []

            files = directory.glob(pattern='*.*')
            for file in files:

                if nome_arquivo in str(file):
                    df_arquivo = pd.read_csv(str(file), sep=';', encoding='latin-1', index_col=None, memory_map=True, decimal=',')
                    lista_df.append(df_arquivo)

            if lista_df:

                df_arquivo_final = pd.concat(lista_df, ignore_index=True)  # type: ignore
                
            return df_arquivo_final  # type: ignore

        except Exception as e:
            logger.error(e)
    
    def carrega_arquivo_para_df(self, arquivo):
        """carrega um arquivo de um diretorio e o converte em um dataframe"""
        try:
            df = pd.DataFrame(pd.read_excel(arquivo))
            return df
        except AttributeError as x:
            messagebox.showwarning('Erro',f'Não foi possivel carregar o arquivo!!\n Verifique se o arquivo possui a aba "Base".\n{x}')
        except Exception as e:
            messagebox.showerror('Erro',f'Ocorreu um erro ao gerar o arquivo em excel\n{e}')
            print(e)

    def selecao_de_de_arquivo(self):
        """Menu para seleção de arquivo"""
        try:
            print('Insira o caminho do arquivo com os pedidos STD')
            opc = str(input('continuar? s/n: '))

            if opc in 'Ss':
                print('Aguardando seleção de Arquivo . . .')
                print("#"*50) 
                diretorio = askopenfilename()
                print(f'Arquivo Selecionado: {diretorio}\n\n')
                print("#"*50) 
                
                if diretorio == "":
                    return ""
                elif os.path.exists(diretorio):
                    return diretorio
                
        except Exception as e:
            messagebox.showerror('Erro','Não foi Possivel Selecionaro arquivo!')
            raise Exception(e)

    def cria_arquivo_csv_temp(self, df_: pd.DataFrame):
        """converte dataframes em aquivos temporarios para uso dentro das tabelas"""
        try:
            dir_temp = os.path.join(os.getcwd(),'temp')
            self.remover_arquivo(dir_temp, '.')
            arq_temp = dir_temp + '\\arquivo_temp.csv'
            self.gera_arquivo_csv(arq_temp, df_)
            return arq_temp
        except Exception as e:
            raise Exception(e)
        
    def gera_arquivo_csv(self, caminho, data: pd.DataFrame):
        """gera um arquivo csv de um dataframe"""
        try:
            data.to_csv(caminho, sep=';',index=False, encoding='latin-1',errors='ignore')
        except Exception as e:
            print(e)

    def gera_arquivo_excel(self, caminho, data:pd.DataFrame):
        """gera um arquivo excel apartir de um data frame"""
        try:
            data.to_excel(caminho,sheet_name='Base',index=False)
        except Exception as e:
            messagebox.showerror('Erro',f'Erro ao gerar saida do arquivo!\n{e}')

    def remover_arquivo(self, dir_download_file, nome_arquivo):
        """Remove os arquivos dentro da pasta"""
        try:

            listagem_arquivos = Path(dir_download_file)
            arquivos = listagem_arquivos.glob(pattern='*.*')

            for arquivo in arquivos:
                if nome_arquivo in str(arquivo):
                        os.remove(arquivo)

        except Exception as e:
            print(f'erro{e}')
    
    def gerar_imagem(self, diretorio, width: int, height: int):
        """Carrega a imagem e formata seus parametros de tamanho"""
        try:
            img= (Image.open(diretorio))
            resized_image= img.resize((width, height), Image.ANTIALIAS)
            return ImageTk.PhotoImage(resized_image) 
        except Exception as e:
            messagebox.showerror('Erro',f'Não foi possivel gerar a imagem!\n{e}')
    
    def ajusta_colunas_para_int(self, df: pd.DataFrame):
        """verifica as colunas e retira os valores float"""
        try:
            colunas = df.columns
            for coluna in colunas:

                if not (df[coluna].dtypes.name == 'object'):
                    df[coluna] = df[coluna].astype(str).apply(lambda x: x.replace('.0', '')).replace('nan',"")
                    df[coluna].fillna("",inplace=True)
                
            return df
        except Exception as e:
            messagebox.showerror('Erro',f'Não foi possivel alterar o tipo da coluna!\n{e}')

    def carrega_arquivo_csv_df(self, arquivo):
        """converte um arquivo csv para dataframe"""
        try:
            return pd.DataFrame(pd.read_csv(arquivo, sep=';',encoding='latin-1')) #type:ignore
        except Exception as e:
            messagebox.showerror('Erro',f'Não foi possivel atualizar os dados!\n{e}')
            raise Exception(e)

    def define_diretorio(self, tipo: str = 'dir'):

        """defini o diretorio ou caminho de um arquivo"""

        try:

            filetypes = (
                        ('text files', '*.xlsx'),
                        ('All files', '*.*')
                        )
            if tipo == 'dir':
                diretorio = askdirectory()
                if not os.path.isdir(diretorio):
                    messagebox.showerror('Erro','Diretório não Existe!\nVerifique e tente novamente.')
                    return ''
                return diretorio
            else:
                return askopenfilename(filetypes=filetypes)  # type: ignore

            #if diretorio:
            #    campo.set(diretorio)  # type: ignore
        except Exception as e:
            messagebox.showerror('Erro',f'Não foi possivel definir o Diretorio/Arquivo!\n{e}')

    def exporta_arquivo_saida(self, dados: dict, nome_arquivo: str, diretorio: str):

        if not nome_arquivo: nome_arquivo = 'BD_SAIDA'
        data_exec = datetime.now().strftime("%d%m%Y%H%M%S")
        data_dia = datetime.now().strftime("%d.%m")
        nome_arquivo_saida = diretorio + f'\\{nome_arquivo} {data_dia}_' + data_exec + '.xlsx'

        try:
            cont = 0
            modo = 'w'
            for sht_name, df in dados.items():
                if cont > 0: modo = 'a'
                self.gera_arquivo_excel_com_abas(nome_arquivo_saida, df, sht_name, modo)  # type: ignore
                cont += 1
            # messagebox.showinfo('Sucesso','Processo Concluido!')
        except Exception as e:
            raise Exception('Erro ao gerar arquivo Conjunto')

    def gera_arquivo_excel_com_abas(self,caminho, data: pd.DataFrame, sheet_name, modo: str = 'w'):
        """cria arquivo excel com varias abas"""
        try:
            # saida de dados em excel 
            
            with pd.ExcelWriter(caminho, mode = modo) as writer:  # type: ignore
                data.to_excel(writer, index=False, sheet_name=sheet_name)

        except Exception as e:
            raise Exception(f'Erro ao gerar arquivo{e}')

    def abrir_arquivo(self):
        """função responsavel em abrir o caminho do arquivo"""
        try:
            filetypes = (
                ('text files', '*.xlsx'),
                ('All files', '*.*')
            )
            caminho = askopenfilename(filetypes=filetypes)
            if os.path.isfile(caminho):
                return caminho
        except Exception as e:
            raise Exception(e)

    def mostra_senha(self, campo: Tk):
        """mostra a senha oculta"""
        try:
            if campo.cget('show') == '':
                campo.config(show='•')  # type: ignore
            else:
                campo.config(show='')   # type: ignore
        except:
            pass

    def alterar_formato_data(self, data, tipo):
        """altera o tipo de data de acordo com o parametro"""

        if tipo == 'texto':
            data_convert = datetime.strptime(data, "%d/%m/%Y")
            return datetime.strftime(data_convert, "%Y-%m-%d")
            
    def carrega_lista_colunas_bd(self, tipo: int = 1):
        """carrega as colunas """
        if tipo == 1:
            return [
                    'id',
                    'estado',
                    'aberto',
                    'pai',
                    'tipo_servico',
                    'codigo_servico',
                    'status_cortesia',
                    'valor_total',
                    'matricula_do_solic',
                    'filial_para_atendimento',
                    'telefone_cel_solicitante',
                    'descricao',
                    'pim',
                    'status_pim',
                    'status_chamado',
                    'data'
                ]   
        else:
            return [
                    'id',
                    'CHAMADO',
                    'COLUNA',
                    'ITEM',
                    'DESCRICAO',
                    'QTDE',
                    'STATUS_MTG',
                    'VAL_UNIT',
                    'VAL_TOTAL',
                    'STATUS_ERRO',
                    'DATA'

            ]
    
    def alterar_dados_tabela(self, table, sep=None):
        """Export table data to a comma separated file"""
        
        import platform
        dir_temp = os.path.join(os.getcwd(),'temp')
        self.remover_arquivo(dir_temp, '.')
        arq_temp = dir_temp + '\\arquivo_temp.csv'

        parent=table.parentframe
        if not arq_temp:
            return
        if sep == None:
            sep = ';'
        writer = csv.writer(open(arq_temp, "w"), delimiter=sep)
        model=table.getModel()
        recs = model.getAllCells()
        #take column labels as field names
        colnames = model.columnNames
        collabels = model.columnlabels
        row=[]
        for c in colnames:
            row.append(collabels[c])
        writer.writerow(row)
        for row in recs.keys():
            writer.writerow(recs[row])
        
        return arq_temp
    
    def procurar_pim_texto(self, texto: str):
        """extrai o pim do texto que esteja entre o texto inicio e o texto fim"""
        # texto = 'OPERAÇÃO EFETUADA - NR. DA MONTAGEM: 012548697 DATA DE MONTAGEM: 18.01.2023'

        regex = r'MONTAGEM:  0(.*?) DATA DE'

        pim = re.search(regex, texto)
        numero_pim = pim.group(1) #type: ignore
        if pim:
            return numero_pim
        return ''
    
    def corrige_texto(self, texto: str):
        """analisa cada carcter e vefifica se esta dentro do padrão ascii"""
        texto_ajustado: str = ''
        for caracter in texto:
            if ord(caracter) < 128:
                texto_ajustado += caracter
            else:
                texto_ajustado += ''
                
        return texto_ajustado
        
    def format_tel(self,telefone):
        """retira os caracteres do texto"""
        return re.sub(r'[^0-9]+', '', telefone)
    
    def format_descr(self,descricao):
        """retira os caracteres do texto"""
        try:
            padrao = re.compile(r'[^a-zA-Z0-9\s]')
            texto_formatado = re.sub(padrao, '', descricao.replace('\n', ' ').replace('\r', ' '))
            return texto_formatado
        except Exception as e:
            raise Exception('Erro ao converter descrição para formato válido')

    def formatacao_numero_doc(self, lista_doc: list, valor_max):
        """realiza a formatação e saparação por quantidade para consulta"""
        try:
            # retira caracteres indesejaveis
            # texto_formatado = re.sub(r"[^0-9,]", "", txt_volume)
            # divide o texto em lista com o caractere ","
            # lista_volume = texto_formatado.split(",")
            logger.debug(f'Total de volumes: {len(lista_doc)}')

            # sepera em grupos de acordo com a quantidade maxima
            nova_lista: list = []
            contador = 1
            for volume in range(0, len(lista_doc), int(valor_max)):
                lista = lista_doc[volume:volume+int(valor_max)]
                dict_volumes = {
                    'num_lista': contador,
                    'status': 'pendente',
                    'quantidade': len(lista),
                    'volumes': "\n".join(map(str, lista))
                }
                nova_lista.append(dict_volumes)
                contador += 1

            return nova_lista

        except Exception as e:
            messagebox.showerror(title='', message=f'{e}')
            print(e)

    def aguarda_download(self,caminho):

        fileends = "crdownload"
        logger.warning(f'Downloading em andamento aguarde...')

        while "crdownload" == fileends:
            time.sleep(1)
            newest_file = self.arquivo_recente(caminho)
            if "crdownload" in str(newest_file):  # type: ignore
                fileends = "crdownload"
            else:
                fileends = "none"
                logger.success('Downloading Completo...')    

    def arquivo_recente(self, caminho):

        data_criacao = lambda f: f.stat().st_ctime
        data_modificacao = lambda f: f.stat().st_mtime

        directory = Path(caminho)
        files = directory.glob(pattern='*.*')
        sorted_files = sorted(files, key=data_criacao, reverse=True)
        return sorted_files[0]  

    def remover_pastas(self, dir: str):
        """remove uma pasta dentro de um diretorio"""
        lista_pastas: list = os.listdir(dir) 

        if lista_pastas:
            for pasta in lista_pastas:
                diretorio = os.path.join(dir,pasta)
                if os.path.isdir(diretorio):
                    shutil.rmtree(diretorio)   

    def criar_pasta(self, dir: str, nome_pasta: str):
        """cria pastas dentro de um diretorio"""

        if os.path.exists(dir):
            novo_diretorio = os.path.join(dir, nome_pasta)
            os.mkdir(novo_diretorio)
            return novo_diretorio
        
    def mover_arquivo(self,dir_origem: str, dir_destino: str, nome_arquivo: str):
        """move arquivos para outro local"""
        try:
            for arq in os.listdir(dir_origem):
                if nome_arquivo in arq:
                    arquivo = os.path.join(dir_origem,arq)
                    destino = os.path.join(dir_destino,arq)
                    shutil.move(arquivo, destino)

        except Exception as e:
            raise Exception('Erro ao movimentar o arquivo')      

    def remover_arquivos(self, dir_origem: str, nome_arquivo):
        """remove um arquivo do diretório de origem"""
        try:
            for arq in os.listdir(dir_origem):
                if nome_arquivo in arq:
                    arquivo = os.path.join(dir_origem,arq)
                    os.remove(arquivo)
        except Exception as e:
            raise Exception('Não foi Possivel remover arquivo')

    def importar_excel_para_dataframe(self, diretorio, nome_aba):

        """carrega uma arquivo excel para dataframe"""

        df_arquivo = pd.DataFrame(pd.read_excel(diretorio, sheet_name=nome_aba))
        return df_arquivo

    def lista_colunas(self):
        """lista todas colunas no data frame"""
        return [
                'Transportador',
                'Entrega',
                'PV',
                'dsm',
                'Empresa',
                'Etiqueta',
                'filial',
                'nota',
                'serie',
                'Status Atual',
                'Data Status',
                'Observacao',
                'Previsao Entrega',
                'Numero Arquivo OCORREN',
                'valor Pedido',
                'Id Ocorrencia',
                'Descricao Ocorrencia',
                'Data Ocorrencia',
                'Etapa Pedido',
                'Dias Em Etapa',
                'Etapa Pedido Data Hora',
                'Horas em Etapa',
                'CCEP',
                'Cep',
                'Regional',
                'Distrito',
                'Bairro',
                'Cidade',
                'Uf',
                'uf Destino',
                'data Compra',
                'data Expedicao',
                'Dt Prometida',
                'Aging Prometida',
                'Prazo Cliente D0',
                'Data Prevista',
                'Data Ajustada',
                'Aging Ajustada',
                'Prazo Transportadora D0',
                'Unidade De Negocio',
                'Tipo Entrega',
                'Ordem Venda',
                'Nome da Transportadora',
                'Descricao Contrato',
                'Carga',
                'Gaiola',
                'danfe',
                'data Carga',
                'Data Ultima Ocorrência Interna',
                'Relacionamento',
                'CAE',
                'CPP',
                'Migrado',
                'periodo Entrega',
                'Solicitante Packing List',
                'Tempo em Etapa',
                'Tipo Entrega Descrição DBO',
                'Acao Venda',
                'gerente Regional',
                'Ultima Ocorrência Online Data/Hora Processamento',
                'Ultimo Insucesso Codigo',
                'Ultimo Insucesso Data',
                'Ultimo Insucesso Descricao',
                'Ultimo Processamento',
                'Responsavel',
                'Matriz Atuação',
                'Matriz Situação',
                'Modalidade VVLOG',
                'Alto Valor',
                # 'Tipo Reclamação',
                # 'Status',
                # 'Ult. Romaneio',
                # 'Sigla Unidade Atual'
                ]
    
    def localiza_diretorio(self):
        """seleção de arquivo"""
        try:
            dir_arquivo = askdirectory()
            if dir_arquivo:
                return dir_arquivo
            else:
                return
        except Exception as e:
            logger.error(e)

    def formatacao_numero_doc_ponto(self, qtd_doc: int, lista_doc: list):

        """realiza a formatação e saparação por quantidade para consulta criando dicionarios"""

        try:
            logger.debug(f'Total de volumes: {len(lista_doc)}')
            # sepera em grupos de acordo com a quantidade maxima
            nova_lista: list = []
            contador = 1
            for idx, volume in enumerate(range(0, len(lista_doc), qtd_doc)):


                lista = lista_doc[volume:volume+qtd_doc]
                concat_doc = ";\n".join(map(str, lista))

                dct_consulta: dict = {}
                dct_consulta['consulta'] =  f'Consulta {idx + 1}'
                dct_consulta['descricao'] =  ''
                dct_consulta['status'] =  'Pendente'
                dct_consulta['pedidos'] =  concat_doc

                nova_lista.append(dct_consulta.copy())
                contador += 1

            return nova_lista 
        except Exception as e:
           print(e)

    def formatacao_numero_doc_ponto_2(self, qtd_doc: int, lista_doc: list):
        """realiza a formatação e saparação por quantidade para consulta criando dicionarios"""
        try:
            logger.debug(f'Total de volumes: {len(lista_doc)}')
            # sepera em grupos de acordo com a quantidade maxima
            nova_lista: list = []
            contador = 1
            for idx, volume in enumerate(range(0, len(lista_doc), qtd_doc)):


                lista = lista_doc[volume:volume+qtd_doc]
                concat_doc = ";\n".join(map(str, lista))

                dct_consulta: dict = {}
                dct_consulta['consulta'] =  f'Consulta {idx + 1}'
                dct_consulta['descricao'] =  ''
                dct_consulta['status'] =  'inserindo_listagem'
                dct_consulta['pedidos'] =  concat_doc
                dct_consulta['id_web'] =  ''

                nova_lista.append(dct_consulta.copy())
                contador += 1

            return nova_lista 
        except Exception as e:
           print(e)

    def concatenar_arquivos(self, diretorio: str, salvar_em: str, nome_arquivo: str):
        try:

            # Localizar todos os arquivos .xls no diretório que contenham o nome específico
            arquivos_xls = [arquivo for arquivo in glob.glob(os.path.join(diretorio, f'*{nome_arquivo}*.xls'))]

            # Verificar se existem arquivos correspondentes
            if not arquivos_xls:
                print(f"Nenhum arquivo com o nome '{nome_arquivo}' encontrado.")
            else:
                # Criar uma lista para armazenar os DataFrames dos arquivos correspondentes
                dataframes = []

                # Loop para ler cada arquivo correspondente e armazená-lo na lista
                for arquivo in arquivos_xls:
                    df = pd.read_excel(arquivo, skiprows=[0])
                    dataframes.append(df)

                # Combinar os DataFrames em um único DataFrame
                df_final = pd.concat(dataframes, ignore_index=True)

                data_hora = datetime.now()
                data_format = data_hora.strftime('%d%m%Y_%H%M%S')
                # Salvar o DataFrame combinado em um novo arquivo .xls
                arquivo_saida = salvar_em + '//' + f'consolidado_{nome_arquivo}_{data_format}.csv'
                df_final.to_csv(arquivo_saida, sep=";", index=False, encoding='latin-1')

                print(f"Arquivos com o nome '{nome_arquivo}' combinados e salvos como {arquivo_saida}")
        except Exception as e:
            raise Exception(f'Erro ao gerar arquivo {e}')
        
    def calcular_data_excel(self, data_transp):
        """realiza o calculo de dias uteis"""
        try:
            if data_transp not in ['None', 'none', 'nan', None, 'NaT']:
                data_hoje = datetime.today().date()
                dias_uteis = 0
                data_transportador = datetime.strptime(data_transp,__format='%Y-%m-%d %H:%M:%S').date()

                while data_transportador > data_hoje:
                    if data_transportador.weekday() < 5:  # Verificar se o dia da semana não é sábado (5) ou domingo (6)
                        dias_uteis += 1
                    data_transportador -= timedelta(days=1)

                if dias_uteis <= 9 and dias_uteis > 0:
                    return "AT" + str(dias_uteis)
            return "-"
        except Exception as e:
            raise Exception(f'Erro ao realizar cálculos das datas.{e}')
        
    def remover_acentos_palavras(self, lista_palavras):

        palavras_sem_acentos = []

        for palavra in lista_palavras:
            palavra_sem_acentos = unidecode(palavra)
            palavras_sem_acentos.append(palavra_sem_acentos)

        return palavras_sem_acentos  

    def concatenar_arquivos_xls(self, diretorio, nome_arquivo):
        arquivos_xls = [arquivo for arquivo in os.listdir(diretorio) if arquivo.endswith(".xls") and arquivo.startswith(nome_arquivo)]
        
        if not arquivos_xls:
            raise ValueError(f"Nenhum arquivo .xls encontrado com o nome '{nome_arquivo}' no diretório '{diretorio}'.")

        dfs = []

        for arquivo_xls in arquivos_xls:
            caminho_arquivo = os.path.join(diretorio, arquivo_xls)
            df = pd.read_excel(caminho_arquivo, skiprows=[0])
            dfs.append(df)

        if len(dfs) > 1:
            dataframe_concatenado = pd.concat(dfs, ignore_index=True)
        else:
            dataframe_concatenado = dfs[0]

        return dataframe_concatenado
