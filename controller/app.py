from PyQt5.QtWidgets import QTextEdit, QApplication

class Run:

    def __init__(self, text_edit: QTextEdit):

        self.text_Edit: QTextEdit = text_edit
        self.lista_pedido = []


    def analiseBases(self):

        msg = ">> Iniciar Analize Bases"
        self.add_text_to_text_edit(msg)

        from src.analiseBase import Analise
        baseCiclo = Analise()
        baseCiclo.lerBaseCSV()
        baseCiclo.criarAnaliseBaseCiclo()

        msg = (
            '\n===========================================\n'
            '       ------>> Processo Total Finalizado <<------\n'
            '===========================================\n'
        )
        self.add_text_to_text_edit(msg)


    def tmsUX(self):

        from src.aut_tms_ux import AutomacaoTmsUX
        aut = AutomacaoTmsUX(self.lista_pedido, textEdit=self.text_Edit)
        aut.nova_execucao_processo()

        msg = (
               '\n===========================================\n'
               '        ------>> Consulta TmsUX finalizada <<------\n'
               '===========================================\n'
        )
        self.add_text_to_text_edit(msg)

    def tratativaBases(self, arqFullfilment, arqDataFormatado,arqValidacao, arqCliclo):

        import time
        from datetime import datetime
        inicio = time.time()
        tempo_formatado = datetime.fromtimestamp(inicio).strftime('%H:%M:%S')

        texto = f"Processo iniciado as : {str( tempo_formatado )}\n"
        self.add_text_to_text_edit(texto)

        from src.tratativaBase import Tratativa

        inicio = time.time()
        tt = Tratativa()
        tt.tratarBaseFormatacaoCareteiraPedido(arquivo=arqDataFormatado)
        fim1 = time.time()
        hora = datetime.fromtimestamp(fim1 - inicio).strftime('%M:%S')
        tempo = datetime.fromtimestamp(fim1 - inicio).strftime('%M:%S')
        texto = f"Importação da Carteira Pedido! tempo: {hora} | tempo app: {tempo}"
        print(texto)
        self.add_text_to_text_edit(texto=texto)

        # ---------------------------------------------------------------#
        tt.tratarBaseFormatacaoFullfilmentPedidos(arquivo=arqFullfilment)
        fim2 = time.time()
        hora = datetime.fromtimestamp(fim2 - fim1).strftime('%M:%S')
        tempo = datetime.fromtimestamp(fim2 - inicio).strftime('%M:%S')
        texto = f"importação da base FullFilment! tempo: {hora} | tempo app: {tempo}"
        print(texto)
        self.add_text_to_text_edit(texto=texto)

        # ---------------------------------------------------------------#
        tt.tratarBaseFormatacaoCarteiraAsap(arquivo=arqValidacao)
        fim3 = time.time()
        hora = datetime.fromtimestamp(fim3 - fim2).strftime('%M:%S')
        tempo = datetime.fromtimestamp(fim3 - inicio).strftime('%M:%S')
        texto = f"Importação da Carteira Asap! tempo: {hora} | tempo app: {tempo}"
        print(texto)
        self.add_text_to_text_edit(texto=texto)

        # ---------------------------------------------------------------#
        tt.tratarbaseFormatacaoCarteiraTMS(arquivo=arqCliclo)
        fim4 = time.time()
        hora = datetime.fromtimestamp(fim4 - fim3).strftime('%M:%S')
        tempo = datetime.fromtimestamp(fim4 - inicio).strftime('%M:%S')
        texto = f"Importação Carteira TMS! tempo: {hora} | tempo app: {tempo}"
        print(texto)
        self.add_text_to_text_edit(texto=texto)

        self.lista_pedido = tt.mergeLista_pedido()

        msg = (
            '\n=================================================\n'
            '       ------>> Inportações de Bases finalizada <<------\n'
            '=================================================\n'
        )
        self.add_text_to_text_edit(msg)

        # import pandas as pd
        # lit_df = pd.DataFrame(self.lista_pedido)
        # print(lit_df)
        # lit_df.to_csv(path_or_buf='lista Pedido.csv', index=False, sep=';')

    def add_text_to_text_edit(self, texto):

        self.text_Edit.append(texto)
        QApplication.processEvents()
