# README.md


**Тестируемый API:**
- **Host:** https://qa-internship.avito.com
- **Версии API:** v1 и v2

**Основные функции API:**
- ✅ Создание объявлений (POST /api/1/item)
- ✅ Получение объявления по ID (GET /api/1/item/:id)
- ✅ Получение всех объявлений пользователя (GET /api/1/:sellerID/item)
- ✅ Получение статистики объявления (GET /api/1/statistic/:id, /api/2/statistic/:id)
- ✅ Удаление объявления (DELETE /api/2/item/:id)

**Что включено в проект:**
-  31 подробный тест-кейс (TESTCASES.md)
-  24 автоматизированных теста на Python + pytest
-  Все тесты прошли успешно
-  3 найденных бага (BUGS.md)

---

## Требования

### Минимальные требования:
- **Python 3.8+**
- **pip** (Python package manager)


## Старт


```bash
# 1. Установить зависимости
pip install -r requirements.txt

# 2. Запустить тесты
pytest test_api.py -v

# 3. Посмотреть результаты
# ✅ 24 passed, 1 skipped
```

---

## Установка

### 1. Клонирование репозитория или скачивание файлов

```bash
git clone 1sarmatt/avito-qa
cd avito-qa

```

### 2. Создание виртуального окружения (рекомендуется)



```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```


---

## Запуск тестов

### Запуск всех тестов

```bash
pytest test_api.py -v
```

### Запуск с подробным выводом

```bash
pytest test_api.py -v -s
```

### Запуск конкретного класса тестов

```bash
# Только тесты создания объявлений
pytest test_api.py::TestCreateItem -v

# Только тесты получения объявления
pytest test_api.py::TestGetItemById -v

# Только тесты получения списка объявлений
pytest test_api.py::TestGetSellerItems -v

# Только тесты получения статистики
pytest test_api.py::TestGetStatistic -v

# Только тесты удаления
pytest test_api.py::TestDeleteItem -v
```

### Запуск конкретного теста

```bash
pytest test_api.py::TestCreateItem::test_001_create_item_success -v
```

### Сохранение результатов в файл

```bash
pytest test_api.py -v > test_results.txt
```

### Быстрая проверка (без вывода)

```bash
pytest test_api.py -q
```

---



### Описание файлов

**test_api.py** (650+ строк)
- `TestCreateItem` — 9 тестов создания объявлений
- `TestGetItemById` — 4 теста получения объявления
- `TestGetSellerItems` — 5 тестов получения списка объявлений
- `TestGetStatistic` — 4 теста получения статистики
- `TestDeleteItem` — 2 теста удаления объявлений


---

## Результаты тестирования

### Статус: ✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ

```
test_api.py::TestCreateItem::test_001_create_item_success PASSED
test_api.py::TestCreateItem::test_002_create_item_minimal_data PASSED
test_api.py::TestCreateItem::test_003_create_item_high_price PASSED
test_api.py::TestCreateItem::test_004_create_item_missing_name PASSED
test_api.py::TestCreateItem::test_005_create_item_missing_price PASSED
test_api.py::TestCreateItem::test_006_create_item_negative_price PASSED
test_api.py::TestCreateItem::test_007_create_item_empty_name PASSED
test_api.py::TestCreateItem::test_008_create_item_invalid_json PASSED
test_api.py::TestCreateItem::test_009_create_duplicate_items PASSED
test_api.py::TestGetItemById::test_201_get_existing_item PASSED
test_api.py::TestGetItemById::test_202_get_nonexistent_item PASSED
test_api.py::TestGetItemById::test_203_get_item_empty_id PASSED
test_api.py::TestGetItemById::test_204_get_item_invalid_format PASSED
test_api.py::TestGetSellerItems::test_301_get_seller_items_multiple PASSED
test_api.py::TestGetSellerItems::test_302_get_seller_items_empty PASSED
test_api.py::TestGetSellerItems::test_303_get_items_nonexistent_seller PASSED
test_api.py::TestGetSellerItems::test_304_get_items_negative_seller_id PASSED
test_api.py::TestGetSellerItems::test_305_get_items_invalid_seller_id PASSED
test_api.py::TestGetStatistic::test_401_get_statistic_success PASSED
test_api.py::TestGetStatistic::test_402_get_statistic_nonexistent PASSED
test_api.py::TestGetStatistic::test_403_get_statistic_v2 PASSED
test_api.py::TestGetStatistic::test_404_get_statistic_empty_id PASSED
test_api.py::TestDeleteItem::test_501_delete_existing_item PASSED
test_api.py::TestDeleteItem::test_502_delete_nonexistent_item PASSED
test_api.py::TestDeleteItem::test_503_delete_invalid_id PASSED

========================== 24 passed, 1 skipped in 19.16s ==========================
```

### Покрытие функциональности

| Функция | Positive | Negative | Итого | Статус |
|---------|----------|----------|-------|--------|
| Создание | 4 | 5 | 9 | ✅ |
| Получение по ID | 1 | 3 | 4 | ✅ |
| Получение списка | 2 | 3 | 5 | ✅ |
| Статистика | 3 | 1 | 4 | ✅ |
| Удаление | 1 | 2 | 3 | ✅ |
| **ИТОГО** | **11** | **14** | **25** | **✅** |

---

