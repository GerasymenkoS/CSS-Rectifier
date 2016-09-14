# CSS-Rectifier
Python script for parsing css and html files.

Скрипт написанный языком Python 3.4, который выполняет поиск всех css и html файлов в выбранной директории (поиск проводится также в субдиректориях выбранной папки) и отслеживает на используемость каждого css-стиля в файлах html. 

Требования : 

1. Python 3.x

2. jinja2

3. pyjade

Возможности : 

1. Поиск любых css селекторов в html. 

2. Вывод неиспользуемых либо неправильно записанных селекторов.

3. Проверка каждого html файла на соотношение закрытых тегов к открытым.

4. Наличие конфигурационного файла для игнорирования определенных css файлов или директорий (node_modules).

5. Наличие опций при запуске скрипта (--path full/path/to/project/). Если путь не указан скрипт будет отрабатывать в директории из которой был вызван скрипт.

6. Вычисление % используемости всех css селекторов.

7. Минификация всех css файлов (включая удаление комментариев).

8. Возможность получить информацию по всем селекторам (в каком файле находится и номер строки в файле).

9. Если селектор описан не правильно и лишь часть его правильно описана, существует возможность узнать в каком файле html существует селектор, который правильно описан (работает только для id и class).

10. Создание отчета по неиспользуемым селекторам в виде html страницы.

11. Возможность указать в каком виде нужно вывести данные: список, либо отчет.

12. Добавлена опция --report path, с помощью которой скрипт создаст файл отчета в <path>, если <path> не задан, тогда файл отчета будет создан в папке вызова скрипта.

13. Добавлена опция --template name_of_template_processor, с помощью которой скрипт соеденит воедино нужные шаблоны по заданному шаблонизатору.

13. Добавлена возможность парсинга html страниц использующих шаблонизатор jinja2.

14. Добавлена возможность парсинга html страниц использующих шаблонизатор jade.
