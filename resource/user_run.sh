#!/bin/bash

set -eu

source /home/agent/agent.env
source /home/agent/auth-$AGENT_TYPE.env

cd /work
./cmd.sh
