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

class ExampleApp(QtWidgets.QMainWindow, UI_mainwindow2.Ui_MainWindow):

	app_name = "Odrive Tester"
	def __init__(self):
		# Simple reason why we use it here is that it allows us to
		# access variables, methods etc in the design.py file
		super(self.__class__, self).__init__()
		self.setupUi(self)  # This is defined in design.py file automatically
							# It sets up layout and widgets that are defined

		self.treeView.setModel(self.odr_model())
		self.treeView.setDragDropMode(QtGui.QAbstractItemView.DragOnly)
		self.pushButton_123 = QtWidgets.QPushButton()
		self.pushButton_123.setObjectName("pushButton_123")
		self.mdiArea.addSubWindow(self.pushButton_123)




	def odr_model(self):
		model = QtGui.QStandardItemModel(0, 2, self)
		model.setHeaderData(0, QtCore.Qt.Horizontal, "From")
		# child = QtGui.QStandardItem("yolo")
		# child2 = QtGui.QStandardItem("yolo2")
		# child.appendRow(child2)
		item = QtGui.QStandardItem("type")
		child = QtGui.QStandardItem("objects3")  # Apple
		item.appendRow(child)
		child = QtGui.QStandardItem("objects4")  # Banana
		item.appendRow(child)
		model.setItem(0, 0, item)
		# child.appendRow(QtGui.QStandardItem("nooooo"))
		# child2 = QtGui.QStandardItem("yolo2")
		# child.appendRow(child2)
		# # model.setHeaderData(1, QtCore.Qt.Horizontal, "Subject")
		# # model.setHeaderData(2, QtCore.Qt.Horizontal, "Date")
		# # model = QtGui.QStandardItemModel(self.load_config_template())
		model.setItem(0,1, child)
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


def main():
	app = QtWidgets.QApplication(sys.argv)  # A new instance of QApplication
	form = ExampleApp()                 # We set the form to be our (design)
	form.show()                         # Show the form
	app.exec_()                         # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
	main()                              # run the main function
