from django.db import models

class Category(models.Model):
    CATEGORIES = [
        ('TEXTBOOK', 'Textbook'),
        ('MARKETPLACE', 'Marketplace'),
        ('SERVICE', 'Service'),
        ('HOUSING', "Housing"),
    ]
    name = models.CharField(max_length=50, choices=CATEGORIES, null=False)