
from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph import PlotWidget
import pyqtgraph as pg
# import odrive
from odrive.enums import *

class ControllerWindow(QtWidgets.QWidget):
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

		self.quit_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+Q"), self)
		self.quit_shortcut.activated.connect(self.close_application)

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
		

		self.control_statusBar = QtWidgets.QLabel()
		self.verticalLayout.addWidget(self.control_statusBar)
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

	def close_application(self):
		self.close()
		# print("Closing!!!")
		# try:
		# 	self.odrive_worker.stop()
		# except Exception as e:
		# 	print("exception stopping, closing: {}".format(e))
		# sys.exit()

	def setup_control_axis(self, axis):
		size_width = 50
		size_height = 70

		self.ct[axis]["control_box"] =  QtWidgets.QGroupBox()
		self.ct[axis]["control_box"].setTitle(axis)
		self.ct[axis]["control_box_layout"] = QtWidgets.QVBoxLayout(self.ct[axis]["control_box"])
		self.ct[axis]["state_buttons_layout"] = QtWidgets.QGridLayout()
		self.ct[axis]["control_box_layout"].addLayout(self.ct[axis]["state_buttons_layout"])
		self.ct[axis]["state_idle_pb"] = QtWidgets.QPushButton()
		self.ct[axis]["state_idle_pb"].clicked.connect(self.machine_state_clicked)
		self.ct[axis]["state_idle_pb"].setObjectName("state_idle_pb_{}".format(axis))
		self.ct[axis]["state_idle_pb"].setMinimumSize(size_width,size_height)
		self.ct[axis]["state_idle_pb"].setText("Idle")
		self.ct[axis]["state_buttons_layout"].addWidget(self.ct[axis]["state_idle_pb"], 0, 0, 1, 1)
		self.ct[axis]["state_start_up_sequece_pb"] = QtWidgets.QPushButton()
		self.ct[axis]["state_start_up_sequece_pb"].clicked.connect(self.machine_state_clicked)
		self.ct[axis]["state_start_up_sequece_pb"].setObjectName("state_start_up_sequece_pb_{}".format(axis))
		self.ct[axis]["state_start_up_sequece_pb"].setMinimumSize(size_width,size_height)#setMinimumSize(50,50)
		self.ct[axis]["state_start_up_sequece_pb"].setText("Startup\nSequence")
		self.ct[axis]["state_buttons_layout"].addWidget(self.ct[axis]["state_start_up_sequece_pb"], 0, 1, 1, 1)
		self.ct[axis]["state_full_calibration_sequence_pb"] = QtWidgets.QPushButton()
		self.ct[axis]["state_full_calibration_sequence_pb"].clicked.connect(self.machine_state_clicked)
		self.ct[axis]["state_full_calibration_sequence_pb"].setObjectName("state_full_calibration_sequence_pb_{}".format(axis))
		self.ct[axis]["state_full_calibration_sequence_pb"].setMinimumSize(size_width,size_height)
		self.ct[axis]["state_full_calibration_sequence_pb"].setText("Full\nCalibration\nSeqience")
		self.ct[axis]["state_buttons_layout"].addWidget(self.ct[axis]["state_full_calibration_sequence_pb"], 0, 2, 1, 1)
		self.ct[axis]["state_motor_calibration_pb"] = QtWidgets.QPushButton()
		self.ct[axis]["state_motor_calibration_pb"].clicked.connect(self.machine_state_clicked)
		self.ct[axis]["state_motor_calibration_pb"].setObjectName("state_motor_calibration_pb_{}".format(axis))
		self.ct[axis]["state_motor_calibration_pb"].setMinimumSize(size_width,size_height)
		self.ct[axis]["state_motor_calibration_pb"].setText("Motor\nCalibration")
		self.ct[axis]["state_buttons_layout"].addWidget(self.ct[axis]["state_motor_calibration_pb"], 0, 3, 1, 1)
		self.ct[axis]["state_sensorless_control_pb"] = QtWidgets.QPushButton()
		self.ct[axis]["state_sensorless_control_pb"].clicked.connect(self.machine_state_clicked)
		self.ct[axis]["state_sensorless_control_pb"].setObjectName("state_sensorless_control_pb_{}".format(axis))
		self.ct[axis]["state_sensorless_control_pb"].setMinimumSize(size_width,size_height)
		self.ct[axis]["state_sensorless_control_pb"].setText("Sensorless\nControl")
		self.ct[axis]["state_buttons_layout"].addWidget(self.ct[axis]["state_sensorless_control_pb"], 1, 0, 1, 1)
		self.ct[axis]["state_encoder_index_search_pb"] = QtWidgets.QPushButton()
		self.ct[axis]["state_encoder_index_search_pb"].clicked.connect(self.machine_state_clicked)
		self.ct[axis]["state_encoder_index_search_pb"].setObjectName("state_encoder_index_search_pb_{}".format(axis))
		self.ct[axis]["state_encoder_index_search_pb"].setMinimumSize(size_width,size_height)
		self.ct[axis]["state_encoder_index_search_pb"].setText("Encoder\nIndex\nSearch")
		self.ct[axis]["state_buttons_layout"].addWidget(self.ct[axis]["state_encoder_index_search_pb"], 1, 1, 1, 1)
		self.ct[axis]["state_encoder_offset_calibration_pb"] = QtWidgets.QPushButton()
		self.ct[axis]["state_encoder_offset_calibration_pb"].clicked.connect(self.machine_state_clicked)
		self.ct[axis]["state_encoder_offset_calibration_pb"].setObjectName("state_encoder_offset_calibration_pb_{}".format(axis))
		self.ct[axis]["state_encoder_offset_calibration_pb"].setMinimumSize(size_width,size_height)
		self.ct[axis]["state_encoder_offset_calibration_pb"].setText("Encoder\nOffset\nCalibration")
		self.ct[axis]["state_buttons_layout"].addWidget(self.ct[axis]["state_encoder_offset_calibration_pb"], 1, 2, 1, 1)
		self.ct[axis]["state_closed_loop_control_pb"] = QtWidgets.QPushButton()
		self.ct[axis]["state_closed_loop_control_pb"].clicked.connect(self.machine_state_clicked)
		self.ct[axis]["state_closed_loop_control_pb"].setObjectName("state_closed_loop_control_pb_{}".format(axis))
		self.ct[axis]["state_closed_loop_control_pb"].setMinimumSize(size_width,size_height)
		self.ct[axis]["state_closed_loop_control_pb"].setText("Closed\nLoop\nControl")
		self.ct[axis]["state_buttons_layout"].addWidget(self.ct[axis]["state_closed_loop_control_pb"], 1, 3, 1, 1)

		self.PIXMAP_FORWARD = QtGui.QPixmap("Icons/Right.png")
		self.PIXMAP_BACKWARD = QtGui.QPixmap("Icons/Left.png")
		self.PIXMAP_STOP = QtGui.QPixmap("Icons/odrive_icons_stop4.png")
		icon_forward = QtGui.QIcon()
		icon_forward.addPixmap(self.PIXMAP_FORWARD, QtGui.QIcon.Normal, QtGui.QIcon.Off)
		icon_backward = QtGui.QIcon()
		icon_backward.addPixmap(self.PIXMAP_BACKWARD, QtGui.QIcon.Normal, QtGui.QIcon.Off)
		icon_stop = QtGui.QIcon()
		icon_stop.addPixmap(self.PIXMAP_STOP, QtGui.QIcon.Normal, QtGui.QIcon.Off)

		self.ct[axis]["control_buttons_layout"] = QtWidgets.QGridLayout()
		self.ct[axis]["control_box_layout"].addLayout(self.ct[axis]["control_buttons_layout"])
		self.ct[axis]["torque_label"] = QtWidgets.QRadioButton()
		self.ct[axis]["torque_label"].setText("Torque (Nm)")
		self.ct[axis]["control_buttons_layout"].addWidget(self.ct[axis]["torque_label"], 0, 0, 1, 1)
		self.ct[axis]["torque_sb"] = QtWidgets.QSpinBox()
		self.ct[axis]["torque_sb"].setMaximum(100)
		self.ct[axis]["control_buttons_layout"].addWidget(self.ct[axis]["torque_sb"], 0, 1, 1, 1)
		self.ct[axis]["torque_cw_pb"] = QtWidgets.QPushButton()
		self.ct[axis]["torque_ccw_pb"] = QtWidgets.QPushButton()
		self.ct[axis]["torque_stop_pb"] = QtWidgets.QPushButton()
		self.ct[axis]["torque_cw_pb"].setIcon(icon_forward)
		self.ct[axis]["torque_ccw_pb"].setIcon(icon_backward)
		self.ct[axis]["torque_stop_pb"].setIcon(icon_stop)
		self.ct[axis]["torque_cw_pb"].setObjectName("torque_cw_pb_{}".format(axis))
		self.ct[axis]["torque_ccw_pb"].setObjectName("torque_ccw_pb{}".format(axis))
		self.ct[axis]["torque_stop_pb"].setObjectName("torque_stop_pb{}".format(axis))
		self.ct[axis]["torque_cw_pb"].pressed.connect(self.torque_button_pressed)
		self.ct[axis]["torque_ccw_pb"].pressed.connect(self.torque_button_pressed)
		self.ct[axis]["torque_stop_pb"].pressed.connect(self.torque_button_pressed)
		self.ct[axis]["control_buttons_layout"].addWidget(self.ct[axis]["torque_cw_pb"], 0, 4, 1, 1)
		self.ct[axis]["control_buttons_layout"].addWidget(self.ct[axis]["torque_ccw_pb"], 0, 2, 1, 1)
		self.ct[axis]["control_buttons_layout"].addWidget(self.ct[axis]["torque_stop_pb"], 0, 3, 1, 1)

		self.ct[axis]["velocity_label"] = QtWidgets.QRadioButton()
		self.ct[axis]["velocity_label"].setText("Velocity (Turns/s)")
		self.ct[axis]["control_buttons_layout"].addWidget(self.ct[axis]["velocity_label"], 1, 0, 1, 1)
		self.ct[axis]["velocity_sb"] = QtWidgets.QSpinBox()
		self.ct[axis]["velocity_sb"].setMaximum(1000)
		self.ct[axis]["control_buttons_layout"].addWidget(self.ct[axis]["velocity_sb"], 1, 1, 1, 1)
		self.ct[axis]["velocity_cw_pb"] = QtWidgets.QPushButton()
		self.ct[axis]["velocity_ccw_pb"] = QtWidgets.QPushButton()
		self.ct[axis]["velocity_stop_pb"] = QtWidgets.QPushButton()
		self.ct[axis]["velocity_cw_pb"].setIcon(icon_forward)
		self.ct[axis]["velocity_ccw_pb"].setIcon(icon_backward)
		self.ct[axis]["velocity_stop_pb"].setIcon(icon_stop)
		self.ct[axis]["velocity_cw_pb"].setObjectName("velocity_cw_pb{}".format(axis))
		self.ct[axis]["velocity_ccw_pb"].setObjectName("velocity_ccw_pb{}".format(axis))
		self.ct[axis]["velocity_stop_pb"].setObjectName("velocity_stop_pb{}".format(axis))
		self.ct[axis]["velocity_cw_pb"].pressed.connect(self.velocity_button_pressed)
		self.ct[axis]["velocity_ccw_pb"].pressed.connect(self.velocity_button_pressed)
		self.ct[axis]["velocity_stop_pb"].pressed.connect(self.velocity_button_pressed)
		self.ct[axis]["control_buttons_layout"].addWidget(self.ct[axis]["velocity_cw_pb"], 1, 4, 1, 1)
		self.ct[axis]["control_buttons_layout"].addWidget(self.ct[axis]["velocity_ccw_pb"], 1, 2, 1, 1)
		self.ct[axis]["control_buttons_layout"].addWidget(self.ct[axis]["velocity_stop_pb"], 1, 3, 1, 1)

		self.ct[axis]["position_label"] = QtWidgets.QRadioButton()
		self.ct[axis]["position_label"].setText("Position (Turns)")
		self.ct[axis]["control_buttons_layout"].addWidget(self.ct[axis]["position_label"], 2, 0, 1, 1)
		self.ct[axis]["position_sb"] = QtWidgets.QSpinBox()
		self.ct[axis]["position_sb"].setMaximum(10000)
		self.ct[axis]["position_sb"].setMinimum(10000)
		self.ct[axis]["position_sb"].setValue(0)
		self.ct[axis]["control_buttons_layout"].addWidget(self.ct[axis]["position_sb"], 2, 1, 1, 1)
		self.ct[axis]["position_go_pb"] = QtWidgets.QPushButton("GO")
		self.ct[axis]["position_go_pb"].setObjectName("position_go_pb{}".format(axis))
		self.ct[axis]["position_go_pb"].pressed.connect(self.position_button_pressed)

		# self.ct[axis]position_go_zero_pb = QtWidgets.QPushButton("Go to Zero")
		# self.ct[axis]position_stop_pb = QtWidgets.QPushButton()
		# self.ct[axis]control_buttons_layout.addWidget(self.ct[axis]position_go_zero_pb, 2, 2, 1, 1)
		self.ct[axis]["control_buttons_layout"].addWidget(self.ct[axis]["position_go_pb"], 2, 2, 1, 3)
		# self.ct[axis]control_buttons_layout.addWidget(self.ct[axis]position_stop_pb, 1, 3, 1, 1)

		self.ct[axis]["rb_group"] = QtWidgets.QButtonGroup(self.ct[axis]["control_buttons_layout"]) #
		self.ct[axis]["rb_group"].setObjectName(axis)
		self.ct[axis]["rb_group"].buttonClicked.connect(self.axis_controller_mode_changed)
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
		self.timer.start(250)

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

	def axis_controller_mode_changed(self, id):
		button_name = id.text()
		group_name = id.sender().objectName()
		# print("button name {}".format(button_name))
		# print("group name {}".format(group_name))
		if group_name == "axis0":
			if button_name == "Position (Turns)":
				self.axis_control_mode_changed(CONTROL_MODE_POSITION_CONTROL, 0)
			elif button_name == "Torque (Nm)":
				self.axis_control_mode_changed(CONTROL_MODE_TORQUE_CONTROL, 0)
			elif button_name == "Velocity (Turns/s)":
				self.axis_control_mode_changed(CONTROL_MODE_VELOCITY_CONTROL, 0)
		elif group_name == "axis1":
			if button_name == "Position (Turns)":
				self.axis_control_mode_changed(CONTROL_MODE_POSITION_CONTROL, 1)
			elif button_name == "Torque (Nm)":
				self.axis_control_mode_changed(CONTROL_MODE_TORQUE_CONTROL, 1)
			elif button_name == "Velocity (Turns/s)":
				self.axis_control_mode_changed(CONTROL_MODE_VELOCITY_CONTROL, 1)


	def axis_control_mode_changed(self, control_mode, axis):
		# print("changin stuff")
		
		if control_mode == CONTROL_MODE_POSITION_CONTROL:
			self.axis_controller_fields_position_enabled(CONTROL_MODE_POSITION_CONTROL, axis)
		elif control_mode == CONTROL_MODE_TORQUE_CONTROL:
			self.axis_controller_fields_position_enabled(CONTROL_MODE_TORQUE_CONTROL, axis)
		elif control_mode == CONTROL_MODE_VELOCITY_CONTROL:
			self.axis_controller_fields_position_enabled(CONTROL_MODE_VELOCITY_CONTROL, axis)
		# Updated mode inside odrive board
		if axis == 0:
			self.my_drive.axis0.controller.config.control_mode = control_mode
		elif axis == 1:
			self.my_drive.axis1.controller.config.control_mode = control_mode

	def axis_controller_fields_position_enabled(self, control_mode, axis_num):
		if axis_num == 0:
			axis = "axis0"
		else:
			axis = "axis1"

		self.ct[axis]["torque_sb"].setDisabled(True)
		self.ct[axis]["torque_cw_pb"].setDisabled(True)
		self.ct[axis]["torque_ccw_pb"].setDisabled(True)
		self.ct[axis]["torque_stop_pb"].setDisabled(True)
		self.ct[axis]["velocity_sb"].setDisabled(True)
		self.ct[axis]["velocity_cw_pb"].setDisabled(True)
		self.ct[axis]["velocity_ccw_pb"].setDisabled(True)
		self.ct[axis]["velocity_stop_pb"].setDisabled(True)
		self.ct[axis]["position_sb"].setDisabled(True)
		self.ct[axis]["position_go_pb"].setDisabled(True)

		if control_mode == CONTROL_MODE_POSITION_CONTROL:
			self.ct[axis]["position_sb"].setDisabled(False)
			self.ct[axis]["position_go_pb"].setDisabled(False)
		elif control_mode == CONTROL_MODE_VELOCITY_CONTROL:
			self.ct[axis]["velocity_sb"].setDisabled(False)
			self.ct[axis]["velocity_cw_pb"].setDisabled(False)
			self.ct[axis]["velocity_ccw_pb"].setDisabled(False)
			self.ct[axis]["velocity_stop_pb"].setDisabled(False)
		elif control_mode == CONTROL_MODE_TORQUE_CONTROL:
			self.ct[axis]["torque_sb"].setDisabled(False)
			self.ct[axis]["torque_cw_pb"].setDisabled(False)
			self.ct[axis]["torque_ccw_pb"].setDisabled(False)
			self.ct[axis]["torque_stop_pb"].setDisabled(False)


	def torque_button_pressed(self):
		button_name = self.sender().objectName()
		axis = button_name[-5:]
		value = self.ct[axis]["torque_sb"].value()
		if button_name[:-5] == "torque_ccw_pb":
			value = value * -1
		elif button_name[:-5] == "torque_stop_pb":
			value = 0
		# print("Button {}, Axis {}".format(button_name, axis))
		exec_string = "self.my_drive.{}.controller.input_torque = {}".format(axis, value)
		# print(exec_string)
		exec(exec_string)

	def velocity_button_pressed(self):
		button_name = self.sender().objectName()
		axis = button_name[-5:]
		value = self.ct[axis]["velocity_sb"].value()
		if button_name[:-5] == "velocity_ccw_pb":
			value = value * -1
		elif button_name[:-5] == "velocity_stop_pb":
			value = 0
		# print("Button {}, Axis {}".format(button_name, axis))
		exec_string = "self.my_drive.{}.controller.input_vel = {}".format(axis, value)
		# print(exec_string)
		exec(exec_string)
		

	def position_button_pressed(self):
		button_name = self.sender().objectName()
		axis = button_name[-5:]
		# print("Button {}, Axis {}".format(button_name, axis))
		exec_string = "self.my_drive.{}.controller.input_pos = {}".format(axis, self.ct[axis]["position_sb"].value())
		exec(exec_string)
		# print(exec_string)

	def update_controller_mode(self):
		# print("Controller mode {}".format(self.my_drive.axis0.controller.config.control_mode))
		
		axis0_control_mode = self.my_drive.axis0.controller.config.control_mode
		if axis0_control_mode == CONTROL_MODE_POSITION_CONTROL:
			# self.axis0Position_radioButton.setChecked(True)
			self.ct["axis0"]["position_label"].setChecked(True)
			self.axis_controller_fields_position_enabled(CONTROL_MODE_POSITION_CONTROL, 0)
		elif axis0_control_mode == CONTROL_MODE_VELOCITY_CONTROL:
			self.ct["axis0"]["velocity_label"].setChecked(True)
			# self.axis0Current_radioButton.setChecked(True)
			self.axis_controller_fields_position_enabled(CONTROL_MODE_VELOCITY_CONTROL, 0)
		elif axis0_control_mode == CONTROL_MODE_TORQUE_CONTROL:
			# self.axis0Velocity_radioButton.setChecked(True)
			self.ct["axis0"]["torque_label"].setChecked(True)
			self.axis_controller_fields_position_enabled(CONTROL_MODE_TORQUE_CONTROL, 0)

		axis1_control_mode = self.my_drive.axis1.controller.config.control_mode
		if axis1_control_mode == CONTROL_MODE_POSITION_CONTROL:
			# self.axis1Position_radioButton.setChecked(True)
			self.ct["axis1"]["position_label"].setChecked(True)
			self.axis_controller_fields_position_enabled(CONTROL_MODE_POSITION_CONTROL, 1)
		elif axis1_control_mode == CONTROL_MODE_VELOCITY_CONTROL:
			self.ct["axis1"]["velocity_label"].setChecked(True)
			# self.axis1Current_radioButton.setChecked(True)
			self.axis_controller_fields_position_enabled(CONTROL_MODE_VELOCITY_CONTROL, 1)
		elif axis1_control_mode == CONTROL_MODE_TORQUE_CONTROL:
			# self.axis1Velocity_radioButton.setChecked(True)
			self.ct["axis1"]["torque_label"].setChecked(True)
			self.axis_controller_fields_position_enabled(CONTROL_MODE_TORQUE_CONTROL, 1)

	def error_checks(self):
		# axis0_error = hex(self.my_drive.axis0.error)[2:]
		# axis1_error = hex(self.my_drive.axis1.error)[2:]
		axis0_message = "A0: "
		axis1_message = "A1: "
		axis0_error = self.check_axis_errors(hex(self.my_drive.axis0.error)[2:])
		axis1_error = self.check_axis_errors(hex(self.my_drive.axis1.error)[2:])
		axis0_encoder_error = self.check_axis_encoder_errors(hex(self.my_drive.axis0.encoder.error)[2:])
		axis1_encoder_error = self.check_axis_encoder_errors(hex(self.my_drive.axis1.encoder.error)[2:])
		axis0_motor_error = self.check_axis_motor_errors(hex(self.my_drive.axis0.motor.error)[2:])
		axis1_motor_error = self.check_axis_motor_errors(hex(self.my_drive.axis1.motor.error)[2:])

		axis0_error += ", E: "
		axis1_error += ", E: "

		axis0_error += axis0_encoder_error
		axis1_error += axis1_encoder_error

		axis0_error += ", M: "
		axis1_error += ", M: "

		axis0_error += axis0_motor_error
		axis1_error += axis1_motor_error

		axis0_message += axis0_error
		axis1_message += axis1_error

		self.control_statusBar.setText(axis0_message + "    " + axis1_message)

	def check_axis_motor_errors(self, motor_error):
		error_string = ""
		if len(motor_error) == 1:
			first_bit = motor_error
			error_string = self.check_motor_error_b1(first_bit)
		elif len(motor_error) == 2:
			first_bit = motor_error[1]
			second_bit = motor_error[0]
			error_string = self.check_motor_error_b1(first_bit)
			error_string += " - "
			error_string += self.check_motor_error_b2(second_bit)
		elif len(motor_error) == 3:
			first_bit = motor_error[2]
			second_bit = motor_error[1]
			third_bit = motor_error[0]
			error_string = self.check_motor_error_b1(first_bit)
			error_string += " - "
			error_string += self.check_motor_error_b2(second_bit)
			error_string += " - "
			error_string += self.check_motor_error_b3(third_bit)
		return error_string

	def check_motor_error_b1(self, bit):
		error_string = "NULL"
		if bit == "0": #ERROR_NONE = 0x00,
			error_string = "No errors"
		elif bit == "1": #ERROR_PHASE_RESISTANCE_OUT_OF_RANGE = 0x0001,
			error_string = "ERROR_PHASE_RESISTANCE_OUT_OF_RANGE"
		elif bit == "2": #ERROR_PHASE_INDUCTANCE_OUT_OF_RANGE = 0x0002,
			error_string = "ERROR_PHASE_INDUCTANCE_OUT_OF_RANGE"
		elif bit == "4": #ERROR_ADC_FAILED = 0x0004,
			error_string = "ERROR_ADC_FAILED"
		elif bit == "8": #ERROR_DRV_FAULT = 0x0008,
			error_string = "ERROR_DRV_FAULT"
		return error_string

	def check_motor_error_b2(self, bit):
		error_string = " "
		if bit == "1": #ERROR_CONTROL_DEADLINE_MISSED = 0x0010,
			error_string = "ERROR_CONTROL_DEADLINE_MISSED"
		elif bit == "2": #ERROR_NOT_IMPLEMENTED_MOTOR_TYPE = 0x0020,
			error_string = "ERROR_NOT_IMPLEMENTED_MOTOR_TYPE"
		elif bit == "4": #ERROR_BRAKE_CURRENT_OUT_OF_RANGE = 0x0040,
			error_string = "ERROR_BRAKE_CURRENT_OUT_OF_RANGE"
		elif bit == "8": #ERROR_MODULATION_MAGNITUDE = 0x0080,
			error_string = "ERROR_MODULATION_MAGNITUDE"
		return error_string

	def check_motor_error_b3(self, bit):
		error_string = " "
		if bit == "1": #ERROR_BRAKE_DEADTIME_VIOLATION = 0x0100,
			error_string = "ERROR_BRAKE_DEADTIME_VIOLATION"
		elif bit == "2": #ERROR_UNEXPECTED_TIMER_CALLBACK = 0x0200,
			error_string = "ERROR_UNEXPECTED_TIMER_CALLBACK"
		elif bit == "4": #ERROR_CURRENT_SENSE_SATURATION = 0x0400
			error_string = "ERROR_CURRENT_SENSE_SATURATION"
		return error_string

	def check_axis_encoder_errors(self, encoder_error):
		error_string = ""
		if len(encoder_error) == 1:
			first_bit = encoder_error
			error_string = self.check_encoder_error_b1(first_bit)
		elif len(encoder_error) == 2:
			first_bit = encoder_error[1]
			second_bit = encoder_error[0]
			error_string = self.check_encoder_error_b1(first_bit)
			error_string += " - "
			error_string += self.check_encoder_error_b2(second_bit)
		return error_string

	def check_encoder_error_b1(self, bit):
		error_string = "NULL"
		if bit == "0": #ERROR_NONE = 0x00,
			error_string = "No errors"
		elif bit == "1": #ERROR_UNSTABLE_GAIN = 0x01,
			error_string = "ERROR_UNSTABLE_GAIN"
		elif bit == "2": #ERROR_CPR_OUT_OF_RANGE = 0x02,
			error_string = "ERROR_CPR_OUT_OF_RANGE"
		elif bit == "4": #ERROR_NO_RESPONSE = 0x04,
			error_string = "ERROR_NO_RESPONSE"
		elif bit == "8": #ERROR_UNSUPPORTED_ENCODER_MODE = 0x08,
			error_string = "ERROR_UNSUPPORTED_ENCODER_MODE"
		return error_string

	def check_encoder_error_b2(self, bit):
		error_string = " "
		if bit == "1": #ERROR_ILLEGAL_HALL_STATE = 0x10,
			error_string = "ERROR_ILLEGAL_HALL_STATE"
		elif bit == "2": #ERROR_INDEX_NOT_FOUND_YET = 0x20,
			error_string = "ERROR_INDEX_NOT_FOUND_YET"
		return error_string


	def check_axis_errors(self, axis_error):
		error_string = ""
		if len(axis_error) == 1:
			first_bit = axis_error
			error_string = self.check_axis_error_b1(first_bit)
		elif len(axis_error) == 2:
			first_bit = axis_error[1]
			second_bit = axis_error[0]
			error_string = self.check_axis_error_b1(first_bit)
			error_string += " - "
			error_string += self.check_axis_error_b2(second_bit)
		elif len(axis_error) == 3:
			first_bit = axis_error[2]
			second_bit = axis_error[1]
			third_bit = axis_error[0]
			error_string = self.check_axis_error_b1(first_bit)
			error_string += " - "
			error_string += self.check_axis_error_b2(second_bit)
			error_string += " - "
			error_string += self.check_axis_error_b3(third_bit)
		return error_string


	def check_axis_error_b1(self, bit):
		error_string = "NULL"
		if bit == "0": #ERROR_NONE = 0x00,
			error_string = "No errors"
		elif bit == "1": #ERROR_INVALID_STATE = 0x01, //<! an invalid state was requested
			error_string = "ERROR_INVALID_STATE"
		elif bit == "2": #ERROR_DC_BUS_UNDER_VOLTAGE = 0x02,
			error_string = "ERROR_DC_BUS_UNDER_VOLTAGE"
		elif bit == "4": #ERROR_DC_BUS_OVER_VOLTAGE = 0x04,
			error_string = "ERROR_DC_BUS_OVER_VOLTAGE"
		elif bit == "8": #ERROR_CURRENT_MEASUREMENT_TIMEOUT = 0x08,
			error_string = "ERROR_CURRENT_MEASUREMENT_TIMEOUT"
		return error_string

	def check_axis_error_b2(self, bit):
		error_string = " "
		if bit == "1": #ERROR_BRAKE_RESISTOR_DISARMED = 0x10, //<! the brake resistor was unexpectedly disarmed
			error_string = "ERROR_BRAKE_RESISTOR_DISARMED"
		elif bit == "2": #ERROR_MOTOR_DISARMED = 0x20, //<! the motor was unexpectedly disarmed
			error_string = "ERROR_MOTOR_DISARMED"
		elif bit == "4": #ERROR_MOTOR_FAILED = 0x40, // Go to motor.hpp for information, check odrvX.axisX.motor.error for error value
			error_string = "ERROR_MOTOR_FAILED"
		elif bit == "8": #ERROR_SENSORLESS_ESTIMATOR_FAILED = 0x80,
			error_string = "ERROR_SENSORLESS_ESTIMATOR_FAILED"
		return error_string

	def check_axis_error_b3(self, bit):
		error_string = " "
		if bit == "1": #ERROR_ENCODER_FAILED = 0x100, // Go to encoder.hpp for information, check odrvX.axisX.encoder.error for error value
			error_string = "ERROR_ENCODER_FAILED"
		elif bit == "2": #ERROR_CONTROLLER_FAILED = 0x200,
			error_string = "ERROR_CONTROLLER_FAILED"
		elif bit == "4": #ERROR_POS_CTRL_DURING_SENSORLESS = 0x400,
			error_string = "ERROR_POS_CTRL_DURING_SENSORLESS"
		return error_string

	def update_statuses(self):
		# pass
		# self.update_voltage()
		try:
			self.update_machine_state()
			self.update_controller_mode()
			self.error_checks()
		except Exception as e:
			print(e)
			# self.odrive_disconnected_exception()

	def machine_state_clicked(self):
		button_name = self.sender().objectName()
		axis_name = button_name[-5:]
		m_state_name = button_name[:-6]
		# print(axis_name)
		# print(m_state_name)

		if axis_name == "axis0":
			axis = self.my_drive.axis0
		elif axis_name == "axis1":
			axis = self.my_drive.axis1

		if m_state_name == "state_idle_pb":
			axis.requested_state = AXIS_STATE_IDLE
		elif m_state_name == "state_start_up_sequece_pb":
			axis.requested_state = AXIS_STATE_STARTUP_SEQUENCE
		elif m_state_name == "state_full_calibration_sequence_pb":
			axis.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
		elif m_state_name == "state_motor_calibration_pb":
			axis.requested_state = AXIS_STATE_MOTOR_CALIBRATION
		elif m_state_name == "state_sensorless_control_pb":
			axis.requested_state = AXIS_STATE_SENSORLESS_CONTROL
		elif m_state_name == "state_encoder_index_search_pb":
			axis.requested_state = AXIS_STATE_ENCODER_INDEX_SEARCH
		elif m_state_name == "state_encoder_offset_calibration_pb":
			axis.requested_state = AXIS_STATE_ENCODER_OFFSET_CALIBRATION
		elif m_state_name == "state_closed_loop_control_pb":
			axis.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

	def update_machine_state(self):
		current_state = self.my_drive.axis0.current_state
		if self.axis0_state != current_state:
			self.axis0_state = current_state
			# print("New state axis0: {}".format(self.axis0_state))
			self.update_machine_state_color(current_state, 0)

		current_state = self.my_drive.axis1.current_state
		if self.axis1_state != current_state:
			self.axis1_state = current_state
			# print("New state axis1: {}".format(self.axis1_state))
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