#-----------------------------------------------------------
# Copyright (C) 2020 Raymond Nijssen
#-----------------------------------------------------------
# Licensed under the terms of GNU GPL 2
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#---------------------------------------------------------------------

#from value_painter import ValuePainter
from PyQt5.QtWidgets import QAction, QMessageBox

from .value_painter import ValuePainter

def classFactory(iface):
    return ValuePainter(iface)
