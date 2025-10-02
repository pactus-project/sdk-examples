use jsonrpsee::http_client::HttpClient;
use pactus_jsonrpc::pactus::PactusOpenRPC;

#[tokio::main]
async fn main() {
    println!("Pactus JSON-RPC Examples");
    println!("========================\n");

    // Create JSON-RPC client
        let client = HttpClient::builder().build("https://testnet1.pactus.org/jsonrpc").unwrap();
	let rpc: PactusOpenRPC<HttpClient> = PactusOpenRPC::new(client);

    // Get blockchain info
    println!("Getting blockchain info...");
    let blockchain_info = rpc.pactus_blockchain_get_blockchain_info().await.unwrap();
    println!("✅ Blockchain Info:");
    println!("{}", serde_json::to_string_pretty(&blockchain_info).unwrap());
    println!();

    // Get latest block
    println!("Getting latest block...");
    let block = rpc.pactus_blockchain_get_block(blockchain_info.last_block_height, 1).await.unwrap();
    println!("✅ Latest Block:");
    println!("{}", serde_json::to_string_pretty(&block).unwrap());
    println!();

    // Get node info
    println!("Getting node info...");
    let node_info = rpc.pactus_network_get_node_info().await.unwrap();
    println!("✅ Node Info:");
    println!("{}", serde_json::to_string_pretty(&node_info).unwrap());
    println!();
}
