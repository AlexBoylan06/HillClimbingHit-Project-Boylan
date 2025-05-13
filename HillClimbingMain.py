import math

from NoisyFunctionFile import NoisyFunction
import cv2
import numpy as np
from typing import Tuple, List
import random

NUM_CLIMBERS = 15
WINDOW_SIZE = 700

MODE_GREEDY = 0
MODE_ANNEALING = 1

def main():
    global mode
    mode = MODE_GREEDY
    nf = NoisyFunction(WINDOW_SIZE)
    actual_max, actual_max_pt = nf.actual_max()
    color_frame = cv2.cvtColor(nf.to_ndarray(), cv2.COLOR_GRAY2RGB)
    cv2.imshow("original", color_frame)
    cv2.waitKey(1)
    best_value = 0
    best_pt = (nf.get_size()/2, nf.get_size()/2)
    stopping_points = []
    total_steps = 0
    for i in range(NUM_CLIMBERS):
        stops, pt = climb_hill_to_max(nf)
        print(f"{pt} by way of {stops}")

        clr = (random.randint(0, 196), random.randint(0, 196), random.randint(0, 196))
        if len(stops) > 0:
            p1 = stops[0]
            for j in range(1, len(stops)):
                p2 = stops[j]
                cv2.line(color_frame, pt1=(p1[1], p1[0]), pt2=(p2[1], p2[0]), color=clr, thickness=1)
                p1 = p2

        stopping_points.append(pt)
        total_steps += len(stops)
        if nf.get_value_at_point(pt) > best_value:
            best_value = nf.get_value_at_point(pt)
            best_pt = pt
    num_at_best_point = 0
    num_at_actual_point = 0
    for pt in stopping_points:
        cv2.circle(color_frame, center=(pt[1], pt[0]), radius=7, color=(255, 0, 0), thickness=-1)
        if pt == best_pt:
            num_at_best_point += 1
        if pt == actual_max_pt:
            num_at_actual_point += 1
        cv2.putText(color_frame, f"{num_at_best_point}", (best_pt[1] - 4, best_pt[0] + 4), cv2.FONT_HERSHEY_PLAIN, 0.75,
                    (255, 255, 0))
    if best_pt is not None:
        cv2.line(color_frame, pt1=(best_pt[1] - 10, best_pt[0]), pt2=(best_pt[1] - 15, best_pt[0]), color=(0, 0, 0),
                 thickness=2)
        cv2.line(color_frame, pt1=(best_pt[1] + 10, best_pt[0]), pt2=(best_pt[1] + 15, best_pt[0]), color=(0, 0, 0),
                 thickness=2)
        cv2.line(color_frame, pt1=(best_pt[1], best_pt[0] - 10), pt2=(best_pt[1], best_pt[0] - 15), color=(0, 0, 0),
                 thickness=2)
        cv2.line(color_frame, pt1=(best_pt[1], best_pt[0] + 10), pt2=(best_pt[1], best_pt[0] + 15), color=(0, 0, 0),
                 thickness=2)

    print(f"I found the best value = {best_value} at {best_pt}")
    print(f"The actual best value  = {actual_max} at {actual_max_pt}.")
    print(f"{int(num_at_actual_point / NUM_CLIMBERS * 100)}% of the {NUM_CLIMBERS} stopping points were close to the actual location.")
    print(f"It took an average of {total_steps / len(stopping_points)} steps to reach these points.")
    # draw "X" around actual max point.
    cv2.line(color_frame, pt1=(actual_max_pt[1] - 8, actual_max_pt[0] - 8),
             pt2=(actual_max_pt[1] - 12, actual_max_pt[0] - 12), color=(0, 0, 0,), thickness=2)
    cv2.line(color_frame, pt1=(actual_max_pt[1] + 8, actual_max_pt[0] + 8),
             pt2=(actual_max_pt[1] + 12, actual_max_pt[0] + 12), color=(0, 0, 0,), thickness=2)
    cv2.line(color_frame, pt1=(actual_max_pt[1] + 8, actual_max_pt[0] - 8),
             pt2=(actual_max_pt[1] + 12, actual_max_pt[0] - 12), color=(0, 0, 0,), thickness=2)
    cv2.line(color_frame, pt1=(actual_max_pt[1] - 8, actual_max_pt[0] + 8),
             pt2=(actual_max_pt[1] - 12, actual_max_pt[0] + 12), color=(0, 0, 0,), thickness=2)

    cv2.imshow("discovery", color_frame)
    cv2.moveWindow("discovery", nf.get_size(), 0)
    cv2.waitKey(0)

def in_bounds(pt:Tuple[int, int])-> bool:
   return pt[0]>-1 and pt[1]>-1 and pt[0]<WINDOW_SIZE and pt[1]<WINDOW_SIZE

def climb_hill_to_max(func:NoisyFunction) -> Tuple[List[Tuple[int, int]],Tuple[int,int]]:
    """
    starting at a random location, finds a (local?) maximum.
    :param func: the function that determines the "value" (height) of a given (row, col).
    :return: a found location with a (local?) maximum
    """
    pt = (random.randint(0, func.get_size()), random.randint(0, func.get_size()))
    stops: List[Tuple[int, int]] = []

    relative_steps = [(0,1), (1,0), (0,-1), (-1,0)]
    should_keep_checking = True
    while should_keep_checking:
        stops.append(pt)
        val_to_beat = func.get_value_at_point(pt)
        should_keep_checking = False  # assume we don't find a worthwhile step to make...
        random.shuffle(relative_steps)
        for delta in relative_steps:
            temp_pt = (pt[0]+delta[0], pt[1]+delta[1])
            if not in_bounds(temp_pt):
                continue
            if func.get_value_at_point(temp_pt) > val_to_beat:
                pt = temp_pt
                should_keep_checking = True  # we took a step, so keep looking.
                break

    # if we got here, then after our last move, none of the four directions showed an improvement.
    return stops, pt

if __name__ == "__main__":
    main()