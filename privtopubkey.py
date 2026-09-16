import os
import wgconfig
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
    public_key = public_key[0]
    print(private_key, public_key)
pubkey()