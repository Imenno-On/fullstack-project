from app.models.test_model import Test, TestStatus

TESTS = [
    Test(
        id=1,
        title="История России XX века",
        date="15 октября 2025",
        link="https://forms.yandex.ru/cloud/12345abcde/",
        students=24,
        completed=18,
        status=TestStatus.ACTIVE,
        description="Тест для 10 класса по ключевым событиям XX века",
    ),
    Test(
        id=2,
        title="Основы программирования на Python",
        date="12 октября 2025",
        link="https://forms.yandex.ru/cloud/67890fghij/",
        students=32,
        completed=32,
        status=TestStatus.COMPLETED,
        description="Проверочный тест по базовому синтаксису Python",
    ),
    Test(
        id=3,
        title="Английская грамматика: Present Perfect",
        date="10 октября 2025",
        link="https://forms.yandex.ru/cloud/klmno12345/",
        students=28,
        completed=15,
        status=TestStatus.ACTIVE,
        description="Практика образования и использования Present Perfect",
    ),
]
