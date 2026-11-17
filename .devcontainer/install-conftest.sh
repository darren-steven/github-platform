#!/usr/bin/env bash

set -e

LATEST_VERSION=$(curl -s https://api.github.com/repos/open-policy-agent/conftest/releases/latest \
  | grep '"tag_name"' \
  | sed -E 's/.*"([^"]+)".*/\1/' \
  | cut -c 2-)

wget "https://github.com/open-policy-agent/conftest/releases/download/v${LATEST_VERSION}/conftest_${LATEST_VERSION}_Linux_x86_64.tar.gz"

tar xzf "conftest_${LATEST_VERSION}_Linux_x86_64.tar.gz"

sudo mv conftest /usr/local/bin/

rm -f "conftest_${LATEST_VERSION}_Linux_x86_64.tar.gz"

conftest --version
