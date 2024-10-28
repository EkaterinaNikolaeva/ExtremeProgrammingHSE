# ExtremeProgrammingHSE

***Приложение-Web: сбор/проверка дз***

Web-Приложение для сбора и проверки домашних заданий.

**Требования**

1. Поддержка авторизации преподавателей и студентов

2. Для роли `Студент` возможность отправить домашнее задание: формочка с выбором предмета, группы, домашнего задания, возможностью прикрепить файл

3. Для роли `Студент` возможность посмотреть баллы и фидбек за сданные работы

4. Для роли `Преподаватель` функциональность просмотра всех непроверенных работа и архива проверенных работ

5. Для роли `Преподаватель` возможность проверить домашнее задание, выставить балл и прикрепить сообщение

6. Функциональность просмотра всех оценок группы по предмету. Доступно всем преподавателям и студентам соответсвующих групп.

**Приемо-сдаточные работы**

1. Авторизация для преподавателей и студентов работает, отображаются окна, доступные только определенной роли

2. С аккаунта студента отправляется работа. С аккаунта соответсвующего преподавателя проверяется, что работа получена. Выставляется балл, пишется сообщение. Проверяется, что в таблице появился балл для студента. Работа у преподавателя не числится в непроверенных. С аккаунта студента проверяется, что балл появился в таблице, а на вкладке сданных работ появился фидбек. 

**Детали реализации**

1. Язык написания - Python. Хорошо подходит для написания веб-приложений, множество готовых подходящих библиотек для упрощения написания функциональности.

2. Для хранения информации о студентах, преподавателях, группах и работах используется SQLAlchemy+SQLite. SQLAlchemy позволяет вместо сырых SQL-запросов использовать методы, что упрощает разработку. SQLite легко развертывается и позволяет достаточно эффективно работать для сервисов с низким трафиком.

3. Flask - легковесный веб-фреймворк. Предоставляет основной набор инструментов, при этом является простым и минималистичным.

4. API: 

GET, POST `/login`

POST `/review`

POST `/submit_homework`

GET `/untested`

GET `/submitted_works`

GET `/view_homework`

`/logout`

**Планирование**

*Первый этап*

1. Написание сервера с основными запросами (авторизация, получение списка оценок, непроверенных работ для преподаветелей, информации о сданных работах для студентов)

2. Написание моделей для базы данных

3. Интерфейс представлен авторизацией, возможностью сдать работу и получить список оценок
