from enum import Enum

class BuildStatus(Enum):

    SUCCEEDED = ["succeeded"]
    IN_PROGRESS = ["inprogress", "in progress"]
    FAILED = ["failed"]
    CANCELLED = ["cancelled"]
    QUEUED = []