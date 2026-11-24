# XBLIG Marketplace downloads

## Download the Marketplace client

The **r2 client is a Unity release build**. Development Build, script debugging and profiler connection are off, and there is no Development Build watermark.

**[Download Marketplace for Windows x64](https://github.com/famousstu-beep/xblig-marketplace-downloads/releases/download/marketplace-client-2026-11-24/XBLIG-Marketplace-Windows-x64-20261124-r2.zip)**

Extract the entire ZIP and run `Marketplace.exe`. You do not need the Unity Editor. Select a category, choose a game and press **Download**; once installed, press **Play**.

The shared client downloads all five currently published games: **End Of Days Infected Vs Mercs**, **Avatar Paintball**, **1 vs 100**, **Bully: Scholarship Edition**, and **20 Games to Play With Your Mates**. Bully's three package parts are handled automatically; allow at least **9 GB free** for its download and installation.

All five public packages passed a fresh download and installation check on 24 November 2026, including checksums, extraction and Bully’s split package. This verifies installation; gameplay limitations are listed below.

Windows x64 and the current [Microsoft Visual C++ x64 Redistributable](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist) are required. [Release notes, instructions and SHA-256 checksum](https://github.com/famousstu-beep/xblig-marketplace-downloads/releases/tag/marketplace-client-2026-11-24). The game catalogue refreshes at startup, or use **Add Games → Refresh game catalogue**.

Each title has its own Download button in the Unity Marketplace. The client downloads the selected package, checks its size and SHA-256 checksum, then installs it. Progress, pause, cancel, retry, and installed games are shown in My Downloads. Downloading a game does not open a GitHub page.

Game features have separate limitations. Bully's full campaign synchronization and several online features are still in development. Publishing a package does not certify that every feature is complete.

## 20 Games to Play With Your Mates

Use the Marketplace client above and open **Xbox Indie Games → 20 Games to Play With Your Mates → Download**. [Game package and original release notes](https://github.com/famousstu-beep/xblig-marketplace-downloads/releases/tag/twenty-games-2026-11-24).

This client adds the `twenty-games` runtime, the original menus and all 20 minigames, solo/local play, PUN online parties, and the Marketplace guide. Older clients need this client update before installing the separate `.xbliggame` package. The shared client includes the graphics fixes for Astro Pods and Not My Brains!

Host an online party and share its room code. Up to four people can join, each controlling their own character in the original shared-screen game. Individual minigame limits are unchanged; Sumo and Fruits allow two players. Press **Home**, or hold **Menu**, to open the guide and use **Return to game** to continue.

All 20 minigames passed loading and simulation checks. Separate two-client and four-client Unity/PUN runs compared gameplay state across processes. These checks are not exhaustive playthroughs of every rule and outcome. Download checksums are included in the release.

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
