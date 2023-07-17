import pytest
import run as GUI

from GUI.constants import (
    MSG_INVALID_EQUATION, 
    MSG_INVALID_INPUT, 
    MSG_INVALID_RANGE, 
    MSG_MISSED_FUNCTION,
    VALID_INPUTS,
)

data_missed_function = {
    'fx': '',
    'min': -10,
    'max': 10,
}

data_invalid_equation = {
    'fx': 'x + ',
    'min': 2,
    'max': 5,
}

data_invalid_input = {
    'fx': 'x%',
    'min': -10,
    'max': 10,
}

data_invalid_range = {
    'fx': 'x',
    'min': 0.01,
    'max': 0,
}

data_accepted = {
    'fx': '(x ^ 2) + (50 * x) - 2^x',
    'min': -10,
    'max': 10,
}

data_accepted2 = {
    'fx': '5',
    'min': -10,
    'max': 10,
}

@pytest.mark.parametrize(
    ('input_data', 'expected_error'),
    (
        (data_missed_function, MSG_MISSED_FUNCTION),
        (data_invalid_equation, MSG_INVALID_EQUATION),
        (data_invalid_range, MSG_INVALID_RANGE),
        (data_invalid_input, MSG_INVALID_INPUT),
        (data_accepted, ''),
        (data_accepted2, ''),
    )
)

def test_app(qtbot, input_data, expected_error): 
    app = GUI.MainWindow()
    qtbot.addWidget(app)
    
    sidebar = app.sidebar
    plot_button = sidebar.plot_button
    inputs_box = sidebar.inputs_box
    error_box = sidebar.error_box
    
    qtbot.addWidget(error_box)
    fx = input_data['fx']
    min = input_data['min']
    max = input_data['max']
    inputs_box.function_input.setText(fx)
    inputs_box.min_input.setValue(min)
    inputs_box.max_input.setValue(max)
    
    if input_data == data_invalid_input:
        expected_error = expected_error.format(char='%', valid_chars=(', ').join(VALID_INPUTS))

    plot_button.click()
    assert error_box.text() == expected_error