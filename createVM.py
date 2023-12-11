import os
import socket
import subprocess,argparse,random

passHeadnode='ubuntu'

def find_available_portVNC(starting_port=5901):
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', starting_port))
                return starting_port-5900
        except socket.error:
            starting_port += 1

def runCommand(command):
	result=subprocess.run("sudo "+command,shell=True,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	return result

def createTap(port,idVlan):
	runCommand(f"ip tuntap add mode tap name slice{idVlan}-tap{port}")
	print(f"TAP slice{idVlan}-tap{port}: creado exitosamente!!")

def createVM(port,idVlan,path_imagen,size_ram,dir_mac):
	set_path_image(path_imagen)
	runCommand(f"qemu-system-x86_64 -enable-kvm -m {size_ram} -vnc 0.0.0.0:{port} -netdev tap,id=slice{idVlan}-tap{port},ifname=slice{idVlan}-tap{port},script=no,downscript=no -device e1000,netdev=slice{idVlan}-tap{port},mac={dir_mac} -daemonize -snapshot {path_imagen}")

def set_path_image(path_imagen):
	path_absoluto=os.path.expanduser(path_imagen)

	# Dividir la ruta en el directorio y el nombre del archivo
	directorio, archivo = os.path.split(path_absoluto)

	# Crear el directorio si no existe
	if not os.path.exists(directorio):
		os.makedirs(directorio)

	# Verificar si el archivo ya existe
	if not os.path.exists(path_absoluto):
		#Se crea previamente las llaves duplicadas para acceso directo
		subprocess.run(f"sshpass -p '{passHeadnode}' sudo scp -o StrictHostKeyChecking=no ubuntu@10.0.0.1:{path_absoluto} {path_absoluto}",shell=True,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

if __name__=='__main__':
	parser = argparse.ArgumentParser(description='Script para crear VM')
	parser.add_argument('param1', type=str, help='Nombre del OVS')
	parser.add_argument('param2', type=str, help='ID de la Vlan')
	#parser.add_argument('param3', type=str, help='El puerto VNC:')
	parser.add_argument('param3', type=str, help='El path de la imagen')
	parser.add_argument('param4', type=str, help='Size Ram de la VM')
	parser.add_argument('param5', type=str, help='Dirección MAC')

	args = parser.parse_args()

	name_OVS= args.param1
	id_Vlan= args.param2
	#port_vnc=  args.param3
	path_imagen=  args.param4
	size_ram=  args.param5
	dir_mac= args.param6

	port_vnc=find_available_portVNC()

    #Creamos el TAP
	#createTap(port_vnc,id_Vlan)

        #Creamos la VM
	#createVM(port_vnc,id_Vlan,path_imagen,size_ram,dir_mac)

        #Añadimos TAP a la OVS
	#runCommand(f"ovs-vsctl add-port {name_OVS} slice{id_Vlan}-tap{port_vnc} tag={id_Vlan}")

        #Encendemos el TAP
	#runCommand(f"ip link set dev slice{id_Vlan}-tap{port_vnc} up")

	print(port_vnc)



	