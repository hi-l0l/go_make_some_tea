import json
import requests
from alive_progress import alive_bar
import aiohttp
import asyncio

with open('config_socks4.json') as f:
    proxy_providers = json.load(f)


class colors:
    red='\033[31m'
    blue='\033[34m'
    purple='\033[35m'
    white= '\033[37m'


def get_proxy():
    global socks4_list
    global socks5_list
    global http_list
    socks4_list = socks5_list = http_list = list()
    total = len(proxy_providers["proxy-providers"])

    print("Getting proxy -->   ")
    with alive_bar(total) as bar:
        for i in range(len(proxy_providers["proxy-providers"])):
            try:
                r = requests.get(proxy_providers["proxy-providers"][i]['url'], timeout=proxy_providers["proxy-providers"][i]['timeout'])
            except:
                pass
            match proxy_providers["proxy-providers"][i]['type']:
                case 5: #socks5
                    socks5_list = r.text.split("\n")
                case 4: #socks4
                    socks4_list = r.text.split("\n")
                case 1: #http
                    http_list = r.text.split("\n")
            bar()



async def check_proxy(ip, protocol):
    async with aiohttp.ClientSession() as session:

        proxy = f"{protocol}://{ip}"
        try:
            async with session.get("https://1.1.1.1/", proxy = proxy, timeout=2) as response:
                resp = await response.status
                print(resp)
                return True
        except Exception as x:
            return False




def check(socks4_list, socks5_list, http_list):
    _all = list()
        
    print("Check SOCKS4 -->")
    with alive_bar(len(socks4_list)) as bar:

        for ip_and_port in socks4_list:
            print(f"socks4://{ip_and_port}")

            if asyncio.run(check_proxy(ip_and_port, "socks4")) == True:
                print(f"{colors.purple}socks4://{ip_and_port}{colors.white}")
                _all.append(f"socks4://{ip_and_port}")

            bar()



    print("Check SOCKS5 -->")
    with alive_bar(len(socks5_list)) as bar:

        for ip_and_port in socks5_list:
            print(f"socks5://{ip_and_port}")

            if asyncio.run(check_proxy(ip_and_port, "socks5")) == True:
                print(f"{colors.purple}socks5://{ip_and_port}{colors.white}")
                _all.append(f"socks5://{ip_and_port}")

            bar()



    print("Check HTTP -->")
    with alive_bar(len(http_list)) as bar:

        for ip_and_port in http_list:
            print(f"http://{ip_and_port}")

            if check_proxy(ip_and_port, "http") == True:
                print(f"{colors.purple}http://{ip_and_port}{colors.white}")
                _all.append(f"http://{ip_and_port}")

            bar()

    return _all

if __name__=='__main__':
    get_proxy()
    all_pr = check(socks4_list, socks5_list, http_list)

    with open('parsed_proxies.txt', 'w') as wr:
        for string in all_pr:
            wr.write(string+"\n")

    answer = input(f"""{colors.blue}
    DONE!\n   {colors.white}
    Output data write in ./parsed_proxies.txt\n
    Show? y/N {colors.blue}
    """)
    print(colors.white)
    if answer.lower() == "y" or "yes":
        for string in all_pr:
            print(string)
            
