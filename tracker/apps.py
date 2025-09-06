from django.apps import AppConfig

class TrackerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tracker"

    def ready(self):
        # import inside ready to avoid "Apps aren't loaded yet"
        from django.contrib.auth.models import Group
        from django.db.utils import OperationalError, ProgrammingError

        try:
            Group.objects.get_or_create(name="Student")
            Group.objects.get_or_create(name="Teacher")
        except (OperationalError, ProgrammingError):
            # Database might not be ready on first migrate
            pass

    def ready(self):
        import tracker.signals

