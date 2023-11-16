import time
from eth_account import Account
from eth_account.signers.local import LocalAccount
from web3 import Web3

w3 = Web3(Web3.HTTPProvider("https://rpc.ankr.com/polygon"))


ascii = """
 ██▓███   ██▀███   ▄████▄         ██▓███   ▒█████   ██▓      ██████                                
▓██░  ██▒▓██ ▒ ██▒▒██▀ ▀█        ▓██░  ██▒▒██▒  ██▒▓██▒    ▒██    ▒                                
▓██░ ██▓▒▓██ ░▄█ ▒▒▓█    ▄       ▓██░ ██▓▒▒██░  ██▒▒██░    ░ ▓██▄                                  
▒██▄█▓▒ ▒▒██▀▀█▄  ▒▓▓▄ ▄██▒      ▒██▄█▓▒ ▒▒██   ██░▒██░      ▒   ██▒                               
▒██▒ ░  ░░██▓ ▒██▒▒ ▓███▀ ░      ▒██▒ ░  ░░ ████▓▒░░██████▒▒██████▒▒                               
▒▓▒░ ░  ░░ ▒▓ ░▒▓░░ ░▒ ▒  ░      ▒▓▒░ ░  ░░ ▒░▒░▒░ ░ ▒░▓  ░▒ ▒▓▒ ▒ ░                               
░▒ ░       ░▒ ░ ▒░  ░  ▒         ░▒ ░       ░ ▒ ▒░ ░ ░ ▒  ░░ ░▒  ░ ░                               
░░         ░░   ░ ░              ░░       ░ ░ ░ ▒    ░ ░   ░  ░  ░                                 
            ░     ░ ░                         ░ ░      ░  ░      ░                                 
                  ░                                                                                
 ███▄ ▄███▓ █    ██  ██▓  ▄▄▄█████▓ ██▓          ███▄ ▄███▓ ██▓ ███▄    █ ▄▄▄█████▓▓█████  ██▀███  
▓██▒▀█▀ ██▒ ██  ▓██▒▓██▒  ▓  ██▒ ▓▒▓██▒         ▓██▒▀█▀ ██▒▓██▒ ██ ▀█   █ ▓  ██▒ ▓▒▓█   ▀ ▓██ ▒ ██▒
▓██    ▓██░▓██  ▒██░▒██░  ▒ ▓██░ ▒░▒██▒         ▓██    ▓██░▒██▒▓██  ▀█ ██▒▒ ▓██░ ▒░▒███   ▓██ ░▄█ ▒
▒██    ▒██ ▓▓█  ░██░▒██░  ░ ▓██▓ ░ ░██░         ▒██    ▒██ ░██░▓██▒  ▐▌██▒░ ▓██▓ ░ ▒▓█  ▄ ▒██▀▀█▄  
▒██▒   ░██▒▒▒█████▓ ░██████▒▒██▒ ░ ░██░         ▒██▒   ░██▒░██░▒██░   ▓██░  ▒██▒ ░ ░▒████▒░██▓ ▒██▒
░ ▒░   ░  ░░▒▓▒ ▒ ▒ ░ ▒░▓  ░▒ ░░   ░▓           ░ ▒░   ░  ░░▓  ░ ▒░   ▒ ▒   ▒ ░░   ░░ ▒░ ░░ ▒▓ ░▒▓░
░  ░      ░░░▒░ ░ ░ ░ ░ ▒  ░  ░     ▒ ░         ░  ░      ░ ▒ ░░ ░░   ░ ▒░    ░     ░ ░  ░  ░▒ ░ ▒░
░      ░    ░░░ ░ ░   ░ ░   ░       ▒ ░         ░      ░    ▒ ░   ░   ░ ░   ░         ░     ░░   ░ 
       ░      ░         ░  ░        ░                  ░    ░           ░             ░  ░   ░     
                                                                                                 
"""
print(ascii)
print("这是由Nya制作的POLS铭文批量铸造工具~")
print("有任何疑问请移步telegram: https://t.me/nyas_lodge")

prk = input("请输入你的私钥：")
num = int(input("请输入你要铸造的数量："))
account: LocalAccount = Account.from_key(prk)
start_nonce = w3.eth.get_transaction_count(account.address)
nonce = start_nonce

def estimate_gas(txn):
            gas = w3.eth.estimate_gas({
                "from": txn['from'],
                "to": txn['to'],
                "value": txn['value'],
                "data": txn['data']
            })
            gas = int(gas + (gas/10)) #increase 10% of the gas
            return gas

def Mint(private_key):
    global account
    global start_nonce
    global nonce 

    transaction = {
        "from": account.address,
        "nonce": nonce,
        # "nonce": nonce,
        "value": 0,
        "gas": 33036,
        "gasPrice": int(w3.eth.gas_price * 1.1),
        "to": account.address,
        "chainId": 137,
        "data": "0x646174613a2c7b2270223a227072632d3230222c226f70223a226d696e74222c227469636b223a22706f6c73222c22616d74223a22313030303030303030227d"
    }


    transaction.update({'gas': int(estimate_gas(transaction))})

    singer = account.sign_transaction(transaction_dict=transaction)

    tx = w3.eth.send_raw_transaction(singer.rawTransaction)
    tx_hash = Web3.to_hex(tx)


    # 检查交易状态
    while True:
        try:
            result = w3.eth.get_transaction_receipt(transaction_hash=tx_hash)
            if result['blockNumber'] is None:
                time.sleep(3)
            elif result['status']:
                print(f"[成功] - https://polygonscan.com/tx/{tx_hash}")
                nonce += 1
                return result['contractAddress']
            else:
                print(f"[失败] -  https://polygonscan.com/tx/{tx_hash}")
                return False
        except:
            time.sleep(2)


if __name__ == '__main__':

    try:
        for i in range(num):
            print("当前铸造的数量：", i+1)
            Mint(prk)
        print("铸造完成，程序即将退出...蟹蟹使用啦！")
        time.sleep(2)

    except Exception as e:
         print("Ooops，出现问题了诶！如果你没法自行解决的话请到telegram联系我叭。")
         print("报错信息如下：")
         print(e)
    input("输入任意键退出，拜拜啦~")
    