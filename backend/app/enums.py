from enum import Enum

class LogFieldType(str, Enum):
    string = "string"
    float = "float"
    int = "int"
    bool = "bool"
