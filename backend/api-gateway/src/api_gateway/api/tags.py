"""API documentation tags for OpenAPI/Swagger UI."""

from typing import List, Dict, Any


class ApiTags:
    """Constants for API tags used in OpenAPI documentation."""
    
    # Main service tags
    CLIP = "CLIP"
    UPLOAD = "Upload"
    SEARCH = "Search"
    
    # Auth service tags (with hierarchy)
    AUTH_AUTHENTICATION = "Auth - Authentication"
    AUTH_USERS = "Auth - Users"
    AUTH_ROLES = "Auth - Roles"


def get_tags_metadata() -> List[Dict[str, Any]]:
    """Get metadata for API documentation tags.
    
    Returns:
        List of tag metadata dictionaries for FastAPI openapi_tags parameter.
    """
    return [
        {
            "name": ApiTags.CLIP,
            "description": (
                "**CLIP Service Operations**\n\n"
                "Operations for working with CLIP (Contrastive Language-Image Pre-training) model:\n"
                "- Calculate similarity between images and text descriptions\n"
                "- Generate embeddings for images and text\n"
                "- Compare pre-computed embeddings"
            ),
        },
        {
            "name": ApiTags.AUTH_AUTHENTICATION,
            "description": (
                "**Authentication Operations**\n\n"
                "Core authentication functionality:\n"
                "- User signup and login\n"
                "- Token validation and refresh\n"
                "- Session management (logout)"
            ),
        },
        {
            "name": ApiTags.AUTH_USERS,
            "description": (
                "**User Management**\n\n"
                "CRUD operations for user accounts:\n"
                "- List, search and retrieve users\n"
                "- Create, update and delete users\n"
                "- Password management\n\n"
                "*Requires Admin or Moderator role*"
            ),
        },
        {
            "name": ApiTags.AUTH_ROLES,
            "description": (
                "**Role Management**\n\n"
                "CRUD operations for user roles:\n"
                "- List and retrieve roles\n"
                "- Create, update and delete roles\n\n"
                "*Requires Admin role*"
            ),
        },
        {
            "name": ApiTags.UPLOAD,
            "description": (
                "**Image Upload Operations**\n\n"
                "Operations for uploading and storing images:\n"
                "- Upload images to storage\n"
                "- Trigger image processing pipeline\n"
                "- Associate images with users"
            ),
        },
        {
            "name": ApiTags.SEARCH,
            "description": (
                "**Image Search Operations**\n\n"
                "Vector similarity search operations:\n"
                "- Search images by text description\n"
                "- Search images by embedding vector\n"
                "- Search similar images by image\n\n"
                "*Note: This service is planned for future implementation*"
            ),
        },
    ]


__all__ = ["ApiTags", "get_tags_metadata"]

