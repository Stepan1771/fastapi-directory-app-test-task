Тестовое задание.

### Описание
Данный проект соответствует ТЗ.
Тесты написать не успел, в ближайшее время доделаю.
Если вы видите это, значит еще не доделал

### Запуск
1. Перейдите в пустую папку и клонируйте репозиторий
 - git clone https://github.com/Stepan1771/fastapi-directory-app-test-task.git
2. Перейдите в папку проекта
 - cd <папка_проекта>
3. Установите зависимости проекта
 - poetry install или pip install -r requirements.txt
4. Настройте файл alembic.ini и env.py, указав правильные параметры подключения к базе данных.
5. Миграция с тестовыми данными создана, активируй её
 - alembic upgrade head
6. Запуск сервера uvicorn
 - uvicorn main:main_app

# Приложение запускается из "directory-app"

## API_KEY = qwerty 


### Связь со мной:
- тг: @BonusYou
- резюме: https://saratov.hh.ru/resume/02efc04aff0f738fe90039ed1f47356d686a63
