import yaml
from typing import Dict,Any


def load_config(config_path:str)->Dict[str,Any]:
    """
        从路径中读取yml数据

        Args:
            config_path(str): yml文件的路径
        Returns:
            Dict[str,Any]: 配置文件的字典数据
    """
    with open(config_path,"r") as config_file:
        return yaml.safe_load(config_file)
