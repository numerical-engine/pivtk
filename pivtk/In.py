import numpy as np
from pivtk import geom

def read(filename:str):
    with open(filename, "r") as file:
        lines = file.readlines()[3:]
    
    data_type = lines[0].split(" ")[-1][:-1]
    if data_type == "UNSTRUCTURED_GRID":
        return read_UnstructuredGrid(lines[1:])
    else:
        raise NotImplementedError

def read_UnstructuredGrid(lines:list[str]):
    current_idx = 0
    point_num = int(lines[current_idx].split(" ")[1])
    current_idx += 1

    points = []
    for _ in range(point_num):
        points.append(np.array([float(s) for s in lines[current_idx].split(" ")]))
        current_idx += 1
    points = np.stack(points)

    cell_num = int(lines[current_idx].split(" ")[1])
    current_idx += 1

    cells = []
    for _ in range(cell_num):
        indice = np.array([int(l) for l in lines[current_idx].split(" ")[1:]])
        cells.append({"indice":indice})
        current_idx += 1
    current_idx += 1 #skip "CELL_TYPES ** line"
    for i in range(cell_num):
        cells[i]["type"] = int(lines[current_idx])
        current_idx += 1
    
    return geom.unstructured_grid(points, cells)
    ###TODO read point data and cell data