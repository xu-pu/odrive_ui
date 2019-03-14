

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets


import fibre


class CustomMDIArea(QtWidgets.QMdiArea):
	odrive_request_sig = QtCore.pyqtSignal()

	def __init__(self,type, parent=None):
		super(self.__class__, self).__init__()
		# self.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
		self.setAcceptDrops(True)
		self.my_drive_list = []
		# self.odrive = fibre.remote_object.RemoteObject()

	def dragEnterEvent(self, event):
		print("drag enter event")
		print(event)
		event.accept()

	def dragMoveEnter(self, event):
		print("drag move enter")
		print(event)

	def add_odrive(self, my_drive):
		self.my_drive = my_drive
		self.my_drive_list.append(my_drive)
		# print(self.odrive)
	def add_sliders_config(self, slider_config):
		self.slider_config = slider_config

	def dropEvent(self, event):
		print("drop event")
		subwindow_dict = {}

		for index in event.source().selectedIndexes():
			subwindow_list = self.find_parents_list(index)

			centralWidget = QtWidgets.QWidget(self)
			str1 = '-'.join(subwindow_list)
			centralWidget.setWindowTitle(str1)
			gridLayout = QtWidgets.QGridLayout(centralWidget)

			print(subwindow_list)
			cr = index.model().itemFromIndex(index)
			# subwindow_list.append(cr.text())
			print(cr.hasChildren())
			if cr.hasChildren():
				print(cr.text())
				# print(type(cr))
				label_list = []
				spinBox_list = []
				for row in range(0,cr.rowCount()):
					print("1 - " + cr.child(row,0).text())

					if cr.child(row, 0).hasChildren():
						subgroupBox =  QtWidgets.QGroupBox(centralWidget)
						subgroupBox.setObjectName(cr.child(row,0).text())
						subgroupBox.setTitle(cr.child(row,0).text())
						subgroupBox_layout = QtWidgets.QGridLayout(subgroupBox)
						# self.groupBox = QtWidgets.QGroupBox(self.centralWidget)
						# self.groupBox.setObjectName("groupBox")
						# self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox)
						for sub_child in range(0, cr.child(row,0).rowCount()):
							print("2 - " + cr.child(row,0).child(sub_child,0).text())

							if cr.child(row,0).child(sub_child,0).hasChildren():
								subgroupBox2 =  QtWidgets.QGroupBox(subgroupBox)
								subgroupBox2.setObjectName(cr.child(row,0).child(sub_child,0).text())
								subgroupBox2.setTitle(cr.child(row,0).child(sub_child,0).text())
								subgroupBox2_layout = QtWidgets.QGridLayout(subgroupBox2)
								for sub2_child in range(0, cr.child(row,0).child(sub_child,0).rowCount()):
									print("3 - " + cr.child(row,0).child(sub_child,0).child(sub2_child,0).text())

									if cr.child(row,0).child(sub_child,0).child(sub2_child,0).hasChildren():
										subgroupBox3 =  QtWidgets.QGroupBox(subgroupBox2)
										subgroupBox3.setObjectName(cr.child(row,0).child(sub_child,0).child(sub2_child,0).text())
										subgroupBox3.setTitle(cr.child(row,0).child(sub_child,0).child(sub2_child,0).text())
										subgroupBox3_layout = QtWidgets.QGridLayout(subgroupBox3)
										for sub3_child in range(0, cr.child(row,0).child(sub_child,0).child(sub2_child,0).rowCount()):
											print("4 - " + cr.child(row,0).child(sub_child,0).child(sub2_child,0).child(sub3_child,0).text())

											if cr.child(row,0).child(sub_child,0).child(sub2_child,0).child(sub3_child,0).hasChildren():
												for sub4_child in range(0, cr.child(row,0).child(sub_child,0).child(sub2_child,0).child(sub3_child,0).rowCount()):
													print("5 - " + cr.child(row,0).child(sub_child,0).child(sub2_child,0).child(sub3_child,0).child(sub4_child,0).text())
											else:
												print("4 no children")
												sub5_window_list = []
												sub5_window_list.clear()
												sub5_window_list = subwindow_list.copy()
												sub5_window_list.insert(0,cr.child(row,0).text())
												sub5_window_list.insert(0,cr.child(row,0).child(sub_child,0).text())
												sub5_window_list.insert(0,cr.child(row,0).child(sub_child,0).child(sub2_child,0).text())
												sub5_window_list.insert(0,cr.child(row,0).child(sub_child,0).child(sub2_child,0).child(sub3_child,0).text())
												subwindow_dict5 = self.add_single_layout_line(self.slider_config,sub5_window_list, self.my_drive)
												self.setup_line_items(subgroupBox3_layout, subwindow_dict5, sub3_child)
										subgroupBox2_layout.addWidget(subgroupBox3,sub2_child,0,1,-1,QtCore.Qt.AlignLeft)#AlignHCenter
									else:
										print("3 no children")
										sub4_window_list = []
										sub4_window_list.clear()
										sub4_window_list = subwindow_list.copy()
										sub4_window_list.insert(0,cr.child(row,0).text())
										sub4_window_list.insert(0,cr.child(row,0).child(sub_child,0).text())
										sub4_window_list.insert(0,cr.child(row,0).child(sub_child,0).child(sub2_child,0).text())
										subwindow_dict4 = self.add_single_layout_line(self.slider_config,sub4_window_list, self.my_drive)
										self.setup_line_items(subgroupBox2_layout, subwindow_dict4, sub2_child)
								subgroupBox_layout.addWidget(subgroupBox2,sub_child,0,1,-1,QtCore.Qt.AlignLeft)#AlignHCenter

							else:
								print("2 no children")
								sub3_window_list = []
								sub3_window_list.clear()
								sub3_window_list = subwindow_list.copy()
								sub3_window_list.insert(0,cr.child(row,0).text())
								sub3_window_list.insert(0,cr.child(row,0).child(sub_child,0).text())
								subwindow_dict3 = self.add_single_layout_line(self.slider_config,sub3_window_list, self.my_drive)
								self.setup_line_items(subgroupBox_layout, subwindow_dict3, sub_child)
						gridLayout.addWidget(subgroupBox,row,0,1,-1,QtCore.Qt.AlignLeft)#AlignHCenter
					else:
						print("1 no children")
						sub2_window_list = []
						sub2_window_list.clear()
						sub2_window_list = subwindow_list.copy()
						sub2_window_list.insert(0,cr.child(row,0).text())
						if sub2_window_list[0] in ["fw_version", "hw_version"]:
							subwindow_dict2 = check_version_type(sub2_window_list, self.my_drive)
							gridLayout.addWidget(subwindow_dict2["label"], row,0,1,1)
							gridLayout.addWidget(subwindow_dict2["value"], row,1,1,1)
						else:
							subwindow_dict2 = self.add_single_layout_line(self.slider_config,sub2_window_list, self.my_drive)
							self.setup_line_items(gridLayout, subwindow_dict2, row)
			else:
				print("0 no children")
				if subwindow_list[0] in ["fw_version", "hw_version"]:
					fw_dict = check_version_type(subwindow_list, self.my_drive)
					gridLayout.addLayout(fw_dict["HLayout"],0,0,1,2)
				else:
					subwindow_dict = self.add_single_layout_line(self.slider_config,subwindow_list, self.my_drive)
					gridLayout.addLayout(subwindow_dict["layout"]["HLayout"],0,0,1,-1)
				# gridLayout.addWidget(subwindow_dict["layout"]["label"], 0,0,1,1)
				# gridLayout.addWidget(subwindow_dict["layout"]["value"], 0,1,1,1)
			self.addSubWindow(centralWidget).show()


	def find_parents_list(self, index):
		subwindow_list = []
		cr = index.model().itemFromIndex(index)
		subwindow_list.append(cr.text())
		if index.parent().isValid():
			i1 = index.parent()
			# print(i1.model().itemFromIndex(i1).text())
			subwindow_list.append(i1.model().itemFromIndex(i1).text())
			if i1.parent().isValid():
				i2 = i1.parent()
				# print(i2.model().itemFromIndex(i2).text())
				subwindow_list.append(i2.model().itemFromIndex(i2).text())
				if i2.parent().isValid():
					i3 = i2.parent()
					# print(i3.model().itemFromIndex(i3).text())
					subwindow_list.append(i3.model().itemFromIndex(i3).text())
					if i3.parent().isValid():
						i4 = i3.parent()
						# print(i4.model().itemFromIndex(i4).text())
						subwindow_list.append(i4.model().itemFromIndex(i4).text())
		return subwindow_list

	def add_single_layout_line(self, slider_config,  path_list, my_drive):
		ra_dict = {}

		if path_list[1] == "config":
			if len(path_list) == 2:
				ra_dict["layout"] = self.add_config_item(slider_config, path_list, my_drive._remote_attributes[path_list[0]])
			elif len(path_list) == 3:
				ra_dict["layout"] = self.add_config_item(slider_config, path_list, my_drive._remote_attributes[path_list[1]]._remote_attributes[path_list[0]])
			elif len(path_list) == 4:
				ra_dict["layout"] = self.add_config_item(slider_config, path_list, my_drive._remote_attributes[path_list[2]]._remote_attributes[path_list[1]]._remote_attributes[path_list[0]])
			elif len(path_list) == 5:
				ra_dict["layout"] = self.add_config_item(slider_config, path_list, my_drive._remote_attributes[path_list[3]]._remote_attributes[path_list[2]]._remote_attributes[path_list[1]]._remote_attributes[path_list[0]])
		else:
			if len(path_list) == 2:
				if isinstance(my_drive._remote_attributes[path_list[0]], fibre.remote_object.RemoteFunction):
					ra_dict["layout"] = self.add_pushButton( path_list)
				elif isinstance(my_drive._remote_attributes[path_list[0]], fibre.remote_object.RemoteProperty):
					ra_dict["layout"] = self.add_label( path_list, my_drive._remote_attributes[path_list[0]])
			elif len(path_list) == 3:
				if isinstance(my_drive._remote_attributes[path_list[1]]._remote_attributes[path_list[0]], fibre.remote_object.RemoteFunction):
					ra_dict["layout"] = self.add_pushButton( path_list)
				elif isinstance(my_drive._remote_attributes[path_list[1]]._remote_attributes[path_list[0]], fibre.remote_object.RemoteProperty):
					ra_dict["layout"] = self.add_label( path_list, my_drive._remote_attributes[path_list[1]]._remote_attributes[path_list[0]])
			elif len(path_list) == 4:
				if isinstance(my_drive._remote_attributes[path_list[2]]._remote_attributes[path_list[1]]._remote_attributes[path_list[0]], fibre.remote_object.RemoteFunction):
					ra_dict["layout"] = self.add_pushButton( path_list)
				elif isinstance(my_drive._remote_attributes[path_list[2]]._remote_attributes[path_list[1]]._remote_attributes[path_list[0]], fibre.remote_object.RemoteProperty):
					ra_dict["layout"] = self.add_label( path_list, my_drive._remote_attributes[path_list[2]]._remote_attributes[path_list[1]]._remote_attributes[path_list[0]])
			elif len(path_list) == 5:
				if isinstance(my_drive._remote_attributes[path_list[3]]._remote_attributes[path_list[2]]._remote_attributes[path_list[1]]._remote_attributes[path_list[0]], fibre.remote_object.RemoteFunction):
					ra_dict["layout"] = self.add_pushButton( path_list)
				elif isinstance(my_drive._remote_attributes[path_list[3]]._remote_attributes[path_list[2]]._remote_attributes[path_list[1]]._remote_attributes[path_list[0]], fibre.remote_object.RemoteProperty):
					ra_dict["layout"] = self.add_label( path_list, my_drive._remote_attributes[path_list[3]]._remote_attributes[path_list[2]]._remote_attributes[path_list[1]]._remote_attributes[path_list[0]])
		return ra_dict

	def add_config_item(self, slider_config, path_list, remote_attribute):
		print(path_list[2])
		if path_list[2] == "axis0" or path_list[2] == "axis1":
			parent_name = "config"
		else:
			parent_name = path_list[2]

		if parent_name == "odrv0":
			ra_dict = {}
			ra_dict["value_path"] = remote_attribute

			ra_dict["label"] = QtWidgets.QLabel()
			ra_dict["label"].setObjectName(path_list[0])
			ra_dict["label"].setText(path_list[0])
			ra_dict["HLayout"] = QtWidgets.QHBoxLayout()
			ra_value = remote_attribute.get_value()
			if type(ra_value) == float:
				ra_dict["type"] = "float"
				ra_dict["value"] = QtWidgets.QDoubleSpinBox()
				ra_dict["value"].setValue(ra_value)
				ra_dict["HLayout"].addWidget(ra_dict["value"])
			elif type(ra_value) == int:
				ra_dict["type"] = "int"
				ra_dict["value"] = QtWidgets.QSpinBox()
				ra_dict["value"].setValue(ra_value)
				ra_dict["HLayout"].addWidget(ra_dict["value"])
			elif type(ra_value) == bool:
				ra_dict["type"] = "bool"
				ra_dict["radiobutton_t"] = QtWidgets.QRadioButton()
				ra_dict["radiobutton_f"] = QtWidgets.QRadioButton()
				icon_false = QtGui.QIcon()
				icon_false.addPixmap(QtGui.QPixmap("Icons/False.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
				icon_true = QtGui.QIcon()
				icon_true.addPixmap(QtGui.QPixmap("Icons/True.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
				ra_dict["radiobutton_t"].setIcon(icon_true)
				ra_dict["radiobutton_f"].setIcon(icon_false)
				ra_dict["buttonGroup"] = QtWidgets.QButtonGroup(ra_dict["HLayout"]) #
				ra_dict["buttonGroup"].addButton(ra_dict["radiobutton_t"])
				ra_dict["buttonGroup"].addButton(ra_dict["radiobutton_f"])
				ra_dict["HLayout"].addWidget(ra_dict["radiobutton_t"])
				ra_dict["HLayout"].addWidget(ra_dict["radiobutton_f"])
				if ra_value:
					ra_dict["radiobutton_t"].setChecked(True)
				else:
					ra_dict["radiobutton_f"].setChecked(True)
		else:
			# print(slider_config[parent_name]["item_list"])
			# if path_list[0] in slider_config.keys()
			for settings_item in slider_config[parent_name]["item_list"]:
				print(path_list[0])
				print(settings_item["name"].text())
				if path_list[0] == settings_item["name"].text():
					parent_item = settings_item
					print(parent_item)
				# print(path_list[0])
				# if path_list[0] == settings_item[parent_name]["name"].text():
					# parent_item = settings_item
			ra_dict = {}
			ra_dict["value_path"] = remote_attribute

			ra_dict["label"] = QtWidgets.QLabel()
			ra_dict["label"].setObjectName(path_list[0])
			ra_dict["label"].setText(path_list[0])
			ra_dict["HLayout"] = QtWidgets.QHBoxLayout()

			ra_value = remote_attribute.get_value()
			if type(ra_value) == float:
				ra_dict["type"] = "float"
				ra_dict["value"] = QtWidgets.QDoubleSpinBox()
				ra_dict["value"].setValue(ra_value)
				ra_dict["slider"] = QtWidgets.QSlider()
				ra_dict["slider"].setOrientation(QtCore.Qt.Horizontal)
				ra_dict["slider"].setMaximum(parent_item["max"].value())
				ra_dict["slider"].setMinimum(parent_item["min"].value())
				ra_dict["slider"].setSingleStep(parent_item["step"].value())
				ra_dict["slider"].setValue(ra_value)
				ra_dict["HLayout"].addWidget(ra_dict["slider"])
				ra_dict["HLayout"].addWidget(ra_dict["value"])

				#TODO add signals of value changed on slider to change it inside sliderbox
			elif type(ra_value) == int:
				ra_dict["type"] = "int"
				ra_dict["value"] = QtWidgets.QSpinBox()
				ra_dict["value"].setValue(ra_value)
				ra_dict["slider"] = QtWidgets.QSlider()
				ra_dict["slider"].setOrientation(QtCore.Qt.Horizontal)
				ra_dict["slider"].setMaximum(parent_item["max"].value())
				ra_dict["slider"].setMinimum(parent_item["min"].value())
				ra_dict["slider"].setSingleStep(parent_item["step"].value())
				ra_dict["slider"].setValue(ra_value)
				ra_dict["HLayout"].addWidget(ra_dict["slider"])
				ra_dict["HLayout"].addWidget(ra_dict["value"])

			elif type(ra_value) == bool:
				ra_dict["type"] = "bool"
				ra_dict["radiobutton_t"] = QtWidgets.QRadioButton()
				ra_dict["radiobutton_f"] = QtWidgets.QRadioButton()
				icon_false = QtGui.QIcon()
				icon_false.addPixmap(QtGui.QPixmap("Icons/False.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
				icon_true = QtGui.QIcon()
				icon_true.addPixmap(QtGui.QPixmap("Icons/True.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
				ra_dict["radiobutton_t"].setIcon(icon_true)
				ra_dict["radiobutton_f"].setIcon(icon_false)
				ra_dict["buttonGroup"] = QtWidgets.QButtonGroup(ra_dict["HLayout"]) #
				ra_dict["buttonGroup"].addButton(ra_dict["radiobutton_t"])
				ra_dict["buttonGroup"].addButton(ra_dict["radiobutton_f"])
				ra_dict["HLayout"].addWidget(ra_dict["radiobutton_t"])
				ra_dict["HLayout"].addWidget(ra_dict["radiobutton_f"])
				if ra_value:
					ra_dict["radiobutton_t"].setChecked(True)
				else:
					ra_dict["radiobutton_f"].setChecked(True)
				# pixmap_false = QtGui.QPixmap("Icons/False.jpg")
				# pixmap_true = QtGui.QPixmap("Icons/True.jpg")
				# ra_dict["value"] = QtWidgets.QLabel()
				# if ra_value:
				# 	ra_dict["value"].setPixmap(pixmap_true)
				# else:
				# 	ra_dict["value"].setPixmap(pixmap_false)
				# ra_dict["HLayout"].addWidget(ra_dict["value"])
		return ra_dict

	def add_label(self, path_list, remote_attribute):
		ra_dict = {}
		ra_dict["type"] = "label"
		ra_dict["label"] = QtWidgets.QLabel()
		ra_dict["label"].setObjectName(path_list[0])
		ra_dict["label"].setText(path_list[0])

		ra_dict["value"] = QtWidgets.QLabel()
		ra_value = remote_attribute.get_value()

		if type(ra_value) == float:
			ra_dict["value"].setText(str(ra_value))
		elif type(ra_value) == int:
			ra_dict["value"].setText(str(ra_value))
		elif type(ra_value) == bool:
			pixmap_false = QtGui.QPixmap("Icons/False.jpg")
			pixmap_true = QtGui.QPixmap("Icons/True.jpg")
			if ra_value:
				ra_dict["value"].setPixmap(pixmap_true)
			else:
				ra_dict["value"].setPixmap(pixmap_false)
		ra_dict["value_path"] = remote_attribute
		ra_dict["HLayout"] = QtWidgets.QHBoxLayout()
		ra_dict["HLayout"].addWidget(ra_dict["label"])
		ra_dict["HLayout"].addWidget(ra_dict["value"])
		return ra_dict

	def setup_line_items(self, grid_layout, subwindow_dict, row):
		if subwindow_dict["layout"]["type"] == "label":
			grid_layout.addWidget(subwindow_dict["layout"]["label"], row,0,1,1)
			grid_layout.addWidget(subwindow_dict["layout"]["value"], row,1,1,1)
		elif subwindow_dict["layout"]["type"] == "pushbutton":
			grid_layout.addWidget(subwindow_dict["layout"]["pushbutton"], row,0,1,2)
		elif subwindow_dict["layout"]["type"] == "float":
			grid_layout.addWidget(subwindow_dict["layout"]["label"], row,0,1,1)
			grid_layout.addWidget(subwindow_dict["layout"]["slider"], row,1,1,1)
			grid_layout.addWidget(subwindow_dict["layout"]["value"], row,2,1,1)
		elif subwindow_dict["layout"]["type"] == "int":
			grid_layout.addWidget(subwindow_dict["layout"]["label"], row,0,1,1)
			grid_layout.addWidget(subwindow_dict["layout"]["slider"], row,1,1,1)
			grid_layout.addWidget(subwindow_dict["layout"]["value"], row,2,1,1)
		elif subwindow_dict["layout"]["type"] == "bool":
			grid_layout.addWidget(subwindow_dict["layout"]["label"], row,0,1,1)
			grid_layout.addLayout(subwindow_dict["layout"]["HLayout"], row,2,1,-1)

	def add_pushButton(self, path_list):
		ra_dict = {}
		ra_dict["type"] = "pushbutton"
		ra_dict["pushbutton"] = QtWidgets.QPushButton()
		ra_dict["pushbutton"].setObjectName(path_list[0])
		ra_dict["pushbutton"].setText(path_list[0])
		ra_dict["HLayout"] = QtWidgets.QHBoxLayout()
		ra_dict["HLayout"].addWidget(ra_dict["pushbutton"])
		return ra_dict
