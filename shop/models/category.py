from django.db import models
import uuid

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )  # UUID as a secondary unique identifier
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        
    def __str__(self):
        return self.name