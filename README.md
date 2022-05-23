# API для YaTube

Проект API интерфейса социальной сети с возможностью просматривать посты, добавлять комментарии,
подписываться на пользователей, оставлять собственные посты

### Запуск проекта

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/SergeSGH/api_final_yatube.git
```

```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
py -m venv venv
```

```
. venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции и создать суперпользователя:

```
py manage.py migrate
```
```
py manage.py createsuperuser
```

Запустить проект:

```
py manage.py runserver
```
