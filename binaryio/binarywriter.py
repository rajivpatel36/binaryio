import io
import struct


class BinaryWriter:
    def __init__(self, raw):
        self.raw = raw
        self.endianness = "<"  # Little-endian

    def __enter__(self):
        self.writer = io.BufferedWriter(self.raw)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.writer.close()

    def align(self, alignment):
        self.writer.seek(-self.writer.tell() % alignment, io.SEEK_CUR)

    def seek(self, offset, whence=io.SEEK_SET):
        self.writer.seek(offset, whence)

    def tell(self):
        return self.writer.tell()

    def write_0_string(self, value, encoding="ascii"):
        self.write_raw_string(value, encoding)
        self.write_byte(0)

    def write_byte(self, value):
        self.writer.write(struct.pack("B", value))

    def write_bytes(self, value):
        self.writer.write(value)

    def write_int32(self, value):
        self.writer.write(struct.pack(self.endianness + "i", value))

    def write_int32s(self, value):
        self.writer.write(struct.pack(self.endianness + str(len(value)) + "i", *value))

    def write_sbyte(self, value):
        self.writer.write(struct.pack(self.endianness + "b", value))

    def write_sbytes(self, value):
        self.writer.write(struct.pack(self.endianness + str(len(value)) + "b", *value))

    def write_single(self, value):
        self.writer.write(struct.pack(self.endianness + "f", value))

    def write_singles(self, value):
        self.writer.write(struct.pack(self.endianness + str(len(value)) + "f", *value))

    def write_uint16(self, value):
        self.writer.write(struct.pack(self.endianness + "H", value))

    def write_uint16s(self, value):
        self.writer.write(struct.pack(self.endianness + str(len(value)) + "H", *value))

    def write_uint32(self, value):
        self.writer.write(struct.pack(self.endianness + "I", value))

    def write_uint32s(self, value):
        self.writer.write(struct.pack(self.endianness + str(len(value)) + "I", *value))

    def write_raw_string(self, value, encoding="ascii"):
        self.writer.write(bytearray(value, encoding))
