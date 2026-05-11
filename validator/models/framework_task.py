from dataclasses import dataclass


@dataclass
class FrameworkTask:
    task_name: str
    params: dict
