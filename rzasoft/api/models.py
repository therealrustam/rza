from django.db import models


class Tag(models.Model):
    tag = models.CharField(max_length=200)


class Picture(models.Model):
    image = models.ImageField()
    amount = models.IntegerField()
    category = models.ManyToManyField(Tag,
                                      through='CategoryPicture',
                                      related_name='pictures')


class CategoryPicture(models.Model):
    category = models.ForeignKey(Picture,
                                 on_delete=models.SET_NULL,
                                 blank='true')
    tag = models.ForeignKey(Tag,
                            on_delete=models.SET_NULL,
                            blank='true')
