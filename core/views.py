from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .ssh_utils import SSHConnector
from users.permissions import IsAdminUserRole, IsEquipeUserRole

@api_view(['GET'])
@permission_classes([IsEquipeUserRole])
def check_server_status(request):
    """
    Endpoint da API para obter estatísticas do servidor via SSH.
    """
    connector = SSHConnector()
    success, message = connector.connect()
    
    if not success:
        return Response(
            {"status": "error", "message": message}, 
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    
    stats = connector.get_system_stats()
    connector.close()
    
    return Response({
        "status": "success", 
        "stats": stats
    })

@api_view(['GET'])
@permission_classes([IsEquipeUserRole])
def get_processes(request):
    """
    Lista os processos que mais consomem recursos.
    """
    connector = SSHConnector()
    connector.connect()
    processes = connector.get_processes()
    connector.close()
    return Response({"status": "success", "processes": processes})

@api_view(['GET'])
@permission_classes([IsEquipeUserRole])
def get_logs(request):
    """
    Obtém logs recentes do sistema.
    """
    connector = SSHConnector()
    connector.connect()
    logs = connector.get_logs()
    connector.close()
    return Response({"status": "success", "logs": logs})

@api_view(['GET'])
@permission_classes([IsEquipeUserRole])
def get_network(request):
    """
    Obtém informações de rede.
    """
    connector = SSHConnector()
    connector.connect()
    network = connector.get_network_stats()
    connector.close()
    return Response({"status": "success", "network": network})

@api_view(['GET'])
@permission_classes([IsEquipeUserRole])
def get_domains(request):
    """
    Lista os domínios ou pastas de sites encontrados no servidor.
    """
    connector = SSHConnector()
    connector.connect()
    domains = connector.get_domains()
    connector.close()
    return Response({"status": "success", "domains": domains})

@api_view(['POST'])
@permission_classes([IsAdminUserRole])
def manage_service_api(request):
    """
    Endpoint para gerenciar um serviço uwsgi via SSH (start, stop, restart).
    Apenas para ADM.
    Body: {"domain": "exemplo.com", "action": "restart"}
    """
    domain = request.data.get('domain')
    action = request.data.get('action', 'restart') # Padrão é restart
    
    if not domain:
        return Response({"status": "error", "message": "Domínio não informado."}, status=status.HTTP_400_BAD_REQUEST)

    connector = SSHConnector()
    connector.connect()
    success, message = connector.manage_service(domain, action)
    connector.close()

    if success:
        return Response({"status": "success", "message": message})
    else:
        return Response({"status": "error", "message": message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def index(request):
    return render(request, 'core/index.html')
