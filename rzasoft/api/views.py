from django.shortcuts import render
from .models import Picture, Tag
import csv


def index(request):
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
                image=row['Image_URL'], amount=row['needed_amount_of_shows'])
            for tag in tags:
                image[0].category.add(tag[0].id)
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
    for image in image_list:
        picture = image
        break
    url = f'<img class="image" src="{picture.image}" alt="">'
    context = {'URL': url}
    return render(request, 'api/index.html', context)
