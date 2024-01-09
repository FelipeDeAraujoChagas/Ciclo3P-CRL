from datetime import datetime
import numpy as np
#from src.aut_tms_ux import AutomacaoTmsUX
import pandas as pd
from data.data_base_sql import DataBaseSQL
from utils.func_aux import FuncoesAux
import re
#from unidecode import unidecode


class FormatacaoCarteiraTMS:

    def __init__(self, caminhoArquivo) -> None:

        if caminhoArquivo is None:
            self.caminho_pasta = 'arquivos 3p\CICLO_ 9.xlsx'
        else:
            self.caminho_pasta = caminhoArquivo
        pass

    def analise_ciclo_antigo(self):
        """realiza os filtros dentro da carteira para consulta"""
        try:
            df_tms = pd.DataFrame(pd.read_excel(io=self.caminho_pasta, sheet_name='BD', skiprows=[0]))
            # print(df_tms)
        except Exception as e:
            print(e)
            raise Exception('Erro ao carregar dados')
        try:
            lista_pedidos = list(set(df_tms['Nro. Entrega'].astype(str).str.replace(".0", "").to_list()))
            return lista_pedidos
        except Exception as e:
            print(e)
            raise Exception('Erro ao carregar dados')

class FormatacaoCarteiraAsap:

    def __init__(self, caminhoArquivo):

        if caminhoArquivo is None:
            self.caminho_pasta = 'arquivos 3p\Base Validação (10).xlsx'
        else:
            self.caminho_pasta = caminhoArquivo
        pass

    def analise_carteira_asap(self):
        """realiza os filtros dentro do arquivo"""

        try:
                # df_asap = pd.DataFrame(pd.read_csv('arquivos 3p\Base Validação (10).csv',sep=";", encoding='latin-1'))
                df_asap = pd.DataFrame(pd.read_excel(self.caminho_pasta))
        except Exception as e:
            print(e)
            raise Exception('Erro ao carregar dados')
        
        try:    
                # import ipdb;ipdb.set_trace()
                regex = r'\b[A-Za-z]{2} - \d{1,4} - .*?\b'
                df_asap['Nome Filial'] = df_asap['Nome Filial'].astype(str)
                df_asap = df_asap[~df_asap['Nome Filial'].str.contains(regex, regex=True) |
                                   ~df_asap['Nome Filial'].str.contains('mini hub', case=False)]
        except Exception as e:
            print(e)
            raise Exception('Erro Filtrar dados da carteira Asap')
        try:    
                lista_pedidos = list(set(df_asap['Nro. Entrega'].astype(str).str.replace(".0", "").to_list()))
                return lista_pedidos
        except Exception as e:
            print(e)
            raise Exception('Erro Filtrar dados da carteira Asap')

class FormatacaoFullfilmentPedidos:
    def __init__(self, caminhoArquivo=None) -> None:

        if caminhoArquivo is None:
            self.caminho_pasta = 'arquivos 3p\Fullfilment_formatado_07_12.xlsx'
        else:
            self.caminho_pasta = caminhoArquivo
        pass

    def analise_fullfilment(self):
        try:
            try:
                # df_full = pd.DataFrame(pd.read_csv('Fullfilment_formatado.csv',sep=";", encoding='latin-1'))
                df_full = pd.DataFrame(pd.read_excel(self.caminho_pasta))
                df_full = df_full[~df_full['Ponto Pedido'].isin(['Cancelado', 'Entregue'])]
            except Exception as e:
                print(e)
                raise Exception('Erro ao carregar dados')
            
            try:
                # df_full.to_csv('saida_Fullfilment.csv',sep=";",encoding='latin-1', index=False)
                lista_pedidos = list(set(df_full['Entrega'].astype(str).str.replace(".0","").to_list()))
                return lista_pedidos
            except Exception as e:
                print(e)
                raise Exception('Erro na finalização do processo') 
            
        except Exception as e:
            raise Exception(e)


class FormatacaoCarteiraPedidos:

    def __init__(self, caminhoArquivo = None) -> None:

        if caminhoArquivo is None:
            self.path_arquivo = 'arquivos 3p\data_formatado_07_12.xlsx'
        else:
            self.path_arquivo = caminhoArquivo

        self.colunas = [
            'DIA DA BASE', 'Status Geral', 'Modelo de Operação', 'Pedido/Entrega', 
            'Pedido/Lojista', 'Dias', 'Aging Cliente', 'Etiqueta', 'Plataforma', 
            'Entrega TMS', 'Subcontratada', 'ASAP', 'Modal TMS', 'UF', 'Região Tarifária', 
            'Status correios', 'Data Correios', 'Motivo de atraso', 'SITUAÇÃO ', 'STATUS', 
            'Subclassificação', 'STATUS TMS', 'DATA', 'PENDENCIA', 'DATA ENTREGA', 'Retorno time', 
            'Previsão', 'Controlador', 'POSTADO POR FORA', 'Código de rastreio', 'Manteve?', 'Motivo', 'Obs.:', 
            ]

        self.lista_aux = list

    def insere_novo_status_pedido(self, lista_pontos: list):
        """insere no depara o  ponto atualizado"""
        if lista_pontos:

            bd = DataBaseSQL()
            sql_insert: str = """
                INSERT INTO Tbl_De_Para_Pedidos_Mongo (EMG_Status_Pedido, EMG_Descricao, EMG_Classificacao)
                SELECT '{}','{}', '{}'
                WHERE NOT EXISTS (
                    SELECT 1
                    FROM Tbl_De_Para_Pedidos_Mongo
                    WHERE EMG_Status_Pedido = '{}');
            """
            for pontos in lista_pontos:
                bd.insert_dados(sql_insert.format(pontos[0], pontos[1], 'NÃO DEFINIDO', pontos[0]))

    def insere_novo_lojista(self, lista_lojista: list):
        """insere no depara novo lojista"""
        try:
            if lista_lojista:
                bd = DataBaseSQL()
                padrao = ['ff', 'full', 'fullfilment']
                regex = re.compile('|'.join(padrao), flags=re.IGNORECASE)
                sql_insert: str = """
                    INSERT INTO Tbl_De_Para_Carteira_Lojista (CLJ_ID_Lojista, CLJ_Nome_Lojista, CLJ_Carteira_Lojista)
                    SELECT '{}','{}', '{}'
                    WHERE NOT EXISTS (
                        SELECT 1
                        FROM Tbl_De_Para_Carteira_Lojista
                        WHERE CLJ_ID_Lojista = '{}');
                """
                for lojista in lista_lojista:
                    f_lojista = str(lojista[1]).replace(__old='\'', __new='')
                    localizar = regex.findall(f_lojista)
                    if localizar:
                        bd.insert_dados(sql_insert.format(lojista[0], f_lojista, 'Full', lojista[0]))
                    else:
                        bd.insert_dados(sql_insert.format(lojista[0], f_lojista, 'Envvias', lojista[0]))

        except Exception as e:
            print(e)
            raise Exception(e)                

    def regra_sla(self, df: pd.DataFrame, col_inicial: str, col_saida: str, tipo: str = 'Int32'):
        """insere a regra dentro do dataframe"""
        try:
            # df[col_inicial] = df[col_inicial].astype(tipo, errors='ignore') 
            df[col_inicial] = pd.to_numeric(df[col_inicial], errors='coerce')

            df.loc[df[col_inicial].isna(), col_saida] = 'Sem ID'
            df.loc[df[col_inicial] < 0, col_saida] = 'Dentro do prazo'
            df.loc[df[col_inicial] == 0, col_saida] = 'Vence hoje'
            df.loc[df[col_inicial] == 1, col_saida] = '01.'
            df.loc[df[col_inicial] == 2, col_saida] = '02.'
            df.loc[df[col_inicial] == 3, col_saida] = '03.'
            df.loc[df[col_inicial].isin([4, 5]), col_saida] = '04 a 05.'
            df.loc[(df[col_inicial].isin([6, 7, 8, 9, 10])), col_saida] = '06 a 10.'
            df.loc[(df[col_inicial].isin([11, 12, 13, 14, 15])), col_saida] = '11 a 15.'
            df.loc[(df[col_inicial].isin([16, 17, 18, 19, 20])), col_saida] = '16 a 20.'
            df.loc[df[col_inicial] > 20, col_saida] = '20+'
            return df
        except Exception as e:
            print(f"Erro na função regra_sla\n{e}")
            raise Exception('Erro na função regra_sla')

    def dados_depara_lojista(self):
        """carraga os dados dos lojistas"""
        try:

            bd = DataBaseSQL()
            df_depara_lojista = bd.select_dados("""SELECT * FROM Tbl_De_Para_Carteira_Lojista""")
            df_depara_lojista['CLJ_ID_Lojista'] = df_depara_lojista['CLJ_ID_Lojista'].str.replace(' ','').astype(int)
            dct_lojista = dict(zip(df_depara_lojista['CLJ_ID_Lojista'], df_depara_lojista['CLJ_Carteira_Lojista']))
            
            return dct_lojista
        except Exception as e:
            print(e)
            raise Exception('Erro ao carregar deparas')

    def dados_depara_pedidos_mongo(self):
        """carraga os dados dos pedidos mongo"""
        try:
            bd = DataBaseSQL()
            df_depara_mg = bd.select_dados("""SELECT * FROM Tbl_De_Para_Pedidos_Mongo""")
            df_depara_mg['EMG_Status_Pedido'] = df_depara_mg['EMG_Status_Pedido'].str.replace(' ','')
            dct_mg = dict(zip(df_depara_mg['EMG_Status_Pedido'], df_depara_mg['EMG_Classificacao']))
            
            return dct_mg
        except Exception as e:
            print(e)
            raise Exception('Erro ao carregar deparas')

    def analise_carteira(self):
        try:
            try:
                # df_carteira = pd.DataFrame(pd.read_csv('data_formatado.csv',sep=";", encoding='latin-1'))
                df_carteira = pd.DataFrame(pd.read_excel(self.path_arquivo))
                df_carteira = df_carteira.drop_duplicates(['CdEntregaPedidoSite'])
            except Exception as e:
                print(e)
                raise Exception('Erro ao carregar dados')
            
            try:
              
                dct_lojista = self.dados_depara_lojista()
                # criando colunas auxiliar
                for col in self.colunas:
                    df_carteira[col] = ''

            except Exception as e:
                print(e)
                raise Exception('Erro ao carregar deparas')

            try:

                condicao = df_carteira['StEntregaPedidoMongo'] == ''
                dados = df_carteira.loc[condicao.fillna(False), ['StEntregaPedidoSite', 'DsSituaçãoAgrupada']].values
                # atualizado depara
                df_aux: pd.DataFrame = df_carteira.loc[condicao]
                self.lista_aux = list(zip(df_aux['StEntregaPedidoSite'], df_aux['DsSituaçãoAgrupada']))
                self.insere_novo_status_pedido(self.lista_aux)
                df_carteira.loc[condicao.fillna(False), ['StEntregaPedidoMongo', 'DsSituacaoEntregaPedidoMongo']] = dados

            except Exception as e:
                print(e)
                raise Exception('Erro na analise baisca de coluna')

            try:
                # inserção de analises
                df_carteira['DIA DA BASE'] = datetime.now().date().strftime('%d/%m/%Y')
                df_carteira['Pedido/Lojista'] = df_carteira['CdPedidoSite'].astype(str) + df_carteira['NmLojista'].astype(str)
                
                # df_carteira['DhPrevisaoEntrega'] = df_carteira['DhPrevisaoEntrega'].astype('datetime64[D]')
                df_carteira['DhPrevisaoEntrega'] = pd.to_datetime(df_carteira['DhPrevisaoEntrega'])
                df_carteira['Aging SLA'] = (pd.to_datetime(datetime.now().date()) - df_carteira['DhPrevisaoEntrega']).dt.days
                df_carteira['Aging SLA'] = df_carteira['Aging SLA'].astype('Int32', errors='ignore')  

            except Exception as e:
                print(e)
                raise Exception('Erro na analise baisca de coluna')
            
            try:
                df_carteira = self.regra_sla(df_carteira, 'Aging SLA', 'Faixa_Aging')
                
            except Exception as e:
                print(e)
                raise Exception('e')


            try:
                dct_mg =  self.dados_depara_pedidos_mongo()
                # definição status geral
                df_carteira['Status Geral'] = df_carteira['StEntregaPedidoMongo'].map(dct_mg)
            except Exception as e:
                print(e)
                raise Exception('Erro ao carregar deparas')

            try:
                df_carteira['Modelo de Operação'] = df_carteira['IdLojista'].map(dct_lojista)

                # atualizado depara
                condicao = (~df_carteira['Modelo de Operação'].isin(['Full', 'Envvias']))
                df_aux: pd.DataFrame = df_carteira.loc[condicao]
                lista_aux = list(zip(df_aux['IdLojista'], df_aux['NmLojista']))
                self.insere_novo_lojista(lista_aux)
                dct_lojista = self.dados_depara_lojista()
                # atualiza novamente os lojistas
                df_carteira['Modelo de Operação'] = df_carteira['IdLojista'].map(dct_lojista)

            except Exception as e:
                print(e)
                raise Exception('Erro na analise baisca de coluna')

            try:
                # verificar se o pedido é duplicado ou unico
                df_carteira['Pedido/Entrega'] = df_carteira.duplicated(subset=['CdPedidoSite', 'NmLojista', 'StEntregaPedidoMongo'], keep=False)
                df_carteira['Pedido/Entrega'] = df_carteira['Pedido/Entrega'].map({True: 'Duplicado', False: 'Unico'})
            except Exception as e:
                print(e)
                raise Exception('Erro na analise baisca de coluna 2')

            try:
                # calculo de sla desconsiderando feriados
                fnc = FuncoesAux()
                lista_datas = fnc.definicao_feriados()
                df_carteira['DhPrevisaoEntrega'] = df_carteira['DhPrevisaoEntrega'].replace('-', np.nan)
                df_carteira['DhPrevisaoEntrega'] = pd.to_datetime(df_carteira['DhPrevisaoEntrega'], format='%d/%m/%Y', errors='coerce')
                valid_dates = df_carteira['DhPrevisaoEntrega'].notnull()
                data_inicial = np.array(df_carteira.loc[valid_dates, 'DhPrevisaoEntrega'].values.astype('datetime64[D]'))
                df_carteira.loc[valid_dates, 'Dias'] = np.busday_count(data_inicial, datetime.now().date(), holidays=lista_datas)

            except Exception as e:
                print(e)
                raise Exception('Erro na definição de feriados')
            
            try:
                # df_carteira.to_csv('saida_carteira_1.csv',sep=";",encoding='latin-1', index=False, errors='ignore')
                df_carteira = self.regra_sla(df_carteira, 'Dias', 'Aging Cliente')
            except Exception as e:
                print(e)
                raise Exception(e)
            
            try:
                df_carteira.to_csv(path_or_buf='saida_carteira.csv', sep=";",
                                   encoding='latin-1', index=False, errors='ignore')
                lista_pedidos = list(set(df_carteira['CdEntregaPedidoSite'].astype(str).str.replace(".0","").to_list()))
                return lista_pedidos
            except Exception as e:
                print(e)
                raise Exception('Erro na finalização do processo')
            
        except Exception as e:
            raise Exception(e)
