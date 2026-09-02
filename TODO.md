# 📋 TODO List - Raze Casino

## 🔥 КРИТИЧНО (Сделать в первую очередь)

### Backend API:
- [ ] **Доделать Tower endpoints** в `backend/app/api/games.py`
  - POST /games/tower/start
  - POST /games/tower/choose
  - POST /games/tower/cashout

- [ ] **Доделать Roulette endpoints** в `backend/app/api/games.py`
  - POST /games/roulette/bet
  - GET /games/roulette/result

- [ ] **Добавить Payment endpoints** (новый файл `backend/app/api/payments.py`)
  - POST /payments/deposit (CryptoBot + xRocket)
  - GET /payments/deposit/status
  - POST /payments/withdraw
  - GET /payments/withdrawals (история)

- [ ] **Добавить Balance endpoints** в `backend/app/api/balance.py`
  - GET /balance
  - POST /balance/ref-transfer (перевод с реферального на основной)
  - GET /balance/transactions

- [ ] **Добавить User endpoints** в `backend/app/api/user.py`
  - GET /user/profile
  - PATCH /user/settings
  - GET /user/stats
  - POST /user/daily-bonus

- [ ] **Добавить Referral endpoints** в `backend/app/api/referral.py`
  - GET /referral/info
  - GET /referral/list
  - POST /referral/claim-bonus

- [ ] **Добавить Admin endpoints** в `backend/app/api/admin.py`
  - GET /admin/users
  - POST /admin/user/ban
  - POST /admin/user/balance
  - GET /admin/stats
  - GET /admin/withdrawals
  - POST /admin/withdrawal/approve
  - POST /admin/withdrawal/reject
  - POST /admin/promocode/create
  - POST /admin/broadcast

### Frontend:
- [ ] **Доделать MinesPage.tsx**
  - Интеграция с API (reveal, cashout)
  - Анимация взрывов
  - Звуковые эффекты

- [ ] **Сделать TowerPage.tsx** полностью
  - UI башни с 10 уровнями
  - Выбор дверей (3 на уровень)
  - Анимация подъёма
  - Интеграция с API

- [ ] **Сделать RoulettePage.tsx** полностью
  - Анимированное колесо рулетки
  - Выбор множителя (x2, x3, x5, x30)
  - История результатов
  - Интеграция с API

- [ ] **Создать DepositPage.tsx**
  - Выбор метода (CryptoBot / xRocket)
  - Генерация invoice
  - Проверка статуса платежа
  - История депозитов

- [ ] **Создать WithdrawPage.tsx**
  - Форма вывода
  - Список заявок (pending/approved/rejected)
  - История выводов

- [ ] **Доделать HistoryPage.tsx**
  - Загрузка истории игр из API
  - Фильтры (по игре, дате)
  - Пагинация
  - Детали каждой игры

- [ ] **Создать ChatPage.tsx**
  - WebSocket подключение
  - Отправка сообщений
  - Live обновления
  - Модерация

- [ ] **Создать AdminPage.tsx**
  - Статистика (пользователи, обороты)
  - Управление пользователями
  - Заявки на вывод
  - Создание промокодов
  - Рассылка

### Bot:
- [ ] **Добавить уведомления**
  - При выигрыше (с деталями)
  - При новом реферале
  - О доступном бонусе

- [ ] **Логирование в канал**
  - Новые пользователи
  - Крупные выигрыши
  - Депозиты/выводы
  - Действия админа

---

## ⚠️ ВАЖНО (Сделать после критичных)

### Backend:
- [ ] Добавить Promocode logic
- [ ] Добавить Daily bonus cooldown check
- [ ] Добавить Wager tracking
- [ ] Настроить WebSocket для чата
- [ ] Добавить Rate limiting
- [ ] Настроить Redis для кеша
- [ ] Добавить email notifications (опционально)

### Frontend:
- [ ] Добавить анимации для всех игр
- [ ] Добавить звуковые эффекты
- [ ] Добавить прогресс бары
- [ ] Оптимизация под мобильные
- [ ] Добавить loading states везде
- [ ] Обработка ошибок (toast notifications)
- [ ] Offline mode support

### Security:
- [ ] Добавить CSRF protection
- [ ] Input validation на всех формах
- [ ] Rate limiting на API
- [ ] Captcha для критичных действий
- [ ] 2FA для админа (опционально)

---

## 🎨 УЛУЧШЕНИЯ (Можно сделать потом)

### UI/UX:
- [ ] Лучшая адаптация под разные экраны
- [ ] Skeleton loaders
- [ ] Smooth transitions
- [ ] Haptic feedback (Telegram)
- [ ] Confetti анимация при выигрыше
- [ ] Dark/Light theme sync с Telegram

### Features:
- [ ] Лидерборды (топ по выигрышам)
- [ ] Достижения (badges)
- [ ] VIP система
- [ ] Турниры
- [ ] Jackpot система
- [ ] Колесо фортуны
- [ ] Ежедневные задания

### Analytics:
- [ ] Интеграция Sentry (error tracking)
- [ ] Google Analytics
- [ ] User behavior tracking
- [ ] A/B testing

### Performance:
- [ ] Lazy loading компонентов
- [ ] Image optimization
- [ ] Bundle size optimization
- [ ] API response caching
- [ ] Database query optimization

---

## 🔧 ТЕХНИЧЕСКИЙ ДОЛГ

### Backend:
- [ ] Написать тесты (pytest)
- [ ] Добавить API documentation (Swagger)
- [ ] Настроить Alembic migrations properly
- [ ] Добавить logging во все endpoints
- [ ] Error handling improvement
- [ ] Add type hints везде
- [ ] Refactor large files

### Frontend:
- [ ] Написать тесты (Jest + React Testing Library)
- [ ] Добавить Storybook для компонентов
- [ ] Рефакторинг дублирующегося кода
- [ ] TypeScript strict mode
- [ ] ESLint rules enforcement
- [ ] Accessibility (a11y) improvements

### DevOps:
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Automated testing
- [ ] Automated deployment
- [ ] Monitoring setup (UptimeRobot)
- [ ] Backup strategy
- [ ] Disaster recovery plan

---

## 📊 МЕТРИКИ ДЛЯ ОТСЛЕЖИВАНИЯ

После запуска отслеживать:
- [ ] DAU (Daily Active Users)
- [ ] Retention rate
- [ ] Average session duration
- [ ] Conversion rate (регистрация → первая ставка)
- [ ] ARPU (Average Revenue Per User)
- [ ] House profit margin
- [ ] Withdrawal approval time
- [ ] Support ticket response time

---

## 🐛 ИЗВЕСТНЫЕ БАГИ

> Пока нет, но добавляй сюда по мере нахождения!

---

## 💡 ИДЕИ ДЛЯ БУДУЩЕГО

- [ ] Мобильное приложение (iOS/Android)
- [ ] Web версия (не только Telegram)
- [ ] Другие криптовалюты (TON, BTC, ETH)
- [ ] NFT интеграция
- [ ] Social features (друзья, челленджи)
- [ ] Live дилеры (для карточных игр)
- [ ] Спортивные ставки
- [ ] Интеграция с другими платформами

---

## 📝 ПРИОРИТЕТЫ

### Неделя 1:
1. Доделать все game endpoints (Tower, Roulette)
2. Доделать все game pages во frontend
3. Базовое тестирование

### Неделя 2:
1. Payment integration (CryptoBot + xRocket)
2. Deposit/Withdraw pages
3. Admin panel

### Неделя 3:
1. Referral system полностью
2. Daily bonus
3. Promocodes

### Неделя 4:
1. Chat system
2. History page
3. Notifications

### Неделя 5:
1. Testing все features
2. Bug fixes
3. Performance optimization

### Неделя 6:
1. Production deploy
2. Marketing materials
3. Launch! 🚀

---

## ✅ CHECKLIST ПЕРЕД ЗАПУСКОМ

Production Ready:
- [ ] Все игры работают
- [ ] Платежи работают (deposit + withdraw)
- [ ] Реферальная система работает
- [ ] Админ панель работает
- [ ] Нет критичных багов
- [ ] Security audit пройден
- [ ] Performance оптимизирован
- [ ] Backup настроен
- [ ] Monitoring настроен
- [ ] Support готов
- [ ] Документация готова
- [ ] Terms of Service написаны
- [ ] Privacy Policy написана
- [ ] Legal advice получен (gambling законы)

---

**Удачи в разработке! 🔥**

*Отмечай выполненные задачи галочками ✅*
