#!/usr/bin/env python3
"""
Pactus SDK Example: Fetch and Decode a Block
=============================================

This example demonstrates how to:
1. Connect to the Pactus testnet via JSON-RPC
2. Fetch blockchain info and pick a random block height
3. Retrieve a block and inspect its structure
4. Decode each transaction in the block using pactus-sdk Transaction.decode()

Usage:
    python sdk_example.py
"""

import asyncio
import random

from pactus.transaction import Transaction
from pactus.transaction.payload import PayloadType
from pactus_jsonrpc.client import PactusOpenRPCClient

TESTNET_RPC = "https://testnet1.pactus.org/jsonrpc"


async def get_raw_transaction(client, tx_data):
    """Get the raw unsigned transaction hex for a given transaction from the block."""
    ptype_value = tx_data["payload_type"]
    try:
        ptype = PayloadType(ptype_value)
    except ValueError:
        # Unsupported payload type (e.g. BatchTransfer = 6)
        return None
    payload = tx_data.get("Payload", {})
    fee = int(tx_data.get("fee", 0) or 0)
    memo = tx_data.get("memo", "")

    if ptype == PayloadType.TRANSFER:
        transfer = payload.get("Transfer", payload)
        resp = await client.pactus.transaction.get_raw_transfer_transaction(
            lock_time=tx_data["lock_time"],
            sender=transfer["sender"],
            receiver=transfer["receiver"],
            amount=transfer["amount"],
            fee=fee,
            memo=memo,
        )
        return resp["raw_transaction"]

    elif ptype == PayloadType.BOND:
        bond = payload.get("Bond", payload)
        resp = await client.pactus.transaction.get_raw_bond_transaction(
            lock_time=tx_data["lock_time"],
            sender=bond["sender"],
            receiver=bond["receiver"],
            stake=bond["stake"],
            public_key=bond.get("public_key", ""),
            fee=fee,
            memo=memo,
        )
        return resp["raw_transaction"]

    elif ptype == PayloadType.UNBOND:
        unbond = payload.get("Unbond", payload)
        resp = await client.pactus.transaction.get_raw_unbond_transaction(
            lock_time=tx_data["lock_time"],
            validator_address=unbond["validator"],
            memo=memo,
        )
        return resp["raw_transaction"]

    elif ptype == PayloadType.WITHDRAW:
        withdraw = payload.get("Withdraw", payload)
        resp = await client.pactus.transaction.get_raw_withdraw_transaction(
            lock_time=tx_data["lock_time"],
            validator_address=withdraw["validator"],
            account_address=withdraw["account"],
            amount=withdraw["amount"],
            fee=fee,
            memo=memo,
        )
        return resp["raw_transaction"]

    return None


def decode_and_display(i, tx_data, raw_hex):
    """Decode raw transaction bytes with the SDK and display the result."""
    if raw_hex is None:
        print(f"  [{i}] (no raw data available)")
        return

    raw = bytes.fromhex(raw_hex)
    tx, _ = Transaction.decode(raw)

    ptype = tx.payload.get_type().name
    details = [f"version={tx.version}", f"lock_time={tx.lock_time.value}"]
    if tx.fee.value > 0:
        details.append(f"fee={tx.fee.value}")
    if tx.memo:
        details.append(f"memo='{tx.memo}'")
    if hasattr(tx.payload, "sender"):
        details.append(f"sender={tx.payload.sender.string()[:20]}...")
    if hasattr(tx.payload, "receiver"):
        details.append(f"receiver={tx.payload.receiver.string()[:20]}...")
    if hasattr(tx.payload, "amount"):
        details.append(f"amount={tx.payload.amount.value}")
    if hasattr(tx.payload, "stake"):
        details.append(f"stake={tx.payload.stake.value}")

    print(f"  [{i}] {ptype}: {' | '.join(details)}")


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
    print(f"  Latest height: {latest_height}")

    # 2. Pick a random block height (skip genesis, skip recent to avoid reorgs)
    height = random.randint(10, latest_height - 50)
    print(f"\nFetching block at height {height}...")

    block_data = await client.pactus.blockchain.get_block(height=height, verbosity=2)
    print(f"  Hash:      {block_data['hash']}")
    print(f"  Time:      {block_data['block_time']}")
    print(f"  # Txs:     {len(block_data.get('txs', []))}")

    # 3. Display header
    header = block_data["header"]
    print(f"\nHeader:")
    print(f"  Version:       {header['version']}")
    print(f"  Prev block:    {header['prev_block_hash'][:24]}...")
    print(f"  Proposer:      {header['proposer_address']}")

    # 4. Display previous certificate
    cert = block_data.get("prev_cert")
    if cert:
        committers = len(cert.get("committers", []))
        absentees = len(cert.get("absentees", []))
        print(f"\nPrev Certificate: {committers} committers, {absentees} absentees")

    # 5. Decode each transaction using pactus-sdk
    txs = block_data.get("txs", [])
    print(f"\nTransactions decoded with pactus-sdk ({len(txs)}):")
    for i, tx_data in enumerate(txs, 1):
        tx_id = tx_data["id"][:16]
        raw_hex = await get_raw_transaction(client, tx_data)
        if raw_hex is None:
            print(f"  [{i}] {tx_id}... (unsupported payload type)")
        else:
            decode_and_display(i, tx_data, raw_hex)

    print("\nDone.")


if __name__ == "__main__":
    asyncio.run(fetch_and_decode_block())
