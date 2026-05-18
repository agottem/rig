#!/bin/bash

set -eux

for arg in "$@"; do
    case $arg in
        --b64-cmd=*)
            B64_CMD="${arg#*=}"
            shift
            ;;
        --vm-name=*)
            VM_NAME="${arg#*=}"
            shift
            ;;
        --agent-type=*)
            AGENT_TYPE="${arg#*=}"
            shift
            ;;
        --openai-api-key=*)
            OPENAI_API_KEY="${arg#*=}"
            shift
            ;;
        --anthropic-api-key=*)
            ANTHROPIC_API_KEY="${arg#*=}"
            shift
            ;;
        *)
            echo "Unknown option $arg"
            exit 1
            ;;
    esac
done

# Create OpenAI auth env
echo export OPENAI_API_KEY=$OPENAI_API_KEY >> /home/agent/auth-openai.env

# Create Anthropic auth env
echo export ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY >> /home/agent/auth-anthropic.env

# Create OpenCode auth env
if [[ -e "/mnt/auth-cfg/opencode" ]]; then
    touch /home/agent/auth-opencode.env

    mkdir -p /home/agent/.local/share/opencode
    cp -R /mnt/auth-cfg/opencode /home/agent/.local/share/
else
    echo export OPENAI_API_KEY=$OPENAI_API_KEY       >> /home/agent/auth-opencode.env
    echo export ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY >> /home/agent/auth-opencode.env
fi

echo export VM_NAME=$VM_NAME                     >> /home/agent/agent.env
echo export AGENT_TYPE=$AGENT_TYPE               >> /home/agent/agent.env
echo export REPO=/work/repo                      >> /home/agent/agent.env
echo export ARTIFACTS_DIR=/artifacts/$VM_NAME    >> /home/agent/agent.env

if [[ ! -z "$B64_CMD" ]]; then
    echo $B64_CMD | base64 -d > /work/cmd.sh
else
    echo "echo No command provided" > /work/cmd.sh
fi

chmod +x /work/cmd.sh

git clone --no-local /mnt/staging/git /work/repo

cp /mnt/resource/AGENTS.md /work

mkdir /artifacts/$VM_NAME
