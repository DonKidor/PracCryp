import requests
from bs4 import BeautifulSoup
import PySimpleGUI as sg
import threading

headings = ['Coin', 'Price', 'MarketCap']
values = []

col1=[[sg.Button('Download')],[sg.Text('Enter Coin Name:'),sg.InputText(key='-INPUT-')],[sg.Button('Find')]]
col2=[[sg.Table(headings=headings,size=(50,20) ,auto_size_columns=False, key='-TABLE-',col_widths=[30,10,20] ,values=values, justification='left')]]
layout = [[sg.Column(col1,size=(200,100)), sg.Column(col2, size=(600,400))]]

window = sg.Window('Coins', layout, finalize=True)

url = "https://coinmarketcap.com/"
req = requests.get(url)
soup = BeautifulSoup(req.text, 'html.parser')
l=soup.find('table', class_='h7vnx2-2 czTsgW cmc-table').tbody
l=l.findAll('tr')

coins = []
ncoins=[]

stop=False

class Coin:
    def __init__(self, url):
        req = requests.get(url)
        soup = BeautifulSoup(req.text, 'html.parser')
        text = soup.find('h2', class_='sc-1q9q90x-0 jCInrl h1')
        self.name = text.text[:-len(text.findNext().text)]
        self.price = soup.find('div', class_='priceValue').text
        self.marketCap = soup.find('div', class_='statsValue').text

    def __str__(self):
        return self.name + " " + self.price + ", marketCap: " + self.marketCap

def getCoins():
    global l,coins,ncoins
    for i in l:
        if stop: return
        x = i.find('a', class_='cmc-link')
        coin = Coin(url[:-1] + x['href'])
        coins.append(coin)
        print(str(coin))
        ncoins.append([coin.name, coin.price, coin.marketCap])

    coins.sort(key=lambda  x: x.name)
    ncoins.sort(key=lambda x: x[0])

while True:
    event, values = window.read(timeout=1)
    if event == 'Exit' or event == sg.WIN_CLOSED:
        stop=True
        break
    elif event=='Download':
        threading.Thread(target=getCoins).start()
    elif event=='Find':
        val = values['-INPUT-']
        val= val.lower()
        ncoins=[]
        for i in coins:
            if i.name.lower().find(val)>=0:
                ncoins.append([i.name, i.price, i.marketCap])
    window['-TABLE-'].update(ncoins)

window.close()