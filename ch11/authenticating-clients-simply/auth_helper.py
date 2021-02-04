#!/usr/bin/env python
import hmac
import os


def client_authenticate(conn, secret_key):
    message = conn.recv(32)
    hash = hmac.new(secret_key, message, digestmod="md5")
    digest = hash.digest()
    conn.send(digest)


def server_authenticate(conn, secret_key):
    message = os.urandom(32)
    conn.send(message)
    hash = hmac.new(secret_key, message, digestmod="md5")
    digest = hash.digest()
    resp = conn.recv(len(digest))
    return hmac.compare_digest(digest, resp)
