# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PS2MSGUI.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QScrollArea, QSizePolicy, QSpacerItem, QTabWidget,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(670, 520)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QSize(670, 520))
        Form.setMaximumSize(QSize(6500, 2000))
        self.verticalLayout_2 = QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.tabWidget = QTabWidget(Form)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setEnabled(True)
        self.tabWidget.setMinimumSize(QSize(603, 480))
        self.tabWidget.setMaximumSize(QSize(6030, 5000))
        self.tabWidget.setDocumentMode(False)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        sizePolicy.setHeightForWidth(self.tab.sizePolicy().hasHeightForWidth())
        self.tab.setSizePolicy(sizePolicy)
        self.tab.setMinimumSize(QSize(603, 450))
        self.tab.setMaximumSize(QSize(6030, 4500))
        self.verticalLayout = QVBoxLayout(self.tab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(self.tab)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy1)
        self.groupBox.setMinimumSize(QSize(580, 70))
        self.groupBox.setMaximumSize(QSize(5800, 700))
        font = QFont()
        font.setBold(True)
        self.groupBox.setFont(font)
        self.horizontalLayout = QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, -1, 11, -1)
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setBold(False)
        self.label.setFont(font1)

        self.horizontalLayout.addWidget(self.label)

        self.lineEdit = QLineEdit(self.groupBox)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMaximumSize(QSize(120, 26))

        self.horizontalLayout.addWidget(self.lineEdit)

        self.pushButton = QPushButton(self.groupBox)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout.addWidget(self.pushButton)

        self.pushButton_3 = QPushButton(self.groupBox)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout.addWidget(self.pushButton_3)

        self.pushButton_6 = QPushButton(self.groupBox)
        self.pushButton_6.setObjectName(u"pushButton_6")

        self.horizontalLayout.addWidget(self.pushButton_6)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_13)


        self.verticalLayout.addWidget(self.groupBox)

        self.groupBox_3 = QGroupBox(self.tab)
        self.groupBox_3.setObjectName(u"groupBox_3")
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setMinimumSize(QSize(580, 140))
        self.groupBox_3.setMaximumSize(QSize(5800, 1200))
        self.groupBox_3.setFont(font)
        self.gridLayout = QGridLayout(self.groupBox_3)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(7)
        self.gridLayout.setContentsMargins(-1, -1, -1, 11)
        self.label_136 = QLabel(self.groupBox_3)
        self.label_136.setObjectName(u"label_136")
        font2 = QFont()
        font2.setPointSize(8)
        font2.setBold(False)
        self.label_136.setFont(font2)

        self.gridLayout.addWidget(self.label_136, 2, 0, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_7, 0, 5, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_6, 0, 2, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(18, 19, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_5, 2, 8, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(18, 19, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_4, 0, 8, 1, 1)

        self.comboBox_13 = QComboBox(self.groupBox_3)
        self.comboBox_13.addItem("")
        self.comboBox_13.addItem("")
        self.comboBox_13.addItem("")
        self.comboBox_13.addItem("")
        self.comboBox_13.setObjectName(u"comboBox_13")
        self.comboBox_13.setMaximumSize(QSize(50, 22))

        self.gridLayout.addWidget(self.comboBox_13, 0, 7, 1, 1)

        self.lineEdit_113 = QLineEdit(self.groupBox_3)
        self.lineEdit_113.setObjectName(u"lineEdit_113")
        self.lineEdit_113.setMaximumSize(QSize(50, 22))

        self.gridLayout.addWidget(self.lineEdit_113, 2, 4, 1, 1)

        self.label_133 = QLabel(self.groupBox_3)
        self.label_133.setObjectName(u"label_133")
        self.label_133.setFont(font2)

        self.gridLayout.addWidget(self.label_133, 0, 3, 1, 1)

        self.lineEdit_114 = QLineEdit(self.groupBox_3)
        self.lineEdit_114.setObjectName(u"lineEdit_114")
        self.lineEdit_114.setMaximumSize(QSize(50, 22))

        self.gridLayout.addWidget(self.lineEdit_114, 2, 1, 1, 1)

        self.label_134 = QLabel(self.groupBox_3)
        self.label_134.setObjectName(u"label_134")
        self.label_134.setFont(font2)

        self.gridLayout.addWidget(self.label_134, 0, 0, 1, 1)

        self.lineEdit_111 = QLineEdit(self.groupBox_3)
        self.lineEdit_111.setObjectName(u"lineEdit_111")
        self.lineEdit_111.setMaximumSize(QSize(50, 22))

        self.gridLayout.addWidget(self.lineEdit_111, 0, 1, 1, 1)

        self.label_132 = QLabel(self.groupBox_3)
        self.label_132.setObjectName(u"label_132")
        self.label_132.setFont(font2)

        self.gridLayout.addWidget(self.label_132, 0, 6, 1, 1)

        self.lineEdit_112 = QLineEdit(self.groupBox_3)
        self.lineEdit_112.setObjectName(u"lineEdit_112")
        self.lineEdit_112.setMaximumSize(QSize(50, 22))

        self.gridLayout.addWidget(self.lineEdit_112, 0, 4, 1, 1)

        self.label_135 = QLabel(self.groupBox_3)
        self.label_135.setObjectName(u"label_135")
        self.label_135.setFont(font2)

        self.gridLayout.addWidget(self.label_135, 2, 3, 1, 1)

        self.label_2 = QLabel(self.groupBox_3)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font1)

        self.gridLayout.addWidget(self.label_2, 2, 6, 1, 1)

        self.comboBox = QComboBox(self.groupBox_3)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setMaximumSize(QSize(50, 16777215))

        self.gridLayout.addWidget(self.comboBox, 2, 7, 1, 1)

        self.lineEdit_7 = QLineEdit(self.groupBox_3)
        self.lineEdit_7.setObjectName(u"lineEdit_7")
        self.lineEdit_7.setMaximumSize(QSize(50, 22))

        self.gridLayout.addWidget(self.lineEdit_7, 3, 1, 1, 1)

        self.label_9 = QLabel(self.groupBox_3)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFont(font2)

        self.gridLayout.addWidget(self.label_9, 3, 3, 1, 1)

        self.label_8 = QLabel(self.groupBox_3)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setFont(font2)

        self.gridLayout.addWidget(self.label_8, 3, 0, 1, 1)

        self.lineEdit_8 = QLineEdit(self.groupBox_3)
        self.lineEdit_8.setObjectName(u"lineEdit_8")
        self.lineEdit_8.setMaximumSize(QSize(50, 22))

        self.gridLayout.addWidget(self.lineEdit_8, 3, 4, 1, 1)


        self.verticalLayout.addWidget(self.groupBox_3)

        self.groupBox_4 = QGroupBox(self.tab)
        self.groupBox_4.setObjectName(u"groupBox_4")
        sizePolicy.setHeightForWidth(self.groupBox_4.sizePolicy().hasHeightForWidth())
        self.groupBox_4.setSizePolicy(sizePolicy)
        self.groupBox_4.setMinimumSize(QSize(580, 110))
        self.groupBox_4.setMaximumSize(QSize(5800, 900))
        self.groupBox_4.setFont(font)
        self.gridLayout_2 = QGridLayout(self.groupBox_4)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_15 = QLabel(self.groupBox_4)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setFont(font2)

        self.gridLayout_2.addWidget(self.label_15, 0, 1, 1, 1)

        self.label_16 = QLabel(self.groupBox_4)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setFont(font2)

        self.gridLayout_2.addWidget(self.label_16, 0, 4, 1, 1)

        self.label_13 = QLabel(self.groupBox_4)
        self.label_13.setObjectName(u"label_13")
        font3 = QFont()
        font3.setPointSize(8)
        font3.setBold(True)
        self.label_13.setFont(font3)

        self.gridLayout_2.addWidget(self.label_13, 0, 0, 1, 1)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_11, 0, 9, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_8, 0, 12, 1, 1)

        self.label_18 = QLabel(self.groupBox_4)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setFont(font2)

        self.gridLayout_2.addWidget(self.label_18, 0, 10, 1, 1)

        self.label_17 = QLabel(self.groupBox_4)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setFont(font2)

        self.gridLayout_2.addWidget(self.label_17, 0, 7, 1, 1)

        self.lineEdit_12 = QLineEdit(self.groupBox_4)
        self.lineEdit_12.setObjectName(u"lineEdit_12")
        self.lineEdit_12.setMaximumSize(QSize(50, 22))

        self.gridLayout_2.addWidget(self.lineEdit_12, 0, 8, 1, 1)

        self.lineEdit_11 = QLineEdit(self.groupBox_4)
        self.lineEdit_11.setObjectName(u"lineEdit_11")
        self.lineEdit_11.setMaximumSize(QSize(50, 22))

        self.gridLayout_2.addWidget(self.lineEdit_11, 0, 5, 1, 1)

        self.label_14 = QLabel(self.groupBox_4)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setFont(font3)

        self.gridLayout_2.addWidget(self.label_14, 1, 0, 1, 1)

        self.comboBox_2 = QComboBox(self.groupBox_4)
        self.comboBox_2.addItem("")
        self.comboBox_2.setObjectName(u"comboBox_2")
        self.comboBox_2.setMaximumSize(QSize(50, 22))

        self.gridLayout_2.addWidget(self.comboBox_2, 0, 11, 1, 1)

        self.label_20 = QLabel(self.groupBox_4)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setFont(font2)

        self.gridLayout_2.addWidget(self.label_20, 1, 1, 1, 1)

        self.lineEdit_10 = QLineEdit(self.groupBox_4)
        self.lineEdit_10.setObjectName(u"lineEdit_10")
        self.lineEdit_10.setMaximumSize(QSize(50, 22))

        self.gridLayout_2.addWidget(self.lineEdit_10, 0, 2, 1, 1)

        self.lineEdit_15 = QLineEdit(self.groupBox_4)
        self.lineEdit_15.setObjectName(u"lineEdit_15")
        self.lineEdit_15.setMaximumSize(QSize(50, 22))

        self.gridLayout_2.addWidget(self.lineEdit_15, 1, 5, 1, 1)

        self.lineEdit_16 = QLineEdit(self.groupBox_4)
        self.lineEdit_16.setObjectName(u"lineEdit_16")
        self.lineEdit_16.setMaximumSize(QSize(50, 22))

        self.gridLayout_2.addWidget(self.lineEdit_16, 1, 2, 1, 1)

        self.label_21 = QLabel(self.groupBox_4)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setFont(font2)

        self.gridLayout_2.addWidget(self.label_21, 1, 4, 1, 1)

        self.lineEdit_14 = QLineEdit(self.groupBox_4)
        self.lineEdit_14.setObjectName(u"lineEdit_14")
        self.lineEdit_14.setMaximumSize(QSize(50, 22))

        self.gridLayout_2.addWidget(self.lineEdit_14, 1, 8, 1, 1)

        self.label_19 = QLabel(self.groupBox_4)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setFont(font2)

        self.gridLayout_2.addWidget(self.label_19, 1, 7, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_3, 1, 9, 1, 1)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_10, 0, 6, 1, 1)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_9, 0, 3, 1, 1)


        self.verticalLayout.addWidget(self.groupBox_4)

        self.groupBox_5 = QGroupBox(self.tab)
        self.groupBox_5.setObjectName(u"groupBox_5")
        sizePolicy.setHeightForWidth(self.groupBox_5.sizePolicy().hasHeightForWidth())
        self.groupBox_5.setSizePolicy(sizePolicy)
        self.groupBox_5.setMinimumSize(QSize(580, 60))
        self.groupBox_5.setMaximumSize(QSize(5800, 600))
        self.groupBox_5.setFont(font)
        self.groupBox_5.setCheckable(False)
        self.groupBox_5.setChecked(False)
        self.horizontalLayout_3 = QHBoxLayout(self.groupBox_5)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_3 = QLabel(self.groupBox_5)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font1)

        self.horizontalLayout_3.addWidget(self.label_3)

        self.comboBox_3 = QComboBox(self.groupBox_5)
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.setObjectName(u"comboBox_3")

        self.horizontalLayout_3.addWidget(self.comboBox_3)

        self.horizontalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.label_12 = QLabel(self.groupBox_5)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setFont(font2)

        self.horizontalLayout_3.addWidget(self.label_12)

        self.lineEdit_17 = QLineEdit(self.groupBox_5)
        self.lineEdit_17.setObjectName(u"lineEdit_17")
        self.lineEdit_17.setMaximumSize(QSize(50, 22))

        self.horizontalLayout_3.addWidget(self.lineEdit_17)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.verticalLayout.addWidget(self.groupBox_5)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        sizePolicy.setHeightForWidth(self.tab_2.sizePolicy().hasHeightForWidth())
        self.tab_2.setSizePolicy(sizePolicy)
        self.verticalLayout_13 = QVBoxLayout(self.tab_2)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.groupBox_11 = QGroupBox(self.tab_2)
        self.groupBox_11.setObjectName(u"groupBox_11")
        sizePolicy1.setHeightForWidth(self.groupBox_11.sizePolicy().hasHeightForWidth())
        self.groupBox_11.setSizePolicy(sizePolicy1)
        self.groupBox_11.setMinimumSize(QSize(580, 60))
        self.groupBox_11.setMaximumSize(QSize(5800, 60))
        self.groupBox_11.setFont(font)
        self.horizontalLayout_4 = QHBoxLayout(self.groupBox_11)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_41 = QLabel(self.groupBox_11)
        self.label_41.setObjectName(u"label_41")
        self.label_41.setFont(font2)

        self.horizontalLayout_4.addWidget(self.label_41)

        self.lineEdit_33 = QLineEdit(self.groupBox_11)
        self.lineEdit_33.setObjectName(u"lineEdit_33")
        self.lineEdit_33.setMinimumSize(QSize(0, 22))
        self.lineEdit_33.setMaximumSize(QSize(50, 22))

        self.horizontalLayout_4.addWidget(self.lineEdit_33)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_12)


        self.verticalLayout_13.addWidget(self.groupBox_11)

        self.scrollArea_2 = QScrollArea(self.tab_2)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        self.scrollArea_2.setMinimumSize(QSize(0, 0))
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 640, 177))
        self.verticalLayout_8 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")

        self.verticalLayout_8.addLayout(self.verticalLayout_7)

        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_13.addWidget(self.scrollArea_2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButton_4 = QPushButton(self.tab_2)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.horizontalLayout_2.addWidget(self.pushButton_4)

        self.pushButton_2 = QPushButton(self.tab_2)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout_2.addWidget(self.pushButton_2)


        self.verticalLayout_13.addLayout(self.horizontalLayout_2)

        self.scrollArea_4 = QScrollArea(self.tab_2)
        self.scrollArea_4.setObjectName(u"scrollArea_4")
        self.scrollArea_4.setWidgetResizable(True)
        self.scrollAreaWidgetContents_5 = QWidget()
        self.scrollAreaWidgetContents_5.setObjectName(u"scrollAreaWidgetContents_5")
        self.scrollAreaWidgetContents_5.setGeometry(QRect(0, 0, 640, 177))
        self.verticalLayout_14 = QVBoxLayout(self.scrollAreaWidgetContents_5)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_12 = QVBoxLayout()
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")

        self.verticalLayout_14.addLayout(self.verticalLayout_12)

        self.scrollArea_4.setWidget(self.scrollAreaWidgetContents_5)

        self.verticalLayout_13.addWidget(self.scrollArea_4)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        sizePolicy.setHeightForWidth(self.tab_3.sizePolicy().hasHeightForWidth())
        self.tab_3.setSizePolicy(sizePolicy)
        self.verticalLayout_3 = QVBoxLayout(self.tab_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.groupBox_12 = QGroupBox(self.tab_3)
        self.groupBox_12.setObjectName(u"groupBox_12")
        sizePolicy.setHeightForWidth(self.groupBox_12.sizePolicy().hasHeightForWidth())
        self.groupBox_12.setSizePolicy(sizePolicy)
        self.groupBox_12.setMinimumSize(QSize(580, 60))
        self.groupBox_12.setMaximumSize(QSize(5800, 60))
        self.groupBox_12.setFont(font)
        self.horizontalLayout_6 = QHBoxLayout(self.groupBox_12)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_43 = QLabel(self.groupBox_12)
        self.label_43.setObjectName(u"label_43")
        self.label_43.setFont(font2)

        self.horizontalLayout_6.addWidget(self.label_43)

        self.lineEdit_35 = QLineEdit(self.groupBox_12)
        self.lineEdit_35.setObjectName(u"lineEdit_35")
        self.lineEdit_35.setMinimumSize(QSize(0, 22))
        self.lineEdit_35.setMaximumSize(QSize(50, 22))

        self.horizontalLayout_6.addWidget(self.lineEdit_35)

        self.horizontalSpacer_15 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_15)


        self.verticalLayout_3.addWidget(self.groupBox_12)

        self.scrollArea_6 = QScrollArea(self.tab_3)
        self.scrollArea_6.setObjectName(u"scrollArea_6")
        self.scrollArea_6.setMinimumSize(QSize(0, 0))
        self.scrollArea_6.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 640, 177))
        self.verticalLayout_17 = QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.verticalLayout_18 = QVBoxLayout()
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")

        self.verticalLayout_17.addLayout(self.verticalLayout_18)

        self.scrollArea_6.setWidget(self.scrollAreaWidgetContents_2)

        self.verticalLayout_3.addWidget(self.scrollArea_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.pushButton_5 = QPushButton(self.tab_3)
        self.pushButton_5.setObjectName(u"pushButton_5")

        self.horizontalLayout_7.addWidget(self.pushButton_5)

        self.pushButton_8 = QPushButton(self.tab_3)
        self.pushButton_8.setObjectName(u"pushButton_8")

        self.horizontalLayout_7.addWidget(self.pushButton_8)


        self.verticalLayout_3.addLayout(self.horizontalLayout_7)

        self.scrollArea_5 = QScrollArea(self.tab_3)
        self.scrollArea_5.setObjectName(u"scrollArea_5")
        self.scrollArea_5.setWidgetResizable(True)
        self.scrollAreaWidgetContents_6 = QWidget()
        self.scrollAreaWidgetContents_6.setObjectName(u"scrollAreaWidgetContents_6")
        self.scrollAreaWidgetContents_6.setGeometry(QRect(0, 0, 640, 177))
        self.verticalLayout_15 = QVBoxLayout(self.scrollAreaWidgetContents_6)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_16 = QVBoxLayout()
        self.verticalLayout_16.setSpacing(7)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")

        self.verticalLayout_15.addLayout(self.verticalLayout_16)

        self.scrollArea_5.setWidget(self.scrollAreaWidgetContents_6)

        self.verticalLayout_3.addWidget(self.scrollArea_5)

        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        sizePolicy.setHeightForWidth(self.tab_4.sizePolicy().hasHeightForWidth())
        self.tab_4.setSizePolicy(sizePolicy)
        self.verticalLayout_10 = QVBoxLayout(self.tab_4)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.groupBox_15 = QGroupBox(self.tab_4)
        self.groupBox_15.setObjectName(u"groupBox_15")
        sizePolicy.setHeightForWidth(self.groupBox_15.sizePolicy().hasHeightForWidth())
        self.groupBox_15.setSizePolicy(sizePolicy)
        self.groupBox_15.setMinimumSize(QSize(580, 60))
        self.groupBox_15.setMaximumSize(QSize(5800, 60))
        self.groupBox_15.setFont(font)
        self.horizontalLayout_15 = QHBoxLayout(self.groupBox_15)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.label_47 = QLabel(self.groupBox_15)
        self.label_47.setObjectName(u"label_47")
        self.label_47.setFont(font2)

        self.horizontalLayout_15.addWidget(self.label_47)

        self.lineEdit_39 = QLineEdit(self.groupBox_15)
        self.lineEdit_39.setObjectName(u"lineEdit_39")
        self.lineEdit_39.setMinimumSize(QSize(0, 22))
        self.lineEdit_39.setMaximumSize(QSize(50, 22))

        self.horizontalLayout_15.addWidget(self.lineEdit_39)

        self.horizontalSpacer_29 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_15.addItem(self.horizontalSpacer_29)


        self.verticalLayout_10.addWidget(self.groupBox_15)

        self.scrollArea_10 = QScrollArea(self.tab_4)
        self.scrollArea_10.setObjectName(u"scrollArea_10")
        self.scrollArea_10.setMinimumSize(QSize(0, 0))
        self.scrollArea_10.setWidgetResizable(True)
        self.scrollAreaWidgetContents_11 = QWidget()
        self.scrollAreaWidgetContents_11.setObjectName(u"scrollAreaWidgetContents_11")
        self.scrollAreaWidgetContents_11.setGeometry(QRect(0, 0, 640, 177))
        self.verticalLayout_11 = QVBoxLayout(self.scrollAreaWidgetContents_11)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")

        self.verticalLayout_11.addLayout(self.verticalLayout_6)

        self.scrollArea_10.setWidget(self.scrollAreaWidgetContents_11)

        self.verticalLayout_10.addWidget(self.scrollArea_10)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.pushButton_9 = QPushButton(self.tab_4)
        self.pushButton_9.setObjectName(u"pushButton_9")

        self.horizontalLayout_8.addWidget(self.pushButton_9)

        self.pushButton_10 = QPushButton(self.tab_4)
        self.pushButton_10.setObjectName(u"pushButton_10")

        self.horizontalLayout_8.addWidget(self.pushButton_10)


        self.verticalLayout_10.addLayout(self.horizontalLayout_8)

        self.scrollArea = QScrollArea(self.tab_4)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents_3 = QWidget()
        self.scrollAreaWidgetContents_3.setObjectName(u"scrollAreaWidgetContents_3")
        self.scrollAreaWidgetContents_3.setGeometry(QRect(0, 0, 640, 177))
        self.verticalLayout_5 = QVBoxLayout(self.scrollAreaWidgetContents_3)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")

        self.verticalLayout_5.addLayout(self.verticalLayout_9)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents_3)

        self.verticalLayout_10.addWidget(self.scrollArea)

        self.tabWidget.addTab(self.tab_4, "")

        self.verticalLayout_2.addWidget(self.tabWidget)


        self.retranslateUi(Form)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"Case Study", None))
        self.label.setText(QCoreApplication.translate("Form", u"Case Name", None))
        self.pushButton.setText(QCoreApplication.translate("Form", u"Load", None))
        self.pushButton_3.setText(QCoreApplication.translate("Form", u"Save", None))
        self.pushButton_6.setText(QCoreApplication.translate("Form", u"Start", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Form", u"OpenFOAM Parameters", None))
        self.label_136.setText(QCoreApplication.translate("Form", u"TIM Thickness (mm)", None))
        self.comboBox_13.setItemText(0, QCoreApplication.translate("Form", u"LR", None))
        self.comboBox_13.setItemText(1, QCoreApplication.translate("Form", u"RL", None))
        self.comboBox_13.setItemText(2, QCoreApplication.translate("Form", u"FB", None))
        self.comboBox_13.setItemText(3, QCoreApplication.translate("Form", u"BF", None))

        self.label_133.setText(QCoreApplication.translate("Form", u"Air Velocity (m/s)", None))
        self.label_134.setText(QCoreApplication.translate("Form", u"Inlet Temperature (K)", None))
        self.label_132.setText(QCoreApplication.translate("Form", u"Air Direction", None))
        self.label_135.setText(QCoreApplication.translate("Form", u"TIM Kappa (W/m\u00b2\u00b7K)", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Unit", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("Form", u"mm", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("Form", u"cm", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("Form", u"m", None))

        self.label_9.setText(QCoreApplication.translate("Form", u"Number of Cores", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"Iteration", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("Form", u"Define Server", None))
        self.label_15.setText(QCoreApplication.translate("Form", u"X", None))
        self.label_16.setText(QCoreApplication.translate("Form", u"Y", None))
        self.label_13.setText(QCoreApplication.translate("Form", u"PCB", None))
        self.label_18.setText(QCoreApplication.translate("Form", u"Material", None))
        self.label_17.setText(QCoreApplication.translate("Form", u"Z", None))
        self.label_14.setText(QCoreApplication.translate("Form", u"Cabinet", None))
        self.comboBox_2.setItemText(0, QCoreApplication.translate("Form", u"FR4", None))

        self.label_20.setText(QCoreApplication.translate("Form", u"X", None))
        self.label_21.setText(QCoreApplication.translate("Form", u"Y", None))
        self.label_19.setText(QCoreApplication.translate("Form", u"Z", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("Form", u"Reliability", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Mode", None))
        self.comboBox_3.setItemText(0, QCoreApplication.translate("Form", u"No Reliability", None))
        self.comboBox_3.setItemText(1, QCoreApplication.translate("Form", u"Simple Reliability", None))
        self.comboBox_3.setItemText(2, QCoreApplication.translate("Form", u"Advanced Reliability", None))

        self.label_12.setText(QCoreApplication.translate("Form", u"Test Temperature (K)", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Form", u"Main", None))
        self.groupBox_11.setTitle(QCoreApplication.translate("Form", u"Define CPUs", None))
        self.label_41.setText(QCoreApplication.translate("Form", u"Number of CPUs", None))
        self.pushButton_4.setText(QCoreApplication.translate("Form", u"Add CPU Type", None))
        self.pushButton_2.setText(QCoreApplication.translate("Form", u"Remove CPU Type", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Form", u"CPUs", None))
#if QT_CONFIG(accessibility)
        self.tab_3.setAccessibleName("")
#endif // QT_CONFIG(accessibility)
        self.groupBox_12.setTitle(QCoreApplication.translate("Form", u"Define GPUs", None))
        self.label_43.setText(QCoreApplication.translate("Form", u"Number of GPUs", None))
        self.pushButton_5.setText(QCoreApplication.translate("Form", u"Add GPU Type", None))
        self.pushButton_8.setText(QCoreApplication.translate("Form", u"Remove GPU Type", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("Form", u"GPUs", None))
        self.groupBox_15.setTitle(QCoreApplication.translate("Form", u"Define PSUs", None))
        self.label_47.setText(QCoreApplication.translate("Form", u"Number of PSUs", None))
        self.pushButton_9.setText(QCoreApplication.translate("Form", u"Add PSU Type", None))
        self.pushButton_10.setText(QCoreApplication.translate("Form", u"Remove PSU Type", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QCoreApplication.translate("Form", u"PSUs", None))
    # retranslateUi

