#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset


celery -A rental.taskapp beat -l INFO
