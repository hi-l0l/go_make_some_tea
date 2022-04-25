import json
import requests
from alive_progress import alive_bar
from banner import banner
from banner import help_banner
import sys

with open('config_socks4.json') as f:
    proxy_providers = json.load(f)


class colors:
    blue='\033[34m'
    purple='\033[35m'
    white= '\033[37m'

class lists:
    socks4 = list()
    socks5 = list()
    http = list()
    _all = list()


def get_proxy():
    total = len(proxy_providers["proxy-providers"])

    print(f"{colors.blue}Getting proxy -->{colors.white}")
    with alive_bar(total) as bar:
        for i in range(len(proxy_providers["proxy-providers"])):
            try:
                r = requests.get(proxy_providers["proxy-providers"][i]['url'], timeout=proxy_providers["proxy-providers"][i]['timeout'])
            except:
                pass
            match proxy_providers["proxy-providers"][i]['type']:
                case 5:
                    lists.socks5 = r.text.split("\n")
                case 4:
                    lists.socks4 = r.text.split("\n")
                case 1:
                    lists.http = r.text.split("\n")
            bar()

def check_proxy(ip, protocol):
    try:
        proxy = f"{protocol}://{ip}"
        requests.get("https://1.1.1.1/", proxies = {"https": proxy}, timeout = 2)
    except Exception as e:
        return False
    return True
    



def check():
    print(f"{colors.blue}Check SOCKS4 -->{colors.white}")
    with alive_bar(len(lists.socks4)) as bar:
        for ip_and_port in lists.socks4:
            print(f"socks4://{ip_and_port}")
            if check_proxy(ip_and_port, "socks4") == True:
                print(f"{colors.purple}socks4://{ip_and_port}{colors.white}")
                lists._all.append(f"socks4://{ip_and_port}")
            bar()

    print(f"{colors.blue}Check SOCKS5 -->{colors.white}")
    with alive_bar(len(lists.socks5)) as bar:
        for ip_and_port in lists.socks5:
            print(f"socks5://{ip_and_port}")
            if check_proxy(ip_and_port, "socks5") == True:
                print(f"{colors.purple}socks5://{ip_and_port}{colors.white}")
                lists._all.append(f"socks5://{ip_and_port}")
            bar()

    print(f"{colors.blue}Check HTTP -->{colors.white}")
    with alive_bar(len(lists.http)) as bar:
        for ip_and_port in lists.http:
            print(f"http://{ip_and_port}")
            if check_proxy(ip_and_port, "http") == True:
                print(f"{colors.purple}http://{ip_and_port}{colors.white}")
                lists._all.append(f"http://{ip_and_port}")
            bar()

def write_file(file_name, _all):
    with open(file_name, 'w') as wr:
        for string in _all:
            wr.write(string+"\n")


if __name__=='__main__':
    if ('-h' or '--help') in sys.argv:
        help_banner()
        sys.exit()

    banner()
    get_proxy()
    check()



    if ('-o' or '--output') in sys.argv:
        index_file_name = sys.argv.index("-o")+1
        file_name = sys.argv[index_file_name]


    if ('-p' or '--proxychains') in sys.argv:
        for i in lists._all:
            protocol = i.split("://")[0]
            ip = i.split("://")[1].split(":")[0]
            port = i.split("://")[1].split(":")[1]
            pr_ip_port = f"{protocol}  {ip} {port}"
            prchains.append(pr_ip_port)

            write_file(file_name, prchains)
    else:
        file_name = 'parsed_proxies.txt'
        write_file(file_name, lists._all)



    answer = input(f"""{colors.blue}
    DONE!\n   {colors.white}
    Output data write in ./parsed_proxies.txt\n
    Show? Y/n {colors.blue}
    """)
    print(colors.white)

    if answer.lower() == "y" or "yes" or '':
        for string in lists._all:
            print(string)
