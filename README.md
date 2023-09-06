# Overview

Notification using ntfy.sh and MyEmails

# Run

	docker-compose up -d

# Stop

	docker-compose down

# Ports

- 3002 -> 80 for ntfy
- 8000 -> 8000 for myemails

# Change user password if `ntfy user change-pass user_name` fails

Create your hashed password with bcrypt

```python
import bcrypt

bcrypt.hashpw(b"your_password", bcrypt.gensalt())
```


Set the new password (needs to be cast to bytes for bcrypt to check)

1 - Connect to your SQlite database
2 - UPDATE user SET pass=CAST(hashed_pass AS BLOB) WHERE user=username;
