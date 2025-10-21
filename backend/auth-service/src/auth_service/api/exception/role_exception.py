from auth_service.api.exception.base_exception import BaseServiceError


class RoleNotFoundError(BaseServiceError):
    def __init__(self, role_name: str):
        super().__init__(f"Role '{role_name}' not found", status_code=404)