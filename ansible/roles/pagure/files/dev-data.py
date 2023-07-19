#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Populate the pagure db with some dev data. """

from __future__ import print_function, unicode_literals, absolute_import

import os
import pygit2

import tests
import pagure
import pagure.lib.model
import pagure.lib.query
from pagure.lib.login import generate_hashed_value

from sqlalchemy.exc import IntegrityError

_config = pagure.config.reload_config()

userslist = []

from fasjson_client import Client
c = Client('http://tinystage.tinystage.test/fasjson', principal='admin@TINYSTAGE.TEST')

def create_projects_git(folder, project):
    repo_path = os.path.join(folder, f'{project}')
    if not os.path.exists(repo_path):
        os.makedirs(repo_path)
    pygit2.init_repository(repo_path, bare=True)

def insert_data(session):
    _config["EMAIL_SEND"] = False
    _config["TESTING"] = True

    userdata = c.list_users().result
    for user in userdata:
        userslist.append(user['username'])
        u = pagure.lib.model.User(
            user=user['username'],
            fullname=user['human_name'],
            password=generate_hashed_value("password"),
            token=None,
            default_email=user['emails'][0],
        )

        try:
            print(f"adding user {user['username']}")
            session.add(u)
            session.commit()
        except IntegrityError:
            session.rollback()

    grouplist = c.list_groups().result

    for group in grouplist:
        g = pagure.lib.model.PagureGroup(
            group_name=group['groupname'],
            group_type="user",
            user_id=1,
            display_name=group['groupname'],
            description=group['description'],
        )
        try:
            print(f"adding group {group['groupname']}")
            session.add(g)
            session.commit()
        except IntegrityError:
            session.rollback()

        members = c.list_group_members(groupname=group['groupname']).result

        for member in members:
            g = pagure.lib.query.search_groups(
                session, pattern=None, group_name=group['groupname'], group_type=None
            )
            u = pagure.lib.query.get_user(
                session, key=member['username']
            )

            try:
                print(f"adding user {member['username']} to group {group['groupname']}")
                session.add(pagure.lib.model.PagureUserGroup(user_id=u.id, group_id=g.id))
                session.commit()
            except IntegrityError:
                session.rollback()

    projects = ['0ad', 'adapta-backgrounds', 'airspyone_host', 'amtk', 'apache-commons', 'apron', 'arptables', 'astromenace', 'autodir', 'ballbuster', 'bengali-typing-booster', 'blam', 'boost-python3', 'buildah', 'calindori', 'ccls', 'cheat', 'clang14', 'clusterssh', 'coin-or-Blis', 'compat-openssl10', 'containers', 'cpupowerutils', 'ctan-cm-lgc-fonts', 'daap-sharp', 'ddiskit', 'desktop-backgrounds', 'diff-pdf', 'django-staticfiles', 'docker-client', 'drehatlas-warender-bibliothek-fonts', 'drupal7-addressfield', 'drupal-cck', 'e16', 'eclipse-m2e-plexus', 'eegdev', 'elmon', 'endless-sky', 'erlang-exometer_core', 'eruby', 'extra-cmake-modules', 'fcgiwrap', 'fedora-messaging', 'ff-utils', 'flat-remix-theme', 'fonts-japanese', 'freetype1', 'fx', 'gap-pkg-grpconst', 'gcombust', 'geeqie', 'gfs-eustace-fonts', 'ghc-bytestring-show', 'ghc-either', 'ghc-hslua', 'ghc-MonadRandom', 'ghc-RSA', 'ghc-turtle', 'gigolo', 'gkrellm-freq', 'glite-lb-types', 'glslang', 'gnome-calendar', 'gnome-phone-manager', 'gnome-shell-theme-smooth-inset', 'gnutls30', 'golang-github-ajstarks-deck', 'golang-github-auth0-go-jwt-middleware', 'golang-github-bugsnag-panicwrap', 'golang-github-cockroachdb-logtags', 'golang-github-datadog-golz4', 'golang-github-dustinkirkland-petname', 'golang-github-fujiwara-shapeio', 'golang-github-golangplus-testing', 'golang-github-h2non-parth', 'golang-github-inconshreveable-go-vhost', 'golang-github-jedisct1-dnsstamps', 'golang-github-krolaw-dhcp4', 'golang-github-martini', 'golang-github-mmarkdown-mmark', 'golang-github-nxadm-tail', 'golang-github-philhofer-fwd', 'golang-github-rakyll-globalconf', 'golang-github-segmentio-kafka', 'golang-github-spf13-viper', 'golang-github-twmb-murmur3', 'golang-github-xtaci-smux', 'golang-gopkg-check-1', 'golang-k8s-component-base', 'golang-uber-zap', 'gpars', 'gr-fcdproplus', 'gstreamer1-plugin-mpg123', 'gtkspell3', 'hackrf', 'HelixPlayer', 'hotssh', 'hunspell-cv', 'hunspell-tr', 'iaxclient', 'ifm', 'inkscape', 'ipxe', 'jackson2-annotations', 'japanese-bitmap-fonts', 'jbosgi-vfs', 'jcharts', 'jfreechart', 'jpanoramamaker', 'js-tag-it', 'kata-runtime', 'kde-partitionmanager', 'keychecker', 'kf5-kross-interpreters', 'kipi-plugins-elegant-theme', 'konquest', 'ktechlab', 'lagan', 'lesstif', 'libcanberra', 'libdnf-plugin-txnupd', 'libgadu', 'libgusb', 'libkdcraw', 'libmicrodns', 'libnss-mysql', 'libpipeline', 'libretro-prosystem', 'libstorj', 'libuv', 'libxmp', 'link-grammar', 'log4c', 'ltsp', 'lv2-fabla', 'macromilter', 'mariadb-galera', 'maven-assembly-plugin', 'mb2md', 'meego-panel-zones', 'miglayout', 'mingw32-physfs', 'mingw-graphene', 'mingw-libxslt', 'mingw-qt5-qtcharts', 'mingw-xz', 'mnemonicsetter', 'mojarra', 'movit', 'mtdev', 'mysql', 'nativejit', 'nested', 'nexcontrol', 'nodejs-after', 'nodejs-atob', 'nodejs-chai-spies-next', 'nodejs-copy-descriptor', 'nodejs-dreamopt', 'nodejs-file-uri-to-path', 'nodejs-grunt-contrib-htmlmin', 'nodejs-invert-kv', 'nodejs-jsonfile', 'nodejs-memwatch-next', 'nodejs-oauth', 'nodejs-pg-escape', 'nodejs-registry-url', 'nodejs-simple-markdown', 'nodejs-svgo', 'nodejs-umask', 'nodejs-zlib-browserify', 'ntp-refclock', 'observable', 'ocamlmod', 'ocfs2-tools', 'ois', 'openct', 'openriichi', 'opensurge', 'os-collect-config', 'pAgenda', 'pari', 'pdf2svg', 'perl-Alien-wxWidgets', 'perl-autobox-Junctions', 'perl-Catalyst-Log-Log4perl', 'perl-CGI-Prototype', 'perl-ColorThemeBase-Static', 'perl-CPANPLUS-Shell-Default-Plugins-RT', 'perl-Data-Float', 'perl-DateTime-TimeZone-SystemV', 'perl-Devel-PatchPerl', 'perl-Encode-Detect', 'perl-File-Edit-Portable', 'perl-GD-SecurityImage', 'perl-Gtk3-WebKit', 'perl-HTTP-Exception', 'perl-IO-Tee', 'perl-Lingua-EN-Tagger', 'perl-Mail-MboxParser', 'perl-Mixin-Linewise', 'perl-Mojolicious-Plugin-OpenAPI', 'perl-MooseX-Types-VariantTable', 'perl-Net-LDAP-Server-Test', 'perl-ORLite-Mirror', 'perl-Perl-Critic-Storable', 'perl-POE-Component-DBIAgent', 'perl-Regexp-Trie', 'perl-Spreadsheet-ParseExcel', 'perl-Syntax-Keyword-MultiSub', 'perl-Test-Abortable', 'perl-Test-Moose-More', 'perl-Text-BibTeX', 'perl-Time-Duration', 'perl-User-Identity', 'perl-XML-Parser', 'pgtoolkit', 'php-channel-symfony2', 'php-ezc-Graph', 'php-horde-horde-lz4', 'php-laminas-cache', 'phpMemcachedAdmin', 'php-pear-crypt-gpg', 'php-pear-Validate-Finance-CreditCard', 'php-phpdocumentor-reflection1', 'php-pragmarx-google2fa5', 'php-seld-phar-utils', 'php-wikimedia-assert', 'php-zmq', 'pixiewps', 'plexus-components-pom', 'polkit-kde', 'ppc64-utils', 'proxychains-ng', 'purple-matrix', 'PyKDE', 'pytc', 'python38', 'python3-lxc', 'python-afsapi', 'python-applicationinsights', 'python-azure-functions-devops-build', 'python-backlash', 'python-bugzilla', 'python-click-default-group', 'python-confluent-kafka', 'python-datadog', 'python-django-dajaxice', 'python-django-uuslug', 'python-epel-rpm-macros', 'python-flask-debugtoolbar', 'python-fypp', 'python-google-cloud-containeranalysis', 'python-hikvision', 'python-invocations', 'python-jupyter-c-kernel', 'python-libcloud', 'python-markups', 'python-mozbase', 'python-neurosynth', 'python-opencensus-proto', 'python-partd', 'python-pluginlib', 'python-pyasn1', 'python-pyls-spyder', 'python-pysmt', 'python-pythonfinder', 'python-repoze-what', 'python-rtslib', 'python-simplejson', 'python-sphinxcontrib-openapi', 'python-steps', 'python-textual', 'python-tw2-jit', 'python-urwid', 'python-webthing-ws', 'python-XStatic-JQuery-Migrate', 'pythran', 'ql2400-firmware', 'qt5-qtscript', 'quake2', 'raidutils', 'R-caTools', 'redir', 'Rex', 'ricci', 'R-munsell', 'rpm2swidtag', 'R-R.rsp', 'rtorrent', 'rubygem-bootstrap-sass', 'rubygem-delayed_job', 'rubygem-gettext', 'rubygem-json_pure', 'rubygem-net-http-persistent', 'rubygem-rack', 'rubygem-rubyforge', 'rubygem-thin', 'R-udunits2', 'rust-asn1', 'rust-box_drawing', 'rust-cint', 'rust-crc-core', 'rust-deflate0.8', 'rust-enum-iterator', 'rust-foreign-types0.3', 'rust-gmp-mpfr-sys', 'rust-hyper-native-tls', 'rust-konst_macro_rules', 'rust-lru_time_cache', 'rust-netlink-packet-route', 'rust-os_display', 'rust-phf_macros0.7', 'rust-progress-streams', 'rust-rav1e', 'rust-rust-embed-impl5.9', 'rust-serial_test_derive', 'rust-stfu8', 'rust-testing_logger', 'rust-tree-sitter-cli', 'rust-utf-8', 'rust-wezterm-color-types', 'rxvt', 'sblim-smis-hba', 'scrot', 'sepostgresql', 'Shinobi', 'simple-scan', 'smb4k', 'sonatype-gossip', 'sphinxbase', 'ssdeep', 'storage-devices', 'sugar-physics', 'sway', 'sysreport', 'tango-icon-theme-extras', 'telegramqml', 'TeXamator', 'tilp_and_gfm', 'tokyotyrant', 'trac-mastertickets-plugin', 'trytond-country', 'txt2man', 'umbrello', 'urlbuster', 'vaspview', 'vim-ansible', 'volk', 'wayvnc', 'wiki2beamer', 'wmwave', 'x2vnc', 'xdvipdfmx', 'xfce4-xfapplet-plugin', 'xmlrpc', 'xorg-x11-drv-i128', 'xplayer', 'xz-java', 'zabbix30']
    namespaces = ['containers', 'modules', 'flatpaks']
    for project in projects:
        thisusername = userslist[int.from_bytes(bytes(project,'utf-8'), byteorder='big') % len(userslist)  ]
        namespace = namespaces[int.from_bytes(bytes(project,'utf-8'), byteorder='big') % len(namespaces) ]
        u = pagure.lib.query.get_user(
            session, key=thisusername
        )

        p = pagure.lib.model.Project(
            user_id=u.id,
            name=project,
            is_fork=False,
            parent_id=None,
            description=f"{project} {namespace}",
            namespace=namespace,
            hook_token=f"{project} {namespace}"
        )
        p.close_status = ["Invalid", "Insufficient data", "Fixed", "Duplicate"]
        try:
            print(f"adding {project} for user {thisusername} in namespace {namespace}")
            session.add(p)
            session.commit()

        except IntegrityError as e:
            session.rollback()

        projectname = os.path.join(namespace, f'{project}.git')
        create_projects_git(_config["GIT_FOLDER"], projectname)

        thegroup = grouplist[int.from_bytes(bytes(project,'utf-8'), byteorder='big') % len(grouplist) ]

        group = pagure.lib.query.search_groups(
             session, pattern=None, group_name=thegroup['groupname'], group_type=None
        )
        repo = pagure.lib.query.get_authorized_project(session, project, namespace=namespace)
        item = pagure.lib.model.ProjectGroup(
        project_id=repo.id, group_id=group.id, access="commit"
        )
        session.add(item)
        session.commit()




        p = pagure.lib.model.Project(
            user_id=u.id,
            name=project,
            is_fork=False,
            parent_id=None,
            description=f"{project} rpm",
            namespace='rpms',
            hook_token=f"{project} rpm"
        )
        p.close_status = ["Invalid", "Insufficient data", "Fixed", "Duplicate"]
        try:
            print(f"adding {project} for user {thisusername} in namespace rpms")
            session.add(p)
            session.commit()
        except IntegrityError as e:
            session.rollback()

        projectname = os.path.join("rpms", f'{project}.git')
        create_projects_git(_config["GIT_FOLDER"], projectname)

        thegroup = grouplist[int.from_bytes(bytes(project,'utf-8'), byteorder='big') % len(grouplist) ]
        group = pagure.lib.query.search_groups(
             session, pattern=None, group_name=thegroup['groupname'], group_type=None
        )
        repo = pagure.lib.query.get_authorized_project(session, project, namespace='rpms')
        item = pagure.lib.model.ProjectGroup(
        project_id=repo.id, group_id=group.id, access="commit"
        )
        session.add(item)
        session.commit()




if __name__ == "__main__":
    session = None
    if not session:
        session = pagure.lib.query.create_session(_config["DB_URL"])

    insert_data(session)
