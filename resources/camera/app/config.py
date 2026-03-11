from pathlib import Path
import yaml


CONFIG_PATH = Path("/opt/camera/config/camera-config.yaml")


def load_config():
    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)