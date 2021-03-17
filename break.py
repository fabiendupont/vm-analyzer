 
 #!/usr/bin/env python3

import datetime
import guestfs
import json
import logging
import os
import re
import signal
import subprocess
import ssl
import sys
import time
import uuid

from pyVmomi import vim
from pyVim.connect import SmartStubAdapter, VimSessionOrientedStub, Disconnect
from pyVim.task import WaitForTask

from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse


class VmAnalyzer:
    def __init__(self, request):
        self._request = request
        self._service_instance = self._connect()
        self._vm = self._find_vm_by_id(self._request["vm_uuid"])

        now = datetime.datetime.now()
        self._snapshot_name = "%s-vm-analysis" % now.strftime("%Y%m%d%H%M%S")
        self._snapshot_desc = "%s - VM Analysis" % now.strftime("%Y-%m-%d %H:%M:%S")
        self._snapshot = None

        if not os.path.exists("/tmp/%s" % self._request["vm_uuid"]):
            os.mkdir("/tmp/%s" % self._request["vm_uuid"])


    def __del__(self):
        self._remove_snapshot()
        self._disconnect()


    def _connect(self):
        # https://github.com/vmware/pyvmomi/issues/347#issuecomment-297591340
        print("Connecting to %s as %s" % (self._request["authentication"]["hostname"], self._request["authentication"]["username"]))
        smart_stub = SmartStubAdapter(
            host = self._request["authentication"]["hostname"],
            port = 443,
            sslContext = ssl._create_unverified_context(),
            connectionPoolTimeout = 0
        )
        session_stub = VimSessionOrientedStub(
            smart_stub,
            VimSessionOrientedStub.makeUserLoginMethod(
                self._request["authentication"]["username"],
                self._request["authentication"]["password"]
            )
        )
        si = vim.ServiceInstance('ServiceInstance', session_stub)

        if not si:
            raise Exception("Could not connect to %s" % self._request["authentication"]["hostname"])

        return si


    def _disconnect(self):
        try:
            Disconnect(self._service_instance)
        except:
            pass


    def _find_vm_by_id(self, vm_id):
        print("Looking for virtual machine with UUID '%s'" % vm_id)
        # TODO: understand why FindByUuid fails
        # search_index = self._service_instance.content.searchIndex
        # vm = search_index.FindByUuid(None, vm_id, True, True)
        view_manager = self._service_instance.content.viewManager
        container = view_manager.CreateContainerView(self._service_instance.content.rootFolder, [vim.VirtualMachine], True)
        for c in container.view:
            if c.config.uuid == vm_id:
                vm = c
        if vm is None:
            raise Exception("No virtual machine with UUID '%s'" % vm_id)
        return vm


    def _create_snapshot(self):
        print("Creating snapshot to protect the VM disks")
        task = self._vm.CreateSnapshot(name = self._snapshot_name,
                                 description = self._snapshot_desc,
                                 memory = False,
                                 # The `quiesce` parameter can be False to
                                 # make it slightly faster, but it should
                                 # be first tested independently.
                                 quiesce = True)
        WaitForTask(task)
        # Update the VM data
        self._vm.Reload()
        self._snapshot = self._vm.snapshot.currentSnapshot


    def _remove_snapshot(self):
        print("Removing snapshot")
        if self._snapshot:
            WaitForTask(self._snapshot.RemoveSnapshot_Task(False))


    def _path_win2lin(self, path):
        if not re.compile('^/').match(path):
            path = re.sub('^.*/', '/', path)
        return path


    def _get_vm_hardware(self):
        host = self._vm.runtime.host

        hardware = {
            "metadata": {
                "vmware_moref": self._vm._moId
            },
            "disks": [],
        }

        for device in self._vm.config.hardware.device:
            if type(device).__name__ == 'vim.vm.device.VirtualDisk':
                datastore = device.backing.datastore
                path = device.backing.fileName.replace("[%s] " % datastore.name, "")
                hardware["disks"].append({
                    "id": device.backing.uuid,
                    "key": device.key,
                    "path": path,
                    "size": device.capacityInBytes,
                    "storage_name": datastore.name,
                    "storage_path": datastore.summary.url.replace("ds://", ""),
                    "is_sparse": device.backing.thinProvisioned,
                    "is_rdm": type(device.backing).__name__ == 'vim.vm.device.VirtualDisk.VirtualDiskRawDiskMappingVer1BackingInfo'
                })

        return hardware

    def _get_vm_software(self, vm_hardware):
        self._create_snapshot()
        print("Snapshot MORef: %s" % self._snapshot._moId)

        sockets_paths = []
        for disk in vm_hardware["disks"]:
            socket_path = "/tmp/%s/%s.sock" % (self._request["vm_uuid"], disk["id"])
            # Allowing some time for the socket to be created
            for i in range(10):
                if os.path.exists(socket_path):
                    break
                time.sleep(1)

            sockets_paths.append(socket_path)

        g = guestfs.GuestFS(python_return_dict=True)
        g.set_backend("direct")
        for socket_path in sockets_paths:
            g.add_drive_opts("", protocol="nbd", format="raw", server=["unix:%s" % socket_path], readonly=1)
        g.launch()

    def get_vm_config(self):
        vm_hardware = self._get_vm_hardware()
        vm_config = {
            "hardware": vm_hardware,
            "software": self._get_vm_software(vm_hardware),
        }
        return vm_config

class Break(Resource):
    def post(self):
        input = request.get_json()
        vm_config = VmAnalyzer(input).get_vm_config()
        return jsonify(vm_config)

def main():     
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(Break, '/break')
    app.run(host= '0.0.0.0')


if __name__ == '__main__':
    main()


 
 
 
 
 
 
 socket_path = however you get the first arg in python
 g = guestfs.GuestFS(python_return_dict=True)
 g.set_backend("direct")
 g.add_drive_opts("", protocol="nbd", format="raw",
                  server=["unix:%s" % socket_path], readonly=1)
 g.launch()
