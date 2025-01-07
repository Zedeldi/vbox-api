# vbox-api

[![GitHub license](https://img.shields.io/github/license/Zedeldi/vbox-api?style=flat-square)](https://github.com/Zedeldi/vbox-api/blob/master/LICENSE) [![GitHub last commit](https://img.shields.io/github/last-commit/Zedeldi/vbox-api?style=flat-square)](https://github.com/Zedeldi/vbox-api/commits) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)

Python bindings to the VirtualBox SOAP API.

## Table of Contents

- [Description](#description)
  - [Examples](#examples)
  - [Components](#components)
  - [Models](#models)
- [Installation](#installation)
  - [PyPI](#pypi)
  - [Source](#source)
  - [PyInstaller](#pyinstaller)
  - [PKGBUILD](#pkgbuild)
  - [Docker](#docker)
- [Usage](#usage)
  - [Machine](#machine)
  - [Medium](#medium)
- [Libraries](#libraries)
- [Testing](#testing)
- [Contributing](#contributing)
- [Changelog](#changelog)
- [Credits](#credits)
  - [Contributors](#contributors)
  - [Resources](#resources)
  - [Other Projects](#other-projects)
- [License](#license)
- [Donate](#donate)

## Description

Provides a Python SOAP client using `zeep` to the VirtualBox SOAP API, with Pythonic bindings, and models for object-oriented usage.
Several methods have been added to models to assist with common operations, and simplify many interface methods.

### Examples

Command-line interface:

<p align="center">
  <img src="docs/vbox-api-cli.gif?raw=true" alt="Demonstration of vbox-api-cli."/>
</p>

Web (HTTP) interface:

<p align="center">
  <img src="docs/vbox-api-http-machine-view.png?raw=true" alt="Demonstration of vbox-api-http machine.view endpoint."/>
</p>


### Components

`vbox_api.interface` contains all relevant classes to communicate with the VirtualBox API.

`vbox_api.models` defines classes to use an interface in an object-oriented approach (see [below](#models)).

`vbox_api.cli` contains an entry point for an interactive command-line interface and functions to parse arguments.

`vbox_api.http` includes a Flask application to view and manage virtual machines over HTTP.

`vbox_api.constants` defines many enumerations, mostly generated from the VirtualBox WSDL XML, with added enumerations for those not currently specified but used internally, such as `MachineFrontend`.
These can be used as a reference for expected values to/from the VirtualBox interface, when type hinting or passing values.

`vbox_api.helpers` includes a class, `WebSocketProxyProcess`, to wrap `websockify.WebSocketProxy`, allowing remote control of a virtual machine over HTTP, accessible from the web interface.
`vrde_ext_pack` must be set to `VNC` and [noVNC](https://novnc.com) must be available.

### Models

Models allow properties to be obtained and set in an object-oriented fashion, e.g. `machine.name`, instead of `IMachine_getName(handle)`.
To do this, `BaseModel` defines both a `__getattr__` and a `__setattr__` method, which call the relevant interface method for the requested attribute to either get or set, respectively.
Additionally, the `to_dict` and `from_dict` methods allow multiple properties to be handled at once.

Any valid interface name can be used to create a model, using `BaseModel.from_name`.
The interface is passed via a `Context` object, along with the handle of the model.
All methods of the interface are bound to this model, using `functools.partial` to implictly pass its handle, then wrapped to return model instances.
`BaseModel` also implements `__str__`, allowing models to be passed directly to interface methods as a handle.

Models are automatically instantiated from returned results, by obtaining the interface name from the returned handle, using `ManagedObjectRef.get_interface_name`.
Alternatively, a passed value can be matched by string comparison to an existing interface name.

A metaclass is used to ensure that objects with the same handle and class are not recreated; the same object is returned.
The instances are stored in a `WeakValueDictionary`, allowing them to be garbage collected when no longer referenced.

For example:

```py
machine = api.machines[0]
assert machine is Machine(api.ctx, machine.handle)
```

## Installation

### PyPI

1. Install project: `pip install vbox-api-soap`
2. Run: `vbox-api-cli` (CLI) or `vbox-api-http` (HTTP)

As the name `vbox-api` conflicts with official `vboxapi` on PyPI,
`vbox-api-soap` is used as the package name.

### Source

Alternativelty, after cloning the repository with:
`git clone https://github.com/Zedeldi/vbox-api.git`

#### Build

1. Install project: `pip install .`
2. Run: `vbox-api-cli` (CLI) or `vbox-api-http` (HTTP)

#### Development

1. Install dependencies: `pip install -r requirements.txt`
2. Run: `python -m vbox_api.cli` (CLI) or `python -m vbox_api.http` (HTTP)

### PyInstaller

The server application can be bundled with PyInstaller, by adding the required static files and templates for Flask to the bundle.
Additionally, `vbox_api.http.gui` provides a simple wrapper using [flaskwebgui](https://github.com/ClimenteA/flaskwebgui), to serve and open the Flask application in a browser window.

```sh
pyinstaller \
    --name "vbox-api-gui" \
    --add-data "vbox_api/http/static:vbox_api/http/static" \
    --add-data "vbox_api/http/templates:vbox_api/http/templates" \
    --onefile \
    vbox_api/http/gui.py
```

### PKGBUILD

1. Build and install the package: `makepkg -si`
2. Run: `vbox-api-cli` (CLI) or `vbox-api-http` (HTTP)
   - The HTTP interface can also be started using a systemd unit: `systemctl start vbox-api-http`

Note: if the optional dependency `novnc` is installed from the AUR, HTTP remote control will be available out of the box.

### Docker

Dockerfiles are supplied in `docker/`, to run both `vbox-api-http` and `vboxwebsrv` in a container.

If you already have VirtualBox installed to your machine, you can build and start `vbox-api-http` in a Docker container easily.
The VirtualBox container requires the host kernel modules to be installed for `/dev/vboxdrv` to be available.

#### Build

Build vbox-api image, passing current directory as the build context:
```sh
docker build -t "vbox-api" -f docker/api/Dockerfile .
```

Build VirtualBox image, optionally passing additional build arguments:
```sh
docker build -t "virtualbox" -f docker/virtualbox/Dockerfile .
docker build -t "virtualbox" --build-arg USER="user" --build-arg PASS="password" -f docker/virtualbox/Dockerfile .
docker build -t "virtualbox" --build-arg PACMAN_ARGS="--disable-download-timeout" -f docker/virtualbox/Dockerfile .
```

#### Run

Run `vbox-api-http` in a container interactively, with host network:
```sh
docker run -it --rm --network=host "vbox-api"
```

Run `vboxwebsrv` in a container interactively, with host network (note: VirtualBox host kernel modules must be installed):
```sh
docker run -it --rm --network=host --device /dev/vboxdrv:/dev/vboxdrv -e DISPLAY=unix:0 "virtualbox"
```

## Usage

Ensure that `vboxwebsrv` is running as the intended user.
The `virtualbox` package also provides a systemd unit for this: `systemctl start vboxweb`.

In the following examples, `api` refers to a `VBoxAPI` (or `VirtualBox` model) instance.

### Machine

Get machine information:

```py
for machine in api.machines:
    print(machine.to_dict())
```

Wait for machine to start in headless mode:

```py
progress = machine.start(front_end="headless")  # or MachineFrontend.HEADLESS
progress.wait_for_completion(-1)
```

Write-lock machine and set machine name:

```py
with machine.with_lock(save_settings=True) as locked_machine:
    locked_machine.name = "Machine Name"
    # or
    locked_machine.set_name("Machine Name")
assert machine.name == "Machine Name"
```

Create machine with default settings for Windows 11:

```py
machine = api.create_machine_with_defaults(
    name="Windows 11",
    os_type_id="Windows11_64",
)
```

Create machine from Windows 11 ISO and start unattended installation:

```py
machine = api.create_machine_from_iso(
    iso_path="Win11_23H2_EnglishInternational_x64.iso",
    name="Windows 11",
    unattended_options={
        "user": "username",
        "password": "password",
        "install_guest_additions": True,
    },
)
machine.attach_medium(hard_disk)  # See Medium examples
machine.start()
```

Clone machine:

```py
cloned_machine = machine.clone(f"{machine.name} - Clone")
```

Interact with guest OS of machine:

```py
with machine.with_lock() as locked_machine:
    guest = locked_machine.session.console.guest
    session = guest.create_session("username", "password", "domain", "session_name")
    # Wait for session.status to be GuestSessionStatus.STARTED
    progress = session.copy_from_guest(r"C:\path\to\copy", [], FileCopyFlag.NONE, "/path/to/destination/")
    process = session.process_create(r"C:\path\to\file.exe", ["argument"], ["var=1"], ProcessCreateFlag.NONE, 0)
```

Teleport machine to another on the same host, with a password:

```py
# Configure then start target machine
target_machine.teleport_listen(port=6000, password="password")
target_machine.start()

# Start then teleport source machine to target machine
source_machine.start()
source_machine.teleport_to(host="localhost", port=6000, password="password")
```

### Medium

Get medium information:

```py
for medium in api.mediums:  # or specify dvd_images, floppy_images, hard_disks
    print(medium.to_dict())
```

Create hard-disk medium:

```py
medium = api.create_medium_with_defaults(
    location="/path/to/medium.vdi",
    logical_size=1024 ** 4,  # 1 TiB
    format_="VDI",
)
```

## Libraries

- [Zeep](https://pypi.org/project/zeep/) - SOAP client
- [Flask](https://pypi.org/project/Flask/) - HTTP interface
- [Pillow](https://pypi.org/project/pillow/) - image support
- [psutil](https://pypi.org/project/psutil/) - process information
- [websockify](https://pypi.org/project/websockify/) - remote control

## Testing

`vbox-api` has been tested successfully on Arch Linux and Windows 10.

Unit tests can be run using [pytest](https://pypi.org/project/pytest/), though tests require authentication for the VirtualBox interface: `python -m pytest`

## Contributing

Please contribute by raising an [issue](https://github.com/Zedeldi/vbox-api/issues) or submitting a [pull request](https://github.com/Zedeldi/vbox-api/pulls), whether for code or documentation.

Source code is formatted using [black](https://pypi.org/project/black/), and type hints should be added where possible.

If there are any questions, please do not hesitate to ask.
All contributions are welcome!

## Changelog

For VirtualBox `v7.1.0` onwards (released 09/09/2024), use `v2.0.0` or above of `vbox-api`.
`v7.1.0` was a major update, causing some breaking changes with their API, specifically with the introduction of `PlatformProperties`.

For previous versions of VirtualBox, use `v1.5.3` or below.

For more information, see the [VirtualBox Changelog](https://www.virtualbox.org/wiki/Changelog).

## Credits

### Contributors

 - [@Zedeldi](https://github.com/Zedeldi) - creator & maintainer

### Resources

 - [VirtualBox](https://www.virtualbox.org/) - well, duh.
   - [API Documentation](https://www.virtualbox.org/sdkref/) - reference for interface methods and properties
 - [Bootstrap](https://getbootstrap.com/) - used for HTTP interface
 - [noVNC](https://novnc.com)/[websockify](https://github.com/novnc/websockify) - support for HTTP remote control
 - See [libraries](#libraries) for list of dependencies

### Other Projects

 - [vboxwebber](https://github.com/larshson/vboxwebber/) - VirtualBox SOAP API client for Python
 - [phpVirtualBox](https://github.com/phpvirtualbox/phpvirtualbox) - web interface to manage and access Virtualbox machines
 - [RemoteBox](https://remotebox.knobgoblin.org.uk/) - VirtualBox GUI (GTK3) client

## License

`vbox-api` is licensed under the [MIT Licence](https://mit-license.org/) for everyone to use, modify and share freely.

This project is distributed in the hope that it will be useful, but without any warranty.

The VirtualBox logo is licensed under the [GPL-2.0](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html).

## Donate

If you found this project useful, please consider donating. Any amount is greatly appreciated! Thank you :smiley:

[![PayPal](https://www.paypalobjects.com/webstatic/mktg/Logo/pp-logo-150px.png)](https://paypal.me/ZackDidcott)
