#!/usr/bin/env bash
set -e
curl -s -X POST http://localhost:8087/run_cycle | jq .
