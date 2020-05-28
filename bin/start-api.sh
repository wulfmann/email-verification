#!/bin/bash
cd /app/infrastructure
ls
poetry install
cdk synth

sam local start-api -t cdk.out/${STACK_NAME}.template.json --env-vars /app/dev-environment.json
