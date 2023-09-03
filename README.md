# Overview

Notification using ntfy.sh and MyEmails.

MyEmails utilizes Gmail addresses and shares the same database as Ntfy for user management and access control.

# Run

	docker-compose up -d

# Stop

	docker-compose down

# Ports

- 3002 -> 80 for ntfy
- 8000 -> 8000 for myemails
