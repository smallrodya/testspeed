# speedtest.py

Простой скрипт на **Python 3** (только стандартная библиотека, `pip` не нужен).

Он принимает URL (лучше — тяжёлая картинка или файл), делает **10 запросов подряд**, каждый раз дожидается полного ответа, затем печатает:

- среднее время одного запроса
- объём скачанных данных
- среднюю скорость в **МБ/с** (1 МБ = 1 000 000 байт)

Запросы идут **последовательно**, не параллельно: следующий стартует только после ответа предыдущего.

## Что нужно

- Python 3.8+ (подойдёт 3.9 / 3.10 / 3.11 / 3.12 / 3.13)
- Git
- Интернет
- URL с `http://` или `https://`

Сторонние пакеты не устанавливаются.

## macOS

1. Откройте **Terminal**.
2. Проверьте Python:

```bash
python3 --version
```

Если команды нет, поставьте Python с [python.org](https://www.python.org/downloads/) или через Homebrew: `brew install python`.

3. Склонируйте репозиторий и запустите скрипт:

```bash
git clone https://github.com/smallrodya/testspeed.git
cd testspeed
python3 speedtest.py https://upload.wikimedia.org/wikipedia/commons/3/3f/Fronalpstock_big.jpg
```

## Windows

1. Установите Python 3 с [python.org](https://www.python.org/downloads/windows/).
   На установщике включите галочку **Add python.exe to PATH**.
2. Откройте **Command Prompt** (`cmd`) или **PowerShell**.
3. Проверьте:

```bat
python --version
```

Если не сработало, попробуйте `py --version`.

4. Склонируйте репозиторий и запустите скрипт:

```bat
git clone https://github.com/smallrodya/testspeed.git
cd testspeed
python speedtest.py https://upload.wikimedia.org/wikipedia/commons/3/3f/Fronalpstock_big.jpg
```

или:

```bat
git clone https://github.com/smallrodya/testspeed.git
cd testspeed
py speedtest.py https://upload.wikimedia.org/wikipedia/commons/3/3f/Fronalpstock_big.jpg
```

## Параметры

```text
python3 speedtest.py URL
python3 speedtest.py URL -n 10
python3 speedtest.py URL --timeout 60
```

| Аргумент | Смысл | По умолчанию |
|---|---|---|
| `URL` | Адрес, куда стучаться (картинка / файл) | обязательный |
| `-n` / `--count` | Сколько запросов подряд | `10` |
| `--timeout` | Таймаут одного запроса, секунды | `60` |

Справка:

```bash
python3 speedtest.py -h
```

## Пример вывода

```text
[1/10] GET https://example.com/big.jpg ... 0.842 s, 2457600 bytes, 2.92 MB/s
[2/10] GET https://example.com/big.jpg ... 0.791 s, 2457600 bytes, 3.11 MB/s
...
[10/10] GET https://example.com/big.jpg ... 0.805 s, 2457600 bytes, 3.05 MB/s

--- summary ---
requests:           10
avg request time:   0.812 s
avg payload:        2457600 bytes
total downloaded:   24576000 bytes (24.58 MB)
total time:         8.120 s
average speed:      3.03 MB/s
```

Скорость считается так: **все скачанные байты / суммарное время 10 запросов**.

## Замечания

- Берите достаточно большой файл (хотя бы сотни КБ / несколько МБ). На крошечной картинке скорость будет шумной: большую долю времени займёт рукопожатие TCP/TLS, а не сама передача.
- Это не полноценный speedtest.net: измеряется скорость скачивания **конкретного URL** с вашего компьютера. На результат влияют CDN, кэш, Wi‑Fi и загрузка канала.
- При ошибке HTTP, таймауте или недоступном адресе скрипт печатает причину и выходит с кодом `1`.
