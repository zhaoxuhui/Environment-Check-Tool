import sys
import platform


def checkPythonVersion():
    return float(sys.version[:3])


def checkOS():
    os_info = platform.system()
    return os_info


def checkPipVersionPy3():
    import subprocess
    code, pip_version = subprocess.getstatusoutput("pip --version")
    if code == 1:
        pip_version = 0
    else:
        pip_version = pip_version.split("pip")[1].split("from")[0].strip()
        parts = pip_version.split(".")
        pip_version = float(parts[0] + "." + parts[1])
    return pip_version


def checkPipVersionPy2():
    import commands
    code, pip_version = commands.getstatusoutput("pip --version")
    if code == 1:
        pip_version = 0
    else:
        pip_version = pip_version.split("pip")[1].split("from")[0].strip()
        parts = pip_version.split(".")
        pip_version = float(parts[0] + "." + parts[1])
    return pip_version


def checkCUDAPy3():
    import subprocess
    code, nvcc_info = subprocess.getstatusoutput("nvcc --version")
    if code == 1:
        nvcc_info = 0
    else:
        nvcc_info = float(nvcc_info.split("release")[1].split(",")[0].strip())
    return nvcc_info


def checkCUDAPy2():
    import commands
    code, nvcc_info = commands.getstatusoutput("nvcc --version")
    if code == 1:
        nvcc_info = 0
    else:
        nvcc_info = float(nvcc_info.split("release")[1].split(",")[0].strip())
    return nvcc_info


def checkCondaPy3():
    import subprocess
    code, conda_info = subprocess.getstatusoutput("conda --version")
    if code == 1:
        conda_info = 0
    else:
        parts = conda_info.split("conda")[1].split(".")
        conda_info = float(parts[0] + "." + parts[1])
    return conda_info


def checkCondaPy2():
    import commands
    code, conda_info = commands.getstatusoutput("conda --version")
    if code == 1:
        conda_info = 0
    else:
        parts = conda_info.split("conda")[1].split(".")
        conda_info = float(parts[0] + "." + parts[1])
    return conda_info


def cpuCount():
    try:
        import psutil
        number = psutil.cpu_count()
        return str(number)
    except:
        return "No 'psutil' on your computer,install it with 'pip install psutil'"


def cpuFreq():
    try:
        import psutil
        info = psutil.cpu_freq()
        info = str(round(float(info[2]) / 1000, 2))
        return str(info)
    except:
        return "No 'psutil' on your computer,install it with 'pip install psutil'"


def cpuUsage():
    try:
        import psutil
        info = psutil.cpu_percent(interval=1, percpu=True)
        return info
    except:
        return "No 'psutil' on your computer,install it with 'pip install psutil'"


def memSize():
    try:
        import psutil
        info = psutil.virtual_memory()
        info = str(round(float(info[0]) / pow(1024, 3), 2))
        return str(info)
    except:
        return "No 'psutil' on your computer,install it with 'pip install psutil'"


def memInfo():
    try:
        import psutil
        info = psutil.virtual_memory()
        usage = str(info[2])
        avail = str(round(float(info[1]) / pow(1024, 3), 2))
        return usage, avail
    except:
        return "No 'psutil' on your computer,install it with 'pip install psutil'"


def diskSize():
    import psutil
    disk_size = []
    for item in psutil.disk_partitions():
        mountpoint = item[1]
        opts = item[3]
        if opts == 'cdrom':
            continue
        size = psutil.disk_usage(mountpoint)
        size = round(float(size[0]) / pow(1024, 3), 2)
        disk_size.append(size)
    total_size = round(sum(disk_size), 2)
    return str(total_size)
    try:
        pass
    except:
        return "No 'psutil' on your computer,install it with 'pip install psutil'"


def diskInfo():
    try:
        import psutil
        part_size = []
        part_usage = []
        part_name = []
        part_fstype = []
        for item in psutil.disk_partitions():
            name = item[0]
            mountpoint = item[1]
            fstype = item[2]
            opts = item[3]
            if opts == 'cdrom':
                continue
            info = psutil.disk_usage(mountpoint)
            size = round(float(info[0]) / pow(1024, 3), 2)
            part_size.append(size)
            part_usage.append(str(info[3]) + "%")
            part_name.append(name)
            part_fstype.append(fstype)
        return part_name, part_size, part_usage, part_fstype
    except:
        return "No 'psutil' on your computer,install it with 'pip install psutil'"


if __name__ == '__main__':
    python_v = checkPythonVersion()
    os = checkOS()
    if python_v > 3:
        pip_v = checkPipVersionPy3()
        cuda_v = checkCUDAPy3()
        conda_v = checkCondaPy3()
    else:
        pip_v = checkPipVersionPy2()
        cuda_v = checkCUDAPy2()
        conda_v = checkCondaPy2()

    print("=======================System Information=======================")
    print("* This computer runs " + os + " system.")
    print("* Python version(running this script):" + python_v.__str__())
    if pip_v == 0:
        print("* Pip version:It seems no pip on your computer.")
    else:
        print("* Pip version:" + pip_v.__str__())
    if cuda_v == 0:
        print("* CUDA version:It seems no CUDA on your computer.")
    else:
        print("* CUDA version:" + cuda_v.__str__())
    if conda_v == 0:
        print("* Conda version:It seems no Conda on your computer.")
    else:
        print("* Conda version:" + conda_v.__str__())
    print("=======================System Information=======================")

    cpu_count = cpuCount()
    cpu_freq = cpuFreq()
    cpu_usage = cpuUsage()
    mem_size = memSize()
    mem_usage = memInfo()
    disk_size = diskSize()
    disk_info = diskInfo()

    print("======================Hardware Information======================")
    print("* CPU kernel:" + cpu_count)
    print("* CPU base frequency:" + cpu_freq + " GHz")
    print("* CPU use percentage(current,every kernel):\n" + "  " + str(cpu_usage))
    print("* Memory total size:" + mem_size + " GB")
    print("* Memory use percentage(current):" + mem_usage[0] + "%, free:" + mem_usage[1] + " GB")
    print("* Disk total size:" + disk_size + " GB")
    print("* Disk partion info:")
    print("  Identifier\tTotal size(GB)\tUsage(percentage)\tFile format")
    for i in range(len(disk_info)):
        print("  " + disk_info[0][i] + "\t\t\t" + str(disk_info[1][i]) + "\t\t\t" + str(disk_info[2][i]) + "\t\t\t\t" +
              disk_info[3][i])
    print("======================Hardware Information======================")
