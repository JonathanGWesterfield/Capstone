# import sys
# import time
#
# import numpy as np
#
# from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
# if is_pyqt5():
#     from matplotlib.backends.backend_qt5agg import (
#         FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
# else:
#     from matplotlib.backends.backend_qt4agg import (
#         FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
# from matplotlib.figure import Figure
#
#
# class ApplicationWindow(QtWidgets.QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self._main = QtWidgets.QWidget()
#         self.setCentralWidget(self._main)
#         layout = QtWidgets.QVBoxLayout(self._main)
#
#         static_canvas = FigureCanvas(Figure(figsize=(5, 3)))
#         layout.addWidget(static_canvas)
#         self.addToolBar(NavigationToolbar(static_canvas, self))
#
#         dynamic_canvas = FigureCanvas(Figure(figsize=(5, 3)))
#         layout.addWidget(dynamic_canvas)
#         self.addToolBar(QtCore.Qt.BottomToolBarArea,
#                         NavigationToolbar(dynamic_canvas, self))
#
#         self._static_ax = static_canvas.figure.subplots()
#         t = np.linspace(0, 10, 501)
#         self._static_ax.plot(t, np.tan(t), ".")
#
#         self._dynamic_ax = dynamic_canvas.figure.subplots()
#         self._timer = dynamic_canvas.new_timer(
#             100, [(self._update_canvas, (), {})])
#         self._timer.start()
#
#     def _update_canvas(self):
#         self._dynamic_ax.clear()
#         t = np.linspace(0, 10, 101)
#         # Shift the sinusoid as a function of time.
#         self._dynamic_ax.plot(t, np.sin(t + time.time()))
#         self._dynamic_ax.figure.canvas.draw()
#
#
#
# if __name__ == "__main__":
#     qapp = QtWidgets.QApplication(sys.argv)
#     app = ApplicationWindow()
#     app.show()
#     qapp.exec_()

import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

from mpl_toolkits.mplot3d.axes3d import get_test_data
# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import


# set up a figure twice as wide as it is tall
fig = plt.figure(figsize=plt.figaspect(0.5))

#===============
#  First subplot
#===============
# set up the axes for the first plot
ax = fig.add_subplot(1, 2, 1, projection='3d')

# plot a 3D surface like in the example mplot3d/surface3d_demo
X = np.arange(-5, 5, 0.25)
Y = np.arange(-5, 5, 0.25)
X, Y = np.meshgrid(X, Y)
R = np.sqrt(X**2 + Y**2)
Z = np.sin(R)
surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
ax.set_zlim(-1.01, 1.01)
fig.colorbar(surf, shrink=0.5, aspect=10)

#===============
# Second subplot
#===============
# set up the axes for the second plot
ax = fig.add_subplot(1, 2, 2, projection='3d')

# plot a 3D wireframe like in the example mplot3d/wire3d_demo
X, Y, Z = get_test_data(0.05)
ax.plot_wireframe(X, Y, Z, rstride=10, cstride=10)

plt.show()