// Pactus gRPC Example
// ===================
//
// This example demonstrates how to interact with the Pactus blockchain
// using the official pactus-grpc JavaScript SDK.
//

import grpc from "@grpc/grpc-js";
import blockchain_pb from "pactus-grpc/blockchain_pb.js";
import blockchain_grpc_pb from "pactus-grpc/blockchain_grpc_pb.js";
import network_pb from "pactus-grpc/network_pb.js";
import network_grpc_pb from "pactus-grpc/network_grpc_pb.js";

// Configuration
const GRPC_URL = "testnet1.pactus.org:50052";

console.log("gRPC Examples");
console.log("================\n");

// Initialize gRPC clients
const blockchainStub = new blockchain_grpc_pb.BlockchainClient(
  GRPC_URL,
  grpc.credentials.createInsecure()
);
const networkStub = new network_grpc_pb.NetworkClient(
  GRPC_URL,
  grpc.credentials.createInsecure()
);

// Helper function to convert gRPC callback to Promise with timeout
function grpcToPromise(client, method, request) {
  return new Promise((resolve, reject) => {
    client[method](
      request,
      { deadline: new Date(Date.now() + 30000) },
      (error, response) => {
        if (error) {
          reject(error);
        } else {
          resolve(response);
        }
      }
    );
  });
}

console.log("Getting blockchain info...");
const blockchainInfoRequest = new blockchain_pb.GetBlockchainInfoRequest();
const blockchainInfoResponse = await grpcToPromise(
  blockchainStub,
  "getBlockchainInfo",
  blockchainInfoRequest
);
console.log(
  "✅ Blockchain Info:",
  JSON.stringify(blockchainInfoResponse.toObject(), null, 2)
);
console.log("");

console.log("Getting latest block...");
const blockRequest = new blockchain_pb.GetBlockRequest();
blockRequest.setHeight(blockchainInfoResponse.getLastBlockHeight());
blockRequest.setVerbosity(1);

const blockResponse = await grpcToPromise(
  blockchainStub,
  "getBlock",
  blockRequest
);
console.log(
  "✅ Latest Block:",
  JSON.stringify(blockResponse.toObject(), null, 2)
);
console.log("");

console.log("Getting node info...");
const nodeInfoRequest = new network_pb.GetNodeInfoRequest();
const nodeInfoResponse = await grpcToPromise(
  networkStub,
  "getNodeInfo",
  nodeInfoRequest
);
console.log("✅ Node Info:", JSON.stringify(nodeInfoResponse.toObject(), null, 2));
console.log("");
