# SecureVaultX

A local-first, encrypted notes vault built with Kivy for Android.

## Features
- Master-password-protected vault
- Random data-encryption key (DEK), wrapped by the master password
- Recovery key generated during first-time setup
- AES-256-GCM authenticated encryption for note contents
- Scrypt key derivation for password-based key wrapping
- SQLite storage in Kivy's private application data directory
- Obsidian/graphite skeuomorphic interface
- Automatic lock when the app is paused/backgrounded

## Project layout
See the requested `core/`, `screens/`, `ui/`, and `assets/` package layout.

## Run locally
Use Python 3.10+ in a virtual environment:

```bash
pip install -r requirements.txt
python main.py
```

## Build Android APK (Linux)
Install Buildozer and its system dependencies, then:

```bash
buildozer android debug
```

The first Android build downloads the Android toolchain and may take a while. The generated APK is normally placed in `bin/`.

## Important security notes
- Save the recovery key outside the phone. It is not stored in plaintext by the app.
- Losing both the master password and recovery key means the encrypted notes cannot be recovered.
- This initial version stores note titles and bodies together as encrypted JSON blobs.
- The database is stored in the app-private data directory, but this project does not yet implement cloud sync, biometric unlock, secure backup/export, or password change.
- Android screenshots/keyboard behavior and the Android build must be tested on a real device before release.
