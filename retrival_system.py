from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from build_system import Data_prepossed

class UI_window(QWidget):
    def select_iden(self):
        self.level=self.cblevel.currentText()
        self.level_dic={'游客':1,'学生':2,'教师':3,'管理员':4}
        self.level=self.level_dic[self.level]
    def select_query(self):
        self.query_method=self.cbquery.currentText()
    def textchanged(self,text):
        self.query=text
        print ("contents of text box: "+text)
    def search_click(self,reader):
        
        if self.query_method=='网页':
            result=reader.create_web_index(self.query,self.level)
        else:
            result=Reader.create_file_index('./file_data.json',self.query,self.level) 
        
        
        self.query_result.addItem(result)
        
        return
    def setupUI(self,reader):
        self.setWindowTitle('今日哈工大信息检索')
        self.layout=QGridLayout()
        self.cblevel=QComboBox()
        self.cblevel.addItems(['游客','学生','教师','管理员'])
        self.cblevel.currentIndexChanged.connect(self.select_iden)
        self.cbquery=QComboBox()
        self.cbquery.addItems(['网页','附件'])
        self.cbquery.currentIndexChanged.connect(self.select_query)
        self.queryline=QLineEdit()
        self.queryline.textChanged.connect(self.textchanged)
        self.query_button=QPushButton('查询')
        self.query_button.clicked.connect(lambda:self.search_click(reader))
        self.query_result=QListWidget()
        self.layout.addWidget(self.cblevel, 0, 0)
        self.layout.addWidget(self.cbquery,0,2)
        self.layout.addWidget(QLabel('请输入要查询的内容'),1,0)
        self.layout.addWidget(self.queryline, 1, 2,1,4)
        self.layout.addWidget(self.query_button,2,0)
        self.layout.addWidget(self.query_result, 3, 0, 3, 5)
        # Set the layout on the application's window
        self.setLayout(self.layout)

        
    
if __name__=='__main__':
    app=QtWidgets.QApplication(sys.argv)
    Reader=Data_prepossed()
    UI=UI_window()
    UI.setupUI(Reader)
    UI.show()
    sys.exit(app.exec_())