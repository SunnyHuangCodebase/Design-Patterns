from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
import random


@dataclass
class File:
  name: str
  data: dict[int, bytes]


@dataclass
class Storage(ABC):
  """Data storage."""
  files: dict[str, File]

  def read(self, file_name: str) -> File:
    """Reads a file from storage."""
    return self.files[file_name]

  def write(self, file_name: str, file: File):
    """Writes a file to storage."""
    if not self.files.get(file_name, None):
      self.files[file_name] = file


class TemporaryFiles(Storage):
  """Temporary file storage for streaming."""


class HardDrive(Storage):
  """Persistent file storage."""


class Host(ABC):
  """File host."""
  storage: Storage

  def has_file(self, file_name: str) -> bool:
    return file_name in self.storage.files

  def request(self, file_name: str) -> File:
    """Returns a file from the server"""

    if self.has_file(file_name):
      return self.storage.read(file_name)

    else:
      raise FileNotFoundError


@dataclass
class Server(Host):
  """A dedicated file host."""
  storage: HardDrive


@dataclass
class Client(Host):
  storage: HardDrive
  temporary_storage: TemporaryFiles
  """A computer capable of transmitting/receiving data in a network."""


class FileTransfer(ABC):
  """A file transfer system using the facade design pattern."""

  @abstractmethod
  def download(self, requested_file: str):
    """Store files in persistent storage."""

  @abstractmethod
  def stream(self, requested_file: str):
    """Store and access files from temporary storage."""


@dataclass
class ServerToClient(FileTransfer):
  """Exchange files between a server and a client."""
  server: Server
  client: Client

  def download(self, requested_file: str):
    """Store files in persistent storage."""
    file = self.server.request(requested_file)
    file_name = input("Save file as:")
    self.client.storage.write(file_name, file)

  def stream(self, requested_file: str):
    """Store and access files from temporary storage."""
    file = self.server.request(requested_file)
    file_name = str(random.randint(1, 1_000_000))
    self.client.temporary_storage.write(file_name, file)


@dataclass
class PeerToPeer(FileTransfer):
  """Exchange files between clients in a network."""
  network: list[Client]
  client: Client

  def available_peers(self, requested_file: str) -> list[Client]:
    return [peer for peer in self.network if peer.has_file(requested_file)]

  def download(self, requested_file: str):
    """Store files in persistent storage."""
    peers = self.available_peers(requested_file)
    peer = random.choice(peers)
    file = peer.request(requested_file)
    file_name = input("Save file as:")
    self.client.storage.write(file_name, file)

  def stream(self, requested_file: str):
    """Store and access files from temporary storage."""
    peers = self.available_peers(requested_file)
    peer = random.choice(peers)
    file = peer.request(requested_file)
    file_name = str(random.randint(1, 1_000_000))
    self.client.temporary_storage.write(file_name, file)
