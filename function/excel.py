# function/excel.py

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableView, QComboBox, QHeaderView, QPushButton, QHBoxLayout
from PyQt5.QtCore import QAbstractTableModel, Qt, pyqtSignal
import sys
import pandas as pd

class DataFrameModel(QAbstractTableModel):
    def __init__(self, df=pd.DataFrame(), parent=None):
        super().__init__(parent)
        self._df = df

    def rowCount(self, parent=None):
        return len(self._df)

    def columnCount(self, parent=None):
        return len(self._df.columns)

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid() and role == Qt.DisplayRole:
            return str(self._df.iloc[index.row(), index.column()])
        return None

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._df.columns[section])
            elif orientation == Qt.Vertical:
                return str(self._df.index[section])
        return None

class DataFrameViewer(QWidget):
    def __init__(self, dataframe, width=1600, height=800):
        super().__init__()
        self.setWindowTitle("Excel Data")
        self.setGeometry(100, 100, width, height)
        self.layout = QVBoxLayout(self)

        self.filter_panel = QHBoxLayout()
        self.filters = []

        self.table = QTableView()
        self.model = DataFrameModel(dataframe)
        self.table.setModel(self.model)

        # 添加篩選器
        for col in range(dataframe.shape[1]):
            combo = QComboBox()
            unique_values = ["All"] + sorted(dataframe.iloc[:, col].astype(str).unique().tolist())
            combo.addItems(unique_values)
            combo.currentIndexChanged.connect(lambda index, col=col: self.apply_filter(col, combo.currentText()))
            self.filters.append(combo)
            self.filter_panel.addWidget(combo)
            combo.adjustSize()

        self.layout.addLayout(self.filter_panel)
        self.layout.addWidget(self.table)

        self.table.horizontalHeader().sectionResized.connect(self.adjust_filter_width)

        self.reset_button = QPushButton("重置篩選")
        self.reset_button.clicked.connect(self.reset_filters)
        self.layout.addWidget(self.reset_button)

        self.original_dataframe = dataframe

    def adjust_filter_width(self, index, oldSize, newSize):
        if index < len(self.filters):
            self.filters[index].setFixedWidth(newSize)

    def apply_filter(self, col, filter_value):
        if filter_value != "All":
            filtered_df = self.original_dataframe[self.original_dataframe.iloc[:, col].astype(str) == filter_value]
        else:
            filtered_df = self.original_dataframe.copy()
        self.model = DataFrameModel(filtered_df)
        self.table.setModel(self.model)

    def reset_filters(self):
        for combo in self.filters:
            combo.setCurrentIndex(0)  # Reset to "All"
        self.apply_filter(None, None)

def show_dataframe(dataframe, width=1600, height=800):
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    viewer = DataFrameViewer(dataframe, width, height)
    viewer.show()
    app.exec_()