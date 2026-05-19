# High level agent instruction

## Dev environment overview
- This dev environment is running in a sandbox VM that'll be thrown away when work is complete
- This dev environment can be uniquely identified by the name specified by the environment variable
  "VM_NAME"
- Request installation of any packages that are required but missing
- The git repo to work on is specified in the environment variable "REPO"
- Always check the root directory of the REPO git repository for an AGENTS.md and process it if
  found
- Any completed work that should persist outside of this VM should be written to the directory
  specified by the environment variable "ARTIFACTS_DIR"
