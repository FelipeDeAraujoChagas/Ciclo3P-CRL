import pyodbc
#import os
#import dotenv
import pandas as pd
from data.data_base import Database


class DataBaseSQL:

    def __init__(self) -> None:

        self.variaveis_de_conexao()

    def carregar_dados(self):
        """Carrega dos dados para login dentro do PCOM"""

        try:
            bd = Database()
            self.__dados = bd.select_dados('SELECT * FROM tb_param_sql WHERE id = 1')
            self.__server  = self.__dados[0][1]
            self.__database = self.__dados[0][2]
            self.__username = self.__dados[0][3]
            self.__password = self.__dados[0][4]

        except Exception as e:
            print('Erro', f'Não foi possivel carregar os parametros.\n{e}')

    def variaveis_de_conexao(self):
        """"""
        try:
            self.carregar_dados()
            self.server = self.__server
            self.database = self.__database
            self.username = self.__username
            self.password = self.__password
        except Exception as e:
            pass

    def criar_conexao(self):

        """estabelece conexão com o banco de dados"""

        try:

            conn_str = (f"DRIVER={{SQL Server}};"
                        f"SERVER={self.server};"
                        f"DATABASE={self.database};" 
                        f"DATABASE={self.database};"    
                        f"UID={self.username};"
                        f"PWD={self.password}")


            # print(conn_str)
            return pyodbc.connect(conn_str)

        except Exception as e:

            print(e)

    def select_dados(self, sql_string):
        ''' Retorna um DataFrame, necessita passar a uma strig com comando sql para a consulta '''

        try:

            conn = self.criar_conexao()
            df: pd.DataFrame = pd.read_sql_query(sql_string, conn)
            conn.close()

            return df

        except Exception as e:
            # conn.rollback()
            raise ValueError(f"Erro retornar dados{e}")

        finally:
            pass
            

    def insert_dados(self, sql_string, dados: list = None):

        """  """
        conn = self.criar_conexao()
        try:
            if not dados:
                conn.cursor().execute(sql_string)
            else:
                conn.cursor().execute(sql_string, dados)
            conn.commit()
        except Exception as e:

            raise ValueError(f"Erro ao inserir Dados.{e}")

        finally:

            conn.close()

    def update_dados(self, sql_string):

        """"""
        try:
            conn = self.criar_conexao()
            conn.cursor().execute(sql_string)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise ValueError("Erro ao atualizar")
        finally:
            conn.close()

    def delete_dados(self, sql_string):

        """"""
        try:
            conn = self.criar_conexao()
            conn.cursor().execute(sql_string)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise ValueError("Erro ao tentar excluir registro")
        finally:
            conn.close()


class ConsultaTabelas(DataBaseSQL):

    def consultarUsuarios(self, usuario: str, password: str):

        try:
            sql = f'SELECT * FROM Tbl_Usuarios where matricula = {usuario} and senha = {password}'
            data: pd.DataFrame = self.select_dados(sql)
            return data
        except Exception as e:
            print(e)

    def consultarUserExiste(self, usuario):

        try:

            sql = f''' select matricula from Tbl_Usuarios where matricula = '{usuario}' '''
            data: pd.DataFrame = self.select_dados(sql)
            user = data.iloc[0, 0]
            if user == usuario:
                return True
            else:
                return False
        except:
            return False




if __name__ == '__main__':
    sql_exe = DataBaseSQL()
    # conn = sql_exe.criar_conexao() 
    sql ="""SELECT * FROM Tbl_De_Para_Ponto"""
           
    df = sql_exe.select_dados(sql)
    print(df)