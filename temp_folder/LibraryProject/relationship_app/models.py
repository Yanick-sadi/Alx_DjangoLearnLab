from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

# ----------------------------
# User Profile (Role management)
# ----------------------------
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ("Admin", "Admin"),
        ("Librarian", "Librarian"),
        ("Member", "Member"),
    ]
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="relationship_profile",  # ✅ avoid clashes
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="Member")

    def __str__(self):
        return f"{self.user.username} - {self.role}"


# ----------------------------
# Library Model
# ----------------------------
class Library(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# ----------------------------
# Book Model with Permissions
# ----------------------------
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    library = models.ForeignKey(
        Library,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title

    class Meta:
        permissions = [
            ("can_add_book", "Can add a book"),
            ("can_change_book", "Can change a book"),
            ("can_delete_book", "Can delete a book"),
        ]


# ----------------------------
# Signals: Auto-create profile for each user
# ----------------------------
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_relationship_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, role="Member")


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_relationship_profile(sender, instance, **kwargs):
    if hasattr(instance, "relationship_profile"):
        instance.relationship_profile.save()
