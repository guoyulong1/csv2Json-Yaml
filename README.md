# CSV到JSON/YAML转换工具

一个专业的CSV到JSON/YAML转换工具，专门用于将传感器配置CSV文件转换为标准化的JSON和YAML格式。

## ✨ 功能特性

- **双格式输出**：同时支持JSON和YAML格式输出
- **图形界面**：提供直观的GUI界面，支持文件导入、数据预览编辑和文件导出
- **命令行工具**：适合批处理和自动化场景
- **传感器配置**：专门针对雷达、线结构光、3D ToF、RGB等传感器类型优化
- **参数映射**：支持中文到英文的智能映射转换
- **实时预览**：支持JSON和YAML内容的实时预览

## 🚀 快速开始

### 环境要求
- Python 3.7+
- tkinter（通常随Python安装）
- PyYAML

### 安装依赖
```bash
pip install -r requirements.txt
```

### 图形界面版本（推荐）
```bash
python gui_app.py
```
### 命令行版本
```bash
python convert.py
```

## 📁 项目结构

```
├── gui_app.py              # Tkinter图形界面主程序
├── convert.py              # 命令行转换脚本
├── requirements.txt        # Python依赖项
├── config/
│   └── mapping_config.json # 传感器映射配置文件
├── data/                   # CSV数据文件目录
├── output/                 # 输出目录（JSON和YAML文件）
├── examples/               # 示例文件
├── docs/                   # 文档目录
└── src/
    └── csv_to_json_converter.py  # 核心转换器模块
```

## 💡 使用说明

### GUI界面操作
1. 启动程序后，点击"导入CSV文件"选择数据文件
2. 在"数据表格"标签页中预览和编辑数据
3. 在"JSON预览"标签页查看JSON格式转换结果
4. 在"YAML预览"标签页查看YAML格式转换结果
5. 点击"导出JSON"或"导出YAML"保存文件

### 命令行操作
1. 将CSV文件放入 `data/` 目录
2. 运行 `python convert.py`
3. 结果文件将保存到 `output/` 目录

## ⚙️ 配置说明

### 映射配置文件

编辑 `config/mapping_config.json` 来管理传感器映射关系：

```json
{
  "sensor_types": {
    "雷达": "lidar",
    "线结构光": "linelaser",
    "3dToF": "threedtof",
    "RGB": "rgb"
  },
  "communication_types": {
    "大小核通信": "ipc",
    "rpmsg": "ipc"
  },
  "lidar_models": {
    "欢创PMA2": "camsense_pma2_lidar"
  },
  "threedtof_models": {
    "光鉴Nebula280": "guangjian_nebula280_3dtof"
  },
  "special_values": {
    "无": null
  }
}
```

## 📋 输出格式

### JSON格式
```json
{
  "project_2537": {
    "sensor": {
      "lidar": "camsense_pma2_lidar",
      "linelaser": null,
      "threedtof": "guangjian_nebula280_3dtof",
      "rgb": null
    },
    "comm": {
      "ipc": "ipc"
    },
    "body": {}
  }
}
```

### YAML格式
```yaml
sensor:
  LaserSerialPort: /dev/ttyAS8           #laser 串口号
  LaserBiasDist: 0.068           #laser 距离偏差(m)
  LaserBiasAngle: 118           #laser 角度偏差(度)
  ThirdTofPort: /dev/video4           #3dtof 设备端口
  ThirdTofBiasDist: 0           #3dtof 距离偏差(m)
  ThirdTofBiasHight: 0           #3dtof 安装高度(m)
  ThirdTofBiasLeft: 0           #3dtof 安装左右偏差(m)

robot:
  robot_radius: 0           #机器人半径(m)
```

## 📝 注意事项

- CSV文件需要放在 `data/` 文件夹下
- 支持的CSV格式包含：Version、Group、Type、Value、参数解释、Define等列
- 如需添加新的传感器映射，请编辑 `config/mapping_config.json`
- 输出文件将保存到 `output/` 目录
- YAML文件包含传感器参数和机器人参数的详细配置

## 🔄 版本历史

### v2.0.0
- 新增YAML格式输出支持
- 优化CSV解析逻辑，支持新的数据格式
- 改进GUI界面，增加YAML预览功能
- 修复配置文件路径问题
- 完善项目文档和目录结构

## 📄 许可证

本项目采用MIT许可证。

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目。

## 🛠️ 依赖要求

- Python 3.7+
- tkinter（GUI界面，通常随Python安装）
- PyYAML（YAML文件处理）

---

**简单、高效、易维护** - 专业的CSV到JSON/YAML转换工具