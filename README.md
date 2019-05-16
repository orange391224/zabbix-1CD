# zabbix-1CD
Шаблон Zabbix для мониторинга файловых баз 1С (с autodiscovery)
Используется библиотека onec_dtools для проверки структуры базы, подсчета количества таблиц в ней.

## Наблюдаемые параметры
* Количество таблиц в БД
* Размер БД
* Версия БД (именно БД, не конфигурации)
В случае, если при попытке прочтения какого-либо параметра возникает ошибка, взводится тригер

## Инструкция по установке
Импортируйте шаблон в zabbix, назначьте template хосту. 
Вы можете вручную создать item. Для этого используйте ключ:
```
1ctest[C://Path//to//1Cv8.1CD]
```
!!! **Обратите внимание на обратные двойные слэши** - указывать путь до .1CD файла следует именно так, т.к. в Zabbix недопустим символ `\`
Пример ключа:
```
1ctest[F://Tmp//tstbase//1Cv8.1CD]
```
Тип данных: Tекст (Text)
