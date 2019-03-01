#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import UI_mainwindow2

import odrive
from odrive.enums import *

import json
import glob
import datetime

import os

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets

from serialThread import odriveWorker

ICON_TRUE = "Icons/True.jpg"
ICON_FALSE = "Icons/False.jpg"
ICON_NOSTATE = "Icons/NoState.jpg"

class CustomMDIArea(QtWidgets.QMdiArea):
	def __init__(self,type, parent=None):
		super(self.__class__, self).__init__()
		# self.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
		self.setAcceptDrops(True)

	def dragEnterEvent(self, event):
		print("drag enter event")
		print(event)
		event.accept()

	def dragMoveEnter(self, event):
		print("drag move enter")
		print(event)


	def dropEvent(self, event):
		print("drop event")
		print(event)
		event.accept()
		# print(event.data())
		# print(event.mimeData().data())
		print(event.mimeData().formats())
		print(event.source())
		print(isinstance(event.source(),QtGui.QAbstractItemView))
		print(event.source().treePosition())
		print(event.source().currentIndex())
		print(event.source().currentIndex().row())
		# print(event.source().model().model().rowCount())
		print(event.source().model().itemPrototype())
		print(event.source().model().item(0).text())
		print(event.source().selectedIndexes())
		# print(event.source().selectedIndexes()[0].text())
		print(event.source().selectedIndexes()[0].row())
		index = event.source().selectedIndexes()[0]
		crawler = index.model().itemFromIndex(index)
		print(crawler.text())
		# encodedData = event.mimeData("application/x-qstandarditemmodeldatalist")
		# stream = QDataStream(encodedData, QIODevice.ReadOnly)
		# row = stream.readInt32()
		# column = stream.readInt32()
		# print(encodedData)
		# print(stream)
		# print(row)
		# print(column)



class ExampleApp(QtWidgets.QMainWindow, UI_mainwindow2.Ui_MainWindow):

	app_name = "Odrive Tester"
	def __init__(self):
		# Simple reason why we use it here is that it allows us to
		# access variables, methods etc in the design.py file
		super(self.__class__, self).__init__()
		self.setupUi(self)  # This is defined in design.py file automatically
							# It sets up layout and widgets that are defined




		self.quit_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+Q"), self)
		self.quit_shortcut.activated.connect(self.close_application)

		self.treeView.setModel(self.odr_model())
		self.treeView.setDragEnabled(True)
		# self.treeView.setAcceptDrops(True)
		# self.treeView.setDragDropMode(QtGui.QAbstractItemView.DragOnly)

		self.pushButton_123 = QtWidgets.QPushButton()
		self.pushButton_123.setObjectName("pushButton_123")
		self.mdiArea.addSubWindow(self.pushButton_123)
		# self.mdiArea.dropEvent(self.droping)
		self.mdiArea.setAcceptDrops(True)

		self.testmdi = CustomMDIArea(self)
		self.gridLayout.addWidget(self.testmdi, 1, 0, 1, 1)
		# self.mdiArea.dragMoveEvent(QtGui.QDragMoveEvent())

	def droping(self):
		print("drop")




	def odr_model(self):
		model = QtGui.QStandardItemModel(0, 2, self)
		model.setHeaderData(0, QtCore.Qt.Horizontal, "Odrive")
		model.setHeaderData(1, QtCore.Qt.Horizontal, "Graph enable")
		# child = QtGui.QStandardItem("yolo")
		# child2 = QtGui.QStandardItem("yolo2")
		# child.appendRow(child2)
		item = QtGui.QStandardItem("type")
		child = QtGui.QStandardItem("objects3")  # Apple
		item.appendRow(child)
		child2 = QtGui.QStandardItem("objects4")  # Banana
		item.appendRow(child2)
		model.setItem(0, 0, item)


		item2 = QtGui.QStandardItem("type222")
		model.setItem(1, 0, item2)
		# self.checkBox2 = QtWidgets.QCheckBox(self.centralWidget)
		# self.checkBox2.setObjectName("checkBox2")
		# model.setItem(0, 1, self.checkBox2)
		# child.appendRow(QtGui.QStandardItem("nooooo"))
		# child2 = QtGui.QStandardItem("yolo2")
		# child.appendRow(child2)
		# # model.setHeaderData(1, QtCore.Qt.Horizontal, "Subject")
		# # model.setHeaderData(2, QtCore.Qt.Horizontal, "Date")
		# # model = QtGui.QStandardItemModel(self.load_config_template())
		# model.setItem(0,1, child)
		# model.setItem(1,1, child2)
		return model
		#
		# group = QGroupBox()
		# box = QBoxLayout(QBoxLayout.TopToBottom)
		# group.setLayout(box)
		# group.setTitle("Buttons")
		# widget_laytout.addWidget(group)
		#
		# fruits = ["Buttons in GroupBox", "TextBox in GroupBox", "Label in GroupBox", "TextEdit"]
		# view = QListView(self)
		# model = QStandardItemModel()
		# for f in fruits:
		#     model.appendRow(QStandardItem(f))
		# view.setModel(model)
		# box.addWidget(view)
		#
		# self.stk_w.addWidget(Widget_1())
		# self.stk_w.addWidget(Widget_2())
		# self.stk_w.addWidget(Widget_3())
		# self.stk_w.addWidget(QTextEdit())
		#
		# widget_laytout.addWidget(self.stk_w)
		# self.setLayout(widget_laytout)

	def load_config_template(self):
		config_template = {}
		with open("config_template.json") as f:
			config_template = json.load(f)
		return config_template

	def close_application(self):
		print("whooaaaa so custom!!!")
		# try:
		# 	self.odrive_worker.stop()
		# except:
		# 	pass
		sys.exit()


def main():
	app = QtWidgets.QApplication(sys.argv)  # A new instance of QApplication
	form = ExampleApp()                 # We set the form to be our (design)
	form.show()                         # Show the form
	app.exec_()                         # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
	main()                              # run the main function
