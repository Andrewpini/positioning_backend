# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\test.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!

def legg_hain_t():
    ui.add_node('3', '10.0.0.1', 'FFFF')


from PyQt5 import QtCore, QtGui, QtWidgets
import time


class Ui_main_widget(object):

    def __init__(self):
        self.node_list = dict()

    def setupUi(self, main_widget):

        #--- Create all buttons ---
        self.init_btn = QtWidgets.QPushButton()
        self.init_btn.setObjectName("init_btn")
        self.init_btn.setText("Initialize")
        self.time_sync_stop_btn = QtWidgets.QPushButton()
        self.time_sync_stop_btn.setObjectName("time_sync_stop_btn")
        self.time_sync_stop_btn.setText("Stop")
        self.time_sync_start_btn = QtWidgets.QPushButton()
        self.time_sync_start_btn.setObjectName("time_sync_start_btn")
        self.time_sync_start_btn.setText("Start")
        self.sync_line_stop_btn = QtWidgets.QPushButton()
        self.sync_line_stop_btn.setObjectName("sync_line_stop_btn")
        self.sync_line_stop_btn.setText("Stop")
        self.sync_line_start_btn = QtWidgets.QPushButton()
        self.sync_line_start_btn.setObjectName("sync_line_start_btn")
        self.sync_line_start_btn.setText("Start")
        self.reset_btn = QtWidgets.QPushButton()
        self.reset_btn.setObjectName("reset_btn")
        self.reset_btn.setText("Reset")


        # --- Create all lists ---
        self.list_of_nodes = QtWidgets.QListWidget()
        self.list_of_nodes.setProperty("showDropIndicator", False)
        self.list_of_nodes.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.list_of_nodes.setObjectName("list_of_nodes")


        # --- Create all labels ---
        self.sync_line_label = QtWidgets.QLabel()
        self.sync_line_label.setObjectName("sync_line_label")
        self.sync_line_label.setText("Waiting for initialization")
        self.time_sync_label = QtWidgets.QLabel()
        self.time_sync_label.setObjectName("time_sync_label")
        self.time_sync_label.setText("Waiting for initialization")


        # --- Create all combo boxes ---
        self.sync_line_selector = QtWidgets.QComboBox()
        self.sync_line_selector.setObjectName("sync_line_selector")
        self.time_sync_selector = QtWidgets.QComboBox()
        self.time_sync_selector.setObjectName("time_sync_selector")


        #---  Create Syncronization line group box ---
        self.sync_line_gbox = QtWidgets.QGroupBox()
        self.sync_line_gbox.setObjectName("sync_line_gbox")
        self.sync_line_gbox.setTitle("Sync line")
        self.sync_line_gbox_layout = QtWidgets.QVBoxLayout(self.sync_line_gbox)
        self.sync_line_gbox_layout.setObjectName("sync_line_gbox_layout")
        self.sync_line_gbox_layout.addWidget(self.sync_line_selector)
        self.sync_line_gbox_layout.addWidget(self.sync_line_label)
        self.sync_line_btn_layout = QtWidgets.QHBoxLayout()
        self.sync_line_btn_layout.setObjectName("sync_line_btn_layout")
        self.sync_line_btn_layout.addWidget(self.sync_line_start_btn)
        self.sync_line_btn_layout.addWidget(self.sync_line_stop_btn)
        self.sync_line_gbox_layout.addLayout(self.sync_line_btn_layout)


        # ---  Create Time syncronization group box ---
        self.time_sync_gbox = QtWidgets.QGroupBox()
        self.time_sync_gbox.setObjectName("time_sync_gbox")
        self.time_sync_gbox.setTitle("Time syncronization")
        self.time_sync_gbox_layout = QtWidgets.QVBoxLayout(self.time_sync_gbox)
        self.time_sync_gbox_layout.setObjectName("time_sync_gbox_layout")
        self.time_sync_btn_layout = QtWidgets.QHBoxLayout()
        self.time_sync_btn_layout.setObjectName("time_sync_btn_layout")
        self.time_sync_gbox_layout.addWidget(self.time_sync_selector)
        self.time_sync_gbox_layout.addWidget(self.time_sync_label)
        self.time_sync_btn_layout.addWidget(self.time_sync_start_btn)
        self.time_sync_btn_layout.addWidget(self.time_sync_stop_btn)
        self.time_sync_gbox_layout.addLayout(self.time_sync_btn_layout)


        # ---  Create Available nodes group box ---
        self.nodes_gbox = QtWidgets.QGroupBox()
        self.nodes_gbox.setObjectName("nodes_gbox")
        self.nodes_gbox.setTitle("Available nodes")
        self.nodes_gbox_layout = QtWidgets.QVBoxLayout(self.nodes_gbox)
        self.nodes_gbox_layout.setObjectName("nodes_gbox_layout")
        self.nodes_gbox_layout.addWidget(self.list_of_nodes)


        # ---  Create is initialized frame group box ---
        #(used to group objects that needs to be collectivly be enabled/disabled)
        self.is_init_frame = QtWidgets.QFrame()
        self.is_init_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.is_init_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.is_init_frame.setObjectName("is_init_frame")
        self.is_init_frame_layout = QtWidgets.QVBoxLayout(self.is_init_frame)
        self.is_init_frame_layout.setObjectName("is_init_frame_layout")
        self.is_init_frame_layout.addWidget(self.sync_line_gbox)
        self.is_init_frame_layout.addWidget(self.time_sync_gbox)
        self.is_init_frame_layout.addWidget(self.reset_btn)


        #--- Create main layout ---
        main_widget.setObjectName("main_widget")
        main_widget.resize(332, 549)
        main_widget.setWindowTitle("Command Panel")
        self.main_layout = QtWidgets.QVBoxLayout(main_widget)
        self.main_layout.setObjectName("main_layout")
        self.main_layout.addWidget(self.init_btn)
        self.main_layout.addWidget(self.nodes_gbox)
        self.main_layout.addWidget(self.is_init_frame)


        QtCore.QMetaObject.connectSlotsByName(main_widget)

    def add_node(self, unicast, ip, mac):
        active_node_color = QtGui.QBrush(QtGui.QColor("#4278f5"))
        if ip in self.node_list:
            print('already in there')
            self.node_list[ip]['last_timestamp'] = time.time()
            self.node_list[ip]['list_item'].setForeground(active_node_color)
        else:
            list_item = QtWidgets.QListWidgetItem('IP: ' + ip + ' | ' + 'MAC: ' + mac + ' | ' + 'Unicast: ' + unicast)
            list_item.setForeground(active_node_color)

            self.node_list[ip] = {'ip': ip, 'Mac': mac, 'Uni': unicast, 'last_timestamp': time.time(), 'list_item': list_item}
            self.list_of_nodes.addItem(self.node_list[ip]['list_item'])
        print(self.node_list)

    def node_timeout_check(self):
        unactive_node_color = QtGui.QBrush(QtGui.QColor("#ff1500"))
        timestamp = time.time()
        for node_ip in self.node_list:
            if (timestamp - self.node_list[node_ip]['last_timestamp']) > 5:
                self.node_list[node_ip]['list_item'].setForeground(unactive_node_color)
                print('her')


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_widget = QtWidgets.QWidget()
    ui = Ui_main_widget()
    ui.setupUi(main_widget)

    timer = QtCore.QTimer()
    timer.timeout.connect(ui.node_timeout_check)
    timer.start(5000)

    ui.init_btn.clicked.connect(legg_hain_t)

    ui.add_node('3', '10.0.0.1', 'FFFF')

    main_widget.show()
    sys.exit(app.exec_())

    time.sleep(6)
    ui.add_node('3', '10.0.0.2', 'FFFF')