%define tengine_home %{_localstatedir}/cache/tengine
%define tengine_user tengine
%define tengine_group tengine
%define tengine_loggroup tengine
%define version 2.3.2

Name:           tengine
Version:        %{version}
Release:        1
Summary:        Tengine is a web server originated by Taobao, the largest e-commerce website in Asia. It is based on the Nginx HTTP server and has many advanced features. Tengine has proven to be very stable and efficient on some of the top 100 websites in the world, including taobao.com and tmall.com.

License:        2-clause BSD-like license
URL:            https://tengine.taobao.org
Source0:        https://tengine.taobao.org/download/tengine-%{version}.tar.gz
Source1:        logrotate
Source2:        %{name}.service
Source3:        %{name}.conf
Source4:        %{name}.vh.default.conf

BuildRequires:  openssl-devel redhat-lsb-core systemd libxslt-devel gd-devel luajit-devel GeoIP-devel unzip pcre-devel zlib-devel perl perl-devel perl-ExtUtils-Embed
Requires:       openssl systemd libxslt gd luajit GeoIP

%description
Tengine is a web server originated by Taobao, the largest e-commerce website in Asia. It is based on the Nginx HTTP server and has many advanced features. Tengine has proven to be very stable and efficient on some of the top 100 websites in the world, including taobao.com and tmall.com.

%package devel
Summary:          Development files for %{name}
Group:            Development/Libraries
Requires:         %{name} = %{version}-%{release}

%description devel
Header and Library files for doing development with the %{name}

%prep
%setup -q -n tengine-%{version}

%build

CFLAGS="$RPM_OPT_FLAGS -Wimplicit-fallthrough=0 -Werror=implicit-fallthrough=0"
CXXFLAGS="$RPM_OPT_FLAGS -Wimplicit-fallthrough=0 -Werror=implicit-fallthrough=0"

# export LUAJIT_LIB="/usr/lib64"
# export LUAJIT_INC="/usr/include/luajit-2.1"

#./configure --help
./configure  --prefix=%{_datadir}/%{name} \
    --with-cc-opt="-Wno-error" \
    --sbin-path=%{_sbindir}/%{name} \
    --conf-path=%{_sysconfdir}/%{name}/%{name}.conf \
    --error-log-path=%{_localstatedir}/log/%{name}/error.log \
    --http-log-path=%{_localstatedir}/log/%{name}/access.log \
    --pid-path=%{_localstatedir}/run/%{name}.pid \
    --lock-path=%{_localstatedir}/run/%{name}.lock \
    --user=%{tengine_user} \
    --group=%{tengine_group} \
    --with-select_module \
    --with-poll_module \
    --with-threads \
    --with-file-aio \
    --with-http_ssl_module \
    --with-http_v2_module \
    --with-http_realip_module \
    --with-http_addition_module \
    --with-http_xslt_module \
    --with-http_image_filter_module \
    --with-http_geoip_module \
    --with-http_sub_module \
    --with-http_dav_module \
    --with-http_flv_module \
    --with-http_mp4_module \
    --with-http_gunzip_module \
    --with-http_gzip_static_module \
    --with-http_auth_request_module \
    --with-http_random_index_module \
    --with-http_secure_link_module \
    --with-http_degradation_module \
    --with-http_slice_module \
    --with-http_stub_status_module \
    --http-client-body-temp-path=%{_localstatedir}/cache/%{name}/client_temp \
    --http-proxy-temp-path=%{_localstatedir}/cache/%{name}/proxy_temp \
    --http-fastcgi-temp-path=%{_localstatedir}/cache/%{name}/fastcgi_temp \
    --http-uwsgi-temp-path=%{_localstatedir}/cache/%{name}/uwsgi_temp \
    --http-scgi-temp-path=%{_localstatedir}/cache/%{name}/scgi_temp \
    --with-mail \
    --with-mail_ssl_module \
    --with-stream \
    --with-stream_ssl_module \
    --with-stream_realip_module \
    --with-stream_geoip_module \
    --with-stream_ssl_preread_module \
    --with-stream_sni

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%make_install

#mkdir -p $RPM_BUILD_ROOT/%{_datadir}/%{name}
#mv $RPM_BUILD_ROOT/usr/html $RPM_BUILD_ROOT/%{_datadir}/%{name}

#INSTALL LOGROTATE CONF FILE
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
%{__install} -m 644 -p %{SOURCE1}  $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/%{name}

#INSTALL SERVICE FILE
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
%{__install} -m644 %{SOURCE2}    $RPM_BUILD_ROOT%{_unitdir}/%{name}.service

#RENAME sbin files to avoid confilicts with original nginx executables.
#mv $RPM_BUILD_ROOT/usr/sbin/nginx  $RPM_BUILD_ROOT/usr/sbin/%{name}
#mv $RPM_BUILD_ROOT/usr/sbin/dso_tool  $RPM_BUILD_ROOT/usr/sbin/%{name}_dso_tool

%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/conf.d
#%{__rm} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/nginx.conf
%{__install} -m 644 -p %{SOURCE3} \
    $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/%{name}.conf
%{__install} -m 644 -p %{SOURCE4} \
    $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/conf.d/default.conf

%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/log/%{name}
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/cache/%{name}

%files
%doc README.markdown CHANGES CHANGES.* LICENSE contrib docs

%{_sysconfdir}/%{name}
%{_sysconfdir}/logrotate.d/%{name}
%{_unitdir}/%{name}.service
%{_sbindir}/*
%{_datadir}/%{name}
# %{_libdir}/%{name}
%{_localstatedir}/log/%{name}
%{_localstatedir}/cache/%{name}

%files devel
%defattr(-,root,root,-)

# %{_includedir}/*

%pre
# Add the "tengine" user
getent group %{tengine_group} >/dev/null || groupadd -r %{tengine_group}
getent passwd %{tengine_user} >/dev/null || \
    useradd -r -g %{tengine_group} -s /sbin/nologin \
    -d %{tengine_home} -c "tengine user"  %{tengine_user}
exit 0

%post
# Register the tengine service
if [ $1 -eq 1 ]; then
    /usr/bin/systemctl preset %{name}.service >/dev/null 2>&1 ||:

    # Touch and set permisions on default log files on installation

    if [ -d %{_localstatedir}/log/tengine ]; then
        if [ ! -e %{_localstatedir}/log/tengine/access.log ]; then
            touch %{_localstatedir}/log/tengine/access.log
            %{__chmod} 640 %{_localstatedir}/log/tengine/access.log
            %{__chown} %{tengine_user}:%{tengine_loggroup} %{_localstatedir}/log/tengine/access.log
        fi

        if [ ! -e %{_localstatedir}/log/tengine/error.log ]; then
            touch %{_localstatedir}/log/tengine/error.log
            %{__chmod} 640 %{_localstatedir}/log/tengine/error.log
            %{__chown} %{tengine_user}:%{tengine_loggroup} %{_localstatedir}/log/tengine/error.log
        fi
    fi
fi

%preun
if [ $1 -eq 0 ]; then
    /usr/bin/systemctl --no-reload disable %{name}.service >/dev/null 2>&1 ||:
    /usr/bin/systemctl stop %{name}.service >/dev/null 2>&1 ||:
fi

%postun
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 ||:

%changelog
* Tue Aug 20 2019 Tengine <rpm@tengine.com> -  2.3.2
- Security: fixed CVE-2019-9511, CVE-2019-9513 and CVE-2019-9516. (wangfakang)
- Feature: added dubbo_pass directive to support the back-end HTTP to Dubbo protocol. (MenqqiWu)
- Feature: added VNSWRR algorithm for upstream module. (wangfakang)
- Feature: support IPv6 for dynamic_resolve module. (wangfakang)
- Change: support dynamic build and add some debug log for proxy_connect module. (chobits)
- Change: updated the code from Nginx-1.17.3 version. (wangfakang)
- Change: updated the health_check module document. (zhangqx2010)
- Change: updated README document. (Lin-Buo-Ren)
- Bugfix: fixed JSON format for health_check module. (IYism)
- Bugfix: ensured 'init_worker_by_lua*' does not mutate another Nginx module's main_conf. (wangfakang)
- Bugfix: fixed compilation error of dyups module compiled with a higher version of OpenSSL. (wangfakang)

* Tue Jun 18 2019 Tengine <rpm@tengine.com> -  2.3.1
- Feature: add $ssl_handshake_time variable for stream ssl module (mrpre)
- Feature: support websocket check of upstream check module (mrpre)
- Change: random index logical for round robin (wangfakang)
- Change: update http lua module to v0.10.14 (mrpre)
- Change: update dyups to master branch of yzprofile/dyups (chobits)
- Change: update core to Nginx-1.16.0 (MenqqiWu)
- Change: support dynamic module for reqstatus (chobits)
- Change: support dynamic build for upstream dynamic module (wangfakang)
- Change: support dynamic build for trim module (wangfakang)
- Change: support dynamic build for footer module (wangfakang)
- Change: support dynamic build for user_agent module (wangfakang)
- Change: support dynamic build for concat module (mathieu-aubin)
- Fix: server version strings in http2 and stream response headers (AstroProfundis)
- Fix: "-m" option to show dynamic module (wangfakang)
- Fix：parameter number check for limit_req directive (wangfakang)
- Fix: fixed compilation error on macOS for reqstatus (chobits)

* Thu Sep 28 2017 Tengine <rpm@tengine.com> -  2.2.3
- fix pipe variable 'ccf' set but not used
