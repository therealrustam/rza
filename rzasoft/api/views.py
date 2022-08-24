"""
Основные методы работы приложения.
"""

import csv

from django.shortcuts import render

from .models import Picture, Tag

MEMORY = {'last_image': 0}


def load():
    """
    Метод считывание данных из файла images.csv и
    загрузки в БД.
    """
    with open('images.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            tags = []
            for counter in range(1, 11):
                category_name = f'category{counter}'
                if row[category_name]:
                    tag = Tag.objects.get_or_create(tag=row[category_name])
                    tags.append(tag)
            image = Picture.objects.get_or_create(
                image=row['Image_URL'],
                amount=row['needed_amount_of_shows'])
            for tag in tags:
                image[0].category.add(tag[0].id)


def index(request):
    """
    Метод обработки запроса и предоставления
    изображения по категориям.
    """
    if not Picture.objects.first():
        load()
    categorys = request.GET.getlist('category[]')
    categorys_list = []
    image_list = []
    for category in categorys:
        tag = Tag.objects.get_or_create(tag=category)
        categorys_list.append(tag)
    for tag in categorys_list:
        images = Picture.objects.filter(category=tag[0].id)
        image_list.extend(images)
    picture = 0
    image_list = set(image_list)
    counter_tag = 0
    for image in image_list:
        if (image.counter == image.amount):
            continue
        if (image != MEMORY['last_image']):
            counter_tag += 1
            picture = image
            break
    for image in image_list:
        if (counter_tag == 0) & (image.counter != image.amount):
            picture = image
            break
    if picture == 0:
        return render(request, 'api/index.html')
    url = f'<img class="image" src="{picture.image}" alt="">'
    MEMORY['last_image'] = picture
    picture.counter += 1
    picture.save()
    context = {'URL': url,
               'AMOUNT': picture.amount,
               'COUNTER': picture.counter}
    return render(request, 'api/picture.html', context)
