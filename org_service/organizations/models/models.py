import uuid
from django.db import models
from django.core.exceptions import ValidationError

class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'organizations'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return self.name

class OrgUser(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('member', 'Member'),
        ('viewer', 'Viewer'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, db_index=True)
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    org = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='users')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'org_users'
        constraints = [
            models.UniqueConstraint(fields=['email'], name='unique_email_org_user')
        ]
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['org', 'role']),
            models.Index(fields=['created_at']),
        ]

    def clean(self):
        if self.role not in dict(self.ROLE_CHOICES):
            raise ValidationError({'role': 'Invalid role choice'})

    def __str__(self):
        return f"{self.email} ({self.org.name})"