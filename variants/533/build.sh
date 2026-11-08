#!/usr/bin/env bash
# Rebuild the CII XSLT of validation-1.3.17 for BASE, V1 and V2 with the official
# upstream chain (Maven + ph-schematron-maven-plugin 10.2.0, pom-preprocess.xml then
# pom-xslt-preprocessed.xml, as in update-xslt-and-validate.sh). The licence-header
# step (pom-license.xml) is skipped: it only adds a 5-line comment.
# Needs git, Java 17 and Maven 3.9. Usage: variants/533/build.sh <work-dir>
set -euo pipefail

TAG=validation-1.3.17
COMMIT=d0dea7300c2ad60d50af4a4f31e122fdbf7c0ed3
HERE="$(cd "$(dirname "$0")" && pwd)"
WORK="${1:?usage: build.sh <work-dir>}"
MVN="${MVN:-mvn}"

mkdir -p "$WORK"
if [ ! -d "$WORK/upstream" ]; then
  git clone -q --depth 1 --branch "$TAG" https://github.com/ConnectingEurope/eInvoicing-EN16931.git "$WORK/upstream"
fi
test "$(git -C "$WORK/upstream" rev-parse HEAD)" = "$COMMIT"

for v in BASE V1 V2; do
  rm -rf "$WORK/$v"
  cp -R "$WORK/upstream" "$WORK/$v"
  if [ "$v" != BASE ]; then
    python3 "$HERE/patch_sources.py" "$WORK/$v" "$v"
    git -C "$WORK/$v" diff > "$HERE/patches/$v.patch"
  fi
  (cd "$WORK/$v" \
    && "$MVN" -q -B -f pom-preprocess.xml generate-resources \
    && "$MVN" -q -B -f pom-xslt-preprocessed.xml process-resources)
  mkdir -p "$HERE/xslt/$v"
  cp "$WORK/$v/cii/xslt/EN16931-CII-validation-preprocessed.xslt" "$HERE/xslt/$v/EN16931-CII-validation.xslt"
done
(cd "$HERE/xslt" && shasum -a 256 */EN16931-CII-validation.xslt > SHA256SUMS)
cat "$HERE/xslt/SHA256SUMS"
