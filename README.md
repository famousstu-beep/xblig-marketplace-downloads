# XBLIG Marketplace downloads

Each title has its own Download button in the Unity Marketplace. The client downloads the selected package, checks its size and SHA-256 checksum, then installs it. Progress, pause, cancel, retry, and installed games are shown in My Downloads. Downloading a game does not open a GitHub page.

These packages are development builds. Bully's full campaign synchronization and several online features are still in development. Publishing a package does not certify that every feature is complete.

## Catalogue sections

- Xbox 360 Full Games
- Xbox Indie Games
- Xbox 360 Arcade
- Original Xbox Games
- Xbox 360 Demos
- Xbox 360 Apps

The original Xbox, Blades, NXE, Kinect, and Metro dashboard entries remain in the Unity client's local dashboard catalogue. Dashboard firmware and account saves are not included in these game downloads.

## Add another game, demo, or app

1. Prepare a ZIP-format `.xbliggame` package for a runtime supported by the Unity client. A catalogue entry alone does not make an arbitrary ISO, Xbox executable, or Windows app compatible.
2. Create its metadata JSON with `id`, `title`, `description`, `developer`, `category`, `contentKind`, `runtimeId`, `executable`, and `contentPath`. IDs must be unique lowercase letters, digits, and hyphens. Content kind is `game`, `demo`, or `application`.
3. Run the supplied `Add-MarketplaceGame.py` with the package, metadata JSON, a local copy of `catalogue.json`, the release download URL, and an output directory. It calculates the sizes/checksums and splits files over 1.5 GB.
4. Upload the generated package files to a GitHub release. Keep its tag and asset filenames identical to the generated URLs. Publish the assets before updating the catalogue.
5. Commit the updated `catalogue.json` to this repository's `main` branch. Existing clients refresh it on startup or through **Add Games → Refresh game catalogue**. A new entry using an existing compatible runtime does not require rebuilding Unity.

Example:

```text
python Add-MarketplaceGame.py my-game.xbliggame --metadata my-game.json --catalogue catalogue.json --release-url https://github.com/famousstu-beep/xblig-marketplace-downloads/releases/download/my-game-v1/ --output upload
```

Bully appears as one title even though its package has three assets. The installer downloads them in order, verifies every part, joins them, and verifies the complete package before installation. Do not rename or install individual `.part` files manually.

Only publish packages you have permission to redistribute. Keep personal saves, login details, keys, and console profiles out of packages. This project does not provide Microsoft Xbox Live authentication.
