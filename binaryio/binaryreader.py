import io

from struct import Struct
from typing import Tuple

from binaryio.seektask import SeekTask
from binaryio.structs import get_struct


class BinaryReader(io.BufferedReader):
    def __init__(self, raw, buffer_size=io.DEFAULT_BUFFER_SIZE, encoding: str = "ascii", endianness: str = "="):
        super().__init__(raw, buffer_size=buffer_size)
        self.encoding = encoding
        self.endianness = endianness

    def __repr__(self):
        return f"{self.__class__} tell()={self.tell()}"

    def _read_value(self, fmt: str):
        """
        Reads a single value of a specified format from the stream.
        Args:
            fmt: The format string for the value to be read from the stream.

        Returns:
            The value read from the stream.
        """
        struct = get_struct(f"{self.endianness}{fmt}")
        return struct.unpack_from(self)[0]

    def _read_values(self, fmt: str, count: int) -> tuple:
        """
        Reads a series of values of a specified format from the stream.
        Args:
            fmt: The format string for the values to be read from the stream.
            count: The number of values to be read from the stream.

        Returns:
            A `tuple` containing the values read from the stream.
        """
        full_format = f"{self.endianness}{count}{fmt}"
        return Struct(full_format).unpack_from(self)

    def align(self, alignment: int) -> None:
        self.seek(-self.tell() % alignment, io.SEEK_CUR)

    def read_byte(self) -> int:
        return self.read(1)[0]

    def read_bytes(self, count: int) -> bytes:
        return self.read(count)

    def read_int16(self) -> int:
        return self._read_value("h")

    def read_int16s(self, count: int) -> Tuple[int]:
        return self._read_values("h", count)

    def read_int32(self) -> int:
        return self._read_value("i")

    def read_int32s(self, count: int) -> Tuple[int]:
        return self._read_values("i", count)

    def read_sbyte(self) -> int:
        return self._read_value("b")

    def read_sbytes(self, count: int) -> Tuple[int]:
        return self._read_values("b", count)

    def read_single(self) -> float:
        return self._read_value("f")

    def read_singles(self, count: int) -> Tuple[float]:
        return self._read_values("f", count)

    def read_0_string(self, encoding: str = None) -> str:
        # This will not work for strings with differently sized characters depending on their code.
        char_size = len("a".encode(encoding or self.encoding))
        str_bytes = bytearray()
        read_bytes = bytearray(self.read(char_size))
        while any(read_bytes):
            str_bytes.append(read_bytes)
            read_bytes = bytearray(self.read(char_size))
        return str_bytes.decode(encoding or self.encoding)

    def read_raw_string(self, length: int, encoding: str = None) -> str:
        return self.read(length).decode(encoding or self.encoding)

    def read_uint16(self) -> int:
        return self._read_value("H")

    def read_uint16s(self, count: int) -> Tuple[int]:
        return self._read_values("H", count)

    def read_uint32(self) -> int:
        return self._read_value("I")

    def read_uint32s(self, count: int) -> Tuple[int]:
        return self._read_values("I", count)

    def read_double(self) -> float:
        return self._read_value("d")

    def read_doubles(self, count: int) -> Tuple(float):
        return self._read_values("d", count)

    def read_length_prefixed_string(self, encoding: str = None) -> str:
        n_bytes = self.read_int16()
        self.read_raw_string(n_bytes, encoding)

    def temporary_seek(self, offset: int = 0, whence=io.SEEK_SET) -> SeekTask:
        return SeekTask(self.raw, offset, whence)
