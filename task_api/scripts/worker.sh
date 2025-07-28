if [ -z "$1" ]; then
  ARG=1
else
  ARG=$1
fi

taskiq worker app.broker:broker --workers "$ARG" --no-configure-logging --fs-discover