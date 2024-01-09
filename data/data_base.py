import os
import sqlite3 as slt
from tkinter import messagebox
#import pandas as pd


class Database:

    def __init__(self) -> None:


        dir_data = os.path.join(os.getcwd(), 'data')
        #dir_pai = os.path.dirname(dir_data) + "\\data"

        self.dbLocal = dir_data + '\\dataBase_ciclo.db'
        #self.dbLocal = r"C:\Users\2901885626\Documents\ciclo3P\ciclo_3p\data\dataBase_ciclo.db"
        #self.dbLocal = r"C:\Users\2103896595\Desktop\arquivos\banco de dados\dataBase_ciclo.db"
                
    def connect_bd(self):
        """Estabelece conexão com o banco de dados"""
        self.conn = slt.connect(self.dbLocal)
        self.cursor = self.conn.cursor()

    def cria_tabelas(self):
        """cria serie de tabelas pré-definidas"""
        try:
            self.connect_bd()
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS tb_usuario(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario         TEXT,
                senha           TEXT,
                diretorio       TEXT,
                max_volumes     TEXT
            )""")

            self.cursor.execute("""CREATE TABLE IF NOT EXISTS tb_bricks(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                host_name     TEXT,
                http_path     TEXT,
                token         TEXT
            )""")

            self.cursor.execute("""CREATE TABLE IF NOT EXISTS tb_depara_transp(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                descri_oco     TEXT,
                ponto          TEXT,
                transp         TEXT
            )""")

            self.cursor.execute("""CREATE TABLE IF NOT EXISTS tb_ponto(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ponto           TEXT,
                descricao       TEXT,
                res_ponto       TEXT
            )""")

            self.cursor.execute("""CREATE TABLE IF NOT EXISTS tb_param_sql(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                server  TEXT,
                database    TEXT,
                username    TEXT,
                password    TEXT
            )""")


            self.conn.commit()
        except Exception as e:
            messagebox.showerror('Erro Consulta', 'Não foi possivel Criar as tabelas.\n{}'.format(e))
        finally:
            self.conn.close()

    def insert_dados(self, string_sql, dados):
        """realiza a inserção de dados dentro do banco"""
        try:
            self.connect_bd()
            self.cursor.executemany(string_sql, dados)
            self.conn.commit()
        except Exception as e:
            messagebox.showerror('Erro Consulta', 'Não foi possivel Inserir os dados.\n{}'.format(e))
        finally:
            self.conn.close()

    def update_dados(self, string_sql):
        """atualiza um registro dentro do banco de dados"""
        try:
            self.connect_bd()
            self.cursor.execute(string_sql)
            self.conn.commit()
        except Exception as e:
            print(e)
            messagebox.showerror('Erro Consulta', 'Não foi possivel Atualizar os dados.\n{}'.format(e))
        finally:
            self.conn.close()

    def delete_dados(self, string_sql):
        """remove um registro dentro do banco de dados"""
        try:
            self.connect_bd()
            self.cursor.execute(string_sql)
            self.conn.commit()
        except Exception as e:
            messagebox.showerror('Erro Consulta', 'Não foi possivel Deletar os dados.\n{}'.format(e))
        finally:
            self.conn.close()

    def select_dados(self, string_sql) -> list:  # type: ignore
        """seleciona os dados apartir de uma consulta"""
        try:
            self.connect_bd()
            self.cursor.execute(string_sql)
            data = self.cursor.fetchall()
            return data
        except Exception as e:
            messagebox.showerror('Erro Consulta', 'Não foi possivel Selecionar os dados.\n{}'.format(e))
        finally:
            self.conn.close()

if __name__ == '__main__':
    data = Database()
    data.cria_tabelas()

    # df = pd.DataFrame(pd.read_excel(r'C:\Users\2103896595\Desktop\ANALISE DIALOGO.xlsx',sheet_name='DEPARA_C'))
    # df['ID']= None
    # df = df[['ID','DESCRI','PONTO', 'TRANSP']]
    # lista = [tuple(x) for x in df.values]
    # data.insert_dados(f"INSERT INTO tb_depara_transp VALUES(?,?,?,?);", lista)