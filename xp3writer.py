import zlib
import struct
import hashlib
from io import BytesIO
from structs import XP3FileIndex, XP3IndexSpecialFormat, XP3FileTime, XP3FileAdler, XP3FileSegments, XP3FileInfo, XP3File, \
    XP3FileEntry, XP3Signature, game_list
from encrypt.encrypt_interface import EncryptInterface


class XP3Writer:
    encrypt_instance: EncryptInterface
    game_name: str

    def __init__(self, 
                 buffer: BytesIO = None, 
                 silent: bool = False, 
                 use_numpy: bool = True, 
                 game_name: str = 'none',
                 encrypt_instance: EncryptInterface = None):
        """
        :param buffer: Buffer object to write data to
        :param silent: Supress prints
        :param use_numpy: Use Numpy for XORing if available
        """
        self.encrypt_instance = encrypt_instance
        self.game_name = game_name
        if not buffer:
            buffer = BytesIO()
        self.buffer = buffer
        self.file_entries = []
        self.silent = silent
        self.use_numpy = use_numpy
        buffer.seek(0)
        buffer.write(XP3Signature)
        buffer.write(struct.pack('<Q', 0))  # File index offset placeholder
        self.packed_up = False
        self._filenames = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.packed_up:
            self.pack_up()
        self.buffer.close()

    def add(self, internal_filepath: str, file: bytes, timestamp: int = 0):
        """
        Add a file to the archive
        :param internal_filepath: Internal file path
        :param file: File to add
        :param encryption_type: Encryption type to encrypt with
        :param timestamp: Timestamp (in milliseconds) to save
        """
        if self.packed_up:
            raise Exception('Archive is already packed up')
        if internal_filepath in self._filenames:
            raise FileExistsError

        self._filenames.append(internal_filepath)
        file_entry, file = self._create_file_entry(
            internal_filepath=internal_filepath,
            uncompressed_data=file,
            offset=self.buffer.tell(),
            timestamp=timestamp)
        self.file_entries.append(file_entry)
        if not self.silent:
            print('| Packing {} ({} -> {} bytes)'.format(internal_filepath,
                                                         file_entry.segm.uncompressed_size,
                                                         file_entry.segm.compressed_size))
        self.buffer.write(file)

    def pack_up(self) -> bytes:
        """
        Write the file index to the archive, returns the resulting archive if it can
        (if already packed, just returns the archive)
        """
        if self.packed_up:
            if hasattr(self.buffer, 'getvalue'):
                return self.buffer.getvalue()

        # Write the file index
        file_index = XP3FileIndex.from_entries(self.file_entries).to_bytes()
        file_index_offset = self.buffer.tell()
        self.buffer.write(file_index)

        # Go back to the header and write the offset
        self.buffer.seek(len(XP3Signature))
        self.buffer.write(struct.pack('<Q', file_index_offset))

        # Mark as packed up and return the resulting archive
        self.packed_up = True
        # Flush the buffer explicitly, had a test fail because index was missing
        self.buffer.flush()
        if hasattr(self.buffer, 'getvalue'):
            return self.buffer.getvalue()

    def _create_file_entry(
            self, 
            internal_filepath, 
            uncompressed_data, 
            offset, 
            timestamp: int = 0
        ) -> tuple[XP3FileEntry, bytes]:
        """
        Create a file entry for a file
        :param internal_filepath: Internal file path
        :param uncompressed_data: File to create entry for
        :param offset: Position in the buffer to put into the segment data
        :param encryption_type: Encryption type to use
        :param timestamp Timestamp (in milliseconds)
        :return XP3FileEntry object and compressed or uncompressed file (to write into buffer)
        """
        encryption_type = self.game_name
        adlr = XP3FileAdler.from_data(uncompressed_data)

        is_encrypted = False if encryption_type in ('none', None) else True
        if is_encrypted:
            uncompressed_data = self.encrypt(uncompressed_data, adlr.value, self.use_numpy, self.encrypt_instance)
            _, _, special_index_chunk_name = game_list[encryption_type]
            if special_index_chunk_name:
                special_format = XP3IndexSpecialFormat(adlr.value, internal_filepath, special_index_chunk_name)
                path_hash = hashlib.md5(internal_filepath.lower().encode('utf-16le')).hexdigest()
            else:
                special_format = path_hash = None
        else:
            special_format = path_hash = None

        uncompressed_size = len(uncompressed_data)
        compressed_data = uncompressed_data #zlib.compress(uncompressed_data, level=9)
        compressed_size = len(compressed_data)

        if compressed_size >= uncompressed_size:
            data = uncompressed_data
            compressed_size = uncompressed_size
            is_compressed = False
        else:
            data = compressed_data
            is_compressed = True

        time = XP3FileTime(timestamp)
        info = XP3FileInfo(is_encrypted=is_encrypted,
                           uncompressed_size=uncompressed_size,
                           compressed_size=compressed_size,
                           file_path=internal_filepath if not path_hash else path_hash  ## modified for me, fuck
                           )

        segment = XP3FileSegments.segment(
            is_compressed=is_compressed,
            offset=offset,
            uncompressed_size=uncompressed_size,
            compressed_size=compressed_size
        )
        segm = XP3FileSegments([segment])

        file_entry = XP3FileEntry(special_format=special_format, time=time, adlr=adlr, segm=segm, info=info)

        return file_entry, data

    @staticmethod
    def encrypt(data: bytes, adler32: int, use_numpy: bool, encrypt_instance: EncryptInterface):
        with BytesIO() as buffer:
            buffer.write(data)

            encrypt_instance.encrypt(buffer, adler32, use_numpy)
            return buffer.getvalue()
