import rlp
from web3 import Web3

## chainId
## nonce
## value
## maxFeePerGas
## gasLimit
## to
## maxPriorityFeePerGas
## v
## r
## s

data_list = []


def decode(i):
    for j in i:
        if j is list:
            decode(j)
        else:
            if len(j) == 0:
                data_list.append('')
            else:
                data_list.append(j.hex())


if __name__ == "__main__":
    raw = 'f87283aa36a707843b9aca00847735940083030d40946e006ce71555b03de544f984a0ac28a72b528d52843b9aca0080c001a098abbcc6169baaa6491235d0cee189f6ca97b2f70ed5ec05b8c06780112d507da003320b01aadd5ab06e22fa52e03a70e53020e978e089a17368203ac0acbce3e5'
    decode(rlp.decode(Web3.to_bytes(hexstr=raw)))
    print("chainId:".ljust(30), data_list[0])
    print("nonce:".ljust(30), data_list[1])
    print("value:".ljust(30), data_list[2])
    print("maxFeePerGas:".ljust(30), data_list[3])
    print("gasLimit:".ljust(30), data_list[4])
    print("to:".ljust(30), data_list[5])
    print("maxPriorityFeePerGas:".ljust(30), data_list[6])
    print("method1:", data_list[7])
    print("method2:", data_list[8])
    print("v:".ljust(30), data_list[9])
    print("r:".ljust(30), data_list[10])
    print("s:".ljust(30), data_list[11])
