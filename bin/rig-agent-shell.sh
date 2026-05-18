#!/bin/bash

set -eu

for arg in "$@"; do
    case $arg in
        --name=*)
            NAME="${arg#*=}"
            shift
            ;;
        --repo=*)
            REPO="${arg#*=}"
            shift
            ;;
        --artifact-root*)
            ARTIFACT_ROOT="${arg#*=}"
            shift
            ;;
        *)
            break
            ;;
     esac
done

CMD=$@

# Rewrite the command if needed
case $CMD in
    "opencode acp")
        AGENT_TYPE=opencode
        ;;
    codex-acp)
        CMD="codex-acp --config sandbox_permissions=danger-full-access --config sandbox_mode=danger-full-access"
        AGENT_TYPE=openai
        ;;
    claude-agent-acp)
        AGENT_TYPE=anthropic
        ;;
    *)
        echo "Agent type could not be determined from the command: $CMD"
        exit 1
        ;;
esac


rig run --name=$NAME --agent-type=$AGENT_TYPE --artifact-root $ARTIFACT_ROOT --repo $REPO --b64-cmd "$(echo $CMD | base64 -w0)"
