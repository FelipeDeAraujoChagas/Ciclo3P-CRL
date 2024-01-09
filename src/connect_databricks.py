import os
import pandas as pd
from databricks import sql as sql_conn
from data.data_base import Database


class ConnectConsultDatabricks:

    def __init__(self) -> None:

        pass

    def carregar_variaveis(self):

        """carrega as variaveis de ambiente do sistema"""

        try:
            bd = Database()
            sql = "SELECT * FROM tb_bricks"
            dados = bd.select_dados(sql)
            self.__server_name = dados[0][1]
            self.__http_path = dados[0][2]
            self.__token = dados[0][3]

        except Exception as e:
            raise Exception('Não foi possivel carregar as variaveis de acesso')
    
    def realiza_consulta(self):

        """efetua a consulta dentro do sistema databricks"""

        try:
            self.carregar_variaveis()
            with sql_conn.connect(server_hostname=self.__server_name,
                                  http_path=self.__http_path,
                                  access_token=self.__token) as connection:
                sql = f"""
                    SELECT *
                    FROM hive_metastore.databox_malhalogistica_comum.matriz_ciclo_crl limit 5
                """

                df_saida = pd.read_sql_query(sql, connection) #type: ignore
                return df_saida

        except Exception as e:
            
            raise Exception(f'Não foi possivel realizar a consulta no databricks!\n{e}')

if __name__ == '__main__':
    bcks = ConnectConsultDatabricks()
    dados = bcks.realiza_consulta()
    dados.to_excel(excel_writer='saida.xlsx', index=False)
