FROM python:3.9.1-slim

# Create a group and user to run our app
ARG APP_USER=anychat
RUN groupadd -r ${APP_USER} && useradd --no-log-init -r -m -g ${APP_USER} ${APP_USER}

# Install packages needed to run your application (not build deps):
#   libpcre2 -- This is a library of functions to support regular expressions whose syntax and semantics are as close as possible to those of the Perl 5 language.
#   mime-support -- for mime types when serving static files
#   libmagic1 -- required by python-magic for mime detection
#   default-libmysqlclient-dev -- for mysql database support
#   inkscape -- for exporting vector graphics like pdf, eps, ps
#   libcurl4-nss-dev libssl-dev -- for pycurl installation (used by celery[sqs])
# We need to recreate the /usr/share/man/man{1..8} directories first because
# they were clobbered by a parent image.
RUN set -ex \
    && RUN_DEPS=" \
#    libpcre3 \
#    mime-support \
#    libmagic1 \
    default-libmysqlclient-dev \
#    inkscape \
#    libcurl4-nss-dev libssl-dev \
    " \
    && seq 1 8 | xargs -I{} mkdir -p /usr/share/man/man{} \
    && apt-get update && apt-get install -y --no-install-recommends $RUN_DEPS \
#    && pip install pipenv \
    && rm -rf /var/lib/apt/lists/*
#    && mkdir -p /home/${APP_USER}/.config/inkscape \
#    && chown -R ${APP_USER} /home/${APP_USER}/.config/inkscape \
    # Create directories
#    && mkdir -p /static_cdn/static_root/ \
#    && chown -R ${APP_USER} /static_cdn/

# Copy in your requirements file
#ADD requirements.txt /requirements.txt
# RUN mkdir /app/ \
# && mkdir /app/config/ \
# && mkdir /app/scripts/ \
# && mkdir /app/static_cdn/ \
# && chown -R ${APP_USER} /app/static_cdn/

WORKDIR /code/

#COPY Pipfile Pipfile.lock /app/

# OR, if you're using a directory for your requirements, copy everything (comment out the above and uncomment this if so):
COPY requirements.txt ./requirements.txt

# Install build deps, then run `pip install`, then remove unneeded build deps all in a single step.
# Correct the path to your production requirements file, if needed.


#RUN set -ex \
#    && apt-get update && apt-get install -y
#ENV PYCURL_SSL_LIBRARY=nss

RUN set -ex \
    && BUILD_DEPS=" \
    build-essential \
#    libpcre3-dev \
#    libpq-dev \
    " \
    && apt-get update && apt-get install -y --no-install-recommends $BUILD_DEPS \
    && pip install -r ./requirements.txt \
#    && export PYCURL_SSL_LIBRARY=nss \
#    && pipenv install --deploy --system \
    \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false $BUILD_DEPS \
    && rm -rf /var/lib/apt/lists/*
#    &&

# Install required graphic tools
#RUN set -ex \
#    && apt-get install -y inkscape

# Copy your application app to the container (make sure you create a .dockerignore file if any large files or directories should be excluded)
COPY scripts/ ./scripts/
COPY configs/ ./configs/
COPY library_data ./library_data
COPY static_my_project/ ./static_my_project

WORKDIR app
COPY ./src ./

# uWSGI will listen on this port
EXPOSE 8000

## Add any static environment variables needed by Django or your settings file here:
#ENV DJANGO_SETTINGS_MODULE=my_project.settings.deploy
#
## Call collectstatic (customize the following line with the minimal environment variables needed for manage.py to run):
#RUN DATABASE_URL='' python manage.py collectstatic --noinput
#
## Tell uWSGI where to find your wsgi file (change this):
ENV UWSGI_WSGI_FILE=qcg/wsgi.py

# Base uWSGI configuration (you shouldn't need to change these):
ENV UWSGI_HTTP=:8000 UWSGI_MASTER=1 UWSGI_HTTP_AUTO_CHUNKED=1 UWSGI_HTTP_KEEPALIVE=1 UWSGI_LAZY_APPS=1 UWSGI_WSGI_ENV_BEHAVIOR=holy

# Number of uWSGI workers and threads per worker (customize as needed):
ENV UWSGI_WORKERS=2 UWSGI_THREADS=4

# uWSGI static file serving configuration (customize or comment out if not needed):
ENV UWSGI_STATIC_MAP="/static/=/static_cdn/static_root/" UWSGI_STATIC_EXPIRES_URI="/static/.*\.[a-f0-9]{12,}\.(css|js|png|jpg|jpeg|gif|ico|woff|ttf|otf|svg|scss|map|txt) 315360000"

# Deny invalid hosts before they get to Django (uncomment and change to your hostname(s)):
# ENV UWSGI_ROUTE_HOST="^(?!localhost:8000$) break:400"

# Change to a non-root user
#USER ${APP_USER}:${APP_USER}

# Uncomment after creating your docker-entrypoint.sh
ENTRYPOINT ["/code/scripts/docker/entrypoint.sh"]

# Start uWSGI
#CMD ["uwsgi", "--show-config"]
