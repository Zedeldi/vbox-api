import functools
from typing import Callable


class PropertyMixin:
    """Mixin to add properties to get getter/setter methods."""

    @property
    def _bound_methods(self) -> dict[str, Callable]:
        """Return dict of bound methods."""
        methods = {}
        for name, method in filter(
            lambda item: callable(item[1]), self.__class__.__dict__.items()
        ):
            try:
                methods[name] = functools.partial(method, getattr(self, name).__self__)
            except AttributeError:
                # Function does not have __self__ attribute, i.e. staticmethod
                methods[name] = method
        return methods

    @property
    def _methods(self) -> dict[str, Callable]:
        """
        Return dict of all callable methods.

        If the method is bound, return a partial function implicitly passing
        the bound object.
        """
        d = {**self.__dict__, **self._bound_methods}
        return {
            method_name: method
            for method_name, method in d.items()
            if callable(method) and not method_name.startswith("_")
        }

    @property
    def _getters(self) -> dict[str, Callable]:
        """Return dict of get methods and their associated property."""
        return self._get_methods_with_prefix("get")

    @property
    def _finders(self) -> dict[str, Callable]:
        """Return dict of find methods and their associated property."""
        return self._get_methods_with_prefix("find")

    @property
    def _setters(self) -> dict[str, Callable]:
        """Return dict of set methods and their associated property."""
        return self._get_methods_with_prefix("set")

    @property
    def _creators(self) -> dict[str, Callable]:
        """Return dict of create methods and their associated property."""
        return self._get_methods_with_prefix("create")

    def _get_methods_with_prefix(self, prefix: str) -> dict[str, Callable]:
        """Return dict of methods with specified prefix."""
        return {
            method_name.removeprefix(prefix).lstrip("_"): method
            for method_name, method in self._methods.items()
            if method_name.startswith(prefix)
        }
