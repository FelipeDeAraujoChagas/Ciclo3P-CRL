# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tela_contener.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_RPA(object):
    def setupUi(self, RPA):
        RPA.setObjectName("RPA")
        RPA.setWindowModality(QtCore.Qt.WindowModal)
        RPA.resize(1091, 781)
        RPA.setMinimumSize(QtCore.QSize(800, 600))
        self.centralwidget = QtWidgets.QWidget(RPA)
        self.centralwidget.setStyleSheet("\n"
"QPushButton {\n"
"    border: 2px solid rgb(52, 59, 72);\n"
"    border-radius: 5px;    \n"
"    background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(57, 65, 80);\n"
"    border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"QPushButton:pressed {    \n"
"    background-color: rgb(35, 40, 49);\n"
"    border: 2px solid rgb(43, 50, 61);\n"
"}\n"
"")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.top_menu = QtWidgets.QFrame(self.centralwidget)
        self.top_menu.setMinimumSize(QtCore.QSize(0, 48))
        self.top_menu.setMaximumSize(QtCore.QSize(16777215, 48))
        self.top_menu.setStyleSheet("background-color: rgb(0, 0, 255);")
        self.top_menu.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.top_menu.setFrameShadow(QtWidgets.QFrame.Raised)
        self.top_menu.setObjectName("top_menu")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.top_menu)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame = QtWidgets.QFrame(self.top_menu)
        self.frame.setMinimumSize(QtCore.QSize(50, 0))
        self.frame.setMaximumSize(QtCore.QSize(50, 16777215))
        self.frame.setStyleSheet("background-color: rgb(35, 35, 35);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(6, 4, 42, 42))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/logo/logo.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.frame)
        self.frame_2 = QtWidgets.QFrame(self.top_menu)
        self.frame_2.setStyleSheet("background-color: rgb(35, 35, 35);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.label_user = QtWidgets.QLabel(self.frame_2)
        self.label_user.setGeometry(QtCore.QRect(820, 20, 191, 16))
        self.label_user.setStyleSheet("color: rgb(200, 200, 200);")
        self.label_user.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_user.setObjectName("label_user")
        self.horizontalLayout_2.addWidget(self.frame_2)
        self.verticalLayout.addWidget(self.top_menu)
        self.context = QtWidgets.QFrame(self.centralwidget)
        self.context.setStyleSheet("background-color: rgb(20, 20, 20);")
        self.context.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.context.setFrameShadow(QtWidgets.QFrame.Raised)
        self.context.setObjectName("context")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.context)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.left_menu = QtWidgets.QFrame(self.context)
        self.left_menu.setMinimumSize(QtCore.QSize(64, 0))
        self.left_menu.setMaximumSize(QtCore.QSize(64, 16777215))
        self.left_menu.setStyleSheet("QWidget{\n"
"    color: rgb(218, 218, 218);\n"
"    font: 10pt \"Segoe UI\";\n"
"}\n"
"\n"
"\n"
"QPushButton {\n"
"    border: 1px solid #555;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    border: 2px solid rgb(177,209,250);\n"
"    padding: 6px;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"    background-color: rgb(177,209,250);\n"
"    border: 2px solid rgb(0, 0, 249);\n"
"    color: rgb(0, 0, 127);    \n"
"}\n"
"")
        self.left_menu.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.left_menu.setFrameShadow(QtWidgets.QFrame.Raised)
        self.left_menu.setObjectName("left_menu")
        self.frame_4 = QtWidgets.QFrame(self.left_menu)
        self.frame_4.setGeometry(QtCore.QRect(2, 40, 60, 45))
        self.frame_4.setMaximumSize(QtCore.QSize(16777215, 45))
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.pushButton_loteMenu = QtWidgets.QPushButton(self.frame_4)
        self.pushButton_loteMenu.setGeometry(QtCore.QRect(0, 0, 60, 45))
        self.pushButton_loteMenu.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/boger/icon_menu.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_loteMenu.setIcon(icon)
        self.pushButton_loteMenu.setCheckable(False)
        self.pushButton_loteMenu.setObjectName("pushButton_loteMenu")
        self.frame_5 = QtWidgets.QFrame(self.left_menu)
        self.frame_5.setGeometry(QtCore.QRect(2, 90, 60, 45))
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.pushButton_Home = QtWidgets.QPushButton(self.frame_5)
        self.pushButton_Home.setGeometry(QtCore.QRect(0, 0, 60, 45))
        self.pushButton_Home.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/home/cil-home.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_Home.setIcon(icon1)
        self.pushButton_Home.setObjectName("pushButton_Home")
        self.frame_6 = QtWidgets.QFrame(self.left_menu)
        self.frame_6.setGeometry(QtCore.QRect(2, 240, 60, 45))
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.pushButton_Colaborador = QtWidgets.QPushButton(self.frame_6)
        self.pushButton_Colaborador.setGeometry(QtCore.QRect(0, 0, 60, 45))
        self.pushButton_Colaborador.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/colaboradores/cil-people.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_Colaborador.setIcon(icon2)
        self.pushButton_Colaborador.setObjectName("pushButton_Colaborador")
        self.frame_8 = QtWidgets.QFrame(self.left_menu)
        self.frame_8.setGeometry(QtCore.QRect(2, 140, 60, 45))
        self.frame_8.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_8.setObjectName("frame_8")
        self.pushButton_Rotinas = QtWidgets.QPushButton(self.frame_8)
        self.pushButton_Rotinas.setGeometry(QtCore.QRect(0, 0, 60, 45))
        self.pushButton_Rotinas.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/camadas/cil-layers.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_Rotinas.setIcon(icon3)
        self.pushButton_Rotinas.setObjectName("pushButton_Rotinas")
        self.frame_9 = QtWidgets.QFrame(self.left_menu)
        self.frame_9.setGeometry(QtCore.QRect(2, 190, 60, 45))
        self.frame_9.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_9.setObjectName("frame_9")
        self.pushButton_Tarefa = QtWidgets.QPushButton(self.frame_9)
        self.pushButton_Tarefa.setGeometry(QtCore.QRect(0, 0, 60, 45))
        self.pushButton_Tarefa.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/fogo/cil-fire.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_Tarefa.setIcon(icon4)
        self.pushButton_Tarefa.setObjectName("pushButton_Tarefa")
        self.horizontalLayout.addWidget(self.left_menu)
        self.contest_right = QtWidgets.QFrame(self.context)
        self.contest_right.setStyleSheet("background-color: rgb(160, 160, 210);\n"
"")
        self.contest_right.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.contest_right.setFrameShadow(QtWidgets.QFrame.Raised)
        self.contest_right.setObjectName("contest_right")
        self.gridLayout = QtWidgets.QGridLayout(self.contest_right)
        self.gridLayout.setObjectName("gridLayout")
        self.frame_3 = QtWidgets.QFrame(self.contest_right)
        self.frame_3.setStyleSheet("background-color: rgb(40, 44, 52);\n"
"border-stayle: solid;\n"
"border-radius: 10px;\n"
"color: rgb(200,200,200)\n"
"\n"
"")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_3)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.stackedWidget = QtWidgets.QStackedWidget(self.frame_3)
        self.stackedWidget.setStyleSheet("QLineEdit{\n"
"    border: 2px solid rgb(45,45,45);\n"
"    border-radiius: 3px;\n"
"    padding: 15px;\n"
"    background-color: rgb(30,30,30);\n"
"    color: rgb(177,177,177);\n"
"}\n"
"\n"
"QLineEdit:hover{\n"
"    border: 2px solid rgb(100, 100, 120);    \n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 2px solid rgb(177, 209, 250);    \n"
"    color: rgb(230,230,230);\n"
"}\n"
"\n"
"QTextEdit{\n"
"    border: 2px solid rgb(45,45,45);\n"
"    border-radiius: 3px;\n"
"    padding: 15px;\n"
"    background-color: rgb(30,30,30);\n"
"    color: rgb(230,230,230);\n"
"}\n"
"\n"
"QTextEdit:hover{\n"
"    border: 2px solid rgb(100, 100, 120);    \n"
"}\n"
"\n"
"QLTextEdit:focus {\n"
"    border: 2px solid rgb(177, 209, 250);    \n"
"    color: rgb(200,200,200);\n"
"}\n"
"\n"
"\n"
"QPushButton{\n"
"    background-color: rgb(52, 59, 72);\n"
"    border: 2px solid rgb(60,60,60);\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgb(70,70,70);\n"
"    border: 2px solid rgb(177,209,250);    \n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"    background-color: rgb(177,209,250);\n"
"    border: 2px solid rgb(177, 185, 249);\n"
"    color: rgb(0, 0, 127);    \n"
"}\n"
"\n"
"")
        self.stackedWidget.setObjectName("stackedWidget")
        self.page_Home = QtWidgets.QWidget()
        self.page_Home.setObjectName("page_Home")
        self.frame_7 = QtWidgets.QFrame(self.page_Home)
        self.frame_7.setGeometry(QtCore.QRect(330, 140, 301, 221))
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.label_2 = QtWidgets.QLabel(self.frame_7)
        self.label_2.setGeometry(QtCore.QRect(40, 20, 231, 181))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap(":/logo/logo.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.stackedWidget.addWidget(self.page_Home)
        self.page_Divisao_Tarefa = QtWidgets.QWidget()
        self.page_Divisao_Tarefa.setObjectName("page_Divisao_Tarefa")
        self.tableView = QtWidgets.QTableView(self.page_Divisao_Tarefa)
        self.tableView.setGeometry(QtCore.QRect(80, 90, 691, 481))
        self.tableView.setObjectName("tableView")
        self.pushButton = QtWidgets.QPushButton(self.page_Divisao_Tarefa)
        self.pushButton.setGeometry(QtCore.QRect(820, 190, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.page_Divisao_Tarefa)
        self.pushButton_2.setGeometry(QtCore.QRect(820, 240, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.stackedWidget.addWidget(self.page_Divisao_Tarefa)
        self.page_AreaImput = QtWidgets.QWidget()
        self.page_AreaImput.setObjectName("page_AreaImput")
        self.lineEdit_1_tratativa = QtWidgets.QLineEdit(self.page_AreaImput)
        self.lineEdit_1_tratativa.setGeometry(QtCore.QRect(120, 50, 471, 51))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.lineEdit_1_tratativa.setFont(font)
        self.lineEdit_1_tratativa.setReadOnly(True)
        self.lineEdit_1_tratativa.setObjectName("lineEdit_1_tratativa")
        self.lineEdit_2_DtFormatado = QtWidgets.QLineEdit(self.page_AreaImput)
        self.lineEdit_2_DtFormatado.setGeometry(QtCore.QRect(120, 140, 471, 51))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.lineEdit_2_DtFormatado.setFont(font)
        self.lineEdit_2_DtFormatado.setReadOnly(True)
        self.lineEdit_2_DtFormatado.setObjectName("lineEdit_2_DtFormatado")
        self.lineEdit_3_BsValidacao = QtWidgets.QLineEdit(self.page_AreaImput)
        self.lineEdit_3_BsValidacao.setGeometry(QtCore.QRect(120, 230, 471, 51))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.lineEdit_3_BsValidacao.setFont(font)
        self.lineEdit_3_BsValidacao.setReadOnly(True)
        self.lineEdit_3_BsValidacao.setObjectName("lineEdit_3_BsValidacao")
        self.pushButton_1_trattv_base = QtWidgets.QPushButton(self.page_AreaImput)
        self.pushButton_1_trattv_base.setGeometry(QtCore.QRect(660, 50, 121, 51))
        self.pushButton_1_trattv_base.setObjectName("pushButton_1_trattv_base")
        self.pushButton_2_DataFormatado = QtWidgets.QPushButton(self.page_AreaImput)
        self.pushButton_2_DataFormatado.setGeometry(QtCore.QRect(660, 140, 121, 51))
        self.pushButton_2_DataFormatado.setObjectName("pushButton_2_DataFormatado")
        self.pushButton_3_BaseValidacao = QtWidgets.QPushButton(self.page_AreaImput)
        self.pushButton_3_BaseValidacao.setGeometry(QtCore.QRect(660, 230, 121, 51))
        self.pushButton_3_BaseValidacao.setObjectName("pushButton_3_BaseValidacao")
        self.pushButton_PlayRotina = QtWidgets.QPushButton(self.page_AreaImput)
        self.pushButton_PlayRotina.setGeometry(QtCore.QRect(410, 400, 181, 41))
        self.pushButton_PlayRotina.setObjectName("pushButton_PlayRotina")
        self.lineEdit_4_Ciclo = QtWidgets.QLineEdit(self.page_AreaImput)
        self.lineEdit_4_Ciclo.setGeometry(QtCore.QRect(120, 320, 471, 51))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.lineEdit_4_Ciclo.setFont(font)
        self.lineEdit_4_Ciclo.setReadOnly(True)
        self.lineEdit_4_Ciclo.setObjectName("lineEdit_4_Ciclo")
        self.pushButton_4_Ciclo = QtWidgets.QPushButton(self.page_AreaImput)
        self.pushButton_4_Ciclo.setGeometry(QtCore.QRect(660, 320, 121, 51))
        self.pushButton_4_Ciclo.setObjectName("pushButton_4_Ciclo")
        self.textEdit = QtWidgets.QTextEdit(self.page_AreaImput)
        self.textEdit.setGeometry(QtCore.QRect(100, 470, 771, 171))
        self.textEdit.setReadOnly(False)
        self.textEdit.setObjectName("textEdit")
        self.stackedWidget.addWidget(self.page_AreaImput)
        self.page_User = QtWidgets.QWidget()
        self.page_User.setObjectName("page_User")
        self.tableView_usuario = QtWidgets.QTableView(self.page_User)
        self.tableView_usuario.setGeometry(QtCore.QRect(160, 110, 471, 401))
        self.tableView_usuario.setStyleSheet("QHeaderView{color: #2933F4;}\n"
"")
        self.tableView_usuario.setObjectName("tableView_usuario")
        self.pushButton_consultarUsuario = QtWidgets.QPushButton(self.page_User)
        self.pushButton_consultarUsuario.setGeometry(QtCore.QRect(800, 120, 120, 30))
        self.pushButton_consultarUsuario.setStyleSheet("")
        self.pushButton_consultarUsuario.setObjectName("pushButton_consultarUsuario")
        self.pushButton_inserirUsuario = QtWidgets.QPushButton(self.page_User)
        self.pushButton_inserirUsuario.setGeometry(QtCore.QRect(800, 180, 120, 30))
        self.pushButton_inserirUsuario.setStyleSheet("")
        self.pushButton_inserirUsuario.setObjectName("pushButton_inserirUsuario")
        self.pushButton_DeletarUsuario = QtWidgets.QPushButton(self.page_User)
        self.pushButton_DeletarUsuario.setGeometry(QtCore.QRect(800, 240, 120, 30))
        self.pushButton_DeletarUsuario.setStyleSheet("")
        self.pushButton_DeletarUsuario.setObjectName("pushButton_DeletarUsuario")
        self.stackedWidget.addWidget(self.page_User)
        self.page_inserir_Usuario = QtWidgets.QWidget()
        self.page_inserir_Usuario.setObjectName("page_inserir_Usuario")
        self.lineEdit_novoUser = QtWidgets.QLineEdit(self.page_inserir_Usuario)
        self.lineEdit_novoUser.setGeometry(QtCore.QRect(340, 130, 280, 50))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.lineEdit_novoUser.setFont(font)
        self.lineEdit_novoUser.setObjectName("lineEdit_novoUser")
        self.lineEdit_senha = QtWidgets.QLineEdit(self.page_inserir_Usuario)
        self.lineEdit_senha.setGeometry(QtCore.QRect(340, 240, 280, 50))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.lineEdit_senha.setFont(font)
        self.lineEdit_senha.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_senha.setObjectName("lineEdit_senha")
        self.lineEdit_senhaConfirma = QtWidgets.QLineEdit(self.page_inserir_Usuario)
        self.lineEdit_senhaConfirma.setGeometry(QtCore.QRect(340, 350, 280, 50))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.lineEdit_senhaConfirma.setFont(font)
        self.lineEdit_senhaConfirma.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_senhaConfirma.setObjectName("lineEdit_senhaConfirma")
        self.pushButton_inserirUser = QtWidgets.QPushButton(self.page_inserir_Usuario)
        self.pushButton_inserirUser.setGeometry(QtCore.QRect(340, 470, 281, 61))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.pushButton_inserirUser.setFont(font)
        self.pushButton_inserirUser.setObjectName("pushButton_inserirUser")
        self.frame_MessagemUser = QtWidgets.QFrame(self.page_inserir_Usuario)
        self.frame_MessagemUser.setGeometry(QtCore.QRect(150, 20, 671, 42))
        self.frame_MessagemUser.setStyleSheet("background-color: rgb(255, 0, 127);\n"
"border-radius:5px;")
        self.frame_MessagemUser.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_MessagemUser.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_MessagemUser.setObjectName("frame_MessagemUser")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_MessagemUser)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_MessageUser = QtWidgets.QLabel(self.frame_MessagemUser)
        self.label_MessageUser.setStyleSheet("QLabel{\n"
"     color:rgb(35, 35, 35);\n"
"}")
        self.label_MessageUser.setAlignment(QtCore.Qt.AlignCenter)
        self.label_MessageUser.setObjectName("label_MessageUser")
        self.horizontalLayout_3.addWidget(self.label_MessageUser)
        self.pushButton_messageInserirUser = QtWidgets.QPushButton(self.frame_MessagemUser)
        self.pushButton_messageInserirUser.setMaximumSize(QtCore.QSize(20, 20))
        self.pushButton_messageInserirUser.setStyleSheet("QPushButton{\n"
"    background-image: url(:/close image/icon_close.png);\n"
"    border-raius: 5px;\n"
"    margin: 0px 0px 0px 0px ;\n"
"    background-position: center;    \n"
"    background-color: rgb(70, 70, 70);\n"
"    background-repeat: no-repeat;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color:rgb(40,40,40);\n"
"    color: rgb(200, 200, 200);\n"
"}\n"
"QpushButton:pressed{\n"
"    background-color: rgb(35,35,35);\n"
"    color: rgb(200, 200, 200);\n"
"}\n"
"")
        self.pushButton_messageInserirUser.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/exit/icon_close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_messageInserirUser.setIcon(icon5)
        self.pushButton_messageInserirUser.setObjectName("pushButton_messageInserirUser")
        self.horizontalLayout_3.addWidget(self.pushButton_messageInserirUser)
        self.pushButton_senhaVisivel = QtWidgets.QPushButton(self.page_inserir_Usuario)
        self.pushButton_senhaVisivel.setGeometry(QtCore.QRect(680, 250, 70, 32))
        self.pushButton_senhaVisivel.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/olhoMagico/cil-low-vision.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_senhaVisivel.setIcon(icon6)
        self.pushButton_senhaVisivel.setObjectName("pushButton_senhaVisivel")
        self.pushButton_senha2visivel = QtWidgets.QPushButton(self.page_inserir_Usuario)
        self.pushButton_senha2visivel.setGeometry(QtCore.QRect(680, 360, 70, 32))
        self.pushButton_senha2visivel.setText("")
        self.pushButton_senha2visivel.setIcon(icon6)
        self.pushButton_senha2visivel.setObjectName("pushButton_senha2visivel")
        self.pushButton_arrowvoltarUser = QtWidgets.QPushButton(self.page_inserir_Usuario)
        self.pushButton_arrowvoltarUser.setGeometry(QtCore.QRect(20, 590, 41, 31))
        self.pushButton_arrowvoltarUser.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/arrowVoltar/cil-account-logout.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_arrowvoltarUser.setIcon(icon7)
        self.pushButton_arrowvoltarUser.setObjectName("pushButton_arrowvoltarUser")
        self.stackedWidget.addWidget(self.page_inserir_Usuario)
        self.gridLayout_2.addWidget(self.stackedWidget, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.frame_3, 0, 0, 1, 1)
        self.horizontalLayout.addWidget(self.contest_right)
        self.verticalLayout.addWidget(self.context)
        RPA.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(RPA)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1091, 21))
        self.menubar.setObjectName("menubar")
        RPA.setMenuBar(self.menubar)

        self.retranslateUi(RPA)
        self.stackedWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(RPA)

    def retranslateUi(self, RPA):
        _translate = QtCore.QCoreApplication.translate
        RPA.setWindowTitle(_translate("RPA", "MainWindow"))
        self.label_user.setText(_translate("RPA", "user"))
        self.pushButton.setText(_translate("RPA", "PushButton"))
        self.pushButton_2.setText(_translate("RPA", "PushButton"))
        self.pushButton_1_trattv_base.setText(_translate("RPA", "Tratativa de Base"))
        self.pushButton_2_DataFormatado.setText(_translate("RPA", "Data Formatado"))
        self.pushButton_3_BaseValidacao.setText(_translate("RPA", "Base Validação"))
        self.pushButton_PlayRotina.setText(_translate("RPA", "Play"))
        self.pushButton_4_Ciclo.setText(_translate("RPA", "Base Ciclo"))
        self.pushButton_consultarUsuario.setText(_translate("RPA", "Consultar"))
        self.pushButton_inserirUsuario.setText(_translate("RPA", "inserir"))
        self.pushButton_DeletarUsuario.setText(_translate("RPA", "Deletar"))
        self.lineEdit_novoUser.setPlaceholderText(_translate("RPA", "novo usuario"))
        self.lineEdit_senha.setPlaceholderText(_translate("RPA", "senha"))
        self.lineEdit_senhaConfirma.setPlaceholderText(_translate("RPA", "Confirme senha"))
        self.pushButton_inserirUser.setText(_translate("RPA", "Inserir"))
        self.label_MessageUser.setText(_translate("RPA", "error"))
import views.file_contener_rc_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    RPA = QtWidgets.QMainWindow()
    ui = Ui_RPA()
    ui.setupUi(RPA)
    RPA.show()
    sys.exit(app.exec_())
