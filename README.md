# 🎰 Raze Casino - Telegram Mini App

> Полнофункциональное онлайн казино в Telegram с провably fair играми, реферальной системой и криптоплатежами.

![Status](https://img.shields.io/badge/status-in%20development-yellow)
![License](https://img.shields.io/badge/license-MIT-blue)

## 🎮 Игры

### ✅ Реализовано:
- **💥 Краш** - Поймай момент до краша с провably fair системой и RTP 96%
- **💎 Мины** - 5x5 поле, 2-24 мины, растущий множитель
- **🏰 Башня** - 10 уровней подъёма с увеличивающимися множителями
- **🎡 Рулетка** - x2, x3, x5, x30 множители с красивой анимацией

### 🎯 Особенности игр:
- Provably Fair система (можно проверить честность)
- Минимальная ставка: $0.30
- Комиссия казино: 5% на выигрыш
- RTP (Return To Player): 96%
- Server + Client Seeds для генерации результатов

---

## 💰 Экономика

### Ставки и выплаты:
- Минимальная ставка: **$0.30**
- Минимальный депозит: **$0.50**
- Минимальный вывод: **$2.00**
- Комиссия на вывод: **5%**

### Реферальная система:
- Обычный реферал: **+$0.15**
- Premium реферал: **+$0.20**
- **35%** с депозитов рефералов
- Бонус за 10 рефералов: **$3.00**
- Вагер на вывод: **x10**
- Минимум перевода на баланс: **$0.90**

### Бонусы:
- Ежедневный бонус (каждые 24 часа)
- Промокоды (создаёт админ)
- Награды за рефералов
- Задание: подписка на канал

---

## 🏗️ Технологии

### Backend:
- **FastAPI** - современный Python web framework
- **PostgreSQL** - база данных
- **SQLAlchemy 2.0** - ORM с async support
- **Redis** - кеширование и real-time
- **Provably Fair** - честная игровая механика

### Frontend:
- **React 18** + **TypeScript**
- **Vite** - быстрый bundler
- **Tailwind CSS** - utility-first CSS
- **Zustand** - state management
- **React Query** - data fetching
- **Telegram Mini Apps SDK** - интеграция с Telegram

### Bot:
- **aiogram 3.x** - modern Telegram bot framework
- **asyncio** - асинхронная работа

### Платежи:
- **CryptoBot API** - USDT платежи
- **xRocket API** - альтернативный провайдер

---

## 📁 Структура проекта

```
c:\Raze_casino\
├── backend/                 # FastAPI API
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Config, security
│   │   ├── db/             # Database models
│   │   ├── games/          # Game logic
│   │   │   ├── crash.py    # ✅ Краш механика
│   │   │   ├── mines.py    # ✅ Мины механика
│   │   │   ├── tower.py    # ✅ Башня механика
│   │   │   └── roulette.py # ✅ Рулетка механика
│   │   └── main.py
│   └── requirements.txt
│
├── frontend/               # React Mini App
│   ├── src/
│   │   ├── api/           # API client
│   │   ├── components/    # UI компоненты
│   │   ├── games/         # Игровые компоненты
│   │   ├── pages/         # Страницы
│   │   │   ├── HomePage.tsx       # ✅ Главная
│   │   │   ├── CrashPage.tsx      # ✅ Краш (полностью)
│   │   │   ├── MinesPage.tsx      # 🔨 Мины (частично)
│   │   │   ├── TowerPage.tsx      # 📝 Башня (заглушка)
│   │   │   ├── RoulettePage.tsx   # 📝 Рулетка (заглушка)
│   │   │   ├── ProfilePage.tsx    # ✅ Профиль
│   │   │   └── HistoryPage.tsx    # 📝 История
│   │   ├── store/         # State management
│   │   └── App.tsx
│   └── package.json
│
├── bot/                   # Telegram Bot
│   ├── main.py           # ✅ Основной бот
│   ├── config.py
│   └── requirements.txt
│
├── SETUP.md              # 📖 Инструкция по установке
├── DEPLOYMENT.md         # 🚀 Инструкция по деплою
└── README.md
```

---

## 🚀 Быстрый старт

### 1. Клонировать репозиторий

```powershell
cd c:\Raze_casino
```

### 2. Backend

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Создай .env файл (смотри backend/.env.example)
# Настрой PostgreSQL

uvicorn app.main:app --reload
```

API: http://localhost:8000

### 3. Frontend

```powershell
cd frontend
npm install

# Создай .env файл (смотри frontend/.env.example)

npm run dev
```

App: http://localhost:5173

### 4. Bot

```powershell
cd bot
pip install -r requirements.txt

# Создай .env файл

python main.py
```

📖 **Подробная инструкция:** [SETUP.md](SETUP.md)

---

## 📦 Деплой

### Рекомендуемый стек:
- **Backend:** Render.com Web Service
- **Database:** Render.com PostgreSQL
- **Frontend:** Vercel
- **Bot:** Render.com Background Worker

**Стоимость:** ~$14/месяц

📖 **Полная инструкция по деплою:** [DEPLOYMENT.md](DEPLOYMENT.md)

---

## ✅ Что готово

### Backend:
- ✅ FastAPI приложение с async
- ✅ База данных (PostgreSQL)
- ✅ Модели данных (Users, Games, Transactions)
- ✅ Аутентификация (Telegram Mini App)
- ✅ Игровая механика Crash (провably fair)
- ✅ Игровая механика Mines
- ✅ Игровая механика Tower  
- ✅ Игровая механика Roulette
- ✅ API endpoints для Crash
- ✅ API endpoints для Mines (частично)
- ✅ Security (JWT, Telegram init data verification)
- ✅ CORS настройка

### Frontend:
- ✅ React + TypeScript + Vite
- ✅ Tailwind CSS styling
- ✅ Layout с навигацией
- ✅ Главная страница (Dashboard)
- ✅ Профиль с реферальной системой
- ✅ Игра Краш (полностью работает)
- ✅ Игра Мины (UI готов)
- ✅ State management (Zustand)
- ✅ API client (axios)
- ✅ Telegram Mini App интеграция
- ✅ Тёмная/светлая тема

### Bot:
- ✅ Telegram бот (aiogram 3.x)
- ✅ Команда /start
- ✅ Кнопка открытия Mini App
- ✅ Логирование в канал

---

## 🔨 Что нужно доделать

### Backend (высокий приоритет):
- [ ] **Tower & Roulette API endpoints** в games.py
- [ ] **Payment system** (CryptoBot + xRocket integration)
- [ ] **User balance operations** (deposit, withdraw)
- [ ] **Referral system** (tracking, bonuses)
- [ ] **Daily bonus** logic
- [ ] **Promocode system** (create, use, track)
- [ ] **Admin endpoints** (users, bans, balance, stats)
- [ ] **WebSocket** для real-time chat
- [ ] **Withdrawal approval** workflow

### Frontend (высокий приоритет):
- [ ] **Полная интеграция Mines** с API
- [ ] **Реализация Tower** игры с UI
- [ ] **Реализация Roulette** с анимацией колеса
- [ ] **Страница депозита** (CryptoBot, xRocket)
- [ ] **Страница вывода** с историей заявок
- [ ] **История игр** с фильтрами
- [ ] **Live чат** с модерацией
- [ ] **Админ панель** (stats, users, withdrawals)
- [ ] **Анимации** для всех игр
- [ ] **Звуковые эффекты**
- [ ] **Уведомления** (Telegram notifications)

### Bot (средний приоритет):
- [ ] **Уведомления о выигрышах** с деталями игры
- [ ] **Уведомления о рефералах** 
- [ ] **Напоминания о бонусе**
- [ ] **Логирование** всех действий в канал
- [ ] **Команды поддержки**

### Дополнительно (низкий приоритет):
- [ ] Лидерборды (топ игроков)
- [ ] VIP система
- [ ] Турниры
- [ ] Достижения
- [ ] Мобильная оптимизация
- [ ] PWA support
- [ ] Мультиязычность
- [ ] Аналитика (Sentry, GA)

---

## 🎨 Дизайн

### Цветовая схема:
- **Тёмная тема** (по умолчанию):
  - Background: `#0a0e1a`
  - Cards: `#111827`
  - Accent: Purple (`#9333ea`) + Blue (`#3b82f6`)
  
- **Светлая тема**:
  - Background: `#f9fafb`
  - Cards: `#ffffff`
  - Accent: Purple + Blue

### UI/UX:
- Glassmorphism эффекты
- Плавные анимации (Framer Motion)
- Градиенты и неоновое свечение
- Адаптивный дизайн
- Touch-friendly интерфейс

---

## 🔐 Безопасность

- ✅ Telegram init data verification
- ✅ JWT токены
- ✅ Provably Fair игры (server + client seeds)
- ✅ Хеширование результатов (SHA256)
- ⏳ Rate limiting (TODO)
- ⏳ Input validation (TODO)
- ⏳ SQL injection protection (using ORM)
- ⏳ XSS protection (TODO)

---

## 📊 Игровые механики

### Crash:
```python
# RTP: 96%
# House Edge: 4%
# Distribution:
# x1.00-x1.50:  40%
# x1.50-x3.00:  30%
# x3.00-x10.0:  20%
# x10.0-x50.0:   8%
# x50.0-x500:   1.8%
# x500+:         0.2%
```

### Mines:
```python
# Field: 5x5 (25 cells)
# Mines: 2-24
# Multipliers based on:
# - Number of mines
# - Cells revealed
# Example: 5 mines, 10 cells = x7.41
```

### Tower:
```python
# Levels: 10
# Doors per level: 3
# Multipliers:
# Level 1: x1.21
# Level 5: x2.94
# Level 10: x8.99
```

### Roulette:
```python
# Sectors: 100
# x2 (blue):   47% chance
# x3 (yellow): 30% chance
# x5 (red):    20% chance
# x30 (green):  3% chance
```

---

## 📝 Конфигурация

### Backend (.env):
```env
DATABASE_URL=postgresql+asyncpg://...
REDIS_URL=redis://...
BOT_TOKEN=...
ADMIN_ID=7924294552
CHANNEL_ID=-1003993864640
LOGS_CHANNEL_ID=-1004462118091
SECRET_KEY=...
CRYPTOBOT_API_KEY=...
XROCKET_API_KEY=...
```

### Frontend (.env):
```env
VITE_API_URL=http://localhost:8000
```

### Bot (.env):
```env
BOT_TOKEN=...
WEBAPP_URL=https://your-app.vercel.app
```

---

## 🧪 Тестирование

```powershell
# Тест игровых механик
python backend/app/games/crash.py
python backend/app/games/mines.py
python backend/app/games/tower.py
python backend/app/games/roulette.py

# Тест API
curl http://localhost:8000/health

# Тест frontend build
cd frontend && npm run build
```

---

## 📞 Поддержка

Если возникли проблемы:
1. Проверь [SETUP.md](SETUP.md)
2. Проверь [DEPLOYMENT.md](DEPLOYMENT.md)
3. Проверь логи в консоли
4. Проверь переменные окружения
5. Открой issue на GitHub

---

## 🎯 Roadmap

### Phase 1 (Текущая): Core Features ✅
- [x] Backend API structure
- [x] Game mechanics (Crash, Mines, Tower, Roulette)
- [x] Frontend structure
- [x] Telegram bot
- [x] Basic UI

### Phase 2: Integration 🔨
- [ ] Complete all game integrations
- [ ] Payment systems
- [ ] Referral system
- [ ] Admin panel

### Phase 3: Polish 📝
- [ ] Animations
- [ ] Sound effects
- [ ] Mobile optimization
- [ ] Testing

### Phase 4: Launch 🚀
- [ ] Production deploy
- [ ] Marketing
- [ ] User onboarding
- [ ] Support

---

## 📄 License

MIT License - делай что хочешь! 🔥

---

## 🤝 Contributing

Contributions welcome! 

1. Fork репозиторий
2. Создай feature branch
3. Commit изменения
4. Push в branch
4. Открой Pull Request

---

**Built with ❤️ by Raze Team**

🎰 Удачи в играх! 🔥
