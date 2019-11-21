from Cython.Build import cythonize
from distutils.core import setup, Extension

setup(
    name = "Flight-App",
    ext_modules = cythonize("Program_Controller.py")
i)
