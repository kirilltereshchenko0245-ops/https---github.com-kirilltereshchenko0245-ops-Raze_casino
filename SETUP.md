# 🚀 Raze Casino - Setup Guide

## 📋 Требования

- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Redis

## ⚙️ Backend Setup

### 1. Установка зависимостей

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Настройка переменных окружения

Создай файл `.env` в папке `backend/`:

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/raze_casino
REDIS_URL=redis://localhost:6379

BOT_TOKEN=8639775102:AAGXojKkcgzyONMSc02UP1o3N2KtkE7f-EQ
ADMIN_ID=7924294552
CHANNEL_ID=-1003993864640
LOGS_CHANNEL_ID=-1004462118091

SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256

CRYPTOBOT_API_KEY=your-key
XROCKET_API_KEY=your-key

FRONTEND_URL=http://localhost:5173
```

### 3. Создание базы данных

```sql
CREATE DATABASE raze_casino;
```

### 4. Запуск backend

```powershell
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API будет доступен на: http://localhost:8000

---

## 🎨 Frontend Setup

### 1. Установка зависимостей

```powershell
cd frontend
npm install
```

### 2. Настройка переменных окружения

Создай файл `.env` в папке `frontend/`:

```env
VITE_API_URL=http://localhost:8000
```

### 3. Запуск frontend

```powershell
npm run dev
```

Frontend будет доступен на: http://localhost:5173

---

## 🤖 Bot Setup

### 1. Установка зависимостей

```powershell
cd bot
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Настройка

Создай файл `.env` в папке `bot/`:

```env
BOT_TOKEN=8639775102:AAGXojKkcgzyONMSc02UP1o3N2KtkE7f-EQ
ADMIN_ID=7924294552
CHANNEL_ID=-1003993864640
LOGS_CHANNEL_ID=-1004462118091
WEBAPP_URL=https://your-frontend-url.vercel.app
```

### 3. Запуск бота

```powershell
python main.py
```

---

## 🌐 Деплой

### Backend (Render.com)

1. Создай новый Web Service
2. Подключи GitHub репозиторий
3. Настройки:
   - Build Command: `pip install -r backend/requirements.txt`
   - Start Command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Добавь переменные окружения
5. Подключи PostgreSQL базу данных

### Frontend (Vercel)

1. Импортируй репозиторий
2. Настройки:
   - Framework Preset: Vite
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`
3. Добавь переменную окружения `VITE_API_URL`

### Bot (Render.com)

1. Создай новый Background Worker
2. Настройки:
   - Build Command: `pip install -r bot/requirements.txt`
   - Start Command: `cd bot && python main.py`
3. Добавь переменные окружения

---

## 🧪 Тестирование

### Backend API

```powershell
# Test health endpoint
curl http://localhost:8000/health

# Test crash game distribution
python backend/app/games/crash.py
```

### Frontend

```powershell
cd frontend
npm run build
npm run preview
```

---

## 📊 Структура проекта

```
c:\Raze_casino\
├── backend/              # FastAPI API
│   ├── app/
│   │   ├── api/         # API endpoints
│   │   ├── core/        # Config, security
│   │   ├── db/          # Database models
│   │   ├── games/       # Game logic
│   │   └── main.py      # Entry point
│   └── requirements.txt
│
├── frontend/            # React Mini App
│   ├── src/
│   │   ├── api/        # API client
│   │   ├── components/ # UI components
│   │   ├── games/      # Game components
│   │   ├── pages/      # Pages
│   │   ├── store/      # State management
│   │   └── App.tsx
│   └── package.json
│
├── bot/                # Telegram Bot
│   ├── handlers/
│   ├── main.py
│   └── requirements.txt
│
└── README.md
```

---

## 🎮 Игры

### Реализовано:
- ✅ Краш (полностью)
- 🔨 Мины (частично - UI готов, нужна интеграция с API)
- 📝 Башня (заглушка)
- 📝 Рулетка (заглушка)

### Механики:
- Провably Fair система
- Комиссия казино 5%
- RTP 96% (Краш)
- Правильное распределение результатов

---

## 🚨 TODO (Что доделать)

### Backend:
- [ ] Endpoints для Tower и Roulette в games.py
- [ ] WebSocket для real-time чата
- [ ] Payment endpoints (CryptoBot, xRocket)
- [ ] Admin panel endpoints
- [ ] Referral system endpoints
- [ ] Daily bonus logic
- [ ] Promocode system

### Frontend:
- [ ] Полная интеграция Mines с API
- [ ] Реализация Tower игры
- [ ] Реализация Roulette игры
- [ ] Страница чата
- [ ] Админ панель
- [ ] Страница депозита/вывода
- [ ] Анимации для игр
- [ ] Звуковые эффекты

### Bot:
- [ ] Уведомления о выигрышах
- [ ] Уведомления о рефералах
- [ ] Логирование в канал
- [ ] Команды для поддержки

---

## 💡 Полезные команды

```powershell
# Backend
cd backend
uvicorn app.main:app --reload

# Frontend
cd frontend
npm run dev
npm run build

# Bot
cd bot
python main.py

# Тест игровых механик
python backend/app/games/crash.py
python backend/app/games/mines.py
python backend/app/games/tower.py
python backend/app/games/roulette.py
```

---

## 📞 Поддержка

Если что-то не работает:
1. Проверь все зависимости установлены
2. Проверь переменные окружения
3. Проверь подключение к базе данных
4. Проверь логи в консоли

---

**Успехов! 🎰🔥**
