#!/usr/bin/env bash
set -euo pipefail

# Stage only tracked package inputs so RPM never receives local caches or settings.
# The temporary tree also prevents generated version metadata from changing Git files.
project_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
package_revision=${PACKAGE_REVISION:-1}
build_root="$project_root/build/rpm/rpmbuild"
staging_root=$(mktemp -d)
trap 'rm -rf "$staging_root"' EXIT

cd "$project_root"
version=$(python3 -c 'import tomllib; print(tomllib.load(open("pyproject.toml", "rb"))["project"]["version"])')
rm -rf "$build_root"
mkdir -p "$build_root"/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}

source_root="$staging_root/bwcsv-$version"
mkdir -p "$source_root/src/bwcsv/assets" \
    "$source_root/data/icons/hicolor/512x512/apps" \
    "$source_root/docs/images" "$source_root/examples"
cp pyproject.toml README.md CHANGELOG.md LICENSE.md MANIFEST.in "$source_root/"
cp src/freeze_entry.py "$source_root/src/"
cp src/bwcsv/*.py src/bwcsv/mainwindow.ui "$source_root/src/bwcsv/"
cp src/bwcsv/assets/*.png "$source_root/src/bwcsv/assets/"
cp data/org.bulkware.bwcsv.desktop data/org.bulkware.bwcsv.metainfo.xml "$source_root/data/"
cp data/icons/hicolor/512x512/apps/org.bulkware.bwcsv.png \
    "$source_root/data/icons/hicolor/512x512/apps/"
cp docs/*.md docs/*.txt "$source_root/docs/"
cp docs/images/*.png "$source_root/docs/images/"
cp examples/*.csv "$source_root/examples/"
tar -czf "$build_root/SOURCES/bwcsv-$version.tar.gz" \
    -C "$staging_root" "bwcsv-$version"

spec_stage="$staging_root/bwcsv.spec"
cp packaging/rpm/bwcsv.spec "$spec_stage"
python3 scripts/package_metadata.py --rpm-spec "$spec_stage" --revision "$package_revision"

rpmbuild --define "_topdir $build_root" -ba "$spec_stage"
