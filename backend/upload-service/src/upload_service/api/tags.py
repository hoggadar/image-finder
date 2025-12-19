from enum import Enum


class ApiTags(str, Enum):
    UPLOAD = "Upload"


def get_tags_metadata():
    return [
        {
            "name": ApiTags.UPLOAD,
            "description": "Upload images to user gallery and send to message queue for processing",
        },
    ]

