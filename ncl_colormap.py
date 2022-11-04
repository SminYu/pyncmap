#%%
import numpy as np
from matplotlib.colors import ListedColormap

def cmap(name):
    if name.endswith('_r'):
        name = name[:-2]
        flag_reverse = True
    else:
        flag_reverse = False

    f = open('cmap_data/{}.rgb'.format(name), 'r')
    lines = f.readlines()
    lines = list(map(lambda s: s.strip('\n'), lines))

    flag_ncolor  = False
    flag_rgb = False
    li_rgb = []
    for i in range(len(lines)):
        line = lines[i]
        if line.startswith('ncolors'):
            flag_ncolor = True
        
        if line.startswith('#') & flag_ncolor:
            flag_rgb = True
        
        if flag_rgb:
            li_rgb.append([int(s) for s in line.split() if s.isdigit()])

    li_rgb = li_rgb[1:]

    if flag_reverse:
        li_rgb = list(reversed(li_rgb))

    data = np.array(li_rgb)
    data = data / np.max(data)
    cmap = ListedColormap(data, name=name)
    return cmap

