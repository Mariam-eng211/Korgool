# 🛡️ Korgool (Коргоол)
**Silent SMS Crisis Response Infrastructure for Kyrgyzstan**

## The Problem
In Kyrgyzstan, women facing domestic violence often cannot use existing reporting apps. Abusers frequently monitor smartphones, check call logs, and control mobile data access. Furthermore, women in rural areas or with disabilities may not have access to smartphones or internet.

## The Solution
Korgool is a **zero-trace, offline-first SMS reporting system**. 
- **No App:** The victim just sends an SMS from any $20 Nokia.
- **No Internet:** SMS works on 2G. The NGO's backend runs on a local laptop.
- **No Trace:** She texts a secret pre-registered codeword (e.g., `РОМАШКА`). The abuser thinks it's a typo.
- **30-Minute Vault:** If she requests a callback (`ПОЗВОНИ`), her number is held in a temporary vault for 30 minutes, allowing the operator to call her from a safe line. It is then permanently deleted.

## How it Works
1. **Codeword Path:** Pre-registered women text their secret word. The system instantly displays her name, exact address, and safe contacts to the NGO operator.
2. **Callback Path:** Anonymous women text for help with "ПОЗВОНИ" (Call Me). The operator calls them back securely.
3. **Anonymous Path:** If she stays fully anonymous, the system logs the severity and district for statistical advocacy and patrol mapping.

## Tech Stack (Offline-First)
- **Backend:** Python (Flask)
- **Database:** SQLite (WAL mode enabled for high concurrency)
- **Frontend:** Vanilla JS, HTML, CSS (Light/Dark mode)
- **SMS Gateway Ready:** Integrates via HTTP POST (`/sms/receive`) with any Android SMS Gateway or local telecom provider.

## Running Locally
1. `pip install flask`
2. `python app.py`
3. Open `http://localhost:5000`
4. Use the built-in SMS Simulator to test the triage engine.

*Note: For actual deployment, any Android phone running an SMS Gateway app can point its webhook to `/sms/receive`.*

## Why Open Source?
We built this as public infrastructure. Any crisis center in Kyrgyzstan can download this code, put it on a $50 laptop, and start saving lives tomorrow. We believe safety should not be proprietary.

# 🛡️ Korgool (Коргоол)
**Инфраструктура экстренного реагирования через «тихие» SMS для Кыргызстана**

## Проблема
В Кыргызстане женщины, сталкивающиеся с домашним насилием, зачастую не могут воспользоваться существующими приложениями для подачи сигналов о помощи. Агрессоры нередко следят за смартфонами, проверяют историю звонков и ограничивают доступ к мобильному интернету. Кроме того, у женщин в сельской местности или женщин с инвалидностью может не быть доступа к смартфонам или сети.

## Решение
Korgool — это система подачи сигналов через SMS, которая **не оставляет следов и работает без интернета**.
- **Без приложений:** Пострадавшая может отправить SMS с любого простейшего телефона (например, кнопочного Nokia).
- **Без интернета:** Система работает через SMS в сетях 2G. Серверная часть (бэкенд) разворачивается на обычном ноутбуке.
- **Без следов:** Женщина отправляет заранее зарегистрированное кодовое слово (например, «РОМАШКА»). Агрессор, увидев сообщение, решит, что это просто опечатка.
- **Временное хранение (30 минут):** Если женщина запрашивает обратный звонок (команда «ПОЗВОНИ»), её номер сохраняется во временном защищенном хранилище на 30 минут. Это позволяет оператору связаться с ней по безопасной линии, после чего номер безвозвратно удаляется.

## Как это работает
1. **Через кодовое слово:** Зарегистрированные в системе женщины отправляют секретное слово. Оператор НПО мгновенно видит имя, точный адрес и контакты доверенных лиц.
2. **Запрос обратного звонка:** Женщины могут отправить сообщение с текстом «ПОЗВОНИ». Оператор перезванивает им по защищенному каналу.
3. **Анонимный режим:** Если женщина предпочитает остаться полностью анонимной, система фиксирует только степень серьезности ситуации и район. Эти данные используются для аналитики, адвокации и планирования маршрутов патрулирования.

## Технологический стек (с приоритетом работы офлайн)
- **Бэкенд:** Python (Flask)
- **База данных:** SQLite (включен режим WAL для обеспечения высокой параллельной нагрузки)
- **Фронтенд:** «Чистый» (Vanilla) JS, HTML, CSS (поддержка светлой и темной тем)
- **Интеграция с SMS-шлюзами:** Поддержка взаимодействия через HTTP POST (`/sms/receive`) с любым Android-шлюзом для SMS или напрямую с локальным оператором связи. ## Запуск локально
1. `pip install flask`
2. `python app.py`
3. Откройте `http://localhost:5000`
4. Используйте встроенный симулятор SMS для тестирования системы сортировки обращений.

*Примечание: для реального развертывания можно использовать любой Android-телефон с установленным приложением SMS-шлюза, настроив его вебхук на адрес `/sms/receive`.*

## Почему открытый исходный код?
Мы создали это как общедоступную инфраструктуру. Любой кризисный центр в Кыргызстане может скачать этот код, запустить его на недорогом ноутбуке (стоимостью около 50 долларов) и уже завтра начать спасать жизни. Мы убеждены, что безопасность не должна быть чьей-то частной собственностью.
