
class Tratativa:

    def __init__(self):

        self.dct_carteira_pedidos = {}
        self.dct_fullfilment = {}
        self.dct_carteira_asap = {}
        self.dct_ciclo_antigo = {}

    def tratarBaseFormatacaoCareteiraPedido(self, arquivo):

        from src.preparacao_base import FormatacaoCarteiraPedidos
        carteira_pedidos = FormatacaoCarteiraPedidos(arquivo)
        dados_carteira_pedidos = carteira_pedidos.analise_carteira()
        self.dct_carteira_pedidos = {
            'fonte': 'Carteira Pedidos',
            'pesquisar_por': 'nro_pedido',
            'lista_doc': dados_carteira_pedidos
        }

    def tratarBaseFormatacaoFullfilmentPedidos(self, arquivo):

        from src.preparacao_base import FormatacaoFullfilmentPedidos
        fullfilment = FormatacaoFullfilmentPedidos(arquivo)
        dados_fullfilment = fullfilment.analise_fullfilment()
        self.dct_fullfilment = {
            'fonte': 'Fullfilment',
            'pesquisar_por': 'nro_pedido',
            'lista_doc': dados_fullfilment
        }

    def tratarBaseFormatacaoCarteiraAsap(self, arquivo):

        from src.preparacao_base import FormatacaoCarteiraAsap
        carteira_asap = FormatacaoCarteiraAsap(arquivo)
        dados_carteira_asap = carteira_asap.analise_carteira_asap()
        # print(dados_carteira_asap) #entrega
        self.dct_carteira_asap = {
            'fonte': 'Carteira Asap',
            'pesquisar_por': 'nro_entrega',
            'lista_doc': dados_carteira_asap
        }

    def tratarbaseFormatacaoCarteiraTMS(self, arquivo):

        from src.preparacao_base import FormatacaoCarteiraTMS
        ciclo_antigo = FormatacaoCarteiraTMS(arquivo)
        dados_ciclo_antigo = ciclo_antigo.analise_ciclo_antigo()
        # print(dados_carteira_tms) #entrega
        self.dct_ciclo_antigo = {
            'fonte': 'Ciclo Antigo',
            'pesquisar_por': 'nro_entrega',
            'lista_doc': dados_ciclo_antigo
        }

    def mergeLista_pedido(self):

        return [
               self.dct_carteira_pedidos,
               self.dct_fullfilment,
               self.dct_carteira_asap,
               self.dct_ciclo_antigo
        ]
