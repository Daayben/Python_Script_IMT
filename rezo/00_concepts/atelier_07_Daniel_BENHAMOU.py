import struct

OCTETS = b"\x00\x00\x00\x2A"

big_endian    = struct.unpack(">I", OCTETS)[0]
little_endian = struct.unpack("<I", OCTETS)[0]
inverse_big   = struct.unpack(">I", OCTETS[::-1])[0]

print(f"Big-endian    : {big_endian}")
print(f"Little-endian : {little_endian}")
print(f"Inversé + BE  : {inverse_big}")

assert little_endian == inverse_big, "les valeurs 2 et 3 devraient être identiques"
print("Les valeurs 2 et 3 sont bien identiques.")

# Pourquoi ? Lire en little-endian = lire en big-endian les octets inversés.
# Les deux opérations produisent donc toujours le même résultat.
