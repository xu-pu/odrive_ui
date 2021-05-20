#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import odrive
from odrive.enums import *

import fibre

import json
import glob
import datetime

import os

from PyQt5 import QtCore, QtGui, QtWidgets

from serialThread import odriveWorker

ICON_TRUE_PATH = "Icons/True.jpg"
ICON_FALSE_PATH = "Icons/False.jpg"
ICON_NOSTATE_PATH = "Icons/NoState.jpg"

ICON_CONNECT_PATH = "Icons/odrive_icons/odrive_icons_Connect.png"
ICON_HELP_PATH = "Icons/odrive_icons/odrive_icons_Help.png"
ICON_OPEN_PATH = "Icons/odrive_icons/odrive_icons_Open.png"
ICON_READ_CONFIG_PATH = "Icons/odrive_icons/odrive_icons_ReadConfig.png"
ICON_SAVE_PATH = "Icons/odrive_icons/odrive_icons_Save.png"
ICON_SETTINGS_PATH = "Icons/odrive_icons/odrive_icons_Settings.png"
ICON_WRITE_CONFIG_PATH = "Icons/odrive_icons/odrive_icons_WriteConfig.png"

version_ignore_list = ["fw_version_revision", "fw_version_major", "fw_version_minor","hw_version_major", "hw_version_minor", "fw_version_unreleased","hw_version_variant"]

class odrive_MainWindow(object):
	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(800, 600)


		# window = QtWidgets.QWidget()
		# layout = QtWidgets.QVBoxLayout()
		# layout.addWidget(QtWidgets.QTreeView())
		# layout.addWidget(QPushButton('Bottom'))
		# MainWindow.setCentralWidget(layout)


		self.centralWidget = QtWidgets.QWidget(MainWindow)
		self.centralWidget.setObjectName("centralWidget")
		self.gridLayout = QtWidgets.QGridLayout(self.centralWidget)
		# self.gridLayout.setContentsMargins(11, 11, 11, 11)
		# self.gridLayout.setSpacing(6)
		# self.gridLayout.setObjectName("gridLayout")
		# self.horizontalLayout = QtWidgets.QHBoxLayout()
		# self.horizontalLayout.setSpacing(6)
		# self.horizontalLayout.setObjectName("horizontalLayout")
		# self.gridLayout.addLayout(self.horizontalLayout, 1, 1, 1, 1)
		self.treeView = QtWidgets.QTreeView()
		# self.treeView.setMinimumSize(QtCore.QSize(250, 0))
		self.treeView.setMaximumSize(QtCore.QSize(250,1000))
		self.treeView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
		# self.treeView.setObjectName("treeView")
		self.gridLayout.addWidget(self.treeView, 0, 0, 1, 1)

		self.scrollArea = QtWidgets.QScrollArea()
		self.scrollArea.setWidgetResizable(True)
		self.scrollArea.setObjectName("scrollArea")
		self.scrollAreaWidgetContents = QtWidgets.QWidget()
		# self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 274, 237))
		self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
		self.scrollArea.setWidget(self.scrollAreaWidgetContents)
		self.gridLayout.addWidget(self.scrollArea, 0, 1, 1, 1)

		MainWindow.setCentralWidget(self.centralWidget)
		self.menuBar = QtWidgets.QMenuBar(MainWindow)
		# self.menuBar.setGeometry(QtCore.QRect(0, 0, 1354, 22))
		self.menuBar.setObjectName("menuBar")
		MainWindow.setMenuBar(self.menuBar)
		self.mainToolBar = QtWidgets.QToolBar(MainWindow)
		self.mainToolBar.setObjectName("mainToolBar")
		MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
		self.statusBar = QtWidgets.QStatusBar(MainWindow)
		self.statusBar.setObjectName("statusBar")
		MainWindow.setStatusBar(self.statusBar)

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

class ExampleApp(QtWidgets.QMainWindow, odrive_MainWindow):
	app_name = "Odrive Tester"
	def __init__(self):
		# Simple reason why we use it here is that it allows us to
		# access variables, methods etc in the design.py file
		super(self.__class__, self).__init__()
		self.setupUi(self)  # This is defined in design.py file automatically
							# It sets up layout and widgets that are defined

		self.setWindowTitle(self.app_name)

		self.quit_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+Q"), self)
		self.quit_shortcut.activated.connect(self.close_application)

		self.connect_to_odrive_action = self.mainToolBar.addAction("Connect to Odrive")
		self.connect_icon = QtGui.QIcon()
		self.connect_icon.addPixmap(QtGui.QPixmap(ICON_CONNECT_PATH), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.connect_to_odrive_action.setIcon(self.connect_icon)
		self.connect_to_odrive_action.triggered.connect(self.odrive_connect)

		# self.save_action = self.mainToolBar.addAction("Save")
		# self.save_icon = QtGui.QIcon()
		# self.save_icon.addPixmap(QtGui.QPixmap(ICON_SAVE_PATH))
		# self.save_action.setIcon(self.save_icon)

		# self.open_action = self.mainToolBar.addAction("Open")
		# self.open_icon = QtGui.QIcon()
		# self.open_icon.addPixmap(QtGui.QPixmap(ICON_OPEN_PATH))
		# self.open_action.setIcon(self.open_icon)

		# self.read_config_action = self.mainToolBar.addAction("Read configuration")
		# self.read_config_icon = QtGui.QIcon()
		# self.read_config_icon.addPixmap(QtGui.QPixmap(ICON_READ_CONFIG_PATH))
		# self.read_config_action.setIcon(self.read_config_icon)

		# self.write_config_action = self.mainToolBar.addAction("Write configuration")
		# self.write_config_icon = QtGui.QIcon()
		# self.write_config_icon.addPixmap(QtGui.QPixmap(ICON_WRITE_CONFIG_PATH))
		# self.write_config_action.setIcon(self.write_config_icon)

		# self.settings_action = self.mainToolBar.addAction("Settings")
		# self.settings_icon = QtGui.QIcon()
		# self.settings_icon.addPixmap(QtGui.QPixmap(ICON_SETTINGS_PATH))
		# self.settings_action.setIcon(self.settings_icon)
		# self.settings_action.triggered.connect(self.open_settings_window)

		# self.help_action = self.mainToolBar.addAction("Help")
		# self.help_icon = QtGui.QIcon()
		# self.help_icon.addPixmap(QtGui.QPixmap(ICON_HELP_PATH))
		# self.help_action.setIcon(self.help_icon)

		# self.treeView.setDragEnabled(True)
		# self.treeView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
		# self.treeView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
		# # self.treeView.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
		# # self.treeView.setAcceptDrops(True)
		# # self.treeView.setDragDropMode(QtGui.QAbstractItemView.DragOnly)
		self.treeView.clicked.connect(self.tree_item_selected)

		self.odrive_connect()

	def tree_item_selected(self):
		index = self.treeView.selectedIndexes()[0]
		tree_selection = index.model().itemFromIndex(index).text()
		print(tree_selection)
		if tree_selection == "General":
			self.setup_general()
		elif tree_selection == "Control Test":
			pass
		else:
			pass
		# print(self.treeView.selectedIndexes()[0].text())

	def setup_general(self):
		
		# for key in self.my_drive._remote_attributes.keys():
		# 	if isinstance(self.my_drive._remote_attributes[key], fibre.remote_object.RemoteObject):
		# 		pass
		# 	else:
		# print(key)
		for item in self.my_drive._json_data:
			# print(item["name"])
			if "members" in item.keys():
				pass
				# print("Has Members")
			else:
				if "access" in item.keys():
					# print(type(item))
					print(item["type"])
					print(item["access"])

					# if item["access"] == "r":
						# print(item["type"])
						# if item["type"] == "float":
						# 	ok = self.my_drive._remote_attributes[item["name"]].get_value()
						# 	print(ok)
	# def odrive_requested(self):
	# 	self.testmdi.add_odrive(self.my_drive)

	# def droping(self):
	# 	print("drop")

	# def load_config_template(self):
	# 	config_template = {}
	# 	with open("config_template.json") as f:
	# 		config_template = json.load(f)
	# 	return config_template

	def close_application(self):
		print("whooaaaa so custom!!!")
		# try:
		# 	self.odrive_worker.stop()
		# except:
		# 	pass
		sys.exit()

	def odrive_connect(self):
		# print("connecting")
		self.statusBar.showMessage("Connecting...")
		self.odrive_worker = odriveWorker()
		self.odrive_worker.odrive_found_sig.connect(self.odrive_connected)
		self.odrive_worker.start()

	def odrive_connected(self, my_drive):
		self.statusBar.showMessage("Connected!", 5000)
		self.my_drive = my_drive
		# self.testmdi.add_odrive(self.my_drive)
		self.treeView.setModel(self.setup_odrive_model(my_drive))

	def setup_odrive_model(self, my_drive):
		print("Odrive found. Setting up model.")
		model = QtGui.QStandardItemModel(0, 1, self)
		model.setHeaderData(0, QtCore.Qt.Horizontal, "Odrive")
		# model.setHeaderData(1, QtCore.Qt.Horizontal, "Type")
		 # isinstance(odrv0._remote_attributes["reboot"], fibre.remote_object.RemoteFunction)
		item = QtGui.QStandardItem("odrv0")
		child = QtGui.QStandardItem("General")
		item.appendRow(child)
		child = QtGui.QStandardItem("Control Test")
		item.appendRow(child)
		for key in my_drive._remote_attributes.keys():
			if isinstance(my_drive._remote_attributes[key], fibre.remote_object.RemoteObject):
				child = QtGui.QStandardItem(key)
				item.appendRow(child)
		# for key in my_drive._remote_attributes.keys():
		# 	# if key not in ignore_list:
		# 	if isinstance(my_drive._remote_attributes[key], fibre.remote_object.RemoteObject):
		# 		child = QtGui.QStandardItem(key)
		# 		for child_key in my_drive._remote_attributes[key]._remote_attributes.keys():
		# 			if isinstance(my_drive._remote_attributes[key]._remote_attributes[child_key], fibre.remote_object.RemoteObject):
		# 				sub1_child = QtGui.QStandardItem(child_key)
		# 				for sub1_child_key in my_drive._remote_attributes[key]._remote_attributes[child_key]._remote_attributes.keys():
		# 					if isinstance(my_drive._remote_attributes[key]._remote_attributes[child_key]._remote_attributes[sub1_child_key], fibre.remote_object.RemoteObject):
		# 						sub2_child = QtGui.QStandardItem(sub1_child_key)
		# 						for sub2_child_key in my_drive._remote_attributes[key]._remote_attributes[child_key]._remote_attributes[sub1_child_key]._remote_attributes.keys():
		# 							if isinstance(my_drive._remote_attributes[key]._remote_attributes[child_key]._remote_attributes[sub1_child_key]._remote_attributes[sub2_child_key], fibre.remote_object.RemoteObject):
		# 								sub3_child = QtGui.QStandardItem(sub2_child_key)
		# 								sub2_child.appendRow(sub3_child)
		# 							else:
		# 								sub3_child = QtGui.QStandardItem(sub2_child_key)
		# 								sub2_child.appendRow(sub3_child)
		# 						sub1_child.appendRow(sub2_child)
		# 					else:
		# 						sub2_child = QtGui.QStandardItem(sub1_child_key)
		# 						sub1_child.appendRow(sub2_child)
		# 				child.appendRow(sub1_child)
		# 			else:
		# 				sub1_child = QtGui.QStandardItem(child_key)
		# 				child.appendRow(sub1_child)
		# 			# elif
		# 		item.appendRow(child)
		# 	else:
		# 		if key not in version_ignore_list:
		# 			child = QtGui.QStandardItem(key)
		# 			item.appendRow(child)

		# child = QtGui.QStandardItem("fw_version")
		# item.appendRow(child)
		# child = QtGui.QStandardItem("hw_version")
		# item.appendRow(child)

		model.setItem(0,0,item)
		# self.testmdi.show()
		return model

def main():
	app = QtWidgets.QApplication(sys.argv)  # A new instance of QApplication
	form = ExampleApp()                 # We set the form to be our (design)
	form.show()                         # Show the form
	app.exec_()                         # and execute the app

if __name__ == '__main__':              # if we're running file directly and not importing it
	main()                              # run the main function
