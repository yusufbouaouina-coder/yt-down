import os
import subprocess


def get_active_interface():
    result = subprocess.run(
        ["powershell", "-Command",
         "Get-NetAdapter | Where-Object {$_.Status -eq 'Up'} | Select-Object -First 1 -ExpandProperty Name"],
        capture_output=True, text=True
    )
    interface = result.stdout.strip()
    if not interface:
        raise RuntimeError("Could not detect an active network adapter")
    return interface


def set_dns_or_fallback(interface, primary="1.1.1.1", secondary="1.0.0.1"):
    result = subprocess.run(
        ["powershell", "-Command",
         f"Set-DnsClientServerAddress -InterfaceAlias '{interface}' -ServerAddresses ('{primary}','{secondary}')"],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f"DNS set to {primary}/{secondary} on {interface}.")
        return True
    else:
        print("Automatic DNS change failed — opening network settings for manual fix.")
        os.startfile("ms-settings:network-status")
        return False


def reset_dns(interface):
    subprocess.run(
        ["powershell", "-Command", f"Set-DnsClientServerAddress -InterfaceAlias '{interface}' -ResetServerAddresses"],
        capture_output=True, text=True
    )


def run_confgen(confgenpath, user, passw, wgconfpath):
    """Runs proton-confgen.exe and returns the completed result (doesn't raise on failure)."""
    return subprocess.run([
        confgenpath,
        "-username", user,
        "-password", passw,
        "-countries", "nl",
        "-free-only",
        "-no-save",
        "-duration", "10m",
        "-output", wgconfpath,
    ], capture_output=True, text=True)


def pyvpn(user, passw):
    directory = os.path.dirname(os.path.abspath(__file__))
    confgenpath = os.path.join(directory, "tools", "proton-conf", "proton-confgen.exe")
    wgconfpath = os.path.join(directory, "tools", "proton-conf", "protonvpn.conf")
    wpconfpath = os.path.join(directory, "tools", "wireproxy", "wireproxy.conf")
    wppath = os.path.join(directory, "tools", "wireproxy", "wireproxy.exe")

    try:
        os.remove(wgconfpath)
        os.remove(wpconfpath)
    except FileNotFoundError:
        pass

    result = run_confgen(confgenpath, user, passw, wgconfpath)
    combined_output = result.stdout + result.stderr

    if result.returncode != 0 and ("no such host" in combined_output or "vpn-api.proton.me" in combined_output):
        print("ProtonVPN API unreachable — likely DNS blocking. Attempting automatic fix...")
        interface = get_active_interface()
        dns_fixed = set_dns_or_fallback(interface)

        if dns_fixed:
            # retry now that DNS is fixed
            result = run_confgen(confgenpath, user, passw, wgconfpath)
        else:
            input("Please finish setting DNS manually in the window that opened, then press Enter to retry...")
            result = run_confgen(confgenpath, user, passw, wgconfpath)

        if result.returncode != 0:
            raise RuntimeError(f"Config generation still failing after DNS fix attempt: {result.stderr}")

    elif result.returncode != 0:
        raise RuntimeError(f"Config generation failed: {result.stderr}")

    with open(wpconfpath, "w") as file:
        file.write(f'''
WGConfig = {wgconfpath}

[Socks5]
BindAddress = 127.0.0.1:1080
''')

    global wp_run
    wp_run = subprocess.Popen([
        wppath,
        '-c', wpconfpath],
        creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP)

    with open("creds.txt", "w") as file:
        file.write(f"{user}\n{passw}")

    del user, passw
    return wp_run