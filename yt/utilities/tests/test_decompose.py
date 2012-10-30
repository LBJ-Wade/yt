"""
Test suite for cartesian domain decomposition.

Author: Kacper Kowalik <xarthisius.kk@gmail.com>
Affiliation: CA UMK
Homepage: http://yt-project.org/
License:
  Copyright (C) 2012 Kacper Kowalik. All Rights Reserved.

  This file is part of yt.

  yt is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from yt.testing import assert_array_equal, assert_almost_equal
import numpy as np
import yt.utilities.decompose as dec


def setup():
    pass


def test_psize_2d():
    procs = dec.get_psize(np.array([5, 1, 7]), 6)
    assert_array_equal(procs, np.array([3, 1, 2]))
    procs = dec.get_psize(np.array([1, 7, 5]), 6)
    assert_array_equal(procs, np.array([1, 2, 3]))
    procs = dec.get_psize(np.array([7, 5, 1]), 6)
    assert_array_equal(procs, np.array([2, 3, 1]))


def test_psize_3d():
    procs = dec.get_psize(np.array([33, 35, 37]), 12)
    assert_array_equal(procs, np.array([3, 2, 2]))


def test_decomposition_2d():
    array = np.ones((7, 5, 1))
    bbox = np.array([[-0.7, 0.0], [1.5, 2.0], [0.0, 0.7]])
    ledge, redge, data = dec.decompose_array(array, np.array([2, 3, 1]), bbox)

    assert_array_equal(data[1].shape, np.array([3, 2, 1]))

    gold_le = np.array([
                       [-0.7, 1.5, 0.0], [-0.7, 1.6, 0.0],
                       [-0.7, 1.8, 0.0], [-0.4, 1.5, 0.0],
                       [-0.4, 1.6, 0.0], [-0.4, 1.8, 0.0]
                       ])
    assert_almost_equal(ledge, gold_le, 8)

    gold_re = np.array(
        [[-0.4, 1.6, 0.7], [-0.4, 1.8, 0.7],
         [-0.4, 2.0, 0.7], [0.0, 1.6, 0.7],
         [0.0, 1.8, 0.7], [0.0, 2.0, 0.7]]
    )
    assert_almost_equal(redge, gold_re, 8)


def test_decomposition_3d():
    array = np.ones((33, 35, 37))
    bbox = np.array([[0., 1.0], [-1.5, 1.5], [1.0, 2.5]])

    ledge, redge, data = dec.decompose_array(array, np.array([3, 2, 2]), bbox)
    assert_array_equal(data[0].shape, np.array([11, 17, 18]))

    gold_le = np.array(
        [[0.00000, -1.50000, 1.00000], [0.00000, -1.50000, 1.72973],
         [0.00000, -0.04286, 1.00000], [0.00000, -0.04286, 1.72973],
         [0.33333, -1.50000, 1.00000], [0.33333, -1.50000, 1.72973],
         [0.33333, -0.04286, 1.00000], [0.33333, -0.04286, 1.72973],
         [0.66667, -1.50000, 1.00000], [0.66667, -1.50000, 1.72973],
         [0.66667, -0.04286, 1.00000], [0.66667, -0.04286, 1.72973]]
    )
    assert_almost_equal(ledge, gold_le, 5)

    gold_re = np.array(
        [[0.33333, -0.04286, 1.72973], [0.33333, -0.04286, 2.50000],
         [0.33333, 1.50000, 1.72973], [0.33333, 1.50000, 2.50000],
         [0.66667, -0.04286, 1.72973], [0.66667, -0.04286, 2.50000],
         [0.66667, 1.50000, 1.72973], [0.66667, 1.50000, 2.50000],
         [1.00000, -0.04286, 1.72973], [1.00000, -0.04286, 2.50000],
         [1.00000, 1.50000, 1.72973], [1.00000, 1.50000, 2.50000]]
    )
    assert_almost_equal(redge, gold_re, 5)