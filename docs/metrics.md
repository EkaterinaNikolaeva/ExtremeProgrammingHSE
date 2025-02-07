## Полученные результаты

### Простые метрики

| Файл                   | LOC  | LLOC | SLOC | Comments | Single Comments | Multi | Blank |
|------------------------|-----|-----|-----|---------|----------------|------|------|
| src/main.py           | 8   | 5   | 5   | 0       | 0              | 0    | 3    |
| src/db/models.py      | 42  | 34  | 34  | 1       | 0              | 0    | 8    |
| src/server/server.py  | 145 | 105 | 113 | 0       | 0              | 0    | 32   |
| tests/unit/test_part_1.py | 66  | 51  | 51  | 0       | 0              | 0    | 15   |
---

### Метрики Холстеда

| Файл                   | h1 (NUOprtr) | h2 (NUOprnd) | N1 (Noprtr) | N2 (Noprnd) | Vocabulary | Length | Calculated Length | Volume (HPVol) | Difficulty (HDiff) | Effort (HEff) | Time | Bugs |
|-----------------------|----|----|----|----|------------|--------|------------------|--------|-----------|--------|------|------|
| src/main.py          | 1  | 2  | 1  | 2  | 3          | 3      | 2.0              | 4.75   | 0.5       | 2.38   | 0.13 | 0.0016 |
| src/db/models.py     | 0  | 0  | 0  | 0  | 0          | 0      | 0.0              | 0.0    | 0.0       | 0.0    | 0.0  | 0.0 |
| src/server/server.py | 6  | 24 | 13 | 25 | 30         | 38     | 125.55           | 186.46 | 3.125     | 582.69 | 32.37| 0.0622 |
| tests/unit/test_part_1.py | 66  | 51  | 51  | 0       | 0              | 0    | 15   |
| tests/unit/test_part_1.py | 1  | 2  | 1  | 2  | 3          | 3      | 2.0              | 4.75   | 0.5       | 2.38   | 0.13 | 0.0016 |
---


### Цикломатическая сложность

| Файл                  | Функция / Класс                      | Сложность |
|----------------------|-------------------------------------|-----------|
| src/main.py         | main                                | A (1)     |
| src/db/models.py    | Teacher                             | A (1)     |
| src/db/models.py    | HomeworkForm                        | A (1)     |
| src/db/models.py    | Student                             | A (1)     |
| src/db/models.py    | Homework                            | A (1)     |
| src/db/models.py    | User                                | A (1)     |
| src/server/server.py | submit_homework                    | B (6)     |
| src/server/server.py | login                               | A (5)     |
| src/server/server.py | review                              | A (4)     |
| src/server/server.py | get_unreviewed                      | A (3)     |
| src/server/server.py | RequestException                   | A (2)     |
| src/server/server.py | submitted_works                    | A (2)     |
| src/server/server.py | RequestException.__init__          | A (1)     |
| src/server/server.py | home                                | A (1)     |
| src/server/server.py | submit_successfully                | A (1)     |
| src/server/server.py | protected                          | A (1)     |
| src/server/server.py | run_server                         | A (1)     |
| src/server/server.py | handle_exception                   | A (1)     |
| src/server/server.py | load_user                          | A (1)     |
| tests/unit/test_part_1.py | HomeworkAppTestCase              | A (2)     |
| tests/unit/test_part_1.py | test_teacher_creation            | A (1)     |
| tests/unit/test_part_1.py | test_student_creation            | A (1)     |
| tests/unit/test_part_1.py | test_homework_creation           | A (1)     |
| tests/unit/test_part_1.py | test_user_creation               | A (1)     |
| tests/unit/test_part_1.py | tearDown                         | A (1)     |
| tests/unit/test_part_1.py | setUp                            | A (1)     |
---

### Индекс сопровождаемости

| Файл                   | Maintainability Index |
|------------------------|----------------------|
| src/main.py           | A (79.74)            |
| src/db/models.py      | A (100.00)           |
| src/server/server.py  | A (37.59)            |
| tests/unit/test_part_1.py | A (56.93)        |
---

## Выявленные недостатки

1. **Высокая цикломатическая сложность в server.py**

* Метрики: Cyclomatic Complexity

* Проблема: Ряд функций (`submit_homework` - B (6), `login` - A (5), `review` - A (4)) имеют высокую сложность, что затрудняет тестирование и увеличивает вероятность ошибок. 

* Подтверждение гипотезы: Действительно, например, в `submit_homework` представлены вложенные ветвления, можно повысить модульность метода.

* Как улучшить: разделить сложные функции на более маленькие, уменьшить количество вложенных ветвлений

2. **Перегруженность файла в server.py**

* Метрики: LOC (Lines of Code), LLOC (Logical Lines of Code)

* Заметим, что в `server.py` 145 строк кода, в то время как во всех файлах 261 строка. То есть больше половины строк сосредоточено в одном файле, из-за чего он может быть перегружен.

* Подтверждение гипотезы: Действительно, в server.py отсутсвует функции, не являющий непосредственно, ручками API, то есть вся логика обработки запроса заключена в рамках одного метода, каждый из которых находится в server.py. 

Решение: Проверку авторизации можно было бы вынести в отдельный файл, так как он представляет собой отдельный логический блок, при увеличении размера проекта он также будет расширяться (за счет обратки OAuth-токенов и session_id). Также можно вынести логику работы с базой данных.