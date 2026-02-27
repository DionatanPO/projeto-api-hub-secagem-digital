from rest_framework import viewsets, permissions
from .models import Project
from .serializers import ProjectSerializer
from users.permissions import IsAdminUserRole, IsEquipeUserRole

class ProjectViewSet(viewsets.ModelViewSet):
    """
    CRUD de Projetos da Startup.
    - Admin: Acesso total.
    - Equipe: Acesso de visualização.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsEquipeUserRole] # Admin e Equipe podem ver
        else:
            permission_classes = [IsAdminUserRole] # Só Admin pode criar/editar/deletar
        return [permission() for permission in permission_classes]
