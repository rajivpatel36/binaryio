import io
import struct

from binaryio.seektask import SeekTask


class BinaryReader:
    def __init__(self, raw, encoding: str = "ascii", endianness: str = "="):
        self.raw = raw
        self.encoding = encoding
        self.endianness = endianness

    def __repr__(self):
        return f"{self.__class__} tell()={self.tell()}"

    def align(self, alignment: int) -> None:
        self.raw.seek(-self.raw.tell() % alignment, io.SEEK_CUR)

    def read_byte(self) -> int:
        return self.raw.read(1)[0]

    def read_bytes(self, count: int) -> tuple:
        return self.raw.read(count)

    def read_int16(self) -> int:
        return self._read("h")[0]

    def read_int16s(self, count: int) -> tuple:
        return self._read("h", count)

    def read_int32(self) -> int:
        return self._read("i")[0]

    def read_int32s(self, count: int) -> tuple:
        return self._read("i", count)

    def read_sbyte(self) -> int:
        return self._read("b")[0]

    def read_sbytes(self, count: int) -> tuple:
        return self._read("b", count)

    def read_single(self) -> float:
        return self._read("f")[0]

    def read_singles(self, count: int) -> tuple:
        return self._read("f", count)

    def read_string_0(self, encoding: str = None) -> str:
        # This will not work for strings with differently sized characters depending on their code.
        char_size = len("a".encode(encoding or self.encoding))
        str_bytes = bytearray()
        read_bytes = bytearray(self.raw.read(char_size))
        while any(read_bytes):
            str_bytes += read_bytes
            read_bytes = bytearray(self.raw.read(char_size))
        return str_bytes.decode(encoding or self.encoding)

    def read_string_raw(self, length: int, encoding: str = None) -> str:
        return self.raw.read(length).decode(encoding or self.encoding)

    def read_uint16(self) -> int:
        return self._read("H")[0]

    def read_uint16s(self, count: int) -> tuple:
        return self._read("H", count)

    def read_uint32(self) -> int:
        return self._read("I")[0]

    def read_uint32s(self, count: int) -> tuple:
        return self._read("I", count)

    def tell(self) -> int:
        return self.raw.tell()

    def seek(self, offset: int, whence=io.SEEK_SET) -> None:
        self.raw.seek(offset, whence)

    def temporary_seek(self, offset: int = 0, whence=io.SEEK_SET) -> SeekTask:
        return SeekTask(self.raw, offset, whence)

    def _read(self, fmt: str, count: int = 1) -> tuple:
        fmt = self.endianness + str(count) + fmt
        count = struct.calcsize(fmt)
        value = self.raw.read(count)
        if len(value) < count:
            raise IOError("Could not read enough bytes to parse data.")
        return struct.unpack(fmt, value)
