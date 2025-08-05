import re
from functools import total_ordering


@total_ordering
class Version:
    _semver_regex = re.compile(
        r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
        r"(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
        r"(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$"
    )

    def __init__(self, version: str):
        self.original = version
        match = self._semver_regex.fullmatch(version)
        if match:
            self.major = int(match.group(1))
            self.minor = int(match.group(2))
            self.patch = int(match.group(3))
            self.prerelease = self._parse_identifiers(match.group(4))
            self.build = match.group(5)
        else:
            m = re.match(r"(\d+)\.(\d+)\.(\d+)([a-zA-Z].*)?$", version)
            if not m:
                raise ValueError(f"Invalid version: {version}")
            self.major = int(m.group(1))
            self.minor = int(m.group(2))
            self.patch = int(m.group(3))
            suffix = m.group(4)
            self.prerelease = [suffix] if suffix else []
            self.build = None

    @staticmethod
    def _parse_identifiers(identifiers):
        if identifiers is None:
            return []
        return identifiers.split(".")

    def _compare_identifiers(self, this_ids, other_ids):
        for a, b in zip(this_ids, other_ids):
            if a == b:
                continue
            a_is_num = a.isdigit()
            b_is_num = b.isdigit()
            if a_is_num and b_is_num:
                return int(a) - int(b)
            elif a_is_num:
                return -1
            elif b_is_num:
                return 1
            else:
                return (a > b) - (a < b)
        return len(this_ids) - len(other_ids)

    def __eq__(self, other):
        return (
            (self.major, self.minor, self.patch, self.prerelease)
            == (other.major, other.minor, other.patch, other.prerelease)
        )

    def __lt__(self, other):
        if (self.major, self.minor, self.patch) != (other.major, other.minor, other.patch):
            return (self.major, self.minor, self.patch) < (other.major, other.minor, other.patch)

        if not self.prerelease and other.prerelease:
            return False
        if self.prerelease and not other.prerelease:
            return True
        if not self.prerelease and not other.prerelease:
            return False

        return self._compare_identifiers(self.prerelease, other.prerelease) < 0


def main():
    to_test = [
        ("1.0.0", "2.0.0"),
        ("1.0.0", "1.42.0"),
        ("1.2.0", "1.2.42"),
        ("1.1.0-alpha", "1.2.0-alpha.1"),
        ("1.0.1b", "1.0.10-alpha.beta"),
        ("1.0.0-rc.1", "1.0.0"),
    ]

    for left, right in to_test:
        assert Version(left) < Version(right), "le failed"
        assert Version(right) > Version(left), "ge failed"
        assert Version(right) != Version(left), "neq failed"


if __name__ == "__main__":
    main()