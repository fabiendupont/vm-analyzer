# VM Analyzer

This project provides a VM analysis tool that leverages libguestfs inspection
capabilities to read the content of a VM and extract information, such as
installed software, specific configuration files... It also extracts the VM
hardware configuration. The list of files to extract is driven by the
`manifest.json` file.

It is meant to run inside a container. See _Usage_ section.

## VDDK

The VM analysis requires VMware Disk Development Kit (VDDK) to stream the disks
over the network. Due to VDDK license, we cannot ship it, so you have to
download the VDDK tar.gz archive from VMware website and unpack it on the
machine that runs the container, e.g. under /opt.

## Usage

__Note__: all paths are hardcoded, because the container image is meant to be
part of a Kubernetes operator that will instantiate the pod with the files
mounted in the expected path.

To analyze a VM, you will need to provide some information in JSON input file.
The following example is all you need for VMware environments.

```json
{
  "vm_uuid": "01234567-89ab-cdef-0123-456789abcdef",
  "authentication": {
    "hostname": "esxi42.example.com",
    "username": "root",
    "password": "secret",
    "fingerprint": "01:23:45:67:89:AB:CD:EF:01:23:45:67:89:AB:CD:EF:01:23:45:56",
    "insecure": true
  }
}
```

__`vm_uuid`__ is the UUID of the VM. You will find it as `vm.config.uuid`.

The __`authentication`__ is the VMware vSphere API endpoint config. We
recommend connecting directly to ESXi host to benefit from the best
performance.

When you have the file ready, say `/tmp/my_vm.json`, we can start the
container. In the example, we use podman that allows you to run it as a
rootless container. The following command will run the analysis and dump
the result on the standard output.

```
$ podman run \
    -v /tmp/input.json:/data/input.json:Z \
    -v /opt/vmware-vix-disklib-distrib:/opt/vmware-vix-disklib-distrib\
    fdupont-redhat/vm-analyzer:latest
```
