import asyncio
import mitmproxy_wireguard
import wgconfig
import os

directory = os.path.dirname(os.path.abspath(__file__))
confgenpath = os.path.join(directory, "tools", "proton-conf", "proton-confgen.exe")
wgconfpath = os.path.join(directory, "tools", "proton-conf", "protonvpn.conf")
wpconfpath = os.path.join(directory, "tools", "wireproxy", "wireproxy.conf")
wppath = os.path.join(directory, "tools", "wireproxy", "wireproxy.exe")

def pubkey():
    config_path = wgconfpath

    # Load the configuration file
    wc = wgconfig.WGConfig(config_path)
    wc.read_file()

    # Retrieve interface data which contains the PrivateKey
    interface_data = wc.get_interface()
    private_key = interface_data.get("PrivateKey")
    public_key = wc.get_peers()
    return [private_key,public_key]
async def main():
    # Define your WireGuard server parameters in user-space
    # No UAC or Windows network configurations are touched here
    server = await mitmproxy_wireguard.start_server(
        host="0.0.0.0",
        port=51820,                     # The UDP port your WireGuard client will connect to
        private_key=pubkey[0], 
        peer_public_key=pubkey[1],
        
        # Handle the intercepted traffic inside mitmproxy
        handle_connection=lambda connection: print(f"Intercepted connection from: {connection.peer_address}")
    )
    
    print("User-space WireGuard server running on port 51820 without UAC elevation.")
    
    try:
        await asyncio.Event().wait()  # Keep the server running
    finally:
        server.close()

if __name__ == "__main__":
    asyncio.run(main())