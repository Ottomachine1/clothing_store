from django.db import models

class Designer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Clothing(models.Model):
    name = models.CharField(max_length=200)
    style_number = models.CharField(max_length=50, unique=True)
    image = models.ImageField(upload_to='clothing_images/')
    material = models.TextField()
    color = models.CharField(max_length=50)
    designer = models.ForeignKey(Designer, on_delete=models.CASCADE, related_name='clothes')
    import_date = models.DateTimeField(auto_now_add=True)
    excel_file = models.FileField(upload_to='excel_files/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.style_number})"
