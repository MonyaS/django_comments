
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

*Name that will be added to all containers, must be uniq*

`PROJECT_NAME`

*Credentials for API gateway service*

`DB_NAME` Db username

`DB_USER`

`DB_USER_PASSWORD`

`POSTGRES_PORT`

*Credentials for comment microservices*

`COMMENTS_DB_NAME` 

`COMMENTS_DB_USER`

`COMMENTS_DB_USER_PASSWORD`

`POSTGRES_PORT`

*Credentials for RabbitMq message broker*

`RABBITMQ_USER`

`RABBITMQ_USER_PASSWORD`

*Credentials for Redis Db*

`REDIS_PASSWORD`

*Secret encription keys*

`SECRET_KEY`

`AUTH_TOKEN_KEY` Key for user auth tokens

`WS_TOKEN_KEY` Key for websocket connection tokens


After creating config.env, you can start an application.
```bash
  docker compose --env-file config.env up  -d --force-recreate --build    
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


## WS documentation

### Incoming messages

#### All exist comments
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `comments` | `list` | List of json formated exist comments. |


##### Comments structure
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `record_id` | `list` | Internal id of record, use while addind a new comments as an answer. |
| `user_id` | `list` | Internal id of user that left this comment. |
| `parent_id` | `list` |  Internal id of the record to which this record is bound. |
| `text` | `list` | Record text. |
| `home_page` | `list` | Url whe this comment was left. |
| `children` | `list` | List of json formated exist comments wich bound to this record. |
| `mailbox_address` | `list` | Mailbox address of user that left this comment. |
| `username` | `list` | Ssername of user that left this comment. |

#### New comment (Some connected user add a new comment)
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `record_id` | `list` | Internal id of record, use while addind a new comments as an answer. |
| `user_id` | `list` | Internal id of user that left this comment. |
| `parent_id` | `list` |  Internal id of the record to which this record is bound. |
| `text` | `list` | Record text. |
| `home_page` | `list` | Url whe this comment was left. |
| `children` | `list` | List of json formated exist comments wich bound to this record. |
| `mailbox_address` | `list` | Mailbox address of user that left this comment. |
| `username` | `list` | Ssername of user that left this comment. |

#### User CAPTCHA
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `image` | `string` | CAPTCHA image in base64 encoding. |


#### An error occurred
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `error` | `string` | Text of an error. |

### Outgoing messages
#### Create a new comment
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `text` | `string` | **Required** Text of a new comment. |
| `captcha` | `string` |**Required** Last CAPTCHA text. |
| `parent_id` | `int` / `none` |  Text of an error. |


## Roadmap
- Create microservices for Logger and connet it to all microservices
