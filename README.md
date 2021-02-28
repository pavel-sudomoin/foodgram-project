# Дипломный проект для Yandex.Praktikum - приложение «Продуктовый помощник»

![foodgram-project_workflow](https://github.com/pavel-sudomoin/foodgram-project/workflows/foodgram-project_workflow/badge.svg)

## Описание проекта

Приложение «Продуктовый помощник» это онлайн-сервис, на котором пользователи могут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволяет пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

Приложение разработано в учебных целях как дипломный проект для **Yandex.Praktikum**.

## Установка проекта

Клонируйте данный репозиторий на свой компьютер и перейдите в папку проекта.

После выполнения указанных ниже команд на вашем компьютере в двух docker-контейнерах будет развёрнут проект «Продуктовый помощник». Будет поднят один docker-контейнер с web-приложением и один с базой данных.

### Установка docker и docker-compose

Для установки docker и docker-compose воспользуйтесь официальной [инструкцией](https://docs.docker.com/get-docker/).

### Структура файла *.env* с переменными окружения

Переменные окружения хранятся в файле *.env*. Вы можете изменять его и задавать собственные настройки и пароли.

По умолчанию файл имеет следующую структуру:

```
SECRET_KEY=YOUR_SECRET_KEY # секретный ключ Django
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (рекомендуется установить свой)
```

### Сборка и запуск контейнеров

<pre><code>sudo docker-compose up</code></pre>

### Миграция базы данных

<pre><code>sudo docker-compose run web python manage.py migrate</code></pre>

### Остановка контейнеров

<pre><code>sudo docker-compose down</code></pre>

## Работа с проектом

### Создание суперпользователя

<pre><code>sudo docker-compose run web python manage.py createsuperuser</code></pre>

### Заполнение базы начальными данными

<pre><code>sudo docker-compose run web python manage.py loaddata fixtures_ingredients.json</code></pre>

## Авторы

* [Yandex.Praktikum](https://praktikum.yandex.ru/)

* [Судомоин Павел](https://github.com/pavel-sudomoin/)
