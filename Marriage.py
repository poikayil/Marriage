# -*- coding: utf-8 -*-
from PyQt5.QtCore import QT_VERSION_STR
from PyQt5.Qt import PYQT_VERSION_STR
from PyQt5.QtWidgets import  QApplication

from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
#from my_function import *
#from my_reports import *#
#from reportb6 import *

#from login_usr_script import *
#from users_add_script import *
#from chng_pwd_script import *
#from mang_usr_script import *
#from addmem_script import *
#from addfmly_script import *
#from splash_script import *
#from report_property_script import *
#from account_item_script import *
#from expenditure_add_script import *
#from income_add_script import *
#from payee_add_script import *
#from payer_add_script import *
#from inc_exp_rpt_script import *
#from open_balance_script import *
#import resources
import os

import mysql.connector  as mariadb
from fnmatch import fnmatch
import sys
import platform
import atexit
import mdigui
__version__ = "1.09"
class MainWindow(QtWidgets.QMainWindow,mdigui.Ui_MainWindow):
    def __init__(self, parent = None):
        global msg
        global userName
        global usrPriv
        global conn
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.progressBar = QProgressBar()
        self.statusbar = self.statusBar()
        self.statusbar.addPermanentWidget(self.progressBar)
        self.statusBar().showMessage('Ready')
        #dbName = getDbName()
        conn = mariadb.connect(host="localhost",user="root",passwd="joseph",dbName="marriage")
        cursor=conn.cursor()

        self.whotheUser()
        self.createTables()
        self.showMaximized()
        compTitle = myCompName()
        self.setWindowTitle(compTitle)
        self.createMenu()
        atexit.register(self.delPdf)
    def createMenu(self):
        bar = self.menuBar()
        fileMnu = bar.addMenu("File")
        rptMnu = bar.addMenu("Reports")
        proMnu = bar.addMenu("Property")
        setMnu = bar.addMenu("Settings")
        rptMnu.addAction("Account Statement")
        rptMnu.addAction("Members Directory")
        rptMnu.addAction("Members")
        fileMnu.addAction("Add Member")
        fileMnu.addAction("Add Family")
        fileMnu.addAction("Add Expenditure")
        fileMnu.addAction("Add Income")
        fileMnu.addAction("Exit")
        
        proMnu.addAction("Directory print")
        
        setMnu.addAction("Expenditure items")
        setMnu.addAction("Income items")
        setMnu.addAction("Opening balance")
        setMnu.addAction("Payee names")
        setMnu.addAction("Payer names")
        
        helpMnu = bar.addMenu("Help")
        helpMnu.addAction("About")
        
        fileMnu.triggered[QAction].connect(self.windowAction)
        proMnu.triggered[QAction].connect(self.windowAction)
        helpMnu.triggered[QAction].connect(self.windowAction)
        rptMnu.triggered[QAction].connect(self.windowAction)
        setMnu.triggered[QAction].connect(self.windowAction)

    def windowAction(self,q):
        if q.text() == "Add Member":
            sub = Addmem(self)
            sub.show()
        if q.text() == "Add Family":
            sub = Addfamily(self)
            sub.show()
        
        if q.text() == "Exit":
            sys.exit(0)
        if q.text() == "Account Statement":
            sub = Incexprpt(self)
            sub.show()
        if q.text() == "Members":
            membRpt(self)
        if q.text() == "Members Directory":
            membRptB6(self)
        if q.text() == "Directory print":
            sub = Rptprop(self)
            sub.show()
        if q.text() == "Opening balance":
            sub = Openbalance(self)
            sub.show()
        if q.text() == "Expenditure items":
            sub = Accitem(self)
            sub.setWindowTitle("Account item - Expenditure")
            sub.accType(0)
            sub.show()
        if q.text() == "Income items":
            sub = Accitem(self)
            sub.setWindowTitle("Account item - Income")
            sub.accType(1)
            sub.show()
        if q.text() == "Payee names":
            sub = Payeeadd(self)
            sub.show()
        if q.text() == "Payer names":
            sub = Payeradd(self)
            sub.show()
        if q.text() == "Add Expenditure":
            sub = Accountadd_E(self)
            sub.show()
        if q.text() == "Add Income":
            self.sub = Accountadd_I(self)
            self.sub.show()
        if q.text() == "About":
            self.helpAbout()
    
    def helpAbout(self):
        QMessageBox.about(self, "About Resassman.", 
                            """<b>Residence Association Management System</b> v %s
                            <p>Developed by "Jeaksoft" :2019
                            <p>Python %s - Qt %s - PyQt %s on %s """ %(
                            __version__, platform.python_version(), 
                            QT_VERSION_STR, PYQT_VERSION_STR,  platform.system()) )
    def whotheUser(self):
        global usrPriv
        global userNam
        
        conn = mariadb.connect(host="localhost",user="root",passwd="joseph",dbName="marriage")
        cursor=conn.cursor()
        cursor.execute("SELECT TEMP_NAME,TEMP_PRIV FROM TEMP_DATA")
        sqlRow=c.fetchone()
        userName = sqlRow[0]
        usrPriv = sqlRow[1]
        db.commit()
        c.close()
        db.close()
        self.userName = QLabel()
        self.userName.setText(userName)
        self.statusbar.addPermanentWidget(self.userName)
    def createTables(self):
        cursor=conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS MEMB_DATA(
                        MEB_ID INTEGER PRIMARY KEY,
                        RES_NUM TEXT,
                        MEB_TTL TEXT,
                        F_NAME TEXT,
                        M_NAME TEXT,
                        L_NAME TEXT,
                        H_NUM TEXT,
                        H_NAME TEXT,
                        MEB_OCU TEXT,
                        RES_TEL	 TEXT,
                        MOB_TEL TEXT,
                        BLD_GRP TEXT,
                        MEB_AGE TEXT,
                        MAIL_ID TEXT,
                        MEB_PHOTO BLOB)
                        """)
        cursor.execute("""CREATE TABLE IF NOT EXISTS FLY_DATA(
                        FLY_ID INTEGER PRIMARY KEY,
                        MEB_ID INTEGER,
                        FLY_TTL TEXT,
                        FLY_NAME TEXT,
                        MEB_REL TEXT,
                        FLY_OCU TEXT,
                        BLD_GRP TEXT,
                        FLY_AGE TEXT
                        )
                        """)
        cursor.execute("""CREATE TABLE IF NOT EXISTS REP_PROP(
                        ITEM_ID INTEGER PRIMARY KEY,
                        ITEM_VAL INTEGER
                        )
                        """)
        cursor.execute("""CREATE TABLE IF NOT EXISTS ACC_ITEMS(
                        ITEM_ID INTEGER PRIMARY KEY,
                        INC_OR_EXP INTEGER,
                        ITEM_NAME TEXT
                        )
                        """)
        cursor.execute("""CREATE TABLE IF NOT EXISTS OPEN_BAL_DATA(
                        ENTRY_ID INTEGER PRIMARY KEY,
                        OPEN_DATE DATE,
                        OPEN_CASH INTEGER,
                        OPEN_BANK INTEGER
                        )
                        """)
        cursor.execute("""CREATE TABLE IF NOT EXISTS ACC_DATA(
                        ENTRY_ID INTEGER PRIMARY KEY,
                        TRAN_DATE DATE,
                        INC_OR_EXP INTEGER,
                        RECI_ID INTEGER,
                        RECI_TABLE INTEGER,
                        ITEM_ID INTEGER,
                        BANK_TRAN INTEGER,
                        CASH_TRAN INTEGER
                        )
                        """)
        cursor.execute("""CREATE TABLE IF NOT EXISTS PAYEE_NAME(
                        ITEM_ID INTEGER PRIMARY KEY,
                        ITEM_NAME TEXT
                        )
                        """)
        cursor.execute("""CREATE TABLE IF NOT EXISTS PAYER_NAME(
                        ITEM_ID INTEGER PRIMARY KEY,
                        ITEM_NAME TEXT
                        )
                        """)
        cursor.close()
#        QMessageBox.information(self,msg,str(e))
    def delPdf(self):
        try:
            for dirpath, dirnames, filenames in os.walk(os.curdir): 
                for file in filenames:
                    if file == "Help.pdf":
                        pass
                    elif fnmatch(file, '*.pdf'):
                        os.remove(os.path.join(dirpath, file))
        except:
            return
    def closeEvent(self, event):
        if conn:
            conn.close()
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
#    splash = Splash()
#    splash.show()
#    for i in range(1, 101):
#        splash.prgBar.setValue(i)
#        t = time.time()
#        while time.time() < t + 0.1:
#           app.processEvents()
#    time.sleep(1)
    login = LoginForm()
#    splash.close()
    login.show()
    if login.exec_() == QtWidgets.QDialog.Accepted:
        myWindow = MainWindow()
        myWindow.show()
        sys.exit(app.exec_())
