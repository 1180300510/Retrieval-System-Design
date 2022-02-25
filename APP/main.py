from forms.ui import Ui_Dialog
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog
import sys

#分别创建两个UI类，一个作为登录界面，一个作为主界面
class Main_Window(QDialog,Ui_Dialog):
    def __init__(self):
        super(Main_Window,self).__init__()
        self.setupUi(self)


if __name__=='__main__':
    app=QtWidgets.QApplication(sys.argv)
    Mwindow=Main_Window()
    Mwindow.show()
    sys.exit(app.exec_())