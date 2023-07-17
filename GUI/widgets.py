import numpy as np
from PySide2.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton,
    QGroupBox, QLabel, QLineEdit,
    QDoubleSpinBox, QMessageBox,
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from .constants import (
    MIN,
    MAX,
    VALID_INPUTS,
    MSG_INVALID_EQUATION, 
    MSG_INVALID_INPUT, 
    MSG_INVALID_RANGE, 
    MSG_MISSED_FUNCTION,
)

"""
    Plot Section Class
        - Responsible for ploting the functions.
    
    methods:
        plot() 
            - ploting the function by passing x, fx
            - x  => np.linspace() discrete values list from min to max
            - fx => user valid input function like => (x^2)+(1/5)*x
            
        clear_plot()
            - clear the plot and set lables and grid
            
        update_plot()
            - updating plot by using clear_plot() then plot().
"""
class PlotSection(QWidget):
    
    def __init__(self, parent=None):
        super().__init__(parent)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Settings some configurations of matplot
        self.ax = self.figure.add_subplot(111) # 11 => 1x1 grid, 111 => the last one is the window number
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('f(x)')
        self.ax.grid(True)

        self.canvas.draw()

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.toolbar)
        self.setLayout(layout)

    def plot(self, x, fx):
        self.ax.plot(x, np.full(x.shape, eval(fx)))
        self.canvas.draw()
    
    def clear_plot(self):
        self.ax.clear()
        self.ax.grid(True)
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('f(x)')
        
    def update_plot(self, x, fx):
        self.clear_plot()
        self.plot(x, fx)
        

"""
    InputGroupBox class
        - Responsible for manage user inputs
    
    methods:
        - get_data() => capture user inputs 
        - normalize_equation()
            => take normal mathematics equation and convert it to python equation and remove spaces
            => ex: fx = (x ^ 2) =====> fx = (x**2)
        - validate() => validate user data and raise errors if exsist
"""
class InputGroupBox(QWidget):
    
    def __init__(self):
        QWidget.__init__(self)

        groupbox = QGroupBox("")
        layout = QVBoxLayout()
        layout.addWidget(groupbox)

        function_label = QLabel("f(x)", self)
        self.function_input = QLineEdit(self)

        min_label = QLabel("Min:", self)
        self.min_input = QDoubleSpinBox(self)
        self.min_input.setMinimum(MIN)
        self.min_input.setMaximum(MAX)

        max_label = QLabel("Max:", self)
        self.max_input = QDoubleSpinBox(self)
        self.max_input.setMinimum(MIN)
        self.max_input.setMaximum(MAX)

        # Create layout
        vbox = QVBoxLayout()
        groupbox.setLayout(vbox)
        vbox.addWidget(function_label)
        vbox.addWidget(self.function_input)
        vbox.addWidget(min_label)
        vbox.addWidget(self.min_input)
        vbox.addWidget(max_label)
        vbox.addWidget(self.max_input)
        
        self.setLayout(layout)
        
    def get_data(self):      
        data = {
            'fx': str(self.function_input.text()),
            'min': float(self.min_input.value()),
            'max': float(self.max_input.value()),
        }
        return data
    
    def normalize_equation(self, fx):
        # 1- remove spaces
        fx = fx.replace(' ', '')
        
        # 2- remove each ^ to ** to make it as python equation
        fx = fx.replace('^', '**')
        return fx
    
    def validate(self):
        data = self.get_data()
        
        mn = data['min']
        mx = data['max']
        if mn >= mx:
            raise Exception(MSG_INVALID_RANGE)
         
        fx = data['fx']
        if not fx:
            raise Exception(MSG_MISSED_FUNCTION)
        
        fx = self.normalize_equation(fx)
        for char in fx:
            if char not in VALID_INPUTS:
                raise Exception(MSG_INVALID_INPUT.format(char=char, valid_chars=(', ').join(VALID_INPUTS)))
        
        x = 1
        try:
            eval(fx)
        except:
            raise Exception(MSG_INVALID_EQUATION)
  
"""
    Sidebar class
        - Responsible for getting data from inputs_box and send it to plotsection 
    
    methods:
        - plot_function()
            => get data from inputs box and check 
                - if there is errors 
                    * display error message in error_box
                - else 
                    * update_plot in plot section
"""          
class Sidebar(QWidget):
    
    def __init__(self, plot_section, parent=None):
        super().__init__(parent)
        self.plot_section = plot_section
        
        self.inputs_box = InputGroupBox()
        self.plot_button = QPushButton("Plot", self)
        self.plot_button.clicked.connect(self.plot_function)
        self.plot_button.setMinimumHeight(150)
        self.plot_button.setMaximumHeight(900)
        self.plot_button.setStyleSheet("font-size: 20px; padding: 20px;")
        
        self.error_box = QMessageBox(self)
        
        layout = QVBoxLayout()
        layout.addWidget(self.inputs_box, 5)
        layout.addWidget(self.plot_button, 5)
        self.setLayout(layout)

    def plot_function(self):
        data = self.inputs_box.get_data()
        try:
            self.inputs_box.validate()
        except Exception as e:
            self.error_box.setWindowTitle("Error !")
            self.error_box.setIcon(QMessageBox.Critical)
            self.error_box.setText(f'{e}')
            self.error_box.show()
            return
        
        x = np.linspace(data['min'], data['max'])
        fx = data['fx']
        fx = self.inputs_box.normalize_equation(fx)
        self.plot_section.update_plot(x, fx)
        