import pytest

from io import BytesIO

from binaryio.binaryreader import BinaryReader
from binaryio.binarywriter import BinaryWriter


def test_strings():
    buffer = BytesIO()

    writer = BinaryWriter(buffer)
    raw_string = "raw_string"
    zero_string = "zero_string"
    length_prefixed_string = "length_prefixed_string"

    # Write some strings to buffer
    writer.write_raw_string(raw_string)
    writer.write_0_string(zero_string)
    writer.write_length_prefixed_string(length_prefixed_string)

    # Flush so it is actually written to buffer
    writer.flush()

    # Reset buffer to start
    buffer.seek(0)

    # Attempt to read strings and check they are what we expect
    reader = BinaryReader(buffer)
    assert reader.read_raw_string(len(raw_string)) == raw_string, "Error reading/writing raw string."
    assert reader.read_0_string() == zero_string, "Error reading/writing zero string"
    assert reader.read_length_prefixed_string() == length_prefixed_string, "Error reading/writing length-prefixed string."


def test_ints_happy_day():
    int_16 = -12345
    int_16s = [-12345, 10, 23456]
    int_32 = -123456789
    int_32s = [-123456789, 11, 234567890]
    int_64 = -1234567891234567
    int_64s = [-1234567891234567, 11, 23456788901234567]
    uint_16 = 12345
    uint_16s = [10, 12345, 23456]
    uint_32 = 123456789
    uint_32s = [11, 123456789, 234567890]
    uint_64 = 123456678901234567
    uint_64s = [11, 12345678901234567, 2345678901234567]

    buffer = BytesIO()

    # Write some integers to buffer
    writer = BinaryWriter(buffer)
    writer.write_int16(int_16)
    writer.write_int16s(int_16s)
    writer.write_int32(int_32)
    writer.write_int32s(int_32s)
    writer.write_int64(int_64)
    writer.write_int64s(int_64s)
    writer.write_uint16(uint_16)
    writer.write_uint16s(uint_16s)
    writer.write_uint32(uint_32)
    writer.write_uint32s(uint_32s)
    writer.write_uint64(uint_64)
    writer.write_uint64s(uint_64s)

    # Flush so it actually gets written to buffer
    writer.flush()

    # Reset buffer to start
    buffer.seek(0)

    # Attempt to read ints and check they are what we expect
    reader = BinaryReader(buffer)
    assert reader.read_int16() == int_16, "Error reading/writing int16"
    assert reader.read_int16s(len(int_16s)) == tuple(int_16s), "Error reading/writing int16s"
    assert reader.read_int32() == int_32, "Error reading/writing int32"
    assert reader.read_int32s(len(int_32s)) == tuple(int_32s), "Error reading/writing int32s"
    assert reader.read_int64() == int_64, "Error reading/writing int64"
    assert reader.read_int64s(len(int_64s)) == tuple(int_64s), "Error reading/writing int64s"
    assert reader.read_uint16() == uint_16, "Error reading/writing uint16"
    assert reader.read_uint16s(len(uint_16s)) == tuple(uint_16s), "Error reading/writing uint16s"
    assert reader.read_uint32() == uint_32, "Error reading/writing uint32"
    assert reader.read_uint32s(len(uint_32s)) == tuple(uint_32s), "Error reading/writing uint32s"
    assert reader.read_uint64() == uint_64, "Error reading/writing uint64"
    assert reader.read_uint64s(len(uint_64s)) == tuple(uint_64s), "Error reading/writing uint64s"


def test_floats():
    single = 3.14159
    singles = [3.14159, -6.14578]

    double = 12345.6789123
    doubles = [12345.6789123, -78976547.543321]

    buffer = BytesIO()

    writer = BinaryWriter(buffer)
    writer.write_single(single)
    writer.write_singles(singles)
    writer.write_double(double)
    writer.write_doubles(doubles)

    writer.flush()

    buffer.seek(0)

    reader = BinaryReader(buffer)
    assert reader.read_single() == pytest.approx(single), "Error reading/writing single."
    assert reader.read_singles(len(singles)) == pytest.approx(tuple(singles)), "Error reading/writing singles."
    assert reader.read_double() == pytest.approx(double), "Error reading/writing double."
    assert reader.read_doubles(len(doubles)) == pytest.approx(doubles), "Error reading/writing doubles."


def test_bytes():
    byte = 7
    byte_array = [1, 2, 3, 4, 5]

    signed_byte = -7
    signed_byte_array = [-1, -2, -3, -4, -5]

    buffer = BytesIO()

    writer = BinaryWriter(buffer)
    writer.write_byte(byte)
    writer.write_bytes(bytes(byte_array))
    writer.write_sbyte(signed_byte)
    writer.write_sbytes(signed_byte_array)

    writer.flush()

    buffer.seek(0)

    reader = BinaryReader(buffer)
    assert reader.read_byte() == byte, "Error reading/writing byte."
    assert reader.read_bytes(len(byte_array)) == bytes(byte_array), "Error reading/writing bytes"
    assert reader.read_sbyte() == signed_byte, "Error reading/writing sbyte"
    assert reader.read_sbytes(len(signed_byte_array)) == tuple(signed_byte_array), "Error reading/writing sbytes"


def test_seek():
    seek = 111

    buffer = BytesIO()

    writer = BinaryWriter(buffer)
    writer.seek(seek)
    assert writer.tell() == seek, "Error seeking."
    writer.write_int16(5)

    writer.flush()

    reader = BinaryReader(buffer)
    reader.seek(seek)
    assert reader.tell() == seek, "Error seeking."
    assert reader.read_int16() == 5, "Error seeking or reading/writing int16."


def test_seek_task():
    seek = 111

    buffer = BytesIO()

    writer = BinaryWriter(buffer)
    writer.seek(seek)
    writer.write_int16(5)

    writer.flush()

    reader = BinaryReader(buffer)
    reader.seek(1)
    with reader.temporary_seek(seek):
        assert reader.tell() == 111, "Error seeking with temporary seek."
        assert reader.read_int16() == 5, "Error seeking with temporary seek or reading/writing int16"

    assert reader.tell() == 1, "Error exiting temporary seek. Didn't reset to previous position."
