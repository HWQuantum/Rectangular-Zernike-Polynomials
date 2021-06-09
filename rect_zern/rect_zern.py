"""Main module."""
import numpy as np
from typing import List, Tuple, Generator, Callable, Iterable


def radial_coeff(m: int, n: int, l: int) -> int:
    '''Radial coefficient in the sum for the radial part of the Zernike polynomial
    '''
    if (n - m) % 2 == 0:
        return int(
            ((np.power(-1, l) * np.math.factorial(n - l)) /
             (np.math.factorial(l) * np.math.factorial(0.5 * (n + m) - l) *
              np.math.factorial(0.5 * (n - m) - l))))
    else:
        return 0


def radial(m: int, n: int) -> List[Tuple[int, int]]:
    '''Radial part of the Zernike polynomial
    '''
    return [(radial_coeff(m, n, l), n - 2 * l)
            for l in range(0,
                           int(round((n - m) / 2)) + 1)]


def coefficients(n: int) -> Generator[Tuple[int, int], None, None]:
    '''Generate the first n non-zero Zernike coefficient indices
    ie: (0, 0), (-1, 1), (1, 1), (-2, 2), (0, 2), (2, 2), ...
    '''
    c = 0
    i, j = 0, 0
    while c < n:
        c += 1
        yield (i, j)
        if i == j:
            j += 1
            i = -j
        else:
            i += 2


def zernike_cartesian(
        m: int, n: int) -> Callable[[np.ndarray, np.ndarray], np.ndarray]:
    '''Returns a function to get the Zernike polynomial in cartesian coordinates
    '''
    abs_m = np.abs(m)
    rs = [(i, j) for (i, j) in radial(abs_m, n) if i != 0]
    if m == 0:
        norm = np.sqrt(n + 1)
    else:
        norm = np.sqrt(2 * (n + 1))
    if m < 0:

        def poly(x, y):
            r = np.sqrt(x**2 + y**2)
            theta = np.arctan2(y, x)
            return norm * np.sum([i * np.power(r, j) for (i, j) in rs],
                                 axis=0) * np.sin(abs_m * theta)

        return poly
    else:

        def poly(x, y):
            r = np.sqrt(x**2 + y**2)
            theta = np.arctan2(y, x)
            return norm * np.sum([i * np.power(r, j) for (i, j) in rs],
                                 axis=0) * np.cos(abs_m * theta)

        return poly


def rect_coords(w: int, h: int) -> Tuple[np.ndarray, np.ndarray]:
    """Get the rectangle coordinates with area pi for the given width and height
    Returns a numpy array with the correct coordinates
    """
    ratio = w / h
    norm_h = np.sqrt(np.pi / ratio)
    norm_w = norm_h * ratio
    x, y = np.mgrid[-norm_w / 2:norm_w / 2:w * 1j,
                    -norm_h / 2:norm_h / 2:h * 1j]
    return x, y


def gram_schmidt(modes: Iterable[Callable[[np.ndarray, np.ndarray],
                                          np.ndarray]], x: np.ndarray,
                 y: np.ndarray) -> List[np.ndarray]:
    """Perform a gram-schmidt orthonormalisation over the given modes. 
    The modes should be functions which operate like modes[i](x, y)
    Returns a list of numpy array modes.
    """
    mode_rep = [m(x, y) for m in modes]
    new_modes = []
    for i in range(len(mode_rep)):
        m = mode_rep[i] - sum(np.sum(m * mode_rep[i]) for m in new_modes[:i])
        new_modes.append(m)

    return [m / (np.sqrt(np.pi * np.sum(m * m))) for m in new_modes]


def rectangular_zernike_modes(
        n_modes: int, w: int,
        h: int) -> Tuple[List[np.ndarray], np.ndarray, np.ndarray]:
    """Given a number of modes to generate, a width and a height return a list containing 
    the modes, and the coordinates over which they're represented.
    """
    x, y = rect_coords(w, h)
    modes = [zernike_cartesian(*c) for c in coefficients(n_modes)]
    g_s = gram_schmidt(modes, x, y)
    return g_s, x, y
