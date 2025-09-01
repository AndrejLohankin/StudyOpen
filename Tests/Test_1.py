import pytest

# Импортируем тестируемую функцию
from Task_1 import solve

@pytest.mark.parametrize(
    "models, available, manufacturers, expected",
    [
        (
            [
                '480 ГБ 2.5" SATA накопитель Kingston A400',
                '500 ГБ 2.5" SATA накопитель Samsung 870 EVO',
                '480 ГБ 2.5" SATA накопитель ADATA SU650',
                '240 ГБ 2.5" SATA накопитель ADATA SU650',
                '250 ГБ 2.5" SATA накопитель Samsung 870 EVO',
                '256 ГБ 2.5" SATA накопитель Apacer AS350 PANTHER',
                '480 ГБ 2.5" SATA накопитель WD Green',
                '500 ГБ 2.5" SATA накопитель WD Red SA500'
            ],
            [1, 1, 1, 1, 0, 1, 1, 0],
            ['Intel', 'Samsung', 'WD'],
            (
                ['500 ГБ 2.5" SATA накопитель Samsung 870 EVO', '480 ГБ 2.5" SATA накопитель WD Green'],
                2
            )
        ),
        # Дополнительный тест: нет подходящих производителей
        (
            ['480 ГБ 2.5" SATA накопитель Kingston A400'],
            [1],
            ['Intel', 'Samsung', 'WD'],
            ([], 0)
        ),
        # Дополнительный тест: все диски подходят и доступны
        (
            ['256 ГБ SSD Intel', '500 ГБ SSD Samsung'],
            [1, 1],
            ['Intel', 'Samsung', 'WD'],
            (['256 ГБ SSD Intel', '500 ГБ SSD Samsung'], 2)
        ),
        # Дополнительный тест: все диски недоступны
        (
            ['480 ГБ 2.5" SATA накопитель Kingston A400'],
            [0],
            ['Intel', 'Samsung', 'WD'],
            ([], 0)
        ),
    ]
)
def test_solve(models, available, manufacturers, expected):
    result = solve(models, available, manufacturers)
    assert result == expected