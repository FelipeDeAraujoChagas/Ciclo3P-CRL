from views.tela_contener import Ui_RPA
from views.tela_login import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QLineEdit, QApplication
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from data.data_base_sql import DataBaseSQL, ConsultaTabelas
import pandas as pd
from tkinter import filedialog


class TelaLogin(QMainWindow):
    def __init__(self):

        super().__init__()
        self.user = None
        self.login = Ui_MainWindow()
        self.login.setupUi(self)
        self.login.frame_erro.setVisible(False)
        self.login.pushButton_cluse_pupup.clicked.connect(self.messagemFechar)
        self.login.pushButton_login.clicked.connect(self.consultarUsuario)
        self.login.pushButton_OlhoMagico.clicked.connect(lambda: self.toggle_echo_mode(self.login.lineEdit_user_2))

    def messagemErro(self, msg):

        self.login.label_erro.setText(msg)
        self.login.frame_erro.setVisible(True)

    def messagemFechar(self):

        self.login.frame_erro.setVisible(False)

    def mudaJanela(self):

        self.contener = TelaContener(user=self.user)
        self.contener.show()
        self.hide()

    def consultarUsuario(self):

        usuario = self.login.lineEdit_user.text()
        password = self.login.lineEdit_user_2.text()
        self.user = usuario

        if usuario == "":
            self.login.label_erro.setText(f'Informe o usuário')
            self.login.frame_erro.setVisible(True)
            return

        if password == '':
            self.login.label_erro.setText(f'Informe a senha')
            self.login.frame_erro.setVisible(True)
            return

        try:
            sqlserve = ConsultaTabelas()
            tb_usuario: pd.DataFrame = sqlserve.consultarUsuarios(usuario=usuario, password=password)
            user = tb_usuario.iloc[0, 1]

            if usuario == user:

                from controller.validarApp import AtivacaoApp
                aplicativoAtivo = AtivacaoApp("Base Ciclo 3p - CRL")

                if aplicativoAtivo.appAtivo:
                    self.mudaJanela()
                else:
                    self.login.label_erro.setText(f'{aplicativoAtivo.motivo}')
                    self.login.frame_erro.setVisible(True)

        except:

            self.login.label_erro.setText(f'Usuario não encontrado')
            self.login.frame_erro.setVisible(True)

    def toggle_echo_mode(self, line_edit):

        current_mode = line_edit.echoMode()
        # Alternar entre Normal e Password
        new_mode = (
            QLineEdit.Normal
            if current_mode == QLineEdit.Password
            else QLineEdit.Password
        )

        line_edit.setEchoMode(new_mode)


class TelaContener(QMainWindow, Ui_RPA):

    def __init__(self, user):
        super().__init__()
        self.setupUi(self)
        self.frame_MessagemUser.setVisible(False)
        self.label_user.setText(user)
        self.stackedWidget.setCurrentIndex(0)

        # Botões do menu lateral esquerdo
        self.pushButton_Colaborador.clicked.connect(lambda: self.show_page('page_User'))
        self.pushButton_inserirUsuario.clicked.connect(lambda: self.show_page('page_inserir_Usuario'))
        self.pushButton_Home.clicked.connect(lambda: self.show_page('page_Home'))
        self.pushButton_arrowvoltarUser.clicked.connect(lambda: self.show_page('page_User'))
        self.pushButton_Rotinas.clicked.connect(lambda: self.show_page('page_AreaImput'))
        self.pushButton_Tarefa.clicked.connect(lambda: self.show_page('page_Divisao_Tarefa'))

        # Botoes tela usuarios
        self.pushButton_consultarUsuario.clicked.connect(self.getDadosColaborador)
        self.pushButton_inserirUser.clicked.connect(self.inserirUser)
        self.pushButton_senhaVisivel.clicked.connect(lambda: self.toggle_echo_mode(self.lineEdit_senha))
        self.pushButton_senha2visivel.clicked.connect(lambda: self.toggle_echo_mode(self.lineEdit_senhaConfirma))
        self.pushButton_messageInserirUser.clicked.connect(lambda: self.frame_MessagemUser.setVisible(False))
        self.pushButton_DeletarUsuario.clicked.connect(self.deleteUser)

        # Botoes tela AreaInput
        self.pushButton_1_trattv_base.clicked.connect(lambda: self.importaArquivo(lineEdit=self.lineEdit_1_tratativa))
        self.pushButton_2_DataFormatado.clicked.connect(lambda: self.importaArquivo(lineEdit=self.lineEdit_2_DtFormatado))
        self.pushButton_3_BaseValidacao.clicked.connect(lambda: self.importaArquivo(lineEdit=self.lineEdit_3_BsValidacao))
        self.pushButton_4_Ciclo.clicked.connect(lambda: self.importaArquivo(lineEdit=self.lineEdit_4_Ciclo))
        self.pushButton_PlayRotina.clicked.connect(self.PlayRotina)

    def show_page(self, nome_page):

        pageBook = {
            'page_Home': 0,
            'page_Divisao_Tarefa': 1,
            'page_AreaImput': 2,
            'page_User': 3,
            'page_inserir_Usuario': 4
        }
        index = pageBook.get(nome_page)
        self.stackedWidget.setCurrentIndex(index)

    def importaArquivo(self, lineEdit):

        arquivo = filedialog.askopenfilename(filetypes=(("Arquivo Excel", '*.xls*'), ('Todos Arquivos', '*.*')))
        lineEdit.setText(f'{str(arquivo)}')

    def PlayRotina(self):


        from controller.app import Run
        play = Run(text_edit=self.textEdit)

        play.tratativaBases(
            arqFullfilment=self.lineEdit_1_tratativa.text(),
            arqDataFormatado=self.lineEdit_2_DtFormatado.text(),
            arqValidacao=self.lineEdit_3_BsValidacao.text(),
            arqCliclo=self.lineEdit_4_Ciclo.text()
        )
        play.tmsUX()
        play.analiseBases()


    def irTelaUser(self):

        self.stackedWidget.setCurrentIndex(2)
        self.getDadosColaborador()

    def getDadosColaborador(self):

        data = DataBaseSQL()
        sql = ''' select id_usuario, matricula, dataIntegracao, usuarioResgitro from Tbl_Usuarios '''
        tbUsuario: pd.DataFrame = data.select_dados(sql)
        self.modelUsuario = QStandardItemModel(self)

        if self.modelUsuario.rowCount() > 0:
            self.modelUsuario.clear()

        self.modelUsuario.setHorizontalHeaderLabels(tbUsuario.columns)

        for k, v in tbUsuario.iterrows():
            row = [QStandardItem(str(cell)) for cell in v]
            self.modelUsuario.appendRow(row)

        self.tableView_usuario.setModel(self.modelUsuario)
        self.tableView_usuario.resizeColumnToContents(0)

    def inserirUser(self):

        novoUser = self.lineEdit_novoUser.text()
        senha = self.lineEdit_senha.text()
        confirmacao = self.lineEdit_senhaConfirma.text()

        if novoUser == "":
            self.label_MessageUser.setText("O usuario não pode estar em branco!")
            self.frame_MessagemUser.setVisible(True)
            return

        if senha != confirmacao:
            self.label_MessageUser.setText("senhas não confere!")
            self.frame_MessagemUser.setVisible(True)
            return

        try:
            userLogado = self.label_user.text()
            data = ConsultaTabelas()

            if not data.consultarUserExiste(novoUser):
                sql2 = f'''insert into Tbl_Usuarios Values ('{novoUser}','{senha}',GETDATE(),'{userLogado}')'''
                data.insert_dados(sql2)
                self.frame_MessagemUser.setStyleSheet(f"background-color: #038C3E")
                self.label_MessageUser.setText("Usuario inserido com sucesso!")
                self.frame_MessagemUser.setVisible(True)
                self.lineEdit_novoUser.text('')
                self.lineEdit_senha.text('')
                self.lineEdit_senhaConfirma.text('')
            else:
                self.label_MessageUser.setText("Usuario já existe")
                self.frame_MessagemUser.setVisible(True)
        except:
            pass

    def toggle_echo_mode(self, line_edit):

        current_mode = line_edit.echoMode()
        # Alternar entre Normal e Password
        new_mode = (
            QLineEdit.Normal
            if current_mode == QLineEdit.Password
            else QLineEdit.Password
        )

        line_edit.setEchoMode(new_mode)

    def deleteUser(self):

        try:
            selected_index = self.tableView_usuario.selectionModel().currentIndex()
            if selected_index.isValid():
                item = self.modelUsuario.item(selected_index.row(), column=0).text()
                data = DataBaseSQL()
                data.delete_dados(f"delete from Tbl_Usuarios Where id_usuario = '{item}'")
                self.getDadosColaborador()

        except:

            print('Faiou')
            pass
