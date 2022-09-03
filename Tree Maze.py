import queue
import time
import tkinter
from tkinter import Tk, Canvas, Frame, BOTH
import random

root = Tk()
frame = Frame(root)
canvas = Canvas(frame)
frame.pack(fill=BOTH, expand=1)
curr_spot = -1
gap = 15
shift = 10


class node:
    north: bool
    west: bool
    north_line: int
    west_line: int
    distance: int
    prev: (int, int)
    rectangle: int

    def __init__(self):
        self.north = False
        self.west = False
        self.north_line = False
        self.west_line = False
        self.distance = -1
        self.prev = None


def display_maze(maze_arr, loc):
    global canvas, curr_spot

    for widget in frame.winfo_children():
        widget.destroy()
    canvas = Canvas(frame)
    canvas.create_line(-1 * gap + shift + gap, 0 * gap + shift,
                       -1 * gap + shift + gap, len(maze_arr[0]) * gap + shift)
    canvas.create_line(-1 * gap + shift + gap, len(maze_arr[0]) * gap + shift,
                       len(maze_arr) * gap + shift,
                       len(maze_arr[0]) * gap + shift)

    for i, lst in enumerate(maze_arr):
        for j, node in enumerate(lst):
            if not node.west:
                node.west_line = canvas.create_line(i * gap + shift + gap,
                                                    j * gap + shift,
                                                    i * gap + shift + gap,
                                                    j * gap + shift + gap)
            if not node.north:
                node.north_line = canvas.create_line(i * gap + shift,
                                                     j * gap + shift,
                                                     i * gap + shift + gap,
                                                     j * gap + shift)
    curr_spot = canvas.create_rectangle(loc[0] * gap + shift,
                                        loc[1] * gap + shift,
                                        loc[0] * gap + shift + gap,
                                        loc[1] * gap + shift + gap, fill="red")
    # canvas.create_rectangle(0, 0, 100, 100, fill= "red")
    canvas.pack(fill=BOTH, expand=1)

    root.geometry("1000x1000+10+10")
    root.update()


def create_maze_move(n: int):
    global curr_spot
    maze_arr = []
    for i in range(n):
        maze_arr.append([])
        for j in range(n):
            temp = node()
            maze_arr[i].append(temp)

    que = []
    unavaliable = {(-1, -1)}
    que.append((0, 0, -1))
    display_maze(maze_arr, (0, 0))

    while len(que) != 0:
        res = random.randint(0, 10)
        if res < 11:
            curr = que.pop()
        else:
            curr = random.choice(que)
            que.remove(curr)
        if (curr[0], curr[1]) in unavaliable:
            continue
        unavaliable.add((curr[0], curr[1]))
        poss = []

        if curr[2] == 0:
            maze_arr[curr[0]][curr[1]].west = True
            canvas.delete(maze_arr[curr[0]][curr[1]].west_line)
        elif curr[2] == 1:
            maze_arr[curr[0] - 1][curr[1]].west = True
            canvas.delete(maze_arr[curr[0] - 1][curr[1]].west_line)
        elif curr[2] == 2:
            maze_arr[curr[0]][curr[1] + 1].north = True
            canvas.delete(maze_arr[curr[0]][curr[1] + 1].north_line)
        elif curr[2] == 3:
            maze_arr[curr[0]][curr[1]].north = True
            canvas.delete(maze_arr[curr[0]][curr[1]].north_line)

        if curr[0] != 0 and (curr[0] - 1, curr[1]) not in unavaliable:
            poss.append((curr[0] - 1, curr[1], 0))
        if curr[0] != n - 1 and (curr[0] + 1, curr[1]) not in unavaliable:
            poss.append((curr[0] + 1, curr[1], 1))
        if curr[1] != 0 and (curr[0], curr[1] - 1) not in unavaliable:
            poss.append((curr[0], curr[1] - 1, 2))
        if curr[1] != n - 1 and (curr[0], curr[1] + 1) not in unavaliable:
            poss.append((curr[0], curr[1] + 1, 3))
        # print(curr, poss)
        random.shuffle(poss)
        for coor in poss:
            que.append(coor)
        canvas.delete(curr_spot)
        curr_spot = canvas.create_rectangle(curr[0] * gap + shift,
                                            curr[1] * gap + shift,
                                            curr[0] * gap + shift + gap,
                                            curr[1] * gap + shift + gap,
                                            fill="red")

        root.update()
        time.sleep(0.002)
    display_maze(maze_arr, (-1, -1))
    canvas.delete(curr_spot)
    return maze_arr


def possibleTravel(coor: (int, int), maze_arr: list[list[node]]):
    lst = []
    if coor[0] != 0 and maze_arr[coor[0] - 1][coor[1]].west and \
            maze_arr[coor[0] - 1][coor[1]].distance == -1:
        lst.append((coor[0] - 1, coor[1]))
    if coor[0] != len(maze_arr) - 1 and maze_arr[coor[0]][coor[1]].west and \
            maze_arr[coor[0] + 1][coor[1]].distance == -1:
        lst.append((coor[0] + 1, coor[1]))
    if coor[1] != 0 and maze_arr[coor[0]][coor[1]].north and maze_arr[coor[0]][
        coor[1] - 1].distance == -1:
        lst.append((coor[0], coor[1] - 1))
    if coor[1] != len(maze_arr[0]) - 1 and maze_arr[coor[0]][
        coor[1] + 1].north and maze_arr[coor[0]][coor[1] + 1].distance == -1:
        lst.append((coor[0], coor[1] + 1))
    return lst


def solve_maze_A(start: (int, int), end: (int, int),
                 maze_arr: list[list[node]]):
    stack = [start]
    maze_arr[start[0]][start[1]].distance = 0
    key = lambda x: -(maze_arr[x[0]][x[1]].distance + abs(end[0] - x[0]) + abs(end[1] - x[1]))
    while stack:
        curr = stack.pop()

        curr_node = maze_arr[curr[0]][curr[1]]

        curr_node.rectangle = canvas.create_rectangle(curr[0] * gap + shift + 1,
                                                      curr[1] * gap + shift + 1,
                                                      curr[
                                                          0] * gap + shift + gap - 1,
                                                      curr[
                                                          1] * gap + shift + gap - 1,
                                                      fill="grey")
        if curr == end:
            break
        for poss in possibleTravel(curr, maze_arr):
            maze_arr[poss[0]][poss[1]].distance = curr_node.distance + 1
            maze_arr[poss[0]][poss[1]].prev = curr
            stack.append(poss)
        #time.sleep(0.0005)
        root.update()
        stack.sort(key=key)
    curr = maze_arr[end[0]][end[1]]

    while True:
        time.sleep(0.003)
        canvas.itemconfig(curr.rectangle, fill='green')
        if curr.prev is None:
            break
        curr = maze_arr[curr.prev[0]][curr.prev[1]]
        root.update()

n = 40
for i in range(4, 30):
    solve_maze_A((0, 0), (n - 1, n - 1), create_maze_move(n))
