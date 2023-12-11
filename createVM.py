import subprocess,argparse,random

def generar_mac():
	parte_fija = "fa:16:3e"
	resto = ':'.join(['{:02x}'.format(random.randint(0, 255)) for _ in range(3)])
	direccion_mac = parte_fija + ':' + resto
	return direccion_mac

def runCommand(command):
	print(command)
	result=subprocess.run(command,shell=True,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

def createTap(port,idVlan):
	runCommand(f"ip tuntap add mode tap name slice{idVlan}-tap{port}")
	print(f"TAP slice{idVlan}-tap{port}: creado exitosamente!!")

def createVM(port,idVlan):
	dir_mac=generar_mac()
	runCommand(f"qemu-system-x86_64 -enable-kvm -vnc 0.0.0.0:{port} -netdev tap,id=slice{idVlan}-tap{port},ifname=slice{idVlan}-tap{port},script=no,downscript=no -device e1000,netdev=slice{idVlan}-tap{port},mac={dir_mac} -daemonize -snapshot cirros-0.5.1-x86_64-disk.img")


if __name__=='__main__':
	print(generar_mac())
	parser = argparse.ArgumentParser(description='Script para crear VM')
	parser.add_argument('param1', type=str, help='Nombre del OVS')
	parser.add_argument('param2', type=str, help='ID de la Vlan')
	parser.add_argument('param3', type=str, help='El puerto VNC:')

	args = parser.parse_args()

	name_OVS= args.param1
	id_Vlan= args.param2
	port_vnc=  args.param3

        #Creamos el TAP
	createTap(port_vnc,id_Vlan)

        #Creamos la VM
	createVM(port_vnc,id_Vlan)

        #Añadimos TAP a la OVS
	runCommand(f"ovs-vsctl add-port {name_OVS} slice{id_Vlan}-tap{port_vnc} tag={id_Vlan}")

        #Encendemos el TAP
	runCommand(f"ip link set dev slice{id_Vlan}-tap{port_vnc} up")


	