# Copyright (C) 2010-2015 Cuckoo Foundation, Optiv, Inc. (brad.spengler@optiv.com)
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

import os
import shutil
from subprocess import call
from lib.common.abstracts import Package

class IcedID(Package):
    """IcedID analysis package."""

    def __init__(self, options={}, config=None):
        """@param options: options dict."""
        self.config = config
        self.options = options
        self.pids = []
        self.options["dll"] = "IcedID.dll"
        self.options["loader"] = "newloader.exe"
        self.options["loader_64"] = "newloader_x64.exe"
        self.options["dump-on-api"] = "RtlDecompressBuffer"

    def start(self, path):
        args = self.options.get("arguments")
        appdata = self.options.get("appdata")
        runasx86 = self.options.get("runasx86")

        # If the file doesn't have an extension, add .exe
        # See CWinApp::SetCurrentHandles(), it will throw
        # an exception that will crash the app if it does
        # not find an extension on the main exe's filename
        if "." not in os.path.basename(path):
            new_path = path + ".exe"
            os.rename(path, new_path)
            path = new_path

        if appdata:
            # run the executable from the APPDATA directory, required for some malware
            basepath = os.getenv('APPDATA')
            newpath = os.path.join(basepath, os.path.basename(path))
            shutil.copy(path, newpath)
            path = newpath
        return self.execute(path, args, path)
