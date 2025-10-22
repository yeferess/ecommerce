from django.db import models

# Create your models here.

class Page(models.Model):
    title = models.CharField(max_length=80)
    slug = models.SlugField(unique=True) # slug: identificador unico de una pagina
    content = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title