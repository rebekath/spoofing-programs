import subprocess
import time

# Nuevas direcciones IP del router y su dirección MAC correcta
ROUTER_IP = "192.168.1.1"
CORRECT_MAC = "00:11:22:33:44:55"  # Cambia esta dirección MAC por la correcta de tu router

def get_mac(ip):
    try:
        output = subprocess.check_output(["arp", "-n", ip])
        for line in output.decode().split("\n"):
            if ip in line:
                return line.split()[2]
    except Exception as e:
        print(f"Error al obtener la MAC para {ip}: {e}")
        return None

def detect_arp_spoofing(router_ip, correct_mac):
    current_mac = get_mac(router_ip)
    if current_mac is None:
        print(f"No se pudo obtener la MAC del router {router_ip}.")
        return
    if current_mac != correct_mac:
        print(f"ALERTA: Se detectó un posible ataque ARP Spoofing. La dirección MAC actual {current_mac} no coincide con la dirección MAC correcta {correct_mac}.")
    else:
        print(f"Todo está bien. La dirección MAC del router {router_ip} no ha sido modificada.")

if __name__ == "__main__":
    while True:
        detect_arp_spoofing(ROUTER_IP, CORRECT_MAC)
