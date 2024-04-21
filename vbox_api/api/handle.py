class Handle(str):
    """Class to store and provide methods to release a handle."""

    def __new__(cls, ctx: "Context", handle: str) -> "Handle":
        """Return new string object."""
        obj = super().__new__(cls, handle)
        obj.ctx = ctx
        return obj

    def release(self) -> None:
        """Release managed object reference."""
        self.ctx.interface.ManagedObjectRef.release(self)
