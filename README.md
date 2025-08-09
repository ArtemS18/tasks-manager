API для распределения задачь в команде.
Проект состоит из:
 - `task_api`
	      -Главное API (FastAPI) со сбором метрик и мониторингом в Grafana
	      -Серврис отправки писем на почту запускается в отдельном воркере c помощью TaskIQ (Аналог Selery), в качестве брокера сообщений использован RabbitMQ
	      -Используется OAutho2 для авторизации Access + Refresh JWT токены, также реализована кастомное подтверждение почты.
	      -Реализован внутрений интерфейс взаимодействия с ботом и вебом.
 - `web_site` Web-интерфейс на Vite+React
 - `tg_bot` Телеграмм бот для быстрого доступа к задачам и уведомлениям (возможность запуска через polling и webhooks (по ngrok))
 - `db_worker` Воркер для основной БД
 

Cтруктура БД и API:
https://miro.com/welcomeonboard/NG9VblFXbUphOCtCa21ka2w3Qy84ZmRDM0FtQlUvT1pLMkVzdDJzaHlmam1mRzhxejhOc0RNclBCWTIwZk40VUVnWWlwUnl5R0VSNVFEZjUwR2dZUWxteWpBQkpKbk0ydy9xUTE5Qnpub1BhalprMXNEZHYzRUNaYUsrbUhwRHp0R2lncW1vRmFBVnlLcVJzTmdFdlNRPT0hdjE=?share_link_id=290801728870
