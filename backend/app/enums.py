from enum import Enum

class ChoreFieldType(str, Enum):
    string = "string"
    float = "float"
    int = "int"
    bool = "bool"
