#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# cython:language_level=3
'''
@File    :   math.py
@Project :
@Time    :   2023/9/25 9:02
@Author  :   Yifei WANG
@Version :
@python  :   v3.10
@Contact :   mail:yifeiwang@amecnsh.com  tel:3445
@Desc    :
'''

import numpy as np
import math
from scipy import optimize
import scipy.signal as signal
from scipy.signal import savgol_filter


# =========================== Geometry.circle ===========================
def point_center_dist(x, y, xc, yc):
    """
    Compute the distance between every point on the circle to the circle center
    Parameters
    ----------
    x : numeric
        x coordination of the real points
    y : numeric
        y coordination of the real points
    xc : numeric
        x coordination of the center
    yc : numeric
        y coordination of the center
    Returns
    -------
    distance: array-like
        the distance between every point on the circle to the circle center
    """
    return np.sqrt((x - xc) ** 2 + (y - yc) ** 2)


def lsq_cost(c, x, y):  # cost function
    Ri = point_center_dist(x, y, c[0], c[1])
    return np.square(Ri - Ri.mean())


def least_squares_circle(coords):  # core code
    """
    fit the least_squares_circle of given graph
    @param coords:
    @return:
    """
    # print("least start")
    if isinstance(coords, np.ndarray):
        x = coords[:, 0]
        y = coords[:, 1]
    elif isinstance(coords, list):
        x = np.array([point[0] for point in coords])
        y = np.array([point[1] for point in coords])
    else:
        raise Exception("Parameter 'coords' is an unsupported type: " + str(type(coords)))
    # coordinates of the barycenter
    x_m = np.mean(x)
    y_m = np.mean(y)
    center_estimate = np.array([x_m, y_m])
    # noinspection PyTupleAssignmentBalance
    center, _ = optimize.leastsq(lsq_cost, center_estimate, args=(x, y))
    xc, yc = center
    Ri = point_center_dist(x, y, *center)
    R = Ri.mean()
    diffs = Ri - R
    # print("diffs:", len(diffs))
    residual = np.sqrt(np.sum(diffs ** 2) / len(Ri))  # 针对整体
    # residual = 1-(np.std(Ri - R) / R) # 针对
    # roundness = residual/R
    # max_idx = [np.argmax(diffs), np.argmin(diffs)]
    diffs_ = np.append(diffs, diffs[:50])
    # print("diffs:", diffs_[:10])
    diffs_ = savgol_filter(diffs_, 50, 5)
    # print("diffs_:", diffs_[:10])
    peaks_, _ = signal.find_peaks(diffs_, height=0, prominence=3, distance=30)
    # print("peaks:", peaks_)
    # plt.plot(diffs_)
    if len(peaks_) > 0:
        for i in range(len(peaks_)):
            if peaks_[i] > len(coords) + 2:
                peaks_[i] = peaks_[i] - len(coords)
        # plt.plot(peaks_, diffs_[peaks_], 'o', color="red", markersize=5)
        bad_points = coords[peaks_]
        # print("diffs[peaks_]:", coords[peaks_])
    else:
        bad_points = []
    # bad_points = []

    return xc, yc, R, residual, bad_points, diffs_

    # print('badpoint:', coords[max_idx])


def coord2angel(ps):
    a = ps[0]
    b = ps[1]
    c = (a[1] - b[1]) / np.absolute(a[0] - b[0])
    return math.atan(c) * 180 / math.pi


# ========================== Coordinate transformer ==============================
def rec2polar(x, y, x_c, y_c):
    theta = math.atan2(y - y_c, x - x_c) * -1
    dist = np.sqrt((x - x_c) ** 2 + (y - y_c) ** 2)
    return theta, dist


def polar_converter(x, y, x_c, y_c):
    theta = math.atan2(y - y_c, x - x_c) * -1
    d = np.sqrt((x - x_c) ** 2 + (y - y_c) ** 2)
    return theta, d


def polar2rec(theta, dist, x_c, y_c):
    rec_x = int(x_c + dist * np.cos(theta))
    rec_y = int(y_c - dist * np.sin(theta))
    return rec_x, rec_y


def contour2coords(contour):
    x_ = [[xi[0][0]] for xi in contour]
    y_ = [[yi[0][1]] for yi in contour]
    coords = np.array([[x_[k][0], y_[k][0]] for k in range(len(x_))])
    return coords


def coords2contour(coords):
    contour = [[[int(c[0]), int(c[1])]] for c in coords]
    return np.array(contour)


def image_flater(image, x_c, y_c, r_o=1200, r_i=400):
    height = int(r_o * np.pi * 2)
    width = r_o - r_i

    rectangle = np.zeros([width, height])
    for row in range(width):
        for col in range(height):
            # 转成极坐标系
            theta = np.pi * 2.0 / height * (col + 1)
            rho = r_o - row - 1
            # 以圆心为原点，求得原来圆环对应的坐标
            position_x = int(x_c + rho * np.cos(theta) + 0.5)
            position_y = int(y_c - rho * np.sin(theta) + 0.5)
            rectangle[row, col] = image[position_y, position_x]
    # 要转回np.uint8型数据，否则显示有问题
    rectangle = np.uint8(rectangle)
    # image_show_plt(rectangle)
    return rectangle


def plot_polar_flat(cnt, x_c, y_c, ax, **kwargs):
    x_ = [[xi[0][0]] for xi in cnt]
    y_ = [[yi[0][1]] for yi in cnt]
    coords = np.array([[x_[k][0], y_[k][0]] for k in range(len(x_))])
    #     M = cv.moments(c)  # step moments of contours
    #     geo_center_x_org = M['m10'] / M['m00']
    #     geo_center_y_org = M['m01'] / M['m00']
    ds = []
    thetas = []
    for co in coords:
        theta, d = polar_converter(co[0], co[1], x_c, y_c)
        thetas.append(theta)
        ds.append(d)
    ax.plot(thetas, ds, **kwargs)
