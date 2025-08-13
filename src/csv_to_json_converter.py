#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSV到JSON转换脚本
将编译选项CSV文件转换为指定的JSON格式
"""

import csv
import json
import os
from typing import Dict, Any, Optional

class CSVToJSONConverter:
    def __init__(self, config_file: str = "config/mapping_config.json"):
        """
        初始化转换器
        
        Args:
            config_file: 映射配置文件路径
        """
        self.config_file = config_file
        self.config = self.load_config()
        
        # 从配置文件构建映射表
        self.chinese_to_english_map = {}
        self._build_mapping_from_config()
    
    def load_config(self) -> Dict[str, Any]:
        """
        加载映射配置文件
        """
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"警告: 配置文件 {self.config_file} 不存在，使用默认配置")
            return self._get_default_config()
        except json.JSONDecodeError as e:
            print(f"错误: 配置文件格式错误 - {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """
        获取默认配置
        """
        return {
            "sensor_types": {
                "雷达": "lidar",
                "线结构光": "linelaser",
                "3dToF": "threedtof",
                "RGB": "rgb"
            },
            "communication_types": {
                "大小核通信": "ipc"
            },
            "lidar_models": {
                "乐动STL50": "camsense_pma2_lidar",
                "欢创PMA2": "camsense_pma2_lidar",
                "无": None
            },
            "linelaser_models": {
                "一微ALF03": "yiwei_alf03_linelaser",
                "无": None
            },
            "threedtof_models": {
                "光鉴Nebula280": "guangjian_nebula280_3dtof",
                "无": None
            },
            "rgb_models": {
                "无": None
            },
            "special_values": {
                "无": None,
                "": None
            },
            "project_prefix": "project_"
        }
    
    def _build_mapping_from_config(self):
        """
        从配置文件构建映射表
        """
        # 合并所有映射到一个字典中
        categories = ["sensor_types", "communication_types", "lidar_models", "linelaser_models", 
                     "threedtof_models", "rgb_models", "special_values"]
        
        for category in categories:
            if category in self.config:
                self.chinese_to_english_map.update(self.config[category])
        
        # 兼容旧的sensor_models配置
        if "sensor_models" in self.config:
            self.chinese_to_english_map.update(self.config["sensor_models"])
        
        # 添加固定的类型映射
        self.chinese_to_english_map.update({
            "Sensor": "sensor",
            "Trans": "comm",
            "rpmsg": "ipc"
        })
    
    def normalize_sensor_name(self, sensor_type: str, model: str) -> Optional[str]:
        """
        根据传感器类型和型号生成标准化名称
        """
        # 检查特殊值
        if model in self.config.get("special_values", {}):
            return self.config["special_values"][model]
        
        if not model or model.strip() == "":
            return None
            
        # 根据传感器类型确定对应的配置类别
        sensor_type_en = self.chinese_to_english_map.get(sensor_type, sensor_type.lower())
        config_key = f"{sensor_type_en}_models"
        
        # 优先使用配置文件中的分类映射
        if config_key in self.config and model in self.config[config_key]:
            return self.config[config_key][model]
        
        # 兼容旧的sensor_models配置
        if model in self.config.get("sensor_models", {}):
            return self.config["sensor_models"][model]
        
        # 如果没有直接映射，使用默认生成规则：厂商_型号_类型
        model_normalized = model.lower().replace(" ", "_").replace("-", "_")
        return f"{model_normalized}_{sensor_type_en}"
    
    def parse_csv_to_dict(self, csv_file_path: str) -> Dict[str, Any]:
        """
        解析CSV文件并转换为字典结构
        """
        result = {}
        
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            rows = list(csv_reader)
            
            if not rows:
                return result
            
            # 获取项目版本作为项目ID
            project_version = rows[1][0] if len(rows) > 1 and rows[1][0] else "unknown"
            project_prefix = self.config.get("project_prefix", "project_")
            project_id = f"{project_prefix}{project_version}"
            
            # 初始化项目结构
            project_data = {
                "sensor": {
                    "lidar": None,
                    "linelaser": None,
                    "threedtof": None,
                    "rgb": None
                },
                "comm": {},
                "body": {}
            }
            
            sensor_params = {}
            robot_params = {}
            
            # 解析CSV数据
            current_group = None
            for row in rows[1:]:  # 跳过标题行
                if len(row) < 4:
                    continue
                    
                version, group, type_name, value = row[0], row[1], row[2], row[3]
                
                # 如果group不为空，更新当前组
                if group:
                    current_group = group
                
                # 处理传感器类型数据
                if current_group == "Sensor_Type" and type_name:
                    # 根据type_name确定传感器类型
                    sensor_key = self.chinese_to_english_map.get(type_name)
                    if sensor_key and sensor_key in project_data["sensor"]:
                        if value and value != "无":
                            normalized_name = self.normalize_sensor_name(type_name, value)
                            project_data["sensor"][sensor_key] = normalized_name
                        else:
                            project_data["sensor"][sensor_key] = None
                        
                # 处理通信数据
                elif current_group == "Trans" and type_name and value:
                    comm_key = self.chinese_to_english_map.get(type_name)
                    if comm_key:
                        comm_value = self.chinese_to_english_map.get(value, value)
                        project_data["comm"][comm_key] = comm_value
                
                # 处理传感器参数（如果有Define列的话）
                elif current_group == "Sensor_Parameter" and len(row) > 5:
                    define = row[5] if len(row) > 5 else None
                    if define and value and value != "无":
                        sensor_params[define] = self._convert_value(value)
                
                # 处理机器人参数
                elif current_group == "robot" and len(row) > 5:
                    define = row[5] if len(row) > 5 else None
                    if define and value:
                        robot_params[define] = self._convert_value(value)
            
            # 生成YAML文件
            if sensor_params or robot_params:
                self._generate_yaml_file(sensor_params, robot_params)
            
            result[project_id] = project_data
            
        return result
    
    def _convert_value(self, value: str):
        """
        转换值的类型
        """
        try:
            # 尝试转换为浮点数
            if '.' in value:
                return float(value)
            # 尝试转换为整数
            return int(value)
        except ValueError:
            # 保持字符串
            return value
    
    def _generate_yaml_file(self, sensor_params: Dict, robot_params: Dict, silent: bool = False):
        """
        生成YAML配置文件
        """
        yaml_content = []
        
        if sensor_params:
            yaml_content.append("sensor:")
            for key, value in sensor_params.items():
                comment = self._get_param_comment(key)
                if isinstance(value, str) and value.startswith('"') and value.endswith('"'):
                    yaml_content.append(f"  {key}: {value}           {comment}")
                else:
                    yaml_content.append(f"  {key}: {value}           {comment}")
        
        if robot_params:
            if yaml_content:
                yaml_content.append("")
            yaml_content.append("robot:")
            for key, value in robot_params.items():
                comment = self._get_param_comment(key)
                if isinstance(value, str) and value.startswith('"') and value.endswith('"'):
                    yaml_content.append(f"  {key}: {value}           {comment}")
                else:
                    yaml_content.append(f"  {key}: {value}           {comment}")
        
        # 确保输出目录存在
        os.makedirs("output", exist_ok=True)
        
        # 写入YAML文件
        with open("output/config.yaml", 'w', encoding='utf-8') as f:
            f.write("\n".join(yaml_content))
        
        # if not silent:
            # print(f"YAML配置文件已生成: output/config.yaml")
    
    def _get_param_comment(self, param_key: str) -> str:
        """
        获取参数的注释
        """
        comments = {
            "LaserSerialPort": "#laser 串口号",
            "LaserBiasDist": "#laser 距离偏差(m)",
            "LaserBiasAngle": "#laser 角度偏差(度)",
            "LineLaserSerialPort": "#linelaser 串口号",
            "LinelaserBias": "#linelaser x轴偏差(m)",
            "LinelaserHeight": "#linelaser 安装高度(m)",
            "LinelaserVisualRange": "#linelaser 可视距离(m)",
            "ThirdTofPort": "#3dtof 设备端口",
            "ThirdTofBiasDist": "#3dtof 距离偏差(m)",
            "ThirdTofBiasHight": "#3dtof 安装高度(m)",
            "ThirdTofBiasLeft": "#3dtof 安装左右偏差(m)",
            "RgbPort": "#rgb 设备端口",
            "robot_radius": "#机器人半径(m)",
            "RobotRadius": "#机器人半径(m)"
        }
        return comments.get(param_key, "#参数")
    
    def convert_csv_to_json(self, csv_file_path: str, output_json_path: str = None) -> str:
        """
        将CSV文件转换为JSON格式
        """
        # 解析CSV
        data_dict = self.parse_csv_to_dict(csv_file_path)
        
        # 转换为JSON字符串
        json_str = json.dumps(data_dict, indent=4, ensure_ascii=False)
        
        # 如果指定了输出路径，保存到文件
        if output_json_path:
            with open(output_json_path, 'w', encoding='utf-8') as f:
                f.write(json_str)
            print(f"JSON文件已保存到: {output_json_path}")
        
        return json_str
    
    def convert_csv_to_yaml(self, csv_file_path: str, output_yaml_path: str = None, silent: bool = False) -> str:
        """
        将CSV文件转换为YAML格式
        """
        # 解析CSV获取参数
        sensor_params = {}
        robot_params = {}
        
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            rows = list(csv_reader)
            
            current_group = None
            for row in rows[1:]:  # 跳过标题行
                if len(row) < 4:
                    continue
                    
                version, group, type_name, value = row[0], row[1], row[2], row[3]
                
                # 如果group不为空，更新当前组
                if group:
                    current_group = group
                
                # 处理传感器参数（如果有Define列的话）
                if current_group == "Sensor_Parameter" and len(row) > 5:
                    define = row[5] if len(row) > 5 else None
                    if define and value and value != "无":
                        sensor_params[define] = self._convert_value(value)
                
                # 处理机器人参数
                elif current_group == "robot" and len(row) > 5:
                    define = row[5] if len(row) > 5 else None
                    if define and value:
                        robot_params[define] = self._convert_value(value)
        
        # 生成YAML内容
        yaml_content = []
        
        if sensor_params:
            yaml_content.append("sensor:")
            for key, value in sensor_params.items():
                comment = self._get_param_comment(key)
                yaml_content.append(f"  {key}: {value}           {comment}")
        
        if robot_params:
            if yaml_content:
                yaml_content.append("")
            yaml_content.append("robot:")
            for key, value in robot_params.items():
                comment = self._get_param_comment(key)
                yaml_content.append(f"  {key}: {value}           {comment}")
        
        yaml_str = "\n".join(yaml_content)
        
        # 如果指定了输出路径，保存到文件
        if output_yaml_path:
            with open(output_yaml_path, 'w', encoding='utf-8') as f:
                f.write(yaml_str)
            if not silent:
                print(f"YAML文件已保存到: {output_yaml_path}")
        
        return yaml_str


def main():
    """
    主函数
    """
    converter = CSVToJSONConverter()
    
    # CSV文件路径
    csv_file = "data/脚本_参数_编译选项_测试标准 - 编译选项.csv"
    
    # 检查文件是否存在
    if not os.path.exists(csv_file):
        print(f"错误: 找不到CSV文件 {csv_file}")
        return
    
    # 转换为JSON
    json_output = converter.convert_csv_to_json(csv_file, "output/result.json")
    print(f"✅ 转换完成！输出文件: output/result.json")

if __name__ == "__main__":
    main()