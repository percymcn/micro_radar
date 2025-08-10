#!/usr/bin/env bash
set -e
curl -s -X POST http://localhost:${PORT_API:-8091}/run_cycle | jq .
