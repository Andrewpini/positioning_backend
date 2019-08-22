# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\test.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
import time
import ethernetcomm
import ctrlpanelwidget
from ethernetmsg import *
import struct
import random


def create_random_TID():
    UINT32_MAX = 0xffffffff
    random.seed(time.time())
    return random.randint(0, UINT32_MAX)

class Ui_main_widget(object):

    def __init__(self, main_widget):
        self.node_list = dict()
        self.node_count = 0
        self.selected_item = str()
        self.current_time_sync_node = 'None'
        self.current_sync_line_node = 'None'
        self.active_node_color = QtGui.QBrush(QtGui.QColor("#4278f5"))
        self.unactive_node_color = QtGui.QBrush(QtGui.QColor("#ff1500"))
        self.current_TID = None

        self.cpw = ctrlpanelwidget.CtrlPanelWidget(main_widget)
        self.connect_widgets()

        # Create ethernet communication instance and connect signals to corresponding handlers
        # self.ethernet = ethernetcomm.EthernetCommunicationThread("0.0.0.0", 11111, "255.255.255.255", 11111)
        # self.ethernet = ethernetcomm.EthernetCommunicationThread("0.0.0.0", 11001, "255.255.255.255", 10000)
        self.ethernet = ethernetcomm.EthernetCommunicationThread("0.0.0.0", 11001, "255.255.255.255", 11001)


        self.ethernet.sig_i_am_alive.connect(self.add_node)
        self.ethernet.sig_start_time_sync.connect(self.handle_foo)
        self.ethernet.sig_stop_time_sync.connect(self.handle_foo)
        self.ethernet.sig_start_sync_line.connect(self.handle_foo)
        self.ethernet.sig_stop_sync_line.connect(self.handle_foo)
        self.ethernet.sig_ack_msg.connect(self.handle_ack_msg)

    def connect_widgets(self):
        self.cpw.list_of_nodes.currentItemChanged.connect(self.on_item_changed)
        self.cpw.time_sync_start_btn.clicked.connect(self.send_time_sync_start_msg)
        self.cpw.time_sync_stop_btn.clicked.connect(self.send_time_sync_stop_msg)
        self.cpw.sync_line_start_btn.clicked.connect(self.send_sync_line_start_msg)
        self.cpw.sync_line_stop_btn.clicked.connect(self.send_sync_line_stop_msg)
        self.cpw.led_on_btn.clicked.connect(lambda: self.send_led_msg(False, True, self.node_list[self.selected_item]['Mac']))
        self.cpw.led_off_btn.clicked.connect(lambda: self.send_led_msg(False, False, self.node_list[self.selected_item]['Mac']))
        self.cpw.led_all_on_btn.clicked.connect(lambda: self.send_led_msg(True, True, None))
        self.cpw.led_all_off_btn.clicked.connect(lambda: self.send_led_msg(True, False, None))
        self.cpw.dfu_single_btn.clicked.connect(lambda: self.send_dfu_msg(False, self.node_list[self.selected_item]['Mac']))
        self.cpw.dfu_all_btn.clicked.connect(lambda: self.send_dfu_msg(True, None))
        self.cpw.reset_btn.clicked.connect(lambda: self.send_reset_msg(False, self.node_list[self.selected_item]['Mac']))
        self.cpw.reset_all_btn.clicked.connect(lambda: self.send_reset_msg(True, None))

    def add_node(self, msg):
        if msg.ID_string in self.node_list:
            self.node_list[msg.ID_string]['last_timestamp'] = time.time()
            self.node_list[msg.ID_string]['is_active'] = True
            self.node_list[msg.ID_string]['list_item'].setForeground(self.active_node_color)
            if self.selected_item == msg.ID_string:
                self.cpw.set_clickable_widgets(True)
        else:
            list_item = QtWidgets.QListWidgetItem(msg.ID_string)
            list_item.setForeground(self.active_node_color)
            self.node_list[msg.ID_string] = {'ip': msg.IP, 'Mac': msg.mac, 'Uni': 0, 'last_timestamp': time.time(), 'list_item': list_item, 'selector_idx': self.node_count, 'is_active': True}
            self.cpw.list_of_nodes.addItem(self.node_list[msg.ID_string]['list_item'])
            self.node_count += 1

    def node_timeout_check(self):
        timestamp = time.time()
        for node_ip in self.node_list:
            if (timestamp - self.node_list[node_ip]['last_timestamp']) > 5:
                self.node_list[node_ip]['list_item'].setForeground(self.unactive_node_color)
                self.node_list[node_ip]['is_active'] = False
                if self.selected_item == node_ip:
                    self.cpw.set_clickable_widgets(False)

    def on_item_changed(self, curr, prev):
        self.selected_item = curr.text()
        self.cpw.list_of_nodes.setCurrentItem(self.node_list[self.selected_item]['list_item'])
        if self.node_list[self.selected_item]['is_active']:
            self.cpw.set_clickable_widgets(True)
        else:
            self.cpw.set_clickable_widgets(False)

    def send_sync_line_start_msg(self):
        self.current_TID = create_random_TID()
        ting = StartSyncLineMsg().get_packed_msg(self.node_list[self.selected_item]['Mac'], self.current_TID)
        self.ethernet.broadcast_data(ting)
        self.cpw.sync_line_label.setText('Starting - Waiting for response from node %s' % self.node_list[self.selected_item]['ip'])
        self.current_sync_line_node = self.node_list[self.selected_item]['ip']
        print('asdfgasd')

    def send_sync_line_stop_msg(self):
        self.current_TID = create_random_TID()
        ting = StopSyncLineMsg().get_packed_msg(self.node_list[self.selected_item]['Mac'], self.current_TID)
        self.ethernet.broadcast_data(ting)
        self.cpw.sync_line_label.setText('Stopping - Waiting for response from node %s' % self.current_sync_line_node)

    def send_time_sync_start_msg(self):
        self.current_TID = create_random_TID()
        ting = StartTimeSyncMsg().get_packed_msg(self.node_list[self.selected_item]['Mac'], self.current_TID)
        self.ethernet.broadcast_data(ting)
        self.cpw.time_sync_label.setText('Starting - Waiting for response from node %s' % self.node_list[self.selected_item]['ip'])
        self.current_time_sync_node = self.node_list[self.selected_item]['ip']

    def send_time_sync_stop_msg(self):
        self.current_TID = create_random_TID()
        ting = StopTimeSyncMsg().get_packed_msg(self.node_list[self.selected_item]['Mac'], self.current_TID)
        self.ethernet.broadcast_data(ting)
        self.cpw.time_sync_label.setText('Stopping - Waiting for response from node %s' % self.current_time_sync_node)

    def send_led_msg(self, is_broadcast, on_off, target_addr):
        ting = LedMsg().get_packed_msg(is_broadcast, on_off, target_addr)
        self.ethernet.broadcast_data(ting)

    def send_dfu_msg(self, is_broadcast, target_addr):
        ting = DfuMsg().get_packed_msg(is_broadcast, target_addr)
        self.ethernet.broadcast_data(ting)

    def send_reset_msg(self, is_broadcast, target_addr):
        ting = ResetMsg().get_packed_msg(is_broadcast, target_addr)
        self.ethernet.broadcast_data(ting)

    def handle_ack_msg(self, msg):
        print(msg)
        if self.current_TID == msg.TID:
            if msg.ack_opcode == OPCODES['StartSyncLineMsg']:
                self.cpw.sync_line_label.setText('Current sync line master is node %s' % msg.sender_mac_addr)
                pass
            if msg.ack_opcode == OPCODES['StopSyncLineMsg']:
                self.cpw.sync_line_label.setText('Sync line was stopped by user')
                pass
            if msg.ack_opcode == OPCODES['StartTimeSyncMsg']:
                self.cpw.time_sync_label.setText('Current time sync master is node %s' % msg.sender_mac_addr)
                pass
            if msg.ack_opcode == OPCODES['StopTimeSyncMsg']:
                self.cpw.time_sync_label.setText('Sync line was stopped by user')
                pass

    def handle_foo(self, msg):
        print('asd')
        ting = AckMsg().get_packed_msg(msg.sender_mac_addr, msg.TID, msg.OPCODE)
        self.ethernet.broadcast_data(ting)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_widget = QtWidgets.QWidget()
    ui = Ui_main_widget(main_widget)

    timer = QtCore.QTimer()
    timer.timeout.connect(ui.node_timeout_check)
    timer.start(1000)

    main_widget.show()
    sys.exit(app.exec_())

