#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSV到JSON转换工具 - 简化版
直接执行即可完成转换，您只需维护 config/mapping_config.json 配置文件
"""

import sys
import os
import glob

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from csv_to_json_converter import CSVToJSONConverter

def main():
    """
    主函数：执行CSV到JSON转换
    """
    print("=== CSV到JSON转换工具 ===")

    # 初始化转换器
    converter = CSVToJSONConverter()

    # 自动查找data文件夹下的CSV文件
    csv_files = glob.glob("data/*.csv")

    if not csv_files:
        print("❌ 在data文件夹下未找到CSV文件")
        return 1

    # 使用第一个找到的CSV文件
    csv_file = csv_files[0]

    # 输出JSON文件路径
    output_file = "output/result.json"

    try:
        # 执行转换
        print(f"正在转换: {csv_file}")
        converter.convert_csv_to_json(csv_file, output_file)
        print(f"\n✅ 转换完成！")
        print(f"📁 输出文件: {output_file}")
        print(f"⚙️  配置文件: config/mapping_config.json")
        
    except FileNotFoundError as e:
        print(f"❌ 文件未找到: {e}")
        print("请确保CSV文件存在于 data/ 目录中")
    except Exception as e:
        print(f"❌ 转换失败: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())