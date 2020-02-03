from enum import Enum

class BuildReason(Enum):
    
    VALIDATE_SHELVE_SET = "validateShelveset"
    INDIVIDUAL_CI = "individualCI"
    MANUAL = "manual"