from pathlib import Path


def _get_self_cpu_cgroup() -> str:
    with open("/proc/self/cgroup") as f:
        for line in f:
            if ":cpu,cpuacct:" in line:
                return ':'.join(line.strip().split(':', 3)[2:])

    raise ValueError("cpu cgroup not found!")


class CpuLimiter:
    def __init__(self, percent: int, cgroupfs: str = "/sys/fs/cgroup"):
        assert 0 < percent <= 100
        self._percent = percent
        path = _get_self_cpu_cgroup()
        self._quota_path = Path(f"{cgroupfs}/cpu{path}/cpu.cfs_quota_us")
        self._period_path = Path(f"{cgroupfs}/cpu{path}/cpu.cfs_period_us")
        self._previous_quota = None

    def __enter__(self):
        self._previous_quota = self._quota_path.read_text()
        period = int(self._period_path.read_text())
        self._quota_path.write_text(str(int(self._percent / 100 * period)))

    def __exit__(self, exc_type, exc_val, exc_tb):
        assert self._previous_quota is not None
        self._quota_path.write_text(self._previous_quota)
        self._previous_quota = None
