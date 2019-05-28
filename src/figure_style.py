def cm2inch(*tupl):
    inch = 2.54
    if isinstance(tupl[0], tuple):
        return tuple(i/inch for i in tupl[0])
    else:
        return tuple(i/inch for i in tupl)

# figure size
SMALL_FIGURE_SIZE=cm2inch(6,4.5) #(8,6)
BIG_FIGURE_SIZE=cm2inch(12,6)
# content size
LINE_WIDTH=1
MARKER_SIZE=7
MARKEREDGE_WIDTH=1
LEGEND_SIZE=7
# label text size
TITLE_SIZE=10
XY_LABEL_SIZE=8
TICK_LABEL_SIZE=6
# spines width
XY_SPINES_WIDTH=1
# grid
GRID_WIDTH=1
