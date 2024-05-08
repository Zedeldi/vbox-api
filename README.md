# vbox-api

[![GitHub license](https://img.shields.io/github/license/Zedeldi/vbox-api?style=flat-square)](https://github.com/Zedeldi/vbox-api/blob/master/LICENSE) [![GitHub last commit](https://img.shields.io/github/last-commit/Zedeldi/vbox-api?style=flat-square)](https://github.com/Zedeldi/vbox-api/commits) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)

Python bindings to the VirtualBox SOAP API.

## Description

Provides a Python SOAP client using `zeep` to the VirtualBox SOAP API, with Pythonic bindings, and models for object-oriented usage.

`vbox_api.http` includes a Flask application to view and manage virtual machines over HTTP.

## Installation

After cloning the repository with: `git clone https://github.com/Zedeldi/vbox-api.git`

### Build

1. Install project: `pip install .`
2. Run: `vbox-api-cli` (CLI) or `vbox-api-http` (HTTP)

### Development

1. Install dependencies: `pip install -r requirements.txt`
2. Run: `python -m vbox_api` (CLI) or `python -m vbox_api.http` (HTTP)

Libraries:

- [Zeep](https://pypi.org/project/zeep/) - SOAP client
- [Flask](https://pypi.org/project/Flask/) - HTTP interface
- [Pillow](https://pypi.org/project/pillow/) - image support
- [websockify](https://pypi.org/project/websockify/) - remote control

## License

`vbox-api` is licensed under the [MIT Licence](https://mit-license.org/) for everyone to use, modify and share freely.

This project is distributed in the hope that it will be useful, but without any warranty.

## Donate

If you found this project useful, please consider donating. Any amount is greatly appreciated! Thank you :smiley:

[![PayPal](https://www.paypalobjects.com/webstatic/mktg/Logo/pp-logo-150px.png)](https://paypal.me/ZackDidcott)
