import numpy as np
from matplotlib.colors import ListedColormap
import os

def is_float(element) -> bool:
    try:
        float(element)
        return True
    except ValueError:
        return False

def cmap(name):
    if name.endswith('_r'):
        name = name[:-2]
        flag_reverse = True
    else:
        flag_reverse = False

    cwd = os.path.dirname(os.path.realpath(__file__))
    f = open(cwd+'/{}.rgb'.format(name), 'r')
    lines = f.readlines()
    lines = list(map(lambda s: s.strip('\n'), lines))

    li_rgb = []
    for i in range(len(lines)):
        line = lines[i]

        colors = [float(s) for s in line.split() if is_float(s)]
        #list only numeric

        if len(colors) == 3: #append to list if fully rgb
            li_rgb.append(colors)

    if flag_reverse:
        li_rgb = list(reversed(li_rgb))

    data = np.array(li_rgb)
    data = data / np.max(data)
    cmap = ListedColormap(data, name=name)
    return cmap

