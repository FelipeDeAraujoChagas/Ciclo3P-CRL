from controller.mainTelas import TelaLogin, TelaContener
from PyQt5.QtWidgets import QApplication

class Main:

    def main(self):

        import sys
        app = QApplication(sys.argv)
        #tela = TelaLogin()
        tela = TelaContener("2901885626")
        tela.show()
        sys.exit(app.exec_())


if __name__ == "__main__":
    Main().main()
