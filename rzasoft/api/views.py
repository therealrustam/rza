from django.shortcuts import render
from .models import Picture, Tag
import csv
from .filter import PictureFilter


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
    filter = PictureFilter(request.GET, queryset=Picture.objects.all())
    print(type(filter))
    url = f'<img class="image" src="{filter}" alt="">'
    context = {'URL': url}
    return render(request, 'api/index.html', context)
