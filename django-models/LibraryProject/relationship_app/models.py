from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# UserProfile model for role-based access
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"


# Library model
class Library(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# Book model with custom permissions
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    library = models.ForeignKey(
        Library,
        on_delete=models.CASCADE,
        null=True,  # allows empty for now
        blank=True  # allows empty in admin/forms
    )

    def __str__(self):
        return f"{self.title} by {self.author}"

    class Meta:
        permissions = [
            ("can_add_book", "Can add book"),
            ("can_change_book", "Can change book"),
            ("can_delete_book", "Can delete book"),
        ]


# Signal to create UserProfile automatically when a User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, role='Member')


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
