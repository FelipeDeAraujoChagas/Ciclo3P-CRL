from datetime import datetime
#from data.database_pyqt import DataBasePyQt


class VerificacaoAcessoSistema:
    
    def __init__(self):

        self.dict_status: dict = {'status': False, 'msg': ''}

    def carregar_status_sistema(self):

        """busca na tabela se o sistema existe algum bloqueio"""

        try:

            # sql = """SELECT * FROM GestaoProjetosRPA.dbo.Tbl_Permissao_Sistema"""
            sql = F"""SELECT * 
                      FROM 
                          vw_Permissao_Sistema
                      WHERE 
                          PS_Nome_Sistema = 'Gestão de Estoque EAD'
                        """
            
            #crud = DataBasePyQt()
            #dados = crud.select_dados_pyqt(string_sql=sql)
            #print( dados.to_dict(orient='records'))
            #return dados.to_dict(orient='records')[0]

        except Exception as e:
            print(e)    

    def verifica_status(self):

        status:dict = self.carregar_status_sistema()

        if not bool(status):
            self.dict_status['status'] = True

        else:
            data_atual = datetime.now().date()
            data_inicial = datetime.strptime(status.get('PS_Data_Inicial'), __format='%Y-%m-%d').date()
            data_final = datetime.strptime(status.get('PS_Data_Final'), __format='%Y-%m-%d').date()
            diferenca_dias = data_inicial - data_atual
            # print(diferenca_dias.days)

            if 0 < (diferenca_dias.days) <= 5:
                dta_formatada = datetime.strftime(data_inicial,'%d/%m/%Y')
                self.dict_status['status'] = True
                self.dict_status['msg'] = f"""O Sistema de {status.get("PS_Nome_Sistema")} esta programado para bloqueio automatico no dia {dta_formatada}!\n Para mais informações entre em contato com a area responsavel."""

            elif data_inicial <= data_atual <= data_final:
                self.dict_status['status'] = False
                self.dict_status['msg'] = status.get('PS_Mensagem')
                # print(status.get('PS_Mensagem'))
                
        return self.dict_status
