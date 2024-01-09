import pandas as pd

class Analise:

    def __init__(self, baseContatenada=None, baseCarteira=None) -> None:

        self.baseContatenada: pd.DataFrame = baseContatenada
        self.baseCarteira: pd.DataFrame = baseCarteira

    def lerBaseCSV(self):

        self.baseContatenada = pd.read_csv(filepath_or_buffer='saida_concatenada.csv', sep=';', encoding='latin-1',
                       low_memory=False)

        self.baseCarteira = pd.read_csv(filepath_or_buffer='saida_carteira.csv', sep=';', encoding='latin-1',
                               low_memory=False)

    def criarAnaliseBaseCiclo(self):

        from src.preparacao_ciclo import FormatacaoBaseCiclo
        ciclo = FormatacaoBaseCiclo(self.baseContatenada, self.baseCarteira)
        ciclo.analise_base_ciclo()
        df_ciclo = pd.read_csv(filepath_or_buffer='saida_ciclo.csv', sep=';', encoding='latin-1')
        ciclo.insere_regras_de_negocio_ciclo(df_ciclo)


