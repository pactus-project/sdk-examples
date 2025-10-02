use pactus_grpc::blockchain_client::BlockchainClient;
use pactus_grpc::{GetBlockRequest, GetBlockchainInfoRequest};
use pactus_grpc::network_client::NetworkClient;
use pactus_grpc::GetNodeInfoRequest;
use tonic::transport::Channel;

#[tokio::main]
async fn main() {
    println!("Pactus gRPC Examples");
    println!("====================\n");

    // Create gRPC channel
    let channel = Channel::from_static("http://testnet1.pactus.org:50052")
        .connect()
        .await.unwrap();

    // Create gRPC clients
    let mut blockchain_client = BlockchainClient::new(channel.clone());
    let mut network_client = NetworkClient::new(channel);

    // Get blockchain info
    println!("Getting blockchain info...");
    let blockchain_info_request = tonic::Request::new(GetBlockchainInfoRequest {});
    let blockchain_info_response = blockchain_client
        .get_blockchain_info(blockchain_info_request)
        .await.unwrap();
    println!("✅ Blockchain Info:");
    println!("{:#?}", blockchain_info_response.get_ref());
    println!();

    // Get latest block using the blockchain info
    let block_request = tonic::Request::new(GetBlockRequest {
        height: blockchain_info_response.get_ref().last_block_height,
        verbosity: 1,
    });
    let block_response = blockchain_client.get_block(block_request).await.unwrap();
    println!("✅ Latest Block:");
    println!("{:#?}", block_response.get_ref());
    println!();

    // Get node info
    println!("Getting node info...");
    let node_info_request = tonic::Request::new(GetNodeInfoRequest {});

    let node_info_response = network_client.get_node_info(node_info_request).await.unwrap();
    println!("✅ Node Info:");
    println!("{:#?}", node_info_response.get_ref());
    println!();
}

