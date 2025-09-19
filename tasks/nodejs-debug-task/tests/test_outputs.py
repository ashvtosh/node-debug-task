# tests/test_outputs.py
import os
import subprocess
import time
import requests
import signal
import sys
import pytest

ROOT = os.path.dirname(os.path.dirname(__file__))
SERVER = os.path.join(ROOT, 'server.js')

def start_server(env=None):
    env = dict(os.environ, **(env or {}))
    proc = subprocess.Popen(
        ['node', SERVER],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=env,
        text=True
    )
    # wait until we see the listening line or process exits
    start = time.time()
    out = ""
    while True:
        if time.time() - start > 5:
            proc.kill()
            raise RuntimeError("Server did not start in time. Output:\n" + out)
        line = proc.stdout.readline()
        if not line:
            time.sleep(0.05)
            continue
        out += line
        if 'listening' in line:
            break
        if proc.poll() is not None:
            raise RuntimeError(f"Server exited early (rc={proc.returncode}). Output:\n{out}")
    return proc, out

def stop_server(proc):
    try:
        proc.terminate()
        proc.wait(timeout=2)
    except Exception:
        proc.kill()

def base_url(port=3000):
    return f'http://127.0.0.1:{port}'

def test_health_endpoint():
    proc, _ = start_server(env={'CONFIG_PATH': os.path.join(ROOT, 'config.json')})
    try:
        r = requests.get(base_url()+"/health", timeout=2)
        assert r.status_code == 200, "expected HTTP 200 from /health"
        assert r.text == "OK", "expected body 'OK' from /health"
    finally:
        stop_server(proc)

def test_greet_with_query_param():
    proc, _ = start_server(env={'CONFIG_PATH': os.path.join(ROOT, 'config.json')})
    try:
        r = requests.get(base_url()+"/greet?name=Alice", timeout=2)
        assert r.status_code == 200
        j = r.json()
        assert j.get('greeting') == "Hello, Alice!"
    finally:
        stop_server(proc)

def test_greet_without_query_uses_default():
    proc, _ = start_server(env={'CONFIG_PATH': os.path.join(ROOT, 'config.json')})
    try:
        r = requests.get(base_url()+"/greet", timeout=2)
        assert r.status_code == 200
        j = r.json()
        assert j.get('greeting') == "Hello, Friend!"
    finally:
        stop_server(proc)

def test_config_path_override_changes_default_name():
    alt = os.path.join(ROOT, 'config.alt.json')
    proc, _ = start_server(env={'CONFIG_PATH': alt})
    try:
        r = requests.get(base_url()+"/greet", timeout=2)
        assert r.status_code == 200
        j = r.json()
        assert j.get('greeting') == "Hello, Stranger!"
    finally:
        stop_server(proc)

def test_url_encoding_accepts_space_in_name():
    proc, _ = start_server(env={'CONFIG_PATH': os.path.join(ROOT, 'config.json')})
    try:
        r = requests.get(base_url()+"/greet?name=John%20Doe", timeout=2)
        assert r.status_code == 200
        j = r.json()
        assert j.get('greeting') == "Hello, John Doe!"
    finally:
        stop_server(proc)

def test_listening_log_present_on_startup():
    proc, out = start_server(env={'CONFIG_PATH': os.path.join(ROOT, 'config.json')})
    try:
        # we already captured the stdout until listening; verify string present
        assert 'listening' in out.lower()
    finally:
        stop_server(proc)