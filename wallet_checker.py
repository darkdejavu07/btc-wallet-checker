import threading
import hashlib
import random, string
import blocksmith
import requests
import contextlib
import os
import time
import json
from rich.console import Console
console = Console()
console.clear()
session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0'})
TOKEN = "TELEGRAM_TOKEN"
chat_id = "CHAT_ID_TELEGRAM"
size = 20 #количество потоков
t = [j for j in range(0, size + 1)]
b = 0
console.print ('[green]Check started[/green]')

def check_balance(address):
	try:
		response = session.get(f'https://btcbook.guarda.co/api/v2/address/{address}')
		if response.content and response.status_code == 200:
			res = response.json()
			return res
		else:
			console.print('[red]Please wait[/red]')
			time.sleep(30)
	except json.JSONDecodeError:
		print('Error decoding JSON response from API')
		
def potok():
	global b, response, tic
	while True:
		hash = ''.join(random.choices('abcdef' + string.digits, k=64))
		address=blocksmith.BitcoinWallet.generate_address(hash)
		resload = check_balance(address)
		if resload:
			balance = resload['balance']
			txs = resload['txs']
			addressinfo = resload['address']
			bal = int(balance)
		if txs > 0 or bal > 0:
			with open("result.txt", "a") as f:
				f.write(f"""\nHash:  {hash}
				Public Address Bitcoin:  {address}
				======================""")
			console.print('[red]Congratulation!!!  Address: [/red]', address, '[green]\tHash: [/green]', hash,'[blue]\tBalance: [/blue]', bal, '\tTXS:', txs)
			url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={str(hash) + '		' + str(address) + '		' + str(bal)}"
			print(requests.get(url).json())
		else:
			b += 1
			console.print('[purple]Total checked: [/purple]', b, '[green]\tHash: [/green]', hash,'[blue]\tAddress: [/blue]', address, '\tBalance: ', balance)
for f in range(1,size):
	t[f] = threading.Thread(target=potok)
	t[f].start()
