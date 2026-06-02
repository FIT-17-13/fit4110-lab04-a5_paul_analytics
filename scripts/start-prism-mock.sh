#!/usr/bin/env bash
set -euo pipefail

node ./node_modules/@stoplight/prism-cli/dist/index.js mock contracts/team-analytics.openapi.yaml --host 0.0.0.0 --port 4010
