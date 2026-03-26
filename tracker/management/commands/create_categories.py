from django.core.management.base import BaseCommand
from tracker.models import Category


CATEGORIES = [
    {"name": "Рестораны и кафе", "icon": "🍜"},
    {"name": "Кино и сериалы", "icon": "🎬"},
    {"name": "Книги", "icon": "📖"},
    {"name": "Путешествия и места", "icon": "🏔️"},
    {"name": "Игры и хобби", "icon": "🎮"},
    {"name": "Музыка и концерты", "icon": "🎵"},
    {"name": "Искусство и выставки", "icon": "🎨"},
    {"name": "Спорт и активный отдых", "icon": "🏆"},
    {"name": "Мастер-классы и обучение", "icon": "💡"},
    {"name": "События и впечатления", "icon": "🎉"},
]


class Command(BaseCommand):
    help = "Создаёт категории для впечатлений"

    def handle(self, *args, **options):
        created_count = 0
        for cat_data in CATEGORIES:
            name_with_icon = f"{cat_data['icon']} {cat_data['name']}"
            category, created = Category.objects.get_or_create(
                name=name_with_icon
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f"✓ Создана категория: {name_with_icon}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"✓ Категория уже существует: {name_with_icon}")
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"\nГотово! Создано {created_count} новых категорий."
            )
        )
