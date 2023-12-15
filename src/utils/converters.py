from typing import Generator


def bytes_to_generator(file_bytes: bytes) -> Generator[bytes, None, None]:
    """
    Generator to yield bytes content for streaming.
    :param file_bytes: Byte content of a file.
    :yield: Yields chunks of file bytes.
    """
    yield file_bytes
