import os
from time import time
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from hashlib import sha256

class CipherForge:
    def __init__(self, content: str, key: str, block_size=16):
        self.content = content
        self.key = sha256(key.encode()).digest()  # Generate 256-bit key
        self.block_size = block_size
        print("Initializing CipherForge Obfuscation...")

    def encrypt(self):
        """Encrypts the script using AES encryption."""
        print("Encrypting script...")
        cipher = AES.new(self.key, AES.MODE_CBC)
        encrypted = cipher.encrypt(pad(self.content.encode(), self.block_size))
        return b64encode(cipher.iv + encrypted).decode()  # Return Base64 encoded output

    def generate_loader(self, encrypted_script):
        """Generates the Python loader for the encrypted script."""
        print("Generating decryption loader...")
        loader = f"""
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from hashlib import sha256

def decrypt_script(key, encrypted):
    key = sha256(key.encode()).digest()
    encrypted = base64.b64decode(encrypted)
    iv = encrypted[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(encrypted[16:]), 16)
    exec(decrypted)

# Provide the same key used for encryption
encryption_key = "{self.key.hex()}"  # Use a hex representation for safety
encrypted_data = "{encrypted_script}"

decrypt_script(encryption_key, encrypted_data)
"""
        return loader

def main():
    print("Welcome to CipherForge Obfuscator!")
    file_path = input("Enter the path of the Python file to obfuscate: ").strip()

    if not os.path.exists(file_path):
        print("Invalid file path. Please try again.")
        return

    with open(file_path, "r") as f:
        original_content = f.read()

    # Encryption key (could be user-provided for more customization)
    encryption_key = input("Enter an encryption key (keep it secret!): ").strip()
    if not encryption_key:
        print("Encryption key cannot be empty.")
        return

    start_time = time()
    forge = CipherForge(content=original_content, key=encryption_key)
    encrypted_script = forge.encrypt()
    loader_script = forge.generate_loader(encrypted_script)
    elapsed_time = round(time() - start_time, 2)

    # Save the encrypted script
    output_dir = "obfuscated_scripts"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"obf-{os.path.basename(file_path)}")
    with open(output_file, "w") as f:
        f.write(loader_script)

    print(f"\nObfuscation completed in {elapsed_time} seconds.")
    print(f"Obfuscated file saved at: {output_file}")


if __name__ == "__main__":
    main()
