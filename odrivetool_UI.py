#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PyQt5.sip import delete
import odrive
from odrive.enums import *

import fibre

import json
import glob
import datetime

import os

from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph import PlotWidget
import pyqtgraph as pg

from control_window import ControllerWindow
from serialThread import odriveWorker

ICON_TRUE_PATH = "Icons/true.png"
ICON_FALSE_PATH = "Icons/false.png"
ICON_NOSTATE_PATH = "Icons/NoState.jpg"

ICON_CONNECT_PATH = "Icons/odrive_icons/odrive_icons_Connect.png"
ICON_HELP_PATH = "Icons/odrive_icons/odrive_icons_Help.png"
ICON_OPEN_PATH = "Icons/odrive_icons/odrive_icons_Open.png"
ICON_READ_CONFIG_PATH = "Icons/odrive_icons/odrive_icons_ReadConfig.png"
ICON_SAVE_PATH = "Icons/odrive_icons/odrive_icons_Save.png"
ICON_SETTINGS_PATH = "Icons/odrive_icons/odrive_icons_Settings.png"
ICON_WRITE_CONFIG_PATH = "Icons/odrive_icons/odrive_icons_WriteConfig.png"
ICON_OPEN_CONTROLLER_PATH = "Icons/odrive_icons/odrive_icons_OpenController2.png"

version_ignore_list = ["fw_version_revision", "fw_version_major", "fw_version_minor","hw_version_major", "hw_version_minor", "fw_version_unreleased","hw_version_variant"]

class odrive_MainWindow(object):
	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(1280, 720)
		# MainWindow.resize(1920, 1080)

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
		self.treeView.setMaximumSize(QtCore.QSize(200,1000))
		self.treeView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
		# self.treeView.setObjectName("treeView")
		self.gridLayout.addWidget(self.treeView, 0, 0, 2, 1)

		self.scrollArea = QtWidgets.QScrollArea()
		self.scrollArea.setWidgetResizable(True)
		self.scrollArea.setObjectName("scrollArea")
		self.scrollAreaWidgetContents = QtWidgets.QWidget()
		# self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 274, 237))
		self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
		self.scrollArea.setWidget(self.scrollAreaWidgetContents)
		self.sb_v_layout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
		self.sb_layout = QtWidgets.QGridLayout()
		self.sb_v_layout.addLayout(self.sb_layout,1,0,1,1)
		self.gridLayout.addWidget(self.scrollArea, 1, 1, 1, 1)

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

		self.PIXMAP_FALSE = QtGui.QPixmap("Icons/false.png")
		self.PIXMAP_TRUE = QtGui.QPixmap("Icons/true.png")

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

		self.odrive_number_label = QtWidgets.QLabel()
		self.odrive_number_label.setText("Set Odrive number to detect")
		self.mainToolBar.addWidget(self.odrive_number_label)

		self.odrive_number_sbox = QtWidgets.QSpinBox()
		self.odrive_number_sbox.setValue(1)
		self.odrive_number_sbox.setMinimum(1)
		self.odrive_number_sbox.setMaximum(10)
		self.odrive_number_sbox.setToolTip("Don't set more than you have connected or it will FREEZE")
		self.mainToolBar.addWidget(self.odrive_number_sbox)

		self.connect_to_odrive_action = self.mainToolBar.addAction("Connect to Odrive")
		self.connect_icon = QtGui.QIcon()
		self.connect_icon.addPixmap(QtGui.QPixmap(ICON_CONNECT_PATH), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.connect_to_odrive_action.setIcon(self.connect_icon)
		self.connect_to_odrive_action.triggered.connect(self.odrive_connect)

		

		self.open_controller = self.mainToolBar.addAction("Open Controller")
		self.open_controller_icon = QtGui.QIcon()
		self.open_controller_icon.addPixmap(QtGui.QPixmap(ICON_OPEN_CONTROLLER_PATH))
		self.open_controller.setIcon(self.open_controller_icon)
		self.open_controller.triggered.connect(self.open_controller_window)

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

		self.changed_settings = {}

		self.treeView.clicked.connect(self.tree_item_selected)

		# self.odrive_connect()

	def open_controller_window(self):
		try:
			my_drive = self.select_odrive()
			# print(my_drive)
			self.controller_window = ControllerWindow()
			self.controller_window.show()
			self.controller_window.give_odrive(my_drive)
		except:
			print("EXCPETIOn")
			w1 = QtWidgets.QMessageBox()
			w1.setText("Select Odrive from the Tree View")
			# w1.show()
			x = w1.exec_()

	def tree_item_selected(self):
		self.changed_settings = {}
		# index = self.treeView.selectedIndexes()[0]
		# tree_selection = index.model().itemFromIndex(index).text()
		# print(tree_selection)
		try:
			self.deleteItems(self.button_layout)
		except:
			pass
		self.add_action_buttons()

		self.setup_config_window()

		# if tree_selection == "General":
		# 	self.setup_general()
		# elif tree_selection == "Control Test":
		# 	pass
		# else:
		# 	self.setup_config(tree_selection)
			# self.setup()
		# print(self.treeView.selectedIndexes()[0].text()).


	def find_tree_parents(self, index, path_list):
		if index.model() == None:
			return path_list
		else:
			path_list.append(index.model().itemFromIndex(index).text())
			path_list = self.find_tree_parents(index.parent(), path_list)
		return path_list



	def find_parent_path(self, object, path_list):
		if object.parent() == None:
			# print("no more parents")
			return path_list
		else:
			path_list.append(object.parent().objectName())
			self.find_parent_path(object.parent(), path_list)
		
		return path_list

	def clean_up_path(self, path_list):
		path_list.remove('scrollAreaWidgetContents')
		path_list.remove('qt_scrollarea_viewport')
		path_list.remove('scrollArea')
		path_list.remove('centralWidget')
		path_list.remove('MainWindow')
		try:
			path_list.remove('')
			path_list.remove('')
			path_list.remove('')
			path_list.remove('')
			path_list.remove('')
		except:
			pass

		return path_list


	def add_to_changes_dict(self,ok):
		pass

	def radio_button_changed(self):
		# print(self.sender().objectName())
		# print(self.sender().checkedButton().objectName())

		path_list = []
		path_list.append(self.sender().objectName())
		if self.sender().checkedButton().objectName() == "True":
			item_value = True
		else:
			item_value = False

		self.find_parent_path(self.sender(), path_list)
		path_list = self.clean_up_path(path_list)
		index = self.treeView.selectedIndexes()[0]
		tree_selection = index.model().itemFromIndex(index).text()
		if tree_selection == "General":
			pass
		else:
			path_list.append(tree_selection)
		odrive_parent = index.parent()
		path_list.append(odrive_parent.model().itemFromIndex(odrive_parent).text())

		# print(path_list)

		pal = QtGui.QPalette()
		pal.setColor(QtGui.QPalette.Base, QtCore.Qt.yellow)
		# pal.setColor(QPalette::Window, Qt::blue);
		self.sender().checkedButton().setPalette(pal)


		pal = QtGui.QPalette()
		pal.setColor(QtGui.QPalette.Button, QtCore.Qt.yellow)
		self.pb_apply.setPalette(pal)

		if str(path_list) in self.changed_settings:
			# print("FOUND ITEM")
			self.changed_settings[str(path_list)]["value"] = item_value
		else:
			# print("NEW PATH")
			self.changed_settings[str(path_list)] = {}
			self.changed_settings[str(path_list)]["value"] = item_value
			self.changed_settings[str(path_list)]["path"] = path_list
		# print(self.sender().text())
		# print(self.sender().value())

	def value_changed_test(self, haha):
		path_list = []
		# path_list.append(self.sender().text())
		item_value = self.sender().value()
		# print(item_value)
		path_list.append(self.sender().objectName())
		self.find_parent_path(self.sender(), path_list)
		path_list = self.clean_up_path(path_list)
		index = self.treeView.selectedIndexes()[0]
		tree_selection = index.model().itemFromIndex(index).text()
		# if tree_selection == "odrv0":
		# 	pass
		# else:

		path_list2 = []
		path_list2 = self.find_tree_parents(self.treeView.selectedIndexes()[0], path_list2)
		if len(path_list2) == 3:
			path_list2.pop(0)
		path_list.extend(path_list2)
		# path_list.append(tree_selection)

		# if tree_selection != "odrv0":
		# 	odrive_parent = index.parent()
			
		# 	path_list.append(odrive_parent.model().itemFromIndex(odrive_parent).text())
		# print(path_list)
		# QPalette pal = widget.palette();
		pal = QtGui.QPalette()
		pal.setColor(QtGui.QPalette.Base, QtCore.Qt.yellow)
		# pal.setColor(QPalette::Window, Qt::blue);
		self.sender().setPalette(pal)
		pal = QtGui.QPalette()
		pal.setColor(QtGui.QPalette.Button, QtCore.Qt.yellow)
		self.pb_apply.setPalette(pal)

		# print(path_list)

		if str(path_list) in self.changed_settings:
			# print("FOUND ITEM")
			self.changed_settings[str(path_list)]["value"] = item_value
		else:
			# print("NEW PATH")
			self.changed_settings[str(path_list)] = {}
			self.changed_settings[str(path_list)]["value"] = item_value
			self.changed_settings[str(path_list)]["path"] = path_list

		
	def apply_changes(self):
		my_drive = self.select_odrive()
		# print(self.changed_settings)
		for key in self.changed_settings:
			# print(len(self.changed_settings[key]["path"]))
			path_length = len(self.changed_settings[key]["path"])
			# print(self.changed_settings[key]["value"])
			path = self.changed_settings[key]["path"]
			if path_length == 3:
				exec("my_drive.{}.{} = {}".format(path[-2], path[-3], self.changed_settings[key]["value"]))
				# my_drive._remote_attributes[]._remote_attributes[] = self.changed_settings[key]["value"]
			elif path_length == 4:
				exec("my_drive.{}.{}.{} = {}".format(path[-2], path[-3], path[-4], self.changed_settings[key]["value"]))
				# my_drive._remote_attributes[path[-2]]._remote_attributes[path[-3]]._remote_attributes[path[-4]] = self.changed_settings[key]["value"]
			elif path_length == 5:
				exec("my_drive.{}.{}.{}.{} = {}".format(path[-2], path[-3], path[-4], path[-5], self.changed_settings[key]["value"]))
				# my_drive._remote_attributes[path[-2]]._remote_attributes[path[-3]]._remote_attributes[path[-4]]._remote_attributes[path[-5]] = self.changed_settings[key]["value"]
			elif path_length == 6:
				exec("my_drive.{}.{}.{}.{}.{} = {}".format(path[-2], path[-3], path[-4], path[-5], path[-6], self.changed_settings[key]["value"]))
				# my_drive._remote_attributes[path[-2]]._remote_attributes[path[-3]]._remote_attributes[path[-4]]._remote_attributes[path[-5]]._remote_attributes[path[-6]] = self.changed_settings[key]["value"]
		self.tree_item_selected()
		# send all commands to odrive


	def deleteItems(self, del_layout):
		try:
			if del_layout.count() > 0:
				while del_layout.count():
					item = del_layout.takeAt(0)
					widget = item.widget()
					if widget is not None:
						widget.deleteLater()
					else:
						self.deleteItems(item.layout())
		except Exception as e:
			print("exception deleting: {}".format(e))

	def select_odrive(self):
		# try:
		path_list = []
		path_list = self.find_tree_parents(self.treeView.selectedIndexes()[0], path_list)
		path_list.reverse()
		odrive_number = int(path_list[0][-1])
		
		# print(path_list)
		# print(odrive_number)

		my_drive = self.my_drive_list[odrive_number]
		return my_drive


	def odrive_reboot(self):
		my_drive = self.select_odrive()
		try:
			# self.deleteItems(self.button_layout)
			self.controller_window.odrive_stopped()
			self.controller_window.close()
		except:
			pass
		try:
			my_drive.reboot()
		except Exception as e:
			print("exception rebooting,: {}".format(e))
			# print("did we reboot?")
		try:
			self.odrive_worker.stop()
		except Exception as e:
			print("exception stopping, closing: {}".format(e))
		self.deleteItems(self.sb_layout)
		self.deleteItems(self.button_layout)
		self.odrive_connect()

	def odrive_save_configuration(self):
		my_drive = self.select_odrive()

		my_drive.save_configuration()

	def odrive_erase_configuration(self):
		my_drive = self.select_odrive()
		my_drive.erase_configuration()

	def add_action_buttons(self):
		self.button_layout = QtWidgets.QGridLayout()

		self.pb_apply = QtWidgets.QPushButton()
		self.pb_apply.setText("Apply")
		self.pb_apply.pressed.connect(self.apply_changes)
		self.button_layout.addWidget(self.pb_apply,0,0,1,1)

		self.pb_save = QtWidgets.QPushButton()
		self.pb_save.setText("Save Configuration")
		self.pb_save.pressed.connect(self.odrive_save_configuration)
		self.button_layout.addWidget(self.pb_save,0,1,1,1)

		self.pb_erase = QtWidgets.QPushButton()
		self.pb_erase.setText("Erase Configuration")
		self.pb_erase.pressed.connect(self.odrive_erase_configuration)
		self.button_layout.addWidget(self.pb_erase,0,2,1,1)

		self.pb_reboot = QtWidgets.QPushButton()
		self.pb_reboot.setText("Reboot")
		self.pb_reboot.pressed.connect(self.odrive_reboot)
		self.button_layout.addWidget(self.pb_reboot,0,3,1,1)

		spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.button_layout.addItem(spacerItem, 0, 4, 1, 1)
		# self.sb_v_layout.addLayout(self.button_layout,0,0,1,1)
		self.gridLayout.addLayout(self.button_layout, 0, 1, 1, 1)


	def setup_non_members(self):
		pass

	def function_button_pressed(self):
		# print(self.sender().objectName())
		button_name = self.sender().objectName()
		
		if button_name == "clear_errors":
			my_drive = self.select_odrive()
			path_list = []
			path_list = self.find_tree_parents(self.treeView.selectedIndexes()[0], path_list)
			path_list.reverse()
			# print(path_list)
			exec_string = "my_drive.{}.clear_errors()".format(path_list[1])
			exec(exec_string)


	def add_function(self, item, my_drive):
		hbox = QtWidgets.QHBoxLayout()
		function_button = QtWidgets.QPushButton()
		function_button.setText(item["name"])
		function_button.setObjectName(item["name"])
		function_button.pressed.connect(self.function_button_pressed)
		hbox.addWidget(function_button)
		# print(item)
		if item["inputs"]:
			# print("has inputs")
			for input in item["inputs"]:
				# print("input name {} type {}".format(input["name"], input["type"]))
				if input["type"] == "int32":
					hbox.addLayout(self.add_input_int32(input))
				elif input["type"] == "uint32":
					hbox.addLayout(self.add_input_uint32(input))
				elif input["type"] == "float":
					hbox.addLayout(self.add_input_float(input))
				elif input["type"] == "bool":
					hbox.addLayout(self.add_input_bool(input))
				else:
					print("MISSING INPUT TYPE: {}".format(input["type"]))
		else:
			# print("no input")
			pass
		# function_button.pressed.connect(self.odrive_save_configuration)
		
		return hbox

	def add_input_bool(self, item):
		hbox = QtWidgets.QHBoxLayout()
		label = QtWidgets.QLabel()
		label.setText(item["name"])
		hbox.addWidget(label)
		if item["access"] == "rw":
			rb_t = QtWidgets.QRadioButton()
			rb_t.setObjectName("True")
			rb_f = QtWidgets.QRadioButton()
			rb_f.setObjectName("False")
			icon_false = QtGui.QIcon()
			icon_false.addPixmap(self.PIXMAP_FALSE, QtGui.QIcon.Normal, QtGui.QIcon.Off)
			icon_true = QtGui.QIcon()
			icon_true.addPixmap(self.PIXMAP_TRUE, QtGui.QIcon.Normal, QtGui.QIcon.Off)
			rb_t.setIcon(icon_true)
			rb_f.setIcon(icon_false)
			bgroup = QtWidgets.QButtonGroup(hbox) #
			bgroup.setObjectName(item["name"])
			# bgroup.buttonClicked.connect(self.radio_button_changed)
			bgroup.addButton(rb_t)
			bgroup.addButton(rb_f)
			# if my_drive._remote_attributes[item["name"]].get_value():
			# 	rb_t.setChecked(True)
			# else:
			# 	rb_f.setChecked(True)
			hbox2 = QtWidgets.QHBoxLayout()
			hbox2.addWidget(rb_t)
			hbox2.addWidget(rb_f)
			hbox.addLayout(hbox2)
		return hbox

	def add_input_float(self, item):
		hbox = QtWidgets.QHBoxLayout()
		label = QtWidgets.QLabel()
		label.setText(item["name"])
		hbox.addWidget(label)
		if item["access"] == "rw":
			val_label = QtWidgets.QDoubleSpinBox()
			val_label.setObjectName(item["name"])
			val_label.setMaximum(2147483647)
			val_label.setMinimum(-2147483647)
			val_label.setDecimals(8)
			# val_label.setValue(my_drive._remote_attributes[item["name"]].get_value())
			# val_label.valueChanged.connect(self.value_changed_test)
			# if "torque" in item["name"]:
				# print(item["name"])
				# print(my_drive._remote_attributes[item["name"]].get_value())
		hbox.addWidget(val_label)
		return hbox

	def add_input_uint32(self, item):
		hbox = QtWidgets.QHBoxLayout()
		label = QtWidgets.QLabel()
		label.setText(item["name"])
		hbox.addWidget(label)
		if item["access"] == "rw":
			val_label = QtWidgets.QSpinBox()
			val_label.setObjectName(item["name"])
			val_label.setMaximum(2147483647)
			# val_label.setValue(my_drive._remote_attributes[item["name"]].get_value())
			# val_label.valueChanged.connect(self.value_changed_test)
		hbox.addWidget(val_label)
		return hbox

	def add_input_int32(self, item):
		hbox = QtWidgets.QHBoxLayout()
		label = QtWidgets.QLabel()
		label.setText(item["name"])
		hbox.addWidget(label)
		if item["access"] == "rw":
			val_label = QtWidgets.QSpinBox()
			val_label.setObjectName(item["name"])
			val_label.setMaximum(32768)
			val_label.setMinimum(-32768)
			# val_label.setValue(my_drive._remote_attributes[item["name"]].get_value())
			# val_label.valueChanged.connect(self.value_changed_test)
		hbox.addWidget(val_label)
		return hbox

	def add_bool(self, item, my_drive):
		hbox = QtWidgets.QHBoxLayout()
		label = QtWidgets.QLabel()
		label.setText(item["name"])
		hbox.addWidget(label)
		if item["access"] == "r":
			val_label = QtWidgets.QLabel()
			if my_drive._remote_attributes[item["name"]].get_value():
				val_label.setPixmap(self.PIXMAP_TRUE)
			else:
				val_label.setPixmap(self.PIXMAP_FALSE)
			hbox.addWidget(val_label)
		elif item["access"] == "rw":
			rb_t = QtWidgets.QRadioButton()
			rb_t.setObjectName("True")
			rb_f = QtWidgets.QRadioButton()
			rb_f.setObjectName("False")
			icon_false = QtGui.QIcon()
			icon_false.addPixmap(self.PIXMAP_FALSE, QtGui.QIcon.Normal, QtGui.QIcon.Off)
			icon_true = QtGui.QIcon()
			icon_true.addPixmap(self.PIXMAP_TRUE, QtGui.QIcon.Normal, QtGui.QIcon.Off)
			rb_t.setIcon(icon_true)
			rb_f.setIcon(icon_false)
			bgroup = QtWidgets.QButtonGroup(hbox) #
			bgroup.setObjectName(item["name"])
			bgroup.buttonClicked.connect(self.radio_button_changed)
			bgroup.addButton(rb_t)
			bgroup.addButton(rb_f)
			if my_drive._remote_attributes[item["name"]].get_value():
				rb_t.setChecked(True)
			else:
				rb_f.setChecked(True)
			hbox2 = QtWidgets.QHBoxLayout()
			hbox2.addWidget(rb_t)
			hbox2.addWidget(rb_f)
			hbox.addLayout(hbox2)
		return hbox

	def add_float(self, item, my_drive):
		hbox = QtWidgets.QHBoxLayout()
		label = QtWidgets.QLabel()
		label.setText(item["name"])
		hbox.addWidget(label)
		if item["access"] == "r":
			val_label = QtWidgets.QLabel()
			val_label.setText(str(my_drive._remote_attributes[item["name"]].get_value()))
		elif item["access"] == "rw":
			val_label = QtWidgets.QDoubleSpinBox()
			val_label.setObjectName(item["name"])
			val_label.setMaximum(2147483647)
			val_label.setMinimum(-2147483647)
			val_label.setDecimals(8)
			val_label.setValue(my_drive._remote_attributes[item["name"]].get_value())
			val_label.valueChanged.connect(self.value_changed_test)
			# if "torque" in item["name"]:
				# print(item["name"])
				# print(my_drive._remote_attributes[item["name"]].get_value())
		hbox.addWidget(val_label)
		return hbox

	def add_uint64(self, item, my_drive):
		hbox = QtWidgets.QHBoxLayout()
		label = QtWidgets.QLabel()
		label.setText(item["name"])
		hbox.addWidget(label)
		if item["access"] == "r":
			val_label = QtWidgets.QLabel()
			val_label.setText(str(my_drive._remote_attributes[item["name"]].get_value()))
		elif item["access"] == "rw":
			val_label = QtWidgets.QSpinBox()
			val_label.setMaximum(18446744073709551616)
			val_label.setValue(my_drive._remote_attributes[item["name"]].get_value())
		hbox.addWidget(val_label)
		return hbox

	def add_uint32(self, item, my_drive):
		hbox = QtWidgets.QHBoxLayout()
		label = QtWidgets.QLabel()
		label.setText(item["name"])
		hbox.addWidget(label)
		if item["access"] == "r":
			val_label = QtWidgets.QLabel()
			val_label.setText(str(my_drive._remote_attributes[item["name"]].get_value()))
		elif item["access"] == "rw":
			val_label = QtWidgets.QSpinBox()
			val_label.setObjectName(item["name"])
			val_label.setMaximum(2147483647)
			val_label.setValue(my_drive._remote_attributes[item["name"]].get_value())
			val_label.valueChanged.connect(self.value_changed_test)
		hbox.addWidget(val_label)
		return hbox

	def add_uint16(self, item, my_drive):
		hbox = QtWidgets.QHBoxLayout()
		label = QtWidgets.QLabel()
		label.setText(item["name"])
		hbox.addWidget(label)
		if item["access"] == "r":
			val_label = QtWidgets.QLabel()
			val_label.setText(str(my_drive._remote_attributes[item["name"]].get_value()))
		elif item["access"] == "rw":
			val_label = QtWidgets.QSpinBox()
			val_label.setObjectName(item["name"])
			val_label.setMaximum(65536)
			val_label.setValue(my_drive._remote_attributes[item["name"]].get_value())
			val_label.valueChanged.connect(self.value_changed_test)
		hbox.addWidget(val_label)
		return hbox

	def add_uint8(self, item, my_drive):
		hbox = QtWidgets.QHBoxLayout()
		label = QtWidgets.QLabel()
		label.setText(item["name"])
		hbox.addWidget(label)
		if item["access"] == "r":
			val_label = QtWidgets.QLabel()
			val_label.setText(str(my_drive._remote_attributes[item["name"]].get_value()))
		elif item["access"] == "rw":
			val_label = QtWidgets.QSpinBox()
			val_label.setObjectName(item["name"])
			val_label.setMaximum(256)
			val_label.setValue(my_drive._remote_attributes[item["name"]].get_value())
			val_label.valueChanged.connect(self.value_changed_test)
		hbox.addWidget(val_label)
		return hbox

	def add_int32(self, item, my_drive):
		hbox = QtWidgets.QHBoxLayout()
		label = QtWidgets.QLabel()
		label.setText(item["name"])
		hbox.addWidget(label)
		if item["access"] == "r":
			val_label = QtWidgets.QLabel()
			val_label.setText(str(my_drive._remote_attributes[item["name"]].get_value()))
		elif item["access"] == "rw":
			val_label = QtWidgets.QSpinBox()
			val_label.setObjectName(item["name"])
			val_label.setMaximum(32768)
			val_label.setMinimum(-32768)
			val_label.setValue(my_drive._remote_attributes[item["name"]].get_value())
			val_label.valueChanged.connect(self.value_changed_test)
		hbox.addWidget(val_label)
		return hbox


		
# float, bool, json, uint64, uint8, uint32, object,  uint16, int32
	def add_single_layout_line(self, item, my_drive):
		line_layout = QtWidgets.QGridLayout()
		if "access" in item.keys():
			if item["type"] == "float":
				line_layout.addLayout(self.add_float(item, my_drive),0,0,1,1)
			elif item["type"] == "bool":
				line_layout.addLayout(self.add_bool(item, my_drive),0,0,1,1)
			elif item["type"] == "uint8":
				line_layout.addLayout(self.add_uint8(item, my_drive),0,0,1,1)
			elif item["type"] == "uint16":
				line_layout.addLayout(self.add_uint16(item, my_drive),0,0,1,1)
			elif item["type"] == "uint32":
				line_layout.addLayout(self.add_uint32(item, my_drive),0,0,1,1)
			elif item["type"] == "uint64":
				line_layout.addLayout(self.add_uint64(item, my_drive),0,0,1,1)
			elif item["type"] == "int32":
				line_layout.addLayout(self.add_int32(item, my_drive),0,0,1,1)
			else:
				print("MISSING implementation {")
				print(item["type"])
				print(item)
		else:
			if item["type"] == "function":
				line_layout.addLayout(self.add_function(item, my_drive),0,0,1,1)
			else:
			# pass
				print("MISSING implementation without access")
				print(item["type"])
				print(item)
		return line_layout
	

	def setup_group_box(self, item, my_drive):
		groupbox =  QtWidgets.QGroupBox()
		groupbox.setTitle(item["name"])
		groupbox.setObjectName(item["name"])
		groupBox_layout = QtWidgets.QGridLayout(groupbox)
		# print(my_drive._remote_attributes)
		# print(item.keys())
		row_index = 0
		if "members" in item.keys():
			for member in item["members"]:
				# print(member["name"])
				if "members" in member.keys():
					group = self.setup_group_box(member, my_drive._remote_attributes[item["name"]])
					groupBox_layout.addWidget(group,row_index,0,1,1)
					row_index += 1
				else:
					item_layout = self.add_single_layout_line(member, my_drive._remote_attributes[item["name"]])
					groupBox_layout.addLayout(item_layout, row_index ,0,1,1)
					row_index += 1
		else:
			item_layout = self.add_single_layout_line(item, my_drive._remote_attributes[item["name"]])
			groupBox_layout.addLayout(item_layout)
		return groupbox

	def clearQTreeWidget(self, tree):
		iterator = QtGui.QTreeWidgetItemIterator(tree, QtGui.QTreeWidgetItemIterator.All)
		while iterator.value():
			iterator.value().takeChildren()
			iterator +=1
		i = tree.topLevelItemCount()
		while i > -1:
			tree.takeTopLevelItem(i)
			i -= 1

	def setup_config_window(self):
		# print("setting up config")
		try:
			my_drive = self.select_odrive()
		except:
			return
		path_list = []
		path_list = self.find_tree_parents(self.treeView.selectedIndexes()[0], path_list)
		# print("setting up config")
		row_index = 0
		col_index = 1
		first_gpio = True
		first_config = True
		member_row_index = 0
		config_row_index = 0
		
		self.deleteItems(self.sb_layout)
		self.general_layout = QtWidgets.QGridLayout()
		self.sb_layout.addLayout(self.general_layout,0,0,1,1)

		path_len = len(path_list)
		path_list.reverse()
		# print(path_list)

		if path_len == 1:
			self.setup_general()
			# print("setup general") # Only high level
		elif path_len == 2:
			# print("first row findings") # setup only high level
			for item in my_drive._json_data:
				if item["name"] == path_list[1]:
					if "members" in item.keys():
						for member in item["members"]:
							if "members" in member.keys():
								pass
							else:
								# print("add Line item")
								item_layout = self.add_single_layout_line(member, my_drive._remote_attributes[path_list[1]])
								self.general_layout.addLayout(item_layout,row_index,0,1,1)
								row_index += 1
					else:
						print("Impossible case all selection are only members")
			spacerItem = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
			self.general_layout.addItem(spacerItem,row_index,0,1,1)
		elif path_len == 3:
			# print("Setting up fully")
			# print("first row findings") # setup only high level
			for item in my_drive._json_data:
				if item["name"] == path_list[1]:
					if "members" in item.keys():
						for member in item["members"]:
							if "members" in member.keys():
								if member["name"] == path_list[2]:
									group = self.setup_group_box(member, my_drive._remote_attributes[path_list[1]])

									self.member_layout = QtWidgets.QGridLayout()
									self.sb_layout.addLayout(self.member_layout,0,col_index,1,1)
									# group_row_index = 0
									self.member_layout.addWidget(group,0,0,1,1)
									spacerItem = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
									self.member_layout.addItem(spacerItem,1,0,1,1)
									col_index += 1
								# if "config" == member["name"] or "thermistor" in  member["name"]:
								# 	if first_config:
								# 		first_config = False
								# 		self.config_layout = QtWidgets.QGridLayout()
								# 		self.sb_layout.addLayout(self.config_layout,0,1,1,1)
								# 		self.config_layout.addWidget(group,config_row_index,0,1,1)
								# 		config_row_index += 1
								# 		if item["name"] == "can":
								# 			spacerItem = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
								# 			self.config_layout.addItem(spacerItem,config_row_index,0,1,1)
								# 	else:
								# 		self.config_layout.addWidget(group,config_row_index,0,1,1)
								# 		config_row_index += 1
								# 	if config_row_index == 3:
								# 		spacerItem = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
								# 		self.config_layout.addItem(spacerItem,config_row_index,0,1,1)

								# elif "motor" == member["name"]:
								# 	self.motor_layout = QtWidgets.QGridLayout()
								# 	self.sb_layout.addLayout(self.motor_layout,0,2,1,1)
								# 	self.motor_layout.addWidget(group,0,0,1,1)
								# 	spacerItem = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
								# 	self.motor_layout.addItem(spacerItem,1,0,1,1)
								# elif "controller" == member["name"]:
								# 	# print("3")
								# 	self.controller_layout = QtWidgets.QGridLayout()
								# 	self.sb_layout.addLayout(self.controller_layout,0,3,1,1)
								# 	self.controller_layout.addWidget(group,0,0,1,1)
								# 	# spacerItem = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
								# 	# self.motor_layout.addItem(spacerItem,1,0,1,1)
								# elif "sensorless_estimator" == member["name"]:
								# 	# self.motor_layout = QtWidgets.QGridLayout()
								# 	# self.sb_layout.addLayout(self.motor_layout,1,3,1,1)
								# 	self.controller_layout.addWidget(group,1,0,1,1)
								# elif "trap_traj" == member["name"]:
								# 	# self.motor_layout = QtWidgets.QGridLayout()
								# 	# self.sb_layout.addLayout(self.motor_layout,1,3,1,1)
								# 	self.controller_layout.addWidget(group,2,0,1,1)
								# 	spacerItem = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
								# 	self.controller_layout.addItem(spacerItem,3,0,1,1)
								# # elif "min_endstop" == member["name"]:
								# # 	# self.motor_layout = QtWidgets.QGridLayout()
								# # 	# self.sb_layout.addLayout(self.motor_layout,1,3,1,1)
								# # 	self.encoder_layout.addWidget(group,2,0,1,1)
								# # 	spacerItem = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
								# # 	self.encoder_layout.addItem(spacerItem,3,0,1,1)
								# elif "encoder" == member["name"]:
								# 	self.encoder_layout = QtWidgets.QGridLayout()
								# 	self.sb_layout.addLayout(self.encoder_layout,0,4,1,1)
								# 	self.encoder_layout.addWidget(group,0,0,1,1)
								# 	# spacerItem = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
								# 	# self.encoder_layout.addItem(spacerItem,1,0,1,1)
								# elif "min_endstop" == member["name"]:
								# 	# self.motor_layout = QtWidgets.QGridLayout()
								# 	# self.sb_layout.addLayout(self.motor_layout,1,3,1,1)
								# 	self.encoder_layout.addWidget(group,1,0,1,1)
								# 	# spacerItem = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
								# 	# self.controller_layout.addItem(spacerItem,3,0,1,1)
								# elif "max_endstop" == member["name"]:
								# 	# self.motor_layout = QtWidgets.QGridLayout()
								# 	# self.sb_layout.addLayout(self.motor_layout,1,3,1,1)
								# 	self.encoder_layout.addWidget(group,2,0,1,1)
								# 	spacerItem = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
								# 	self.encoder_layout.addItem(spacerItem,3,0,1,1)
								# # else:
								# # 	print(member["name"])
								# elif "gpio" in member["name"]:
								# 	if first_gpio:
								# 		first_gpio = False
								# 		self.gpio_layout = QtWidgets.QGridLayout()
								# 		self.sb_layout.addLayout(self.gpio_layout,0,col_index,1,1)
								# 		self.gpio_layout.addWidget(group,member_row_index,0,1,1)
										
								# 	else:
								# 		self.gpio_layout.addWidget(group,member_row_index,0,1,1)
								# 	member_row_index += 1
								# 	# print(member["name"])
								# 	# self.member_layout.addWidget(group,group_row_index,0,1,1)
								# 	# group_row_index += 1
								# else:
								
								# group = self.setup_group_box(member, my_drive._remote_attributes[path_list[1]])
							# else:
							# 	# print("add Line item")
							# 	item_layout = self.add_single_layout_line(member, my_drive._remote_attributes[path_list[1]])
							# 	self.general_layout.addLayout(item_layout,row_index,0,1,1)
							# 	row_index += 1
					else:
						print("Impossible case all selection are only members")
			spacerItem = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
			self.general_layout.addItem(spacerItem,row_index,0,1,1)

	def setup_config(self, tree_selection):
		my_drive = self.select_odrive()
		# print("setting up config")
		row_index = 0
		col_index = 1
		first_gpio = True
		first_config = True

		member_row_index = 0

		config_row_index = 0
		
		self.deleteItems(self.sb_layout)
		self.general_layout = QtWidgets.QGridLayout()
		self.sb_layout.addLayout(self.general_layout,0,0,1,1)
		for item in my_drive._json_data:
			if item["name"] == tree_selection:
				if "members" in item.keys():
					for member in item["members"]:
						# print(member)
						
						# print(my_drive._remote_attributes[tree_selection]._remote_attributes[member["name"]].get_value())
						if "members" in member.keys():
							
							# print("Found members")
							# for new_member in member["members"]:
							group = self.setup_group_box(member, my_drive._remote_attributes[tree_selection])

							if "config" == member["name"] or "thermistor" in  member["name"]:
								if first_config:
									first_config = False
									self.config_layout = QtWidgets.QGridLayout()
									self.sb_layout.addLayout(self.config_layout,0,1,1,1)
									self.config_layout.addWidget(group,config_row_index,0,1,1)
									config_row_index += 1
									if item["name"] == "can":
										spacerItem = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
										self.config_layout.addItem(spacerItem,config_row_index,0,1,1)
								else:
									self.config_layout.addWidget(group,config_row_index,0,1,1)
									config_row_index += 1
								if config_row_index == 3:
									spacerItem = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
									self.config_layout.addItem(spacerItem,config_row_index,0,1,1)

							elif "motor" == member["name"]:
								self.motor_layout = QtWidgets.QGridLayout()
								self.sb_layout.addLayout(self.motor_layout,0,2,1,1)
								self.motor_layout.addWidget(group,0,0,1,1)
								spacerItem = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
								self.motor_layout.addItem(spacerItem,1,0,1,1)
							elif "controller" == member["name"]:
								# print("3")
								self.controller_layout = QtWidgets.QGridLayout()
								self.sb_layout.addLayout(self.controller_layout,0,3,1,1)
								self.controller_layout.addWidget(group,0,0,1,1)
								# spacerItem = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
								# self.motor_layout.addItem(spacerItem,1,0,1,1)
							elif "sensorless_estimator" == member["name"]:
								# self.motor_layout = QtWidgets.QGridLayout()
								# self.sb_layout.addLayout(self.motor_layout,1,3,1,1)
								self.controller_layout.addWidget(group,1,0,1,1)
							elif "trap_traj" == member["name"]:
								# self.motor_layout = QtWidgets.QGridLayout()
								# self.sb_layout.addLayout(self.motor_layout,1,3,1,1)
								self.controller_layout.addWidget(group,2,0,1,1)
								spacerItem = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
								self.controller_layout.addItem(spacerItem,3,0,1,1)
							# elif "min_endstop" == member["name"]:
							# 	# self.motor_layout = QtWidgets.QGridLayout()
							# 	# self.sb_layout.addLayout(self.motor_layout,1,3,1,1)
							# 	self.encoder_layout.addWidget(group,2,0,1,1)
							# 	spacerItem = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
							# 	self.encoder_layout.addItem(spacerItem,3,0,1,1)
							elif "encoder" == member["name"]:
								self.encoder_layout = QtWidgets.QGridLayout()
								self.sb_layout.addLayout(self.encoder_layout,0,4,1,1)
								self.encoder_layout.addWidget(group,0,0,1,1)
								# spacerItem = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
								# self.encoder_layout.addItem(spacerItem,1,0,1,1)
							elif "min_endstop" == member["name"]:
								# self.motor_layout = QtWidgets.QGridLayout()
								# self.sb_layout.addLayout(self.motor_layout,1,3,1,1)
								self.encoder_layout.addWidget(group,1,0,1,1)
								# spacerItem = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
								# self.controller_layout.addItem(spacerItem,3,0,1,1)
							elif "max_endstop" == member["name"]:
								# self.motor_layout = QtWidgets.QGridLayout()
								# self.sb_layout.addLayout(self.motor_layout,1,3,1,1)
								self.encoder_layout.addWidget(group,2,0,1,1)
								spacerItem = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
								self.encoder_layout.addItem(spacerItem,3,0,1,1)
							# else:
							# 	print(member["name"])
							elif "gpio" in member["name"]:
								if first_gpio:
									first_gpio = False
									self.gpio_layout = QtWidgets.QGridLayout()
									self.sb_layout.addLayout(self.gpio_layout,0,col_index,1,1)
									self.gpio_layout.addWidget(group,member_row_index,0,1,1)
									
								else:
									self.gpio_layout.addWidget(group,member_row_index,0,1,1)
								member_row_index += 1
								# print(member["name"])
								# self.member_layout.addWidget(group,group_row_index,0,1,1)
								# group_row_index += 1
							else:
								self.member_layout = QtWidgets.QGridLayout()
								self.sb_layout.addLayout(self.member_layout,0,col_index,1,1)
								# group_row_index = 0
								self.member_layout.addWidget(group,0,0,1,1)
								spacerItem = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
								self.member_layout.addItem(spacerItem,1,0,1,1)
								col_index += 1
							# col_index += 1
							# spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
							# # self.button_layout.addItem(spacerItem, 0, 4, 1, 1)
							# self.sb_layout.addItem(spacerItem,1,col_index,1,1)

							# if "gpio" in member["name"]:
							# 	if first_gpio:
							# 		first_gpio = False
							# 		self.member_layout = QtWidgets.QGridLayout()
							# 		self.sb_layout.addLayout(self.member_layout,0,col_index,1,1)
							# 		self.member_layout.addWidget(group,member_row_index,0,1,1)
									
							# 	else:
							# 		self.member_layout.addWidget(group,member_row_index,0,1,1)
							# 	member_row_index += 1
							# 	# print(member["name"])
							# 	# self.member_layout.addWidget(group,group_row_index,0,1,1)
							# 	# group_row_index += 1
							# elif "thermistor" in member["name"] or "endstop" in member["name"]:
							# 	if first_thermistor:
							# 		first_thermistor = False
							# 		self.member_layout = QtWidgets.QGridLayout()
							# 		self.sb_layout.addLayout(self.member_layout,0,col_index,1,1)
							# 		self.member_layout.addWidget(group,member_row_index,0,1,1)
									
							# 	else:
							# 		self.member_layout.addWidget(group,member_row_index,0,1,1)
							# 	member_row_index += 1
							# 	if member_row_index == 2:
							# 		spacerItem = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
							# 		self.member_layout.addItem(spacerItem,member_row_index,0,1,1)
							# 		col_index += 1


							# else:
							# 	self.member_layout = QtWidgets.QGridLayout()
							# 	self.sb_layout.addLayout(self.member_layout,0,col_index,1,1)
							# 	# group_row_index = 0
							# 	self.member_layout.addWidget(group,0,0,1,1)
							# 	spacerItem = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
							# 	self.member_layout.addItem(spacerItem,1,0,1,1)
							# 	col_index += 1
							# col_index += 1
							# spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
							# # self.button_layout.addItem(spacerItem, 0, 4, 1, 1)
							# self.sb_layout.addItem(spacerItem,1,col_index,1,1)
							
						else:
							# print("add Line item")
							item_layout = self.add_single_layout_line(member, my_drive._remote_attributes[tree_selection])
							self.general_layout.addLayout(item_layout,row_index,0,1,1)
							row_index += 1
						# 	for new_member in member["members"]:
						# 		print(new_member)
						# 		group = self.setup_group_box(new_member, my_drive._remote_attributes[tree_selection])
						# 		# group = self.setup_group_box(new_member, my_drive._remote_attributes[tree_selection]._remote_attributes[new_member["name"]])
						# 		self.sb_layout.addWidget(group)
								# print(new_member)
						# item_layout = self.add_single_layout_line(member, my_drive._remote_attributes[tree_selection])

						# self.sb_layout.addLayout(item_layout,row_index,1,1,1)
						# row_index += 1
				else:
					print("Impossible case all selection are only members")
		spacerItem = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
		self.general_layout.addItem(spacerItem,row_index,0,1,1)
		# spacerItem = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		# self.sb_layout.addItem(spacerItem,0,col_index,1,1)
					

	def setup_general(self):
		my_drive = self.select_odrive()
		row_index = 0
		self.deleteItems(self.sb_layout)
		for item in my_drive._json_data:
			if "members" in item.keys():
				pass
			else:
				item_layout = self.add_single_layout_line(item, my_drive)
				self.sb_layout.addLayout(item_layout,row_index,1,1,1)
				row_index += 1
		spacerItem = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
							# self.button_layout.addItem(spacerItem, 0, 4, 1, 1)
		self.sb_layout.addItem(spacerItem,row_index,1,1,1)



	def close_application(self):
		print("Closing!!!")
		try:
			self.odrive_worker.stop()
		except Exception as e:
			print("exception stopping, closing: {}".format(e))
		sys.exit()

	def odrive_connect(self):
		# print("connecting")
		self.deleteItems(self.sb_layout)
		try:
			self.deleteItems(self.button_layout)
		except:
			pass
		self.treeView.setDisabled(True)
		try:
			
			# self.deleteItems(self.button_layout)
			self.controller_window.odrive_stopped()
			self.controller_window.close()
		except:
			pass
		# self.deleteItems(self.treeView)
		# self.treeView.selectAll()
		# delete_list = self.treeView.selectedIndexes() 
		# for item in delete_list:
			# item.deleteLater()
		# self.clearQTreeWidget(self.treeView)
		
		# self.odrive_connect()
		self.statusBar.showMessage("Connecting... \t This might take a while.")
		self.odrive_worker = odriveWorker()
		self.odrive_worker.odrive_found_sig.connect(self.odrive_connected)
		self.odrive_worker.set_odrive_number(self.odrive_number_sbox.value())
		self.odrive_worker.start()

	def odrive_connected(self, my_drive):
		self.treeView.setDisabled(False)
		self.statusBar.showMessage("Connected!", 5000)
		self.my_drive_list = my_drive
		self.treeView.setModel(self.setup_odrive_model(self.my_drive_list))

	def setup_odrive_model(self, my_drive_list):
		print("Found odrives {}. Setting up model.".format(len(my_drive_list)))
		model = QtGui.QStandardItemModel(0, 1, self)
		model.setHeaderData(0, QtCore.Qt.Horizontal, "Odrive")
		odrive_number = 0
		for my_drive in my_drive_list:
			# model.setHeaderData(1, QtCore.Qt.Horizontal, "Type")
			# isinstance(odrv0._remote_attributes["reboot"], fibre.remote_object.RemoteFunction)
			item = QtGui.QStandardItem("odrv{}".format(odrive_number))
			# child = QtGui.QStandardItem("General")
			# item.appendRow(child)
			# child = QtGui.QStandardItem("Control Test")
			# item.appendRow(child)
			for key in my_drive._remote_attributes.keys():
				if isinstance(my_drive._remote_attributes[key], fibre.remote_object.RemoteObject):
					child = QtGui.QStandardItem(key)
					for child_key in my_drive._remote_attributes[key]._remote_attributes.keys():
						if isinstance(my_drive._remote_attributes[key]._remote_attributes[child_key], fibre.remote_object.RemoteObject):
							sub1_child = QtGui.QStandardItem(child_key)
						# else:
						# 	sub1_child = QtGui.QStandardItem(child_key)
							child.appendRow(sub1_child)
					item.appendRow(child)
				# else:
				# 	# if key not in version_ignore_list:
				# 	child = QtGui.QStandardItem(key)
				# 	item.appendRow(child)
					# item.appendRow(child)
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

			model.setItem(odrive_number,0,item)
			odrive_number += 1
			# self.testmdi.show()
		return model

def main():
	app = QtWidgets.QApplication(sys.argv)  # A new instance of QApplication
	form = ExampleApp()                 # We set the form to be our (design)
	form.show()                         # Show the form
	app.exec_()                         # and execute the app

if __name__ == '__main__':              # if we're running file directly and not importing it
	main()                              # run the main function
