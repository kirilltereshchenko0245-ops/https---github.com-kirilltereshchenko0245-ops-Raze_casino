# 🚀 Deployment Guide - Raze Casino

## Быстрый деплой

### 1. Подготовка репозитория

```powershell
cd c:\Raze_casino
git init
git add .
git commit -m "Initial commit - Raze Casino"
```

Создай репозиторий на GitHub и запуш:

```powershell
git remote add origin https://github.com/yourusername/raze-casino.git
git branch -M main
git push -u origin main
```

---

## 🗄️ База данных (Render PostgreSQL)

1. Зайди на https://render.com
2. New → PostgreSQL
3. Настройки:
   - Name: `raze-casino-db`
   - Database: `raze_casino`
   - User: auto
   - Region: ближайший к тебе
4. Сохрани **Internal Database URL** (понадобится для backend)

---

## 🔧 Backend Deploy (Render)

1. New → Web Service
2. Подключи GitHub репозиторий
3. Настройки:
   - **Name:** `raze-casino-api`
   - **Region:** Frankfurt (или ближайший)
   - **Branch:** main
   - **Root Directory:** `backend`
   - **Runtime:** Python 3
   - **Build Command:**
     ```
     pip install -r requirements.txt
     ```
   - **Start Command:**
     ```
     uvicorn app.main:app --host 0.0.0.0 --port $PORT
     ```

4. Environment Variables:
   ```
   DATABASE_URL=[твой Internal Database URL]
   REDIS_URL=redis://red-xxxxx:6379
   BOT_TOKEN=8639775102:AAGXojKkcgzyONMSc02UP1o3N2KtkE7f-EQ
   ADMIN_ID=7924294552
   CHANNEL_ID=-1003993864640
   LOGS_CHANNEL_ID=-1004462118091
   SECRET_KEY=your-super-secret-random-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=43200
   FRONTEND_URL=https://your-app.vercel.app
   ```

5. **Create Web Service**

6. Сохрани URL (например `https://raze-casino-api.onrender.com`)

---

## 🎨 Frontend Deploy (Vercel)

1. Зайди на https://vercel.com
2. Import Project → GitHub → выбери репозиторий
3. Настройки:
   - **Framework Preset:** Vite
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
   - **Install Command:** `npm install`

4. Environment Variables:
   ```
   VITE_API_URL=https://raze-casino-api.onrender.com
   ```

5. **Deploy**

6. Сохрани URL (например `https://raze-casino.vercel.app`)

---

## 🤖 Bot Deploy (Render Background Worker)

1. New → Background Worker
2. Подключи тот же репозиторий
3. Настройки:
   - **Name:** `raze-casino-bot`
   - **Region:** тот же что и backend
   - **Root Directory:** `bot`
   - **Build Command:**
     ```
     pip install -r requirements.txt
     ```
   - **Start Command:**
     ```
     python main.py
     ```

4. Environment Variables:
   ```
   BOT_TOKEN=8639775102:AAGXojKkcgzyONMSc02UP1o3N2KtkE7f-EQ
   ADMIN_ID=7924294552
   CHANNEL_ID=-1003993864640
   LOGS_CHANNEL_ID=-1004462118091
   WEBAPP_URL=https://raze-casino.vercel.app
   ```

5. **Create Background Worker**

---

## 📱 Настройка Mini App в Telegram

1. Найди @BotFather в Telegram
2. Команда: `/mybots`
3. Выбери своего бота
4. **Bot Settings** → **Menu Button**
5. Настрой:
   - Button text: `🎰 Играть`
   - URL: `https://raze-casino.vercel.app`

6. **Configure Mini App** (если есть):
   - Mini App URL: `https://raze-casino.vercel.app`

---

## ✅ Проверка работоспособности

### 1. Backend
```
https://raze-casino-api.onrender.com/
https://raze-casino-api.onrender.com/health
```

### 2. Frontend
```
https://raze-casino.vercel.app
```

### 3. Bot
Открой бота в Telegram и нажми `/start`

---

## 🔧 Обновление кода

После изменений:

```powershell
git add .
git commit -m "Update: описание изменений"
git push
```

- **Vercel** автоматически пересоберёт frontend
- **Render** автоматически пересоберёт backend и bot

---

## 🐛 Troubleshooting

### Backend не запускается:
1. Проверь логи на Render
2. Проверь DATABASE_URL правильный
3. Проверь все environment variables

### Frontend не подключается к API:
1. Проверь VITE_API_URL в Vercel
2. Проверь CORS в backend (settings.FRONTEND_URL)
3. Открой Console в браузере (F12)

### Bot не отвечает:
1. Проверь логи Background Worker
2. Проверь BOT_TOKEN правильный
3. Проверь WEBAPP_URL указывает на Vercel

---

## 💰 Стоимость

- **Render Free Tier:**
  - Web Service: $0 (спит после 15 мин неактивности)
  - Background Worker: $7/мес
  - PostgreSQL: $7/мес
  
- **Vercel Free Tier:**
  - Hosting: $0
  - 100GB bandwidth

**Total: ~$14/мес** для полностью работающего казино

---

## 🚀 Production Ready Checklist

- [ ] Замени SECRET_KEY на случайную строку
- [ ] Настрой Redis (для chat и real-time)
- [ ] Подключи CryptoBot API
- [ ] Подключи xRocket API  
- [ ] Настрой мониторинг (UptimeRobot)
- [ ] Настрой бэкапы базы данных
- [ ] Добавь rate limiting
- [ ] Настрой логирование ошибок (Sentry)
- [ ] SSL сертификаты (автоматически через Vercel/Render)

---

**Готово! Твоё казино онлайн! 🎰🔥**
