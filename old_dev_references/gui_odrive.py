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



# from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
app = QtWidgets.QApplication([])
window = QtWidgets.QWidget()
layout = QtWidgets.QVBoxLayout()
layout.addWidget(QtWidgets.QTreeView())
# layout.addWidget(QPushButton('Bottom'))
window.setLayout(layout)
window.show()
app.exec()