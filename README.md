A simple utility that utilizes cgroups (and root privs... :) to limit the CPU usage of specific code blocks.

```python
with CpuLimiter(percent=30):
    # this code will be capped at 30% CPU
    # also, any other program it runs, e.g via subprocess.run
```

TODOs
* Create a new cgroup, move current thread into it, instead of changing the limit of current cgroup.
* Try getting it to work in non-privileged containers
