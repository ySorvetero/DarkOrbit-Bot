import time
import requests
from datetime import datetime
import json
import os
from colorama import Fore, Back, Style, init
import colorama
colorama.init()
init(autoreset=True)

with open('config.json') as config_file:
    config_data = json.load(config_file)
print("Iniciado!")

usuario = config_data["login"]
password = config_data["senha"]
iniciar = config_data["iniciar"]
comprar = config_data["comprar"]


while True:
    def principal():
        def login():
            def get_strp(string, start, end):
                str_ = string.split(start)[1].split(end)[0]
                return str_

            def get_str(string, start, end):
                try:
                    str_ = string.split(start)[1].split(end)[0]
                except IndexError:
                    str_ = ""
                return str_

            s = requests.Session()
            getoken = s.get('https://int1.darkorbit.com/index.es?action=externalHome&loginError=94')
            token = get_str(getoken.text, 'name="reloadToken" value="', '">')
            tokenRES = get_str(getoken.text, 'amp;token=', '">')
            if token is not None:
                headers = {
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
                    'Cache-Control': 'max-age=0',
                    'Connection': 'keep-alive',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Origin': 'https://www.darkorbit.com',
                    'Referer': 'https://www.darkorbit.com/',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'cross-site',
                    'Sec-Fetch-User': '?1',
                    'Upgrade-Insecure-Requests': '1',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
                    'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                }

                params = {
                    'authUser': '22',
                    'token': tokenRES,
                }

                data = {
                    'username': usuario,
                    'password': password,
                }

                response = s.post(f'https://sas.bpsecure.com/Sas/Authentication/Bigpoint?authUser=22&token={tokenRES}',
                                  allow_redirects=True, params=params, headers=headers,
                                  data=data)
                current_date_and_time = datetime.now()
                if "LICENÇA DE PILOTO" in response.text:
                    print(Fore.GREEN + "~[ CONSOLE ] - Login realizado.")
                    with open('eventos.log', 'a') as f:
                        f.write(str(current_date_and_time) + ' ~[ CONSOLE ] - Login Realizado' + '\n')
                    getprice = s.get("https://int1.darkorbit.com/indexInternal.es?action=internalAuction")
                    if 'Mais devagar, piloto espacial!' in getprice.text:
                        print(Fore.RED + "~[ CAPTCHA ] - Mais devagar, piloto espacial!")

                    elif 'COMPRA IMEDIATA' in getprice.text:
                        print(Fore.GREEN + '~[ CONSOLE ] - Acesso permitido ao Leilao!')
                        with open('eventos.log', 'a') as f:
                            f.write(
                                str(current_date_and_time) + ' ~[ CONSOLE ] - Acesso permitido ao Leilao!' + '\n')
                        preco = get_str(getprice.text, '" id="item_hour_25_bid" value="', '" />')
                        preco_int = int(preco)
                        print(Fore.GREEN + f"~[ CONSOLE ] PREÇO ATUAL {preco_int}")
                        with open('eventos.log', 'a') as f:
                            f.write(
                                str(current_date_and_time) + f' ~[ CONSOLE ] PREÇO ATUAL {preco_int}' + '\n')
                        while True:
                            current_date_and_time = datetime.now()
                            tempo = current_date_and_time.strftime("%M%S")

                            def modulo():
                                getprice = s.get("https://int1.darkorbit.com/indexInternal.es?action=internalAuction")
                                token = get_strp(getoken.text, 'name="reloadToken" value="', '">')

                                if preco_int <= 100000:
                                    oferta = preco_int + 10000
                                    params = {
                                        'action': 'internalAuction',
                                        'reloadToken': token,
                                    }

                                    data = {
                                        'reloadToken': token,
                                        'auctionType': 'hour',
                                        'subAction': 'bid',
                                        'lootId': 'equipment_extra_cpu_ajp-01',
                                        'itemId': 'item_hour_25',
                                        'credits': oferta,
                                        'auction_buy_button': 'LICITAR',
                                    }

                                    response = s.post('https://int1.darkorbit.com/indexInternal.es', params=params,
                                                      data=data)

                                    cstatus = get_str(response.text, "infoText = '", "';")
                                    if 'Licitação feita' in cstatus:
                                        print(Fore.GREEN + "~[ CONSOLE ] - Licitação feita - Reiniciando..")

                                        with open('compras.txt', 'a') as f:
                                            # Escrever a data e hora atual no arquivo
                                            f.write(str(current_date_and_time) + ' - Compra realizada' + '\n')
                                        with open('eventos.log', 'a') as f:
                                            f.write(
                                                str(current_date_and_time) + ' ~[ CONSOLE ] - Licitação feita - Reiniciando..' + '\n')
                                    else:
                                        print(Fore.YELLOW + "~[ CONSOLE ] - Valor superior a 50.000 - Reiniciando..")
                                        with open('compras.txt', 'a') as f:
                                            # Escrever a data e hora atual no arquivo
                                            f.write(str(current_date_and_time) + ' - Valor Superior a 50.000' + '\n')
                                        with open('eventos.log', 'a') as f:
                                            f.write(
                                                str(current_date_and_time) + ' ~[ CONSOLE ] - Valor Superior a 50.000' + '\n')

                            if comprar in tempo:
                                modulo()
                                time.sleep(18)
                                break
                            else:
                                print(Fore.GREEN + '~[ CONSOLE ] - FEITO LOGIN: ' + tempo)

                elif 'Resolve o captcha' in response.text:
                    print(Fore.RED + '~[ CONSOLE ] - Resolve o captcha')
                    with open('eventos.log', 'a') as f:
                        f.write(str(current_date_and_time) + ' ~[ CONSOLE ] - Resolve o captcha' + '\n')
                else:
                    pass
        while True:
            current_date_and_time = datetime.now()
            minute_second = current_date_and_time.strftime("%M%S")
            if iniciar in minute_second:
                with open('eventos.log', 'a') as f:
                    f.write(str(current_date_and_time) + ' ~[ CONSOLE ] - Ponto de Disparo, fazendo login.' + '\n')
                print(Fore.GREEN + "~[ CONSOLE ] - Ponto de Disparo, fazendo login.")
                login()
                break

    principal()