#!/bin/bash

set -eux

for d in /work /artifacts; do
    mkdir -p $d
    chown -R agent:agent $d
done

# Install OpenAI tooling
npm install -g @openai/codex
npm install -g @zed-industries/codex-acp

# Install Anthropic tooling
sudo -u agent /bin/bash -c 'curl -fsSL https://claude.ai/install.sh | bash'
npm install -g @agentclientprotocol/claude-agent-acp

# Install OpenCode tooling
npm install -g opencode-ai
