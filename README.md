# ДЗ №1 по РИП

Выполнил: Игорь Водка, ИУ5-51

## Запуск

```
cd docker
docker-compose up
```

Далее 127.0.0.1:8080.

## Настройка

В первый раз нужно будет всё настроить.

* Вводим `docker ps | grep python`, находим ID контейнера.
* Пишем `docker exec -it этот_ID sh`, входим в консоль.
* В консоли пишем:
```
cd ..
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py loaddata megadump.json           # тут крутые готовые данные
```
* Если вдруг вываливается с ошибкой, в `views.ProfileView` нужно строчку:
```
form_class = UpdateUserForm                     # uh
```
заменить на:
```
form_class = 'UpdateUserForm'                   # uh
```
А после миграций вернуть всё как было. Извините. :)
* ?????????
* PROFIT!
