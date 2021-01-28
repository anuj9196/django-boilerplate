#!/bin/sh
#set -e

# Run the command and exit with the custom message when the comamnd fails to run
safeRunCommand() {
  cmnd="$*"
  echo cmnd="$cmnd"
  eval "$cmnd"
  ret_code=$?
  if [ $ret_code != 0 ]; then
    printf "Error : [code: %d] when executing command: '$cmnd'\n" $ret_code
    exit $ret_code
  else
    echo "Command run successfully: $cmnd"
  fi
}

runDjangoTest() {
  echo "Running test"
  safeRunCommand "ls -la"
  safeRunCommand "python manage.py test"
  echo "Done: Running test"
}

runDjangoCollectStatic() {
  echo "Collecting static files"
  cmnd="python manage.py collectstatic --noinput"
  safeRunCommand "$cmnd"
  echo "Done: Collecting static files"
}

runDjangoMigrate() {
  echo "Migrating database"
  safeRunCommand "python manage.py migrate --noinput"
  echo "Done: Migrating database"
}

runDjangoCheckDeploy() {
  echo "Checking Django deployment"
  safeRunCommand "python manage.py check --deploy"
  echo "Done: Checking Django deployment"
}

# If Deployment mode is set to production
# Run all tests, collect static, and migrate
if [ "x$DEPLOYMENT_MODE" = 'xproduction' ]; then
  echo "Running in production mode..."
  runDjangoCheckDeploy
  runDjangoTest
  runDjangoCollectStatic
  runDjangoMigrate
fi


# Run Django test.
# The test is run only when environment variable `DJANGO_RUN_TEST` is set to `on`.
if [ "x$DJANGO_RUN_TEXT" = 'xon' ] && [ ! "x$DEPLOYMENT_MODE" = 'xproduction' ]; then
  runDjangoTest
fi


# Run Django collectstatic.
# The command is run only when environment variable `DJANGO_MANAGE_COLLECTSTATIC` is se to `on`.
if [ "x$DJANGO_MANAGE_COLLECTSTATIC" = 'xon' ] && [ ! "x$DEPLOYMENT_MODE" = 'xproduction' ]; then
  runDjangoCollectStatic
fi


# Run Django migrate command.
# The command is run only when environment variable `DJANGO_MANAGE_MIGRATE` is set to `on`.
if [ "x$DJANGO_MANAGE_MIGRATE" = 'xon' ] && [ ! "x$DEPLOYMENT_MODE" = 'xproduction' ]; then
  runDjangoMigrate
fi

#
# Why not running Django runserver?
# Runserver is not required everytime when the container is running.
# May be user wants to login to the `manage.py shell` only and does not want to run the server.
# Excluding runserver from entrypoint prevents running the server everytime any bash script is run.
# In order to invoke runserver, the command can be passed with docker run command.
#

# Accept other commands
exec "$@"