# System Monitor

Это простое desktop-приложение для мониторинга загруженности системы (ЦП, ОЗУ, ПЗУ) в реальном времени с возможностью записи данных в базу данных SQLite.

## Требования

- Python 3.7 или выше
- Библиотека `psutil`

## Установка

1. Клонируйте репозиторий или скачайте файл `system_monitor.py`.

2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
## Использование

1. Запустите
   ```bash
   python system_monitor.py
   ```
2. После записи вы можете проверить данные в базе system_monitor.db с помощью SQLite:
   ```bash
   sqlite3 system_metrics.db
   ```
   Запрос для просмотра данных:
   ```
   SELECT * FROM metrics;
   ```
