
from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph import PlotWidget
import pyqtgraph as pg

class ControllerWindow(QtWidgets.QWidget, ):
	app_name = "Controller"
	def __init__(self):
		# Simple reason why we use it here is that it allows us to
		# access variables, methods etc in the design.py file
		super(self.__class__, self).__init__()
		# self.setupUi(self)  # This is defined in design.py file automatically
							# It sets up layout and widgets that are defined
		self.setWindowTitle(self.app_name)
		self.resize(1280, 720)
		pushButton = QtWidgets.QPushButton()
		# self.setCentralWidget(self.pushButton)
		self.layout = QtWidgets.QGridLayout()
		self.setLayout(self.layout)
		# self.layout.addWidget(pushButton)

		self.hbox = QtWidgets.QHBoxLayout()
		self.layout.addLayout(self.hbox,0,0,1,1)

		groupbox =  QtWidgets.QGroupBox()
		groupbox.setTitle("test")
		groupbox.setObjectName("test")
		groupbox.setMaximumSize(200, 100)

		self.control_vertical_layout = QtWidgets.QVBoxLayout()
		self.hbox.addLayout(self.control_vertical_layout)
		# self.hbox.addWidget(groupbox)

		

		self.verticalLayout = QtWidgets.QVBoxLayout()




		
		self.plotWidget_velocity = PlotWidget()
		self.plotWidget_velocity.setStyleSheet("")
		self.plotWidget_velocity.setObjectName("plotWidget_velocity")
		self.verticalLayout.addWidget(self.plotWidget_velocity)
		self.plotWidget_current = PlotWidget()
		self.plotWidget_current.setMinimumSize(QtCore.QSize(900, 0))
		self.plotWidget_current.setObjectName("plotWidget_current")
		self.verticalLayout.addWidget(self.plotWidget_current)
		self.plotWidget_position = PlotWidget()
		self.plotWidget_position.setObjectName("plotWidget_position")
		self.verticalLayout.addWidget(self.plotWidget_position)
		self.hbox.addLayout(self.verticalLayout)

		self.showAxis0_checkBox = QtWidgets.QCheckBox()
		self.showAxis0_checkBox.setChecked(True)
		self.showAxis0_checkBox.setObjectName("showAxis0_checkBox")
		self.verticalLayout.addWidget(self.showAxis0_checkBox)

		# self.showAxis1_checkBox = QtWidgets.QCheckBox()
		# self.showAxis1_checkBox.setEnabled(True)
		# self.showAxis1_checkBox.setChecked(True)
		# self.showAxis1_checkBox.setObjectName("showAxis1_checkBox")
		# self.verticalLayout.addWidget(self.showAxis1_checkBox)

		self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
		self.horizontalLayout_3.setContentsMargins(11, 11, 11, 11)
		self.horizontalLayout_3.setSpacing(6)
		self.horizontalLayout_3.setObjectName("horizontalLayout_3")
		self.showAxis1_checkBox = QtWidgets.QCheckBox()
		self.showAxis1_checkBox.setEnabled(True)
		self.showAxis1_checkBox.setChecked(True)
		self.showAxis1_checkBox.setObjectName("showAxis1_checkBox")
		self.horizontalLayout_3.addWidget(self.showAxis1_checkBox)
		self.label_13 = QtWidgets.QLabel()
		self.label_13.setObjectName("label_13")
		self.horizontalLayout_3.addWidget(self.label_13)
		self.label_14 = QtWidgets.QLabel()
		self.label_14.setText("")
		self.label_14.setPixmap(QtGui.QPixmap("Icons/legendLines/legendLines_Orange.png"))
		self.label_14.setObjectName("label_14")
		self.horizontalLayout_3.addWidget(self.label_14)
		self.label_8 = QtWidgets.QLabel()
		self.label_8.setObjectName("label_8")
		self.horizontalLayout_3.addWidget(self.label_8)
		self.label_9 = QtWidgets.QLabel()
		self.label_9.setText("")
		self.label_9.setPixmap(QtGui.QPixmap("Icons/legendLines/legendLines_Yellow.png"))
		self.label_9.setObjectName("label_9")
		self.label_13.setText("Setpoint")
		self.label_8.setText("Estimate")
		self.horizontalLayout_3.addWidget(self.label_9)

		self.verticalLayout.addLayout(self.horizontalLayout_3)

		self.clearGraph_pushButton = QtWidgets.QPushButton()
		self.clearGraph_pushButton.setObjectName("clearGraph_pushButton")
		self.verticalLayout.addWidget(self.clearGraph_pushButton)

		self.spinBox_graphTime = QtWidgets.QSpinBox()
		self.spinBox_graphTime.setMinimum(1)
		self.spinBox_graphTime.setMaximum(600)
		self.spinBox_graphTime.setProperty("value", 20)
		self.spinBox_graphTime.setObjectName("spinBox_graphTime")
		self.verticalLayout.addWidget(self.spinBox_graphTime)

		self.showAxis0_checkBox.stateChanged.connect(self.axis0_graph_state_changed)
		self.showAxis1_checkBox.stateChanged.connect(self.axis1_graph_state_changed)
		self.clearGraph_pushButton.clicked.connect(self.clearGraph_clicked)

		self.plotWidget_velocity.setLabel('bottom', 'Time', 's')
		self.plotWidget_velocity.setLabel('left', 'Velocity', 'rpm')
		self.plotWidget_velocity.setTitle("Velocity")

		self.plotWidget_position.setLabel('bottom', 'Time', 's')
		self.plotWidget_position.setLabel('left', 'Position', 'counts')
		self.plotWidget_position.setTitle("Position")

		self.plotWidget_current.setLabel('bottom', 'Time', 's')
		self.plotWidget_current.setLabel('left', 'Current', 'Iq')
		self.plotWidget_current.setTitle("Current")

		self.ad = {} #axis_dcit

		pen_sp_axis0 = pg.mkPen(color=(0, 128, 255), width=1) # Blue: 0 128 255
		pen_est_axis0 = pg.mkPen(color=(135, 0, 191), width=1) # Purple: 135 0 191

		pen_sp_axis1 = pg.mkPen(color=(255, 78, 0), width=1) # Red: 255 78 0
		pen_est_axis1 = pg.mkPen(color=(255, 212, 0), width=1) #Yellow 255 212 0
		 # Poop yellow)Orange: 155 170 0
		# old orange (color=(255, 192, 0)

		self.ad["axis0"] = {}
		self.ad["axis0"]["time_array"] = []
		self.ad["axis0"]["position"] = {}
		self.ad["axis0"]["position"]["estimate"] = []
		self.ad["axis0"]["position"]["set_point"] = []
		self.ad["axis0"]["velocity"] = {}
		self.ad["axis0"]["velocity"]["estimate"] = []
		self.ad["axis0"]["velocity"]["set_point"] = []
		self.ad["axis0"]["current"] = {}
		self.ad["axis0"]["current"]["estimate"] = []
		self.ad["axis0"]["current"]["set_point"] = []
		self.ad["axis0"]["vel_sp_curve"] = self.plotWidget_velocity.plot(name="Setpoint", pen=pen_sp_axis0)
		self.ad["axis0"]["vel_est_curve"] = self.plotWidget_velocity.plot(name="Estimate", pen=pen_est_axis0)
		self.ad["axis0"]["pos_sp_curve"] = self.plotWidget_position.plot(name="Setpoint", pen=pen_sp_axis0)
		self.ad["axis0"]["pos_est_curve"] = self.plotWidget_position.plot(name="Estimate", pen=pen_est_axis0)
		self.ad["axis0"]["current_sp_curve"] = self.plotWidget_current.plot(name="Setpoint", pen=pen_sp_axis0)
		self.ad["axis0"]["current_est_curve"] = self.plotWidget_current.plot(name="Estimate", pen=pen_est_axis0)

		self.ad["axis1"] = {}
		self.ad["axis1"]["time_array"] = []
		self.ad["axis1"]["position"] = {}
		self.ad["axis1"]["position"]["estimate"] = []
		self.ad["axis1"]["position"]["set_point"] = []
		self.ad["axis1"]["velocity"] = {}
		self.ad["axis1"]["velocity"]["estimate"] = []
		self.ad["axis1"]["velocity"]["set_point"] = []
		self.ad["axis1"]["current"] = {}
		self.ad["axis1"]["current"]["estimate"] = []
		self.ad["axis1"]["current"]["set_point"] = []
		self.ad["axis1"]["vel_sp_curve"] = self.plotWidget_velocity.plot(name="Setpoint", pen=pen_sp_axis1)
		self.ad["axis1"]["vel_est_curve"] = self.plotWidget_velocity.plot(name="Estimate", pen=pen_est_axis1)
		self.ad["axis1"]["pos_sp_curve"] = self.plotWidget_position.plot(name="Setpoint", pen=pen_sp_axis1)
		self.ad["axis1"]["pos_est_curve"] = self.plotWidget_position.plot(name="Estimate", pen=pen_est_axis1)
		self.ad["axis1"]["current_sp_curve"] = self.plotWidget_current.plot(name="Setpoint", pen=pen_sp_axis1)
		self.ad["axis1"]["current_est_curve"] = self.plotWidget_current.plot(name="Estimate", pen=pen_est_axis1)

		self.axis0_state = None
		self.axis1_state = None

		# print(self.my_drive)
	def give_odrive(self, my_drive):
		self.my_drive = my_drive

		self.timer = pg.QtCore.QTimer()
		self.timer.timeout.connect(self.update_statuses)
		self.timer.start(500)

		self.ad["start_time"] = pg.ptime.time()
		self.timer_graphUpdate = pg.QtCore.QTimer()
		self.timer_graphUpdate.timeout.connect(self.update_graphs)
		self.timer_graphUpdate.start(20)

	def odrive_stopped(self):
		self.timer.stop()
		self.timer_graphUpdate.stop()

	def clearGraph_clicked(self):
		self.clear_axis_graph_lists("axis0")
		self.clear_axis_graph_lists("axis1")
		self.ad["start_time"] = pg.ptime.time()

	def axis0_graph_state_changed(self, state):
		if state != QtCore.Qt.Checked:
			self.clear_axis_graph_lists("axis0")
		self.axis_graph_state_changed()

	def axis1_graph_state_changed(self, state):
		if state != QtCore.Qt.Checked:
			self.clear_axis_graph_lists("axis1")
		self.axis_graph_state_changed()

	def axis_graph_state_changed(self):
		axis0_state = self.showAxis0_checkBox.isChecked()
		axis1_state = self.showAxis1_checkBox.isChecked()
		if axis0_state == False and axis1_state == False:
			self.timer_graphUpdate.stop()
			# add something to clear graphs
		else:
			if self.timer_graphUpdate.isActive() == False:
				self.timer_graphUpdate.start(20)
				self.ad["start_time"] = pg.ptime.time()

	def clear_axis_graph_lists(self, axis_key):
		self.ad[axis_key]["time_array"] = []
		self.ad[axis_key]["velocity"]["set_point"] = []
		self.ad[axis_key]["velocity"]["estimate"] = []
		self.ad[axis_key]["current"]["set_point"] = []
		self.ad[axis_key]["current"]["estimate"] = []
		self.ad[axis_key]["position"]["set_point"] = []
		self.ad[axis_key]["position"]["estimate"] = []
		self.ad[axis_key]["vel_sp_curve"].setData([],[])
		self.ad[axis_key]["vel_est_curve"].setData([],[])
		self.ad[axis_key]["current_sp_curve"].setData([],[])
		self.ad[axis_key]["current_est_curve"].setData([],[])
		self.ad[axis_key]["pos_sp_curve"].setData([],[])
		self.ad[axis_key]["pos_est_curve"].setData([],[])

	def update_velocity_graph(self, axis_key, odrv_axis):
		self.ad[axis_key]["velocity"]["estimate"].append(odrv_axis.encoder.vel_estimate)
		self.ad[axis_key]["velocity"]["set_point"].append(odrv_axis.controller.vel_setpoint)
		self.ad[axis_key]["vel_sp_curve"].setData(self.ad[axis_key]["time_array"], self.ad[axis_key]["velocity"]["set_point"])
		self.ad[axis_key]["vel_est_curve"].setData(self.ad[axis_key]["time_array"], self.ad[axis_key]["velocity"]["estimate"])

	def update_current_graph(self, axis_key, odrv_axis):
		self.ad[axis_key]["current"]["estimate"].append(odrv_axis.motor.current_control.Iq_measured)
		self.ad[axis_key]["current"]["set_point"].append(odrv_axis.motor.current_control.Iq_setpoint)
		self.ad[axis_key]["current_sp_curve"].setData(self.ad[axis_key]["time_array"], self.ad[axis_key]["current"]["set_point"])
		self.ad[axis_key]["current_est_curve"].setData(self.ad[axis_key]["time_array"], self.ad[axis_key]["current"]["estimate"])

	def update_position_graph(self, axis_key, odrv_axis):
		self.ad[axis_key]["position"]["estimate"].append(odrv_axis.encoder.pos_estimate)
		self.ad[axis_key]["position"]["set_point"].append(odrv_axis.controller.pos_setpoint)
		self.ad[axis_key]["pos_sp_curve"].setData(self.ad[axis_key]["time_array"], self.ad[axis_key]["position"]["set_point"])
		self.ad[axis_key]["pos_est_curve"].setData(self.ad[axis_key]["time_array"], self.ad[axis_key]["position"]["estimate"])

	def update_X_range(self, axis):
		upper_limit = self.ad[axis]["time_array"][-1]
		lower_limit = self.ad[axis]["time_array"][0]
		delta = self.spinBox_graphTime.value()
		if (upper_limit - lower_limit) > delta:
			while((upper_limit - lower_limit) > delta):
				self.ad[axis]["time_array"].pop(0)
				self.ad[axis]["velocity"]["estimate"].pop(0)
				self.ad[axis]["velocity"]["set_point"].pop(0)
				self.ad[axis]["current"]["estimate"].pop(0)
				self.ad[axis]["current"]["set_point"].pop(0)
				self.ad[axis]["position"]["estimate"].pop(0)
				self.ad[axis]["position"]["set_point"].pop(0)
				upper_limit = self.ad[axis]["time_array"][-1]
				lower_limit = self.ad[axis]["time_array"][0]

	def update_statuses(self):
		pass
		# self.update_voltage()
		# try:
		# 	self.update_machine_state()
		# 	self.update_controller_mode()
		# 	self.error_checks()
		# except Exception as e:
		# 	print(e)
		# 	self.odrive_disconnected_exception()

		# print(self.my_drive.vbus_voltage)
	def update_graphs(self):
		delta = pg.ptime.time() - self.ad["start_time"]
		try:
			if self.showAxis0_checkBox.isChecked():
				self.ad["axis0"]["time_array"].append(delta)
				self.update_velocity_graph("axis0", self.my_drive.axis0)
				self.update_position_graph("axis0", self.my_drive.axis0)
				self.update_current_graph("axis0", self.my_drive.axis0)
				self.update_X_range("axis0")
			if self.showAxis1_checkBox.isChecked():
				self.ad["axis1"]["time_array"].append(delta)
				self.update_velocity_graph("axis1", self.my_drive.axis1)
				self.update_position_graph("axis1", self.my_drive.axis1)
				self.update_current_graph("axis1", self.my_drive.axis1)
				self.update_X_range("axis1")

		except Exception as e:
			print(e)
			# self.odrive_disconnected_exception()

		# self.centralWidget = QtWidgets.QWidget(MainWindow)
		# self.centralWidget.setObjectName("centralWidget")
		# gridLayout = QtWidgets.QGridLayout(self)

		# treeView = QtWidgets.QTreeView()
		# # self.treeView.setMinimumSize(QtCore.QSize(250, 0))
		# treeView.setMaximumSize(QtCore.QSize(200,1000))
		# treeView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
		# # self.treeView.setObjectName("treeView")
		# self.layout.addWidget(treeView, 0, 0, 2, 1)