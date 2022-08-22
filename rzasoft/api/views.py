from django.shortcuts import render
from models import Picture, Tag
import csv


def index():
    if not Picture.objects.first():
        with open('images.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Tag.objects.get_or_create(tag=)
                Picture.objects.create()
