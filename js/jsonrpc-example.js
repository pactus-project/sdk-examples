// Pactus JSON-RPC Example
// ===================
//
// This example demonstrates how to interact with the Pactus blockchain
// using the official pactus-jsonrpc JavaScript SDK.
//

import PactusOpenRPC from "pactus-jsonrpc";

console.log("📡 JSON-RPC Examples");
console.log("===================\n");

// Initialize JSON-RPC client with timeout
const jsonrpcClient = new PactusOpenRPC({
  transport: {
    type: "https",
    host: "testnet1.pactus.org/jsonrpc",
    timeout: 30000, // 30 seconds timeout
  },
});

console.log("Getting blockchain info...");
const blockchainInfo = await jsonrpcClient.pactusBlockchainGetBlockchainInfo();
console.log("✅ Blockchain Info:", JSON.stringify(blockchainInfo, null, 2));
console.log("");

console.log("Getting latest block...");
const latestBlock = await jsonrpcClient.pactusBlockchainGetBlock(
  blockchainInfo.last_block_height,
  1
);
console.log("✅ Latest Block:", JSON.stringify(latestBlock, null, 2));
console.log("");

console.log("Getting node info...");
const nodeInfo = await jsonrpcClient.pactusNetworkGetNodeInfo();
console.log("✅ Node Info:", JSON.stringify(nodeInfo, null, 2));
console.log("");
