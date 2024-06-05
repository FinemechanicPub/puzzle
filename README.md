## Установка
### Загрузка проекта

```shell
git clone https://github.com/FinemechanicPub/puzzle.git
```

### Установка зависимостей
Предварительно создайте и активируйте окружение с помощью пакета [venv](https://docs.python.org/3/library/venv.html) или другого средства.

```shell
pip install -r requirements.txt
```

## Запуск
### Отладочный режим

```shell
uvicorn app.main:app --reload
```