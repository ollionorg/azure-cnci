from enum import Enum

class EventType(Enum):

    def __str__(self):
        return str(self.value)

    BUILD_COMPLETE_EVENT = "build.complete"
    BUILD_RUNSTATE_CHANGE_EVENT = "ms.vss-pipelines.run-state-changed-event"