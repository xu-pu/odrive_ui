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
import numpy as np

from odrive_thread import odriveWorker

ICON_TRUE = "/home/imu/Projects/odrive/odrive_ui/Icons/True.jpg"
ICON_FALSE = "/home/imu/Projects/odrive/odrive_ui/Icons/False.jpg"
ICON_NOSTATE = "/home/imu/Projects/odrive/odrive_ui/Icons/NoState.jpg"

class ExampleApp(QtWidgets.QMainWindow, UI_mainwindow.Ui_MainWindow):

	app_name = "Odrive Tester"
	def __init__(self):
		# Explaining super is out of the scope of this article
		# So please google it if you're not familar with it
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

		self.axis0_pushButton_sendController.clicked.connect(self.send_axis_control)

		self.axis0_listWidget_controller.currentItemChanged.connect(self.control_mode_selected)


		self.plotWidget_velocity.setLabel('bottom', 'Time', 's')
		self.plotWidget_velocity.setLabel('left', 'Velocity', 'rpm')
		#self.plotWidget_velocity.setXRange(0,self.spinBox_graphTime.value())
		#self.plotWidget_velocity.setYRange(0, 12)
		self.plotWidget_velocity.setTitle("Velocity")
		# self.plotWidget_velocity.addLegend()
		self.velocity_setpoint_curve = self.plotWidget_velocity.plot(name="Setpoint", pen=pg.mkPen(color=(0, 128, 255), width=2))
		self.velocity_estimate_curve = self.plotWidget_velocity.plot(name="Estimate", pen=pg.mkPen(color=(255, 192, 0), width=2))

		self.plotWidget_position.setLabel('bottom', 'Time', 's')
		self.plotWidget_position.setLabel('left', 'Position', 'counts')
		#self.plotWidget_position.setXRange(0,self.spinBox_graphTime.value())
		#self.plotWidget_position.setYRange(0, 12)
		self.plotWidget_position.setTitle("Position")
		self.position_setpoint_curve = self.plotWidget_position.plot(name="Setpoint", pen=pg.mkPen(color=(0, 128, 255), width=2))
		self.position_estimate_curve = self.plotWidget_position.plot(name="Estimate", pen=pg.mkPen(color=(255, 192, 0), width=2))

		self.plotWidget_current.setLabel('bottom', 'Time', 's')
		self.plotWidget_current.setLabel('left', 'Current', 'Iq')
		#self.plotWidget_current.setXRange(0,self.spinBox_graphTime.value())
		#self.plotWidget_current.setYRange(0, 12)
		self.plotWidget_current.setTitle("Current")
		self.current_setpoint_curve = self.plotWidget_current.plot(name="Setpoint", pen=pg.mkPen(color=(0, 128, 255), width=2))
		self.current_estimate_curve = self.plotWidget_current.plot(name="Estimate", pen=pg.mkPen(color=(255, 192, 0), width=2))

		self.axis_dict = {}
		self.axis_dict["position"] = {}
		self.axis_dict["position"]["estimate"] = []
		self.axis_dict["position"]["set_point"] = []
		self.axis_dict["velocity"] = {}
		self.axis_dict["velocity"]["estimate"] = []
		self.axis_dict["velocity"]["set_point"] = []
		self.axis_dict["current"] = {}
		self.axis_dict["current"]["estimate"] = []
		self.axis_dict["current"]["set_point"] = []

		self.axis_dict["time_array"] = []

		self.axis0_state = None

		self.setDisabled_odrive_ui(True)

		self.odrive_connect()



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


	def odrive_connected(self, my_drive):
		self.my_drive = my_drive

		self.statusBar.showMessage("Serial number: {}".format(self.my_drive.serial_number))
		#if my drive is found
		self.timer = pg.QtCore.QTimer()
		self.timer.timeout.connect(self.update)
		self.timer.start(500)

		self.axis_dict["start_time"] = pg.ptime.time()
		self.timer2 = pg.QtCore.QTimer()
		self.timer2.timeout.connect(self.update_graphs)
		self.timer2.start(20)

		self.setDisabled_odrive_ui(False)

		self.axis0_listWidget_controller.setDisabled(False)
		self.groupBox_controller.setDisabled(False)
		self.groupBox_13.setDisabled(False)

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



	def update_controller_mode(self):
		print("Controller mode {}".format(self.my_drive.axis0.controller.config.control_mode))
		self.axis0_listWidget_controller.setCurrentRow(self.my_drive.axis0.controller.config.control_mode)

	def update_graphs(self):
		delta = pg.ptime.time() - self.axis_dict["start_time"]
		self.axis_dict["time_array"].append(delta)
		self.update_velocity_graph()
		self.update_position_graph()
		self.update_current_graph()
		self.update_X_range()

	def update_velocity_graph(self):
		self.axis_dict["velocity"]["estimate"].append(self.my_drive.axis0.encoder.vel_estimate)
		self.axis_dict["velocity"]["set_point"].append(self.my_drive.axis0.controller.vel_setpoint)
		self.velocity_setpoint_curve.setData(self.axis_dict["time_array"], self.axis_dict["velocity"]["set_point"])
		self.velocity_estimate_curve.setData(self.axis_dict["time_array"], self.axis_dict["velocity"]["estimate"])

	def update_current_graph(self):
		self.axis_dict["current"]["estimate"].append(self.my_drive.axis0.motor.current_control.Iq_measured)
		self.axis_dict["current"]["set_point"].append(self.my_drive.axis0.motor.current_control.Iq_setpoint)
		self.current_setpoint_curve.setData(self.axis_dict["time_array"], self.axis_dict["current"]["set_point"])
		self.current_estimate_curve.setData(self.axis_dict["time_array"], self.axis_dict["current"]["estimate"])

	def update_position_graph(self):
		self.axis_dict["position"]["estimate"].append(self.my_drive.axis0.encoder.pos_estimate)
		self.axis_dict["position"]["set_point"].append(self.my_drive.axis0.controller.pos_setpoint)
		self.position_setpoint_curve.setData(self.axis_dict["time_array"], self.axis_dict["position"]["set_point"])
		self.position_estimate_curve.setData(self.axis_dict["time_array"], self.axis_dict["position"]["estimate"])

	def update_X_range(self):
		upper_limit = self.axis_dict["time_array"][-1]
		lower_limit = self.axis_dict["time_array"][0]
		delta = self.spinBox_graphTime.value()
		if (upper_limit - lower_limit) > delta:
			while((upper_limit - lower_limit) > delta):
				self.axis_dict["time_array"].pop(0)
				self.axis_dict["velocity"]["estimate"].pop(0)
				self.axis_dict["velocity"]["set_point"].pop(0)
				self.axis_dict["current"]["estimate"].pop(0)
				self.axis_dict["current"]["set_point"].pop(0)
				self.axis_dict["position"]["estimate"].pop(0)
				self.axis_dict["position"]["set_point"].pop(0)
				upper_limit = self.axis_dict["time_array"][-1]
				lower_limit = self.axis_dict["time_array"][0]

		# if upper_limit >= delta:
		# 	lower_l = upper_limit - delta
		# 	self.plotWidget_velocity.setXRange(lower_l, upper_limit)
		# 	self.plotWidget_position.setXRange(lower_l, upper_limit)
		# 	self.plotWidget_current.setXRange(lower_l, upper_limit)


	def update(self):
		# self.update_voltage()
		self.update_machine_state()

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
		self.label_serialNumberValue.setText(str(int(self.my_drive.serial_number)))



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
		pass

	def scan_axis0_motor_config(self):
		pass



	def scan_axis1_config(self):
		pass

	def send_axis_control(self):
		print(self.axis0_spinBox_controllerValue.value())

		print(self.axis0_listWidget_controller.currentRow())
		print(self.my_drive.axis0.controller.config.control_mode)
		if self.my_drive.axis0.controller.config.control_mode == self.axis0_listWidget_controller.currentRow():
			if self.axis0_listWidget_controller.currentRow() == 3:
				self.my_drive.axis0.controller.pos_setpoint = self.axis0_spinBox_controllerValue.value()

		# self.my_drive.axis0.
	#
    # <axis>.controller.pos_setpoint = <encoder_counts>
    # <axis>.controller.current_setpoint = <current_in_A>
    # <axis>.controller.vel_setpoint = <encoder_counts/s>

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
		self.my_drive.reboot()

	def idle_state_clicked(self):
		self.my_drive.axis0.requested_state = AXIS_STATE_IDLE
		self.idle_state()

	def startupSequence_state_clicked(self):
		self.my_drive.axis0.requested_state = AXIS_STATE_STARTUP_SEQUENCE
		self.startup_seq_state()

	def fullCalibrationSequence_state_clicked(self):
		self.my_drive.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
		self.full_calibration_seq_state()

	def motorCalibration_state_clicked(self):
		self.my_drive.axis0.requested_state = AXIS_STATE_MOTOR_CALIBRATION
		self.motor_calibration_state()

	def sensorlessControl_state_clicked(self):
		self.my_drive.axis0.requested_state = AXIS_STATE_SENSORLESS_CONTROL
		self.sensorless_control_state()

	def econderIndexSearch_state_clicked(self):
		self.my_drive.axis0.requested_state = AXIS_STATE_ENCODER_INDEX_SEARCH
		self.encoder_index_search_state()

	def encoderOffsetCalibration_state_clicked(self):
		self.my_drive.axis0.requested_state = AXIS_STATE_ENCODER_OFFSET_CALIBRATION
		self.encoder_offset_calibration_state()

	def closedLoopControl_state_clicked(self):
		self.my_drive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
		self.closed_loop_control_state()


	def control_mode_selected(self, list_item):
		name = list_item.text()
		print("Selected new control mode - {}".format(name))
		if name == "Position":
			self.my_drive.axis0.controller.config.control_mode = CTRL_MODE_POSITION_CONTROL
		elif name == "Current":
			self.my_drive.axis0.controller.config.control_mode = CTRL_MODE_CURRENT_CONTROL
		elif name == "Velocity":
			self.my_drive.axis0.controller.config.control_mode = CTRL_MODE_VELOCITY_CONTROL



def main():
	app = QtWidgets.QApplication(sys.argv)  # A new instance of QApplication
	form = ExampleApp()                 # We set the form to be our (design)
	form.show()                         # Show the form
	app.exec_()                         # and execute the app



if __name__ == '__main__':              # if we're running file directly and not importing it
	main()                              # run the main function
