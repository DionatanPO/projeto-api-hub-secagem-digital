from rest_framework import permissions

class IsAdminUserRole(permissions.BasePermission):
    """
    Só permite acesso para usuários com role='ADMIN'.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'ADMIN')

class IsEquipeUserRole(permissions.BasePermission):
    """
    Permite acesso para usuários com role='ADMIN' ou 'EQUIPE'.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role in ['ADMIN', 'EQUIPE'])
