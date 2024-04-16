from PIL import Image

import numpy
import cv2

FPS = 25
GENS = 1
GEN_FRAMES = 50

black = Image.new("RGB", (1920, 1080), (0, 0, 0))
video = cv2.VideoWriter("video.mp4", cv2.VideoWriter_fourcc(*'mp4v'), FPS, (1920, 1080))

points = [(100, 540), (1820, 540)]
points_new = []

def progress_point(a: tuple, b: tuple, progress: int):
    return (a[0] * progress + b[0] * (1 - progress), a[1] * progress + b[1] * (1 - progress))

def gen_bump(a, b, length):
    global points_new
    length *= 1/3
    direction = {}

    p1 = (
        (a[1] > b[1]) * length - (a[1] < b[1]) * length,
        (a[0] > b[0]) * length - (a[0] < b[0]) * length
    )
    points_new.append(p1)
    points_new.append(
        p1[0] + b[0] - a[0],
        p1[1] + b[1] - a[1]
    )

for generation in range(GENS):
    for point in range(len(points - 1)):
        points.append(points[point]) #point itself
        base_1 = progress_point( #first peak of protrusion
            points[point],
            points[point + 1],
            1/3
        )
        points.append(progress_point( #first base of protrusion
            points[point],
            base_1,
            1/2
        ))
        points.append(base_1)
        base_2 = progress_point( #second peak of protrustion
            points[point],
            points[point + 1],
            2/3
        )
        points.append(base_2)
        points.append(progress_point( #second base of protrustion
            base_2,
            points[point + 1]
        ))

        points_new.append(points[point])
        points_new.append(base_1)
        gen_bump(base_1, base_2)
        points_new.append(base_2)
        
    for frame in range(GEN_FRAMES):
        pass

video.release()
