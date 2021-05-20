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

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets

from serialThread import odriveWorker

import ui_odrive

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

class ExampleApp(QtWidgets.QMainWindow, ui_odrive.Ui_odriveMainWindow):
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

		# self.connect_to_odrive_action = self.mainToolBar.addAction("Connect to Odrive")
		# self.connect_icon = QtGui.QIcon()
		# self.connect_icon.addPixmap(QtGui.QPixmap(ICON_CONNECT_PATH), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		# self.connect_to_odrive_action.setIcon(self.connect_icon)
		# self.connect_to_odrive_action.triggered.connect(self.odrive_connect)

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

		# self.help_action = self.mainToolBar.addAction("Help")
		# self.help_icon = QtGui.QIcon()
		# self.help_icon.addPixmap(QtGui.QPixmap(ICON_HELP_PATH))
		# self.help_action.setIcon(self.help_icon)

		# self.treeView.setDragEnabled(True)
		# self.treeView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
		# self.treeView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
		# self.treeView.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
		# self.treeView.setAcceptDrops(True)
		# self.treeView.setDragDropMode(QtGui.QAbstractItemView.DragOnly)

		# self.testmdi = CustomMDIArea(self)
		# # self.s1 = QtWidgets.QScrollBar()
		# self.testmdi.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
		# self.testmdi.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
		# self.testmdi.odrive_request_sig.connect(self.odrive_requested)
		# self.gridLayout.addWidget(self.testmdi, 0, 2, -1, 1)

		# self.testmdi.add_sliders_config(self.settings_window.a_gb_dict)

		self.odrive_connect()


	# def odrive_requested(self):
	# 	self.testmdi.add_odrive(self.my_drive)

	def close_application(self):
		print("whooaaaa so custom!!!")
		# try:
		# 	self.odrive_worker.stop()
		# except:
		# 	pass
		sys.exit()

	def odrive_connect(self):
		# print("connecting")
		self.statusbar.showMessage("Connecting...")
		self.odrive_worker = odriveWorker()
		self.odrive_worker.odrive_found_sig.connect(self.odrive_connected)
		self.odrive_worker.start()

	def odrive_connected(self, my_drive):
		self.statusbar.showMessage("Connected!", 5000)
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
		for key in my_drive._remote_attributes.keys():
			# if key not in ignore_list:
			if isinstance(my_drive._remote_attributes[key], fibre.remote_object.RemoteObject):
				child = QtGui.QStandardItem(key)
				for child_key in my_drive._remote_attributes[key]._remote_attributes.keys():
					if isinstance(my_drive._remote_attributes[key]._remote_attributes[child_key], fibre.remote_object.RemoteObject):
						sub1_child = QtGui.QStandardItem(child_key)
						for sub1_child_key in my_drive._remote_attributes[key]._remote_attributes[child_key]._remote_attributes.keys():
							if isinstance(my_drive._remote_attributes[key]._remote_attributes[child_key]._remote_attributes[sub1_child_key], fibre.remote_object.RemoteObject):
								sub2_child = QtGui.QStandardItem(sub1_child_key)
								for sub2_child_key in my_drive._remote_attributes[key]._remote_attributes[child_key]._remote_attributes[sub1_child_key]._remote_attributes.keys():
									if isinstance(my_drive._remote_attributes[key]._remote_attributes[child_key]._remote_attributes[sub1_child_key]._remote_attributes[sub2_child_key], fibre.remote_object.RemoteObject):
										sub3_child = QtGui.QStandardItem(sub2_child_key)
										sub2_child.appendRow(sub3_child)
									else:
										sub3_child = QtGui.QStandardItem(sub2_child_key)
										sub2_child.appendRow(sub3_child)
								sub1_child.appendRow(sub2_child)
							else:
								sub2_child = QtGui.QStandardItem(sub1_child_key)
								sub1_child.appendRow(sub2_child)
						child.appendRow(sub1_child)
					else:
						sub1_child = QtGui.QStandardItem(child_key)
						child.appendRow(sub1_child)
					# elif
				item.appendRow(child)
			else:
				if key not in version_ignore_list:
					child = QtGui.QStandardItem(key)
					item.appendRow(child)

		child = QtGui.QStandardItem("fw_version")
		item.appendRow(child)
		child = QtGui.QStandardItem("hw_version")
		item.appendRow(child)

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
