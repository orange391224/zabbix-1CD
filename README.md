# zabbix-1CD
Шаблон Zabbix для мониторинга файловых баз 1С (с autodiscovery)

Используется библиотека onec_dtools (https://github.com/Infactum/onec_dtools) для проверки структуры базы, подсчета количества таблиц в ней.

## Наблюдаемые параметры
* Количество таблиц в БД
* Размер БД
* Версия БД (именно БД, не конфигурации)
В случае, если при попытке прочтения какого-либо параметра возникает ошибка, взводится тригер

## Инструкция по установке
Необходимо добавить Userparameter для агента. 
Для этого скопируйте файл `test1C.exe` в директорию на машине-агенте (**крайне желательно, чтобы в пути не было пробелов и русских символов**). 

Далее, в conf файле агента добавьте Userparameter:
```
UserParameter=1ctest[*],C:\path\to\test1C.exe "$1"
```
Например:
```
UserParameter=1ctest[*],C:\zabbix_mod\test1C.exe "$1"
```
_____________

Далее импортируйте шаблон в zabbix, назначьте template хосту. 
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

Но проще будет прописать свои параметры в 1cd_config.cfg, запустить 1cd_discovery.exe - и в заббиксе всё создастся само.

## Настройка autodiscovery
***!!!*** В силу особенностей компиляции скрипт обнаружения будет работать только в x64 окружении. В папке src лежат исходные тексты на Python, вы можете запустить их в своем окружении через интерпретатор Python.

В том случае, если у Вас много баз данных и/или они добавляются пригодится автообнаружение. Для его настройки скопируйте файлы
1cd_discovery.exe и 1cd_config.cfg в папку на машине-агенте (**крайне желательно, чтобы в пути не было пробелов и русских символов**).
Затем укажите свои параметры в файле 1cd_config.cfg

Следующим шагом, настройте автоматически запуск 1cd_discovery.exe с необходимой периодичностью. Для этой цели прекрасно подходит планировщик windows 

Скрипт 1cd_discovery.exe рекурсивно проходит по всем дискам машины в поисках файлов `*.1CD`.После обхода, сформированный JSON отправляется в Zabbix-сервер и на нём создаются item'ы и триггеры для всех баз. Поскольку данный процесс достсточно затратный в плане IO рекомендую настроить его запуск во время минимальной нагрузки на машину. 

### Техподдержка:
Вопросы можете задать в Telegram: orangekrs

Либо создавайте issues
