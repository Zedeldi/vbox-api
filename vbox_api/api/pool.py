"""Module to provide a mechanism for maintaining a pool of machines."""

from collections.abc import Iterator
from contextlib import contextmanager
from queue import Queue
from typing import Optional
from uuid import uuid4

from vbox_api.models import Machine


class MachinePool(Queue):
    """Class to handle and maintain a pool of machines."""

    def __init__(
        self,
        machine: Machine,
        size: int,
        name: Optional[str] = None,
        group: Optional[list[str]] = None,
    ) -> None:
        """Initialise instance of pool."""
        self.base = machine
        self.name = name or f"{self.base.name} (Pool)"
        self.group = group or [f"/{self.name}"]
        super().__init__(maxsize=size)

    def create_machine(self) -> Machine:
        """Clone machine and add to pool."""
        if self.full():
            raise ValueError("Machine pool has reached maximum size")
        machine_name = uuid4()
        cloned_machine = self.base.clone(machine_name, self.group)
        self.put(cloned_machine)
        return cloned_machine

    def get_machine(self) -> Machine:
        """
        Get machine from the pool.

        The machine will be removed from the queue but not deleted.
        """
        if self.empty():
            self.create_machine()
        return self.get()

    @contextmanager
    def with_machine(self) -> Iterator[Machine]:
        """Yield machine and destroy on close."""
        try:
            machine = self.get_machine()
            yield machine
        finally:
            machine.delete()

    def refresh(self) -> None:
        """Refresh machine pool back to size."""
        while not self.full():
            self.create_machine()

    def delete(self) -> None:
        """Delete all machines in pool."""
        while not self.empty():
            self.get().delete()
