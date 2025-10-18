#!/usr/bin/env bash
cd "$(dirname "$0")"

docker build -t webserver:latest .

docker run -p 8000:8000 webserver:latest

