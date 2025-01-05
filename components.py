from PyQt5.QtWidgets import QSpacerItem, QSizePolicy


def spacer():
    return QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Expanding)


def hspacer():
    return QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
