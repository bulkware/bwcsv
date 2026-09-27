# This template is copied and versioned by scripts/package_metadata.py before
# rpmbuild runs, keeping release automation from modifying tracked inputs.
Name:           bwcsv
Version:        1.5.0
Release:        1%{?dist}
Summary:        Lightweight desktop application for viewing CSV files

License:        GPL-3.0-or-later
URL:            https://github.com/bulkware/bwcsv
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-pyside6
BuildRequires:  python3-setuptools
BuildRequires:  pyproject-rpm-macros
BuildRequires:  desktop-file-utils
BuildRequires:  appstream
Requires:       python3-pyside6

%description
bwCSV displays comma-separated value files in a searchable table and lets users
select delimiters and table headers.

%prep
%autosetup

%build
%pyproject_wheel

%check
PYTHONPATH=src %{python3} -m unittest discover -s tests -v

%install
%pyproject_install
install -D -m 644 data/org.bulkware.bwcsv.desktop \
    %{buildroot}%{_datadir}/applications/org.bulkware.bwcsv.desktop
install -D -m 644 data/org.bulkware.bwcsv.metainfo.xml \
    %{buildroot}%{_metainfodir}/org.bulkware.bwcsv.metainfo.xml
install -D -m 644 data/icons/hicolor/512x512/apps/org.bulkware.bwcsv.png \
    %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/org.bulkware.bwcsv.png

%files
%license LICENSE.md
%doc CHANGELOG.md README.md
%{_bindir}/bwcsv
%{python3_sitelib}/bwcsv
%{python3_sitelib}/bwcsv-*.dist-info
%{_datadir}/applications/org.bulkware.bwcsv.desktop
%{_metainfodir}/org.bulkware.bwcsv.metainfo.xml
%{_datadir}/icons/hicolor/512x512/apps/org.bulkware.bwcsv.png

%changelog
* Wed Sep 23 2026 Antti-Pekka Meronen <antice@kapsi.fi> - 1.5.0-1
- Packaging system for Debian (deb) and Red Hat (rpm) based distros.
