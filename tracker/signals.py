from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Student

@receiver(post_save, sender=User)
def create_student_user(sender, instance, created, **kwargs):
    if created and hasattr(instance, "is_student") and instance.is_student:
        Student.objects.create(
            user=instance,
            first_name=instance.first_name,
            last_name=instance.last_name,
            email=instance.email,
            date_of_birth=None  # or pull from form if available
        )

