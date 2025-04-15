import yaml
import json
import os
from collections.abc import MutableMapping
# 读取 YAML 文件
def load_yaml(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)
#写yaml
def fix_json_string(json_str):
    """自动修正 YAML 里的非标准 JSON 格式"""
    json_str = json_str.replace("'", "\"")  # 替换单引号为双引号
    if not json_str.startswith("{"):  # 防止空值
        return "{}"
    try:
        json.loads(json_str)  # 检查是否是合法 JSON
        return json_str
    except json.JSONDecodeError:
        return "{}"  # 如果解析失败，返回空 JSON

def write_yaml(filepath,data):
    # 写入 YAML 文件
    with open(filepath, 'w', encoding='utf-8') as file:
        yaml.dump(data, file, allow_unicode=True, sort_keys=False)


def append_yaml(filepath, data_string, target_path=None):
    """
    追加授权信息到 YAML 文件，支持多重嵌套结构

    参数:
        filepath: YAML文件路径
        data_string: 要追加的数据字符串，格式为"key: value"或"path.to.key: value"
        target_path: 可选，指定嵌套路径，如"headers.auth"或"data.credentials"
    """
    try:
        # 1. 解析输入字符串
        if ":" not in data_string:
            raise ValueError("输入的字符串必须包含 ':' 分隔符")

        key_part, value = [part.strip() for part in data_string.split(":", 1)]

        # 2. 确定嵌套路径
        if target_path:
            # 使用指定的目标路径
            path_keys = target_path.split('.')
            final_key = key_part
        else:
            # 从字符串中解析路径
            if '.' in key_part:
                path_keys = key_part.split('.')
                final_key = path_keys.pop()
            else:
                path_keys = []
                final_key = key_part

        # 3. 构建嵌套字典结构
        new_data = {final_key: value}
        for key in reversed(path_keys):
            new_data = {key: new_data}

        # 4. 读取现有数据
        existing_data = {}
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    existing_data = yaml.safe_load(file) or {}
            except yaml.YAMLError as e:
                print(f"警告: YAML解析错误，将创建新文件。错误: {str(e)}")

        # 5. 深度合并字典
        def deep_update(d, u):
            for k, v in u.items():
                if isinstance(v, dict):
                    d[k] = deep_update(d.get(k, {}), v)
                else:
                    d[k] = v
            return d

        merged_data = deep_update(existing_data, new_data)

        # 6. 写入文件
        with open(filepath, 'w', encoding='utf-8') as file:
            yaml.dump(merged_data, file, allow_unicode=True, sort_keys=False)

    except Exception as e:
        print(f"写入YAML文件失败: {str(e)}")
        raise