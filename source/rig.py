#!/usr/bin/env python3

import os
import datetime
import argparse
import pathlib
import tempfile

import template
import exec


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="rig",
                                     description="Rig together safe environments for agent software")
    sub = parser.add_subparsers(dest="action", required=True, help="Action to perform")

    subp = sub.add_parser("setup-templates")
    subp.add_argument("--lim-mem",    type=str, default="8GiB")
    subp.add_argument("--lim-cpu",    type=str, default="1")
    subp.add_argument("--parent-nic", type=str, required=True)
    subp.add_argument("--vm-image",   type=str, default="images:debian/12/cloud")

    subp = sub.add_parser("delete-templates")

    subp = sub.add_parser("run")
    subp.add_argument("--profile",           type=str,  default="rig-std")
    subp.add_argument("--template",          type=str,  default="rig-std")
    subp.add_argument("--name",              type=str,  required=True)
    subp.add_argument("--agent-type",        type=str,  required=True)
    subp.add_argument("--artifact-root",     type=str,  default=os.getenv("RIG_ARTIFACTS_DIR"))
    subp.add_argument("--repo",              type=str,  required=True)
    subp.add_argument("--auth-cfg-dir",      type=str,  default=os.getenv("RIG_AUTH_CFG_DIR"))
    subp.add_argument("--openai-api-key",    type=str,  default=os.getenv("OPENAI_API_KEY"))
    subp.add_argument("--anthropic-api-key", type=str,  default=os.getenv("ANTHROPIC_API_KEY"))
    subp.add_argument("--b64-cmd",           type=str)
    subp.add_argument("--keep-vm",           type=bool, default=False)

    subp = sub.add_parser("pull")
    subp.add_argument("--name",          type=str,  required=True)
    subp.add_argument("--artifact-root", type=str,  default=os.getenv("RIG_ARTIFACT_ROOT"))

    resource_dir = f"{pathlib.Path(__file__).resolve().parent.parent}/resource"

    args = parser.parse_args()
    match args.action:
        case "setup-templates":
            template.build_std_templs(args.lim_mem,
                                      args.lim_cpu,
                                      args.parent_nic,
                                      args.vm_image,
                                      resource_dir)

        case "delete-templates":
            template.delete_std_templs()

        case "run":
            staging_dir = pathlib.Path(tempfile.mkdtemp())
            timestamp   = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            exec.run_vm(args.profile,
                        args.template,
                        f"rig-{args.name}-{timestamp}",
                        args.agent_type,
                        resource_dir,
                        str(staging_dir),
                        args.artifact_root,
                        args.repo,
                        args.auth_cfg_dir,
                        args.openai_api_key,
                        args.anthropic_api_key,
                        args.b64_cmd,
                        keep_vm=args.keep_vm)

        case "pull":
            exec.pull_artifacts(args.name, args.artifact_root)
