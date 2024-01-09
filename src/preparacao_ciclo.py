from datetime import date, datetime, timedelta
import re
import numpy as np
import pandas as pd
from data.data_base_sql import DataBaseSQL
# from pandas_market_calendars import get_calendar
# from numba import jit
from workadays import workdays as wd
from utils.func_aux import FuncoesAux

class FormatacaoBaseCiclo:

    def __init__(self, df_base: pd.DataFrame, df_carteira: pd.DataFrame) -> None:

        self.df_base = df_base
        self.df_carteira = df_carteira
        fnc = FuncoesAux()
        self.df_feriados = fnc.definicao_feriados()
        self.colunas = [
                    'Mês Refer.', 'Dias Prazo Atual', 'Prazo Atual', 'Aging Prazo Atual', 'ASAP',
                    'Modalidade', 'Análise entregue', 'Resumo', 'Situação', 'Teve sobreposição?',
                    'Modalidade_carteira', 'Ponto da carteira', 'Status Geral', 'ID Lojista', 'Nome Lojista',
                    'Data Prometida', 'Dias Prometida', 'Aging Prometida', 'Dias Ocorr.', 'Aging Processamento',
                    'Modal Corrigido', 'Apelido Corrigido', 'Etiqueta', 'Plataforma', 'Entrega TMS', 'Subcontratada',
                    'ASAP', 'Modal TMS', 'UF', 'Região Tarifária', 'Status correios', 'Data Correios',
            ]
        # self.analise_base_ciclo()

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
        
    def regra_aging_processamento(self, df: pd.DataFrame, col_inicial: str, col_saida: str, tipo: str = 'Int32'):
        """insere a regra dentro do dataframe"""
        try:
            df[col_inicial] = pd.to_numeric(df[col_inicial], errors='coerce')
            df.loc[df[col_inicial].isna(), col_saida] = 'Sem ID'
            df.loc[df[col_inicial] < 0, col_saida] = 'Dentro do prazo'
            df.loc[df[col_inicial] == 0, col_saida] = 'Hoje'
            df.loc[df[col_inicial] == 1, col_saida] = '01.'
            df.loc[df[col_inicial] == 2, col_saida] = '02.'
            df.loc[df[col_inicial] == 3, col_saida] = '03.'
            df.loc[df[col_inicial].isin([4, 5]), col_saida] = '04 a 05.'
            df.loc[(df[col_inicial].isin([6, 7, 8, 9, 10])), col_saida] = '06 a 10.'
            df.loc[(df[col_inicial].isin([11, 12, 13, 14, 15])), col_saida] = '11 a 15.'
            df.loc[(df[col_inicial].isin([16, 17, 18, 19, 20])), col_saida] = '16 a 20.'
            df.loc[(df[col_inicial] >= 21) & (df[col_inicial] <= 49), col_saida] = '21 a 49.'
            df.loc[(df[col_inicial] >= 50) & (df[col_inicial] <= 100), col_saida] = '50 a 100.'
            df.loc[df[col_inicial] > 100, col_saida] = '100+'
            return df
        except Exception as e:
            print(f"Erro na função regra_sla\n{e}")
            raise Exception('Erro na função regra_sla')

    def calcular_diferenca_dias_uteis(self, row):
        try:
            return wd.networkdays(start_date=pd.to_datetime(row['Dt. Prazo Atual']), end_date=datetime.now())
        except Exception as e:
            return None

    def insere_novas_filiais(self, lista_lojista: str):
        """insere no depara as filiais não cadastradas"""
        try:
            if lista_lojista:
                bd = DataBaseSQL()
                padrao = ['ff', 'full', 'fullfilment']
                regex = re.compile('|'.join(padrao), flags=re.IGNORECASE)
                sql_insert: str = """
                    INSERT INTO Tbl_De_Para_TMS_Lojista (TLT_Filial, TLT_Filial_Ajustada, TLT_Em_Analise, TLT_Nome_Na_Carteira, TLT_Modelo_De_Operacao)
                    SELECT '{}', '', '', '', '{}'
                    WHERE NOT EXISTS (
                        SELECT 1
                        FROM Tbl_De_Para_TMS_Lojista
                        WHERE TLT_Filial = '{}');
                """
                for lojista in lista_lojista:
                    lojista = lojista.replace('\'', '')
                    localizar = regex.findall(str(lojista).lower())
                    if localizar:
                        bd.insert_dados(sql_insert.format(lojista,'Full', lojista))
                    else:
                        bd.insert_dados(sql_insert.format(lojista,'Envvias', lojista))
        except Exception as e:
            print(e)
            raise Exception(e)

    def insere_pedido_erro(self, lista_pedidos: str): 
        """insere na tabela os pedidos com algum tipo de erro"""
        bd = DataBaseSQL()
        if lista_pedidos:
            for pedido in lista_pedidos:
                sql_insert = f"""
                    INSERT INTO Tbl_Pedidos_Com_Erro (PCE_Pedido, PCE_Motivo)
                    SELECT '{pedido}', 'Cancelado'
                    WHERE NOT EXISTS (
                        SELECT 1
                        FROM Tbl_Pedidos_Com_Erro
                        WHERE PCE_Pedido = '{pedido}');
                """
                bd.insert_dados(sql_insert)

    def dados_depara_nome_lojista(self):
        """carraga os dados dos lojistas"""
        try:
            bd = DataBaseSQL()
            df_depara_lojista = bd.select_dados("""SELECT * FROM Tbl_De_Para_TMS_Lojista""")
            dct_nome_lojista = dict(zip(df_depara_lojista['TLT_Filial'], df_depara_lojista['TLT_Modelo_De_Operacao']))
            
            return dct_nome_lojista
        except Exception as e:
            print(e)
            raise Exception('Erro ao carregar deparas')

    def analise_base_ciclo(self):
        """analisa a base gerada"""
        try:

            try:
                self.df_base = self.df_base.drop_duplicates(['Nro. Entrega'])
                # formatação de colunas
                for col in self.colunas:
                    self.df_base[col] = ''

                self.df_base['Chave NFe'] = self.df_base['Chave NFe'].apply(lambda x: f"'{x}")
                lista = self.df_base.columns.to_list()

            except Exception as e:

                print(e)
                raise Exception('Erro de formatação')
            
            try:

                self.df_base['Dt. Cadastro'] = pd.to_datetime(self.df_base['Dt. Cadastro'], format='%d/%m/%Y', errors='coerce')
                self.df_base['Mês Refer.'] = self.df_base['Dt. Cadastro'].dt.strftime('%m/%Y')

                #self.df_base['Mês Refer.'] = self.df_base['Dt. Cadastro'].astype('datetime64[D]').dt.strftime("%b-%y")
                # self.df_base['Mês Refer.'] = self.df_base['Mês Refer.'].astype(str).upper()
            except Exception as e:
                print(e)
                raise Exception('Erro de formatação')
            try:
                
                # campos vazios inserir a data atual
                # self.df_base['Dt. Prazo Atual'] = self.df_base['Dt. Prazo Atual'].replace('-', np.nan)
                self.df_base['Dt. Prazo Atual'] = self.df_base['Dt. Prazo Atual'].replace('-', pd.to_datetime(datetime.now().date()))
                self.df_base['Dt. Prazo Atual'] = pd.to_datetime(self.df_base['Dt. Prazo Atual'], format='%d/%m/%Y', errors='coerce')
                valid_dates = self.df_base['Dt. Prazo Atual'].notnull()
                data_inicial = np.array(self.df_base.loc[valid_dates, 'Dt. Prazo Atual'].values.astype('datetime64[D]'))
                self.df_base.loc[valid_dates, 'Dias Prazo Atual'] = np.busday_count(data_inicial, datetime.now().date(), holidays=self.df_feriados)

            except Exception as e:
                print(e)
                raise Exception('Erro na definição Dias Prazo Atual')
            
            try:

                self.df_base.loc[pd.to_datetime(self.df_base['Dt. Prazo Atual']) < datetime.now(), 'Prazo Atual'] = 'Fora do Prazo'
                self.df_base.loc[pd.to_datetime(self.df_base['Dt. Prazo Atual']) >= datetime.now(), 'Prazo Atual'] = 'Dentro do Prazo'
                
            except Exception as e:
                print(e)
                raise Exception('Erro na definição de feriados')
            
            try:
                self.df_base = self.regra_sla(self.df_base, col_inicial='Dias Prazo Atual', col_saida='Aging Prazo Atual')
                
            except Exception as e:
                print(e)
                raise Exception('Erro na definição de feriados')

            try:

                bd = DataBaseSQL()
                df_depara_modalidade = bd.select_dados("""SELECT * FROM Tbl_Transportador_Modalidade_Ciclo""")
                self.df_base = self.df_base.merge(df_depara_modalidade, left_on='Sigla Unidade Entrega', right_on='TRM_Unidade_Entrega', how='left')
                self.df_base['ASAP'] = self.df_base['TRM_Transportadora'] # TODO: verificar se existem campos em branco inserir transp COL(sigla Unidade Entrega)
                self.df_base['Modalidade'] = self.df_base['TRM_Modalidade']
                self.df_base['Apelido Corrigido'] = self.df_base['TRM_Apelido']

                df_depara_pendecia = bd.select_dados("""SELECT * FROM Tbl_Ultima_Pendencia_Ciclo""")
                self.df_base = self.df_base.merge(df_depara_pendecia, left_on='Últ. Pendência', right_on='UPC_Ultima_Pendencia', how='left')

                df_depara_status = bd.select_dados("""SELECT * FROM Tbl_Status_Entrega_Ciclo""")
                self.df_base = self.df_base.merge(df_depara_status, left_on='Status', right_on='SEC_Status', how='left')

                # self.df_base.to_csv('saida_ciclo.csv',sep=';', index=False, encoding='latin-1')

            except Exception as e:
                print(e)
                raise Exception('Erro ao carregar deparas')
            
            
            try:
                self.df_base.loc[(self.df_base['Status'] == 'PENDENTE'), 'Resumo'] = self.df_base['UPC_Resumo']
                self.df_base.loc[(self.df_base['Status'] != 'PENDENTE'), 'Resumo'] = self.df_base['SEC_Resumo']
            except Exception as e:
                print(e)
                raise Exception('Erro ao carregar deparas')
            
            try:
                self.df_base.loc[(self.df_base['Status'] == 'PENDENTE'), 'Situação'] = self.df_base['UPC_Situacao']
                self.df_base.loc[(self.df_base['Status'] != 'PENDENTE'), 'Situação'] = self.df_base['SEC_Situacao']
            except Exception as e:
                print(e)
                raise Exception('Erro ao carregar deparas')
            
            try:
                self.df_base['Dt. Entrega'] = pd.to_datetime(self.df_base['Dt. Entrega'], format='%d/%m/%Y', errors='coerce')
                self.df_base['Dt. Prazo Atual'] = pd.to_datetime(self.df_base['Dt. Prazo Atual'], format='%d/%m/%Y', errors='coerce')
                self.df_base.loc[(self.df_base['Status'] == 'ENTREGUE') & (self.df_base['Dt. Entrega'] <= self.df_base['Dt. Prazo Atual']), 'Análise entregue'] = 'Entregue no Prazo'
                self.df_base.loc[(self.df_base['Status'] == 'ENTREGUE') & (self.df_base['Dt. Entrega'] > self.df_base['Dt. Prazo Atual']), 'Análise entregue'] = 'Entregue Fora do Prazo'
                self.df_base.loc[(self.df_base['Análise entregue'] == ''), 'Análise entregue'] = self.df_base['Situação']
            except Exception as e:
                print(e)
                raise Exception('Erro ao carregar deparas')
            
            try:
                colunas = ['CdEntregaPedidoSite','Modelo de Operação','StEntregaPedidoMongo', 'Status Geral', 
                           'IdLojista', 'NmLojista', 'DhPrevisaoEntrega', 'Dias', 'Aging Cliente']
                self.df_carteira = self.df_carteira[colunas]
                self.df_carteira['CdEntregaPedidoSite'] = self.df_carteira['CdEntregaPedidoSite'].astype('object')
                self.df_carteira = self.df_carteira.rename(columns={'Status Geral': 'Status Geral Carteira'})

                self.df_base['N° Pedido'] = self.df_base['N° Pedido'].apply(lambda x: re.sub('[="]','', str(x)))
                self.df_carteira['CdEntregaPedidoSite'] = self.df_carteira['CdEntregaPedidoSite'].apply(lambda x: re.sub('.0','', str(x)))
                self.df_base = self.df_base.merge(self.df_carteira, left_on='N° Pedido', right_on='CdEntregaPedidoSite', how='left')
                self.df_base['Modalidade_carteira'] = self.df_base['Modelo de Operação']
                self.df_base['Ponto da carteira'] = self.df_base['StEntregaPedidoMongo']
                self.df_base['Status Geral'] = self.df_base['Status Geral Carteira']
                self.df_base['ID Lojista'] = self.df_base['IdLojista']
                self.df_base['Nome Lojista'] = self.df_base['NmLojista']
                self.df_base['Data Prometida'] = self.df_base['DhPrevisaoEntrega']
                self.df_base['Dias Prometida'] = self.df_base['Dias']
                self.df_base['Aging Prometida'] = self.df_base['Aging Cliente']

            except Exception as e:
                print(e)
                raise Exception('Erro ao carregar deparas')
            
            try:
                self.df_base.loc[(self.df_base['Nome Lojista'].isna()), 'Nome Lojista'] = self.df_base['Filial']
                self.df_base.loc[(self.df_base['Data Prometida'].isna()), 'Data Prometida'] = self.df_base['Dt. Prazo Atual']
                self.df_base.loc[(self.df_base['Dias Prometida'].isna()), 'Dias Prometida'] = self.df_base['Dias Prazo Atual']
                self.df_base = self.regra_sla(self.df_base, 'Dias Prometida', 'Aging Prometida')

            except Exception as e:
                print(e)
                raise Exception('Erro ao carregar deparas')

            try:

                bd = DataBaseSQL()
                df_tms_lojista = bd.select_dados("""SELECT * FROM Tbl_De_Para_TMS_Lojista""")
                self.df_base = self.df_base.merge(df_tms_lojista, left_on='Filial', right_on='TLT_Filial', how='left')

                self.df_base.loc[(self.df_base['Modalidade_carteira'].isna()), 'Modalidade_carteira'] = self.df_base['TLT_Modelo_De_Operacao']
                self.df_base.loc[(self.df_base['Ponto da carteira'].isna()), 'Ponto da carteira'] = '-'
                self.df_base.loc[(self.df_base['Status Geral'].isna()), 'Modalidade_carteira'] = '-'
                self.df_base.loc[(self.df_base['ID Lojista'].isna()), 'ID Lojista'] = '-'


            except Exception as e:
                print(e)
                raise Exception('Erro ao carregar deparas')

            try:

                df_lojista_depara: pd.DataFrame = self.df_base.loc[((self.df_base['Modalidade_carteira'].isna() | 
                                                                    self.df_base['Modalidade_carteira'].isin(['-', '']))) &
                                                                    (self.df_base['Nome Lojista'] != '')]
                lista_lojista = list(set(df_lojista_depara['Nome Lojista'].to_list()))
                self.insere_novas_filiais(lista_lojista)

            except Exception as e:
                print(e)
                raise Exception('Erro ao carregar deparas')

            try:
                df_temp = self.df_base.loc[((self.df_base['Modalidade_carteira'].isna() | 
                                             self.df_base['Modalidade_carteira'].isin(['-', '']))) &
                                            (self.df_base['Nome Lojista'] != '')]

            except Exception as e:
                print(e)
                raise Exception('Erro ao carregar deparas')


            try:
                dct_m_lojista = self.dados_depara_nome_lojista()
                df_temp['Modalidade_carteira'] = df_temp['Filial'].map(dct_m_lojista)
                self.df_base.loc[df_temp.index, 'Modalidade_carteira'] = df_temp['Modalidade_carteira']


            except Exception as e:
                print(e)
                raise Exception('Erro ao carregar deparas')
            
            try:
                # self.df_base['Dt. Ult. Ocorrência'] = self.df_base['Dt. Ult. Ocorrência'].replace('-', np.nan) # TODO: verificar se é possive incluir a mesma regra data atual
                self.df_base['Dt. Ult. Ocorrência'] = self.df_base['Dt. Ult. Ocorrência'].replace('-', pd.to_datetime(datetime.now().date())) # TODO: verificar se é possive incluir a mesma regra data atual
                self.df_base['Dt. Ult. Ocorrência'] = pd.to_datetime(self.df_base['Dt. Ult. Ocorrência'], format='%d/%m/%Y', errors='coerce')
                valid_dates = self.df_base['Dt. Ult. Ocorrência'].notnull()
                # import ipdb;ipdb.set_trace()
                data_inicial = np.array(self.df_base.loc[valid_dates, 'Dt. Ult. Ocorrência'].values.astype('datetime64[D]'))
                # data_inicial = np.array(self.df_base['Dt. Ult. Ocorrência'].values.astype('datetime64[D]'))
                self.df_base.loc[valid_dates, 'Dias Ocorr.'] = np.busday_count(data_inicial, datetime.now().date(), holidays=self.df_feriados)

            except Exception as e:
                print(e)
                raise Exception('Erro ao calcular dias Ocorr.')
            
            try:
                # self.df_base.to_csv('saida_ciclo.csv',sep=';', index=False, encoding='latin-1')
                self.df_base = self.regra_aging_processamento(self.df_base, col_inicial='Dias Ocorr.', col_saida='Aging Processamento')
            except Exception as e:
                print(e)
                raise Exception('Erro ao carregar deparas')
            
            try:
                self.df_base.loc[(self.df_base['Modalidade'] == 'Full/Mar aberto') | 
                                 (self.df_base['Modalidade'] == 'Mar aberto'), 'Modal Corrigido'] = 'Mar Aberto'
                self.df_base.loc[(self.df_base['Modalidade'] == 'Envvias/Full') | 
                                 (self.df_base['Modalidade'] == 'Envvias'), 'Modal Corrigido'] = 'Envvias'
                self.df_base.loc[(self.df_base['Modalidade'] == 'Full'), 'Modal Corrigido'] = 'Full'
                self.df_base['Modal Corrigido'].fillna('Mallory', inplace=True)

                self.df_base.to_csv(path_or_buf='saida_ciclo.csv', sep=';', index=False, encoding='latin-1')

            except Exception as e:

                print(e)
                raise Exception('Erro ao carregar deparas')

        except Exception as e:

            print(e)
            raise Exception('Erro de formatação')

    def insere_regras_de_negocio_ciclo(self, df_base: pd.DataFrame):
        """realiza a analise do sistema""" 

        try:

            self.df_base:pd.DataFrame = df_base

        except Exception as e:
            print(e)
            raise Exception('Erro de formatação')   

        ############################################################################################################################################################################
        # PONTOS FINALIZADORES
        ############################################################################################################################################################################

        try:
            condicao = self.df_base['Últ. Pendência'].str.contains('rota',case=False)
            retorno = ['Devolução', 'Finalizado', 'Devolução']
            self.df_base.loc[condicao.fillna(False), ['Análise entregue', 'Resumo', 'Situação']] = retorno
        except Exception as e:
            print(e)
            raise Exception('Erro de formatação')   

        try:
            condicao = self.df_base['Últ. Pendência'].str.contains('extravio|avaria|roubo|sinistro',case=False)
            retorno = ['AVA/EXT/ROU', 'Finalizado', 'AVA/EXT/ROU']
            self.df_base.loc[condicao.fillna(False), ['Análise entregue', 'Resumo', 'Situação']] = retorno

        except Exception as e:
            print(e)
            raise Exception('Erro de formatação') 

        try:
            procura_texto = 'em rota de devolução|extravio|avaria|roubo'
            condicao = (self.df_base['Resumo'].str.contains('Devolução|Em aberto', case=False) &
                        self.df_base['Pendências'].str.contains(procura_texto, case=False))

            retorno = ['Sobreposição', 'Finalizado', 'Sobreposição']
            self.df_base.loc[condicao.fillna(False), ['Análise entregue', 'Resumo', 'Situação']] = retorno

        except Exception as e:
            print(e)
            raise Exception('Erro de formatação')
            
        ############################################################################################################################################################################
        # VALIDAR PENDENCIAS
        ############################################################################################################################################################################
        try:    
            try:
                df_temp = self.df_base[(self.df_base['Situação'] == 'Validar pendencia')]
                # import ipdb;ipdb.set_trace()

            except Exception as e:
                print(e)
                raise Exception('Erro ao carregar deparas')

            try:
                df_temp.loc[(df_temp['Status'] == 'PENDENTE EMBARCADOR'), 'Situação'] = df_temp['UPC_Situacao']
                df_temp.loc[(df_temp['Status'] != 'PENDENTE EMBARCADOR'), 'Situação'] = df_temp['SEC_Situacao']

            except Exception as e:
                print(e)
                raise Exception('Erro ao carregar deparas')


            try:
                df_temp['Dt. Entrega'] = pd.to_datetime(df_temp['Dt. Entrega'], format='%d/%m/%Y', errors='coerce')
                df_temp['Dt. Prazo Atual'] = pd.to_datetime(df_temp['Dt. Prazo Atual'], format='%d/%m/%Y', errors='coerce')
                df_temp.loc[(df_temp['Status'] == 'ENTREGUE') & (df_temp['Dt. Entrega'] <= df_temp['Dt. Prazo Atual']), 'Análise entregue'] = 'Entregue no Prazo'
                df_temp.loc[(df_temp['Status'] == 'ENTREGUE') & (df_temp['Dt. Entrega'] > df_temp['Dt. Prazo Atual']), 'Análise entregue'] = 'Entregue Fora do Prazo'
                df_temp.loc[(df_temp['Análise entregue'] == ''), 'Análise entregue'] = df_temp['Situação']
            except Exception as e:
                print(e)
                raise Exception('Erro ao carregar deparas')


            try:
                condicao = df_temp['Análise entregue'].isin(['Fiscalização'])
                retorno = ['Fiscalização liberada', 'Em aberto', 'Fiscalização liberada']
                df_temp.loc[condicao.fillna(False), ['Análise entregue', 'Resumo', 'Situação']] = retorno

            except Exception as e:
                print(e)
                raise Exception('Erro ao carregar deparas')

            try:
                self.df_base.loc[df_temp.index, 'Análise entregue'] = df_temp['Análise entregue']
                self.df_base.loc[df_temp.index, 'Resumo'] = df_temp['Resumo']
                self.df_base.loc[df_temp.index, 'Situação'] = df_temp['Situação']
                # self.df_base.to_csv('saida_analise.csv', sep=';', encoding='latin-1')
            except Exception as e:
                print(e)
                raise Exception('Erro ao carregar deparas')

        except Exception as e:
            raise Exception(e)
        ############################################################################################################################################################################
        # VALIDAR RECEBIMENTO
        ############################################################################################################################################################################
        try:    
            try:
                df_temp = self.df_base[(self.df_base['Situação'] == 'Validar  recebimento')]

            except Exception as e:
                print(e)
                raise Exception('Erro ao carregar deparas')


            try:
                condicao = (df_temp['Ult. Unidade Ocorrência'] != '') # TODO: validar com ponto focal video(54:10)
                retorno = ['Em Transporte', 'Em aberto', 'Em Transporte']
                df_temp.loc[condicao.fillna(False), ['Análise entregue', 'Resumo', 'Situação']] = retorno

            except Exception as e:
                print(e)
                raise Exception('Erro ao carregar deparas')

            try:
                regex = r'[a-zA-Z]' # regex para verificação de existencia de letras
                df_temp['Sigla Unidade Atual'] = df_temp['Sigla Unidade Atual'].fillna('')
                condicao = (df_temp['Sigla Unidade Atual'].str.contains(regex, na=False) & 
                           (~df_temp['Sigla Unidade Atual'].astype(str).str.contains('seller', case=False)))
                retorno = ['Em Transporte', 'Em aberto', 'Em Transporte']
                df_temp.loc[condicao.fillna(False), ['Análise entregue', 'Resumo', 'Situação']] = retorno

            except Exception as e:
                print(e)
                raise Exception('Erro ao carregar deparas')

            try:
                condicao = (df_temp['Sigla Unidade Atual'].str.contains('seller', case=False))
                retorno = ['Não coletado pela Asap', 'Não coletado', 'Não coletado pela Asap']
                df_temp.loc[condicao.fillna(False), ['Análise entregue', 'Resumo', 'Situação']] = retorno

            except Exception as e:
                print(e)
                raise Exception('Erro ao carregar deparas')

            try:
                condicao = ((df_temp['Sigla Unidade Atual'] == 1) & (df_temp['Sigla Unidade Entrega'] == 'TOTAL 1200'))
                retorno = ['Em Transporte', 'Em aberto', 'Em transporte']
                df_temp.loc[condicao.fillna(False), ['Análise entregue', 'Resumo', 'Situação']] = retorno

            except Exception as e:
                print(e)
                raise Exception('Erro ao carregar deparas')


            try:
                regex = r'^\d+$' # regex para verificação de existencia de numero TODO: verificar listagem para filtro da coluna ocorrencia
                condicao = ((df_temp['Sigla Unidade Atual'].str.contains(regex, na=False) | df_temp['Sigla Unidade Atual'] == '') & 
                            df_temp['Últ. Ocorrência'].isin(['Sincronização', 'Chegada na filial']))
                retorno = ['Em Transporte', 'Em aberto', 'Em Transporte']
                df_temp.loc[condicao.fillna(False), ['Análise entregue', 'Resumo', 'Situação']] = retorno

            except Exception as e:
                print(e)
                raise Exception('Erro ao carregar deparas')

            try:
                regex = r'[0-9]' # regex para verificação de existencia de numero TODO: verificar listagem para filtro da coluna ocorrencia
                condicao = ((df_temp['Sigla Unidade Atual'].str.contains(regex, na=False) | df_temp['Sigla Unidade Atual'] == '') & 
                            (~df_temp['Últ. Ocorrência'].isin(['sincronização', 'chegada na filial'])))
                retorno = ['No Hub', 'Em aberto', 'No Hub']
                df_temp.loc[condicao.fillna(False), ['Análise entregue', 'Resumo', 'Situação']] = retorno

            except Exception as e:
                print(e)
                raise Exception('Erro ao carregar deparas')

            try:
                self.df_base.loc[df_temp.index, 'Análise entregue'] = df_temp['Análise entregue']
                self.df_base.loc[df_temp.index, 'Resumo'] = df_temp['Resumo']
                self.df_base.loc[df_temp.index, 'Situação'] = df_temp['Situação']
                # self.df_base.to_csv('saida_analise.csv', sep=';', encoding='latin-1')
            except Exception as e:
                print(e)
                raise Exception('Erro ao carregar deparas')

        except Exception as e:
            raise Exception(e)


        ############################################################################################################################################################################
        # PEDIDOS COM ERRO
        ############################################################################################################################################################################
        # verificar os pedidos que tem algum tipo de historico de erro
        try:
            bd = DataBaseSQL()
            df_depara_modalidade = bd.select_dados("""SELECT * FROM Tbl_Pedidos_Com_Erro""")
            self.df_base = self.df_base.merge(df_depara_modalidade, left_on='N° Pedido', right_on='PCE_Pedido', how='left')
            self.df_base['Teve sobreposição?'] = self.df_base['PCE_Motivo'] # TODO: verificar se existem campos em branco inserir transp COL(sigla Unidade Entrega)
            

        except Exception as e:
            print(e)
            raise Exception('Erro ao carregar deparas')

        try:
            df_temp = self.df_base[(self.df_base['Teve sobreposição?'] != '')]

        except Exception as e:
            print(e)
            raise Exception('Erro ao carregar deparas')

        try:
            df_temp['Análise entregue'] = df_temp['Teve sobreposição?']
            df_temp['Resumo'] = 'Não coletado'
            df_temp['Situação'] = df_temp['Teve sobreposição?']

        except Exception as e:
            print(e)
            raise Exception('Erro ao carregar deparas')


        try:
            self.df_base.loc[df_temp.index, 'Análise entregue'] = df_temp['Análise entregue']
            self.df_base.loc[df_temp.index, 'Resumo'] = df_temp['Resumo']
            self.df_base.loc[df_temp.index, 'Situação'] = df_temp['Situação']
            # self.df_base.to_csv('saida_analise.csv', sep=';', encoding='latin-1')
        except Exception as e:
            print(e)
            raise Exception('Erro ao carregar deparas')

        ############################################################################################################################################################################
        # NÃO COLETADO | FINALIZADO
        ############################################################################################################################################################################
        try:
            df_temp = self.df_base[(~self.df_base['Resumo'].isin(['Finalizado', 'Não coletado'])) & 
                                   (self.df_base['Situação'].isin(['Em Transporte']))]

        except Exception as e:
            print(e)
            raise Exception('Erro ao carregar deparas')


        try:
            regex = r'^\d+$'
            condicao = df_temp['Sigla Unidade Destino'].str.contains(regex, na=False)
            retorno = ['Em Transporte hub', 'Em aberto', 'Em Transporte hub']
            df_temp.loc[condicao.fillna(False), ['Análise entregue', 'Resumo', 'Situação']] = retorno

        except Exception as e:
            print(e)
            raise Exception('Erro ao carregar deparas')

        try:
            self.df_base.loc[df_temp.index, 'Análise entregue'] = df_temp['Análise entregue']
            self.df_base.loc[df_temp.index, 'Resumo'] = df_temp['Resumo']
            self.df_base.loc[df_temp.index, 'Situação'] = df_temp['Situação']
            # self.df_base.to_csv('saida_analise.csv', sep=';', encoding='latin-1')
        except Exception as e:
            print(e)
            raise Exception('Erro ao carregar deparas')
            
        ############################################################################################################################################################################
        # NÃO COLETADO | FINALIZADO parte 2
        ############################################################################################################################################################################
        try:
            df_temp = self.df_base[(self.df_base['Situação'].isin(['Em Transporte']))]

        except Exception as e:
            print(e)
            raise Exception('Erro ao carregar deparas')


        try:
            condicao = df_temp['Últ. Pendência'].str.contains('BARRAR ENTREGA', case=False)
            retorno = ['Devolução', 'Em aberto', 'Devolução']
            df_temp.loc[condicao.fillna(False), ['Análise entregue', 'Resumo', 'Situação']] = retorno

        except Exception as e:
            print(e)
            raise Exception('Erro ao carregar deparas')

        try:
            self.df_base.loc[df_temp.index, 'Análise entregue'] = df_temp['Análise entregue']
            self.df_base.loc[df_temp.index, 'Resumo'] = df_temp['Resumo']
            self.df_base.loc[df_temp.index, 'Situação'] = df_temp['Situação']
            # self.df_base.to_csv('saida_analise.csv', sep=';', encoding='latin-1')
        except Exception as e:
            print(e)
            raise Exception('Erro ao carregar deparas')
        ############################################################################################################################################################################
        # NÃO COLETADO | FINALIZADO parte 2
        ############################################################################################################################################################################
        try:
            df_temp = self.df_base[(~self.df_base['Resumo'].isin(['Finalizado', 'Não coletado']))]

        except Exception as e:
            print(e)
            raise Exception('Erro ao carregar deparas')


        try:
            status = ['Anular cancelamento', 'Anular recebimento', 'Cancelamento de lista first mile'] # TODO: validar os textos
            condicao = df_temp['Últ. Pendência'].str.contains("|".join(status), case=False)
            retorno = ['Em Transporte', 'Não coletado', 'Em Transporte']
            df_temp.loc[condicao.fillna(False), ['Análise entregue', 'Resumo', 'Situação']] = retorno


            # separação dos pedidos com erro
            df_aux = df_temp[condicao]
            lista_ped: list = list(set(df_aux['N° Pedido'].to_list()))
            self.insere_pedido_erro(lista_ped)

        except Exception as e:
            print(e)
            raise Exception('Erro ao carregar deparas')

        try:
            # df_temp['Sigla Unidade Atual'] = df_temp['Sigla Unidade Atual'].fillna('')
            condicao = ((df_temp['Últ. Pendência'].str.contains('Cancelamento de solicitação', case=False)) & 
                        (df_temp['Pendências'] == '') & (df_temp['Sigla Unidade Atual'] == ''))
            retorno = ['Cancelado', 'Não coletado', 'Cancelamento Lista First Mile']
            df_temp.loc[condicao.fillna(False), ['Análise entregue', 'Resumo', 'Situação']] = retorno


            # separação dos pedidos com erro
            df_aux = df_temp[condicao]
            lista_ped: list = list(set(df_aux['N° Pedido'].to_list()))
            self.insere_pedido_erro(lista_ped)

        except Exception as e:
            print(e)
            raise Exception('Erro ao carregar deparas')

        try:
            self.df_base.loc[df_temp.index, 'Análise entregue'] = df_temp['Análise entregue']
            self.df_base.loc[df_temp.index, 'Resumo'] = df_temp['Resumo']
            self.df_base.loc[df_temp.index, 'Situação'] = df_temp['Situação']
            # self.df_base.to_csv('saida_analise.csv', sep=';', encoding='latin-1')

        except Exception as e:

            print(e)
            raise Exception('Erro ao carregar deparas')

        ############################################################################################################################################################################
        # NÃO COLETADO | FINALIZADO parte 3
        ############################################################################################################################################################################
        try:
            df_temp = self.df_base[(~self.df_base['Resumo'].isin(['Finalizado', 'Não coletado']))]

        except Exception as e:
            print(e)
            raise Exception('Erro ao carregar deparas')


        try:
            condicao = df_temp['Últ. Ocorrência'].str.contains('BARRAR ENTREGA', case=False)
            retorno = ['Devolução', 'Em aberto', 'Devolução']
            df_temp.loc[condicao.fillna(False), ['Análise entregue', 'Resumo', 'Situação']] = retorno

        except Exception as e:
            print(e)
            raise Exception('Erro ao carregar deparas')

        try:
            self.df_base.loc[df_temp.index, 'Análise entregue'] = df_temp['Análise entregue']
            self.df_base.loc[df_temp.index, 'Resumo'] = df_temp['Resumo']
            self.df_base.loc[df_temp.index, 'Situação'] = df_temp['Situação']
            # self.df_base.to_csv('saida_analise.csv', sep=';', encoding='latin-1')
        except Exception as e:
            print(e)
            raise Exception('Erro ao carregar deparas')

        ############################################################################################################################################################################
        # NÃO COLETADO | FINALIZADO parte 3
        ############################################################################################################################################################################
        try:
            df_temp = self.df_base[(self.df_base['Análise entregue'].isin(['Devolução'])) &
                                    (~self.df_base['Resumo'].isin(['Finalizado']))]

        except Exception as e:
            print(e)
            raise Exception('Erro ao carregar deparas')


        try:
            regex = r'^\d+$'
            condicao = (df_temp['Sigla Unidade Atual'].str.contains(regex, na=False) | 
                        df_temp['Sigla Unidade Atual'].str.contains('seller', case=False))

            retorno = ['FRACIONADA HUB','Em Transporte hub', 'Em aberto', 'Em Transporte hub']
            df_temp.loc[condicao.fillna(False), ['Modalidade', 'Análise entregue', 'Resumo', 'Situação']] = retorno

        except Exception as e:
            print(e)
            raise Exception('Erro ao carregar deparas')

        try:
            self.df_base.loc[df_temp.index, 'Modalidade'] = df_temp['Modalidade']
            self.df_base.loc[df_temp.index, 'Análise entregue'] = df_temp['Análise entregue']
            self.df_base.loc[df_temp.index, 'Resumo'] = df_temp['Resumo']
            self.df_base.loc[df_temp.index, 'Situação'] = df_temp['Situação']
            # self.df_base.to_csv('saida_analise.csv', sep=';', encoding='latin-1')
        except Exception as e:
            print(e)
            raise Exception('Erro ao carregar deparas')

        ############################################################################################################################################################################
        # MODALIDADE
        ############################################################################################################################################################################
        try:
            self.df_base.loc[(self.df_base['Modalidade'].isin(['HUB ASAP', 'LML'])), 'Modalidade'] = 'LML'

        except Exception as e:
            print(e)
            raise Exception('Erro ao carregar deparas')


        ############################################################################################################################################################################
        # MODALIDADE
        ############################################################################################################################################################################
        try:
            self.df_base.loc[((self.df_base['Modalidade'] == 'FRACIONADA') & 
                              (~self.df_base['Resumo'].isin(['Finalizado', 'Não coletado'])) &
                              (self.df_base['Análise entregue'].str.contains('hub', case=False))), 'Modalidade'] = 'FRACIONADA HUB'

        except Exception as e:
            print(e)
            raise Exception('Erro ao carregar deparas')
        ############################################################################################################################################################################
        # SAIDA
        ############################################################################################################################################################################
        try:
            saida_dados_s_lml = self.df_base[(~self.df_base['Resumo'].isin(['Finalizado', 'Não coletado'])) &
                                             (self.df_base['Modalidade'] != 'LML')]

        except Exception as e:
            print(e)
            raise Exception('Erro ao carregar deparas')

        try:
            saida_dados_c_lml = self.df_base[(self.df_base['Modalidade'] == 'LML') & 
                                             (self.df_base['Modalidade_carteira'] != 'Mar Aberto')]

        except Exception as e:
            print(e)
            raise Exception('Erro ao carregar deparas')


        try:
            df_final_ciclo: pd.Dataframe = pd.concat([saida_dados_s_lml, saida_dados_c_lml])
            df_final_ciclo.to_csv(path_or_buf='saida_final_ciclo.csv', sep=';', encoding='latin-1')
            self.df_base.to_csv(path_or_buf='saida_analise.csv', sep=';', encoding='latin-1')
        except Exception as e:
            print(e)
            raise Exception('Erro ao carregar deparas')

    def formatacao_arquivo_final_ciclo(self,  df_base: pd.DataFrame):
        """video(01:08:20)"""
        ...
