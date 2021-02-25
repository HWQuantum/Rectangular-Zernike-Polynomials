===============================
Rectangular Zernike Polynomials
===============================


Generate orthogonal zernike polynomials over a rectangle


* Free software: MIT license
* Documentation: https://rect-zern.readthedocs.io.

Example
-------

To generate 10 modes over a rectangular with width 200 and height 300:

.. code:: python

    import rect_zern as rz
    modes, x, y = rz.rectangular_zernike_modes(10, 200, 300)
