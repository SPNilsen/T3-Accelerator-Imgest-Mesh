from pathlib import Path
import shutil

class Router:
    def __init__(self, targets: list[dict]):
        self.targets = targets
        self.index = 0

    def route_file(self, source_path: str) -> tuple[str, str]:
        target = self.targets[self.index]
        target_dir = Path(target["output_directory"])
        target_dir.mkdir(parents=True, exist_ok=True)

        source = Path(source_path)
        destination = target_dir / source.name
        shutil.copy2(source, destination)

        self.index = (self.index + 1) % len(self.targets)
        return target["name"], str(destination)