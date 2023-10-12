from config import Connect
from gecko import Gecko
from web3 import Web3
from db import Database
import requests
import json
import time
import sys
import subprocess
from datetime import datetime

class Main:
    def __init__(self):
        self.connectin = Connect()
        self.db = Database()
        self.gecko = Gecko()
        self.connectin.make_connection()
        bsc = "https://bsc-dataseed.binance.org/"
        self.web3 = Web3(Web3.HTTPProvider(bsc))
        self.menu()
    def menu(self):
        while True:
            balance = self.get_bnb_balance()
            wbnb_balance = self.get_wbnb_balance()
            print('//////////////////////')
            print('Current BNB balance : ',balance,' WBNB balance:', wbnb_balance,'\n')
            print('1.Create new trade 2. Show active trades 3. Change bsc address 4. quit\n')
            cmd = input('Choose comand to execute:')
            if cmd == '1':
                self.create_trade()
    def create_trade(self):
        sender_address = self.db.get_address()[0]
        trades_number = self.db.count_trades()[0][0]
        print('TRADES NUMBER:', trades_number)
        if trades_number>=3:
            print('Too many trades are active, pls close existing trades or w8 for them to finish')
            sys.exit()

    def get_bnb_balance(self):
        balance = self.web3.eth.get_balance(self.db.get_address()[0])
        balance = self.web3.from_wei(balance,'ether')
        return balance
    def get_wbnb_balance(self):
        wbnb_abi = '[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"guy","type":"address"},{"name":"wad","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"src","type":"address"},{"name":"dst","type":"address"},{"name":"wad","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"wad","type":"uint256"}],"name":"withdraw","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"dst","type":"address"},{"name":"wad","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"deposit","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"},{"name":"","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"payable":true,"stateMutability":"payable","type":"fallback"},{"anonymous":false,"inputs":[{"indexed":true,"name":"src","type":"address"},{"indexed":true,"name":"guy","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"src","type":"address"},{"indexed":true,"name":"dst","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"dst","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"src","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Withdrawal","type":"event"}]'
        wbnb_contract = self.web3.eth.contract('0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c', abi=wbnb_abi)
        wbnb_balance = self.web3.from_wei(wbnb_contract.functions.balanceof(self.db.get_address()[0]).call(),'ether')
        return wbnb_balance
    
Main()            