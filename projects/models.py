from django.db import models

class Project(models.Model):
    STATUS_CHOICES = (
        ('PROSPECT', 'Prospecção'),
        ('PLANNING', 'Planejamento'),
        ('DEVELOPMENT', 'Em Desenvolvimento'),
        ('MAINTENANCE', 'Manutenção'),
        ('FINISHED', 'Finalizado'),
        ('PAUSED', 'Pausado'),
    )

    name = models.CharField(max_length=200, verbose_name="Nome do Projeto")
    client_name = models.CharField(max_length=200, blank=True, null=True, verbose_name="Cliente")
    start_date = models.DateField(verbose_name="Data de Início")
    registration_date = models.DateField(auto_now_add=True, verbose_name="Data de Registro")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PLANNING')
    description = models.TextField(blank=True, null=True, verbose_name="Descrição")
    observations = models.TextField(blank=True, null=True, verbose_name="Observações")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-start_date']
        verbose_name = "Projeto"
        verbose_name_plural = "Projetos"
