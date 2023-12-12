import argparse
import subprocess

def runCommand(command):
        result=subprocess.run("sudo "+command,shell=True,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        return result.stdout.strip()

def kill_qemu_processes(interface_name):
    # Obtener la lista de PIDs asociados con la interfaz TAP
    pid = runCommand(f"ps -aux | grep qemu | grep {interface_name} | grep -v grep | awk '{{print $2}}'")
    runCommand(f"kill -9 {pid}")


def remove_interfaces_with_idVlan(number):
    # Obtener las interfaces con el número específico
    result = runCommand(f"ovs-vsctl show | awk '/{number}/ && /Interface/ {{print $2}}'")
    interfaces = result.splitlines()

    # Iterar sobre las interfaces y eliminar cada una
    for interface in interfaces:
        kill_qemu_processes(interface)
        runCommand(f"ovs-vsctl del-port {interface}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kill QEMU processes associated with a specific VLAN ID.")
    parser.add_argument("id_vlan", type=int, help="VLAN ID for which QEMU processes should be killed.")
    args = parser.parse_args()
    remove_interfaces_with_idVlan(args.id_vlan)