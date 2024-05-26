# Maintainer: Zack Didcott

pkgname=vbox-api-git
pkgver=0.10.0
pkgrel=1
pkgdesc="Python bindings to the VirtualBox SOAP API."
arch=("any")
url="https://github.com/Zedeldi/vbox-api"
license=("MIT")
depends=("python" "gunicorn")
makedepends=("python-build" "python-installer" "python-setuptools" "python-wheel")
provides=("vbox-api")
conflicts=("vbox-api")
source=("${pkgname}::git+https://github.com/Zedeldi/vbox-api.git")
b2sums=("SKIP")

build() {
    cd "${pkgname}"
    python -m build --wheel --no-isolation
}

package() {
    cd "${pkgname}"
    install -Dm644 "deployment/systemd/vbox-api-http.service" "${pkgdir}/usr/lib/systemd/system/vbox-api-http.service"
    install -Dm644 "deployment/config/vbox-api-http.conf" "${pkgdir}/etc/vbox-api-http.conf"
    python -m installer --destdir="${pkgdir}" dist/*.whl
}