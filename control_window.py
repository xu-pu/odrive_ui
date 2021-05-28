
from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph import PlotWidget
import pyqtgraph as pg
# import odrive
from odrive.enums import *

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
		# self.setCentralWidget(self.pushButton)
		self.new_layout = QtWidgets.QGridLayout()
		self.setLayout(self.new_layout)
		# self.layout.addWidget(pushButton)

		self.hbox = QtWidgets.QHBoxLayout()
		self.new_layout.addLayout(self.hbox,0,0,1,1)

		self.ct = {}

		self.ct["axis0"] = {}
		self.ct["axis1"] = {}
		
		# self.ct["axis0"]velocity_label = QtWidgets.QLabel()
		# self.ct["axis0"]velocity_label.setText("Velocity (Turns/s)")
		# self.ct["axis0"]control_buttons_layout.addWidget(self.ct["axis0"]velocity_label, 1, 0, 1, 1)
		self.setup_control_axis("axis0")
		self.setup_control_axis("axis1")

		# self.ct["axis0"]control_box.addLayout
		# self.ct["axis0"]control_box.setObjectName("test")
		# self.ct["axis0"]control_box.setMaximumWidth(300)

		# self.axis1_control_box =  QtWidgets.QGroupBox()
		# self.axis1_control_box.setTitle("Axis1")
		# self.ct["axis0"]control_box.setObjectName("test")
		# self.axis1_control_box.setMaximumWidth(300)

		self.control_vertical_layout = QtWidgets.QVBoxLayout()
		self.control_vertical_layout.addWidget(self.ct["axis0"]["control_box"])
		self.control_vertical_layout.addWidget(self.ct["axis1"]["control_box"])
		self.hbox.addLayout(self.control_vertical_layout)
		# self.hbox.addWidget(groupbox)

		

		self.verticalLayout = QtWidgets.QVBoxLayout()
		self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
		self.verticalLayout.addLayout(self.horizontalLayout_3)

		self.hbox.addLayout(self.verticalLayout)



		
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
		

		

		# self.showAxis1_checkBox = QtWidgets.QCheckBox()
		# self.showAxis1_checkBox.setEnabled(True)
		# self.showAxis1_checkBox.setChecked(True)
		# self.showAxis1_checkBox.setObjectName("showAxis1_checkBox")
		# self.verticalLayout.addWidget(self.showAxis1_checkBox)

		

		self.showAxis0_checkBox = QtWidgets.QCheckBox()
		self.showAxis0_checkBox.setText("Axis0")
		self.showAxis0_checkBox.setChecked(True)
		self.showAxis0_checkBox.setObjectName("showAxis0_checkBox")
		self.horizontalLayout_3.addWidget(self.showAxis0_checkBox)

		self.label_2 = QtWidgets.QLabel("Estimate")
		self.label_2.setObjectName("label_2")
		self.horizontalLayout_3.addWidget(self.label_2)
		self.label_6 = QtWidgets.QLabel()
		self.label_6 = QtWidgets.QLabel()
		self.label_6.setText("")
		self.label_6.setPixmap(QtGui.QPixmap("Icons/legendLines/legendLines_Blue.png"))
		self.label_6.setObjectName("label_6")
		self.horizontalLayout_3.addWidget(self.label_6)
		self.label = QtWidgets.QLabel("Estimate")
		self.label.setObjectName("label")
		self.horizontalLayout_3.addWidget(self.label)
		self.label_7 = QtWidgets.QLabel()
		self.label_7.setText("")
		self.label_7.setPixmap(QtGui.QPixmap("Icons/legendLines/legendLines_Purple.png"))
		self.label_7.setObjectName("label_7")
		self.horizontalLayout_3.addWidget(self.label_7)

		# self.horizontalLayout_3.setContentsMargins(11, 11, 11, 11)
		# self.horizontalLayout_3.setSpacing(6)
		self.horizontalLayout_3.setObjectName("horizontalLayout_3")
		self.showAxis1_checkBox = QtWidgets.QCheckBox()
		self.showAxis1_checkBox.setEnabled(True)
		self.showAxis1_checkBox.setChecked(True)
		self.showAxis1_checkBox.setText("Axis1")
		# self.showAxis1_checkBox.setLayoutDirection(QtCore.Qt.RightToLeft)
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

		

		
		self.label_graph_time = QtWidgets.QLabel()
		self.label_graph_time.setText("Time Window (sec)")
		self.horizontalLayout_3.addWidget(self.label_graph_time)
		self.spinBox_graphTime = QtWidgets.QSpinBox()
		
		# self.spinBox_graphTime.setT
		self.spinBox_graphTime.setMinimum(1)
		self.spinBox_graphTime.setMaximum(600)
		self.spinBox_graphTime.setProperty("value", 20)
		self.spinBox_graphTime.setObjectName("spinBox_graphTime")
		self.horizontalLayout_3.addWidget(self.spinBox_graphTime)

		self.clearGraph_pushButton = QtWidgets.QPushButton()
		self.clearGraph_pushButton.setText("Clear Graph")
		self.clearGraph_pushButton.setObjectName("clearGraph_pushButton")
		self.horizontalLayout_3.addWidget(self.clearGraph_pushButton)

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

	def setup_control_axis(self, axis):
		size_width = 50
		size_height = 70

		self.ct[axis]["control_box"] =  QtWidgets.QGroupBox()
		self.ct[axis]["control_box"].setTitle(axis)
		self.ct[axis]["control_box_layout"] = QtWidgets.QVBoxLayout(self.ct[axis]["control_box"])
		self.ct[axis]["state_buttons_layout"] = QtWidgets.QGridLayout()
		self.ct[axis]["control_box_layout"].addLayout(self.ct[axis]["state_buttons_layout"])
		self.ct[axis]["state_idle_pb"] = QtWidgets.QPushButton()
		self.ct[axis]["state_idle_pb"].setMinimumSize(size_width,size_height)
		self.ct[axis]["state_idle_pb"].setText("Idle")
		self.ct[axis]["state_buttons_layout"].addWidget(self.ct[axis]["state_idle_pb"], 0, 0, 1, 1)
		self.ct[axis]["state_start_up_sequece_pb"] = QtWidgets.QPushButton()
		self.ct[axis]["state_start_up_sequece_pb"].setMinimumSize(size_width,size_height)#setMinimumSize(50,50)
		self.ct[axis]["state_start_up_sequece_pb"].setText("Startup\nSequence")
		self.ct[axis]["state_buttons_layout"].addWidget(self.ct[axis]["state_start_up_sequece_pb"], 0, 1, 1, 1)
		self.ct[axis]["state_full_calibration_sequence_pb"] = QtWidgets.QPushButton()
		self.ct[axis]["state_full_calibration_sequence_pb"].setMinimumSize(size_width,size_height)
		self.ct[axis]["state_full_calibration_sequence_pb"].setText("Full\nCalibration\nSeqience")
		self.ct[axis]["state_buttons_layout"].addWidget(self.ct[axis]["state_full_calibration_sequence_pb"], 0, 2, 1, 1)
		self.ct[axis]["state_motor_calibration_pb"] = QtWidgets.QPushButton()
		self.ct[axis]["state_motor_calibration_pb"].setMinimumSize(size_width,size_height)
		self.ct[axis]["state_motor_calibration_pb"].setText("Motor\nCalibration")
		self.ct[axis]["state_buttons_layout"].addWidget(self.ct[axis]["state_motor_calibration_pb"], 0, 3, 1, 1)
		self.ct[axis]["state_sensorless_control_pb"] = QtWidgets.QPushButton()
		self.ct[axis]["state_sensorless_control_pb"].setMinimumSize(size_width,size_height)
		self.ct[axis]["state_sensorless_control_pb"].setText("Sensorless\nControl")
		self.ct[axis]["state_buttons_layout"].addWidget(self.ct[axis]["state_sensorless_control_pb"], 1, 0, 1, 1)
		self.ct[axis]["state_encoder_index_search_pb"] = QtWidgets.QPushButton()
		self.ct[axis]["state_encoder_index_search_pb"].setMinimumSize(size_width,size_height)
		self.ct[axis]["state_encoder_index_search_pb"].setText("Encoder\nIndex\nSearch")
		self.ct[axis]["state_buttons_layout"].addWidget(self.ct[axis]["state_encoder_index_search_pb"], 1, 1, 1, 1)
		self.ct[axis]["state_encoder_offset_calibration_pb"] = QtWidgets.QPushButton()
		self.ct[axis]["state_encoder_offset_calibration_pb"].setMinimumSize(size_width,size_height)
		self.ct[axis]["state_encoder_offset_calibration_pb"].setText("Encoder\nOffset\nCalibration")
		self.ct[axis]["state_buttons_layout"].addWidget(self.ct[axis]["state_encoder_offset_calibration_pb"], 1, 2, 1, 1)
		self.ct[axis]["state_closed_loop_control_pb"] = QtWidgets.QPushButton()
		self.ct[axis]["state_closed_loop_control_pb"].setMinimumSize(size_width,size_height)
		self.ct[axis]["state_closed_loop_control_pb"].setText("Closed\nLoop\nControl")
		self.ct[axis]["state_buttons_layout"].addWidget(self.ct[axis]["state_closed_loop_control_pb"], 1, 3, 1, 1)

		self.ct[axis]["control_buttons_layout"] = QtWidgets.QGridLayout()
		self.ct[axis]["control_box_layout"].addLayout(self.ct[axis]["control_buttons_layout"])
		self.ct[axis]["torque_label"] = QtWidgets.QRadioButton()
		self.ct[axis]["torque_label"].setText("Torque (Nm)")
		self.ct[axis]["control_buttons_layout"].addWidget(self.ct[axis]["torque_label"], 0, 0, 1, 1)
		self.ct[axis]["torque_sb"] = QtWidgets.QSpinBox()
		self.ct[axis]["control_buttons_layout"].addWidget(self.ct[axis]["torque_sb"], 0, 1, 1, 1)
		self.ct[axis]["torque_cw_pb"] = QtWidgets.QPushButton()
		self.ct[axis]["torque_ccw_pb"] = QtWidgets.QPushButton()
		self.ct[axis]["torque_stop_pb"] = QtWidgets.QPushButton()
		self.ct[axis]["control_buttons_layout"].addWidget(self.ct[axis]["torque_cw_pb"], 0, 2, 1, 1)
		self.ct[axis]["control_buttons_layout"].addWidget(self.ct[axis]["torque_ccw_pb"], 0, 4, 1, 1)
		self.ct[axis]["control_buttons_layout"].addWidget(self.ct[axis]["torque_stop_pb"], 0, 3, 1, 1)

		self.ct[axis]["velocity_label"] = QtWidgets.QRadioButton()
		self.ct[axis]["velocity_label"].setText("Velocity (Turns/s)")
		self.ct[axis]["control_buttons_layout"].addWidget(self.ct[axis]["velocity_label"], 1, 0, 1, 1)
		self.ct[axis]["velocity_sb"] = QtWidgets.QSpinBox()
		self.ct[axis]["control_buttons_layout"].addWidget(self.ct[axis]["velocity_sb"], 1, 1, 1, 1)
		self.ct[axis]["velocity_cw_pb"] = QtWidgets.QPushButton()
		self.ct[axis]["velocity_ccw_pb"] = QtWidgets.QPushButton()
		self.ct[axis]["velocity_stop_pb"] = QtWidgets.QPushButton()
		self.ct[axis]["control_buttons_layout"].addWidget(self.ct[axis]["velocity_cw_pb"], 1, 2, 1, 1)
		self.ct[axis]["control_buttons_layout"].addWidget(self.ct[axis]["velocity_ccw_pb"], 1, 4, 1, 1)
		self.ct[axis]["control_buttons_layout"].addWidget(self.ct[axis]["velocity_stop_pb"], 1, 3, 1, 1)

		self.ct[axis]["position_label"] = QtWidgets.QRadioButton()
		self.ct[axis]["position_label"].setText("Position (Turns)")
		self.ct[axis]["control_buttons_layout"].addWidget(self.ct[axis]["position_label"], 2, 0, 1, 1)
		self.ct[axis]["position_sb"] = QtWidgets.QSpinBox()
		self.ct[axis]["control_buttons_layout"].addWidget(self.ct[axis]["position_sb"], 2, 1, 1, 1)
		self.ct[axis]["position_go_pb"] = QtWidgets.QPushButton("GO")
		# self.ct[axis]position_go_zero_pb = QtWidgets.QPushButton("Go to Zero")
		# self.ct[axis]position_stop_pb = QtWidgets.QPushButton()
		# self.ct[axis]control_buttons_layout.addWidget(self.ct[axis]position_go_zero_pb, 2, 2, 1, 1)
		self.ct[axis]["control_buttons_layout"].addWidget(self.ct[axis]["position_go_pb"], 2, 2, 1, 3)
		# self.ct[axis]control_buttons_layout.addWidget(self.ct[axis]position_stop_pb, 1, 3, 1, 1)

		self.ct[axis]["rb_group"] = QtWidgets.QButtonGroup(self.ct[axis]["control_buttons_layout"]) #
		# self.ct[axis]rb_group.setObjectName(item["name"])
		# bgroup.buttonClicked.connect(self.radio_button_changed)
		self.ct[axis]["rb_group"].addButton(self.ct[axis]["torque_label"])
		self.ct[axis]["rb_group"].addButton(self.ct[axis]["velocity_label"])
		self.ct[axis]["rb_group"].addButton(self.ct[axis]["position_label"])

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
		# pass
		# self.update_voltage()
		try:
			self.update_machine_state()
			self.update_controller_mode()
			self.error_checks()
		except Exception as e:
			print(e)
			self.odrive_disconnected_exception()


	def update_machine_state(self):
		current_state = self.my_drive.axis0.current_state
		if self.axis0_state != current_state:
			self.axis0_state = current_state
			print("New state axis0: {}".format(self.axis0_state))
			self.update_machine_state_color(current_state, 0)

		current_state = self.my_drive.axis1.current_state
		if self.axis1_state != current_state:
			self.axis1_state = current_state
			print("New state axis1: {}".format(self.axis1_state))
			self.update_machine_state_color(current_state, 1)

	def update_machine_state_color(self, current_state, axis):
			self.clear_state_buttons(axis)
			if current_state == AXIS_STATE_IDLE:
				self.set_state_button_color(axis, "state_idle_pb")
			elif current_state == AXIS_STATE_STARTUP_SEQUENCE:
				self.set_state_button_color(axis, "state_start_up_sequece_pb")
			elif current_state == AXIS_STATE_FULL_CALIBRATION_SEQUENCE:
				self.set_state_button_color(axis, "state_full_calibration_sequence_pb")
			elif current_state == AXIS_STATE_MOTOR_CALIBRATION:
				self.set_state_button_color(axis, "state_motor_calibration_pb")
			elif current_state == AXIS_STATE_SENSORLESS_CONTROL:
				self.set_state_button_color(axis, "state_sensorless_control_pb")
			elif current_state == AXIS_STATE_ENCODER_INDEX_SEARCH:
				self.set_state_button_color(axis, "state_encoder_index_search_pb")
			elif current_state == AXIS_STATE_ENCODER_OFFSET_CALIBRATION:
				self.set_state_button_color(axis, "state_encoder_offset_calibration_pb")
			elif current_state == AXIS_STATE_CLOSED_LOOP_CONTROL:
				self.set_state_button_color(axis, "state_closed_loop_control_pb")

	def clear_state_buttons(self, axis_num):
		if axis_num == 0:
			axis = "axis0"
		else:
			axis = "axis1"
		self.ct[axis]["state_idle_pb"].setStyleSheet("")
		self.ct[axis]["state_start_up_sequece_pb"].setStyleSheet("")
		self.ct[axis]["state_full_calibration_sequence_pb"].setStyleSheet("")
		self.ct[axis]["state_motor_calibration_pb"].setStyleSheet("")
		self.ct[axis]["state_sensorless_control_pb"].setStyleSheet("")
		self.ct[axis]["state_encoder_index_search_pb"].setStyleSheet("")
		self.ct[axis]["state_encoder_offset_calibration_pb"].setStyleSheet("")
		self.ct[axis]["state_closed_loop_control_pb"].setStyleSheet("")

	def set_state_button_color(self, axis_num, button):
		if axis_num == 0:
			axis = "axis0"
		else:
			axis = "axis1"
		self.ct[axis][button].setStyleSheet("background-color: rgb(246, 224, 143);")


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