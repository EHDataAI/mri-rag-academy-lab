"""Regression tests for local-only Ollama HTTP transport."""

from __future__ import annotations

import json

import pytest

from mri_rag import answer


class _FakeResponse:
    def __init__(self, status=200, body=b"{}"):
        self.status = status
        self.body = body

    def read(self, size):
        return self.body[:size]


class _FakeConnection:
    response = _FakeResponse()
    calls = []

    def __init__(self, host, port, timeout):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.closed = False
        self.__class__.calls.append(self)

    def request(self, method, path, body, headers):
        self.method = method
        self.path = path
        self.body = body
        self.headers = headers

    def getresponse(self):
        return self.response

    def close(self):
        self.closed = True


def test_loopback_post_uses_fixed_endpoint(monkeypatch):
    fake = _FakeConnection
    fake.calls = []
    fake.response = _FakeResponse(200, json.dumps({"response": "[S1] OK"}).encode())
    monkeypatch.setattr(answer, "HTTPConnection", fake)
    result = answer._request_local_ollama("http://localhost:11434", b"{}")
    conn = fake.calls[0]
    assert result == {"response": "[S1] OK"}
    assert (conn.host, conn.port, conn.timeout) == ("127.0.0.1", 11434, 45)
    assert (conn.method, conn.path) == ("POST", "/api/generate")
    assert conn.closed


@pytest.mark.parametrize("status", [301, 302, 307, 308, 403, 500])
def test_redirects_and_http_errors_do_not_follow(monkeypatch, status):
    fake = _FakeConnection
    fake.calls = []
    fake.response = _FakeResponse(status, b"{}")
    monkeypatch.setattr(answer, "HTTPConnection", fake)
    with pytest.raises(ValueError, match="HTTP inesperada"):
        answer._request_local_ollama("http://127.0.0.1:11434", b"{}")
    assert len(fake.calls) == 1
    assert fake.calls[0].closed


def test_oversized_response_refused(monkeypatch):
    fake = _FakeConnection
    fake.calls = []
    fake.response = _FakeResponse(200, b"x" * (512 * 1024 + 1))
    monkeypatch.setattr(answer, "HTTPConnection", fake)
    with pytest.raises(ValueError, match="demasiado grande"):
        answer._request_local_ollama("http://127.0.0.1:11434", b"{}")
    assert fake.calls[0].closed
