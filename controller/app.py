from src.tratativaBase import Tratativa


class Run:

    def __init__(self):

        self.lista_pedido = []

    # def rodar(self, arquivo):
    #
    #     self.tratativaBases(arquivo)
    #     #self.tmsUX()
    #     #self.analiseBases()

    def analiseBases(self):

        from src.analiseBase import Analise
        baseCiclo = Analise()
        baseCiclo.lerBaseCSV()
        baseCiclo.criarAnaliseBaseCiclo()


    def tmsUX(self):

        from src.aut_tms_ux import AutomacaoTmsUX
        aut = AutomacaoTmsUX(self.lista_pedido)
        aut.nova_execucao_processo()

    def tratativaBases(self, arqFullfilment, arqDataFormatado,arqValidacao, arqCliclo):

        import time
        from src.tratativaBase import Tratativa

        inicio = time.time()
        tt = Tratativa()
        tt.tratarBaseFormatacaoCareteiraPedido(arquivo=arqDataFormatado)
        fim1 = time.time()
        print(f"etapa 1 concluida! tempo: {fim1 - inicio:.2f} / tempo app: {fim1 - inicio:.2f}")
        tt.tratarBaseFormatacaoFullfilmentPedidos(arquivo=arqFullfilment)
        fim2 = time.time()
        print(f"etapa 2 concluida! tempo: {fim2 - fim1 :.2f} / tempo app: {fim2 - inicio :.2f}")
        tt.tratarBaseFormatacaoCarteiraAsap(arquivo=arqValidacao)
        fim3 = time.time()
        print(f"etapa 3 concluida! tempo: {fim3 - fim2 :.2f} / tempo app: {fim3 - inicio:.2f}")
        tt.tratarbaseFormatacaoCarteiraTMS(arquivo=arqCliclo)
        fim4 = time.time()
        print(f"etapa 4 concluida! tempo: {fim4 - fim3 :.2f} / tempo app: {fim4 - inicio :.2f}")
        self.lista_pedido = tt.mergeLista_pedido()


