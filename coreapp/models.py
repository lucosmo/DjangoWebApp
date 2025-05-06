from django.db import models
from PIL import Image as PilImage

class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Article(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    body = models.TextField(blank=True)
    author = models.ForeignKey(User, related_name='articles', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Image(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.ImageField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def resize(self, width, height):
        img = PilImage.open(self.file.path)
        img = img.resize((width, height))
        img.save(self.file.path)

    def grayscale(self):
        img = PilImage.open(self.file.path).convert('L')
        img.save(self.file.path)

    def crop(self, left, top, right, bottom):
        img = PilImage.open(self.file.path)
        img = img.crop((left, top, right, bottom))
        img.save(self.file.path)

    def composite(self, width, height, left, top, right, bottom):
        self.resize(width, height)
        self.grayscale()
        self.crop(left, top, right, bottom)