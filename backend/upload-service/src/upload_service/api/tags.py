from enum import Enum


class ApiTags(str, Enum):
    """API tags for Swagger documentation."""
    
    UPLOAD = "Upload"


def get_tags_metadata():
    """Return metadata for OpenAPI tags."""
    return [
        {
            "name": ApiTags.UPLOAD,
            "description": "Upload images to user gallery and send to message queue for processing",
        },
    ]

