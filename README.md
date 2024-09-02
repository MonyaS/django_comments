
# Django comments

Django comments service.

Buid with Django, React, RabbitMQ.

Additional 




## Installation

Install my-project with docker-compose

```bash
  git clone https://github.com/MonyaS/django_comments.git
  cd django_comments
```

After copying the repository you need to create config.env file from config_example.env.


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`PROJECT_NAME`

`DB_NAME` Db username

`DB_USER`

`DB_USER_PASSWORD`

`POSTGRES_PORT`

`SECRET_KEY`

`AUTH_TOKEN_KEY` Key for user auth tokens

`WS_TOKEN_KEY` Key for websocket connection tokens


After creating config.env, you can start an application.
```bash
  docker-compose --env-file config.env up  -d --force-recreate --build    
```
## API Reference

#### User registration

```http
  POST /api/register/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `mailbox_address` | `string` | **Required**. User mailbox address. |
| `password` | `string` | **Required**. User password.Password must contain 8 characters and at least one number, one letter and one special character. |
| `username` | `string` | **Required**. User username. |

#### User login

```http
  POST /api/login/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `mailbox_address`      | `string` | **Required**. User mailbox address. |
| `password`      | `string` | **Required**. User password.|

#### Get user WebSocket token

```http
  POST /api/refresh_token/
```

| Cookies | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `token`      | `string` | **Required**. Token from auth user methods. |

#### WebSocket connection

```Websocker
  ws /ws/comments/
```

| Headers | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Authorization`      | `string` | **Required**. Token from WebSocket token method. |

## Roadmap

- Connect Pika for WS consumer and add RabbitMQ broker to docker compose file

- Create microservices for Captcha, Comments saving, Logger
