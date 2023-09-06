# Overview

Notification using ntfy.sh and MyEmails.

MyEmails utilizes Gmail addresses and shares the same database as Ntfy for user management and access control.

# Ntfy documentation

https://docs.ntfy.sh/config/

# Configuration

	cp .env-example .env

 	cp emails/src/.env-example emails/src/.env

Modify the environment variables as needed, as well as the ports and volumes in docker-compose.yml

# Run

	docker-compose up -d

# Stop

	docker-compose down

# Ports

- 3002 -> 80 for ntfy
- 8000 -> 8000 for myemails

# Easily send notifications (and emails) using script

`notify.sh`

	sudo chmod +x notify.sh

	Usage: ./notify.sh [options]
	
	Options:
	  Required:
	    --message=<message> Message to publish
	
	  Optional:
	    --topic=<topic>     Topic to publish (default: value from .env)
	    --email=<0|1>       Whether to also send an email or not (default: 0)
	    --error=<0|1>       Whether it notifies an error or not (default: 0)

# Change user password if `ntfy user change-pass user_name` fails

Create your hashed password with bcrypt

```python
import bcrypt

bcrypt.hashpw(b"your_password", bcrypt.gensalt()).decode()
```


Set the new password (needs to be cast to bytes for bcrypt to check)

Connect to your SQlite database

	UPDATE user SET pass=CAST(hashed_pass AS BLOB) WHERE user=username;
