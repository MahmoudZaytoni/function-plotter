import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget
from GUI.widgets import Sidebar, PlotSection

"""
    The MainWindow has two sections in its layout:
        1- Sidebar
        2- Plot Section
        +---+-------------------+
        |   |                   |
        |   |                   |
        |   |                   |
        |   |                   |
        +---+-------------------+
          2 :         8
"""
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Function Plotter')

        self.plot_section = PlotSection(self)
        self.sidebar = Sidebar(self.plot_section, self)
        
        layout = QHBoxLayout()
        layout.addWidget(self.sidebar, 2)
        layout.addWidget(self.plot_section, 8)
        
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()