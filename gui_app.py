#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSV到JSON转换工具 - PyQt图形界面版本
支持导入Excel/CSV文件，预览和编辑数据，然后导出为JSON格式
"""

import sys
import os
import json
import pandas as pd
from typing import Dict, Any, List, Optional
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QPushButton, QTableWidget, QTableWidgetItem, QFileDialog,
    QMessageBox, QLabel, QComboBox, QLineEdit, QTextEdit,
    QSplitter, QGroupBox, QGridLayout, QHeaderView, QTabWidget,
    QScrollArea, QFrame, QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIcon

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
from csv_to_json_converter import CSVToJSONConverter


class EditableTableWidget(QTableWidget):
    """可编辑的表格控件，支持下拉选择和限制选项"""
    
    tableDataChanged = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config_data = {}
        self.constraint_rules = {}
        # 设置大小策略，确保表格能够扩展
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # 连接信号
        self.itemChanged.connect(self.on_item_changed)
        
    def set_config_data(self, config_data: Dict[str, Any]):
        """设置配置数据，用于生成下拉选项"""
        self.config_data = config_data
        self._setup_constraint_rules()
        
    def _setup_constraint_rules(self):
        """设置约束规则"""
        self.constraint_rules = {
            '雷达': list(self.config_data.get('lidar_models', {}).keys()),
            '线结构光': list(self.config_data.get('linelaser_models', {}).keys()),
            '3dToF': list(self.config_data.get('threedtof_models', {}).keys()),
            'RGB': list(self.config_data.get('rgb_models', {}).keys()),
            '大小核通信': list(self.config_data.get('communication_types', {}).keys())
        }
        
    def setup_cell_constraints(self, row: int, col: int, cell_type: str):
        """为特定单元格设置约束"""
        if cell_type in self.constraint_rules:
            combo = QComboBox()
            combo.addItems(self.constraint_rules[cell_type])
            combo.setEditable(True)
            combo.currentTextChanged.connect(self.on_combo_changed)
            self.setCellWidget(row, col, combo)
            
    def on_combo_changed(self):
        """当下拉框改变时发出信号"""
        self.tableDataChanged.emit()
        
    def get_cell_value(self, row: int, col: int) -> str:
        """获取单元格值"""
        widget = self.cellWidget(row, col)
        if isinstance(widget, QComboBox):
            return widget.currentText()
        else:
            item = self.item(row, col)
            return item.text() if item else ""
            
    def set_cell_value(self, row: int, col: int, value: str):
        """设置单元格值"""
        widget = self.cellWidget(row, col)
        if isinstance(widget, QComboBox):
            widget.setCurrentText(value)
        else:
            item = QTableWidgetItem(str(value))
            self.setItem(row, col, item)
            
    def on_item_changed(self, item):
        """表格项改变事件"""
        self.tableDataChanged.emit()


class CSVJsonConverterGUI(QMainWindow):
    """CSV到JSON转换器的图形界面"""
    
    def __init__(self):
        super().__init__()
        # 获取当前脚本所在目录，构建配置文件的绝对路径
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(current_dir, "config", "mapping_config.json")
        self.converter = CSVToJSONConverter(config_path)
        self.current_file_path = None
        self.data_frame = None
        
        self.init_ui()
        self.load_config()
        
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle("CSV到JSON转换工具")
        self.setGeometry(100, 100, 1200, 800)
        
        # 创建中央窗口
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # 创建工具栏
        self.create_toolbar(main_layout)
        
        # 创建分割器
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter, 1)  # 设置拉伸因子为1，让分割器占用剩余空间
        
        # 创建左侧面板（数据表格）
        self.create_data_panel(splitter)
        
        # 创建右侧面板（配置和预览）
        self.create_config_panel(splitter)
        
        # 设置分割器比例
        splitter.setSizes([800, 400])
        
        # 创建状态栏
        self.statusBar().showMessage("就绪 - 请导入CSV或Excel文件")
        
    def create_toolbar(self, parent_layout):
        """创建工具栏"""
        toolbar_layout = QHBoxLayout()
        
        # 导入按钮
        self.import_btn = QPushButton("导入文件")
        self.import_btn.clicked.connect(self.import_file)
        toolbar_layout.addWidget(self.import_btn)
        
        # 保存按钮
        self.save_btn = QPushButton("保存CSV")
        self.save_btn.clicked.connect(self.save_csv)
        self.save_btn.setEnabled(False)
        toolbar_layout.addWidget(self.save_btn)
        
        # 导出JSON按钮
        self.export_json_btn = QPushButton("导出JSON")
        self.export_json_btn.clicked.connect(self.export_json)
        self.export_json_btn.setEnabled(False)
        toolbar_layout.addWidget(self.export_json_btn)
        
        # 导出YAML按钮
        self.export_yaml_btn = QPushButton("导出YAML")
        self.export_yaml_btn.clicked.connect(self.export_yaml)
        self.export_yaml_btn.setEnabled(False)
        toolbar_layout.addWidget(self.export_yaml_btn)
        
        # 添加弹性空间
        toolbar_layout.addStretch()
        
        # 文件路径标签
        self.file_label = QLabel("未选择文件")
        toolbar_layout.addWidget(self.file_label)
        
        parent_layout.addLayout(toolbar_layout)
        
    def create_data_panel(self, parent):
        """创建数据面板"""
        data_widget = QWidget()
        data_layout = QVBoxLayout(data_widget)
        
        # 数据表格标题
        data_label = QLabel("数据预览和编辑")
        data_label.setFont(QFont("Arial", 12, QFont.Bold))
        data_layout.addWidget(data_label)
        
        # 创建可编辑表格
        self.data_table = EditableTableWidget()
        self.data_table.tableDataChanged.connect(self.on_data_changed)
        data_layout.addWidget(self.data_table, 1)  # 设置拉伸因子为1，让表格占用剩余空间
        
        parent.addWidget(data_widget)
        
    def create_config_panel(self, parent):
        """创建配置面板"""
        config_widget = QWidget()
        config_layout = QVBoxLayout(config_widget)
        
        # 创建标签页
        tab_widget = QTabWidget()
        
        # 配置标签页
        self.create_config_tab(tab_widget)
        
        # JSON预览标签页
        self.create_preview_tab(tab_widget)
        
        config_layout.addWidget(tab_widget)
        parent.addWidget(config_widget)
        
    def create_config_tab(self, tab_widget):
        """创建配置标签页"""
        config_tab = QWidget()
        config_layout = QVBoxLayout(config_tab)
        
        # 配置标题
        config_label = QLabel("映射配置")
        config_label.setFont(QFont("Arial", 11, QFont.Bold))
        config_layout.addWidget(config_label)
        
        # 配置编辑区域
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        # 传感器类型配置
        self.create_sensor_config_group(scroll_layout)
        
        # 通信类型配置
        self.create_comm_config_group(scroll_layout)
        
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        config_layout.addWidget(scroll_area)
        
        # 保存配置按钮
        save_config_btn = QPushButton("保存配置")
        save_config_btn.clicked.connect(self.save_config)
        config_layout.addWidget(save_config_btn)
        
        tab_widget.addTab(config_tab, "配置")
        
    def create_sensor_config_group(self, parent_layout):
        """创建传感器配置组"""
        sensor_group = QGroupBox("传感器配置")
        sensor_layout = QGridLayout(sensor_group)
        
        # 这里可以添加传感器配置的具体控件
        info_label = QLabel("传感器映射配置将在这里显示")
        sensor_layout.addWidget(info_label, 0, 0)
        
        parent_layout.addWidget(sensor_group)
        
    def create_comm_config_group(self, parent_layout):
        """创建通信配置组"""
        comm_group = QGroupBox("通信配置")
        comm_layout = QGridLayout(comm_group)
        
        # 这里可以添加通信配置的具体控件
        info_label = QLabel("通信映射配置将在这里显示")
        comm_layout.addWidget(info_label, 0, 0)
        
        parent_layout.addWidget(comm_group)
        
    def create_preview_tab(self, tab_widget):
        """创建JSON预览标签页"""
        # JSON预览标签页
        json_preview_tab = QWidget()
        json_preview_layout = QVBoxLayout(json_preview_tab)
        
        # JSON预览标题
        json_preview_label = QLabel("JSON预览")
        json_preview_label.setFont(QFont("Arial", 11, QFont.Bold))
        json_preview_layout.addWidget(json_preview_label)
        
        # JSON预览文本框
        self.json_preview = QTextEdit()
        self.json_preview.setFont(QFont("Consolas", 10))
        self.json_preview.setReadOnly(True)
        json_preview_layout.addWidget(self.json_preview)
        
        # JSON刷新预览按钮
        json_refresh_btn = QPushButton("刷新JSON预览")
        json_refresh_btn.clicked.connect(self.refresh_json_preview)
        json_preview_layout.addWidget(json_refresh_btn)
        
        tab_widget.addTab(json_preview_tab, "JSON预览")
        
        # YAML预览标签页
        yaml_preview_tab = QWidget()
        yaml_preview_layout = QVBoxLayout(yaml_preview_tab)
        
        # YAML预览标题
        yaml_preview_label = QLabel("YAML预览")
        yaml_preview_label.setFont(QFont("Arial", 11, QFont.Bold))
        yaml_preview_layout.addWidget(yaml_preview_label)
        
        # YAML预览文本框
        self.yaml_preview = QTextEdit()
        self.yaml_preview.setFont(QFont("Consolas", 10))
        self.yaml_preview.setReadOnly(True)
        yaml_preview_layout.addWidget(self.yaml_preview)
        
        # YAML刷新预览按钮
        yaml_refresh_btn = QPushButton("刷新YAML预览")
        yaml_refresh_btn.clicked.connect(self.refresh_yaml_preview)
        yaml_preview_layout.addWidget(yaml_refresh_btn)
        
        tab_widget.addTab(yaml_preview_tab, "YAML预览")
        
    def load_config(self):
        """加载配置"""
        try:
            config = self.converter.load_config()
            self.data_table.set_config_data(config)
            self.statusBar().showMessage("配置加载成功")
        except Exception as e:
            QMessageBox.warning(self, "警告", f"加载配置失败: {str(e)}")
            
    def import_file(self):
        """导入文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择文件", "", 
            "支持的文件 (*.csv *.xlsx *.xls);;CSV文件 (*.csv);;Excel文件 (*.xlsx *.xls)"
        )
        
        if file_path:
            try:
                self.load_file_data(file_path)
                self.current_file_path = file_path
                self.file_label.setText(f"当前文件: {os.path.basename(file_path)}")
                self.statusBar().showMessage(f"文件导入成功: {os.path.basename(file_path)}")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"导入文件失败: {str(e)}")
                
    def load_file_data(self, file_path: str):
        """加载文件数据"""
        try:
            if file_path.endswith('.csv'):
                # 尝试不同编码读取CSV
                encodings = ['utf-8', 'gbk', 'gb2312', 'utf-8-sig']
                for encoding in encodings:
                    try:
                        self.data_frame = pd.read_csv(file_path, encoding=encoding, header=None)
                        break
                    except UnicodeDecodeError:
                        continue
                if self.data_frame is None:
                    raise ValueError("无法读取CSV文件，请检查文件编码")
            else:
                # Excel文件
                self.data_frame = pd.read_excel(file_path, header=None)
                
            # 填充表格
            self.populate_table()
            
            # 启用按钮
            self.save_btn.setEnabled(True)
            self.export_json_btn.setEnabled(True)
            self.export_yaml_btn.setEnabled(True)
            
        except Exception as e:
            raise Exception(f"读取文件失败: {str(e)}")
            
    def populate_table(self):
        """填充表格数据"""
        if self.data_frame is None:
            return
            
        # 设置表格大小
        rows, cols = self.data_frame.shape
        self.data_table.setRowCount(rows)
        self.data_table.setColumnCount(cols)
        
        # 设置表头
        headers = [f"列{i+1}" for i in range(cols)]
        self.data_table.setHorizontalHeaderLabels(headers)
        
        # 填充数据
        for row in range(rows):
            for col in range(cols):
                value = self.data_frame.iloc[row, col]
                if pd.isna(value):
                    value = ""
                else:
                    value = str(value)
                    
                self.data_table.set_cell_value(row, col, value)
                
                # 为特定列设置约束
                if col == 2 and row > 0:  # 传感器类型列
                    sensor_type = self.data_table.get_cell_value(row, col)
                    if sensor_type in ['雷达', '线结构光', '3dToF', 'RGB']:
                        self.data_table.setup_cell_constraints(row, col+1, sensor_type)
                        
        # 调整列宽
        self.data_table.resizeColumnsToContents()
        
    def on_data_changed(self):
        """数据改变事件"""
        self.refresh_json_preview()
        self.refresh_yaml_preview()
        
    def save_csv(self):
        """保存CSV文件"""
        if self.data_frame is None:
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存CSV文件", "", "CSV文件 (*.csv)"
        )
        
        if file_path:
            try:
                # 从表格获取当前数据
                updated_data = self.get_table_data()
                updated_df = pd.DataFrame(updated_data)
                updated_df.to_csv(file_path, index=False, header=False, encoding='utf-8')
                QMessageBox.information(self, "成功", "CSV文件保存成功！")
                self.statusBar().showMessage(f"CSV文件已保存: {os.path.basename(file_path)}")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"保存CSV文件失败: {str(e)}")
                
    def get_table_data(self) -> List[List[str]]:
        """获取表格数据"""
        data = []
        for row in range(self.data_table.rowCount()):
            row_data = []
            for col in range(self.data_table.columnCount()):
                value = self.data_table.get_cell_value(row, col)
                row_data.append(value)
            data.append(row_data)
        return data
        
    def export_json(self):
        """导出JSON文件"""
        if self.data_frame is None:
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self, "导出JSON文件", "", "JSON文件 (*.json)"
        )
        
        if file_path:
            try:
                # 先保存当前数据到临时CSV文件
                temp_csv = "temp_export.csv"
                updated_data = self.get_table_data()
                updated_df = pd.DataFrame(updated_data)
                updated_df.to_csv(temp_csv, index=False, header=False, encoding='utf-8')
                
                # 使用转换器转换为JSON
                json_str = self.converter.convert_csv_to_json(temp_csv, file_path)
                
                # 删除临时文件
                if os.path.exists(temp_csv):
                    os.remove(temp_csv)
                    
                QMessageBox.information(self, "成功", "JSON文件导出成功！")
                self.statusBar().showMessage(f"JSON文件已导出: {os.path.basename(file_path)}")
                
            except Exception as e:
                QMessageBox.critical(self, "错误", f"导出JSON文件失败: {str(e)}")
                
    def export_yaml(self):
        """导出YAML文件"""
        if self.data_frame is None:
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self, "导出YAML文件", "", "YAML文件 (*.yaml *.yml)"
        )
        
        if file_path:
            try:
                # 先保存当前数据到临时CSV文件
                temp_csv = "temp_yaml_export.csv"
                updated_data = self.get_table_data()
                updated_df = pd.DataFrame(updated_data)
                updated_df.to_csv(temp_csv, index=False, header=False, encoding='utf-8')
                
                # 使用转换器转换为YAML
                yaml_str = self.converter.convert_csv_to_yaml(temp_csv, file_path)
                
                # 删除临时文件
                if os.path.exists(temp_csv):
                    os.remove(temp_csv)
                    
                QMessageBox.information(self, "成功", "YAML文件导出成功！")
                self.statusBar().showMessage(f"YAML文件已导出: {os.path.basename(file_path)}")
                
            except Exception as e:
                QMessageBox.critical(self, "错误", f"导出YAML文件失败: {str(e)}")
            
    def refresh_json_preview(self):
        """刷新JSON预览"""
        if self.data_frame is None:
            self.json_preview.setText("请先导入文件")
            return
            
        try:
            # 创建临时CSV文件进行转换
            temp_csv = "temp_preview.csv"
            updated_data = self.get_table_data()
            updated_df = pd.DataFrame(updated_data)
            updated_df.to_csv(temp_csv, index=False, header=False, encoding='utf-8')
            
            # 转换为JSON
            json_str = self.converter.convert_csv_to_json(temp_csv)
            
            # 删除临时文件
            if os.path.exists(temp_csv):
                os.remove(temp_csv)
                
            # 格式化JSON显示
            json_obj = json.loads(json_str)
            formatted_json = json.dumps(json_obj, indent=2, ensure_ascii=False)
            self.json_preview.setText(formatted_json)
            
        except Exception as e:
            self.json_preview.setText(f"预览生成失败: {str(e)}")
            
    def refresh_yaml_preview(self):
        """刷新YAML预览"""
        if self.data_frame is None:
            self.yaml_preview.setText("请先导入文件")
            return
            
        try:
            # 创建临时CSV文件进行转换
            temp_csv = "temp_yaml_preview.csv"
            updated_data = self.get_table_data()
            updated_df = pd.DataFrame(updated_data)
            updated_df.to_csv(temp_csv, index=False, header=False, encoding='utf-8')
            
            # 转换为YAML (静默模式，不打印消息)
            yaml_str = self.converter.convert_csv_to_yaml(temp_csv, silent=True)
            
            # 删除临时文件
            if os.path.exists(temp_csv):
                os.remove(temp_csv)
                
            self.yaml_preview.setText(yaml_str)
            
        except Exception as e:
            self.yaml_preview.setText(f"YAML预览生成失败: {str(e)}")
            
    def save_config(self):
        """保存配置"""
        QMessageBox.information(self, "提示", "配置保存功能待实现")


def main():
    """主函数"""
    print("=== CSV到JSON转换工具 - 图形界面版本 ===")
    
    # 创建应用程序
    app = QApplication(sys.argv)
    
    # 创建主窗口
    window = CSVJsonConverterGUI()
    window.show()
    
    # 运行应用程序
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()