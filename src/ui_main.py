from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
import pyqtgraph as pg
import sys

from src.data_loader import load_mock_breathing_data
from src.signal_processing import bandpass_filter, estimate_breathing_rate

class BreathUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Breathing Monitor")
        self.resize(600, 400)

        # 创建界面布局
        layout = QVBoxLayout()
        self.setLayout(layout)

        # 呼吸频率标签
        self.label = QLabel("Breathing Rate: -- bpm")
        layout.addWidget(self.label)

        # 波形图区域
        self.plot = pg.PlotWidget()
        layout.addWidget(self.plot)

        # 加载数据并显示
        self.plot_breath_data()

    def plot_breath_data(self):
        raw = load_mock_breathing_data()
        filtered = bandpass_filter(raw)
        bpm = estimate_breathing_rate(filtered)

        self.label.setText(f"Breathing Rate: {bpm:.2f} bpm")
        self.plot.plot(filtered, pen='g')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = BreathUI()
    ui.show()
    sys.exit(app.exec_())
