from django.apps import AppConfig


class SessaoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sessao'

    def ready(self):
        from django.contrib.auth.models import Group, Permission
        from django.contrib.contenttypes.models import ContentType
        from filmes.models import Filme, Comentario

        # Cria o grupo de Moderadores
        moderador_group, created = Group.objects.get_or_create(name="Moderador")

        # Adiciona a permissão ao grupo de Editores
        content_type = ContentType.objects.get_for_model(Filme)
        post_permission = Permission.objects.filter(content_type=content_type)

        for perm in post_permission:
            if perm.codename == "change_filme":
                moderador_group.permissions.add(perm)
            if perm.codename == "add_filme":
                moderador_group.permissions.add(perm)

        content_type = ContentType.objects.get_for_model(Comentario)
        post_permission = Permission.objects.filter(content_type=content_type)

        for perm in post_permission:
            if perm.codename == "delete_comentario":
                moderador_group.permissions.add(perm)
