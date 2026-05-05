# Secure Software Development in Python

**Author:** CJ Phillips  
**Course:** CMSI 662 — Secure Software Development  
**Date:** April 2026

---

## Abstract

Python is one of the most widely used programming languages, powering web applications, data pipelines, machine learning systems, and cloud infrastructure. Its ease of use and vast ecosystem of third-party packages make it productive but also introduce security risks that developers must actively manage. This paper serves as a practical guide to secure software development in Python, covering the most common vulnerability classes, demonstrating vulnerable and corrected code patterns, and presenting tools and frameworks for building secure Python applications. The discussion is organized around OWASP and CERT secure coding guidelines, with a summary table for quick reference.

---

## 1. Introduction

Python's popularity in web development (Django, Flask), data science (pandas, NumPy), DevOps (Ansible, SaltStack), and machine learning (TensorFlow, PyTorch) means that vulnerabilities in Python code can have far-reaching consequences. Unlike memory-unsafe languages such as C and C++, Python is not susceptible to buffer overflows or use-after-free bugs. However, Python applications face their own class of security challenges: injection attacks, insecure deserialization, dependency supply chain risks, improper secret handling, and path traversal vulnerabilities.

This guide targets developers who are comfortable with Python but want to understand and adopt secure coding practices. Each section presents a vulnerability class, demonstrates a vulnerable code snippet, explains the risk, and provides a corrected implementation.

---

## 2. Injection Attacks

Injection flaws occur when untrusted input is incorporated into commands or queries without proper sanitization. In Python, the most common injection vectors are SQL injection and OS command injection.

### 2.1 SQL Injection

**Vulnerable:**

```python
import sqlite3

def get_user(username):
    conn = sqlite3.connect("app.db")
    query = f"SELECT * FROM users WHERE name = '{username}'"
    return conn.execute(query).fetchone()

# Attacker input: ' OR '1'='1
get_user("' OR '1'='1")
# Executes: SELECT * FROM users WHERE name = '' OR '1'='1'
# Returns all users — authentication bypass
```

The f-string directly interpolates user input into the SQL query, allowing an attacker to modify the query structure.

**Secure:**

```python
import sqlite3

def get_user(username):
    conn = sqlite3.connect("app.db")
    query = "SELECT * FROM users WHERE name = ?"
    return conn.execute(query, (username,)).fetchone()
```

Parameterized queries ensure user input is treated as data, never as SQL syntax. This is the single most effective defense against SQL injection. ORMs like SQLAlchemy and Django's ORM use parameterized queries by default, but developers must avoid raw query methods that accept string interpolation.

### 2.2 OS Command Injection

**Vulnerable:**

```python
import os

def ping_host(host):
    os.system(f"ping -c 1 {host}")

# Attacker input: "8.8.8.8; rm -rf /"
ping_host("8.8.8.8; rm -rf /")
```

`os.system()` passes the string directly to the shell, allowing command chaining via `;`, `&&`, or `|`.

**Secure:**

```python
import subprocess
import shlex

def ping_host(host):
    # Option 1: Use a list of arguments (no shell)
    subprocess.run(["ping", "-c", "1", host], check=True)

    # Option 2: If shell=True is unavoidable, sanitize
    safe_host = shlex.quote(host)
    subprocess.run(f"ping -c 1 {safe_host}", shell=True, check=True)
```

Using `subprocess.run()` with a list of arguments avoids shell interpretation entirely. If shell mode is required, `shlex.quote()` escapes special characters. The CERT guideline IDS07-J (adapted for Python) recommends never constructing shell commands from untrusted input.

---

## 3. Insecure Deserialization

Deserialization converts stored or transmitted data back into objects. In Python, several serialization formats are vulnerable to arbitrary code execution.

### 3.1 Pickle

**Vulnerable:**

```python
import pickle

def load_session(data):
    return pickle.loads(data)  # Executes arbitrary code!
```

An attacker can craft a pickle payload that executes arbitrary Python code upon deserialization by defining a `__reduce__` method:

```python
import pickle
import os

class Exploit:
    def __reduce__(self):
        return (os.system, ("echo HACKED",))

payload = pickle.dumps(Exploit())
# Sending this payload to load_session() executes "echo HACKED"
```

**Secure:**

```python
import json

def load_session(data):
    return json.loads(data)  # Safe — only parses JSON primitives
```

Replace `pickle` with `json` for data interchange. If pickle is truly necessary (e.g., for ML model serialization), use `hmac` to sign pickled data and verify signatures before loading, or use the `fickling` library to analyze pickle files for malicious content.

### 3.2 YAML

**Vulnerable:**

```python
import yaml

config = yaml.load(user_input)  # yaml.load can execute Python objects
```

**Secure:**

```python
import yaml

config = yaml.safe_load(user_input)  # Only loads basic YAML types
```

`yaml.safe_load()` restricts deserialization to basic Python types (strings, numbers, lists, dicts) and refuses to construct arbitrary objects.

---

## 4. Path Traversal

Path traversal attacks exploit file operations that use unsanitized user input to access files outside intended directories.

**Vulnerable:**

```python
from pathlib import Path

UPLOAD_DIR = Path("/app/uploads")

def read_file(filename):
    filepath = UPLOAD_DIR / filename
    return filepath.read_text()

# Attacker input: "../../etc/passwd"
read_file("../../etc/passwd")  # Reads /etc/passwd
```

**Secure:**

```python
from pathlib import Path

UPLOAD_DIR = Path("/app/uploads").resolve()

def read_file(filename):
    filepath = (UPLOAD_DIR / filename).resolve()
    if not filepath.is_relative_to(UPLOAD_DIR):
        raise ValueError("Access denied: path traversal detected")
    return filepath.read_text()
```

Using `Path.resolve()` to canonicalize the path and then verifying it remains within the intended directory prevents traversal. The `is_relative_to()` method (Python 3.9+) provides a clean check.

---

## 5. Secrets and Randomness

### 5.1 Insecure Randomness

**Vulnerable:**

```python
import random

def generate_token():
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=32))
```

Python's `random` module uses a Mersenne Twister PRNG, which is deterministic and predictable. An attacker who observes 624 consecutive outputs can reconstruct the internal state and predict all future values.

**Secure:**

```python
import secrets

def generate_token():
    return secrets.token_hex(32)  # 64-character hex string, cryptographically secure
```

The `secrets` module (PEP 506, Python 3.6+) wraps the OS CSPRNG and is specifically designed for security-sensitive randomness: tokens, passwords, nonces, and session identifiers.

### 5.2 Hardcoded Secrets

**Vulnerable:**

```python
API_KEY = "sk-live-abc123secretkey"
DATABASE_URL = "postgresql://admin:password@prod-db:5432/app"
```

Hardcoded credentials end up in version control, logs, and error messages.

**Secure:**

```python
import os

API_KEY = os.environ["API_KEY"]
DATABASE_URL = os.environ["DATABASE_URL"]
```

Store secrets in environment variables or a secrets manager (AWS Secrets Manager, HashiCorp Vault). Use `.env` files with `python-dotenv` for development, but never commit `.env` to version control. Add `.env` to `.gitignore`.

---

## 6. Dependency and Supply Chain Security

Python's ecosystem relies heavily on PyPI, which has been a target for supply chain attacks including typosquatting (e.g., `reqeusts` instead of `requests`) and malicious package updates.

### Best Practices

1. **Pin dependencies** with exact versions in `requirements.txt` or use lock files (`pip-compile`, `poetry.lock`).
2. **Audit dependencies** regularly:
   ```bash
   pip install pip-audit
   pip-audit
   ```
3. **Verify package integrity** using hashes:
   ```
   # requirements.txt
   requests==2.31.0 --hash=sha256:58cd2187c01e70e6e26505bca751777aa9f2ee0b7f4300988b709f44e013003eb
   ```
4. **Use virtual environments** (`venv`) to isolate project dependencies and prevent global package pollution.
5. **Review new dependencies** before adding them — check download counts, maintenance activity, and known vulnerabilities.

---

## 7. Static Analysis and Security Tools

Python has a rich ecosystem of security-focused static analysis tools:

- **Bandit** — Scans Python code for common security issues (hardcoded passwords, use of `eval`, insecure hash functions, etc.):
  ```bash
  pip install bandit
  bandit -r myproject/
  ```
- **Safety / pip-audit** — Checks installed packages against known vulnerability databases.
- **mypy** — While primarily a type checker, mypy catches type-related bugs that can lead to security issues (e.g., passing unsanitized strings where validated types are expected).
- **Semgrep** — A pattern-based static analysis tool with Python-specific security rules from the community registry.
- **Pylint** — General-purpose linter that can flag dangerous patterns like unused imports (potential typosquat indicators) and broad exception handling.

### Example: Catching Dangerous Functions with Bandit

```python
# Bandit flags these:
eval(user_input)          # B307: Use of possibly insecure function
exec(user_input)          # B102: Use of exec
os.system(cmd)            # B605: Start process with a shell
pickle.loads(data)        # B301: Pickle usage
```

Running `bandit -r .` on a codebase provides an immediate report of high-confidence security issues organized by severity and confidence levels.

---

## 8. Web Application Security

For Python web frameworks (Django, Flask, FastAPI), additional considerations apply:

- **CSRF Protection:** Django includes CSRF middleware by default. Flask requires `Flask-WTF`.
- **XSS Prevention:** Template engines (Jinja2, Django templates) auto-escape output by default. Never use `| safe` or `Markup()` on untrusted input.
- **Authentication:** Use established libraries (`django.contrib.auth`, `Flask-Login`) rather than implementing custom session management.
- **HTTPS:** Configure `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, and `CSRF_COOKIE_SECURE` in Django settings. Use `Talisman` for Flask.
- **Security Headers:** Set `Content-Security-Policy`, `X-Content-Type-Options`, `X-Frame-Options`, and `Strict-Transport-Security` headers.

---

## 9. Summary Table

| Vulnerability | Risk Level | Example | Mitigation | Tool |
|---|---|---|---|---|
| SQL Injection | Critical | String formatting in queries | Parameterized queries / ORM | Bandit, Semgrep |
| Command Injection | Critical | `os.system()` with user input | `subprocess.run()` with list args | Bandit (B605) |
| Pickle Deserialization | Critical | `pickle.loads()` on untrusted data | Use `json`; sign if pickle required | Bandit (B301) |
| YAML Deserialization | High | `yaml.load()` | Use `yaml.safe_load()` | Bandit (B506) |
| Path Traversal | High | Unsanitized file paths | `resolve()` + `is_relative_to()` | Semgrep |
| Insecure Randomness | High | `random` for tokens | `secrets` module | Bandit (B311) |
| Hardcoded Secrets | High | API keys in source | Environment variables / vault | Bandit (B105) |
| Dependency Risks | High | Typosquatting, vulnerable packages | `pip-audit`, pinned deps, hashes | pip-audit, Safety |
| XSS | Medium | `| safe` on untrusted input | Auto-escaping templates | Semgrep |
| CSRF | Medium | Missing CSRF tokens | Framework CSRF middleware | Django check --deploy |

---

## 10. Resources

1. **OWASP Python Security Project** — https://owasp.org/www-project-python-security/
2. **OWASP Top Ten** — https://owasp.org/www-project-top-ten/
3. **Bandit Documentation** — https://bandit.readthedocs.io/
4. **PEP 506: Adding a Secrets Module** — https://peps.python.org/pep-0506/
5. **Python `secrets` Module Documentation** — https://docs.python.org/3/library/secrets.html
6. **pip-audit** — https://github.com/pypa/pip-audit
7. **Semgrep Python Rules** — https://semgrep.dev/r?lang=python&tag=security
8. **Django Security Documentation** — https://docs.djangoproject.com/en/stable/topics/security/
9. **Flask Security Considerations** — https://flask.palletsprojects.com/en/stable/security/
10. **CERT Secure Coding Standards** — https://wiki.sei.cmu.edu/confluence/display/seccode

---

## Bibliography

[1] OWASP Foundation. "OWASP Top Ten Web Application Security Risks." OWASP, 2021.

[2] Van Rossum, G. et al. "PEP 506 — Adding A Secrets Module To The Standard Library." Python Enhancement Proposals, 2015.

[3] Python Software Foundation. "Security Considerations." Python Documentation, 2024.

[4] Bandit Developers. "Bandit: A Security Linter for Python." OpenStack Security Group.

[5] Wheeler, D. "Secure Programming HOWTO." 2015.

[6] CERT/SEI. "SEI CERT Coding Standards." Carnegie Mellon University Software Engineering Institute.

[7] Django Software Foundation. "Security in Django." Django Documentation.

[8] Pallets Projects. "Security Considerations — Flask Documentation." Pallets.
