Код который распознаёт ATX файлы из папки CONF и при взаимодействии с кнопками программы добавляет их в БД, либо же обновляет данные по прибору, если была созданна новая конфигурация. По нажатию кнопки может создать и удалить таблицы для базы данных. Создаёт таблицы "atx" и "shadow".
В atx хранится актуальная информация о конфигурации прибора, а в "тени" хранятся данные которые были до обновления данных в atx через программу, тоесть бэкапы.

GUI Реализован через библиотеку tkinter, и в папке output лежит скомпилированный exe-шник скрипта.

РАБОТАЕТ НА POSTGRESQL 
