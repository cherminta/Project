import csv, codecs 
import os
import pandas
 
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QPainter
from PyQt5.QtCore import QFile, QLine
 
class MyWindow(QtWidgets.QWidget):
   def __init__(self, fileName, parent=None):
        super().__init__()
        self.model =  QtGui.QStandardItemModel(self)
 
        self.tableView = QtWidgets.QTableView(self)
        self.tableView.setStyleSheet(stylesheet(self))
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.setShowGrid(True)
        self.tableView.setGeometry(10, 50, 780, 645)
        self.model.dataChanged.connect(self.finishedEdit)

        #open csv
        fileName = "disney_movie_data_final.csv"
 
        ff = open(fileName, 'r')
        mytext = ff.read()
#            print(mytext)
        ff.close()
        f = open(fileName, 'r')

        with f:
            self.fname = os.path.splitext(str(fileName))[0].split("/")[-1]
            self.setWindowTitle(self.fname)

            reader = csv.reader(f)
            self.model.clear()   

            for row in reader:
                #delete the index column
                items = [QtGui.QStandardItem(field) for field in row]
                self.model.appendRow(items)
            self.tableView.resizeColumnsToContents()

        self.ArLabel = QtWidgets.QLabel(self)
        self.ArLabel.setText("Arranged by: \n")
        self.ArLabel.move(10, 0)

        self.TitleBox  = QtWidgets.QComboBox()
        self.TitleBox.addItem("Title")
        self.TitleBox.addItem("A-Z")
        self.TitleBox.addItem("Z-A")
        self.TitleBox.activated[str].connect(self.ButtonAr)
        self.TitleBox.currentTextChanged.connect(self.ori_text)
        self.TitleBox.setStyleSheet(stylesheet(self))
    
        self.DateBox  = QtWidgets.QComboBox()
        self.DateBox.addItem("Release date")
        self.DateBox.addItem("Newest")
        self.DateBox.addItem("Oldest")
        self.DateBox.activated[str].connect(self.ButtonAr)
        self.DateBox.currentTextChanged.connect(self.ori_text)
        self.DateBox.setStyleSheet(stylesheet(self))
    
        self.LengthBox  = QtWidgets.QComboBox()
        self.LengthBox.addItem("Length")
        self.LengthBox.addItem("Shortest")
        self.LengthBox.addItem("Longest")
        self.LengthBox.activated[str].connect(self.ButtonAr)
        self.LengthBox.currentTextChanged.connect(self.ori_text)
        self.LengthBox.setStyleSheet(stylesheet(self))
    
        self.BudgetBox  = QtWidgets.QComboBox()
        self.BudgetBox.addItem("Budget")
        self.BudgetBox.addItem("Most Budget")
        self.BudgetBox.addItem("Least Budget")
        self.BudgetBox.activated[str].connect(self.ButtonAr)
        self.BudgetBox.currentTextChanged.connect(self.ori_text)
        self.BudgetBox.setStyleSheet(stylesheet(self))
    
        self.ImdbBox  = QtWidgets.QComboBox()
        self.ImdbBox.addItem("IMDB score")
        self.ImdbBox.addItem("Highest rating")
        self.ImdbBox.addItem("Lowest rating")
        self.ImdbBox.activated[str].connect(self.ButtonAr)
        self.ImdbBox.currentTextChanged.connect(self.ori_text)
        self.ImdbBox.setStyleSheet(stylesheet(self))
    
        self.MetaBox  = QtWidgets.QComboBox()
        self.MetaBox.addItem("Metascore")
        self.MetaBox.addItem("Highest rating")
        self.MetaBox.addItem("Lowest rating")
        self.MetaBox.activated[str].connect(self.MetaAr)
        self.MetaBox.currentTextChanged.connect(self.meta_text)
        self.MetaBox.setStyleSheet(stylesheet(self))
    
        self.RottenBox  = QtWidgets.QComboBox()
        self.RottenBox.addItem("Rotten tomatoes")
        self.RottenBox.addItem("Highest rating")
        self.RottenBox.addItem("Lowest rating")
        self.RottenBox.activated[str].connect(self.RottenAr)
        self.RottenBox.currentTextChanged.connect(self.rotten_text)
        self.RottenBox.setStyleSheet(stylesheet(self))
    
        grid = QtWidgets.QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self.TitleBox, 0, 0)
        grid.addWidget(self.DateBox, 0, 1)
        grid.addWidget(self.LengthBox, 0, 2)
        grid.addWidget(self.BudgetBox, 0, 3)
        grid.addWidget(self.ImdbBox, 0, 4)
        grid.addWidget(self.MetaBox, 0, 5)
        grid.addWidget(self.RottenBox, 0, 6)
        grid.addWidget(self.tableView, 1, 0, 1, 9)
        self.setLayout(grid)

        item = QtGui.QStandardItem()
        self.model.appendRow(item)
        self.model.setData(self.model.index(0, 0), "", 0)
        self.tableView.resizeColumnsToContents()

   def ori_text(self, text):

        if text != 'A-Z' and text != 'Z-A':
            self.TitleBox.setCurrentText('Title') 
        elif text != 'Newest' and text != 'Oldest':
            self.DateBox.setCurrentText('Release date')
        elif text !=  'Longest' and text != 'Shortest':
            self.LengthBox.setCurrentText('Length')                
        elif text != 'Most Budget' and text != 'Least Budget':
            self.BudgetBox.setCurrentText('Budget')
        elif text != 'Highest rating' and text != 'Lowest rating':
            self.ImdbBox.setCurrentText('IMDB score')

   def meta_text(self, text):
        if text != 'Highest rating' and text != 'Lowest rating':
            self.MetaBox.setCurrentText('Metascore')
    
   def rotten_text(self, text):
        if text != 'Highest rating' and text != 'Lowest rating':
            self.RottenBox.setCurrentText('Rotten tomatoes')

   def arrange(self, Ar):
       f = open(Ar, 'r')
       with f:
            self.fname = os.path.splitext(str(Ar))[0].split("/")[-1]
            self.setWindowTitle(self.fname)

            reader = csv.reader(f)
            self.model.clear()   

            for row in reader:
                #delete the index column
                items = [QtGui.QStandardItem(field) for field in row]
                self.model.appendRow(items)
            self.tableView.resizeColumnsToContents()

   def ButtonAr(self, bt):
        if bt == "A-Z":
           self.arrange('movie_title_ar')
        elif bt == "Z-A":
            self.arrange('movie_title_ba')
        elif bt == "Newest":
            self.arrange('movie_date_ba')
        elif bt == "Oldest":
            self.arrange('movie_date_ar')
        elif bt == "Shortest":
            self.arrange('movie_length_ar')
        elif bt == "Longest":
            self.arrange('movie_length_ba')
        elif bt == "Most Budget":
            self.arrange('movie_budget_ba')
        elif bt == "Least Budget":
            self.arrange('movie_budget_ar')
        elif bt == "Highest rating":
            self.arrange('movie_imdb_ba')
        elif bt == "Lowest rating":
            self.arrange('movie_imdb_ar')

   def MetaAr(self, bt):
        if bt == "Highest rating":
           self.arrange('movie_meta_ba')
        elif bt == "Lowest rating":
           self.arrange('movie_meta_ar')

   def RottenAr(self, bt):
        if bt == "Highest rating":
           self.arrange('movie_rotten_ba')
        elif bt == "Lowest rating":
           self.arrange('movie_rotten_ar')
 

 
   def finishedEdit(self):
       self.tableView.resizeColumnsToContents()

def stylesheet(self):
       return """
       QTableView
       {
border: 1px solid grey;
border-radius: 0px;
font-size: 12px;
        background-color: #f8f8f8;
selection-color: white;
selection-background-color: #759E9C;
       }
 
QTableView QTableCornerButton::section {
    background: #D6D1D1;
    border: 1px outset black;
}
 
QPushButton
{
font-size: 11px;
border: 1px inset grey;
height: 24px;
width: 80px;
color: black;
background-color: #e8e8e8;
background-position: bottom-left;
} 
 
QPushButton::hover
{
border: 2px inset goldenrod;
font-weight: bold;
color: #e8e8e8;
background-color: green;
} 
"""

if __name__ == "__main__":
   import sys
 
   app = QtWidgets.QApplication(sys.argv)
   app.setApplicationName('MyWindow')
   main = MyWindow('')
   main.setMinimumSize(820, 300)
   main.setGeometry(0,0,820,700)
   main.setWindowTitle("Disney Movie Data Table")
   main.show()
 
sys.exit(app.exec_())