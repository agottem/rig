# High level agent instruction

## Dev environment overview
- This dev environment is running in a sandbox VM that'll be thrown away when work is complete
- This dev environment can be uniquely identified by the name specified by the environment variable "VM_NAME"
- Request installation of any packages that are required but missing
- The git repo to work on is specified in the environment variable "REPO"
- Any completed work that should persist outside of this VM should be written to the directory specified by the environment variable "ARTIFACTS_DIR"

<!-- Local Variables: -->
<!-- gptel-model: gpt-5.4 -->
<!-- gptel--backend-name: "OpenAI" -->
<!-- gptel--system-message: "You are a large language model living in Emacs and a helpful assistant. Respond concisely." -->
<!-- gptel--tool-names: nil -->
<!-- gptel--bounds: nil -->
<!-- End: -->
