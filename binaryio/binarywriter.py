import io
import struct

from typing import Iterable


class BinaryWriter(io.BufferedWriter):
    def __init__(self, raw, buffer_size: int=io.DEFAULT_BUFFER_SIZE, endianness: str = ""):
        super().__init__(raw, buffer_size=buffer_size)
        self.endianness = endianness

    def align(self, alignment: int):
        self.seek(-self.tell() % alignment, io.SEEK_CUR)

    def write_0_string(self, value: str, encoding="ascii"):
        self.write_raw_string(value, encoding)
        self.write_byte(0)

    def write_byte(self, value: int):
        self.write(struct.pack("B", value))

    def write_bytes(self, value: bytes):
        self.write(value)

    def write_int32(self, value: int):
        self.write(struct.pack(self.endianness + "i", value))

    def write_int32s(self, value: Iterable[int]):
        self.write(struct.pack(self.endianness + str(len(value)) + "i", *value))

    def write_sbyte(self, value: int):
        self.write(struct.pack(self.endianness + "b", value))

    def write_sbytes(self, value: bytes):
        self.write(struct.pack(self.endianness + str(len(value)) + "b", *value))

    def write_single(self, value: float):
        self.write(struct.pack(self.endianness + "f", value))

    def write_singles(self, value: Iterable[float]):
        self.write(struct.pack(self.endianness + str(len(value)) + "f", *value))

    def write_uint16(self, value: int):
        self.write(struct.pack(self.endianness + "H", value))

    def write_uint16s(self, value: Iterable[int]):
        self.write(struct.pack(self.endianness + str(len(value)) + "H", *value))

    def write_uint32(self, value: int):
        self.write(struct.pack(self.endianness + "I", value))

    def write_uint32s(self, value: Iterable[int]):
        self.write(struct.pack(self.endianness + str(len(value)) + "I", *value))

    def write_raw_string(self, value: str, encoding: str = "ascii"):
        self.write(bytes(value, encoding=encoding))
