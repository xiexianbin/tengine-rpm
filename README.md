# tengine-rpm

build taobao [tengine](https://tengine.taobao.org) rpm use [fedorainfracloud copr](https://copr.fedorainfracloud.org/coprs/xiexianbin/tengine-rpm/)

## Usage

```
sudo curl -sL -o /etc/yum.repos.d/xiexianbin-tengine-rpm-epel-7.repo https://copr.fedorainfracloud.org/coprs/xiexianbin/tengine-rpm/repo/epel-7/xiexianbin-tengine-rpm-epel-7.repo

sudo yum -y install tengine
```

## build rpm step

### Help

`make` help info:

```
# make help
help                 Show this help.
build                Build Docker image to build rpm.
bash                 Run /bin/bash in the Docker image to build rpm.
copr                 Run docker image to build rpm and push srpm to copr.
debug                Build Docker image to build rpm and into bash.
```

### Setup

- go to https://copr.fedorainfracloud.org/api/ and save `API TOKEN` to `~/.config/copr`

### Build docker image

```
make build
```

build docker image: `xiexianbin/rpm-builder:latest`

### debug

```
make bash
```

into docker /bin/bash, you can debug rpm packages

### copr

```
make copr
```

auto public 
