#!/usr/bin/env bash
cd "$(dirname "$0")"

docker build -t test_app:latest .

docker run test_app:latest
