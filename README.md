# tengine-rpm


## rpmbuild env

```
yum install rpm-build make gcc -y
```

## rpm deps

```
yum install redhat-lsb-core systemd libxslt-devel gd-devel luajit-devel GeoIP-devel unzip pcre-devel zlib-devel perl perl-devel perl-ExtUtils-Embed openssl systemd libxslt gd luajit GeoIP
```

## build

```
rpmbuild

cd ~/rpmbuild/SOURCES
wget http://tengine.taobao.org/download/tengine-2.2.3.tar.gz

cd ~/rpmbuild/SPECS
rpmbuild -ba tengine.spec
```
