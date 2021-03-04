# Дипломный проект для Yandex.Praktikum - приложение «Продуктовый помощник»

![foodgram-project_workflow](https://github.com/pavel-sudomoin/foodgram-project/workflows/foodgram-project_workflow/badge.svg)

## Ссылка на проект

Приложение доступно по адресу https://foodgram-project-sudomoin.tk/

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
EMAIL_HOST=smtp.gmail.com # ссылка на smtp сервер
EMAIL_USE_TLS=True # нужно ли использовать протокол TLS
EMAIL_PORT=587 # 587 порт используется если активирован протокол TLS
EMAIL_HOST_USER=*your_account@gmail.com* # ваша почта
EMAIL_HOST_PASSWORD=*your account’s password* # ваш пароль от почты
```

### Сборка и запуск контейнеров

<pre><code>sudo docker-compose up</code></pre>

### Миграция базы данных

<pre><code>sudo docker-compose run web python manage.py migrate</code></pre>

### Остановка контейнеров

<pre><code>sudo docker-compose down</code></pre>

### Получение и настройка SSL-сертификата

Для настройки доступа по протоколу https использовался следующий гайд: https://github.com/wmnnd/nginx-certbot

Для выпуска сертификата необходимо:

1. Отредактировать файл *nginx.conf*, указав имя своего сайта вместо *foodgram-project-sudomoin.tk*

2. Отредактировать файл *init-letsencrypt.sh*, указав имя своего сайта вместо *example.org* и свой email

3. Запустить скрипт следующими командами:
   <pre><code>chmod +x init-letsencrypt.sh</code></pre>
   <pre><code>sudo ./init-letsencrypt.sh</code></pre>

### Настройка отправки сообщений на почту

В данной работе для отправки сообщений на почту пользователям использован SMTP сервер от Google.

Для настройки использовался следующий гайд: https://medium.com/@_christopher/how-to-send-emails-with-python-django-through-google-smtp-server-for-free-22ea6ea0fb8e

## Работа с проектом

### Создание суперпользователя

<pre><code>sudo docker-compose run web python manage.py createsuperuser</code></pre>

### Заполнение базы начальными данными

<pre><code>sudo docker-compose run web python manage.py loaddata fixtures_ingredients.json</code></pre>

## Авторы

* [Yandex.Praktikum](https://praktikum.yandex.ru/)

* [Судомоин Павел](https://github.com/pavel-sudomoin/)
