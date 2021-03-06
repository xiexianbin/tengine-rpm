#!/bin/bash

set -eux

# NOTE(xiexianbin): update COPR_PROJECT_NAME、RPM_NAME and COPR_PROJECT_DESCRIPTION.
COPR_PROJECT_NAME="tengine-rpm"
RPM_NAME="tengine"
ARCH="x86_64"
CHROOTS="epel-7"
SPEC_FILE=${RPM_NAME}.spec
MOCK_CHROOTS="${CHROOTS}-${ARCH}"
GITHUB_REPO_URL="https://github.com/xiexianbin/tengine-rpm"
CONTACT="me@xiexianbin.cn"
COPR_PROJECT_DESCRIPTION="Tengine is a web server originated by Taobao, the largest e-commerce website in Asia. It is based on the Nginx HTTP server and has many advanced features. Tengine has proven to be very stable and efficient on some of the top 100 websites in the world, including taobao.com and tmall.com."
COPR_PROJECT_INSTRUCTIONS="\`\`\`
sudo curl -sL -o /etc/yum.repos.d/${COPR_USERNAME}-${COPR_PROJECT_NAME}-${CHROOTS}.repo https://copr.fedorainfracloud.org/coprs/${COPR_USERNAME}/${COPR_PROJECT_NAME}/repo/${CHROOTS}/${COPR_USERNAME}-${COPR_PROJECT_NAME}-${CHROOTS}.repo
\`\`\`

\`\`\`
sudo yum -y install ${RPM_NAME}
\`\`\`"


usage() {
  cat <<'EOF' 1>&2
Usage: 
  build.sh [command]

Available Commands:
  srpm    build srpm package
  mock    build rpm locally with mock
  copr    upload the srpm and build rpm on copr
EOF
}

topdir=`rpm --eval '%{_topdir}'`

download_source_files() {
  source_urls=`rpmspec -P ${topdir}/SPECS/${SPEC_FILE} | awk '/^Source[0-9]*:\s*http/ {print $2}'`
  for source_url in $source_urls; do
    source_file=${source_url##*/}
    (cd ${topdir}/SOURCES && if [ ! -f ${source_file} ]; then curl -sLO ${source_url}; fi)
  done
}

build_srpm() {
  download_source_files

  rpmbuild -bs "${topdir}/SPECS/${SPEC_FILE}"
  version=`rpmspec -P ${topdir}/SPECS/${SPEC_FILE} | awk '$1=="Version:" { print $2 }'`
  release=`rpmspec -P ${topdir}/SPECS/${SPEC_FILE} | awk '$1=="Release:" { print $2 }'`
  srpm_file=${RPM_NAME}-${version}-${release}.src.rpm
}

build_rpm_with_mock() {
  build_srpm
  for mock_chroot in $MOCK_CHROOTS; do
    /usr/bin/mock -r ${mock_chroot} --rebuild ${topdir}/SRPMS/${srpm_file}

    mock_result_dir=/var/lib/mock/${mock_chroot}/result
    if [ -n "`find ${mock_result_dir} -maxdepth 1 -name \"${RPM_NAME}-*${version}-*.${ARCH}.rpm\" -print -quit`" ]; then
      mkdir -p ${topdir}/RPMS/${ARCH}
      cp ${mock_result_dir}/${RPM_NAME}-*${version}-*.${ARCH}.rpm ${topdir}/RPMS/${ARCH}/
    fi
    if [ -n "`find ${mock_result_dir} -maxdepth 1 -name \"${RPM_NAME}-*${version}-*.noarch.rpm\" -print -quit`" ]; then
      mkdir -p ${topdir}/RPMS/noarch
      cp ${mock_result_dir}/${RPM_NAME}-*${version}-*.noarch.rpm ${topdir}/RPMS/noarch/
    fi
  done
}

build_rpm_on_copr() {
  build_srpm

  # Check the project is already created on copr?
  status=`curl -s -o /dev/null -w "%{http_code}" https://copr.fedorainfracloud.org/api/coprs/${COPR_USERNAME}/${COPR_PROJECT_NAME}/detail/`
  if [ $status = "404" ]; then
    # the project is not exist on copr, create it
    chroot_opts=''
    for mock_chroot in $MOCK_CHROOTS; do
      chroot_opts="$chroot_opts --data-urlencode ${mock_chroot}=y"
    done
    curl -s -X POST \
      -u "${COPR_LOGIN}:${COPR_TOKEN}" \
      --data-urlencode "name=${COPR_PROJECT_NAME}" \
      $chroot_opts \
      --data-urlencode "description=${COPR_PROJECT_DESCRIPTION}" \
      --data-urlencode "instructions=${COPR_PROJECT_INSTRUCTIONS}" \
      --data-urlencode "homepage=${GITHUB_REPO_URL}" \
      --data-urlencode "contact=${CONTACT}" \
      --data-urlencode "build_enable_net=y" \
      https://copr.fedorainfracloud.org/api/coprs/${COPR_USERNAME}/new/
  fi
  # uploading a srpm file and create new build form srpm
  chroot_opts=''
  for mock_chroot in $MOCK_CHROOTS; do
    chroot_opts="$chroot_opts -F ${mock_chroot}=y"
  done
  curl -s -X POST \
    -u "${COPR_LOGIN}:${COPR_TOKEN}" \
    -H "Expect:" $chroot_opts \
    -F "pkgs=@${topdir}/SRPMS/${srpm_file};type=application/x-rpm" \
    https://copr.fedorainfracloud.org/api/coprs/${COPR_USERNAME}/${COPR_PROJECT_NAME}/new_build_upload/
}

case "${1:-}" in
srpm)
  build_srpm
  ;;
mock)
  build_rpm_with_mock
  ;;
copr)
  build_rpm_on_copr
  ;;
*)
  usage
  ;;
esac
