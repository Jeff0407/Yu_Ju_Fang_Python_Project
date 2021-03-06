"""
File: 'babygraphics.py
Name: Yu-Ju Fang
Baby Names Project
Adapted from Nick Parlante's Baby Names assignment by
Jerry Liao.

"""

import tkinter
import babynames
import babygraphicsgui as gui

FILENAMES = [
    'data/full/baby-1900.txt', 'data/full/baby-1910.txt',
    'data/full/baby-1920.txt', 'data/full/baby-1930.txt',
    'data/full/baby-1940.txt', 'data/full/baby-1950.txt',
    'data/full/baby-1960.txt', 'data/full/baby-1970.txt',
    'data/full/baby-1980.txt', 'data/full/baby-1990.txt',
    'data/full/baby-2000.txt', 'data/full/baby-2010.txt'
]
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 600
YEARS = [1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010]
GRAPH_MARGIN_SIZE = 20
COLORS = ['red', 'purple', 'green', 'blue']
TEXT_DX = 2
LINE_WIDTH = 2
MAX_RANK = 1000


def get_x_coordinate(width, year_index):
    """
    Given the width of the canvas and the index of the current year
    in the YEARS list, returns the x coordinate of the vertical
    line associated with that year.

    Input:
        width (int): The width of the canvas
        year_index (int): The index of the current year in the YEARS list
    Returns:
        x_coordinate (int): The x coordinate of the vertical line associated
                              with the specified year.
    """
    margin_between_x = (width - 2 * GRAPH_MARGIN_SIZE) // 12
    x_coordinate = GRAPH_MARGIN_SIZE + margin_between_x * year_index

    return x_coordinate


def draw_fixed_lines(canvas):
    """
    Erases all existing information on the given canvas and then
    draws the fixed background lines on it.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.

    Returns:
        This function does not return any value.
    """
    canvas.delete('all')            # delete all existing lines from the canvas


    canvas.create_line(0, GRAPH_MARGIN_SIZE, CANVAS_WIDTH, GRAPH_MARGIN_SIZE, width=LINE_WIDTH)
    canvas.create_line(0, CANVAS_HEIGHT-GRAPH_MARGIN_SIZE, CANVAS_WIDTH, CANVAS_HEIGHT-GRAPH_MARGIN_SIZE, width=LINE_WIDTH)
    for i in range(len(YEARS)):
        x = get_x_coordinate(CANVAS_WIDTH, i)
        canvas.create_line(x, 0, x, CANVAS_HEIGHT, width=LINE_WIDTH)
        canvas.create_text(x + TEXT_DX,CANVAS_HEIGHT-GRAPH_MARGIN_SIZE, text=YEARS[i], anchor=tkinter.NW)


def draw_names(canvas, name_data, lookup_names):
    """
    Given a dict of baby name data and a list of name, plots
    the historical trend of those names onto the canvas.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.
        name_data (dict): Dictionary holding baby name data
        lookup_names (List[str]): A list of names whose data you want to plot

    Returns:
        This function does not return any value.
    """
    draw_fixed_lines(canvas)        # draw the fixed background grid


    index = 0  # In order to change color
    for name in lookup_names:  # draw all the names we want to lookup
        if name in name_data:
            color = COLORS[index % 4]
            for i in range(len(YEARS)-1):  # calculate all the x and y coordinate in each year to draw graphics
                start_x = get_x_coordinate(CANVAS_WIDTH, i)
                if str(YEARS[i]) in name_data[name]:
                    start_y = int(name_data[name][str(YEARS[i])]) * 0.56 + GRAPH_MARGIN_SIZE
                else:
                    start_y = CANVAS_HEIGHT - GRAPH_MARGIN_SIZE
                end_x = get_x_coordinate(CANVAS_WIDTH, i + 1)
                if str(YEARS[i+1]) in name_data[name]:
                    end_y = int(name_data[name][str(YEARS[i + 1])]) * 0.56 + GRAPH_MARGIN_SIZE
                else:
                    end_y = CANVAS_HEIGHT - GRAPH_MARGIN_SIZE
                if str(YEARS[i]) in name_data[name]:
                    tag = f'{name} {name_data[name][str(YEARS[i])]}'
                else:
                    tag = f'{name} *'
                canvas.create_line(start_x, start_y, end_x, end_y,width=LINE_WIDTH, fill=color)
                canvas.create_text(start_x + TEXT_DX,start_y, text=tag, anchor=tkinter.SW, fill=color)

            #  Since the for loop above will miss the tag of name and rank so we need to add the info after the for loop
            if str(YEARS[i+1]) in name_data[name]:
                start_y = int(name_data[name][str(YEARS[i+1])]) * 0.56 + GRAPH_MARGIN_SIZE
            else:
                start_y = CANVAS_HEIGHT - GRAPH_MARGIN_SIZE
            if str(YEARS[i+1]) in name_data[name]:
                tag = f'{name} {name_data[name][str(YEARS[i+1])]}'
            else:
                tag = f'{name} *'
            canvas.create_text(get_x_coordinate(CANVAS_WIDTH, i + 1) + TEXT_DX, start_y, text=tag, anchor=tkinter.SW, fill=color)
            index += 1

# main() code is provided, feel free to read through it but DO NOT MODIFY
def main():
    # Load data
    name_data = babynames.read_files(FILENAMES)

    # Create the window and the canvas
    top = tkinter.Tk()
    top.wm_title('Baby Names')
    canvas = gui.make_gui(top, CANVAS_WIDTH, CANVAS_HEIGHT, name_data, draw_names, babynames.search_names)

    # Call draw_fixed_lines() once at startup so we have the lines
    # even before the user types anything.
    draw_fixed_lines(canvas)

    # This line starts the graphical loop that is responsible for
    # processing user interactions and plotting data
    top.mainloop()


if __name__ == '__main__':
    main()
