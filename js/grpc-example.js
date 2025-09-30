import grpc from "@grpc/grpc-js";
import blockchain_pb from "pactus-grpc/blockchain_pb.js";
import blockchain_grpc_pb from "pactus-grpc/blockchain_grpc_pb.js";
import network_pb from "pactus-grpc/network_pb.js";
import network_grpc_pb from "pactus-grpc/network_grpc_pb.js";

// Configuration
const GRPC_URL = "testnet1.pactus.org:50051";

console.log("🔗 gRPC Examples");
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
const blockchainInfo = await grpcToPromise(
  blockchainStub,
  "getBlockchainInfo",
  blockchainInfoRequest
);
console.log(
  "✅ Blockchain Info:",
  JSON.stringify(blockchainInfo.toObject(), null, 2)
);
console.log("");

console.log("Getting latest block...");
const getBlockRequest = new blockchain_pb.GetBlockRequest();
getBlockRequest.setHeight(blockchainInfo.getLastBlockHeight());
getBlockRequest.setVerbosity(1);

const latestBlock = await grpcToPromise(
  blockchainStub,
  "getBlock",
  getBlockRequest
);
console.log(
  "✅ Latest Block:",
  JSON.stringify(latestBlock.toObject(), null, 2)
);
console.log("");

console.log("Getting node info...");
const nodeInfoRequest = new network_pb.GetNodeInfoRequest();
const nodeInfo = await grpcToPromise(
  networkStub,
  "getNodeInfo",
  nodeInfoRequest
);
console.log("✅ Node Info:", JSON.stringify(nodeInfo.toObject(), null, 2));
console.log("");
