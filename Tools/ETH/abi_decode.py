import rlp
from web3 import Web3

data = 'f87283aa36a707843b9aca00847735940083030d40946e006ce71555b03de544f984a0ac28a72b528d52843b9aca0080c001a098abbcc6169baaa6491235d0cee189f6ca97b2f70ed5ec05b8c06780112d507da003320b01aadd5ab06e22fa52e03a70e53020e978e089a17368203ac0acbce3e5'
arr = rlp.decode(Web3.to_bytes(hexstr=data))
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


def print_list(i):
    for j in i:
        if j is list:
            print_list(j)
        else:
            if len(j) == 0:
                print('')
            else:
                print(j.hex())


print_list(arr)
