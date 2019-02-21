#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import UI_mainwindow

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

class ExampleApp(QtWidgets.QMainWindow, UI_mainwindow.Ui_MainWindow):

	app_name = "Odrive Tester"
	def __init__(self):
		# Simple reason why we use it here is that it allows us to
		# access variables, methods etc in the design.py file
		super(self.__class__, self).__init__()
		self.setupUi(self)  # This is defined in design.py file automatically
							# It sets up layout and widgets that are defined
		self.quit_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+Q"), self)
		self.quit_shortcut.activated.connect(self.close_application)

		self.Scan_config_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+F"), self)
		self.Scan_config_shortcut.activated.connect(self.scan_all_config)

		self.odrive_connect_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+C"), self)
		self.odrive_connect_shortcut.activated.connect(self.odrive_connect)

		self.actionScan_config.triggered.connect(self.scan_all_config)

		self.pushButton_saveConfiguration.clicked.connect(self.save_odrive_configuration)
		self.pushButton_eraseConfiguration.clicked.connect(self.erase_odrive_configuration)
		self.pushButton_scanConfiguration.clicked.connect(self.scan_all_config)
		self.pushButton_writeConfiguration.clicked.connect(self.write_config)
		self.pushButton_connect.clicked.connect(self.odrive_connect)
		# self.pushButton_save_config.clicked.connect(self.save_config)
		self.pushButton_reboot.clicked.connect(self.odrive_reboot)

		self.axis0_pushButton_idle.clicked.connect(self.idle_state_clicked)
		self.axis0_pushButton_startupSequence.clicked.connect(self.startupSequence_state_clicked)
		self.axis0_pushButton_fullCalibrationSequence.clicked.connect(self.fullCalibrationSequence_state_clicked)
		self.axis0_pushButton_motorCalibration.clicked.connect(self.motorCalibration_state_clicked)
		self.axis0_pushButton_sensorlessControl.clicked.connect(self.sensorlessControl_state_clicked)
		self.axis0_pushButton_econderIndexSearch.clicked.connect(self.econderIndexSearch_state_clicked)
		self.axis0_pushButton_encoderOffsetCalibration.clicked.connect(self.encoderOffsetCalibration_state_clicked)
		self.axis0_pushButton_closedLoopControl.clicked.connect(self.closedLoopControl_state_clicked)

		# Axis Controlls
		self.buttonGroup_13.buttonClicked.connect(self.axis0_controller_mode_changed)

		self.axis0PositionGo_pushButton.clicked.connect(self.send_axis0_position_go)
		self.axis0Backward_pushButton.clicked.connect(self.send_axis0_velocity_current_backward)
		self.axis0Stop_pushButton.clicked.connect(self.send_axis0_velocity_current_stop)
		self.axis0Forward_pushButton.clicked.connect(self.send_axis0_velocity_current_forward)

		# self.buttonGroup_14.buttonClicked.connect(self.axis1_controller_mode_changed)
		# self.axis1PositionGo_pushButton.clicked.connect(self.send_axis1_position_go)
		# self.axis1Backward_pushButton.clicked.connect(self.send_axis1_velocity_current_backward)
		# self.axis1Stop_pushButton.clicked.connect(self.send_axis1_velocity_current_stop)
		# self.axis1Forward_pushButton.clicked.connect(self.send_axis1_velocity_current_forward)
		# self.axis0_pushButton_sendController.clicked.connect(self.send_axis_control)


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

		pen_sp_axis0 = pg.mkPen(color=(0, 128, 255), width=2)
		pen_est_axis0 = pg.mkPen(color=(255, 192, 0), width=2)

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

		self.axis0_state = None
		self.setDisabled_odrive_ui(True)
		self.odrive_connect()
		self.error_checks()

	def error_checks(self):
		axis0_error = hex(self.my_drive.axis0.error)
		self.check_axis_errors(axis_error0)
		axis1_error = hex(self.my_drive.axis1.error)
		self.check_axis_errors(axis_error1)

	def check_axis_errors(self, axis_error):
		error_string = ""

		if axis_error == "0x00": #ERROR_NONE = 0x00,
			# error_string = "No errors"
			return None
		elif axis_error == "0x01": #ERROR_INVALID_STATE = 0x01, //<! an invalid state was requested
			error_string = "ERROR_INVALID_STATE"
		elif axis_error == "0x02": #ERROR_DC_BUS_UNDER_VOLTAGE = 0x02,
			error_string = "ERROR_DC_BUS_UNDER_VOLTAGE"
		elif axis_error == "0x04": #ERROR_DC_BUS_OVER_VOLTAGE = 0x04,
			error_string = "ERROR_DC_BUS_OVER_VOLTAGE"
		elif axis_error == "0x08": #ERROR_CURRENT_MEASUREMENT_TIMEOUT = 0x08,
			error_string = "ERROR_CURRENT_MEASUREMENT_TIMEOUT"
		elif axis_error == "0x10": #ERROR_BRAKE_RESISTOR_DISARMED = 0x10, //<! the brake resistor was unexpectedly disarmed
			error_string = "ERROR_BRAKE_RESISTOR_DISARMED"
		elif axis_error == "0x20": #ERROR_MOTOR_DISARMED = 0x20, //<! the motor was unexpectedly disarmed
			error_string = "ERROR_MOTOR_DISARMED"
		elif axis_error == "0x40": #ERROR_MOTOR_FAILED = 0x40, // Go to motor.hpp for information, check odrvX.axisX.motor.error for error value
			error_string = "ERROR_MOTOR_FAILED"
		elif axis_error == "0x80": #ERROR_SENSORLESS_ESTIMATOR_FAILED = 0x80,
			error_string = "RROR_SENSORLESS_ESTIMATOR_FAILED"
		elif axis_error == "0x100": #ERROR_ENCODER_FAILED = 0x100, // Go to encoder.hpp for information, check odrvX.axisX.encoder.error for error value
			error_string = "ERROR_ENCODER_FAILED"
		elif axis_error == "0x200": #ERROR_CONTROLLER_FAILED = 0x200,
			error_string = "ERROR_CONTROLLER_FAILED"
		elif axis_error == "0x400": #ERROR_POS_CTRL_DURING_SENSORLESS = 0x400,
			error_string = "ERROR_POS_CTRL_DURING_SENSORLESS"

		return error_string

	def check_motor_errors(self, axis_error):
		pass
		# Axis errors
#         ERROR_NONE = 0x00,
#         ERROR_INVALID_STATE = 0x01, //<! an invalid state was requested
#         ERROR_DC_BUS_UNDER_VOLTAGE = 0x02,
#         ERROR_DC_BUS_OVER_VOLTAGE = 0x04,
#         ERROR_CURRENT_MEASUREMENT_TIMEOUT = 0x08,
#         ERROR_BRAKE_RESISTOR_DISARMED = 0x10, //<! the brake resistor was unexpectedly disarmed
#         ERROR_MOTOR_DISARMED = 0x20, //<! the motor was unexpectedly disarmed
#         ERROR_MOTOR_FAILED = 0x40, // Go to motor.hpp for information, check odrvX.axisX.motor.error for error value
#         ERROR_SENSORLESS_ESTIMATOR_FAILED = 0x80,
#         ERROR_ENCODER_FAILED = 0x100, // Go to encoder.hpp for information, check odrvX.axisX.encoder.error for error value
#         ERROR_CONTROLLER_FAILED = 0x200,
#         ERROR_POS_CTRL_DURING_SENSORLESS = 0x400,
		#Motor Errors
#         ERROR_NONE = 0,
#         ERROR_PHASE_RESISTANCE_OUT_OF_RANGE = 0x0001,
#         ERROR_PHASE_INDUCTANCE_OUT_OF_RANGE = 0x0002,
#         ERROR_ADC_FAILED = 0x0004,
#         ERROR_DRV_FAULT = 0x0008,
#         ERROR_CONTROL_DEADLINE_MISSED = 0x0010,
#         ERROR_NOT_IMPLEMENTED_MOTOR_TYPE = 0x0020,
#         ERROR_BRAKE_CURRENT_OUT_OF_RANGE = 0x0040,
#         ERROR_MODULATION_MAGNITUDE = 0x0080,
#         ERROR_BRAKE_DEADTIME_VIOLATION = 0x0100,
#         ERROR_UNEXPECTED_TIMER_CALLBACK = 0x0200,
#         ERROR_CURRENT_SENSE_SATURATION = 0x0400
		#Encoder error
# 		        ERROR_NONE = 0,
#         ERROR_UNSTABLE_GAIN = 0x01,
#         ERROR_CPR_OUT_OF_RANGE = 0x02,
#         ERROR_NO_RESPONSE = 0x04,
#         ERROR_UNSUPPORTED_ENCODER_MODE = 0x08,
#         ERROR_ILLEGAL_HALL_STATE = 0x10,
# ERROR_INDEX_NOT_FOUND_YET = 0x20,
		#Controller error
# ERROR_NONE = 0,
# ERROR_OVERSPEED = 0x01,
		#sensorless error
        # ERROR_NONE = 0,
		# ERROR_OVERSPEED = 0x01,
	# self.my_drive.can.unexpected_errors
	# self.my_drive.system_stats.i2c.error_cnt
	# self.my_drive.axis0.error
	# self.my_drive.axis0.encoder.error
	# self.my_drive.axis0.motor.error
	# controller and sensorless
		error_message_text = "more args"
		message_box_error = QtWidgets.QMessageBox.warning(self, "Error occured", error_message_text,  QtWidgets.QMessageBox.Help | QtWidgets.QMessageBox.Ignore)
		if message_box_error == QtWidgets.QMessageBox.Help:
			QtGui.QDesktopServices.openUrl(QtCore.QUrl("https://docs.odriverobotics.com/troubleshooting"))


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

	def update_controller_mode(self):
		# print("Controller mode {}".format(self.my_drive.axis0.controller.config.control_mode))
		axis0_control_mode = self.my_drive.axis0.controller.config.control_mode
		axis1_control_mode = self.my_drive.axis1.controller.config.control_mode

		if axis0_control_mode == CTRL_MODE_POSITION_CONTROL:
			self.axis0Position_radioButton.setChecked(True)
			self.axis0_controller_fields_position_enabled(True)
		elif axis0_control_mode == CTRL_MODE_CURRENT_CONTROL:
			self.axis0Current_radioButton.setChecked(True)
			self.axis0_controller_fields_position_enabled(False)
		elif axis0_control_mode == CTRL_MODE_VELOCITY_CONTROL:
			self.axis0Velocity_radioButton.setChecked(True)
			self.axis0_controller_fields_position_enabled(False)

	def axis0_controller_mode_changed(self, id):
		button_name = id.text()
		group_name = id.sender().objectName()
		# print()
		if button_name == "Position":
			self.axis_control_mode_changed(CTRL_MODE_POSITION_CONTROL)
		elif button_name == "Current":
			self.axis_control_mode_changed(CTRL_MODE_CURRENT_CONTROL)
		elif button_name == "Velocity":
			self.axis_control_mode_changed(CTRL_MODE_VELOCITY_CONTROL)

	def axis_control_mode_changed(self, control_mode):
		if control_mode == CTRL_MODE_POSITION_CONTROL:
			self.axis0_controller_fields_position_enabled(True)
		elif control_mode == CTRL_MODE_CURRENT_CONTROL:
			self.axis0_controller_fields_position_enabled(False)
		elif control_mode == CTRL_MODE_VELOCITY_CONTROL:
			self.axis0_controller_fields_position_enabled(False)
		# Updated mode inside odrive board
		self.my_drive.axis0.controller.config.control_mode = control_mode
		self.spinBox_controlModeValue.setValue(control_mode)

	def axis0_controller_fields_position_enabled(self, state):
		#Enabled Position objects
		self.axis0Position_doubleSpinBox.setEnabled(state)
		self.axis0PositionGo_pushButton.setEnabled(state)
		#Disable current and velocity objects
		self.axis0Backward_pushButton.setDisabled(state)
		self.axis0Stop_pushButton.setDisabled(state)
		self.axis0Forward_pushButton.setDisabled(state)
		self.axis0Velocity_doubleSpinBox.setDisabled(state)
		self.axis0Current_doubleSpinBox.setDisabled(state)

	def close_application(self):
		print("whooaaaa so custom!!!")
		# try:
		# 	self.odrive_worker.stop()
		# except:
		# 	pass
		sys.exit()

	def odrive_connect(self):
		self.odrive_worker = odriveWorker()
		self.odrive_worker.odrive_found_sig.connect(self.odrive_connected)
		self.odrive_worker.start()
		self.pushButton_connect.setDisabled(True)
		self.pushButton_connect.setText("Connecting . . .")

	def odrive_connected(self, my_drive):
		self.my_drive = my_drive
		self.pushButton_connect.setText("Connected")
		# self.statusBar.showMessage("Serial number: {}".format(self.my_drive.serial_number))
		#if my drive is found
		self.timer = pg.QtCore.QTimer()
		self.timer.timeout.connect(self.update)
		self.timer.start(500)

		self.ad["start_time"] = pg.ptime.time()
		self.timer_graphUpdate = pg.QtCore.QTimer()
		self.timer_graphUpdate.timeout.connect(self.update_graphs)
		self.timer_graphUpdate.start(20)

		self.setDisabled_odrive_ui(False)

		self.update_controller_mode()
		self.scan_all_config()

	def setDisabled_odrive_ui(self, state):
		self.tabWidget.setDisabled(state)
		self.controlTab.setDisabled(state)
		self.groupBox_13.setDisabled(state)

		self.pushButton_reboot.setDisabled(state)
		self.pushButton_scanConfiguration.setDisabled(state)
		self.pushButton_writeConfiguration.setDisabled(state)
		self.pushButton_saveConfiguration.setDisabled(state)
		self.pushButton_eraseConfiguration.setDisabled(state)
		self.pushButton_getTemp.setDisabled(state)

	def update_graphs(self):
		delta = pg.ptime.time() - self.ad["start_time"]
		try:
			if self.showAxis0_checkBox.isChecked():
				self.ad["axis0"]["time_array"].append(delta)
				self.update_velocity_graph("axis0", self.my_drive.axis0)
				self.update_position_graph("axis0", self.my_drive.axis0)
				self.update_current_graph("axis0", self.my_drive.axis0)
			if self.showAxis1_checkBox.isChecked():
				print("Update Axis1")
			self.update_X_range()
		except Exception as e:
			print(e)
			self.odrive_disconnected_exception()

	def odrive_disconnected_exception(self):
		self.timer.stop()
		self.timer_graphUpdate.stop()
		self.odrive_worker.stop()
		self.pushButton_connect.setDisabled(False)
		self.pushButton_connect.setText("Connect")
		self.setDisabled_odrive_ui(True)

		self.clear_axis_graph_lists("axis0")
		# self.clear_axis_graph_lists("axis1")

	def clearGraph_clicked(self):
		self.clear_axis_graph_lists("axis0")
		# self.clear_axis_graph_lists("axis1")
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

	def update_X_range(self):
		upper_limit = self.ad["axis0"]["time_array"][-1]
		lower_limit = self.ad["axis0"]["time_array"][0]
		delta = self.spinBox_graphTime.value()
		if (upper_limit - lower_limit) > delta:
			while((upper_limit - lower_limit) > delta):
				self.ad["axis0"]["time_array"].pop(0)
				self.ad["axis0"]["velocity"]["estimate"].pop(0)
				self.ad["axis0"]["velocity"]["set_point"].pop(0)
				self.ad["axis0"]["current"]["estimate"].pop(0)
				self.ad["axis0"]["current"]["set_point"].pop(0)
				self.ad["axis0"]["position"]["estimate"].pop(0)
				self.ad["axis0"]["position"]["set_point"].pop(0)
				upper_limit = self.ad["axis0"]["time_array"][-1]
				lower_limit = self.ad["axis0"]["time_array"][0]

		# if upper_limit >= delta:
		# 	lower_l = upper_limit - delta
		# 	self.plotWidget_velocity.setXRange(lower_l, upper_limit)
		# 	self.plotWidget_position.setXRange(lower_l, upper_limit)
		# 	self.plotWidget_current.setXRange(lower_l, upper_limit)


	def update(self):
		# self.update_voltage()
		try:
			self.update_machine_state()
			self.update_controller_mode()
		except Exception as e:
			print(e)
			self.odrive_disconnected_exception()


	def update_voltage(self):
		self.label_vbusVoltageValue.setText(str(round(self.my_drive.vbus_voltage, 2)))

	def update_machine_state(self):
		#print(self.my_drive.axis0.current_state)
		current_state = self.my_drive.axis0.current_state
		if self.axis0_state != current_state:
			self.axis0_state = current_state
			print("New state axis0: {}".format(self.axis0_state))

			self.clear_state_buttons()

			if current_state == AXIS_STATE_IDLE:
				self.idle_state()
			elif current_state == AXIS_STATE_STARTUP_SEQUENCE:
				self.startup_seq_state()
			elif current_state == AXIS_STATE_FULL_CALIBRATION_SEQUENCE:
				self.full_calibration_seq_state()
			elif current_state == AXIS_STATE_MOTOR_CALIBRATION:
				self.motor_calibration_state()
			elif current_state == AXIS_STATE_SENSORLESS_CONTROL:
				self.sensorless_control_state()
			elif current_state == AXIS_STATE_ENCODER_INDEX_SEARCH:
				self.encoder_index_search_state()
			elif current_state == AXIS_STATE_ENCODER_OFFSET_CALIBRATION:
				self.encoder_offset_calibration_state()
			elif current_state == AXIS_STATE_CLOSED_LOOP_CONTROL:
				self.closed_loop_control_state()

	def save_odrive_configuration(self):
		self.my_drive.save_configuration()

	def erase_odrive_configuration(self):
		self.my_drive.erase_configuration()

	def write_config(self):
		self.my_drive.axis0.motor.config.phase_inductance = float(self.doubleSpinBox_phaseInductanceValue.value())
		self.my_drive.axis0.motor.config.phase_resistance = float(self.doubleSpinBox_phaseResistanceValue.value())
		self.my_drive.axis0.motor.config.pole_pairs = int(self.spinBox_poleParisValue.value())
		self.my_drive.axis0.motor.config.motor_type = int(self.spinBox_motorTypeValue.value())
		self.my_drive.axis0.motor.config.direction = int(self.spinBox_directionValue.value())
		self.my_drive.axis0.motor.config.calibration_current = float(self.doubleSpinBox_calibrationCurrentValue.value())
		self.my_drive.axis0.motor.config.current_lim = float(self.doubleSpinBox_currentLimValue.value())
		self.my_drive.axis0.motor.config.pre_calibrated = self.radioButton_preCalibratedTrue.isChecked()
		self.my_drive.axis0.motor.config.requested_current_range = float(self.doubleSpinBox_requestedCurrentRangeValue.value())
		# self.my_drive.axis0.motor.config.current_control_bandwidth = float(self.doubleSpinBox_currentControlBandwidthValue.value())
		self.my_drive.axis0.motor.config.resistance_calib_max_voltage = float(self.doubleSpinBox_resistanceCalibMaxVoltageValue.value())

		# self.my_drive.axis0.sensorless_estimator.config.pm_flux_linkage = float(self..value())
		# self.my_drive.axis0.sensorless_estimator.config.pll_bandwidth = float(self..value())
		# self.my_drive.axis0.sensorless_estimator.config.observer_gain = float(self..value())

		self.my_drive.axis0.controller.config.vel_gain = float(self.doubleSpinBox_velGainValue.value())
		self.my_drive.axis0.controller.config.vel_integrator_gain = float(self.doubleSpinBox_velIntegratorGainValue.value())
		self.my_drive.axis0.controller.config.pos_gain = float(self.doubleSpinBox_posGainValue.value())
		self.my_drive.axis0.controller.config.vel_limit = float(self.doubleSpinBox_velLimitValue.value())
		self.my_drive.axis0.controller.config.control_mode = int(self.spinBox_controlModeValue.value())

		self.my_drive.axis0.config.startup_encoder_index_search = self.radioButton_startupEncoderIndexSearchTrue.isChecked()
		self.my_drive.axis0.config.startup_motor_calibration = self.radioButton_startupMotorCalibrationAxisTrue.isChecked()
		self.my_drive.axis0.config.startup_sensorless_control = self.radioButton_startupSensorlessControlTrue.isChecked()
		self.my_drive.axis0.config.startup_closed_loop_control = self.radioButton_startupEncoderLoopControlTrue.isChecked()
		self.my_drive.axis0.config.startup_encoder_offset_calibration = self.radioButton_startupEncoderOffsetCalibrationTrue.isChecked()
		self.my_drive.axis0.config.enable_step_dir = self.radioButton_enableStepDirTrue.isChecked()

		self.my_drive.axis0.config.ramp_up_distance = float(self.doubleSpinBox_rampUpDistanceValue.value())
		self.my_drive.axis0.config.spin_up_current = float(self.doubleSpinBox_spinUpCurrentValue.value())
		self.my_drive.axis0.config.spin_up_target_vel = float(self.doubleSpinBox_spinUpTargetVelValue.value())
		self.my_drive.axis0.config.ramp_up_time = float(self.doubleSpinBox_rampUpTimeValue.value())
		self.my_drive.axis0.config.counts_per_step = float(self.doubleSpinBox_countPerStepValue.value())
		self.my_drive.axis0.config.spin_up_acceleration = float(self.doubleSpinBox_spinUpAccelerationValue.value())

		self.my_drive.axis0.encoder.config.calib_range = float(self.doubleSpinBox_calibRangeValue.value())
		self.my_drive.axis0.encoder.config.mode = int(self.spinBox_modeEncoderValue.value())
		self.my_drive.axis0.encoder.config.offset = int(self.spinBox_offsetValue.value())
		self.my_drive.axis0.encoder.config.pre_calibrated = self.radioButton_preCalibratedEncoderTrue.isChecked()
		self.my_drive.axis0.encoder.config.use_index = self.radioButton_useIndexTrue.isChecked()
		self.my_drive.axis0.encoder.config.cpr = int(self.spinBox_cprValue.value())
		self.my_drive.axis0.encoder.config.idx_search_speed = float(self.doubleSpinBox_idxSearchSpeedValue.value())
		self.my_drive.axis0.encoder.config.offset_float = float(self.doubleSpinBox_offsetFloatValue.value())
		self.my_drive.axis0.encoder.config.bandwidth = float(self.doubleSpinBox_bandwidthValue.value())

		self.my_drive.config.dc_bus_overvoltage_trip_level = float(self.doubleSpinBox_dcBusOvervoltageTripLevelValue.value())
		self.my_drive.config.enable_ascii_protocol_on_usb = self.radioButton_enableAsciiProtocolOnUsbTrue.isChecked()
		self.my_drive.config.dc_bus_undervoltage_trip_level = float(self.doubleSpinBox_dcBusUndervoltageTripLevelValue.value())
		self.my_drive.config.enable_uart = self.radioButton_enableUartTrue.isChecked()
		self.my_drive.config.enable_i2c_instead_of_can = self.radioButton_enableI2cInsteadOfCanTrue.isChecked()
		self.my_drive.config.brake_resistance = float(self.doubleSpinBox_brakeResistanceValue.value())

	def scan_all_config(self):
		print("Scanning all config")
		self.scan_system_stats_config()
		self.scan_can_config()
		self.scan_low_level_config()
		self.scan_config_config()
		self.scan_axis_config()

	def scan_config_config(self):
		# enable uart
		# enable i2c instead of can
		self.doubleSpinBox_dcBusOvervoltageTripLevelValue.setValue(self.my_drive.config.dc_bus_overvoltage_trip_level)
		#self.doubleSpinBox_dcBusOvervoltageTripLevelValue_2.setText(str(self.my_drive.config.dc_bus_undervoltage_trip_level))
		#self.doubleSpinBox_brakeResistanceValue.setText(str(self.my_drive.config.brake_resistance))
		if self.my_drive.config.enable_uart:
			self.radioButton_enableUartTrue.setChecked(True)
		else:
			self.radioButton_enableUartFalse.setChecked(True)

		if self.my_drive.config.enable_i2c_instead_of_can:
			self.radioButton_enableI2cInsteadOfCanTrue.setChecked(True)
		else:
			self.radioButton_enableI2cInsteadOfCanFalse.setChecked(True)

		if self.my_drive.config.enable_ascii_protocol_on_usb:
			self.radioButton_enableAsciiProtocolOnUsbTrue.setChecked(True)
		else:
			self.radioButton_enableAsciiProtocolOnUsbFalse.setChecked(True)

		self.doubleSpinBox_dcBusOvervoltageTripLevelValue.setValue(self.my_drive.config.dc_bus_overvoltage_trip_level)
		self.doubleSpinBox_dcBusUndervoltageTripLevelValue.setValue(self.my_drive.config.dc_bus_undervoltage_trip_level)
		self.doubleSpinBox_brakeResistanceValue.setValue(self.my_drive.config.brake_resistance)
		# enable ascii protocol
		self.scan_config_gpio_pwm_config()

	def scan_config_gpio_pwm_config(self):
		self.doubleSpinBox_gpio1MaxValue.setValue(self.my_drive.config.gpio1_pwm_mapping.max)
		self.doubleSpinBox_gpio2MaxValue.setValue(self.my_drive.config.gpio2_pwm_mapping.max)
		self.doubleSpinBox_gpio3MaxValue.setValue(self.my_drive.config.gpio3_pwm_mapping.max)
		self.doubleSpinBox_gpio4MaxValue.setValue(self.my_drive.config.gpio4_pwm_mapping.max)
		self.doubleSpinBox_gpio1MinValue.setValue(self.my_drive.config.gpio1_pwm_mapping.min)
		self.doubleSpinBox_gpio2MinValue.setValue(self.my_drive.config.gpio2_pwm_mapping.min)
		self.doubleSpinBox_gpio3MinValue.setValue(self.my_drive.config.gpio3_pwm_mapping.min)
		self.doubleSpinBox_gpio4MinValue.setValue(self.my_drive.config.gpio4_pwm_mapping.min)




	def scan_low_level_config(self):
		print("Scanning Low level config...")
		self.label_vbusVoltageValue.setText(str(self.my_drive.vbus_voltage))

		if self.my_drive.brake_resistor_armed:
			self.icon_brakeResistorArmedValue.setPixmap(QtGui.QPixmap(ICON_TRUE))
		else:
			self.icon_brakeResistorArmedValue.setPixmap(QtGui.QPixmap(ICON_FALSE))

		self.icon_userConfigLoadedValue.setPixmap(QtGui.QPixmap(ICON_FALSE))

		if self.my_drive.user_config_loaded:
			self.icon_userConfigLoadedValue.setPixmap(QtGui.QPixmap(ICON_TRUE))
		else:
			self.icon_userConfigLoadedValue.setPixmap(QtGui.QPixmap(ICON_FALSE))

		self.label_hwVersionValue.setText("{}.{}".format(self.my_drive.hw_version_major, self.my_drive.hw_version_minor))
		self.label_hwVersionVariantValue.setText(str(self.my_drive.hw_version_variant))
		self.label_fwVersionValue.setText("{}.{}".format(self.my_drive.fw_version_major, self.my_drive.fw_version_minor))
		self.label_fwVersionRevisionValue.setText(str(self.my_drive.fw_version_revision))
		self.label_fwVersionUnreleasedValue.setText(str(self.my_drive.fw_version_unreleased))

		# Set Icon instead
		#self.label_brakeResistorArmedValue.setText(str(self.my_drive.brake_resistor_armed))


		#self.label_hwVersionMinorValue.setText(str(self.my_drive.node_id))
		#self.label_hwVersionVariantValue.setText(str(self.my_drive.node_id))
		#self.label_hwVersionMajorValue.setText(str(self.my_drive.node_id))
		#self.label_getAdcVoltageValue.setText(str(self.my_drive.node_id))
		self.label_testPropertyValue.setText(str(self.my_drive.test_property))
		#self.label_fwVersionRevisionValue.setText(str(self.my_drive.node_id))
		#self.label_fwVersionUnreleasedValue.setText(str(self.my_drive.node_id))
		#self.label_fwVersionMinorValue.setText(str(self.my_drive.node_id))
		#self.label_fwVersionMajorValue.setText(str(self.my_drive.node_id))

		#self.label_userConfigLoadedValue.setText(str(self.my_drive.user_config_loaded))

		#self.label_getOscilloscopeValValue.setText(str(self.my_drive.node_id))
		self.label_serialNumberValue.setText(hex(self.my_drive.serial_number).upper()[2:])



	def scan_can_config(self):
		print("Scanning CAN config...")
		self.label_TxMailboxAbortCallbackCntValue.setText(str(self.my_drive.can.TxMailboxAbortCallbackCnt))
		self.label_nodeIdValue.setText(str(self.my_drive.can.node_id))
		self.label_receivedMsgCntValue.setText(str(self.my_drive.can.received_msg_cnt))
		self.label_TxMailboxCompleteCallbackCntValue.setText(str(self.my_drive.can.TxMailboxCompleteCallbackCnt))
		self.label_unhandledMessagesValue.setText(str(self.my_drive.can.unhandled_messages))
		self.label_receivedAckValue.setText(str(self.my_drive.can.received_ack))
		self.label_unexpectedErrorsValue.setText(str(self.my_drive.can.unexpected_errors))

	def scan_system_stats_config(self):
		self.label_minStackSpaceAxis1Value.setText(str(self.my_drive.system_stats.min_stack_space_axis1))
		self.label_minStackSpaceStartupValue.setText(str(self.my_drive.system_stats.min_stack_space_startup))
		self.label_minStackSpaceUartValue.setText(str(self.my_drive.system_stats.min_stack_space_uart))
		self.label_minStackSpaceUsbIrqValue.setText(str(self.my_drive.system_stats.min_stack_space_usb_irq))
		self.label_minStackSpaceCommsValue.setText(str(self.my_drive.system_stats.min_stack_space_comms))
		self.label_minHeapSpaceValue.setText(str(self.my_drive.system_stats.min_heap_space))
		self.label_minStackSpaceUsbValue.setText(str(self.my_drive.system_stats.min_stack_space_usb))
		self.label_minStackSpaceAxis0Value.setText(str(self.my_drive.system_stats.min_stack_space_axis0))
		self.label_uptimeValue.setText(str(self.my_drive.system_stats.uptime))

		self.label_rxCntUsbValue.setText(str(self.my_drive.system_stats.usb.rx_cnt))
		self.label_txOverrunCntValue.setText(str(self.my_drive.system_stats.usb.tx_overrun_cnt))
		self.label_txCntValue.setText(str(self.my_drive.system_stats.usb.tx_cnt))
		self.label_rxCntI2cValue.setText(str(self.my_drive.system_stats.i2c.rx_cnt))
		self.label_addrValue.setText(str(self.my_drive.system_stats.i2c.addr))
		self.label_addrMatchCnt_2.setText(str(self.my_drive.system_stats.i2c.addr_match_cnt))
		self.label_errorCntValue.setText(str(self.my_drive.system_stats.i2c.error_cnt))

	def load_config_template(self):
		config_template = {}
		with open("config_template.json") as f:
			config_template = json.load(f)
		return config_template


	def scan_axis_config(self):
		self.scan_axis0_config()

	def scan_axis0_config(self):
		self.label_errorAxisValue.setText(str(self.my_drive.axis0.error))
		self.label_loopCounterValue.setText(str(self.my_drive.axis0.loop_counter))
		# Config
		#self.radioButton_startupMotorCalibrationAxisTrue.setChecked(True) if self.my_drive.axis0.config.startup_motor_calibration else self.radioButton_startupMotorCalibrationAxisFalse.setChecked(True)
		if self.my_drive.axis0.config.startup_motor_calibration:
			self.radioButton_startupMotorCalibrationAxisTrue.setChecked(True)
		else:
			self.radioButton_startupMotorCalibrationAxisFalse.setChecked(True)

		if self.my_drive.axis0.config.startup_encoder_index_search:
			self.radioButton_startupEncoderIndexSearchTrue.setChecked(True)
		else:
			self.radioButton_startupEncoderIndexSearchFalse.setChecked(True)

		if self.my_drive.axis0.config.startup_encoder_offset_calibration:
			self.radioButton_startupEncoderOffsetCalibrationTrue.setChecked(True)
		else:
			self.radioButton_startupEncoderOffsetCalibrationFalse.setChecked(True)

		if self.my_drive.axis0.config.startup_closed_loop_control:
			self.radioButton_startupEncoderLoopControlTrue.setChecked(True)
		else:
			self.radioButton_startupEncoderLoopControlFalse.setChecked(True)

		if self.my_drive.axis0.config.startup_sensorless_control:
			self.radioButton_startupSensorlessControlTrue.setChecked(True)
		else:
			self.radioButton_startupSensorlessControlFalse.setChecked(True)

		if self.my_drive.axis0.config.enable_step_dir:
			self.radioButton_enableStepDirTrue.setChecked(True)
		else:
			self.radioButton_enableStepDirFalse.setChecked(True)

		self.doubleSpinBox_countPerStepValue.setValue(self.my_drive.axis0.config.counts_per_step)
		self.doubleSpinBox_rampUpTimeValue.setValue(self.my_drive.axis0.config.ramp_up_time)
		self.doubleSpinBox_rampUpDistanceValue.setValue(self.my_drive.axis0.config.ramp_up_distance)
		self.doubleSpinBox_spinUpCurrentValue.setValue(self.my_drive.axis0.config.spin_up_current)
		self.doubleSpinBox_spinUpAccelerationValue.setValue(self.my_drive.axis0.config.spin_up_acceleration)
		self.doubleSpinBox_spinUpTargetVelValue.setValue(self.my_drive.axis0.config.spin_up_target_vel)

		self.scan_axis0_encoder_config()
		self.scan_axis0_controller_config()
		self.scan_axis0_motor_config()

	def scan_axis0_encoder_config(self):
		if self.my_drive.axis0.encoder.index_found:
			self.icon_indexFoundValue.setPixmap(QtGui.QPixmap(ICON_TRUE))
		else:
			self.icon_indexFoundValue.setPixmap(QtGui.QPixmap(ICON_FALSE))

		if self.my_drive.axis0.encoder.is_ready:
			self.icon_isReadyEncoderValue.setPixmap(QtGui.QPixmap(ICON_TRUE))
		else:
			self.icon_isReadyEncoderValue.setPixmap(QtGui.QPixmap(ICON_FALSE))

		self.label_posCprValue.setText(str(self.my_drive.axis0.encoder.pos_cpr))
		self.label_posEstimateValue.setText(str(self.my_drive.axis0.encoder.pos_estimate))
		self.label_shadowCountValue.setText(str(self.my_drive.axis0.encoder.shadow_count))
		self.label_interpolationValue.setText(str(self.my_drive.axis0.encoder.interpolation))
		self.label_countInCprValue.setText(str(self.my_drive.axis0.encoder.count_in_cpr))
		self.label_hallStateValue.setText(str(self.my_drive.axis0.encoder.hall_state))
		self.label_errorEncoderValue.setText(str(self.my_drive.axis0.encoder.error))
		self.label_phaseValue.setText(str(self.my_drive.axis0.encoder.phase))

		self.scan_axis0_encoder_config_config()

	def scan_axis0_encoder_config_config(self):
		if self.my_drive.axis0.encoder.config.pre_calibrated:
			self.radioButton_preCalibratedEncoderTrue.setChecked(True)
		else:
			self.radioButton_preCalibratedEncoderFalse.setChecked(True)

		if self.my_drive.axis0.encoder.config.use_index:
			self.radioButton_useIndexTrue.setChecked(True)
		else:
			self.radioButton_useIndexFalse.setChecked(True)


		self.doubleSpinBox_idxSearchSpeedValue.setValue(self.my_drive.axis0.encoder.config.idx_search_speed)
		self.spinBox_cprValue.setValue(self.my_drive.axis0.encoder.config.cpr)
		self.spinBox_modeEncoderValue.setValue(self.my_drive.axis0.encoder.config.mode)
		self.spinBox_offsetValue.setValue(self.my_drive.axis0.encoder.config.offset)
		self.doubleSpinBox_offsetFloatValue.setValue(self.my_drive.axis0.encoder.config.offset_float)
		self.doubleSpinBox_calibRangeValue.setValue(self.my_drive.axis0.encoder.config.calib_range)
		self.doubleSpinBox_bandwidthValue.setValue(self.my_drive.axis0.encoder.config.bandwidth)



	def scan_axis0_controller_config(self):
		self.label_velSetpointValue.setText(str(self.my_drive.axis0.controller.vel_setpoint))
		self.label_setPosSetpoint_2.setText(str(self.my_drive.axis0.controller.vel_integrator_current))
		self.label_posSetpointValue.setText(str(self.my_drive.axis0.controller.pos_setpoint))
		self.label_currentSetpointValue.setText(str(self.my_drive.axis0.controller.current_setpoint))
		self.scan_axis0_controller_config_config()

	def scan_axis0_controller_config_config(self):
		self.doubleSpinBox_posGainValue.setValue(self.my_drive.axis0.controller.config.pos_gain)
		self.doubleSpinBox_velGainValue.setValue(self.my_drive.axis0.controller.config.vel_gain)
		self.doubleSpinBox_velIntegratorGainValue.setValue(self.my_drive.axis0.controller.config.vel_integrator_gain)
		self.doubleSpinBox_velLimitValue.setValue(self.my_drive.axis0.controller.config.vel_limit)
		self.spinBox_controlModeValue.setValue(self.my_drive.axis0.controller.config.control_mode)



	def scan_axis0_motor_config(self):
		self.scan_axis0_motor_config_config()
		self.scan_axis0_motor_general_config()
		self.scan_axis0_motor_currentControl_config()

	def scan_axis0_motor_currentControl_config(self):
		self.label_maxAllowedCurrentValue.setText(str(self.my_drive.axis0.motor.current_control.max_allowed_current))
		self.label_ibusValue.setText(str(self.my_drive.axis0.motor.current_control.Ibus))
		self.label_vCurrentControlIntegralDValue.setText(str(self.my_drive.axis0.motor.current_control.v_current_control_integral_d))
		self.label_vCurrentControlIntegralQValue.setText(str(self.my_drive.axis0.motor.current_control.v_current_control_integral_q))
		self.label_finalVAlphaValue.setText(str(self.my_drive.axis0.motor.current_control.final_v_alpha))
		self.label_finalVBetaValue.setText(str(self.my_drive.axis0.motor.current_control.final_v_beta))
		self.label_pGainValue.setText(str(self.my_drive.axis0.motor.current_control.p_gain))
		self.label_iGainValue.setText(str(self.my_drive.axis0.motor.current_control.i_gain))
		self.label_iqSetpointValue.setText(str(self.my_drive.axis0.motor.current_control.Iq_setpoint))
		self.label_iqMeasuredValue.setText(str(self.my_drive.axis0.motor.current_control.Iq_measured))


	def scan_axis0_motor_general_config(self):
		self.label_drvFaultValue.setText(str(self.my_drive.axis0.motor.gate_driver.drv_fault))
		self.label_dcCalibPhBValue.setText(str(self.my_drive.axis0.motor.DC_calib_phB))
		self.label_dcCalibPhCValue.setText(str(self.my_drive.axis0.motor.DC_calib_phC))
		self.label_errorAxisValue_2.setText(str(self.my_drive.axis0.motor.error))
		self.label_currentMeasPhCValue.setText(str(self.my_drive.axis0.motor.current_meas_phC))

		if self.my_drive.axis0.motor.is_calibrated:
			self.icon_isCalibratedValue.setPixmap(QtGui.QPixmap(ICON_TRUE))
		else:
			self.icon_isCalibratedValue.setPixmap(QtGui.QPixmap(ICON_FALSE))

		self.label_phaseCurrentRevGainValue.setText(str(self.my_drive.axis0.motor.phase_current_rev_gain))
		self.label_currentMeasPhBValue.setText(str(self.my_drive.axis0.motor.current_meas_phB))
		self.label_armedStateValue.setText(str(self.my_drive.axis0.motor.armed_state))




	def scan_axis0_motor_config_config(self):
		if self.my_drive.axis0.motor.config.pre_calibrated:
			self.radioButton_preCalibratedTrue.setChecked(True)
		else:
			self.radioButton_preCalibratedFalse.setChecked(True)

		self.doubleSpinBox_phaseInductanceValue.setValue(self.my_drive.axis0.motor.config.phase_inductance)
		self.doubleSpinBox_phaseResistanceValue.setValue(self.my_drive.axis0.motor.config.phase_resistance)
		self.spinBox_motorTypeValue.setValue(self.my_drive.axis0.motor.config.motor_type)
		self.doubleSpinBox_currentControlBandwidthValue.setValue(self.my_drive.axis0.motor.config.current_control_bandwidth)
		self.doubleSpinBox_requestedCurrentRangeValue.setValue(self.my_drive.axis0.motor.config.requested_current_range)
		self.spinBox_directionValue.setValue(self.my_drive.axis0.motor.config.direction)
		self.doubleSpinBox_resistanceCalibMaxVoltageValue.setValue(self.my_drive.axis0.motor.config.resistance_calib_max_voltage)
		self.doubleSpinBox_currentLimValue.setValue(self.my_drive.axis0.motor.config.current_lim)
		self.spinBox_poleParisValue.setValue(self.my_drive.axis0.motor.config.pole_pairs)
		self.doubleSpinBox_calibrationCurrentValue.setValue(self.my_drive.axis0.motor.config.calibration_current)




	def scan_axis1_config(self):
		pass

	def send_axis0_position_go(self):
		self.my_drive.axis0.controller.pos_setpoint = self.axis0Position_doubleSpinBox.value()

	def send_axis0_velocity_current_stop(self):
		self.send_axis0_velocity_current_command(self.my_drive.axis0.controller.config.control_mode, 0.0)

	def send_axis0_velocity_current_forward(self):
		mode = self.my_drive.axis0.controller.config.control_mode
		value = 0
		if mode == CTRL_MODE_CURRENT_CONTROL:
			value = self.axis0Current_doubleSpinBox.value()
		elif mode == CTRL_MODE_VELOCITY_CONTROL:
			value = self.axis0Velocity_doubleSpinBox.value()
		self.send_axis0_velocity_current_command(self.my_drive.axis0.controller.config.control_mode, value)

	def send_axis0_velocity_current_backward(self):
		mode = self.my_drive.axis0.controller.config.control_mode
		value = 0
		if mode == CTRL_MODE_CURRENT_CONTROL:
			value = self.axis0Current_doubleSpinBox.value() * -1
		elif mode == CTRL_MODE_VELOCITY_CONTROL:
			value = self.axis0Velocity_doubleSpinBox.value() * -1
		self.send_axis0_velocity_current_command(self.my_drive.axis0.controller.config.control_mode, value)


	def send_axis0_velocity_current_command(self, mode, value):
		if mode == CTRL_MODE_CURRENT_CONTROL:
			self.my_drive.axis0.controller.current_setpoint = value
		elif mode == CTRL_MODE_VELOCITY_CONTROL:
			self.my_drive.axis0.controller.vel_setpoint = value


	def clear_state_buttons(self):
		self.axis0_pushButton_idle.setStyleSheet("")
		self.axis0_pushButton_startupSequence.setStyleSheet("")
		self.axis0_pushButton_fullCalibrationSequence.setStyleSheet("")
		self.axis0_pushButton_motorCalibration.setStyleSheet("")
		self.axis0_pushButton_sensorlessControl.setStyleSheet("")
		self.axis0_pushButton_econderIndexSearch.setStyleSheet("")
		self.axis0_pushButton_encoderOffsetCalibration.setStyleSheet("")
		self.axis0_pushButton_closedLoopControl.setStyleSheet("")

	def idle_state(self):
		print("State: Idle")
		# self.axis0_pushButton_idle.setStyleSheet("background-color: rgb(135, 187, 249);")
		self.axis0_pushButton_idle.setStyleSheet("background-color: rgb(246, 224, 143);")

	def startup_seq_state(self):
		self.axis0_pushButton_startupSequence.setStyleSheet("background-color: rgb(246, 224, 143);")

	def full_calibration_seq_state(self):
		self.axis0_pushButton_fullCalibrationSequence.setStyleSheet("background-color: rgb(246, 224, 143);")

	def motor_calibration_state(self):
		self.axis0_pushButton_motorCalibration.setStyleSheet("background-color: rgb(246, 224, 143);")

	def sensorless_control_state(self):
		self.axis0_pushButton_sensorlessControl.setStyleSheet("background-color: rgb(246, 224, 143);")

	def encoder_index_search_state(self):
		self.axis0_pushButton_econderIndexSearch.setStyleSheet("background-color: rgb(246, 224, 143);")

	def encoder_offset_calibration_state(self):
		self.axis0_pushButton_encoderOffsetCalibration.setStyleSheet("background-color: rgb(246, 224, 143);")

	def closed_loop_control_state(self):
		self.axis0_pushButton_closedLoopControl.setStyleSheet("background-color: rgb(246, 224, 143);")

	def save_config(self):
		self.my_drive.save_configuration()

	def odrive_reboot(self):
		try:
			self.my_drive.reboot()
		except Exception as e:
			print(e)
			self.odrive_disconnected_exception()

	def idle_state_clicked(self):
		self.my_drive.axis0.requested_state = AXIS_STATE_IDLE
		# self.idle_state()

	def startupSequence_state_clicked(self):
		self.my_drive.axis0.requested_state = AXIS_STATE_STARTUP_SEQUENCE
		# self.startup_seq_state()

	def fullCalibrationSequence_state_clicked(self):
		self.my_drive.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
		# self.full_calibration_seq_state()

	def motorCalibration_state_clicked(self):
		self.my_drive.axis0.requested_state = AXIS_STATE_MOTOR_CALIBRATION
		# self.motor_calibration_state()

	def sensorlessControl_state_clicked(self):
		self.my_drive.axis0.requested_state = AXIS_STATE_SENSORLESS_CONTROL
		# self.sensorless_control_state()

	def econderIndexSearch_state_clicked(self):
		self.my_drive.axis0.requested_state = AXIS_STATE_ENCODER_INDEX_SEARCH
		# self.encoder_index_search_state()

	def encoderOffsetCalibration_state_clicked(self):
		self.my_drive.axis0.requested_state = AXIS_STATE_ENCODER_OFFSET_CALIBRATION
		# self.encoder_offset_calibration_state()

	def closedLoopControl_state_clicked(self):
		self.my_drive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
		# self.closed_loop_control_state()


def main():
	app = QtWidgets.QApplication(sys.argv)  # A new instance of QApplication
	form = ExampleApp()                 # We set the form to be our (design)
	form.show()                         # Show the form
	app.exec_()                         # and execute the app



if __name__ == '__main__':              # if we're running file directly and not importing it
	main()                              # run the main function
