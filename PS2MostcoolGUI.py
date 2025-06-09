#!/usr/bin/env python
# This is the QT-based frontend for PowerSynth2 Mostcool
# -*- coding: utf-8 -*-

import sys
import os
import logging
#logging.basicConfig(level=logging.INFO)
import json
import time
import tempfile
import csv


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib import cm
from matplotlib.widgets import CheckButtons
from matplotlib.tri import Triangulation
import matplotlib
from matplotlib.colors import Normalize
# Set the backend before importing FigureCanvas
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar

from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QGroupBox, QGridLayout, QVBoxLayout, QHBoxLayout,
                              QLineEdit, QTabWidget, QSlider, QCheckBox, QComboBox, QLabel, QFrame, QScrollArea, QTableWidget, QTableWidgetItem, QHeaderView)
from PySide6.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QFileDialog, QSizePolicy, QSpacerItem
from PySide6.QtGui import QPixmap, QDesktopServices, QDoubleValidator
from PySide6.QtCore import Qt, QTimer, QUrl, Slot, QSize

import fluidfoam as ff
from scipy.interpolate import griddata
import yaml

from gui.qt.py.PS2MSGUI import Ui_Form
from gui.qt.py.SolutionBrowser import Ui_Form as SolutionUi  # Solution UI
from core.PSCore import PSEnv, PSCore
from core.PS2CLI import PS2CLI

class MainWindow(QWidget):
    
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle("PowerSynth MOSTCOOL GUI")
        self.cpu_rows = []
        self.gpu_rows = []
        self.psu_rows = []
        self.cpu_table = None
        self.psu_table = None
        self.cpu_type_table = None
        self.gpu_table = None
        self.gpu_type_table = None
        self.cpu_header_widget = None
        self.gpu_header_widget = None
        self.psu_header_widget = None
        self.results_dir = ""
        self.cpuCount = str(int(os.cpu_count()/2))
        self.timThickness = str(0.0005)
        self.timKappa = str(10)
     
        # Connect inputs
        self.ui.lineEdit_8.setText(self.cpuCount)       # Number of Cores
        self.ui.lineEdit_114.setText(self.timThickness) # TIM Thickness
        self.ui.lineEdit_113.setText(self.timKappa)     # TIM Kappa
        self.ui.lineEdit_39.textChanged.connect(self.createPSURow)
        
        self.ui.lineEdit_33.textChanged.connect(self.createCPURow)
        self.ui.lineEdit_35.textChanged.connect(self.createGPURow)
        
        # Connect signals
        self.ui.pushButton_4.clicked.connect(self.addCPUTypeRow)
        self.ui.pushButton_2.clicked.connect(self.removeCPUTypeRow)
        self.ui.pushButton_5.clicked.connect(self.addGPUTypeRow)
        self.ui.pushButton_8.clicked.connect(self.removeGPUTypeRow)
        self.ui.pushButton_9.clicked.connect(self.addPSUTypeRow)
        self.ui.pushButton_10.clicked.connect(self.removePSUTypeRow)
        self.ui.pushButton_6.clicked.connect(self.createRunPSCase)
        #self.ui.pushButton_7.clicked.connect(self.openResultsDir)
        self.ui.pushButton.clicked.connect(self.onLoadClicked)
        self.ui.pushButton_3.clicked.connect(self.saveYaml)
        
        # Create and configure type table
        self.cpu_type_table = QTableWidget()
        self.gpu_type_table = QTableWidget()
        self.psu_type_table = QTableWidget()
        
        # PS ROOt 
        self.core = PSEnv()
        
        # Load Device Library
        self.cpuIds = []
        self.gpuIds = []
        self.psuIds = []
        self.loadDeviceLibrary()
   
        # Load Default CPU Table
        self.addDefaultCPUTypeRow()
        
        # Load Default GPU Table
        self.addDefaultGPUTypeRow()
        
        # Load Default PSU Table
        self.addDefaultPSUTypeRow()
        
        # Call the whole process without Main Window
        if len(sys.argv) == 2:
            self.RunWithArg()
            
    def loadDeviceLibrary(self):
        compsFile = os.path.join(self.core.PSRoot, 'lib', 'python3.10', 'site-packages', 'gui', 'misc', 'Components.yaml')
        try:
            with open(compsFile, 'r') as file:
                self.dataLib = yaml.safe_load(file)
                
        except Exception as e:
            print(f"Error loading or applying YAML file: {e}")
        
        cpu_data_list = self.dataLib.get('cpus', [])
        num_types = len(cpu_data_list)
        for i in range(num_types):
            cpu_data = cpu_data_list[i]
            self.cpuIds.append(cpu_data.get('id',''))
        
        gpu_data_list = self.dataLib.get('gpus', [])
        num_types = len(gpu_data_list)
        for i in range(num_types):
            gpu_data = gpu_data_list[i]
            self.gpuIds.append(gpu_data.get('id',''))
            
        psu_data_list = self.dataLib.get('psus', [])
        num_types = len(psu_data_list)
        for i in range(num_types):
            psu_data = psu_data_list[i]
            self.psuIds.append(psu_data.get('id',''))   
            
    def createPSURow(self):
        num_psus_text = self.ui.lineEdit_39.text()
        if not num_psus_text.isdigit():
            return
        num_psus = int(num_psus_text)

        # Clear previous elements
        if self.psu_table:
            self.psu_table.deleteLater()
        if self.psu_header_widget:
            self.psu_header_widget.deleteLater()

        # Create new header and table
        self.psu_header_widget = self.createPSUHeaderWidget()
        self.ui.verticalLayout_9.addWidget(self.psu_header_widget)

        # Create table with context-aware widths
        self.psu_table = QTableWidget()
        self.psu_table.setRowCount(num_psus)
        self.psu_table.setColumnCount(3)
        
        # Configure column stretch factors
        stretch_factors = [
            0.5, 0.5, 1.1,           # Location X/Y/Type 
        ]
        
        # Set initial widths and resize modes
        self.psu_table.horizontalHeader().setDefaultSectionSize(100)
        self.psu_table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        
        for col, factor in enumerate(stretch_factors):
            self.psu_table.setColumnWidth(col, int(factor * 100))

        # Configure headers
        sub_headers = [
            "X", "Y",                   # Location
            "Type",                     # Type  
        ]
        self.psu_table.setHorizontalHeaderLabels(sub_headers)

        # Set minimum widths for critical columns
        self.psu_table.horizontalHeader().setMinimumSectionSize(50)

        # Populate table data
        for row in range(num_psus):
            # Location and cooling
            for col in [0, 1]:
                self.psu_table.setItem(row, col, QTableWidgetItem(""))
            
            # Type selection dropdown
            type_combo = QComboBox()
            if self.psu_type_table:
                for type_row in range(self.psu_type_table.rowCount()):
                    type_combo.addItem(self.psu_type_table.item(type_row, 0).text())
            self.psu_table.setCellWidget(row, 2, type_combo)

        self.ui.verticalLayout_9.addWidget(self.psu_table)

        # Connect header resizing
        self.psu_table.horizontalHeader().geometriesChanged.connect(
            lambda: self.syncPSUHeaderWidths()
        )
    
    def createPSUHeaderWidget(self):
        header = QWidget()
        layout = QHBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        #layout.addStretch(1)

        groups = [
            ("Chip", 2.2),         # Wider for coordinate inputs
        ]

        for text, stretch in groups:
            group = QLabel(text)
            group.setAlignment(Qt.AlignCenter)
            group.setStyleSheet("background: #f0f0f0; border: 1px solid #ddd;")
            layout.addWidget(group, stretch=stretch)
        spacer = QSpacerItem(400, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        layout.addItem(spacer)
        
        return header
    
    def syncPSUHeaderWidths(self):
        if not self.psu_table or not self.psu_header_widget:
            return

        header = self.psu_header_widget.layout()
        table = self.psu_table
        
        # Define column groups with their weight factors
        column_groups = [
            (0, 2, 2.2),   # Chip (X/Y/Type) 
        ]

        for group_idx, (start_col, end_col, weight) in enumerate(column_groups):
            total_width = sum(table.columnWidth(col) for col in range(start_col, end_col+1))
            header_item = header.itemAt(group_idx)
            if header_item:
                widget = header_item.widget()
                widget.setFixedWidth(weight*100)  # total_width
                # Adjust font size based on column width
                font_size = 10 #min(max(int(total_width/25), 8), 12)
                widget.setStyleSheet(f"""
                    background: #f0f0f0; 
                    border: 2px solid #ddd;
                    font-size: {font_size}pt;
                """)
                
    def addDefaultPSUTypeRow(self):
           
        psu_data_list = self.dataLib.get('psus', [])
        
        num_types = len(psu_data_list)
        self.psu_type_table.setRowCount(num_types)
        self.psu_type_table.setColumnCount(8)
        
        headers = [
            "Type", "X", "Y", "Z",
            "Cooling Type", "Material", "Power (W)", "Act. Energy (eV)"
        ]
        self.psu_type_table.setHorizontalHeaderLabels(headers)
        
        # Set column widths
        widths = [100, 50, 50, 50, 120, 70, 70, 100]
        for col, width in enumerate(widths):
            self.psu_type_table.setColumnWidth(col, width)

        # Populate type rows
        for i, row in enumerate(range(num_types)):
            psu_data = psu_data_list[i]
            #print(cpu_data)
            # Type column
            type_item = QTableWidgetItem(psu_data.get('id', ''))
            type_item.setFlags(type_item.flags() ^ Qt.ItemIsEditable)
            type_item.setTextAlignment(Qt.AlignCenter) 
            self.psu_type_table.setItem(row, 0, type_item)
            
            # Dimensions
            for col in range(1, 4):
                if col == 1:  # X Location
                    x = str(psu_data.get('x_dim', ''))
                    self.psu_type_table.setItem(row, col, QTableWidgetItem(x))
                elif col == 2:
                    y = str(psu_data.get('y_dim', ''))
                    self.psu_type_table.setItem(row, col, QTableWidgetItem(y))
                elif col == 3:
                    z = str(psu_data.get('z_dim', ''))
                    self.psu_type_table.setItem(row, col, QTableWidgetItem(z))
            
            # Cooling Type
            cooling_combo = QComboBox()
            cooling_combo.addItems(["Air Cooling", "Water Cooling", "No Heatsink"])
            self.psu_type_table.setCellWidget(row, 4, cooling_combo)
            type_value = psu_data.get('type', 'Air Cooling')
            index = cooling_combo.findText(type_value)
            if index >= 0:
                cooling_combo.setCurrentIndex(index)
            
            # Material
            material_combo = QComboBox()
            material_combo.addItems(["Si", "SiC", "Al", "Cu"])
            self.psu_type_table.setCellWidget(row, 5, material_combo)
            material = psu_data.get('material', 'Si')
            index = material_combo.findText(material)
            if index >= 0:
                material_combo.setCurrentIndex(index)
            
            # Power and Energy
            for col in [6, 7]:
                if col == 6:  # X Location
                    power = str(psu_data.get('power', ''))
                    self.psu_type_table.setItem(row, col, QTableWidgetItem(power))
                elif col == 7:
                    actEnergy = str(psu_data.get('activation_energy', ''))
                    self.psu_type_table.setItem(row, col, QTableWidgetItem(actEnergy))

        self.ui.verticalLayout_6.addWidget(self.psu_type_table)
        
    def addPSUTypeRow(self):

        row = self.psu_type_table.rowCount()
        self.psu_type_table.insertRow(row)
        
        # Populate type rows
        # Type column
        type_item = QTableWidgetItem("Custom")
        type_item.setTextAlignment(Qt.AlignCenter) 
        self.psu_type_table.setItem(row, 0, type_item)
        
        # Dimensions
        for col in range(1, 4):
            self.psu_type_table.setItem(row, col, QTableWidgetItem(""))
        
        # Cooling Type
        cooling_combo = QComboBox()
        cooling_combo.addItems(["Air Cooling", "Water Cooling", "No Heatsink"])
        self.psu_type_table.setCellWidget(row, 4, cooling_combo)
        
        # Material
        material_combo = QComboBox()
        material_combo.addItems(["Si", "SiC", "Al", "Cu"])
        self.psu_type_table.setCellWidget(row, 5, material_combo)
        
        # Power and Energy
        for col in [6, 7]:
            self.psu_type_table.setItem(row, col, QTableWidgetItem(""))
            self.psu_type_table.setItem(row, 7, QTableWidgetItem("0.7"))

        self.ui.verticalLayout_6.addWidget(self.psu_type_table)
    
    def removePSUTypeRow(self):
            if self.psu_type_table.rowCount() > 0:
                self.psu_type_table.removeRow(self.psu_type_table.rowCount() - 1)
                
    def createGPURow(self):
        num_gpus_text = self.ui.lineEdit_35.text()
        if not num_gpus_text.isdigit():
            return
        num_gpus = int(num_gpus_text)

        # Clear previous elements
        if self.gpu_table:
            self.gpu_table.deleteLater()
        if self.gpu_header_widget:
            self.gpu_header_widget.deleteLater()

        # Create new header and table
        self.gpu_header_widget = self.createHeaderWidget()
        self.ui.verticalLayout_16.addWidget(self.gpu_header_widget)

        # Create table with context-aware widths
        self.gpu_table = QTableWidget()
        self.gpu_table.setRowCount(num_gpus)
        self.gpu_table.setColumnCount(10)
        
        # Configure column stretch factors
        stretch_factors = [
            0.5, 0.5, 1.1,                  # Location X/Y/Type
            0.5, 0.5, 0.5, 0.5, 0.5, 0.7,   # Heatsink params (X,Y,Z,TB,nFins,FinWidth)
            0.7                             # HS Material   
        ]
        
        # Set initial widths and resize modes
        self.gpu_table.horizontalHeader().setDefaultSectionSize(100)
        self.gpu_table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        
        for col, factor in enumerate(stretch_factors):
            self.gpu_table.setColumnWidth(col, int(factor * 100))

        # Configure headers
        sub_headers = [
            "X", "Y",                   # Location
            "Type",                                    # Type
            "X", "Y", "Z",               # Heatsink Dimensions
            "Tb", "nFins", "Fin Width", # Heatsink Specs
            "Material"                           # HS Material    
        ]
        self.gpu_table.setHorizontalHeaderLabels(sub_headers)
        #self.cpu_table.verticalHeader().setVisible(False)

        # Set minimum widths for critical columns
        self.gpu_table.horizontalHeader().setMinimumSectionSize(50)

        # Populate table data
        for row in range(num_gpus):
            # Location and cooling
            for col in [0, 1]:
                self.gpu_table.setItem(row, col, QTableWidgetItem(""))
            
            # Type selection dropdown
            type_combo = QComboBox()
            if self.gpu_type_table:
                for type_row in range(self.gpu_type_table.rowCount()):
                    type_combo.addItem(self.gpu_type_table.item(type_row, 0).text())
            self.gpu_table.setCellWidget(row, 2, type_combo)
          
            # Heatsink parameters
            for col in range(3, 8):
                self.gpu_table.setItem(row, col, QTableWidgetItem(""))
            
            hs_material_combo = QComboBox()
            hs_material_combo.addItems(["Al", "Copper"])
            self.gpu_table.setCellWidget(row, 9, hs_material_combo)

        self.ui.verticalLayout_16.addWidget(self.gpu_table)

        # Connect header resizing
        self.gpu_table.horizontalHeader().geometriesChanged.connect(
            lambda: self.syncGPUHeaderWidths()
        )
        
    def syncGPUHeaderWidths(self):
        if not self.gpu_table or not self.gpu_header_widget:
            return

        header = self.gpu_header_widget.layout()
        table = self.gpu_table
        
        # Define column groups with their weight factors
        column_groups = [
            (0, 2, 2.2),    # Chip (X/Y/Type) 
            (3, 9, 4)       # Heatsink parameters
        ]

        for group_idx, (start_col, end_col, weight) in enumerate(column_groups):
            total_width = sum(table.columnWidth(col) for col in range(start_col, end_col+1))
            header_item = header.itemAt(group_idx)
            if header_item:
                widget = header_item.widget()
                widget.setFixedWidth(weight*100)    # total_width
                # Adjust font size based on column width
                font_size = 10 #min(max(int(total_width/25), 8), 12)
                widget.setStyleSheet(f"""
                    background: #f0f0f0; 
                    border: 2px solid #ddd;
                    font-size: {font_size}pt;
                """)
                
    def addDefaultGPUTypeRow(self):    
        gpu_data_list = self.dataLib.get('gpus', [])
        
        num_types = len(gpu_data_list)
        self.gpu_type_table.setRowCount(num_types)
        #self.cpu_type_table.insertRow(row)
        #self.cpu_type_table.setRowCount(num_types)
        self.gpu_type_table.setColumnCount(8)
        
        headers = [
            "Type", "X", "Y", "Z",
            "Cooling Type", "Material", "Power (W)", "Act. Energy (eV)"
        ]
        self.gpu_type_table.setHorizontalHeaderLabels(headers)
        
        # Set column widths
        widths = [100, 50, 50, 50, 120, 70, 70, 100]
        for col, width in enumerate(widths):
            self.gpu_type_table.setColumnWidth(col, width)

        # Populate type rows
        for i, row in enumerate(range(num_types)):
            gpu_data = gpu_data_list[i]
            #print(gpu_data)
            # Type column
            type_item = QTableWidgetItem(gpu_data.get('id', ''))
            type_item.setFlags(type_item.flags() ^ Qt.ItemIsEditable)
            type_item.setTextAlignment(Qt.AlignCenter) 
            self.gpu_type_table.setItem(row, 0, type_item)
            
            # Dimensions
            for col in range(1, 4):
                if col == 1:  # X Location
                    x = str(gpu_data.get('x_dim', ''))
                    self.gpu_type_table.setItem(row, col, QTableWidgetItem(x))
                elif col == 2:
                    y = str(gpu_data.get('y_dim', ''))
                    self.gpu_type_table.setItem(row, col, QTableWidgetItem(y))
                elif col == 3:
                    z = str(gpu_data.get('z_dim', ''))
                    self.gpu_type_table.setItem(row, col, QTableWidgetItem(z)) 
            
            # Cooling Type
            cooling_combo = QComboBox()
            cooling_combo.addItems(["Air Cooling", "Water Cooling", "No Heatsink"])
            self.gpu_type_table.setCellWidget(row, 4, cooling_combo)
            type_value = gpu_data.get('type', 'Air Cooling')
            index = cooling_combo.findText(type_value)
            if index >= 0:
                cooling_combo.setCurrentIndex(index)
            
            # Material
            material_combo = QComboBox()
            material_combo.addItems(["Si", "SiC", "Al", "Cu"])
            self.gpu_type_table.setCellWidget(row, 5, material_combo)
            material = gpu_data.get('material', 'Si')
            index = material_combo.findText(material)
            if index >= 0:
                material_combo.setCurrentIndex(index)
            
            # Power and Energy
            for col in [6, 7]:
                if col == 6:  # X Location
                    power = str(gpu_data.get('power', ''))
                    self.gpu_type_table.setItem(row, col, QTableWidgetItem(power))
                elif col == 7:
                    actEnergy = str(gpu_data.get('activation_energy', ''))
                    self.gpu_type_table.setItem(row, col, QTableWidgetItem(actEnergy))

        self.ui.verticalLayout_18.addWidget(self.gpu_type_table)
        
    def addGPUTypeRow(self):

        row = self.gpu_type_table.rowCount()
        self.gpu_type_table.insertRow(row)
       
        # Populate type rows
        # Type column
        type_item = QTableWidgetItem("Custom")
        type_item.setTextAlignment(Qt.AlignCenter) 
        self.gpu_type_table.setItem(row, 0, type_item)
        
        # Dimensions
        for col in range(1, 4):
            self.gpu_type_table.setItem(row, col, QTableWidgetItem(""))
        
        # Cooling Type
        cooling_combo = QComboBox()
        cooling_combo.addItems(["Air Cooling", "Water Cooling", "No Heatsink"])
        self.gpu_type_table.setCellWidget(row, 4, cooling_combo)
        
        # Material
        material_combo = QComboBox()
        material_combo.addItems(["Si", "SiC", "Al", "Cu"])
        self.gpu_type_table.setCellWidget(row, 5, material_combo)
        
        # Power and Energy
        for col in [6, 7]:
            self.gpu_type_table.setItem(row, col, QTableWidgetItem(""))
            self.gpu_type_table.setItem(row, 7, QTableWidgetItem("0.7"))

        self.ui.verticalLayout_18.addWidget(self.gpu_type_table)
    
    def removeGPUTypeRow(self):
            if self.gpu_type_table.rowCount() > 0:
                self.gpu_type_table.removeRow(self.gpu_type_table.rowCount() - 1)
    
    def createHeaderWidget(self):
        header = QWidget()
        layout = QHBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        groups = [
            ("Chip", 2.2),         # Wider for coordinate inputs
            ("Heatsink Parameters", 3.5)         # Expanded parameters
        ]

        for text, stretch in groups:
            group = QLabel(text)
            group.setAlignment(Qt.AlignCenter)
            group.setStyleSheet("background: #f0f0f0; border: 1px solid #ddd;")
            layout.addWidget(group, stretch=stretch)
        spacer = QSpacerItem(10, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        layout.addItem(spacer)
        return header
        
    def createCPURow(self):
        num_cpus_text = self.ui.lineEdit_33.text()
        if not num_cpus_text.isdigit():
            return
        num_cpus = int(num_cpus_text)

        # Clear previous elements
        if self.cpu_table:
            self.cpu_table.deleteLater()
        if self.cpu_header_widget:
            self.cpu_header_widget.deleteLater()

        # Create new header and table
        self.cpu_header_widget = self.createHeaderWidget()
        self.ui.verticalLayout_12.addWidget(self.cpu_header_widget)

        # Create table with context-aware widths
        self.cpu_table = QTableWidget()
        self.cpu_table.setRowCount(num_cpus)
        self.cpu_table.setColumnCount(10)
        
        # Configure column stretch factors
        stretch_factors = [
            0.5, 0.5, 1.1,                  # Location X/Y/Type
            0.5, 0.5, 0.5, 0.5, 0.5, 0.7,   # Heatsink params (X,Y,Z,TB,nFins,FinWidth)
            0.7                             # HS Material   
        ]
        
        # Set initial widths and resize modes
        self.cpu_table.horizontalHeader().setDefaultSectionSize(100)
        self.cpu_table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        
        for col, factor in enumerate(stretch_factors):
            self.cpu_table.setColumnWidth(col, int(factor * 100))

        # Configure headers
        sub_headers = [
            "X", "Y",                   # Location
            "Type",                                    # Type
            "X", "Y", "Z",               # Heatsink Dimensions
            "Tb", "nFins", "Fin Width", # Heatsink Specs
            "Material"                           # HS Material    
        ]
        self.cpu_table.setHorizontalHeaderLabels(sub_headers)
        #self.cpu_table.verticalHeader().setVisible(False)

        # Set minimum widths for critical columns
        self.cpu_table.horizontalHeader().setMinimumSectionSize(50)

        # Populate table data
        for row in range(num_cpus):
            # Location and cooling
            for col in [0, 1]:
                self.cpu_table.setItem(row, col, QTableWidgetItem(""))
            
            # Type selection dropdown
            type_combo = QComboBox()
            if self.cpu_type_table:
                for type_row in range(self.cpu_type_table.rowCount()):
                    type_combo.addItem(self.cpu_type_table.item(type_row, 0).text())
            self.cpu_table.setCellWidget(row, 2, type_combo)
          
            # Heatsink parameters
            for col in range(3, 8):
                self.cpu_table.setItem(row, col, QTableWidgetItem(""))
            
            hs_material_combo = QComboBox()
            hs_material_combo.addItems(["Al", "Copper"])
            self.cpu_table.setCellWidget(row, 9, hs_material_combo)

        self.ui.verticalLayout_12.addWidget(self.cpu_table)

        # Connect header resizing
        self.cpu_table.horizontalHeader().geometriesChanged.connect(
            lambda: self.syncCPUHeaderWidths()
        )
    
    def syncCPUHeaderWidths(self):
        if not self.cpu_table or not self.cpu_header_widget:
            return

        header = self.cpu_header_widget.layout()
        table = self.cpu_table
        
        # Define column groups with their weight factors
        column_groups = [
            (0, 2, 2.2),   # Chip (X/Y/Type) 
            (3, 9, 4)  # Heatsink parameters
        ]

        for group_idx, (start_col, end_col, weight) in enumerate(column_groups):
            total_width = sum(table.columnWidth(col) for col in range(start_col, end_col+1))
            header_item = header.itemAt(group_idx)
            if header_item:
                widget = header_item.widget()
                widget.setFixedWidth(weight*100)  # total_width
                # Adjust font size based on column width
                font_size = 10 #min(max(int(total_width/25), 8), 12)
                widget.setStyleSheet(f"""
                    background: #f0f0f0; 
                    border: 2px solid #ddd;
                    font-size: {font_size}pt;
                """)
                
    def addDefaultCPUTypeRow(self):
        
        cpu_data_list = self.dataLib.get('cpus', [])
        
        num_types = len(cpu_data_list)
        self.cpu_type_table.setRowCount(num_types)
        #self.cpu_type_table.insertRow(row)
        #self.cpu_type_table.setRowCount(num_types)
        self.cpu_type_table.setColumnCount(8)
        
        headers = [
            "Type", "X", "Y", "Z",
            "Cooling Type", "Material", "Power (W)", "Act. Energy (eV)"
        ]
        self.cpu_type_table.setHorizontalHeaderLabels(headers)
        
        # Set column widths
        widths = [100, 50, 50, 50, 120, 70, 70, 100]
        for col, width in enumerate(widths):
            self.cpu_type_table.setColumnWidth(col, width)

        # Populate type rows
        for i, row in enumerate(range(num_types)):
            cpu_data = cpu_data_list[i]
            #print(cpu_data)
            # Type column
            type_item = QTableWidgetItem(cpu_data.get('id', ''))
            type_item.setFlags(type_item.flags() ^ Qt.ItemIsEditable)
            type_item.setTextAlignment(Qt.AlignCenter) 
            self.cpu_type_table.setItem(row, 0, type_item)
            
            # Dimensions
            for col in range(1, 4):
                if col == 1:  # X Location
                    x = str(cpu_data.get('x_dim', ''))
                    self.cpu_type_table.setItem(row, col, QTableWidgetItem(x))
                elif col == 2:
                    y = str(cpu_data.get('y_dim', ''))
                    self.cpu_type_table.setItem(row, col, QTableWidgetItem(y))
                elif col == 3:
                    z = str(cpu_data.get('z_dim', ''))
                    self.cpu_type_table.setItem(row, col, QTableWidgetItem(z))
            
            # Cooling Type
            cooling_combo = QComboBox()
            cooling_combo.addItems(["Air Cooling", "Water Cooling", "No Heatsink"])
            self.cpu_type_table.setCellWidget(row, 4, cooling_combo)
            type_value = cpu_data.get('type', 'Air Cooling')
            index = cooling_combo.findText(type_value)
            if index >= 0:
                cooling_combo.setCurrentIndex(index)
            
            # Material
            material_combo = QComboBox()
            material_combo.addItems(["Si", "SiC", "Al", "Cu"])
            self.cpu_type_table.setCellWidget(row, 5, material_combo)
            material = cpu_data.get('material', 'Si')
            index = material_combo.findText(material)
            if index >= 0:
                material_combo.setCurrentIndex(index)
            
            # Power and Energy
            for col in [6, 7]:
                if col == 6:  # X Location
                    power = str(cpu_data.get('power', ''))
                    self.cpu_type_table.setItem(row, col, QTableWidgetItem(power))
                elif col == 7:
                    actEnergy = str(cpu_data.get('activation_energy', ''))
                    self.cpu_type_table.setItem(row, col, QTableWidgetItem(actEnergy))

        self.ui.verticalLayout_7.addWidget(self.cpu_type_table)
        
    def addCPUTypeRow(self):

        row = self.cpu_type_table.rowCount()
        self.cpu_type_table.insertRow(row)
        
        # Populate type rows
        # Type column
        type_item = QTableWidgetItem("Custom")
        type_item.setTextAlignment(Qt.AlignCenter) 
        self.cpu_type_table.setItem(row, 0, type_item)
        
        # Dimensions
        for col in range(1, 4):
            self.cpu_type_table.setItem(row, col, QTableWidgetItem(""))
        
        # Cooling Type
        cooling_combo = QComboBox()
        cooling_combo.addItems(["Air Cooling", "Water Cooling", "No Heatsink"])
        self.cpu_type_table.setCellWidget(row, 4, cooling_combo)
        
        # Material
        material_combo = QComboBox()
        material_combo.addItems(["Si", "SiC", "Al", "Cu"])
        self.cpu_type_table.setCellWidget(row, 5, material_combo)
        
        # Power and Energy
        for col in [6, 7]:
            self.cpu_type_table.setItem(row, col, QTableWidgetItem(""))
            self.cpu_type_table.setItem(row, 7, QTableWidgetItem("0.7"))

        self.ui.verticalLayout_7.addWidget(self.cpu_type_table)
    
    def removeCPUTypeRow(self):
            if self.cpu_type_table.rowCount() > 0:
                self.cpu_type_table.removeRow(self.cpu_type_table.rowCount() - 1)
    
    def readUi(self):
        """Collect all data from UI"""
        self.data = {
            "case_study": {
                "name": str(self.ui.lineEdit.text())
            },
            "solver_settings": {
                "iteration": int(self.ui.lineEdit_7.text()),
                "number_of_cores": int(self.ui.lineEdit_8.text())
            },
            "reliability": {
                "mode": str(self.ui.comboBox_3.currentIndex()),
                "test_temperature": float(self.ui.lineEdit_17.text() if self.ui.comboBox_3.currentIndex()!=0 else 0)
            },
            "define_server": {
                "pcb": {
                    "x": int(self.ui.lineEdit_10.text()),
                    "y": int(self.ui.lineEdit_11.text()),
                    "z": int(self.ui.lineEdit_12.text()),
                    "material": str(self.ui.comboBox_2.currentText())
                },
                "cabinet": {
                    "x": int(self.ui.lineEdit_16.text()),
                    "y": int(self.ui.lineEdit_15.text()),
                    "z": int(self.ui.lineEdit_14.text())
                }
            },
            "boundary_conditions": {
                "inlet_temperature": float(self.ui.lineEdit_111.text()),
                "air_velocity": float(self.ui.lineEdit_112.text()),
                "air_direction": str(self.ui.comboBox_13.currentText()),
                "tim_thickness": float(self.ui.lineEdit_114.text()),
                "tim_kappa": float(self.ui.lineEdit_113.text()),
                "unit": str(self.ui.comboBox.currentText())
            },
            "define_components": {
                "number_of_cpus": int(self.cpu_table.rowCount()),
                "number_of_gpus": int(self.gpu_table.rowCount()),
                "number_of_psus": int(self.psu_table.rowCount())
            },
            "cpus": [self.getComponentsData(row, is_cpu=True) for row in range(self.cpu_table.rowCount())],
            "gpus": [self.getComponentsData(row, is_gpu=True) for row in range(self.gpu_table.rowCount())],
            "psus": [self.getComponentsData(row, is_psu=True) for row in range(self.psu_table.rowCount())]
        }
        #print(self.data)
    
    def getComponentsData(self, row, is_cpu=False, is_gpu=False, is_psu=False):
        """Extract data from a component row"""
        if is_psu:
            data = {
                "id": "PSU" + str(row+1),
                "x_location": float(self.psu_table.item(row, 0).text()),   # X Location
                "y_location": float(self.psu_table.item(row, 1).text()),   # Y Location
            }    
            
            for i in range(self.psu_type_table.rowCount()):
                if self.psu_type_table.item(i, 0).text() == self.psu_table.cellWidget(row, 2).currentText():
                    data.update({
                    "x_dim": float(self.psu_type_table.item(i, 1).text()),
                    "y_dim": float(self.psu_type_table.item(i, 2).text()),
                    "z_dim": float(self.psu_type_table.item(i, 3).text()),
                    "type": str(self.psu_type_table.cellWidget(i, 4).currentText()),
                    "material": str(self.psu_type_table.cellWidget(i, 5).currentText()),
                    "power": float(self.psu_type_table.item(i, 6).text()),
                    "activation_energy": float(self.psu_type_table.item(i, 7).text()),
                })
            
        elif is_cpu:
            data = {
                "id": "CPU" + str(row+1),
                "x_location": float(self.cpu_table.item(row, 0).text()),  # X Location
                "y_location": float(self.cpu_table.item(row, 1).text()),  # Y Location
                "heatsink": {
                    "x": float(self.cpu_table.item(row, 3).text()),
                    "y": float(self.cpu_table.item(row, 4).text()),
                    "z": float(self.cpu_table.item(row, 5).text()),
                    "tb": float(self.cpu_table.item(row, 6).text()),
                    "n_fins": int(self.cpu_table.item(row, 7).text()),
                    "fin_width": float(self.cpu_table.item(row, 8).text()),
                    "material": str(self.cpu_table.cellWidget(row, 9).currentText())
                }
            }    
            
            #cpu_type = self.cpu_table.cellWidget(row, 2).currentText()
            for i in range(self.cpu_type_table.rowCount()):
                if self.cpu_type_table.item(i, 0).text() == self.cpu_table.cellWidget(row, 2).currentText():
                    data.update({
                    "x_dim": float(self.cpu_type_table.item(i, 1).text()),
                    "y_dim": float(self.cpu_type_table.item(i, 2).text()),
                    "z_dim": float(self.cpu_type_table.item(i, 3).text()),
                    "type": str(self.cpu_type_table.cellWidget(i, 4).currentText()),
                    "material": str(self.cpu_type_table.cellWidget(i, 5).currentText()),
                    "power": float(self.cpu_type_table.item(i, 6).text()),
                    "activation_energy": float(self.cpu_type_table.item(i, 7).text()),
                })
                    
        elif is_gpu:
            data = {
                "id": "GPU" + str(row+1),
                "x_location": float(self.gpu_table.item(row, 0).text()),  # X Location
                "y_location": float(self.gpu_table.item(row, 1).text()),   # Y Location
                "heatsink": {
                    "x": float(self.gpu_table.item(row, 3).text()),
                    "y": float(self.gpu_table.item(row, 4).text()),
                    "z": float(self.gpu_table.item(row, 5).text()),
                    "tb": float(self.gpu_table.item(row, 6).text()),
                    "n_fins": int(self.gpu_table.item(row, 7).text()),
                    "fin_width": float(self.gpu_table.item(row, 8).text()),
                    "material": str(self.gpu_table.cellWidget(row, 9).currentText())
                }
            }    
            
            #cpu_type = self.cpu_table.cellWidget(row, 2).currentText()
            for i in range(self.gpu_type_table.rowCount()):
                if self.gpu_type_table.item(i, 0).text() == self.gpu_table.cellWidget(row, 2).currentText():
                    data.update({
                    "x_dim": float(self.gpu_type_table.item(i, 1).text()),
                    "y_dim": float(self.gpu_type_table.item(i, 2).text()),
                    "z_dim": float(self.gpu_type_table.item(i, 3).text()),
                    "type": str(self.gpu_type_table.cellWidget(i, 4).currentText()),
                    "material": str(self.gpu_type_table.cellWidget(i, 5).currentText()),
                    "power": float(self.gpu_type_table.item(i, 6).text()),
                    "activation_energy": float(self.gpu_type_table.item(i, 7).text()),
                })
            
            #print(data)
        return data
        
    def createRunPSCase(self):
        self.readUi()
        
        # save data on yaml temporary file
        tempFile = tempfile.NamedTemporaryFile(suffix='.yaml')
        filePath = os.path.join(self.core.PSRoot, 'pkg', 'work', 'Sample_Designs', self.data["case_study"]["name"], tempFile.name)
        with open(filePath, 'w') as file:
            yaml.safe_dump(self.data, file, indent=2)
        
        # load yaml temporary file
        try:
            with open(filePath, 'r') as file:
                self.data = yaml.safe_load(file)
                #print(self.data)
        except Exception as e:
            print(f"Error loading or applying YAML file: {e}")
            
        # Create PowerSynth Case
        workFolder = createCase(self.data, self.core)
        compName = createPartFile(self.data, workFolder)
        createMacroScript(self.data, workFolder)
        createLayerStack(self.data, workFolder)
        createLayoutScripts(self.data, workFolder)
        createConstrateFile(self.data, workFolder)
        
        # Run PowerSynth
        ExitCode = runPowerSynth(self.data, self.core)
        
        #if ExitCode == 0:
        self.showResultsWindow(workFolder, compName)
        
    def RunWithArg(self):
        """Read the Case data from yaml file and create OpenFoam Case and show the solution window.
        when the user use the command line to by pass the Main window this method is called."""
        casesFile = sys.argv[1]
        #print(sys.argv[1])
        try:
            with open(casesFile, 'r') as file:
                print("Reading the YAML file of Server")
                caseData = yaml.safe_load(file)
                
        except Exception as e:
            print(f"Error loading or applying YAML file: {e}")
            
        for i, row in enumerate(caseData.get('cpus')):
            row["id"] = "CPU" + str(i+1)
        
        for i, row in enumerate(caseData.get('gpus')):
            row["id"] = "GPU" + str(i+1) 
            
        for i, row in enumerate(caseData.get('psus')):
            row["id"] = "PSU" + str(i+1) 
            
        self.ui.lineEdit_7.setText(str(caseData.get('solver_settings', {}).get('iteration', ''))) # Number of Iteration
        if int(caseData.get('solver_settings', {}).get('number_of_cores', '')) >= int(self.cpuCount):
            caseData['solver_settings']['number_of_cores'] = int(self.cpuCount)
        self.ui.lineEdit.setText(caseData.get('case_study', {}).get('name', '')) # case study name
        #print(caseData)

        # Create PowerSynth Case
        self.data = caseData
        print("Craeting PowerSynth Case and Run the OpenFOAM API")
        workFolder = createCase(self.data, self.core)
        compName = createPartFile(self.data, workFolder)
        createMacroScript(self.data, workFolder)
        createLayerStack(self.data, workFolder)
        createLayoutScripts(self.data, workFolder)
        createConstrateFile(self.data, workFolder)
        
        # Run PowerSynth
        ExitCode = runPowerSynth(self.data, self.core)
        #if ExitCode == 0:

        # call the solution window
        self.showResultsWindow(workFolder, compName)
        
    def showResultsWindow(self, workFolder, compName):
        """ Show the plot results in two tabs: tab1: 2D plot and tab:2 3D view"""
        
        print("Initializing the Results Window")
        self.solution_window = QWidget()
        self.solution_ui = SolutionUi()
        self.solution_ui.setupUi(self.solution_window)
        self.solution_window.setWindowTitle("Simulation Results")
        
        self.figure = plt.Figure(figsize=(16, 12))
        self.canvas = FigureCanvas(self.figure)
        ax = self.figure.add_subplot(111)
        self.figure.subplots_adjust(left=0.30)  # Make space for checkboxes
    
        # Create figure and main axes for Tab 2
        self.figure2 = plt.Figure(figsize=(8, 6), constrained_layout=True)
        self.canvas2 = FigureCanvas(self.figure2)
        # Create 3D axes
        ax2 = self.figure2.add_subplot(111, projection='3d')

        # Reading OpenFoam Case and Gathering the Data
        path = os.path.join(workFolder, 'Solutions', 'Initial_Layout', 'Layout0')
        latestTime = self.ui.lineEdit_7.text()
        regions = compName
        #print(regions)
        grouped_regions = {"Component": compName[1:], "PCB": compName[0:1]}
        
        # Function to load data for a region
        print("Reading the OpenFOAM results")
        def loadRegionData(region):
            try:
                x, y, z = ff.readmesh(path, region=region, structured=False, verbose=False)
                temperature = ff.readfield(path, time_name = latestTime, region=region, name='T', verbose=False)
                x *=1000
                y *=1000
                z *=1000
                # Handle 2D slice if 3D
                if len(np.unique(z)) > 1:
                    if region == 'pcb':
                        mask = z > int(self.data['define_server']['pcb']['z']) - 1  # Slice at min(z); adjust if needed
                    
                    else:
                        thick = int(self.data['define_server']['pcb']['z']) + int(self.data['cpus'][0]['z_dim'])
                        mask = z > thick - 2  # Slice at min(z); adjust if needed
                    
                    start = abs(len(temperature) - len(x)) 
                    if start != 0:
                        temperature = temperature[:-start]    
                    x, y, t = x[mask], y[mask], temperature[mask]- 273.15
                else:
                    x, y, t = x, y, temperature
                return x, y, t
            except Exception as e:
                print(f"Error loading region {region}: {e}")
                return None, None, None
        
        # Load data for all regions
        region_data = {region: loadRegionData(region) for region in regions}
        all_temps = np.concatenate([d[2] for d in region_data.values() if d[2] is not None])
        default_min, default_max = round(np.min(all_temps), ndigits=2), round(np.max(all_temps), ndigits=2)
      
        # Create shared normalization and colormap
        cmap = cm.rainbow
        norm = Normalize()
        sm = cm.ScalarMappable(norm=norm, cmap=cmap)
        sm.set_array(all_temps)  # Set array with all possible values
        
        # Store contour plots and triangulations
        self.plots = {}
        for region in regions:
            x, y, t = region_data[region]
            if x is not None:
                tri = Triangulation(x, y)
                levels = np.linspace(default_min, default_max, 150)
                contour = ax.tricontourf(tri, t, levels=levels, cmap=cmap, norm = norm)
                contour.set_visible(True)  # Initially Visible
                self.plots[region] = contour

        # Create colorbar
        cbar = self.figure.colorbar(sm, ax=ax, shrink=0.75, pad=0.03)
        cbar.set_label('Temperature (C)', fontsize=10, labelpad=10)
        ax.set_aspect('equal')
        #ax.set_title(f"2D Temperature Field at t = {latestTime}", fontsize=12, pad=15)
        cbar.ax.tick_params(labelsize=12)  # Larger colorbar ticks

        # Customize axes
        ax.set_xlabel("X (mm)", fontsize=10)
        ax.set_ylabel("Y (mm)", fontsize=10)

        # Improve tick visibility
        ax.tick_params(axis='both', which='major', labelsize=10)

        # Set tight layout
        self.figure.tight_layout(pad=6)

        # Optional: Add gridlines or annotations
        #ax.grid(True, linestyle='--', alpha=0.3)  # Light grid for reference
        
        def toggleRegion():
            for label, checkbox in self.checkboxes.items():
                if checkbox.isChecked():
                    if label in grouped_regions:
                        for region in grouped_regions[label]:
                            if region in self.plots:
                                self.plots[region].set_visible(True)
                    else:
                        if label in self.plots:
                            self.plots[label].set_visible(True)
                else:
                    if label in grouped_regions:
                        for region in grouped_regions[label]:
                            if region in self.plots:
                                self.plots[region].set_visible(False)
                    else:
                        if label in self.plots:
                            self.plots[label].set_visible(False)
            update2dPlot()
            self.canvas.draw()
            
        def update2dPlot():
            visible_plots = [p for p in self.plots.values() if p.get_visible()]
            if visible_plots:
                try:
                    t_min = float(self.min_edit.text()) if self.min_edit.text().strip() else norm.vmin
                    t_max = float(self.max_edit.text()) if self.max_edit.text().strip() else norm.vmax
                    if t_min >= t_max:
                        raise ValueError("Min must be less than Max")
                except ValueError as e:
                    print(f"Invalid input: {e}. Using previous range: {norm.vmin} - {norm.vmax}")
                    t_min, t_max = norm.vmin, norm.vmax
                
                for plot in visible_plots:
                    plot.set_clim(t_min, t_max)
                #print(t_min)
                #print(t_max)
                norm.vmin = t_min
                norm.vmax = t_max
                sm.norm = norm
                self.canvas.draw()
                
        # Update plot when text is submitted
        def updateTempRange():
            update2dPlot()
            self.canvas.draw()
        
        # PySide6 controls layout in a fixed-width widget, horizontal
        controls_widget = QWidget()
        controls_widget.setMaximumWidth(400)  # Adjusted for horizontal layout
        controls_layout = QHBoxLayout(controls_widget)
        
        # Checkboxes
        checkboxes_widget = QWidget()
        checkboxes_layout = QHBoxLayout(checkboxes_widget)
        self.checkboxes = {}
        toggle_options = list(grouped_regions.keys()) + [r for r in regions if not any(r in v for v in grouped_regions.values())]
        for label in toggle_options:
            checkbox = QCheckBox(label)
            checkbox.setChecked(True)
            checkbox.stateChanged.connect(toggleRegion)
            self.checkboxes[label] = checkbox
            checkboxes_layout.addWidget(checkbox)

        # Temperature limits
        temp_limits_widget = QWidget()
        temp_limits_layout = QHBoxLayout(temp_limits_widget)
        temp_limits_layout.addWidget(QLabel("Min T (C):"))
        self.min_edit = QLineEdit(str(default_min))
        self.min_edit.setFixedWidth(40)
        validator = QDoubleValidator()
        validator.setNotation(QDoubleValidator.StandardNotation)
        self.min_edit.setValidator(validator)
        self.min_edit.returnPressed.connect(updateTempRange)
        temp_limits_layout.addWidget(self.min_edit)

        temp_limits_layout.addWidget(QLabel("Max T (C):"))
        self.max_edit = QLineEdit(str(default_max))
        self.max_edit.setFixedWidth(40)
        self.max_edit.setValidator(validator)
        self.max_edit.returnPressed.connect(updateTempRange)
        temp_limits_layout.addWidget(self.max_edit)

        # Top horizontal layout for toolbar and controls
        top_layout = QHBoxLayout()
        self.toolbar = CustomNavigationToolbar(self.canvas, self.solution_window, region_data, self.plots)
        #self.toolbar = NavigationToolbar(self.canvas)

        top_layout.addWidget(self.toolbar, stretch=1)  # Toolbar expands
        # Outer vertical line separator
        separator_outer = QFrame()
        separator_outer.setFrameShape(QFrame.VLine)
        separator_outer.setFrameShadow(QFrame.Sunken)
        separator_outer.setLineWidth(1)
        top_layout.addWidget(separator_outer)
        #separator.setStyleSheet("QFrame { border: 1px solid black; }")
        #separator.setLineWidth(1)      
        top_layout.addWidget(checkboxes_widget, stretch=0)  # Controls fixed
        separator_inner = QFrame()
        separator_inner.setFrameShape(QFrame.VLine)
        separator_inner.setFrameShadow(QFrame.Sunken)
        separator_inner.setLineWidth(1)
        top_layout.addWidget(separator_inner)
        top_layout.addWidget(temp_limits_widget, stretch=0)  # Controls fixed
        
        #top_layout.addWidget(controls_widget, stretch=0)  # Controls fixed
        
        top_layout.setSpacing(0)
        
        # Add to Tab 2's main vertical layout
        self.solution_ui.verticalLayout_3.addLayout(top_layout)
        self.solution_ui.verticalLayout_3.addWidget(self.canvas, stretch=1)  # Canvas expands vertically
 
        # 3D Plot
        regions = os.listdir(os.path.join(path, latestTime))
        j = 0
        for region in regions:
            if region == 'air': 
                pass
                
            elif region == 'uniform':
                pass
            
            else:
                x, y, z = ff.readmesh(path, region=region, structured=False, verbose=False)
                temp = ff.readscalar(path, time_name = latestTime, region=region, name='T', verbose=False)
                
                if j == 0:
                    Xtotal = x
                    Ytotal = y
                    Ztotal = z
                    Ttotal = temp     
                else:
                    Xtotal = np.concatenate((Xtotal, x))
                    Ytotal = np.concatenate((Ytotal, y))
                    Ztotal = np.concatenate((Ztotal, z))
                    Ttotal = np.concatenate((Ttotal, temp))
                j+=1 
            

        # Plot Server Temperature
        start = abs(len(Ttotal) - len(Xtotal))
        Temp = Ttotal - 273.15
        if start != 0:
            Temp = Temp[:-start]
        
        Xtotal *=1000
        Ytotal *= 1000
        Ztotal *=1000
        
        sc = ax2.scatter(Xtotal, Ytotal, Ztotal, c=Temp, marker='s', s=5, cmap='rainbow')
        #plt.colorbar(sc, shrink=0.3, pad=0.15, label='Temperature (C)')
        ax2.set_aspect('equal')
        ax2.set_xlabel('X (mm)', labelpad=10, fontsize=10)
        ax2.set_ylabel('Y (mm)', labelpad=4, fontsize=10)
        ax2.set_zlabel('Z (mm)', labelpad=4, fontsize=10)
        
        # Improve tick visibility
        ax2.tick_params(axis='both', which='major', labelsize=8)
        ax2.locator_params(axis='z', nbins=3)
        
        # Set tight layout
        self.figure2.tight_layout()
        
        # Plot widget with toolbar and canvas
        plot3_widget = QWidget()
        plot3_layout = QVBoxLayout(plot3_widget)
        self.toolbar3 = NavigationToolbar(self.canvas2, self.solution_window)
        
        # Customize toolbar: Remove the "Pan" button
        actions = self.toolbar3.actions()
        for action in actions:
            if action.text() == "Pan":  # Identify the Pan action by its text
                self.toolbar3.removeAction(action)
            elif action.text() == "Back":
                self.toolbar3.removeAction(action)
            elif action.text() == "Forward":
                self.toolbar3.removeAction(action)
                
        plot3_layout.addWidget(self.toolbar3)
        plot3_layout.addWidget(self.canvas2, stretch=1)
        
        self.solution_ui.verticalLayout.addWidget(plot3_widget)
        
        self.solution_ui.tabWidget.setTabVisible(1, False)  # Preferred method to hide the tab
        
        # tab 3D PNG
        png_path = os.path.join(self.core.PSRoot, 'pkg', 'work', 'Sample_Designs', self.ui.lineEdit.text(), 'Solutions', 'Initial_Layout', 'Layout0', '3DPlot.png')
        self.figure2.savefig(png_path, bbox_inches='tight', dpi=300)

        # Configure graphics view for PNG display
        scene = QGraphicsScene()
        
        # Load the PNG image
        pixmap = QPixmap(png_path)
        if pixmap.isNull():
            print(f"Failed to load PNG file: {png_path}")
            return

        # Create a QGraphicsPixmapItem and add it to the scene
        pixmap_item = QGraphicsPixmapItem(pixmap)
        scene.addItem(pixmap_item)

        # Set the scene to the QGraphicsView in the "3D PNG" tab
        self.solution_ui.graphicsView.setScene(scene)
        
        # Scale to fit the view's width (approximated as 900 pixels)
        view_width = 600
        scale_factor = view_width / pixmap.width()  # Approx. 600 / 1928 ≈ 0.467
        self.solution_ui.graphicsView.scale(scale_factor, scale_factor) 
        
        # tab 3 Summary
        self.summary_table = QTableWidget()
        self.summary_table.setColumnCount(3)
        
        headers = [
            "Components", "Max_Temp (C)", "Acc_Factor"
        ]
        self.summary_table.setHorizontalHeaderLabels(headers)
        
        resultFolder = os.path.join(self.core.PSRoot, 'pkg', 'work', 'Sample_Designs', self.ui.lineEdit.text(), 'Solutions', 'Initial_Layout', 'Layout0')
        fileName = os.path.join(resultFolder, 'reliability.csv')

        with open(fileName, 'r', newline='') as csvfile:
            csvreader = csv.reader(csvfile)

            for i, row in enumerate(csvreader):
                if i:  # Skip the column headers
                    self.summary_table.insertRow(i-1)
                    for j, val in enumerate(row):
                        if j:  # Skip the ID column
                            textedit = QTableWidgetItem()
                            textedit.setText(val)
                            self.summary_table.setItem(i-1, j-1, textedit)
        self.solution_ui.verticalLayout_5.addWidget(self.summary_table)
        
        print("Show the Results Window")
        self.solution_window.show() 
    
    def onLoadClicked(self):
        """
        when the "Load" button is clicked.
        Opens a file dialog for the user to select a YAML file.
        """
        # Open a file dialog with native look and feel
        filePath = os.path.join(self.core.PSRoot, 'pkg', 'work', 'Sample_Designs')
        file_name, _ = QFileDialog.getOpenFileName(
            self,  # Parent window
            "Select YAML File",  # Dialog title
            filePath,  # Starting directory (empty means default directory)
            "YAML Files (*.yaml *.yml);;All Files (*)"  # Filter for file types
        )

        if file_name:  # If a file was selected
            # Here you can add logic to process the selected YAML file
            print(f"Selected file: {file_name}")
            # For example, you might want to load and parse the YAML file here
            self.loadApplyYaml(file_name)
    
    def loadApplyYaml(self, file_path):
        """
        Load the YAML file and apply its values to the UI.
        """
        try:
            with open(file_path, 'r') as file:
                data = yaml.safe_load(file)

            # Apply values to UI elements
            self.applyToUI(data)

        except Exception as e:
            print(f"Error loading or applying YAML file: {e}")
    
    def applyToUI(self, data):
        """
        Apply the YAML data to the corresponding UI elements.
        """
        # Case Study Name
        if hasattr(self.ui, 'lineEdit'):
            self.ui.lineEdit.setText(data.get('case_study', {}).get('name', ''))

        # Solver Settings
        if hasattr(self.ui, 'lineEdit_7') and hasattr(self.ui, 'lineEdit_8'):
            self.ui.lineEdit_7.setText(str(data.get('solver_settings', {}).get('iteration', '')))
            if int(data.get('solver_settings', {}).get('number_of_cores', '')) <= int(self.cpuCount):
                self.ui.lineEdit_8.setText(str(data.get('solver_settings', {}).get('number_of_cores', '')))
            else:
                data['solver_settings']['number_of_cores'] = int(self.cpuCount)

        # Reliability
        if hasattr(self.ui, 'lineEdit_17'):
            reliability = data.get('reliability', {})
            mode = reliability.get('mode', '0')  # 0=no reliability , 1=simple reliabilit, 2=advanced reliability
            self.ui.comboBox_3.setCurrentIndex(int(mode))
            self.ui.lineEdit_17.setText(str(reliability.get('test_temperature', '')))

        # Boundary Conditions
        if hasattr(self.ui, 'lineEdit_111') and hasattr(self.ui, 'lineEdit_112') and hasattr(self.ui, 'lineEdit_113') and hasattr(self.ui, 'lineEdit_114') and hasattr(self.ui, 'comboBox_13'):
            self.ui.lineEdit_111.setText(str(data.get('boundary_conditions', {}).get('inlet_temperature', '')))
            self.ui.lineEdit_112.setText(str(data.get('boundary_conditions', {}).get('air_velocity', '')))
            self.ui.lineEdit_113.setText(str(data.get('boundary_conditions', {}).get('tim_kappa', '')))
            self.ui.lineEdit_114.setText(str(data.get('boundary_conditions', {}).get('tim_thickness', '')))
            air_direction = data.get('boundary_conditions', {}).get('air_direction', 'LR')
            index = self.ui.comboBox_13.findText(air_direction)
            if index >= 0:
                self.ui.comboBox_13.setCurrentIndex(index)
            unit = data.get('boundary_conditions', {}).get('unit', 'mm')
            index = self.ui.comboBox.findText(unit)
            if index >= 0:
                self.ui.comboBox.setCurrentIndex(index)
                
        # Define Server (PCB)
        if hasattr(self.ui, 'lineEdit_10') and hasattr(self.ui, 'lineEdit_11') and hasattr(self.ui, 'lineEdit_12') and hasattr(self.ui, 'comboBox_2'):
            pcb = data.get('define_server', {}).get('pcb', {})
            self.ui.lineEdit_10.setText(str(pcb.get('x', '')))  # X
            self.ui.lineEdit_11.setText(str(pcb.get('y', '')))  # Y
            self.ui.lineEdit_12.setText(str(pcb.get('z', '')))  # Z
            material = pcb.get('material', 'FR4')
            index = self.ui.comboBox_2.findText(material)
            if index >= 0:
                self.ui.comboBox_2.setCurrentIndex(index)

        # Define Server (Cabinet)
        if hasattr(self.ui, 'lineEdit_14') and hasattr(self.ui, 'lineEdit_15') and hasattr(self.ui, 'lineEdit_16'):
            cabinet = data.get('define_server', {}).get('cabinet', {})
            self.ui.lineEdit_16.setText(str(cabinet.get('x', '')))  # X
            self.ui.lineEdit_15.setText(str(cabinet.get('y', '')))  # Y
            self.ui.lineEdit_14.setText(str(cabinet.get('z', '')))  # Z

        # Define Components
        if hasattr(self.ui, 'lineEdit_33') and hasattr(self.ui, 'lineEdit_35') and hasattr(self.ui, 'lineEdit_39'):
            components = data.get('define_components', {})
            self.ui.lineEdit_33.setText(str(components.get('number_of_cpus', '')))
            self.ui.lineEdit_35.setText(str(components.get('number_of_gpus', '')))
            self.ui.lineEdit_39.setText(str(components.get('number_of_psus', '')))
            
            # Fill existing CPU rows with data
            cpu_rows = components.get('number_of_cpus', '')
            cpu_data_list = data.get('cpus', [])
            
            for i in range(len(self.cpuIds)):
                self.removeCPUTypeRow()
            cpuIds = set()
            cpuType = []
            
            i = 0
            for row in range(cpu_rows):
                cpu_data = cpu_data_list[row]
                cpuType.append(cpu_data.get('id', ''))
                #print(cpu_data)
                if str(cpu_data.get('id', '')) not in cpuIds:
                    cpuIds.add(str(cpu_data.get('id', '')))
                    self.addCPUTypeRow()
                    self.cpu_type_table.setItem(i, 0, QTableWidgetItem(str(cpu_data.get('id', ''))))
                    self.cpu_type_table.setItem(i, 1, QTableWidgetItem(str(cpu_data.get('x_dim', ''))))
                    self.cpu_type_table.setItem(i, 2, QTableWidgetItem(str(cpu_data.get('y_dim', ''))))
                    self.cpu_type_table.setItem(i, 3, QTableWidgetItem(str(cpu_data.get('z_dim', ''))))
                    widget = self.cpu_type_table.cellWidget(i, 4)
                    type_value = cpu_data.get('type', 'Air Cooling')
                    index = widget.findText(type_value)
                    if index >= 0:
                        widget.setCurrentIndex(index)
                    widget = self.cpu_type_table.cellWidget(i, 5)
                    material = cpu_data.get('material', 'Si')
                    index = widget.findText(material)
                    if index >= 0:
                        widget.setCurrentIndex(index)
                    self.cpu_type_table.setItem(i, 6, QTableWidgetItem(str(cpu_data.get('power', ''))))
                    self.cpu_type_table.setItem(i, 7, QTableWidgetItem(str(cpu_data.get('activation_energy', ''))))
                    i+=1
                    
            for i, row in enumerate(range(cpu_rows)):
                cpu_data = cpu_data_list[i]
                #print(cpu_data)

                self.cpu_table.setItem(row, 0, QTableWidgetItem(str(cpu_data.get('x_location', ''))))
                self.cpu_table.setItem(row, 1, QTableWidgetItem(str(cpu_data.get('y_location', ''))))
                # Type selection dropdown
                widget = self.cpu_table.cellWidget(row, 2)
                widget.clear()
                if self.cpu_type_table:
                    for type_row in range(self.cpu_type_table.rowCount()):
                        #print(type_row)
                        widget.addItem(self.cpu_type_table.item(type_row, 0).text())
                    index = widget.findText(cpuType[row])
                    if index >= 0:
                        widget.setCurrentIndex(index)
                self.cpu_table.setCellWidget(row, 2, widget)
                self.cpu_table.setItem(row, 3, QTableWidgetItem(str(cpu_data.get('heatsink', {}).get('x', ''))))
                self.cpu_table.setItem(row, 4, QTableWidgetItem(str(cpu_data.get('heatsink', {}).get('y', ''))))
                self.cpu_table.setItem(row, 5, QTableWidgetItem(str(cpu_data.get('heatsink', {}).get('z', ''))))
                self.cpu_table.setItem(row, 6, QTableWidgetItem(str(cpu_data.get('heatsink', {}).get('tb', ''))))
                self.cpu_table.setItem(row, 7, QTableWidgetItem(str(cpu_data.get('heatsink', {}).get('n_fins', ''))))
                self.cpu_table.setItem(row, 8, QTableWidgetItem(str(cpu_data.get('heatsink', {}).get('fin_width', ''))))
                widget = self.cpu_table.cellWidget(row, 9)
                hsMaterial = cpu_data.get('heatsink', {}).get('material', '')
                index = widget.findText(hsMaterial)
                if index >= 0:
                    widget.setCurrentIndex(index)
                    
            # Fill existing GPU rows with data using layout positions (same structure as CPUs)
            gpu_rows = components.get('number_of_gpus', '')
            gpu_data_list = data.get('gpus', [])
            
            for i in range(len(self.gpuIds)):
                self.removeGPUTypeRow()
            gpuIds = set()
            gpuType = []
            i = 0
            for row in range(gpu_rows):
                gpu_data = gpu_data_list[row]
                gpuType.append(gpu_data.get('id', ''))
                #print(gpu_data)
                if str(gpu_data.get('id', '')) not in gpuIds:
                    gpuIds.add(str(gpu_data.get('id', '')))
                    self.addGPUTypeRow()
                    self.gpu_type_table.setItem(i, 0, QTableWidgetItem(str(gpu_data.get('id', ''))))
                    self.gpu_type_table.setItem(i, 1, QTableWidgetItem(str(gpu_data.get('x_dim', ''))))
                    self.gpu_type_table.setItem(i, 2, QTableWidgetItem(str(gpu_data.get('y_dim', ''))))
                    self.gpu_type_table.setItem(i, 3, QTableWidgetItem(str(gpu_data.get('z_dim', ''))))
                    widget = self.gpu_type_table.cellWidget(i, 4)
                    type_value = gpu_data.get('type', 'Air Cooling')
                    index = widget.findText(type_value)
                    if index >= 0:
                        widget.setCurrentIndex(index)
                    widget = self.gpu_type_table.cellWidget(i, 5)
                    material = gpu_data.get('material', 'Si')
                    index = widget.findText(material)
                    if index >= 0:
                        widget.setCurrentIndex(index)
                    self.gpu_type_table.setItem(i, 6, QTableWidgetItem(str(gpu_data.get('power', ''))))
                    self.gpu_type_table.setItem(i, 7, QTableWidgetItem(str(gpu_data.get('activation_energy', ''))))
                    i+=1
                    
            for i, row in enumerate(range(gpu_rows)):
                gpu_data = gpu_data_list[i]
                #print(gpu_data)
                self.gpu_table.setItem(row, 0, QTableWidgetItem(str(gpu_data.get('x_location', ''))))
                self.gpu_table.setItem(row, 1, QTableWidgetItem(str(gpu_data.get('y_location', ''))))
                # Type selection dropdown
                widget = self.gpu_table.cellWidget(row, 2)
                widget.clear()
                if self.gpu_type_table:
                    for type_row in range(self.gpu_type_table.rowCount()):
                        #print(type_row)
                        widget.addItem(self.gpu_type_table.item(type_row, 0).text())
                    index = widget.findText(gpuType[row])
                    if index >= 0:
                        widget.setCurrentIndex(index)
                self.gpu_table.setCellWidget(row, 2, widget)
                self.gpu_table.setItem(row, 3, QTableWidgetItem(str(gpu_data.get('heatsink', {}).get('x', ''))))
                self.gpu_table.setItem(row, 4, QTableWidgetItem(str(gpu_data.get('heatsink', {}).get('y', ''))))
                self.gpu_table.setItem(row, 5, QTableWidgetItem(str(gpu_data.get('heatsink', {}).get('z', ''))))
                self.gpu_table.setItem(row, 6, QTableWidgetItem(str(gpu_data.get('heatsink', {}).get('tb', ''))))
                self.gpu_table.setItem(row, 7, QTableWidgetItem(str(gpu_data.get('heatsink', {}).get('n_fins', ''))))
                self.gpu_table.setItem(row, 8, QTableWidgetItem(str(gpu_data.get('heatsink', {}).get('fin_width', ''))))
                widget = self.gpu_table.cellWidget(row, 9)
                hsMaterial = gpu_data.get('heatsink', {}).get('material', '')
                index = widget.findText(hsMaterial)
                if index >= 0:
                    widget.setCurrentIndex(index)

            # Fill existing PSU rows with data using layout positions
            psu_rows = components.get('number_of_psus', '')
            psu_data_list = data.get('psus', [])

            for i in range(len(self.psuIds)):
                self.removePSUTypeRow()
            psuIds = set()
            psuType = []
            i = 0
            for row in range(psu_rows):
                #if i < len(psu_data_list):  # Ensure we have data for this row
                psu_data = psu_data_list[row]
                psuType.append(psu_data.get('id', ''))
                #print(psu_data)
                if str(psu_data.get('id', '')) not in psuIds:
                    psuIds.add(str(psu_data.get('id', '')))
                    self.addPSUTypeRow()
                    self.psu_type_table.setItem(i, 0, QTableWidgetItem(str(psu_data.get('id', ''))))
                    self.psu_type_table.setItem(i, 1, QTableWidgetItem(str(psu_data.get('x_dim', ''))))
                    self.psu_type_table.setItem(i, 2, QTableWidgetItem(str(psu_data.get('y_dim', ''))))
                    self.psu_type_table.setItem(i, 3, QTableWidgetItem(str(psu_data.get('z_dim', ''))))
                    widget = self.psu_type_table.cellWidget(i, 4)
                    type_value = psu_data.get('type', 'Air Cooling')
                    index = widget.findText(type_value)
                    if index >= 0:
                        widget.setCurrentIndex(index)
                    widget = self.psu_type_table.cellWidget(i, 5)
                    material = psu_data.get('material', 'Si')
                    index = widget.findText(material)
                    if index >= 0:
                        widget.setCurrentIndex(index)
                    self.psu_type_table.setItem(i, 6, QTableWidgetItem(str(psu_data.get('power', ''))))
                    self.psu_type_table.setItem(i, 7, QTableWidgetItem(str(psu_data.get('activation_energy', ''))))
                    i+=1
                    
            for i, row in enumerate(range(psu_rows)):
                #if i < len(psu_data_list):  # Ensure we have data for this row
                psu_data = psu_data_list[i]
                #print(psu_data)
                self.psu_table.setItem(row, 0, QTableWidgetItem(str(psu_data.get('x_location', ''))))
                self.psu_table.setItem(row, 1, QTableWidgetItem(str(psu_data.get('y_location', ''))))
                # Type selection dropdown
                widget = self.psu_table.cellWidget(row, 2)
                widget.clear()
                if self.psu_type_table:
                    for type_row in range(self.psu_type_table.rowCount()):
                        #print(type_row)
                        widget.addItem(self.psu_type_table.item(type_row, 0).text())
                    index = widget.findText(psuType[row])
                    if index >= 0:
                        widget.setCurrentIndex(index)
                self.psu_table.setCellWidget(row, 2, widget)
    
    def openResultsDir(self):
        """Open the resulta directory"""
        resultFolder = os.path.join(self.core.PSRoot, 'pkg', 'work', 'Sample_Designs', self.ui.lineEdit.text(), 'Solutions', 'Initial_Layout', 'Layout0')
        
        # Convert path to QUrl
        url = QUrl.fromLocalFile(resultFolder)
        
        # Open directory in default file explorer
        QDesktopServices.openUrl(url)
        
    def saveYaml(self):
        self.readUi()
        
        filePath = os.path.join(self.core.PSRoot, 'pkg', 'work', 'Sample_Designs', self.ui.lineEdit.text(), 'case.yaml')
        
        # Open a file dialog with native look and feel
        file_name, _ = QFileDialog.getSaveFileName(
            self,  # Parent window
            "Save YAML File",  # Dialog title
            "",  # Starting directory (empty means default directory)
            #"YAML Files (*.yaml *.yml);;All Files (*)"  # Filter for file types
        )
        
        with open(filePath, 'w') as file:
            yaml.safe_dump(self.data, file, indent=4)

# Functions for creating PS folders and files    
def createCase(data, Core):
    caseFolders = ['Figs', 'Part_Lib', 'Solutions', 'Characterization']
    workFolder = os.path.join(Core.PSRoot, 'pkg', 'work', 'Sample_Designs', data["case_study"]["name"])
    if not os.path.exists(workFolder):
        os.makedirs(workFolder)
    
    for folder in caseFolders:
        if not os.path.exists(os.path.join(workFolder, folder)):
            os.makedirs(os.path.join(workFolder, folder))
    return workFolder         

def createPartFile(data, workFolder):
    """
    Creates a .part file for Components.

    :param data: Dictionary containing Components data.
    :param filename: The name of the file to be created.
    """
    path = os.path.join(workFolder, 'Part_Lib')
    data = {
        "Components": {
                "CPUs": data["cpus"],
                "GPUs": data["gpus"],
                "PSUs": data["psus"]
            }
        }
    compName = ['pcb']
    for components in data["Components"].values():
        for comp in components:
            if comp['id'][0:3] != 'PSU':
                compName.append(comp['id'].casefold())
            name = comp['id'] + '.part'
            with open(os.path.join(path, name), 'w') as file:
                # Write the CPU name
                file.write("Name Intel Xeon\n")
                # Write the CPU type
                file.write(f"Type {comp['id'][0:3]}\n")
                # Write the CPU link
                file.write("Link https://www.intel.com/content/www/us/en/products/details/processors/xeon.html\n")
                # Write the CPU footprint
                file.write(f"Footprint {comp['x_dim']} {comp['y_dim']}\n")
                # Write the CPU thickness
                file.write(f"Thickness {comp['z_dim']}\n")
                # Write the CPU material
                file.write(f"Material {comp['material']}\n")
                # Write the CPU activation energy
                #if 'activationEnergy' in comp:
                file.write(f"Activation_Energy {comp['activation_energy']}\n")
                
                # Check if heatsink data exists
                if 'heatsink' in comp:
                    if comp['heatsink']:
                        file.write("Heatsink\n")
                        heatsink_data = comp['heatsink']
                        # Write heatsink dimensions
                        file.write(f"\tdimensions {heatsink_data['x']} {heatsink_data['y']} {heatsink_data['z']} {heatsink_data['tb']} {heatsink_data['n_fins']} {heatsink_data['fin_width']}\n")
                        # Write heatsink material
                        file.write(f"\tmaterial {heatsink_data['material']}\n") 
    return compName
    
def createMacroScript(data, workFolder):
    data1 = {
        "Components": {
                "CPUs": data["cpus"],
                "GPUs": data["gpus"],
                "PSUs": data["psus"]
            }
        }
        
    header = '''# Input scripts:
Layout_script: ./layout_geometry_script.txt
Layer_stack: ./layer_stack.csv
Fig_dir: ./Figs
Solution_dir: ./Solutions
Constraint_file: ./constraint.csv
Model_char: ./Characterization

# Layout Generation Set up:
Design_Type: Server
'''

    option = '''New: 0
Plot_Solution: 1
Option: 1
Layout_Mode: 0

Thermal_Setup:
#	0 is the build in thermal model. 1 is the OpenFOAM model. 2 is the ParaPower model
Model_Select: 1
Measure_Name: Mean_Temperature(K)
'''
    
    script = "macro_script.txt"
    with open(os.path.join(workFolder, script), 'w') as file:  
        file.write(f"{header}")
        file.write(f"Reliability: {data['reliability']['mode']}\n")
        file.write(f"{option}")
        file.write("Selected_Devices: ")
        num = 1
        for comp in data1["Components"].values():  
            for device in comp:
                file.write(f"D{num},")
                num +=1
        
        file.write("\nDevice_Power: ")
        powers = []
        for comp in data1["Components"].values():  
            for device in comp:
                powers.append(str(device['power']))
        powers = ','.join(powers)
        file.write(f"{powers}")
        
        file.write(f"\nAmbient_Temperature: {data['boundary_conditions']['inlet_temperature']}")
        file.write("\nHeat_Convection: 95") 
        file.write("\nEnd_Thermal_Setup.\n")
        file.write("\n# OpenFOAM Setup")
        if data['reliability']['mode']:
            file.write(f"\nTest_Temperature: {data['reliability']['test_temperature']}")
        file.write(f"\nVelocity: {data['boundary_conditions']['air_velocity']}")
        file.write(f"\nDirection: {data['boundary_conditions']['air_direction']}")
        file.write(f"\nTIM_Thickness: {data['boundary_conditions']['tim_thickness']}")
        file.write(f"\nTIM_Kappa: {data['boundary_conditions']['tim_kappa']}")
        file.write(f"\nNumber_Core: {data['solver_settings']['number_of_cores']}")
        file.write(f"\nIteration: {data['solver_settings']['iteration']}")
        file.write(f"\nCabinet_Size: {data['define_server']['cabinet']['x']},{data['define_server']['cabinet']['y']},{data['define_server']['cabinet']['z']}")
                                
def createLayerStack(data, workFolder):
    
    name = "layer_stack.csv"
    
    with open(os.path.join(workFolder, name), 'w') as file:
        file.write("ID,Name,Origin,Width,Length,Thickness,Material,Type,Electrical\n")
        file.write(f"1,Baseplate,\"0,0\",{data['define_server']['pcb']['x']},{data['define_server']['pcb']['y']},{data['define_server']['pcb']['z']},copper,p,F\n")
        file.write(f"2,Bottom_Metal,\"0,0\",{data['define_server']['pcb']['x']},{data['define_server']['pcb']['y']},{data['define_server']['pcb']['z']},copper,p,G\n")
        file.write(f"3,Ceramic1,\"0,0\",{data['define_server']['pcb']['x']},{data['define_server']['pcb']['y']},1,Al_N,p,D\n")
        file.write(f"4,I1,\"0,0\",{data['define_server']['pcb']['x']},{data['define_server']['pcb']['y']},{data['define_server']['pcb']['z']},copper,p,S\n")
        file.write(f"5,C1,,{data['define_server']['pcb']['x']},{data['define_server']['pcb']['y']},1,SiC,a,C")
        
def createLayoutScripts(data, workFolder):
    data1 = {
        "Components": {
                "CPUs": data["cpus"],
                "GPUs": data["gpus"],
                "PSUs": data["psus"]
            }
        }
        
    script = "layout_geometry_script.txt" 
    with open(os.path.join(workFolder, script), 'w') as file:  
        file.write("# Definition\n")
        for comp in data1["Components"].values():
            for device in comp:
                file.write(f"{device['id']} ./Part_Lib/{device['id']}.part\n")
            
        file.write("# Layout Information\n")
        file.write("I1 Z+\n")
        file.write(f"+ T1 power 1 1 {int(data['define_server']['pcb']['x']) - 2} {int(data['define_server']['pcb']['y']) - 2}\n")
        
        num = 1
        for comp in data1["Components"].values():  
            for device in comp:
                file.write(f"\t+ D{num} {device['id']} {device['x_location']} {device['y_location']}\n")
                num +=1
                
def createConstrateFile(data, workFolder):

    script = "constraint.csv"
    
    text = '''Min Dimensions,EMPTY,power_trace,bonding wire pad,power_lead,signal_lead
MinWidth,1,1,0,3.0,1
MinLength,1,1,0,3.0,1
MinHorExtension,1,1,0,3.0,1
MinVerExtension,1,1,0,3.0,1
MinHorEnclosure,EMPTY,power_trace,bonding wire pad,power_lead,signal_lead
EMPTY,1,1,1,1,1
power_trace,1,1,1,1,1
bonding wire pad,1,1,1,1,1
power_lead,1,1,1,1,1
signal_lead,1,1,1,1,1
MinVerEnclosure,EMPTY,power_trace,bonding wire pad,power_lead,signal_lead
EMPTY,1,1,1,1,1
power_trace,1,1,1,1,1
bonding wire pad,1,1,1,1,1
power_lead,1,1,1,1,1
signal_lead,1,1,1,1,1
MinHorSpacing,EMPTY,power_trace,bonding wire pad,power_lead,signal_lead
EMPTY,1,1,1,1,1
power_trace,1,1,1,1,1
bonding wire pad,1,1,1,1,1
power_lead,1,1,1,1,1
signal_lead,1,1,1,1,1
MinVerSpacing,EMPTY,power_trace,bonding wire pad,power_lead,signal_lead
EMPTY,1,1,1,1,1
power_trace,1,1,1,1,1
bonding wire pad,1,1,1,1,1
power_lead,1,1,1,1,1
signal_lead,1,1,1,1,1'''
    
    with open(os.path.join(workFolder, script), 'w') as file:  
        file.write(f"{text}")    

def runPowerSynth(data, Core):
    try:
        workFolder = os.path.join(Core.PSRoot, 'pkg', 'work', 'Sample_Designs', data["case_study"]["name"])
        macro_script_path = os.path.join(workFolder, 'macro_script.txt')
        cli = PS2CLI(macro_script_path)
        ExitCode = cli.run()
        return ExitCode
    except:
        print('error ------------------------------------------')
    print("Process stopped!")

class CustomNavigationToolbar(NavigationToolbar):
    """ add checkbox to toolbar for picking event."""
    # Remove Back and Pan buttons
    toolitems = [t for t in NavigationToolbar.toolitems 
                 if t[0] not in ('Forward', 'Back', 'Pan')]
    
    def __init__(self, canvas, parent, region_data, plots):
        super().__init__(canvas, parent)
        self.data = region_data
        self.plots = plots
        
        # Create message visibility checkbox
        self.message_checkbox = QCheckBox("Show Messages")
        self.message_checkbox.setChecked(True)
        self.message_checkbox.stateChanged.connect(self.toggle_message_visibility)
        
        # Add separator and checkbox to toolbar
        self.addSeparator()
        self.addWidget(self.message_checkbox)
        
        # Find and store the message label
        self.message_label = None
        for child in self.findChildren(QLabel):
            if isinstance(child, QLabel) and child.text() == "":
                self.message_label = child
                break
        
        # Internal flag to track message visibility
        self.message_visible = True

    def toggle_message_visibility(self, state):
        """Toggle visibility flag based on checkbox state"""
        self.message_visible = bool(state)
        
    def set_message(self, s):
        """Override to control message display based on checkbox state"""
        if self.message_visible:
            # Show message if checkbox is checked
            self.canvas.mpl_connect('button_press_event', self.on_pick)
        
        else:
            super().set_message("")
    
    def on_pick(self, event):
        """Efficient point picking handler"""
        # Only process if picking is enabled
        if not self.message_visible:
            return
            
        # Only process left mouse clicks
        if event.button != 1:
            return
            
        # Only process events within the axes
        if event.inaxes != self.canvas.figure.axes[0]:
            return
            
        # Get mouse coordinates
        x, y = event.xdata, event.ydata

        # Print coordinates to console
        #print(f"Picked point: x={x:.6f}, y={y:.6f}")
        
        # Combine data from visible regions for temperature lookup
        x_data, y_data, t_data = [], [], []
        for region, plot in self.plots.items():
            if plot.get_visible():
                rx, ry, rt = self.data[region]
                x_data.extend(rx)
                y_data.extend(ry)
                t_data.extend(rt)

        # Nearest neighbor or interpolation (using griddata for simplicity)
        temp = griddata((x_data, y_data), t_data, (x, y), method='nearest')
        super().set_message(f"({x:.0f},{y:.0f}): {temp:.2f} °C")
        
if __name__ == "__main__":
    print("----------------------PowerSynth Mostcool GUI version------------------")
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
        