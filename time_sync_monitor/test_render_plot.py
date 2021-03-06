
from PyQt5 import QtGui, QtCore
import pyqtgraph
from test_av_sample_parser import *

# TODO:Add better system for picking the colors of the curves
#QtCore.Qt.DashDotLine
COLOR = (
    ['red', (255, 0, 0), QtCore.Qt.DashDotLine],
    ['green', (51, 204, 51)],
    ['blue', (0, 102, 255)],
    ['pink', (255, 102, 255)],
    ['yellow', (255, 255, 0)],
    ['purple', (102, 0, 102)],
    ['magenta', (204, 0, 153)],
    ['dark_green', (0, 102, 0)],
    ['dark_blue', (0, 0, 204)],
    ['teal', (0, 255, 255)],
    ['grey', (102, 102, 153)],
    ['brown', (153, 102, 51)],
)
COLOR_CNT = len(COLOR)


class CurveData(pyqtgraph.PlotCurveItem):
    PARTIAL_CURVE_MAX = 50
    def __init__(self, node_name, color='w', parent=None):
        super(CurveData, self).__init__(parent, name=node_name)
        self.x_axis_data = []
        self.y_axis_data = []
        self.color = color
        self.setPen(color, width=1)
        self.list_length = 0
        self.partial_sample_cnt = 50

    def add_sample(self, x_axis_sample, y_axis_sample):
        self.list_length += 1
        if not self.x_axis_data:
            self.x_axis_data.append(x_axis_sample)
            self.y_axis_data.append(y_axis_sample)
        else:
            for idx in range(len(self.x_axis_data)):
                if x_axis_sample < self.x_axis_data[idx]:
                    self.x_axis_data.insert(idx, x_axis_sample)
                    self.y_axis_data.insert(idx, y_axis_sample)
                    break
                if idx == len(self.x_axis_data) - 1:
                    self.x_axis_data.append(x_axis_sample)
                    self.y_axis_data.append(y_axis_sample)

    def clear_curve(self):
        self.x_axis_data.clear()
        self.y_axis_data.clear()
        self.setData(self.x_axis_data, self.y_axis_data)
        self.clear()

    def set_partial_plot_cnt(self, cnt):
        self.partial_sample_cnt = cnt
        self.plot_partial_curve()

    def plot_entire_curve(self):
        self.setData(self.x_axis_data, self.y_axis_data)

    def plot_partial_curve(self):
        if self.list_length <= self.partial_sample_cnt:
            self.plot_entire_curve()
        else:
            self.setData(self.x_axis_data[-self.partial_sample_cnt:], self.y_axis_data[-self.partial_sample_cnt:])



class TimeSyncPlot(pyqtgraph.PlotWidget):
    UINT32T_MAX = 0xFFFFFFFF
    LATE_SAMPLE_MAX_DIFF = 5
    def __init__(self, plot_partial=False, parent=None):
        super(TimeSyncPlot, self).__init__(parent)
        self.curve_dict = {}
        self.curve_cnt = 0
        self.showGrid(x=True, y=True, alpha=0.8)
        self.plot_partial = plot_partial
        self.highest_sample_nr = 0

    def reset_plotter(self):
        self.highest_sample_nr = 0

    def add_plot_sample(self, sample_nr, sample_dict):
        if sample_nr > self.highest_sample_nr:
            self.highest_sample_nr = sample_nr
        elif (self.highest_sample_nr - sample_nr) > self.LATE_SAMPLE_MAX_DIFF:
            print('Discarding super old sample')
            return
        try:
            for node_name, value in sample_dict.items():
                if node_name in self.curve_dict:
                    # Adds a sample to a existing curve
                    self.curve_dict[node_name].add_sample(sample_nr, value)
                    pass
                else:
                    # Appends a new curve to the curve dict
                    new_curve = CurveData(node_name, COLOR[self.curve_cnt % COLOR_CNT][1])
                    self.curve_cnt += 1
                    self.addItem(new_curve)
                    self.curve_dict[node_name] = new_curve
                    self.curve_dict[node_name].add_sample(sample_nr, value)
            if self.plot_partial:
                self.plot_partial_sampleset()
            else:
                self.plot_full_sampleset()
        except:
            print('Unable to add sample - Discarded')

    def plot_full_sampleset(self):
        for node_name in self.curve_dict:
            self.curve_dict[node_name].plot_entire_curve()

    def clear_entire_plot(self):
        for node_name in self.curve_dict:
            self.curve_dict[node_name].clear_curve()

    def plot_partial_sampleset(self):
        for node_name in self.curve_dict:
            self.curve_dict[node_name].plot_partial_curve()

    def set_partial_sampleset_cnt(self, cnt):
        for node_name in self.curve_dict:
            self.curve_dict[node_name].set_partial_plot_cnt(cnt)




