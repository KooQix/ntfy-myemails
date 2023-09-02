#! /bin/bash


# DEFAULT ARGS
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
env_dir="$DIR/.env"

# Check if .env file exists (can be specified as parameter)
if [ ! -f "$env_dir" ]
then
	echo "Error: .env file not found"
	exit 1
fi


# If one argument and is --help, print help
if [ $# -eq 1 ] && [ "$1" == "--help" ]
then
	echo "Usage: ./publish.sh [options]"
	echo
	echo "Options:"
	echo "  Required:"
	echo "    --message=<message> Message to publish"
	echo
	echo "  Optional:"
	echo "    --topic=<topic>     Topic to publish (default: value from .env)"
	echo "    --email=<0|1>       Whether to also send an email or not (default: 0)"
	echo "    --error=<0|1>       Whether it notifies an error or not (default: 0)"
	exit 0
fi


# Get value number n from .env and return it
get_env_value() {
	# Get value from .env
	value=$(grep -v '^#' $env_dir | xargs | awk -F'[ ]' '{print $'$1'}' | awk -F '=' '{print $2}')

	# If value is empty, return error message
	if [ -z "$value" ]
	then
		echo "Error: $2 not set"
		exit 1
	fi

	echo $value
}


# Get params and associated values, such as parameter: --param=value
for ARGUMENT in "$@"
do
	# Argument must start with --
		if [[ $ARGUMENT != --* ]]
	then
		continue
	fi

	KEY=$(echo $ARGUMENT | cut -f1 -d=)

	KEY_LENGTH=${#KEY}

	# Remove -- from key
	KEY=${KEY:2}

	# Set value
	VALUE="${ARGUMENT:$KEY_LENGTH+1}"

	export "$KEY"="$VALUE"
done


#################### Verify arguments ####################


# If $message not set, return error message
if [ -z "$message" ]
then
	echo "Error: --message not set"
	exit 1
fi

# Get values from .env

user=$(get_env_value 1)
password=$(get_env_value 2)
ntfy_url=$(get_env_value 3)
email_url=$(get_env_value 4)


# If topic not set, use default
if [ -z "$topic" ]
then
	topic=$(get_env_value 5)
fi

# If email not set, use default
if [ -z "$email" ]
then
	email=0
fi

# If error not set, use default
if [ -z "$error" ]
then
	error=0
fi

# Set priority. Default is default, if error, set to urgent
priority="default"

# If error, set priority to urgent
if [ $error -eq 1 ]
then
	priority="urgent"
fi



#################### Send notification ####################


# Publish command like: curl -u kooqix:mypass -d "Look ma, with auth" https://example.com/MyTopic
curl -u $user:$password -H "Priority: $priority" -d "$message" $ntfy_url/$topic


#################### Send email ####################

# No email: stop here
if [ $email -eq 0 ]
then
	exit 0
fi

# Send email (General type: see emails types), sends to default receiver (receivers not specified)

# If priority is default, send to general

# Default values for default priority
gen_default_content() {
	cat << EOF
{
	"subject":"[$topic]",
	"body":"$message"
}
EOF
}

gen_error_content() {
	cat << EOF
{
	"subject":"[$topic ERROR]",
	"error_message":"$message"
}
EOF
}

email_content=$(gen_default_content)
email_full_url=$email_url/general

if [ $priority == "urgent" ]
then
	email_full_url=$email_url/error
	email_content=$(gen_error_content)
fi

curl -H "Content-Type: application/json" -H "X-USER: $user" -H "X-PASS: $password" -H "X-TOPIC: $topic" -X POST  -d "$email_content" $email_full_url
