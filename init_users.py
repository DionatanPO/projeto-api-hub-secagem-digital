import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hub_secagem_digital.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Criar Admin
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin', 
        email='admin@secagem.com', 
        password='admin123', 
        role='ADMIN',
        first_name='Administrador',
        last_name='Hub'
    )
    print("Usuário Admin criado: admin / admin123")

# Criar Equipe
if not User.objects.filter(username='equipe').exists():
    User.objects.create_user(
        username='equipe', 
        email='equipe@secagem.com', 
        password='equipe123', 
        role='EQUIPE',
        first_name='Tecnico',
        last_name='Equipe'
    )
    print("Usuário Equipe criado: equipe / equipe123")
