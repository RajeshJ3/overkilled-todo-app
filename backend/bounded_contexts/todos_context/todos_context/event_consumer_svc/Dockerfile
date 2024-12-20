FROM python:3.13.1

ENV WORKDIR=/app
ENV BOUNDED_CONTEXT_NAME=todos_context
ENV SERVICE_NAME=event_consumer_svc

# build contexts
ENV BUILD_LIB_CONTEXT=libs
ENV BUILD_BC_CONTEXT=bounded_contexts
ENV BUILD_BC_PATH=$BUILD_BC_CONTEXT/$BOUNDED_CONTEXT_NAME
ENV BUILD_SERVICE_CONTEXT=$BUILD_BC_PATH/$BOUNDED_CONTEXT_NAME

# container contexts
ENV LIB_CONTEXT=$WORKDIR/libs
ENV BC_CONTEXT=$WORKDIR/bounded_contexts
ENV BC_PATH=$BC_CONTEXT/$BOUNDED_CONTEXT_NAME
ENV SERVICE_CONTEXT=$BC_PATH/$BOUNDED_CONTEXT_NAME

# installing poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python3 - --preview

# context files
COPY $BUILD_BC_PATH/poetry.lock                                     $BC_PATH/poetry.lock
COPY $BUILD_BC_PATH/pyproject.toml                                  $BC_PATH/pyproject.toml

# service files
COPY $BUILD_SERVICE_CONTEXT/__init__.py                             $SERVICE_CONTEXT/__init__.py
COPY $BUILD_SERVICE_CONTEXT/alembic.ini                             $SERVICE_CONTEXT/alembic.ini
COPY $BUILD_SERVICE_CONTEXT/config.py                               $SERVICE_CONTEXT/config.py
COPY $BUILD_SERVICE_CONTEXT/alembic                                 $SERVICE_CONTEXT/alembic
COPY $BUILD_SERVICE_CONTEXT/db                                      $SERVICE_CONTEXT/db
COPY $BUILD_SERVICE_CONTEXT/utils                                   $SERVICE_CONTEXT/utils
COPY $BUILD_SERVICE_CONTEXT/$SERVICE_NAME                           $SERVICE_CONTEXT/$SERVICE_NAME

# libs
COPY $BUILD_LIB_CONTEXT/common_lib                                  $LIB_CONTEXT/common_lib
COPY $BUILD_LIB_CONTEXT/events_framework                            $LIB_CONTEXT/events_framework

# installing dependencies
RUN cd $BC_PATH && /etc/poetry/bin/poetry install

# runing the service
CMD cd $BC_PATH && /etc/poetry/bin/poetry run python $BOUNDED_CONTEXT_NAME/$SERVICE_NAME/main.py
