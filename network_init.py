import asyncio
from miner import Miner
from servers import BootstrapServer


def main():
    i = 5
    peers = [Miner.Peer("1270.0.0.1", 8880 + x) for x in range(0,i)]
    miners = [Miner("127.0.0.1", 8880 + x, str(x), peers, pow(10, 6)) for x in range(0,i)]
    bootserver = BootstrapServer.boot(peers)
