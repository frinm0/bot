
# Bytecasino — Telegram Mini App на Bytecoin

Полноценное WebApp-казино с Telegram-ботом, реферальной системой, выводом/пополнением и админ-панелью.

---

## 📁 Структура проекта

- `index.html` — Web-интерфейс
- `script.js` — логика WebApp
- `style.css` — оформление
- `admin_api.py` — FastAPI сервер
- `bot.py` — Telegram-бот
- `data.json`, `promos.json`, `transactions.json` — данные
- `.env.example` — переменные окружения

---

## 🚀 Установка

```bash
pip install fastapi uvicorn python-dotenv
```

---

## 🖥 Запуск

1. **API сервер**:
```bash
uvicorn admin_api:app --reload
```

2. **Telegram-бот**:
```bash
python bot.py
```

3. **WebApp (локально)**:
```bash
python3 -m http.server 8080
```

---

## ⚙ Настройки

Создай `.env` на основе `.env.example`, добавь:

```
BOT_TOKEN=...
ADMIN_ID=...
```

---

## 👨‍💼 Админ-функции

- Резерв казино
- История и лог транзакций
- График доходов (по дням)
- Промокоды
- Вывод и пополнение
- CSV экспорт

---

## 📦 Деплой

- Render / VPS / Docker
- Указать WebApp URL в `@BotFather`

---

## ✅ Поддержка

- RTP 90%
- История ставок
- Ежедневный бонус
- Рефералка: 100000 BCN + 2% от ставок
