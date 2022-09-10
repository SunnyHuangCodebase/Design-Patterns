from typing import Callable
import pytest

from patterns.structural.facade.downloader import Client, File, HardDrive, PeerToPeer, Server, ServerToClient, TemporaryFiles


class TestFacade:

  @pytest.fixture
  def file(self):
    return File("File Name", {
        1: b"File Part 1",
        2: b"File Part 2",
        3: b"File Part 3",
        4: b"File Part 4"
    })

  @pytest.fixture
  def temp_files(self, file: File):
    return TemporaryFiles({file.name: file})

  @pytest.fixture
  def empty_temp_files(self):
    return TemporaryFiles({})

  @pytest.fixture
  def hard_drive(self, file: File):
    return HardDrive({file.name: file})

  @pytest.fixture
  def empty_hard_drive(self):
    return HardDrive({})

  @pytest.fixture
  def server(self, hard_drive: HardDrive):
    return Server(hard_drive)

  @pytest.fixture
  def client(self, empty_hard_drive: HardDrive,
             empty_temp_files: TemporaryFiles):
    return Client(empty_hard_drive, empty_temp_files)

  @pytest.fixture
  def peer1(self, hard_drive: HardDrive, temp_files: TemporaryFiles):
    return Client(hard_drive, temp_files)

  @pytest.fixture
  def peer2(self, empty_hard_drive: HardDrive,
            empty_temp_files: TemporaryFiles):
    return Client(empty_hard_drive, empty_temp_files)

  def test_server_download(self, server: Server, client: Client,
                           monkeypatch: pytest.MonkeyPatch):
    """"""
    inputs: list[str] = ["Downloaded File"]
    next_input: Callable[..., str] = lambda _: inputs.pop(0)
    monkeypatch.setattr("builtins.input", next_input)

    transfer = ServerToClient(server, client)
    transfer.download("File Name")
    assert client.has_file("Downloaded File")

  def test_server_stream(self, file: File, server: Server, client: Client):
    transfer = ServerToClient(server, client)
    transfer.stream("File Name")
    assert file in client.temporary_storage.files.values()

  def test_peer_to_peer_download(self, file: File, peer1: Client, peer2: Client,
                                 client: Client,
                                 monkeypatch: pytest.MonkeyPatch):
    """"""
    inputs = ["Downloaded File"]
    next_input: Callable[..., str] = lambda _: inputs.pop(0)
    monkeypatch.setattr("builtins.input", next_input)
    transfer = PeerToPeer([peer1, peer2], client)
    transfer.download("File Name")
    assert peer1.has_file("File Name")
    with pytest.raises(FileNotFoundError):
      peer2.request("File Name")
    assert client.has_file("Downloaded File")

  def test_peer_to_peer_stream(self, file: File, peer1: Client, peer2: Client,
                               client: Client):
    """"""
    transfer = PeerToPeer([peer1, peer2], client)
    transfer.stream("File Name")
    assert file in client.temporary_storage.files.values()


if __name__ == "__main__":
  pytest.main([__file__])
