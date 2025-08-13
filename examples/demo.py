#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
演示脚本 - 展示GUI应用程序的主要功能
"""

import os
import sys
import pandas as pd

def create_demo_excel():
    """创建演示用的Excel文件"""
    print("创建演示Excel文件...")
    
    # 创建演示数据
    demo_data = [
        ['Version', '', 'Type', 'Sensor', '参数解释'],
        ['2537', 'Sensor', '雷达', '欢创PMA2', '选择与项目适配的雷达，没有选无'],
        ['', '', '雷达安装距离', '0.068', '(与机器中心距离，单位m)'],
        ['', '', '雷达安装角度', '118', '(与机器中垂线偏差角度，顺时针为正，单位度)'],
        ['', '', '线结构光', '一微ALF03', '选择与项目适配的线激光，没有选无'],
        ['', '', '线结构光距离偏差', '0', '(与机器中心距离，单位m)'],
        ['', '', '线结构光安装高度', '0', '(距地面高度，单位m)'],
        ['', '', '线结构光标准可视距离', '0', '(标准工装下理想可视距离，单位m)'],
        ['', '', '3dToF', '光鉴Nebula280', '选择与项目适配的3dtof，没有选无'],
        ['', '', '3DTOF距离偏差', '0', '(与机器中心距离，单位m)'],
        ['', '', '3DTOF安装高度', '0', '(距地面高度，单位m)'],
        ['', '', '3DTOF安装左右偏差', '0', '(接受端距离机器中垂线的距离，单位m)'],
        ['', '', 'RGB', '', '选择与项目适配的RGB模组，没有选无'],
        ['', 'Trans', '大小核通信', 'rpmsg', '选择与项目适配的ipc通信方式']
    ]
    
    # 创建DataFrame
    df = pd.DataFrame(demo_data)
    
    # 保存为Excel文件
    demo_file = 'demo_data.xlsx'
    df.to_excel(demo_file, index=False, header=False)
    
    print(f"✓ 演示Excel文件已创建: {demo_file}")
    return demo_file

def show_gui_features():
    """展示GUI功能特性"""
    print("\n=== CSV到JSON转换工具 - GUI功能特性 ===")
    print()
    print("🎯 主要功能:")
    print("  1. 文件导入 - 支持Excel (.xlsx, .xls) 和CSV (.csv) 文件")
    print("  2. 数据预览 - 在表格中查看和编辑数据")
    print("  3. 智能编辑 - 传感器型号自动提供下拉选项")
    print("  4. 实时预览 - 在JSON预览标签页查看转换结果")
    print("  5. 数据导出 - 保存为CSV或导出为JSON格式")
    print()
    print("🔧 界面布局:")
    print("  ├── 工具栏")
    print("  │   ├── 导入文件按钮")
    print("  │   ├── 保存CSV按钮")
    print("  │   ├── 导出JSON按钮")
    print("  │   └── 当前文件显示")
    print("  ├── 左侧面板 - 数据预览和编辑表格")
    print("  └── 右侧面板")
    print("      ├── 配置标签页 - 映射配置管理")
    print("      └── JSON预览标签页 - 实时转换结果")
    print()
    print("⚡ 智能特性:")
    print("  • 传感器型号约束 - 根据传感器类型自动限制可选型号")
    print("  • 配置文件集成 - 使用mapping_config.json进行映射")
    print("  • 实时转换预览 - 编辑数据时自动更新JSON预览")
    print("  • 错误处理 - 友好的错误提示和状态显示")
    print()
    print("📋 使用步骤:")
    print("  1. 启动GUI: python gui_app.py")
    print("  2. 点击'导入文件'选择Excel或CSV文件")
    print("  3. 在表格中预览和编辑数据")
    print("  4. 使用下拉菜单选择传感器型号")
    print("  5. 在'JSON预览'标签页查看转换结果")
    print("  6. 点击'导出JSON'保存最终结果")

def show_config_info():
    """显示配置信息"""
    print("\n=== 配置文件说明 ===")
    print()
    print("📁 config/mapping_config.json - 映射配置文件")
    print("  包含以下映射类别:")
    print("  • sensor_types - 传感器类型映射")
    print("  • lidar_models - 雷达型号映射")
    print("  • linelaser_models - 线结构光型号映射")
    print("  • threedtof_models - 3dToF型号映射")
    print("  • rgb_models - RGB模组型号映射")
    print("  • communication_types - 通信类型映射")
    print("  • special_values - 特殊值处理")
    print()
    print("🔄 GUI会自动读取配置文件并:")
    print("  • 为传感器型号列提供下拉选项")
    print("  • 根据配置进行中英文映射")
    print("  • 验证数据有效性")

def main():
    """主演示函数"""
    print("=== CSV到JSON转换工具 - 演示程序 ===")
    print()
    
    # 创建演示文件
    demo_file = create_demo_excel()
    
    # 显示功能特性
    show_gui_features()
    
    # 显示配置信息
    show_config_info()
    
    print("\n=== 快速开始 ===")
    print(f"1. 演示文件已创建: {demo_file}")
    print("2. 启动GUI: python gui_app.py")
    print("3. 导入演示文件进行测试")
    print()
    print("💡 提示: 您也可以使用自己的Excel或CSV文件进行测试")
    print()
    
    return 0

if __name__ == "__main__":
    exit(main())