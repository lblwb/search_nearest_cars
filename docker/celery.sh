#!/bin/bash

if [[ "${1}" == "celery" ]]; then
    celery --app=app.tasks.celery_conf:celery_app worker -l INFO
elif [[ "${1}" == "flower" ]]; then
    celery --app=app.tasks.celery_conf:celery_app flower
elif [[ "${1}" == "beat" ]]; then
    celery --app=app.tasks.celery_conf:celery_app beat -l INFO
fi
