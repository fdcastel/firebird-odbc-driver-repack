#!/usr/bin/env python3
"""
Script to process releases.json and create GitHub releases with installer assets.
"""

import json
import os
import sys
import subprocess
import zipfile
from pathlib import Path
from urllib.request import urlretrieve
import tempfile
import shutil

def run_command(cmd, check=True):
    """Run a shell command and return output."""
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        check=check
    )
    return result.stdout.strip(), result.stderr.strip(), result.returncode

def check_release_exists(version):
    """Check if a GitHub release already exists for the given version."""
    stdout, _, returncode = run_command(
        f'gh release view "v{version}"',
        check=False
    )
    return returncode == 0

def download_and_extract(url, extract_dir):
    """Download a ZIP file and extract its contents."""
    print(f"Downloading {url}...")
    
    # Download to temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as tmp_file:
        tmp_path = tmp_file.name
        urlretrieve(url, tmp_path)
    
    print(f"Extracting to {extract_dir}...")
    
    # Extract ZIP file
    with zipfile.ZipFile(tmp_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
    
    # Clean up temporary file
    os.unlink(tmp_path)
    
    # List extracted files
    extracted_files = list(Path(extract_dir).glob('*.exe'))
    print(f"Extracted files: {[f.name for f in extracted_files]}")
    
    return extracted_files

def create_github_release(version, installer_files):
    """Create a GitHub release and upload installer files."""
    tag = f"v{version}"
    
    print(f"\nCreating release {tag}...")
    
    # Create the release
    cmd = f'gh release create "{tag}" --title "Firebird ODBC Driver {version}" --notes "Firebird ODBC Driver version {version}\n\nThis release contains:\n- Windows x86 (32-bit) installer\n- Windows x64 (64-bit) installer\n\nOriginal distribution repackaged for easier access via GitHub API."'
    
    stdout, stderr, returncode = run_command(cmd, check=False)
    
    if returncode != 0:
        print(f"Error creating release: {stderr}")
        return False
    
    print(f"Release created: {stdout}")
    
    # Upload each installer file as an asset
    for installer_file in installer_files:
        print(f"Uploading {installer_file.name}...")
        cmd = f'gh release upload "{tag}" "{installer_file}"'
        stdout, stderr, returncode = run_command(cmd, check=False)
        
        if returncode != 0:
            print(f"Error uploading {installer_file.name}: {stderr}")
            return False
        
        print(f"Uploaded {installer_file.name}")
    
    return True

def main():
    """Main function to process releases."""
    # Check if gh CLI is available
    stdout, stderr, returncode = run_command('gh --version', check=False)
    if returncode != 0:
        print("Error: GitHub CLI (gh) is not installed or not in PATH")
        sys.exit(1)
    
    print(f"Using GitHub CLI: {stdout.split()[0]} {stdout.split()[2]}")
    
    # Check if GITHUB_TOKEN is set
    if not os.environ.get('GITHUB_TOKEN'):
        print("Error: GITHUB_TOKEN environment variable is not set")
        sys.exit(1)
    
    # Read releases.json
    releases_file = Path('releases.json')
    if not releases_file.exists():
        print("Error: releases.json not found")
        sys.exit(1)
    
    with open(releases_file, 'r') as f:
        releases = json.load(f)
    
    print(f"Found {len(releases)} release(s) in releases.json\n")
    
    # Process each release
    for version, url in releases.items():
        print(f"{'='*60}")
        print(f"Processing version {version}")
        print(f"{'='*60}")
        
        # Check if release already exists
        if check_release_exists(version):
            print(f"Release v{version} already exists, skipping...")
            continue
        
        # Create temporary directory for extraction
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                # Download and extract
                installer_files = download_and_extract(url, temp_dir)
                
                if not installer_files:
                    print(f"Warning: No installer files found for version {version}")
                    continue
                
                # Create GitHub release
                success = create_github_release(version, installer_files)
                
                if success:
                    print(f"✓ Successfully published release v{version}")
                else:
                    print(f"✗ Failed to publish release v{version}")
                    
            except Exception as e:
                print(f"Error processing version {version}: {e}")
                import traceback
                traceback.print_exc()
        
        print()
    
    print("All releases processed.")

if __name__ == '__main__':
    main()
