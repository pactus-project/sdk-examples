#!/usr/bin/env python3
"""
Pactus SDK Example: Fetch and Decode a Block
=============================================

This example demonstrates how to:
1. Connect to the Pactus testnet via JSON-RPC
2. Fetch blockchain info and pick a random block height
3. Retrieve a block and inspect its structure
4. Decode raw transaction bytes using the pactus-sdk Transaction decoder

Usage:
    python sdk_example.py
"""

import asyncio
import random

from pactus.block import Block
from pactus.transaction import Transaction
from pactus.transaction.payload import PayloadType
from pactus_jsonrpc.client import PactusOpenRPCClient

TESTNET_RPC = "https://testnet1.pactus.org/jsonrpc"


async def fetch_and_decode_block():
    client = PactusOpenRPCClient(
        headers={},
        timeout=30,
        client_url=TESTNET_RPC,
    )

    # 1. Get blockchain info
    print("Connecting to Pactus testnet...")
    info = await client.pactus.blockchain.get_blockchain_info()
    latest_height = info["last_block_height"]
    print(f"  Network: {info.get('network', 'testnet')}")
    print(f"  Latest height: {latest_height}")

    # 2. Pick a random block height (avoid genesis)
    height = random.randint(1, latest_height - 1)
    print(f"\nFetching block at height {height}...")

    block_data = await client.pactus.blockchain.get_block(height=height, verbosity=2)
    print(f"  Hash: {block_data['hash']}")
    print(f"  Time: {block_data['block_time']}")
    print(f"  Transactions: {len(block_data.get('txs', []))}")

    # 3. Inspect block header
    header = block_data["header"]
    print(f"\nHeader:")
    print(f"  Version: {header['version']}")
    print(f"  Previous block: {header['prev_block_hash']}")
    print(f"  State root: {header['state_root']}")
    print(f"  Proposer: {header['proposer_address']}")

    # 4. Inspect previous certificate
    cert = block_data.get("prev_cert")
    if cert:
        print(f"\nPrevious Certificate:")
        print(f"  Hash: {cert['hash']}")
        print(f"  Committers: {len(cert['committers'])}")

    # 5. Show transaction details
    print(f"\nTransactions ({len(block_data.get('txs', []))}):")
    for i, tx_data in enumerate(block_data.get("txs", []), 1):
        ptype = PayloadType(tx_data["payload_type"]).name if "payload_type" in tx_data else "?"
        print(f"  {i}. {tx_data['id'][:16]}...  lock_time={tx_data.get('lock_time','?')}  type={ptype}")
        if "value" in tx_data:
            print(f"     value={tx_data['value']} nanoPAC")

    # 6. Demonstrate SDK Transaction.decode() with a known raw transaction
    #    (Transfer tx from Pactus testnet, verified on-chain)
    raw_tx_hex = (
        "000124a3230080ade2040b77616c6c65742d636f726501"
        "037098338e0b6808119dfd4457ab806b9c2059b89b"
        "037a14ae24533816e7faaa6ed28fcdde8e55a7df21"
        "8084af5f"
        "4ed8fee3d8992e82660dd05bbe8608fc56ceabffdeeee61e3213b9b49d33a0fc"
        "8dea6d79ee7ec60f66433f189ed9b3c50b2ad6fa004e26790ee736693eda8506"
        "95794161374b22c696dabb98e93f6ca9300b22f3b904921fbf560bb72145f4fa"
    )
    raw = bytes.fromhex(raw_tx_hex)
    tx, _ = Transaction.decode(raw)

    print(f"\n--- SDK Decode Demo ---")
    print(f"Decoded transaction from raw hex:")
    print(f"  Version:     {tx.version}")
    print(f"  Lock time:   {tx.lock_time.value}")
    print(f"  Fee:         {tx.fee.value} nanoPAC")
    print(f"  Memo:        {tx.memo}")
    print(f"  Payload:     {tx.payload.get_type().name}")
    print(f"  Sender:      {tx.payload.sender.string()}")
    print(f"  Receiver:    {tx.payload.receiver.string()}")
    print(f"  Amount:      {tx.payload.amount.value} nanoPAC")
    print(f"  TxID:        {str(tx.id())}")
    print(f"  Signature:   {'present' if tx.signature else 'missing'}")
    print(f"  Public key:  {'present' if tx.public_key else 'missing'}")

    print("\nDone.")


if __name__ == "__main__":
    asyncio.run(fetch_and_decode_block())
