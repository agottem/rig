# High level agent instruction

## Dev environment overview
- This dev environment is running in a sandbox VM that'll be thrown away when work is complete
- This dev environment can be uniquely identified by the name specified by the environment variable
  "VM_NAME"
- Agents have sudo permissions should they need to make changes to the VM but be sure to document
  any changes made
- The git repo to work on is specified in the environment variable "REPO"
- Always check the root directory of the REPO git repository for an AGENTS.md and process it if
  found
- Any completed work that should persist outside of this VM should be written to the directory
  specified by the environment variable "ARTIFACTS_DIR"
- Work written to the ARTIFACTS_DIR should not include build artifacts or other temporary files
- Work written to the ARTIFACTS_DIR should have a short descriptive name along with a date-time
  suffix
- When changes are made to the repo and work is complete, use "git format-patch" to produce a patch
  file and store it in the ARTIFACTS_DIR
- Any new or modified code should retain the formatting and styling of the existing code base,
  matching naming case convention and style, alignment and overall arrangement of the code.
