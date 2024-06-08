# Django Project

## Описание

"Сервис рассылок" представляет собой веб-приложение, разработанное с использованием Django. Основные функции включают управление пользователями, отображение контента и кэширование данных для улучшения производительности.

## Установка

Для установки проекта выполните следующие шаги:

1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/maxmit69/mailing_list_service
    ```

2. Перейдите в каталог проекта:
    ```bash
    cd mailing_list_service
    ```

3. Установите Poetry, если он еще не установлен:
    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```

    Затем добавьте Poetry в PATH, добавив следующую строку в ваш профиль (`~/.bashrc`, `~/.zshrc` или аналогичный файл):
    ```bash
    export PATH="$HOME/.local/bin:$PATH"
    ```

4. Установите зависимости проекта с помощью Poetry:
    ```bash
    poetry install
    ```

5. Активируйте виртуальное окружение, созданное Poetry:
    ```bash
    poetry shell
    ```

6. Выполните миграции базы данных:
    ```bash
    python manage.py migrate
    ```

7. Загрузите фикстуры данных:
    ```bash
    python manage.py loaddata mailing_app/fixtures/mailing_data.json
    python manage.py loaddata mailing_app/fixtures/message_data.json
    python manage.py loaddata mailing_app/fixtures/customers_data.json
    python manage.py loaddata mailing_app/fixtures/attemptsend_data.json
    python manage.py loaddata blogs_app/fixtures/blog_data.json
    python manage.py loaddata users_app/fixtures/user_data.json
    ```

8. Загрузите фикстуры данных:
    ```bash
    python manage.py loaddata fixtures/groups_permissions.json
    ```

9. Создайте суперпользователя:
    ```bash
    python manage.py createsuperuser
    ```

10. Запустите сервер разработки:
    ```bash
    python manage.py runserver
    ```

## Использование

Для запуска приложения выполните команду:
```bash
python manage.py runserver

Откройте браузер и перейдите по адресу http://127.0.0.1:8000/, чтобы увидеть приложение в действии.
Кэширование
Проект использует кэширование для улучшения производительности. Основные настройки кэширования находятся в файле settings.py:

CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 60
CACHE_MIDDLEWARE_KEY_PREFIX = 'blogs'


Команды управления
Очистка кэша
Создана команда для очистки кэша, которая может быть выполнена через: 
python manage.py clearcache

Лицензия
Этот проект лицензируется под MIT License.

Контакты
Если у вас есть вопросы или предложения, вы можете связаться с нами по адресу maxmit83@gmail.com.


### Объяснение изменений

1. **Установка Poetry**: Добавлены шаги по установке Poetry и добавлению его в PATH.
2. **Установка зависимостей**: Команда `poetry install` заменяет `pip install -r requirements.txt`.
3. **Активация виртуального окружения**: Использование `poetry shell` для активации виртуального окружения, созданного Poetry.

### Дополнительные советы по работе с Poetry

- **Добавление зависимости**:
    ```bash
    poetry add <package_name>
    ```

- **Удаление зависимости**:
    ```bash
    poetry remove <package_name>
    ```

- **Обновление зависимостей**:
    ```bash
    poetry update
    ```

- **Запуск команд в виртуальном окружении**:
    ```bash
    poetry run <command>
    ```

Теперь ваш проект будет использовать Poetry для управления зависимостями, что сделает его настройку и установку более простой и надежной.
