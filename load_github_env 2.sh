#!/bin/bash
# Load GitHub credentials from macOS Keychain
export GITHUB_TOKEN=$(security find-generic-password -a "$(whoami)" -s "github-token" -w 2>/dev/null)
export GITHUB_REPO=$(security find-generic-password -a "$(whoami)" -s "github-repo" -w 2>/dev/null || echo "")
