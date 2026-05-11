from dataclasses import dataclass


@dataclass
class TaskDefinition:

    category: str

    promocionable: bool

    required_params: list

    optional_params: list

    produces: dict
