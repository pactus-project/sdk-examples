#!/usr/bin/env python3
"""
Pactus gRPC Example
===================

This example demonstrates how to interact with the Pactus blockchain
using the official pactus-grpc Python SDK.
"""

import asyncio
import grpc
from pactus_grpc import blockchain_pb2_grpc, blockchain_pb2, network_pb2_grpc, network_pb2


async def main():
    print("gRPC Examples")
    print("================\n")

    # Initialize gRPC channel
    channel = grpc.aio.insecure_channel("testnet1.pactus.org:50052")

    # Create gRPC stubs
    blockchain_stub = blockchain_pb2_grpc.BlockchainStub(channel)
    network_stub = network_pb2_grpc.NetworkStub(channel)

    print("Getting blockchain info...")
    blockchain_info_request = blockchain_pb2.GetBlockchainInfoRequest()
    blockchain_info_response = await blockchain_stub.GetBlockchainInfo(blockchain_info_request)
    print("✅ Blockchain Info:")
    print(blockchain_info_response)
    print()

    print("Getting latest block...")
    block_request = blockchain_pb2.GetBlockRequest()
    block_request.height = blockchain_info_response.last_block_height
    block_request.verbosity = 1
    block_response = await blockchain_stub.GetBlock(block_request)
    print("✅ Latest Block:")
    print(block_response)
    print()

    print("Getting node info...")
    node_info_request = network_pb2.GetNodeInfoRequest()
    node_info_response = await network_stub.GetNodeInfo(node_info_request)
    print("✅ Node Info:")
    print(node_info_response)
    print()

    # Clean up the channel
    await channel.close()


if __name__ == "__main__":
    asyncio.run(main())
