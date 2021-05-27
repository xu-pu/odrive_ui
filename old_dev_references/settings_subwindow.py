import UI_settings_window
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets
import json

ICON_SAVE_PATH = "Icons/odrive_icons/odrive_icons_Save.png"
ICON_OPEN_PATH = "Icons/odrive_icons/odrive_icons_Open.png"

class SettingsWindow(QtWidgets.QMainWindow, UI_settings_window.Ui_MainWindow):
	app_name = "Settings"
	def __init__(self):
		# Simple reason why we use it here is that it allows us to
		# access variables, methods etc in the design.py file
		super(self.__class__, self).__init__()
		self.setupUi(self)  # This is defined in design.py file automatically
							# It sets up layout and widgets that are defined
		self.setWindowTitle(self.app_name)

		self.mainToolBar = QtWidgets.QToolBar(self)
		self.mainToolBar.setObjectName("mainToolBar")
		self.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)

		self.save_action = self.mainToolBar.addAction("Save settings")
		self.save_icon = QtGui.QIcon()
		self.save_icon.addPixmap(QtGui.QPixmap(ICON_SAVE_PATH))
		self.save_action.setIcon(self.save_icon)

		self.restoreDefault_action = self.mainToolBar.addAction("Restore to default settings")
		self.restore_icon = QtGui.QIcon()
		self.restore_icon.addPixmap(QtGui.QPixmap(ICON_OPEN_PATH))
		self.restoreDefault_action.setIcon(self.restore_icon)

		self.settings_dict = self.open_json("settings/custom_settings.json")
		self.a_gb_dict = {} #dict that contains a group box for each settings item
		# elf.gridLayout_2.addWidget(self.groupBox, 1, 2, 1, 1)
		row = 2
		for key in self.settings_dict:
			print(key)
			self.a_gb_dict[key] = {}
			self.a_gb_dict[key]["groupBox"] = QtWidgets.QGroupBox(self.scrollArea)
			# self.a_gb_dict[key]["groupBox"].setGeometry(QtCore.QRect(20, 20, 571, 223))
			self.a_gb_dict[key]["groupBox"].setTitle(key)
			self.a_gb_dict[key]["gb_layout"] = QtWidgets.QGridLayout(self.a_gb_dict[key]["groupBox"])
			self.a_gb_dict[key]["layout"] = QtWidgets.QGridLayout()

			self.a_gb_dict[key]["name_label"] = QtWidgets.QLabel(self.a_gb_dict[key]["groupBox"])
			self.a_gb_dict[key]["name_label"].setText("Name")
			self.a_gb_dict[key]["layout"].addWidget(self.a_gb_dict[key]["name_label"], 0, 0, 1, 1)

			self.a_gb_dict[key]["min_label"] = QtWidgets.QLabel(self.a_gb_dict[key]["groupBox"])
			self.a_gb_dict[key]["min_label"].setText("Minimum")
			self.a_gb_dict[key]["layout"].addWidget(self.a_gb_dict[key]["min_label"], 0, 1, 1, 1)

			self.a_gb_dict[key]["max_label"] = QtWidgets.QLabel(self.a_gb_dict[key]["groupBox"])
			self.a_gb_dict[key]["max_label"].setText("Maximum")
			self.a_gb_dict[key]["layout"].addWidget(self.a_gb_dict[key]["max_label"], 0, 2, 1, 1)

			self.a_gb_dict[key]["ss_label"] = QtWidgets.QLabel(self.a_gb_dict[key]["groupBox"])
			self.a_gb_dict[key]["ss_label"].setText("Single Step")
			self.a_gb_dict[key]["layout"].addWidget(self.a_gb_dict[key]["ss_label"], 0, 3, 1, 1)

			self.a_gb_dict[key]["item_list"] = []
			test_n = 1 #self.settings_dict["odrive_config"][key].index(list_item)
			for list_item in self.settings_dict[key]:
				item_dict = {}
				item_dict["name"] = QtWidgets.QLabel(self.a_gb_dict[key]["groupBox"])
				item_dict["name"].setText(list_item["name"])
				self.a_gb_dict[key]["layout"].addWidget(item_dict["name"],test_n , 0, 1, 1)

				if list_item["type"] == "float":
					item_dict["min"] = QtWidgets.QDoubleSpinBox(self.a_gb_dict[key]["groupBox"])
					item_dict["min"].setDecimals(list_item["decimals"])
				else:
					item_dict["min"] = QtWidgets.QSpinBox(self.a_gb_dict[key]["groupBox"])
				item_dict["min"].setMaximum(list_item["max"])
				item_dict["min"].setMinimum(list_item["min"])
				item_dict["min"].setSingleStep(list_item["step"])
				item_dict["min"].setValue(list_item["slider_min"])
				self.a_gb_dict[key]["layout"].addWidget(item_dict["min"],test_n , 1, 1, 1)

				if list_item["type"] == "float":
					item_dict["max"] = QtWidgets.QDoubleSpinBox(self.a_gb_dict[key]["groupBox"])
					item_dict["max"].setDecimals(list_item["decimals"])
				else:
					item_dict["max"] = QtWidgets.QSpinBox(self.a_gb_dict[key]["groupBox"])
				item_dict["max"].setMaximum(list_item["max"])
				item_dict["max"].setMinimum(list_item["min"])
				item_dict["max"].setSingleStep(list_item["step"])
				item_dict["max"].setValue(list_item["slider_max"])
				self.a_gb_dict[key]["layout"].addWidget(item_dict["max"],test_n , 2, 1, 1)

				if list_item["type"] == "float":
					item_dict["step"] = QtWidgets.QDoubleSpinBox(self.a_gb_dict[key]["groupBox"])
					item_dict["step"].setDecimals(list_item["decimals"])
				else:
					item_dict["step"] = QtWidgets.QSpinBox(self.a_gb_dict[key]["groupBox"])
				item_dict["step"].setMaximum(list_item["max"])
				item_dict["step"].setMinimum(list_item["min"])
				item_dict["step"].setSingleStep(list_item["step"])
				item_dict["step"].setValue(list_item["slider_step"])
				self.a_gb_dict[key]["layout"].addWidget(item_dict["step"],test_n , 3, 1, 1)


				self.a_gb_dict[key]["item_list"].append(item_dict)
				test_n += 1
			self.a_gb_dict[key]["gb_layout"].addLayout(self.a_gb_dict[key]["layout"], 0, 0, 1, 1)
			self.gridLayout_3.addWidget(self.a_gb_dict[key]["groupBox"], row,0,1,1)
			row += 1



	def open_json(self, json_path):
		json_dict = {}
		with open(json_path) as f:
			json_dict = json.load(f)
		return json_dict

	def get_settings_value(self, parent_name, item_name):
		self.a_gb_dict[parent_name]["item_list"]
		return value
