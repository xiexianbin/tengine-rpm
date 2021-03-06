# Create by xiexianbin, For build rpm for copr.fedorainfracloud.org 
# v1.0.0

# base image 
FROM centos:7

# labels 
LABEL maintainer="me@xiexianbin.cn"

# Dockerfile build cache 
ENV REFRESHED_AT 2021-03-06
ENV BUILD_USER builder

# build env
RUN yum -y install rpm-build rpmdevtools sudo mock patch make vim \
    && yum clean all \
    && useradd -G mock ${BUILD_USER} \
    && echo '${BUILD_USER} ALL=(ALL) NOPASSWD: ALL' > /etc/sudoers.d/${BUILD_USER}

USER ${BUILD_USER}
RUN rpmdev-setuptree
WORKDIR /home/${BUILD_USER}/rpmbuild
ADD SPECS/ ./SPECS/
ADD SOURCES/ ./SOURCES/
ADD build.sh ./

USER root
RUN chown -R ${BUILD_USER}:${BUILD_USER} . && chmod +x ./*.sh

USER ${BUILD_USER}
CMD ["./build.sh", "copr"]
