from auth_service.core.exception.base_exeption import BaseAppException


class RoleNotFoundException(BaseAppException):
    def __init__(self, role_name: str):
        super().__init__(f"Role '{role_name}' not found", status_code=404)


class RoleAlreadyExistsException(BaseAppException):
    def __init__(self, role_name: str):
        super().__init__(f"Role '{role_name}' already exists", status_code=409)


class RoleCreationException(BaseAppException):
    def __init__(self, reason: str):
        super().__init__(f"Role creation failed: {reason}", status_code=400)


class RoleUpdateException(BaseAppException):
    def __init__(self, reason: str):
        super().__init__(f"Role update failed: {reason}", status_code=400)


class RoleDeletionException(BaseAppException):
    def __init__(self, reason: str):
        super().__init__(f"Role deletion failed: {reason}", status_code=400)


class InsufficientPermissionsException(BaseAppException):
    def __init__(self, required_permission: str):
        super().__init__(f"Insufficient permissions. Required: {required_permission}", status_code=403)


class InvalidRoleAssignmentException(BaseAppException):
    def __init__(self, reason: str):
        super().__init__(f"Invalid role assignment: {reason}", status_code=400)
