import io

from struct import Struct
from typing import Iterable

from binaryio.structs import get_struct


class BinaryWriter(io.BufferedWriter):
    def __init__(self, raw, buffer_size: int=io.DEFAULT_BUFFER_SIZE, encoding: str = "utf-8", endianness: str = ""):
        super().__init__(raw, buffer_size=buffer_size)
        self._default_encoding = encoding
        self._endianness = endianness
        self._structs_cache = {}

    def _write_value(self, fmt: str, value):
        """
        Writes a single value of a specified format to the stream.
        Args:
            fmt: The format string for the value to be written to the stream.
            value: The value to write to the stream.
        """
        struct = get_struct(f"{self._endianness}{fmt}")
        self.write(struct.pack(value))

    def _write_values(self, fmt: str, values: Iterable):
        """
        Writes an iterable of values of the specified format to the stream.
        Args:
            fmt: The format of the values to be written to the stream.
            values: The iterable of values to be written to the stream.
        """
        # This does not use _get_struct because the length of `values` may change frequently so the cache
        # would not be effective.
        full_format = f"{self._endianness}{len(values)}{fmt}"
        self.write(Struct(full_format).pack(*values))

    def align(self, alignment: int):
        self.seek(-self.tell() % alignment, io.SEEK_CUR)

    def write_0_string(self, value: str, encoding: str = None):
        self.write_raw_string(value, encoding)
        self.write_byte(0)

    def write_byte(self, value: int):
        self._write_value("B", value)

    def write_bytes(self, value: bytes):
        self.write(value)

    def write_int32(self, value: int):
        self._write_value("i", value)

    def write_int32s(self, value: Iterable[int]):
        self._write_values("i", value)

    def write_sbyte(self, value: int):
        self._write_value("b", value)

    def write_sbytes(self, value: bytes):
        self._write_values("b", value)

    def write_single(self, value: float):
        self._write_value("f", value)

    def write_singles(self, value: Iterable[float]):
        self._write_values("f", value)

    def write_int16(self, value: int):
        self._write_value("h", value)

    def write_int16s(self, value: Iterable[int]):
        self._write_values("h", value)

    def write_uint16(self, value: int):
        self._write_value("H", value)

    def write_uint16s(self, value: Iterable[int]):
        self._write_values("H", value)

    def write_uint32(self, value: int):
        self._write_value("I", value)

    def write_uint32s(self, value: Iterable[int]):
        self._write_values("I", value)

    def write_raw_string(self, value: str, encoding: str = None):
        self.write(bytes(value, encoding=encoding or self._default_encoding))

    def write_double(self, value: float):
        self._write_value("d", value)

    def write_doubles(self, value: Iterable[float]):
        self._write_values("d", value)

    def write_length_prefixed_string(self, value: str, encoding: str = None):
        bytes_to_write = bytes(value, encoding=encoding or self._default_encoding)
        self.write_int16(len(bytes_to_write))
        self.write(bytes_to_write)
