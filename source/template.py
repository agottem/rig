import subprocess

import util


def create_profile (name, lim_mem, lim_cpu, parent_nic):
    util.run_acp_safe(["incus", "profile", "create", name], check=True)

    try:
        util.run_acp_safe(["incus", "profile", "set", name, "limits.memory", lim_mem], check=True)
        util.run_acp_safe(["incus", "profile", "set", name, "limits.cpu", lim_cpu], check=True)
        util.run_acp_safe(["incus", "profile", "device", "add", name, "root", "disk", "pool=default", "path=/"], check=True)
        util.run_acp_safe(["incus", "profile", "device", "add", name, "eth0", "nic", "nictype=bridged", f"parent={parent_nic}", "name=eth0"], check=True)

    except Exception as e:
        util.print_acp_safe(f"Failed to create profile {name} due to the error: {e}")
        util.run_acp_safe(["incus", "profile", "delete", name])
        raise

def create_image (profile, template, vm_image, resource_dir):
    vm_name = "rig-tmp-img-create"

    util.run_acp_safe(["incus", "init", vm_image, vm_name, "--vm", "-p", profile], check=True)

    try:
        with open(f"{resource_dir}/cloud_init.yaml", "r") as f:
            util.run_acp_safe(["incus", "config", "set", vm_name, "cloud-init.user-data", "-"], stdin=f, text=True, check=True)

        util.run_acp_safe(["incus", "config", "device", "add", vm_name, "resource-dir", "disk",
                           f"source={resource_dir}", "path=/mnt/resource", "readonly=true"],
                          check=True)

        util.run_acp_safe(["incus", "start", vm_name], check=True)

        util.wait_vm_ready(vm_name)

        util.run_acp_safe(["incus", "exec", vm_name, "--",
                           "/mnt/resource/vm_init.sh"],
                          check=True)
        util.run_acp_safe(["incus", "exec", vm_name, "--",
                           "cloud-init", "status", "--wait"],
                          check=True)
        util.run_acp_safe(["incus", "exec", vm_name, "--",
                           "/mnt/resource/root_init.sh"],
                          check=True)
        util.run_acp_safe(["incus", "exec", vm_name, "--",
                           "/mnt/resource/vm_finalize.sh"],
                          check=True)

        util.run_acp_safe(["incus", "stop", vm_name], check=True)
        util.run_acp_safe(["incus", "publish", vm_name, "--alias", template, "--compression", "zstd"], check=True)

    except Exception as e:
        util.print_acp_safe(f"Failed to setup VM image for template {template}, error: {e}")
        raise
    finally:
        util.run_acp_safe(["incus", "delete", "-f", vm_name], check=True)

def delete_profile (name):
    util.run_acp_safe(["incus", "profile", "delete", name])

def delete_image (name):
    util.run_acp_safe(["incus", "image", "delete", name])

def build_std_templs (lim_mem, lim_cpu, parent_nic, vm_image, resource_dir):
    create_profile("rig-std", lim_mem, lim_cpu, parent_nic)

    try:
        create_image("rig-std", "rig-std", vm_image, resource_dir)
    except Exception as e:
        delete_profile("rig-std")
        raise

def delete_std_templs ():
    delete_image("rig-std")
    delete_profile("rig-std")
