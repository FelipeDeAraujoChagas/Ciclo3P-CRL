import pyodbc
from datetime import datetime
from data.data_base import Database


class AtivacaoApp:

    def __init__(self, aplicativo):

        self.appAtivo = False
        self.motivo = None
        self.__server = None
        self.__database = None
        self.__username = None
        self.__password = None

        self.getDadosConexacao()

        self.__string_conn = (f"DRIVER={{SQL Server}};"
                             f"SERVER={self.__server};"
                             f"DATABASE={self.__database};"
                             f"UID={self.__username};"
                             f"PWD={self.__password}")

        self.__sql = f"select * from vw_Permissao_Sistema where PS_Nome_Sistema = '{aplicativo}'"

        self.statusApp()

    def getDadosConexacao(self):

        data = Database()
        sql = ''' select * from tb_param_sql where id = 3 '''
        dados = data.select_dados(sql)

        ruw = dados[0]

        self.__server = ruw[1]
        self.__database = ruw[2]
        self.__username = ruw[3]
        self.__password = ruw[4]


    def statusApp(self):

        try:

            with pyodbc.connect(self.__string_conn) as conn:
                cursor = conn.cursor()
                cursor.execute(self.__sql)
                data = cursor.fetchall()

            data_de_hoje = datetime.today().date()

            if not data:
                self.appAtivo = True
                return

            for k, v in enumerate(data):
                data_inicio = v[2]
                data_fim = v[3]
                data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
                data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()

                if data_inicio <= data_de_hoje <= data_fim:
                   self.motivo = v[4]
                   self.appAtivo = False

                else:
                    self.appAtivo = True

        except:

            self.appAtivo = False


if __name__ == "__main__":
    em = AtivacaoApp("Base Ciclo 3p - CRL")
    print(em.appAtivo)
