API для распределения задачь в команде.
Проект состоит из:
 - `task_api`:
 - Главное API (FastAPI) со сбором метрик и мониторингом в Grafana
 - Серврис отправки писем на почту запускается в отдельном воркере c помощью TaskIQ (Аналог Selery), в качестве брокера сообщений использован RabbitMQ
 - Используется OAutho2 для авторизации Access + Refresh JWT токены, также реализована кастомное подтверждение почты.
 - Реализован внутрений интерфейс взаимодействия с ботом и вебом.
 - `web_site`: Web-интерфейс на Vite+React
 - `tg_bot`: Телеграмм бот для быстрого доступа к задачам и уведомлениям (возможность запуска через polling и webhooks (по ngrok))
 - `db_worker`: Воркер для основной БД
 

Cтруктура БД и API:
- Публичные эндпоинты (на момент 09.08.2025)
- Управления проетами:
- <img width="755" height="161" alt="изображение" src="https://github.com/user-attachments/assets/67f97ea1-68ee-427f-b6cd-46f28ebc7221" />
- Управление участниками проекта:
- <img width="912" height="460" alt="изображение" src="https://github.com/user-attachments/assets/92cf2ae6-8f98-4ad5-baaa-1e7beee3c94a" />
- Управление задачами проекта
- <img width="940" height="577" alt="изображение" src="https://github.com/user-attachments/assets/ae99f8f1-d5f6-4c85-886b-d585fed41b3b" />
- Авторизация и Регистрация
- <img width="656" height="307" alt="изображение" src="https://github.com/user-attachments/assets/9e915383-24aa-43cb-bbba-f41cb23ee967" />


https://miro.com/welcomeonboard/NG9VblFXbUphOCtCa21ka2w3Qy84ZmRDM0FtQlUvT1pLMkVzdDJzaHlmam1mRzhxejhOc0RNclBCWTIwZk40VUVnWWlwUnl5R0VSNVFEZjUwR2dZUWxteWpBQkpKbk0ydy9xUTE5Qnpub1BhalprMXNEZHYzRUNaYUsrbUhwRHp0R2lncW1vRmFBVnlLcVJzTmdFdlNRPT0hdjE=?share_link_id=290801728870
