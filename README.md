# CSV到JSON转换工具

一个简单易用的CSV到JSON转换工具，专门用于将传感器配置CSV文件转换为标准化的JSON格式。

## 🚀 快速开始

### 使用方法

1. 将CSV文件放入 `csvdata/` 文件夹
2. 运行转换命令：
   ```bash
   python convert.py
   ```
3. 转换结果将保存到 `output/result.json`

### 项目结构

```
├── convert.py              # 主转换脚本
├── config/
│   └── mapping_config.json # 映射配置文件
├── csvdata/               # CSV文件目录
├── output/                # 输出目录
└── src/
    └── csv_to_json_converter.py  # 核心转换器
```

## ⚙️ 配置说明

### 映射配置文件

编辑 `config/mapping_config.json` 来管理中英文映射关系：

```json
{
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
    "乐动STL50": "ld_stl50_lidar",
    "欢创PMA2": "camsense_pma2_lidar"
  },
  "linelaser_models": {
    "一微ALF03": "amicro_alf03_linelaser"
  },
  "threedtof_models": {
    "深锐280": "deptrum_nebula280_3dtof"
  },
  "rgb_models": {
    "无": null
  },
  "special_values": {
    "无": null,
    "": null
  },
  "project_prefix": "project_"
}
```

### 配置类别说明

- **sensor_types**: 传感器类型映射
- **communication_types**: 通信类型映射
- **lidar_models**: 雷达传感器型号映射
- **linelaser_models**: 线结构光传感器型号映射
- **threedtof_models**: 3D ToF传感器型号映射
- **rgb_models**: RGB传感器型号映射
- **special_values**: 特殊值映射（如"无"、空字符串）
- **project_prefix**: 项目ID前缀

## 🔧 配置管理

直接编辑 `config/mapping_config.json` 文件来维护映射关系。

当遇到新的传感器类型或型号时，只需在对应的配置类别中添加映射即可。

## 📋 输出格式

转换后的JSON格式：

```json
{
  "project_2407": {
    "sensor": {
      "lidar": "ld_stl50_lidar",
      "linelaser": "amicro_alf03_linelaser",
      "threedtof": null,
      "rgb": null
    },
    "comm": {
      "ipc": "mailbox"
    },
    "body": {}
  }
}
```

## 📝 注意事项

- CSV文件需要放在 `csvdata/` 文件夹下
- 工具会自动查找并使用第一个找到的CSV文件
- 如需添加新的映射关系，请编辑 `config/mapping_config.json`
- 支持多种传感器类型的分类管理

## 🛠️ 依赖要求

- Python 3.6+
- 无额外第三方依赖，仅使用Python标准库

---

**简单、高效、易维护** - 专注于CSV到JSON的转换任务