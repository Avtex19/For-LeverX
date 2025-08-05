# Semantic Version Comparison in Python

This project implements a `Version` class that supports **semantic versioning** comparison according to the [Semantic Versioning 2.0.0 specification](https://semver.org/).

## Features

- Supports full SemVer format: `MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]`
- Implements rich comparison (`==`, `<`, `>`, etc.)
- Handles common variations like `1.0.1b` (gracefully falls back if not fully SemVer-compliant)
- Ignores build metadata (`+build`) in comparisons, as per SemVer rules

---

## Usage
```
>>> Version('1.1.3') < Version('2.2.3')
True
>>> Version('1.3.0') > Version('0.3.0')
True
>>> Version('0.3.0b') < Version('1.2.42')
True
>>> Version('1.3.42') == Version('42.3.1')
False
```
