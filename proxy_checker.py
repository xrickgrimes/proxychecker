import requests
from bs4 import BeautifulSoup
import re
import datetime
import os
import io
import shutil
from concurrent.futures import ThreadPoolExecutor
from icmplib import ping

ping_values = []  # Nueva lista para almacenar los valores de ping

def get_proxies():
    log("Obteniendo y verificando proxies...")

    # Listas de URLs de donde se extraen los proxys, las páginas pueden sufrir caídas o simplemente cambian
    # Cada página, se actualiza de 20-30 minutos, depende mucho xd
    urls = [
        "https://www.sslproxies.org/",
        "https://raw.githubusercontent.com/yemixzy/proxy-list/main/proxies/http.txt",
        "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt -o http.txt",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        "https://raw.githubusercontent.com/proxylist-to/proxy-list/main/http.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
        "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/http.txt",
        "https://raw.githubusercontent.com/casals-ar/proxy-list/main/http",
        "https://raw.githubusercontent.com/zloi-user/hideip.me/main/http.txt",
        "https://raw.githubusercontent.com/prxchk/proxy-list/main/http.txt",
        "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/http.txt",
        "https://raw.githubusercontent.com/lkx1331anon/proxy-list/main/http_worldwide.txt",
        "http://feeds.feedburner.com/proxypandora",
        "http://fineproxy.org/eng/fresh-proxies/",
        "http://free-proxy-list.net/anonymous-proxy.html",
        "http://hack-hack.chat.ru/proxy/anon.txt",
        "http://hack-hack.chat.ru/proxy/p1.txt",
        "http://hack-hack.chat.ru/proxy/p2.txt",
        "http://hack-hack.chat.ru/proxy/p3.txt",
        "http://hack-hack.chat.ru/proxy/p4.txt",
        "http://nntime.com/proxy-updated-01.htm",
        "http://nntime.com/proxy-updated-02.htm",
        "http://nntime.com/proxy-updated-03.htm",
        "http://nntime.com/proxy-updated-04.htm",
        "http://nntime.com/proxy-updated-05.htm",
        "http://nntime.com/proxy-updated-06.htm",
        "http://nntime.com/proxy-updated-07.htm",
        "http://nntime.com/proxy-updated-08.htm",
        "http://nntime.com/proxy-updated-09.htm",
        "http://nntime.com/proxy-updated-10.htm",
        "http://premiumproxy.net",
        "http://premiumproxy.net/anonymous-proxy-list.php",
        "http://premiumproxy.net/http-proxy-list.php",
        "http://premiumproxy.net/https-ssl-proxy-list.php",
        "http://proxyape.com/",
        "http://proxydb.net/",
        "http://proxylistchecker.org/proxylists.php?t=elite",
        "http://proxytime.ru/http",
        "http://rootjazz.com/proxies/proxies.txt",
        "http://spys.me/proxy.txt",
        "http://spys.ru/free-proxy-list/RU/",
        "http://txt.proxyspy.net/proxy.txt",
        "http://www.freeproxy.ru/download/lists/goodproxy.txt",
        "http://www.gatherproxy.com/",
        "http://www.live-socks.net/feeds/posts/default",
        "http://www.megaproxylist.net/",
        "http://www.proxylists.net/http.txt",
        "http://www.proxylists.net/http_highanon.txt",
        "http://www.proxylists.net/socks4.txt",
        "http://www.proxylists.net/socks5.txt",
        "https://55utd55.com/",
        "https://advanced.name/freeproxy",
        "https://api.openproxylist.xyz/http.txt",
        "https://api.openproxylist.xyz/socks4.txt",
        "https://api.openproxylist.xyz/socks5.txt",
        "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http",
        "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
        "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4",
        "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=10000&country=all",
        "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=10000&country=all",
        "https://free-proxy-list.com/",
        "https://free-proxy-list.net/",
        "https://free-proxy-list.net/anonymous-proxy.html",
        "https://free-proxy-list.net/uk-proxy.html",
        "https://freevpn.ninja/free-proxy/txt",
        "https://geonode.com/free-proxy-list",
        "https://guncelproxy.com/",
        "https://hidemy.name/de/proxy-list/",
        "https://hidemyna.me/en/proxy-list/",
        "https://multiproxy.org/txt_all/proxy.txt",
        "https://openproxy.space/list/http",
        "https://openproxy.space/list/socks4",
        "https://premiumproxy.net/",
        "https://premiumproxy.net/full-proxy-list",
        "https://premproxy.com/list/ip-port/1.htm",
        "https://premproxy.com/list/ip-port/10.htm",
        "https://premproxy.com/list/ip-port/11.htm",
        "https://premproxy.com/list/ip-port/12.htm",
        "https://premproxy.com/list/ip-port/13.htm",
        "https://premproxy.com/list/ip-port/14.htm",
        "https://premproxy.com/list/ip-port/15.htm",
        "https://premproxy.com/list/ip-port/16.htm",
        "https://premproxy.com/list/ip-port/17.htm",
        "https://premproxy.com/list/ip-port/18.htm",
        "https://premproxy.com/list/ip-port/19.htm",
        "https://premproxy.com/list/ip-port/2.htm",
        "https://premproxy.com/list/ip-port/3.htm",
        "https://premproxy.com/list/ip-port/4.htm",
        "https://premproxy.com/list/ip-port/5.htm",
        "https://premproxy.com/list/ip-port/6.htm",
        "https://premproxy.com/list/ip-port/7.htm",
        "https://premproxy.com/list/ip-port/8.htm",
        "https://premproxy.com/list/ip-port/9.htm",
        "https://premproxy.com/list/{01-15}.htm",
        "https://premproxy.com/socks-list/ip-port/1.htm",
        "https://premproxy.com/socks-list/ip-port/2.htm",
        "https://premproxy.com/socks-list/ip-port/3.htm",
        "https://premproxy.com/socks-list/ip-port/4.htm",
        "https://premproxy.com/socks-list/ip-port/5.htm",
        "https://premproxy.com/socks-list/ip-port/6.htm",
        "https://premproxy.com/socks-list/ip-port/8.htm",
        "https://premproxy.com/socks-list/{01-20}.htm",
        "https://proxydb.net/?offset=105",
        "https://proxydb.net/?offset=120",
        "https://proxydb.net/?offset=135",
        "https://proxydb.net/?offset=15",
        "https://proxydb.net/?offset=150",
        "https://proxydb.net/?offset=30",
        "https://proxydb.net/?offset=45",
        "https://proxydb.net/?offset=75",
        "https://proxydb.net/?offset=90",
        "https://proxyfreaks.com/",
        "https://proxypremium.top/elite-proxy-list",
        "https://proxypremium.top/full-proxy-list",
        "https://proxypremium.top/http-proxy-list",
        "https://proxypremium.top/https-ssl-proxy-list",
        "https://proxypremium.top/socks-proxy-list",
        "https://proxyservers.pro/",
        "https://proxyunique.com",
        "https://raw.githubusercontent.com/almroot/proxylist/master/list.txt",
        "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
        "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt",
        "https://raw.githubusercontent.com/drakelam/Free-Proxy-List/main/proxy_s4.txt",
        "https://raw.githubusercontent.com/hendrikbgr/Free-Proxy-Repo/master/proxy_list.txt",
        "https://raw.githubusercontent.com/Inplex-sys/proxy-list/main/https.txt",
        "https://raw.githubusercontent.com/Inplex-sys/proxy-list/main/socks4.txt",
        "https://raw.githubusercontent.com/Inplex-sys/proxy-list/main/socks5.txt",
        "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http%2Bhttps.txt",
        "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks4.txt",
        "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies.txt",
        "https://raw.githubusercontent.com/manuGMG/proxy-365/main/SOCKS5.txt",
        "https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt",
        "https://raw.githubusercontent.com/mmpx12/proxy-list/master/https.txt",
        "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks4.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
        "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
        "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt",
        "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt",
        "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
        "https://raw.githubusercontent.com/TundzhayDzhansaz/proxy-list-auto-pull-in-30min/main/proxies/http.txt",
        "https://raw.githubusercontent.com/UserR3X/proxy-list/main/http%2Bs.txt",
        "https://raw.githubusercontent.com/UserR3X/proxy-list/main/socks4.txt",
        "https://raw.githubusercontent.com/Volodichev/proxy-list/main/http.txt",
        "https://raw.githubusercontent.com/zeynoxwashere/proxy-list/main/http.txt",
        "https://raw.githubusercontent.com/zeynoxwashere/proxy-list/main/socks4.txt",
        "https://raw.githubusercontent.com/zeynoxwashere/proxy-list/main/socks5.txt",
        "https://spys.one/en/free-proxy-list/",
        "https://topproxy.info/",
        "https://worldproxy.info/",
        "https://www.google-proxy.net/",
        "https://www.my-proxy.com/free-anonymous-proxy.html",
        "https://www.my-proxy.com/free-elite-proxy.html",
        "https://www.my-proxy.com/free-proxy-list-10.html",
        "https://www.my-proxy.com/free-proxy-list-2.html",
        "https://www.my-proxy.com/free-proxy-list-3.html",
        "https://www.my-proxy.com/free-proxy-list-4.html",
        "https://www.my-proxy.com/free-proxy-list-5.html",
        "https://www.my-proxy.com/free-proxy-list-6.html",
        "https://www.my-proxy.com/free-proxy-list-7.html",
        "https://www.my-proxy.com/free-proxy-list-8.html",
        "https://www.my-proxy.com/free-proxy-list-9.html",
    ]

    valid_proxies = []
        # Usar más de 500 workers, puede perjudircar el rendimiento de tu pc, queda en tu responsabilidad xd
    with ThreadPoolExecutor(max_workers=500) as executor:

        # Utilizo concurrencia para obtener y verificar proxies en paralelo, así compruebo y valido proxys más rápido
        futures = [executor.submit(get_and_check_proxy, url, valid_proxies) for url in urls]

    return valid_proxies

def get_and_check_proxy(url, valid_proxies):
    try:
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            proxies = re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', soup.text)

            for proxy in proxies:
                if check_proxy(proxy):
                    valid_proxies.append(proxy)
                    save_proxy(proxy)
                    measure_ping(proxy)
                else:
                    log_invalid_proxy(proxy)
        else:
            log(f"Error al obtener proxies de {url}. Código de estado: {response.status_code}")

    except requests.RequestException as e:
        log(f"Error al obtener proxies de {url}: {e}")

def check_proxy(proxy):
    try:
        response = requests.get('http://www.google.com', proxies={'http': proxy, 'https': proxy}, timeout=5)
        return response.status_code == 200
    except requests.RequestException as e:
        return False

def measure_ping(proxy):
    try:
        # Aquí uso la librería icmplib para medir el ping xd
        host = proxy.split(':')[0]
        response = ping(host, count=4)

        if response.is_alive:
            log_ping(f"Ping a {host}: {response.avg_rtt} ms")
            ping_values.append(response.avg_rtt)  # Agrega el valor de ping a la lista
        else:
            log_ping(f"No se pudo medir el ping a {host}")
            ping_values.append(None)  # Agrega "None" si no se pudo medir el ping

    except Exception as e:
        log_ping(f"Error al medir el ping de {proxy}: {e}")
        ping_values.append(None)  # Agrega "None" si hay un error

def save_proxy(proxy):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    proxies_file_path = os.path.join(script_dir, 'proxies.txt')

    # Elimina duplicados antes de agregar la nueva proxy
    existing_proxies = set(read_existing_proxies(proxies_file_path))
    existing_proxies.add(proxy)

    log(f"Proxy válida guardada en {proxies_file_path}: {proxy}")

    try:
        with open(proxies_file_path, 'w') as file:
            for existing_proxy in existing_proxies:
                file.write(existing_proxy + '\n')
    except Exception as e:
        log(f"Error al escribir en {proxies_file_path}: {e}")

def read_existing_proxies(file_path):
    try:
        with open(file_path, 'r') as file:
            return {line.strip() for line in file}
    except FileNotFoundError:
        return set()

def log_invalid_proxy(proxy):
    log(f"Proxy inválido: {proxy}")

def check_proxies(proxies):
    log("Guardando proxies válidos en proxies.txt...")

    with open('proxies.txt', 'w') as file:
        for valid_proxy in proxies:
            file.write(valid_proxy + '\n')

    log("Proxies válidos finales guardados en proxies.txt:")
    for valid_proxy in proxies:
        log(valid_proxy)

def log_ping(message):
    separator = "=" * 50  # Separador de igual tamaño
    log(f"{separator}\n{message}\n{separator}")

def log(message, include_date=True):
    timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]") if include_date else ""
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_folder = os.path.join(script_dir, 'proxy_logs')
    log_path = os.path.join(log_folder, 'proxies_log.txt')

    try:
        # Crea la carpeta si no existe...
        os.makedirs(log_folder, exist_ok=True)

        formatted_message = f"{timestamp} >>> {message}" if include_date else message

        # Esto imprime solo el mensaje simplificado
        print(formatted_message)

        with io.open(log_path, 'a', encoding='utf-8') as file:
            file.write(formatted_message + '\n')
    except Exception as e:
        print(f"Error al escribir en {log_path}: {e}")

def set_console_size(width, height):
    os.system(f"mode con: cols={width} lines={height}")

def print_large_title(title):
    os.system("cls" if os.name == "nt" else "clear")  # Limpiar la consola

    # Esto obtiene el ancho actual de la consola
    console_width = shutil.get_terminal_size().columns

    # Y aqui se ajusta el título Rick Grimes a cualquier tamaño de la consola (ESTO NO FUNCIONA xdddd, me harté y lo dejo en el code)
    adjusted_title = "\n".join([line.center(console_width) for line in title.split("\n")])

    # Imprimir el título en grande
    print(adjusted_title)

def main():
    set_console_size(82, 30)  # Ajusta el tamaño de la consola, para que se note el codigo ASCII :)

    title = "  n\
    ___    ____  _____   __ __       _____   ___    ____   __  ___   ____   ____ n\
   / _ \  /  _/ / ___/  / //_/      / ___/  / _ \  /  _/  /  |/  /  / __/  / __/ n\
  / , _/ _/ /  / /__   / ,<        / (_ /  / , _/ _/ /   / /|_/ /  / _/   _\ \  n\
 /_/|_| /___/  \___/  /_/|_|       \___/  /_/|_| /___/  /_/  /_/  /___/  /___/ "

    create_by_rick_grimes="         ╬ ─────Checker creado e inspirado en el prototipo de 0.1───── ╬"

    print_large_title(title)
    print("\n" * 1)
    print(create_by_rick_grimes)

    print("\n           ========== Bienvenido al verificador de proxies. ==========")
    print("\n" *0)
    log("                          1. Obtener y verificar proxys", include_date=False)
    log("                                2. Salir de aquí", include_date=False)

    while True:
        print("\n" *0)
        choice = input("                           Selecciona una opción (1-2): ")

        if choice == '1':
            # Obtiene la lista de proxies
            proxy_list = get_proxies()

            # Verifica los proxies y los guarda en proxies.txt
            check_proxies(proxy_list)
            
        elif choice == '2':
            log("Saliendo del programa.")
            print("Saliendo del programa.")
            break  # Se sale del bucle y termina el programa
        else:
            print("\n" *0)
            log("                Opción no válida. Por favor, selecciona (1 o 2).", False)  # False hace que no incluya la fecha en las opciones...

if __name__ == "__main__":
    main()

    #Y nada, hice lo mejor que pude, sé que esto es una mrd, pero me divertí haciéndolo xd