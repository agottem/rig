import sys
import subprocess

import util


def pull_artifacts (vm_name, artifact_root):
    util.print_acp_safe(f"Pulling artifacts from {vm_name} to {artifact_root} ...", end="")

    try:
        util.run_acp_safe(["mkdir", "-p", artifact_root], check=True)
        util.run_acp_safe(["incus", "file", "pull", "-r", f"{vm_name}/artifacts/{vm_name}", artifact_root], check=True)
        util.print_acp_safe("Done")

    except Exception as e:
        util.print_acp_safe("Failed: {e}")
        raise

def run_vm (profile,
            template,
            vm_name,
            agent_type,
            resource_dir,
            staging_dir,
            artifact_root,
            git_repo,
            auth_cfg_dir,
            openai_api_key,
            anthropic_api_key,
            b64_cmd,
            **kwargs):
    util.print_acp_safe(f"Rigging new VM:\n"
                        f"\tprofile:           {profile}\n"
                        f"\ttemplate:          {template}\n"
                        f"\tvm-name:           {vm_name}\n"
                        f"\tagent-type:        {agent_type}\n"
                        f"\tresource-dir:      {resource_dir}\n"
                        f"\tstaging-dir:       {staging_dir}\n"
                        f"\tartifact-root:     {artifact_root}\n"
                        f"\tgit-repo:          {git_repo}\n"
                        f"\tauth-cfg-dir:      {auth_cfg_dir}\n"
                        f"\topenai-api-key:    {openai_api_key}\n"
                        f"\tanthropic-api-key: {anthropic_api_key}\n"
                        f"\tb64-cmd:           {b64_cmd}\n")

    try:
        util.run_acp_safe(["mkdir", "-p", staging_dir], check=True)
        util.run_acp_safe(["git", "clone", "--no-local", git_repo, f"{staging_dir}/git"],
                          check=True)

        util.run_acp_safe(["incus", "init", template, vm_name, "--vm", "-p", profile], check=True)
        util.run_acp_safe(["incus", "config", "device", "add", vm_name, "resource-dir", "disk",
                           f"source={resource_dir}", "path=/mnt/resource", "readonly=true"],
                          check=True)
        util.run_acp_safe(["incus", "config", "device", "add", vm_name, "staging-dir", "disk",
                           f"source={staging_dir}", "path=/mnt/staging", "readonly=true"],
                          check=True)

        if auth_cfg_dir:
            util.run_acp_safe(["incus", "config", "device", "add", vm_name, "auth-cfg-dir", "disk",
                               f"source={auth_cfg_dir}", "path=/mnt/auth-cfg", "readonly=true"],
                              check=True)

        util.run_acp_safe(["incus", "start", vm_name], check=True)

        util.wait_vm_ready(vm_name)

        util.run_acp_safe(["incus", "exec", vm_name, "--", "cloud-init", "status", "--wait"], check=True)
        util.run_acp_safe(["incus", "exec", vm_name, "--",
                           "runuser", "-l", "agent", "-c",
                           f"/mnt/resource/user_init.sh --b64-cmd={b64_cmd} --vm-name={vm_name} --agent-type={agent_type} --openai-api-key={openai_api_key} --anthropic-api-key={anthropic_api_key}"],
                          check=True)
        subprocess.run(["incus", "exec", vm_name, "--",
                        "runuser", "-l", "agent", "-c", f"/mnt/resource/user_run.sh"],
                       check=True)

        pull_artifacts(vm_name, artifact_root)

        if "keep_vm" not in kwargs or kwargs.get("keep_vm") == False:
            util.run_acp_safe(["incus", "delete", "-f", vm_name], check=True)
        else:
            util.print_acp_safe(f"VM '{vm_name}' kept running")

    except Exception as e:
        util.print_acp_safe(f"VM '{vm_name}' encounted the error: {e}, instance kept running")
        raise
    finally:
        util.run_acp_safe(["rm", "-rf", staging_dir])
