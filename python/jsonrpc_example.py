#!/usr/bin/env python3
"""
Pactus JSON-RPC Example
=======================

This example demonstrates how to interact with the Pactus blockchain
using the official pactus-jsonrpc Python SDK.
"""

import json
import asyncio
from pactus_jsonrpc.client import PactusOpenRPCClient


async def main():
    print("JSON-RPC Examples")
    print("===================\n")

    # Initialize JSON-RPC client
    client = PactusOpenRPCClient(
        headers={},
        client_url="https://testnet1.pactus.org/jsonrpc"
    )

    print("Getting blockchain info...")
    blockchain_info = await client.pactus.blockchain.get_blockchain_info()
    print("✅ Blockchain Info:")
    print(json.dumps(blockchain_info, indent=2))
    print()

    print("Getting latest block...")
    latest_height = blockchain_info.get("last_block_height", 0)
    latest_block = await client.pactus.blockchain.get_block(latest_height, 1)
    print("✅ Latest Block:")
    print(json.dumps(latest_block, indent=2))
    print()

    print("Getting node info...")
    node_info = await client.pactus.network.get_node_info()
    print("✅ Node Info:")
    print(json.dumps(node_info, indent=2))
    print()


if __name__ == "__main__":
    asyncio.run(main())
