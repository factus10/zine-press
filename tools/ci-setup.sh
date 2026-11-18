#!/bin/sh
# CI (ubuntu-24.04): what make.sh needs besides the runner's Google Chrome.
# Pandoc is a pinned release (Ubuntu's is too old), so the PDFs don't change
# with the runner image.
set -e
PANDOC=3.5
curl -fsSL --retry 3 -o /tmp/pandoc.deb \
  "https://github.com/jgm/pandoc/releases/download/$PANDOC/pandoc-$PANDOC-1-amd64.deb"
sudo dpkg -i /tmp/pandoc.deb
python3 -m pip install --quiet --user --break-system-packages pypdf pyyaml fonttools
pandoc --version | head -1
google-chrome --version
