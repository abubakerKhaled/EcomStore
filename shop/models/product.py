from django.db import models
from .category import Category
import uuid
class Product(models.Model):
    category = models.ForeignKey(
        Category,
        related_name = 'products',
        on_delete= models.CASCADE
    )
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False, 
        unique=True
    )  # UUID as secondary identifier
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    image = models.ImageField(
        upload_to = 'products/%Y/%m/%d',
        blank=True
    )
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]
        
    def __str__(self):
        return self.name
