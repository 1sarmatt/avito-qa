# BUGS.md

## Общее

**Всего найдено багов:** 3
**Распределение по приоритетам:**
- High: 1 баг
- Medium: 1 баг
- Low: 1 баг

Найдены баги, связанные с валидацией данных и консистентностью API ответов.

---

## Таблица всех багов

| ID | Название | Приоритет | Статус | Тест |
|---|---|---|---|---|
| BUG-API-001 | Возможность создания объявления с отрицательной ценой | High | New | TC-006 |
| BUG-API-002 | Неконсистентное поведение при удалении несуществующего объявления | Medium | New | TC-502 |
| BUG-API-003 | Отсутствие валидации на пустое имя объявления (пробелы) | Low | New | Additional |

---

## Подробное описание багов

---

## BUG-API-001: Возможность создания объявления с отрицательной ценой

### ОПИСАНИЕ ПРОБЛЕМЫ
При создании объявления система принимает отрицательное значение для поля `price`, вместо того чтобы отклонить запрос с ошибкой валидации.

### ФАКТИЧЕСКИЙ РЕЗУЛЬТАТ
- HTTP статус: 200 OK
- Объявление создается успешно
- В ответе возвращается объявление с отрицательной ценой `-1000`

### ОЖИДАЕМЫЙ РЕЗУЛЬТАТ
- HTTP статус: 400 Bad Request
- Сообщение об ошибке, указывающее на то, что цена не может быть отрицательной


### ПРИМЕР ЗАПРОСА
```json
POST /api/1/item
{
  "sellerID": 555128,
  "name": "Товар",
  "price": -1000,
  "statistics": {
    "likes": 0,
    "viewCount": 0,
    "contacts": 0
  }
}
```

### ПРИМЕР ОТВЕТА
```json
HTTP/1.1 200 OK
{
  "id": "abc123def456",
  "sellerId": 555128,
  "name": "Товар",
  "price": -1000,
  "statistics": {
    "likes": 0,
    "viewCount": 0,
    "contacts": 0
  },
  "createdAt": "2025-11-21T10:30:00Z"
}
```

### РЕШЕНИЕ
Добавить валидацию на backend:
```python
if price < 0:
    raise ValidationError("Price must be positive")
```

### ТЕСТ ДЛЯ ВОСПРОИЗВЕДЕНИЯ
```python
def test_006_create_item_negative_price():
    payload = {
        "sellerID": 555128,
        "name": "Товар",
        "price": -1000,
        "statistics": {"likes": 0, "viewCount": 0, "contacts": 0}
    }
    response = requests.post(f"{API_V1}/item", json=payload)
    assert response.status_code == 400  # Fails: returns 200
```

---

## BUG-API-002: Неконсистентное поведение при удалении несуществующего объявления

### ОПИСАНИЕ ПРОБЛЕМЫ
При удалении объявления, которое не существует или уже было удалено, API возвращает различные HTTP коды в зависимости от того, как был сформирован ID:
- Иногда возвращает 200 OK (пустой ответ)
- Иногда возвращает 404 Not Found
- Иногда возвращает 400 Bad Request


### ФАКТИЧЕСКИЙ РЕЗУЛЬТАТ
- Первое удаление: HTTP 200 OK
- Второе удаление того же ID: HTTP 200 OK (вместо 404)

### ОЖИДАЕМЫЙ РЕЗУЛЬТАТ
- Первое удаление: HTTP 200 OK
- Второе удаление того же ID: HTTP 404 Not Found

### ПРИМЕР ЗАПРОСОВ
```bash
# Первый DELETE — успех
DELETE /api/2/item/abc123def456
HTTP/1.1 200 OK

# Второй DELETE того же ID — должен быть 404
DELETE /api/2/item/abc123def456
HTTP/1.1 200 OK  #  Некорректно, должно быть 404
```

### РЕШЕНИЕ
Добавить проверку существования объявления перед удалением:
```python
if not item_exists(item_id):
    return Response(status=404, body={"error": "Item not found"})
else:
    delete_item(item_id)
    return Response(status=200)
```

### ТЕСТ ДЛЯ ВОСПРОИЗВЕДЕНИЯ
```python
def test_504_delete_twice():
    item_id = create_test_item()["id"]
    
    response1 = requests.delete(f"{API_V2}/item/{item_id}")
    assert response1.status_code == 200
    
    response2 = requests.delete(f"{API_V2}/item/{item_id}")
    assert response2.status_code == 404  # Fail: returns 200
```

---

## BUG-API-003: Отсутствие валидации пробелов в имени объявления

### ОПИСАНИЕ ПРОБЛЕМЫ
Система позволяет создавать объявления с именем, состоящим только из пробелов (whitespace). Это приводит к созданию объявлений без видимого имени.


### ФАКТИЧЕСКИЙ РЕЗУЛЬТАТ
- HTTP статус: 200 OK
- Объявление создается с пустым (невидимым) именем

### ОЖИДАЕМЫЙ РЕЗУЛЬТАТ
- HTTP статус: 400 Bad Request
- Сообщение об ошибке: "Name cannot be empty or contain only whitespace"


### ПРИМЕР ЗАПРОСА
```json
POST /api/1/item
{
  "sellerID": 555135,
  "name": "     ",
  "price": 1000,
  "statistics": {
    "likes": 0,
    "viewCount": 0,
    "contacts": 0
  }
}
```

### РЕШЕНИЕ
Добавить валидацию с обрезкой пробелов:
```python
name = name.strip()
if not name:
    raise ValidationError("Name cannot be empty")
```

### ТЕСТ ДЛЯ ВОСПРОИЗВЕДЕНИЯ
```python
def test_whitespace_name():
    payload = {
        "sellerID": 555135,
        "name": "     ",
        "price": 1000,
        "statistics": {"likes": 0, "viewCount": 0, "contacts": 0}
    }
    response = requests.post(f"{API_V1}/item", json=payload)
    assert response.status_code == 400
```



