# Firebird ODBC Driver Releases

This repository repackages Firebird ODBC drivers and publishes them as proper GitHub Releases for easier access via the GitHub API.

## Overview

The official Firebird ODBC drivers are distributed as ZIP files containing both x86 and x64 installers. This repository automates the process of extracting and publishing these installers as individual release assets.

## How It Works

1. **releases.json** - Defines the available versions and their download URLs
2. **GitHub Actions Workflow** - Automatically processes each release when `releases.json` is updated
3. **Published Releases** - Each version is published as a GitHub Release with the x86 and x64 installers as separate assets

## Adding a New Release

To add a new release:

1. Edit `releases.json` and add the new version and URL:
   ```json
   {
     "3.0.1.22": "https://github.com/user-attachments/files/xxxxx/win_installers.zip",
     "3.0.1.21": "https://github.com/user-attachments/files/24675532/win_installers.zip",
     ...
   }
   ```

2. Commit and push the changes:
   ```bash
   git add releases.json
   git commit -m "Add Firebird ODBC Driver version 3.0.1.22"
   git push
   ```

3. The GitHub Actions workflow will automatically:
   - Download the ZIP file
   - Extract the x86 and x64 installers
   - Create a new GitHub Release
   - Upload the installers as release assets

## Accessing Releases

### Via GitHub Web Interface

Visit the [Releases page](../../releases) to download installers.

### Via GitHub API

List all releases:
```bash
curl -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/YOUR_USERNAME/firebird-odbc-driver-repack/releases
```

Get a specific release:
```bash
curl -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/YOUR_USERNAME/firebird-odbc-driver-repack/releases/tags/v3.0.1.21
```

## Release Format

Each release includes:
- **Tag**: `v{version}` (e.g., `v3.0.1.21`)
- **Title**: `Firebird ODBC Driver {version}`
- **Assets**:
  - `Firebird_ODBC_{version}_Win32.exe` - 32-bit Windows installer
  - `Firebird_ODBC_{version}_x64.exe` - 64-bit Windows installer

## Manual Trigger

You can also manually trigger the workflow from the [Actions tab](../../actions/workflows/publish-releases.yml) by clicking "Run workflow".

## License

This repository only repackages and redistributes the official Firebird ODBC drivers. Please refer to the original [Firebird ODBC Driver project](https://github.com/FirebirdSQL/firebird-odbc-driver) for license information.
