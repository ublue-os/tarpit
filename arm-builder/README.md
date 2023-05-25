# Deploying via Equinix Metal


1. Boot a c3.large.arm64 in the Washington, DC Datacenter using Ubuntu 22.04 and the contents of `cloud-init.yml` in Optional Settings -> User data
1. SSH into the host, create a Fedora 38 LXC guest with `lxc launch images:fedora/38 build-runner`
1. Exec into the build-runner guest and install the pre-requisites for building fedora-ostree-desktops
    ```sh
    lxc exec build-runner bash
    wget https://gitlab.com/fedora/ostree/buildroot/-/raw/main/coreos-continuous.repo -O /etc/yum.repos.d/coreos-continuous.repo
    wget https://gitlab.com/fedora/ostree/buildroot/-/raw/main/coreos-continuous.gpg -O /etc/pki/rpm-gpg/coreos-continuous.gpg
    dnf -y upgrade
    dnf -y install buildah dbus-daemon file flatpak git-core jq just lorax ostree podman python3-pyyaml rpm-ostree selinux-policy-targeted skopeo tar zstd
    mkdir src
    ```
1. Checkout the ci-test Fedora OSTree project, build and load the image
    ```sh
    cd src
    git clone https://gitlab.com/fedora/ostree/ci-test.git
    cd ci-test
    just compose-image silverblue
    podman load -i fedora-silverblue.ociarchive
    podman tag $(podman image ls -q | head -n1) quay.io/fedora-ostree-desktops/silverblue:38
    cd ..
    ```

1. Checkout the Universal Blue Main project, build the image
    ```sh
    git clone https://github.com/ublue-os/main.git
    cd main
    podman build --build-arg FEDORA_MAJOR_VERSION=38 -f Containerfile -t ublue-os/silverblue:38 .
    ```
