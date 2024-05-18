#!/bin/bash

response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/)

if [ "$response" == "200" ]; then
    exit 0  # Server is healthy
else
    exit 1  # Server is unhealthy
fi
