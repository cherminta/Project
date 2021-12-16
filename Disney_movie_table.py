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
                del row[0] #delete the index column
                items = [QtGui.QStandardItem(field) for field in row]
                self.model.appendRow(items)
            self.tableView.resizeColumnsToContents()

        self.ArLabel = QtWidgets.QLabel(self)
        self.ArLabel.setText("Arranged by: \n")
        self.ArLabel.move(10, 0)
        
        popupAboutToBeShown = QtCore.pyqtSignal()

        self.TitleBox  = QtWidgets.QComboBox()
        self.TitleBox.addItem("Title")
        self.TitleBox.addItem("A-Z")
        self.TitleBox.popupAboutToBeShown.connect(self.populateConbo)
        self.TitleBox.addItem("Z-A")
        self.TitleBox.setStyleSheet(stylesheet(self))
    
        self.DateBox  = QtWidgets.QComboBox()
        self.DateBox.addItem("Release date")
        self.DateBox.addItem("Newest")
        self.DateBox.addItem("Oldest")
        self.DateBox.setStyleSheet(stylesheet(self))
    
        self.LengthBox  = QtWidgets.QComboBox()
        self.LengthBox.addItem("Length")
        self.LengthBox.addItem("Shortest")
        self.LengthBox.addItem("Longest")
        self.LengthBox.setStyleSheet(stylesheet(self))
    
        self.BudgetBox  = QtWidgets.QComboBox()
        self.BudgetBox.addItem("Budget")
        self.BudgetBox.addItem("Most Budget")
        self.BudgetBox.addItem("Least Budget")
        self.BudgetBox.setStyleSheet(stylesheet(self))
    
        self.ImdbBox  = QtWidgets.QComboBox()
        self.ImdbBox.addItem("IMDB score")
        self.ImdbBox.addItem("Highest rating")
        self.ImdbBox.addItem("LLowest rating")
        self.ImdbBox.setStyleSheet(stylesheet(self))
    
        self.MetaBox  = QtWidgets.QComboBox()
        self.MetaBox.addItem("Metascore")
        self.MetaBox.addItem("Highest rating")
        self.MetaBox.addItem("LLowest rating")
        self.MetaBox.setStyleSheet(stylesheet(self))
    
        self.RottenBox  = QtWidgets.QComboBox()
        self.RottenBox.addItem("Rotten tomatoes")
        self.RottenBox.addItem("Highest rating")
        self.RottenBox.addItem("LLowest rating")
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

   def arrange(self, Ar):
       csv_file = pandas.read_csv('disney_movie_data_final.csv')
       sorted_csv = csv_file.sort_values(by=[Ar])

   def titleAr(self, button):
       if button == "A-Z":
           return 

   def writeCsv(self, fileName):
        # find empty cells
       for row in range(self.model.rowCount()):
           for column in range(self.model.columnCount()):
               myitem = self.model.item(row,column)
               if myitem is None:
                   item = QtGui.QStandardItem("")
                   self.model.setItem(row, column, item)
       fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", 
                       (QtCore.QDir.homePath() + "/" + self.fname + ".csv"),"CSV Files (*.csv)")
       if fileName:
           print(fileName)
           f = open(fileName, 'w')
           with f:
               writer = csv.writer(f, delimiter = '\t')
               for rowNumber in range(self.model.rowCount()):
                   fields = [self.model.data(self.model.index(rowNumber, columnNumber),
                                        QtCore.Qt.DisplayRole)
                    for columnNumber in range(self.model.columnCount())]
                   writer.writerow(fields)
               self.fname = os.path.splitext(str(fileName))[0].split("/")[-1]
               self.setWindowTitle(self.fname)
 
   def handlePrint(self):
       dialog = QtPrintSupport.QPrintDialog()
       if dialog.exec_() == QtWidgets.QDialog.Accepted:
           self.handlePaintRequest(dialog.printer())
 
   def handlePreview(self):
       dialog = QtPrintSupport.QPrintPreviewDialog()
       dialog.setFixedSize(1000,700)
       dialog.paintRequested.connect(self.handlePaintRequest)
       dialog.exec_()
 
   def handlePaintRequest(self, printer):
       # find empty cells
       for row in range(self.model.rowCount()):
           for column in range(self.model.columnCount()):
               myitem = self.model.item(row,column)
               if myitem is None:
                   item = QtGui.QStandardItem("")
                   self.model.setItem(row, column, item)
       printer.setDocName(self.fname)
       document = QtGui.QTextDocument()
       cursor = QtGui.QTextCursor(document)
       model = self.tableView.model()
       table = cursor.insertTable(model.rowCount(), model.columnCount())
       for row in range(table.rows()):
           for column in range(table.columns()):
               cursor.insertText(model.item(row, column).text())
               cursor.movePosition(QtGui.QTextCursor.NextCell)
       document.print_(printer)
 
   def removeRow(self):
       model = self.model
       indices = self.tableView.selectionModel().selectedRows() 
       for index in sorted(indices):
           model.removeRow(index.row()) 
 
   def addRow(self):
       item = QtGui.QStandardItem("")
       self.model.appendRow(item)
 
   def clearList(self):
       self.model.clear()
 
   def removeColumn(self):
       model = self.model
       indices = self.tableView.selectionModel().selectedColumns() 
       for index in sorted(indices):
           model.removeColumn(index.column()) 
 
   def addColumn(self):
       count = self.model.columnCount()
       print (count)
       self.model.setColumnCount(count + 1)
       self.model.setData(self.model.index(0, count), "", 0)
       self.tableView.resizeColumnsToContents()
 
   def finishedEdit(self):
       self.tableView.resizeColumnsToContents()
 
   def contextMenuEvent(self, event):
       self.menu = QtWidgets.QMenu(self)
       # copy
       copyAction = QtWidgets.QAction('Copy', self)
       copyAction.triggered.connect(lambda: self.copyByContext(event))
       # paste
       pasteAction = QtWidgets.QAction('Paste', self)
       pasteAction.triggered.connect(lambda: self.pasteByContext(event))
       # cut
       cutAction = QtWidgets.QAction('Cut', self)
       cutAction.triggered.connect(lambda: self.cutByContext(event))
       # delete selected Row
       removeAction = QtWidgets.QAction('delete Row', self)
       removeAction.triggered.connect(lambda: self.deleteRowByContext(event))
       # add Row after
       addAction = QtWidgets.QAction('insert new Row after', self)
       addAction.triggered.connect(lambda: self.addRowByContext(event))
       # add Row before
       addAction2 = QtWidgets.QAction('insert new Row before', self)
       addAction2.triggered.connect(lambda: self.addRowByContext2(event))
       # add Column before
       addColumnBeforeAction = QtWidgets.QAction('insert new Column before', self)
       addColumnBeforeAction.triggered.connect(lambda: self.addColumnBeforeByContext(event))
       # add Column after
       addColumnAfterAction = QtWidgets.QAction('insert new Column after', self)
       addColumnAfterAction.triggered.connect(lambda: self.addColumnAfterByContext(event))
       # delete Column
       deleteColumnAction = QtWidgets.QAction('delete Column', self)
       deleteColumnAction.triggered.connect(lambda: self.deleteColumnByContext(event))
       # add other required actions
       self.menu.addAction(copyAction)
       self.menu.addAction(pasteAction)
       self.menu.addAction(cutAction)
       self.menu.addSeparator()
       self.menu.addAction(addAction)
       self.menu.addAction(addAction2)
       self.menu.addSeparator()
       self.menu.addAction(addColumnBeforeAction)
       self.menu.addAction(addColumnAfterAction)
       self.menu.addSeparator()
       self.menu.addAction(removeAction)
       self.menu.addAction(deleteColumnAction)
       self.menu.popup(QtGui.QCursor.pos())


def stylesheet(self):
       return """
       QTableView
       {
border: 1px solid grey;
border-radius: 0px;
font-size: 12px;
        background-color: #f8f8f8;
selection-color: white;
selection-background-color: #00ED56;
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