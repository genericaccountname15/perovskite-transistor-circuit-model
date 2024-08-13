"""
Generates array of axes positions for slider objects
They occupy a box with edges [(0.07, 0.05) (0.07, 0.15) (0.82, 0.15) (0.82, 0.05)]

Timothy Chew
12/8/2024
"""

def gen_axes(param_list):
    """
    Generates arrays of axes positions which occupies
    box with edges [(0.07, 0.05) (0.07, 0.15) (0.82, 0.15) (0.82, 0.05)]
    Args:
        param_list: list of parameters
    Returns:
        List of axes positions for sliders and buttons
    """
    no_of_columns = (len(param_list) - 2) // 3 + 1
    #kbt and n no slider

    #y-axis positions
    y_pos = [0.15, 0.10, 0.05]

    object_height = 0.03
    column_length = ( 0.82 - 0.07 ) / (no_of_columns)
    slider_length = column_length * 0.5
    button_length = column_length * 0.2
    padding = column_length * 0.1
    spacing = column_length * 0.2

    #array axes positions
    ax_pos_slider = []
    ax_pos_button = []

    for i in range(no_of_columns):
        for j in range(3):
            xpos_slider = 0.07 + i * column_length
            xpos_button = 0.07 + slider_length + padding + i * column_length
            ax_pos_slider.append([xpos_slider, y_pos[j], slider_length, object_height])
            ax_pos_button.append([xpos_button, y_pos[j], button_length, object_height])

    return ax_pos_slider, ax_pos_button
