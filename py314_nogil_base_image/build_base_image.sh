#!/usr/bin/env bash
cd "$(dirname "$0")"

docker build -t py314_nogil:latest .
