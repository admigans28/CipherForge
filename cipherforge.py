import base64
import marshal
import zlib
import os

def obfuscate_script(input_path):
    # Periksa apakah file ada
    if not os.path.isfile(input_path):
        print("File tidak ditemukan. Pastikan path benar.")
        return

    # Baca kode Python dari file input
    with open(input_path, "r") as f:
        original_code = f.read()

    # Kompilasi kode menjadi bytecode
    bytecode = compile(original_code, "<string>", "exec")
    
    # Serialize bytecode menggunakan marshal
    serialized_bytecode = marshal.dumps(bytecode)
    
    # Kompresi bytecode
    compressed_bytecode = zlib.compress(serialized_bytecode)
    
    # Encode bytecode ke base64
    encoded_bytecode = base64.b64encode(compressed_bytecode).decode('utf-8')
    
    # Buat kode Python obfuscated
    obfuscated_code = f"""
import base64, marshal, zlib
exec(marshal.loads(zlib.decompress(base64.b64decode('{encoded_bytecode}'))))
"""
    # Tentukan path output file
    output_path = os.path.splitext(input_path)[0] + "_obfuscated.py"

    # Tulis hasil obfuscasi ke file output
    with open(output_path, "w") as f:
        f.write(obfuscated_code)

    print(f"Script berhasil di-obfuscate dan disimpan ke {output_path}")

# Main program
if __name__ == "__main__":
    file_path = input("Enter the path of the Python file to obfuscate: ")
    obfuscate_script(file_path)
