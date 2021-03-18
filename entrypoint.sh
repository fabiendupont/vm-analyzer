#!/bin/sh -e

# This is documented here:
# https://docs.openshift.com/container-platform/3.11/creating_images/guidelines.html#openshift-specific-guidelines
if ! whoami &>/dev/null; then
  if [ -w /etc/passwd ]; then
    echo "${USER_NAME:-vm-analyzer}:x:$(id -u):$(id -g):${USER_NAME:-vm-analyzer} user:${HOME}:/sbin/nologin" >> /etc/passwd
  fi
fi
#####

#set -x +e
#VDDK="/opt/vmware-vix-disklib-distrib/"
#ls -l "/usr/lib64/nbdkit/plugins/nbdkit-vddk-plugin.so"
#ls -ld "$VDDK"
## Use find to detect misplaced library. This does not allow for arbitrary
## location, the path is hard-coded in wrapper.
#lib="$(find "$VDDK" -name libvixDiskLib.so.6)"
#LD_LIBRARY_PATH="$(dirname "$lib")" nbdkit --dump-plugin vddk
#LIBGUESTFS_BACKEND='direct' libguestfs-test-tool
#set +x -e
#
#echo
#echo "...  OK  ..."
#echo

#exec  nbdkit -U - memory 1G --readonly --exit-with-parent --newstyle --run 'python3 /usr/local/bin/break "$unixsocket"'
#exec /usr/local/bin/vm-analyzer
ulimit -c unlimited
echo '/var/tmp/core.%p' > /proc/sys/kernel/core_pattern
exec /usr/local/bin/break