import csv

from django.core.management import BaseCommand

from api_yamdb.settings import CSV_FILES_DIR
from reviews.models import (
    Category,
    Comment,
    Genre,
    # GenreTitle,
    Review,
    Title
)
from users.models import User

FILES_CLASSES = {
    'category.csv': Category,
    'genre.csv': Genre,
    'titles.csv': Title,
    # 'genre_title.csv': GenreTitle,
    'users.csv': User,
    'review.csv': Review,
    'comments.csv': Comment,
}


class Command(BaseCommand):
    """Класс загрузки тестовой базы данных."""

    def handle(self, *args, **kwargs):
        for csv_file, model in FILES_CLASSES.items():
            with open(
                    f'{CSV_FILES_DIR/{csv_file}}',
                    'r',
                    encoding='utf-8'
            ) as csv_f:
                reader = csv.DictReader(csv_f)
                model.objects.bulk_create(
                    model(**data) for data in reader)
        self.stdout.write(self.style.SUCCESS('Данные загружены'))
