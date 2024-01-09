import time
from loguru import logger
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select  # type: ignore
from selenium.webdriver.support.wait import WebDriverWait
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
# from .download_driver import DownloadChromeDirver

from tkinter import messagebox
import os
import pyperclip as colar_win
from utils.func_aux import FuncoesAux
from data.data_base import Database
from random import randint

class automacao:
    def __init__(self):
        ...

    def extrai_dados_tms(self):

        print('extraindo dados')

    def gerencia_dowload(self):

        print('movimentando dados')

    def executa_processo(self):

        self.extrai_dados_tms()
        time.sleep(2)
        self.gerencia_dowload()   


class AutomacaoTmsUX(FuncoesAux):

    def __init__(self, lista: list, pasta_aux: str = '') -> None:


        self.carregar_dados()
        self.lista_pesquisa = lista
        if pasta_aux:
            self.dir_download_temp = pasta_aux
        else:
            self.dir_download_temp = os.path.join(os.getcwd(), 'temp')
        
        self.url = "http://vvlog.uxdelivery.com.br/"
        self.url_ent_consulta = "http://vvlog.uxdelivery.com.br/Entregas/EntregaConsulta"

        #self.nova_execucao_processo()

    ################################################################################################################################
    # CONFIGURAÇÕES DO BROWSER
    ################################################################################################################################
    def carregar_dados(self):
        """Carrega dos dados para login dentro do PCOM"""

        try:
            bd = Database()
            self.__dados = bd.select_dados('SELECT * FROM tb_usuario WHERE id = 1')
            self.__usuario = self.__dados[0][1]
            self.__senha = self.__dados[0][2]
            self.diretorio_download  = self.__dados[0][3]
            self.var_max_volume = self.__dados[0][4]

        except Exception as e:
            messagebox.showerror('Erro',f'Não foi possivel carregar os parametros.\n{e}')
            raise TypeError(e)

    def variaveis_ambiente(self):
        """carrega as variveis de ambiente responsavel pelo login"""
        # try:
            # self.__usuario = config('USER')
            # self.__senha = config('SENHA')
            # self.__usuario = os.environ.get('USER_TMS_UX')
            # self.__senha = os.environ.get('SENHA_TMS_UX')
        # except Exception as e:
        #     messagebox.showerror('',f'{e}')
        #     raise Exception('Erro de variaveis')

    def configuracao_driver_2(self, visivel: bool = True):
        """configura os parametros para o funcionamento do driver"""
        try:
            service = Service(executable_path=r'navegador\chromedriver.exe')
            chrome_exe_path = r'navegador\chrome.exe'
            options = webdriver.ChromeOptions()
            options.add_experimental_option(name='prefs', value={"download.default_directory": self.dir_download_temp,
                                                     "download.Prompt_for_download": False, 
                                                     "download.directory_upgrade": True})
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-popup-blocking')
            options.add_argument('--disable-infobars')
            options.add_argument('--disable-notifications')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-software-rasterizer')
            options.add_argument('--disable-logging')
            options.binary_location = chrome_exe_path
            if visivel:
                options.add_argument("--headless")
            self.driver = webdriver.Chrome(service=service, options=options)
            self.wait = WebDriverWait(self.driver, timeout=100)
            self.wait_2 = WebDriverWait(self.driver, timeout=500)
            self.driver.maximize_window()
            self.driver.get(self.url)

        except Exception as e:
            raise Exception(f'Erro ao configurar o chromedirver!\n{e}')

    def configuracao_driver(self, visivel: bool = True):
        """configura os paramentros para criação do driver"""
        try:

            options = Options()
            options.add_experimental_option(name='prefs', value={"download.default_directory": self.dir_download_temp,
                                                     "download.Prompt_for_download": False, 
                                                     "download.directory_upgrade": True})
            # mostra o browser em tempo de execução
            if visivel:
                options.add_argument("--headless")

            service = Service(executable_path=r'src\chromedriver.exe')
            self.driver = webdriver.Chrome(service=service, options=options)
            # self.driver = webdriver.Chrome(self.executa_processo_download_driver()) # type: ignore
            # self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options) # type: ignore
            self.wait = WebDriverWait(self.driver, timeout=30)
            self.driver.maximize_window()
            self.driver.get(self.url)


        except Exception as e:
            messagebox.showerror(title='', message=f'{e}')

    ################################################################################################################################
    # AÇÕES DO BROWSER
    ################################################################################################################################
    def valida_elemento(self,tipo, path):
        """verifica se o elemento esta presente na tela"""
        try: self.driver.find_element(by=tipo,value=path)
        except NoSuchElementException as e: return False
        return True

    def esperar_elemento(self, tipo, path, atividade: str = 'visivel', tempo_limite: int = 120):
        """aguarda até que o elemento apareça na tela"""
        try:
            tempo_inicial = time.time()
            if atividade == 'visivel':
                while True:
                    if self.valida_elemento(tipo, path): return True
                    time.sleep(2)
                    if time.time() - tempo_inicial > tempo_limite:
                        return False
            else:
                while True:
                    if not self.valida_elemento(tipo, path): return True
                    time.sleep(2)
                    if time.time() - tempo_inicial > tempo_limite:
                        return False

        except Exception as e:
            messagebox.showerror(title='',message=f'{e}')
    
    ################################################################################################################################
    # EXECUÇÃO DO BROWSER
    ################################################################################################################################

    def login_usuario(self):
        """realiza o login do usuario"""
        try:
            id_login = "login"
            id_senha = "senha"
            xpt_button = '//button[text()="ENTRAR"]'
            self.wait.until(EC.element_to_be_clickable((By.ID, id_login))).send_keys(self.__usuario)
            self.wait.until(EC.element_to_be_clickable((By.ID, id_senha))).send_keys(self.__senha)
            time.sleep(1)
            self.wait.until(EC.element_to_be_clickable((By.ID, id_senha))).send_keys(Keys.ENTER)
            # self.driver.find_element(By.XPATH, xpt_button).send_keys(Keys.ENTER)
            # self.driver.execute_script("arguments[0].click();", self.wait.until(EC.element_to_be_clickable((By.XPATH, xpt_button))))

            # verificação de acesso
            if self.verifica_acesso():
                pass
            else:
                raise

        except Exception as e:
            raise Exception('Erro de Login')

    def verifica_acesso(self):
        """verifica se o acesso foi concluido com sucesso"""
        try:
            xpt_erro = '//h4[contains(text(),"Acesso Negado!")]'

            if self.valida_elemento(By.XPATH, xpt_erro):
                messagebox.showwarning(title='Atenção', message='Acesso Negado!\nVerifque suas credencias e tente novamente')
                return False
            return True
        except Exception as e:
            messagebox.showerror(title='',message=f'{e}')
            raise Exception('Erro ao validar acesso')

    def acesso_tela(self, url):

        """navega até a tela correspondente"""

        try:
            self.driver.get(url)

        except Exception as e:
            messagebox.showerror(title='', message=f'{e}')

    def select_tipo_busca(self, pesquisar_por: str):
        """seleciona o tipo de busca para consulta"""

        try:

            id_busca = 'tipoBusca'
            campo_busca = Select(self.driver.find_element(By.ID, id_busca))
            campo_busca.select_by_value(pesquisar_por)

        except Exception as e:
            messagebox.showerror(title='', message=f'{e}')

    def select_tipo_saida(self):

        """seleciona o tipo de saida em excel"""

        try:

            id_excel = 'tipoSaida'
            campo_busca = Select(self.driver.find_element(By.ID, id_excel))
            campo_busca.select_by_value('excel')

        except Exception as e:
            messagebox.showerror(title='', message=f'{e}')

    ################################################################################################################################
    # EXECUÇÃO DE CONSULTA DOCUMENTOS
    ################################################################################################################################
    def nova_execucao_processo(self):
        """executa o processo de consulta dentro do tms"""
        try:

            fnc = FuncoesAux()
            # self.var_max_volume  = 15000
            self.var_max_volume = 50000  #TODO APAGAR VARIAVEL

            self.tela_de_consulta()
            lista_dados = self.formatacao_numero_entrega(self.var_max_volume, self.lista_pesquisa)
            fnc.remover_arquivo(dir_download_file=self.dir_download_temp, nome_arquivo='entregas_consulta')
            dados = self.administrador_de_paginas(lista_dados)
            self.aguarda_download(caminho=self.dir_download_temp)

            dados_ponto = fnc.concatenar_arquivos_csv_massivo(diretorio=self.dir_download_temp,
                                                              salvar_em=self.dir_download_temp,
                                                              nome_arquivo='entregas_consulta')
            
            dados_ponto.to_csv(path_or_buf='saida_concatenada.csv', sep=';', encoding='latin-1')

            for dado in dados:
                print(f"{dado['fonte']}: {dado['consulta']} - {dado['descricao']}")

        except Exception as e:

            messagebox.showerror(title='', message=f'{e}')

    def executa_processo_consulta(self):
        """executa o processo de consulta com os volumes capturados"""
        try:
            pass
        except Exception as e:
            messagebox.showerror(title='',message= f'{e}')

    def inserir_valores(self, id: str, texto: str):

        """executa a colagem dos dados dentro do campo"""

        try:

            logger.success(f'num_lista_{id}')
            id_text_area = 'valorBusca'
            text_area = self.driver.find_element(By.ID, id_text_area)
            colar_win.copy("")
            colar_win.copy(texto)
            text_area.send_keys(Keys.CONTROL + "v")
            
        except Exception as e:
            messagebox.showerror(title='', message=f'{e}')

    def verifica_barra_progresso(self, xpt_barra, xpt_progresso, id_pesquisa, percentual_atual, tentativa):
        """acompanha o processo de download do arquivo"""
        
        if self.esperar_elemento(By.ID, xpt_barra):
            percentual_antigo = percentual_atual
            contagem = tentativa
                #verifica se percentua da barra de progresso chegou a 100%

            try:

                time.sleep(2)
                percentual = self.driver.find_element(By.XPATH, xpt_progresso).text
                logger.debug(f'execução {id_pesquisa} em {percentual}')

                if percentual == '100%':
                    return percentual, contagem
                else:
                    if percentual == percentual_antigo:
                        contagem += 1

                    if contagem == 5:
                        percentual = 'erro'
                        logger.error(f'{id_pesquisa}: Tempo de Carregamento excedido')

                    return percentual, contagem
                
            except Exception as e:
                logger.error(f'Erro na espera do donwload!!\n{e}')
                return False

    def erro_processamento(self):
        """Verifica se ouve algum status de erro durante o processo"""
        try:
            # xpt = '//div[@id="swal2-content" and contains(text(),"A consulta não retornou nenhum resultado!")]'
            time.sleep(2)
            id_erro = 'swal2-content'
            xpath_btn_erro = '//button[text()="OK"]'
            if self.valida_elemento(By.ID, id_erro):
                valor = self.driver.find_element(By.ID, id_erro).text
                self.driver.find_element(By.XPATH, xpath_btn_erro).click()
                return valor
            return ''
        except Exception as e:
            messagebox.showerror( title='', message=f'{e}')
            raise Exception(e)

    ################################################################################################################################
    # ADMINISTRADOR DE PROCESSO
    ################################################################################################################################
    def formatacao_numero_entrega(self, qtd_doc: int, lista_doc: list):

        """realiza a formatação e saparação por quantidade para consulta criando dicionarios"""

        try:

            logger.debug(f'Total de volumes: {len(lista_doc)}')
            # sepera em grupos de acordo com a quantidade maxima
            nova_lista: list = []
            contador = 1

            for dict_dados in lista_doc:

                fonte = dict_dados['fonte']
                pesquisar_por = dict_dados['pesquisar_por']
                documentos = dict_dados['lista_doc']

                for idx, volume in enumerate(range(0, len(documentos), qtd_doc)):

                    lista = documentos[volume:volume+qtd_doc]
                    concat_doc = "\n".join(map(str, lista))
                    dct_consulta: dict = {}
                    dct_consulta['fonte'] = fonte
                    dct_consulta['pesquisar_por'] = pesquisar_por
                    dct_consulta['consulta'] = f'Consulta {idx + 1}'
                    dct_consulta['qtd_pedidos'] = len(lista)
                    dct_consulta['descricao'] = ''
                    dct_consulta['status'] = 'inserindo_listagem'
                    dct_consulta['entrega'] = concat_doc
                    dct_consulta['id_web'] = ''
                    dct_consulta['percentual'] = '0%'
                    dct_consulta['tentativa_percent'] = 1
                    dct_consulta['tentativa'] = 0
                    nova_lista.append(dct_consulta.copy())
                    contador += 1

            return nova_lista

        except Exception as e:

            print(e)

            return []

    def duplicar_paginas(self, qtd_paginas):

        """multiplica as paginas para consulta"""

        try:

            url_atual = self.driver.current_url
            if qtd_paginas > 1:
                for pag in range(0, qtd_paginas - 1):
                    self.driver.execute_script(f"window.open('{url_atual}', '_blank');")

            lista_id_paginas = self.driver.window_handles

            return lista_id_paginas

        except Exception as e:
            print(e)  
            return []

    def insere_id_web(self, lista_paginas: list, lista_id_web: list):

        """insere o id para cada consulta"""

        for idx, id_web in enumerate(lista_id_web):
            lista_paginas[idx]['id_web'] = id_web

        return lista_paginas

    def administrador_de_paginas(self, lista_paginas: list):

        """gerencia o status das paginas e ações"""

        try:

            self.contador_pagina = 0
            self.contador_registro = 0
            ativ_concluidas = 0
            lista_id_aba = self.duplicar_paginas(len(lista_paginas))
            lista_paginas = self.insere_id_web(lista_paginas=lista_paginas, lista_id_web=lista_id_aba)
            lista_log = ['processo_concluido', 'erro_de_execucao', 'nenhum_registro_encontrado', 'erro_de_formato']

            while True:

                for pagina in lista_paginas:
                    logger.info(f'{pagina["consulta"]}: {pagina["status"]}',"#"*10)

                    # verifica se ainda existe alguma etapa pendente:
                    if str(pagina['status']) not in lista_log:

                        self.navegar_abas(str(pagina['id_web']))
                        status_atual, descricao, percentual, tentativa_percent, tentativa = self.acao(dados_pagina=pagina)
                        pagina['status'] = status_atual
                        pagina['descricao'] = descricao
                        pagina['percentual'] = percentual
                        pagina['tentativa_percent'] = tentativa_percent
                        pagina['tentativa'] = tentativa

                        if int(pagina['tentativa']) > 2:
                            pagina['status'] = 'erro_de_execucao'

                        # verifica se a etapa foi concluida
                        if str(pagina['status']) in lista_log:
                            ativ_concluidas += 1

                        # verifica quantas atividades ja foram concluidas
                        if ativ_concluidas == len(lista_paginas):
                            return lista_paginas

        except Exception as e:
            print(e)     

    def acao(self, dados_pagina: dict):
        """realiza determinada ação com base no status passado"""
        try:

            match str(dados_pagina['status']):

                case 'inserindo_listagem':

                    try:
                        self.select_tipo_busca(dados_pagina['pesquisar_por'])
                        self.select_tipo_saida()
                        self.inserir_valores(dados_pagina['consulta'],dados_pagina['entrega'])

                        # inicia a pesquisa
                        name_pesquisar = '//input[@type="button" and @value="Buscar"]'
                        self.wait.until(EC.element_to_be_clickable((By.XPATH, name_pesquisar))).click()
                        # valida erros
                        if (erro := self.erro_processamento()):
                            logger.error(f'{dados_pagina["consulta"]}: Erro de processo')
                            return 'erro_de_execucao', erro, '0%', 1, 3

                        return 'aguardando_carregar', '', '0%', 1, 1
                    
                    except TimeoutException or NoSuchElementException as e:
                        return 'erro_de_execucao', ''

                    except Exception as e:
                        raise Exception(e)
                    
                case 'aguardando_carregar':

                    try:
                        xp_download = 'btDownload'
                        xpt_barra = 'barraProgressoExcel'
                        xpt_progresso = '//div[@id="barraProgressoExcel"]/div'
                        # verificação a progressão da barra de carregamento
                        if (erro := self.erro_processamento()):
                            logger.error(f'{dados_pagina["consulta"]}: {erro}')
                            return 'erro_de_execucao', erro, '0%', 1, 3
                        
                        tentativa_exec = dados_pagina['tentativa']
                        percentual, tentativa_percent = self.verifica_barra_progresso(xpt_barra,
                                                                               xpt_progresso, 
                                                                               dados_pagina['consulta'], 
                                                                               dados_pagina['percentual'],
                                                                               dados_pagina['tentativa_percent'])
                        if percentual == '100%':         
                            return 'aguardando_importar_excel', '', percentual, tentativa_percent, tentativa_exec
                        
                        elif "%" in percentual:
                            time.sleep(randint(a=1, b=2))
                            return 'aguardando_carregar', '', percentual, tentativa_percent, tentativa_exec
                        else:
                            incr_tentativa = tentativa_exec + 1
                            self.driver.refresh()
                            logger.warning(f'{dados_pagina["consulta"]}: Percentual parado reiniciando... tentativas{dados_pagina["tentativa"]}')
                            return 'inserindo_listagem', '', percentual, 1, incr_tentativa
                    
                    except TimeoutException or NoSuchElementException as e:
                        return 'erro_de_execucao', ''
                    except Exception as e:
                        raise Exception(e)
                                        
                case 'aguardando_importar_excel':
                    try:
                        name_pesquisar = '//input[@type="button" and @value="Buscar"]'
                        xp_download = 'btDownload'
                        if self.esperar_elemento(By.ID, xp_download):
                            self.wait.until(EC.element_to_be_clickable((By.ID, xp_download))).click()
                            logger.success(f'{dados_pagina["consulta"]}: realizando impressão!!!')
                            if (erro := self.erro_processamento()):
                                logger.error(f'{dados_pagina["consulta"]}: Erro de processo')
                                return 'erro_de_execucao', erro, '0%', 1, 3
                            
                        return 'processo_concluido', \
                               'Processo Concluido', \
                                dados_pagina['percentual'], \
                                dados_pagina['tentativa_percent'], \
                                dados_pagina['tentativa']
                    
                    except TimeoutException or NoSuchElementException as e:
                        return 'erro_de_execucao', '', '', ''
                    except Exception as e:
                        raise Exception(e)

                case _:
                    pass
            
        except Exception as e:
            print(e)

    def navegar_abas(self, id_aba: str):
        """acessa a aba plo ai"""

        try:
            self.driver.switch_to.window(id_aba)
        except Exception as e:
            print(e)

    def tela_de_consulta(self):

        """navega até a tela de consulta"""

        try:
            # inicialização da tela
            self.configuracao_driver_2(visivel=False)
            # login
            self.login_usuario()
            time.sleep(2)
            self.acesso_tela(self.url_ent_consulta)
            xpt_titulo = '//h3[contains(text()," Filtros de Busca")]'

            # esperar tela ser carregada
            if self.esperar_elemento(tipo=By.XPATH, path=xpt_titulo, atividade='visivel'):
                #self.select_tipo_busca("Nro. Entrega")
                self.select_tipo_saida()
            else:
                raise Exception('Tempo esgotado para o carregamento da tela')
            # filtros

        except Exception as e:
            print(e)

