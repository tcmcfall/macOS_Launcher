# macOS Launcher for Kodi

**Programs Add-on — Installation & Usage Manual**

---

## 1. Overview

**macOS Launcher** is a Kodi *Programs* add-on designed to integrate native macOS applications into the Kodi interface while respecting Kodi’s navigation model, artwork system, and favorites mechanism.

Its goals are:

- Allow browsing and launching of macOS `.app` bundles directly from Kodi
- Seamlessly return Kodi to its prior state after an app exits
- Provide rich, configurable artwork without altering original app icons
- Harden Kodi Favorites so accidental deletion outside the add-on does not break functionality
- Centralize all app launch configuration in one place

The add-on treats **Kodi as the primary UI**, not as something to be exited or replaced.

---

## 2. Supported Platforms

- **macOS only**
- Tested against modern Kodi releases using Python 3
- Requires standard macOS utilities:

  - `open`
  - `osascript`
  - `iconutil`
  - `qlmanage`
  - `sips`

No third-party binaries are required.

---

## 3. Installation

### 3.1 Install the ZIP

1. Download the provided ZIP file:

   ```
   plugin.program.macoslauncher-<version>.zip
   ```

2. In Kodi:

   - **Settings → Add-ons**
   - **Install from zip file**
   - Select the ZIP

The add-on will appear under:

```
Add-ons → Program add-ons → macOS Launcher
```

---

### 3.2 Artwork Caching Note (Important)

Kodi caches add-on icons and thumbnails aggressively.

If the add-on icon or app icons appear incorrect after installation:

1. Quit Kodi
2. Delete:

   ```
   ~/Library/Application Support/Kodi/userdata/Thumbnails/
   ~/Library/Application Support/Kodi/userdata/Database/Textures*.db
   ```

3. Relaunch Kodi

This forces Kodi to reload all artwork.

---

## 4. Add-on Structure

When opened, **macOS Launcher** presents two root-level entries:

```
macOS Applications
Saved Favorites
```

These are always present.

---

## 5. macOS Applications

### 5.1 Purpose

This directory lists all discoverable macOS applications found in standard locations:

- `/Applications`
- `/System/Applications`
- `~/Applications`

Each entry represents a real `.app` bundle on disk.

---

### 5.2 Artwork Behavior (macOS Applications)

For each application:

- **Icon / Thumb**

  - Uses the app’s **original icon**
  - No blur
  - No background fill
  - No compositing
  - No poster logic applied

- **Poster**

  - Generated automatically
  - Background color = **dominant color extracted from the icon**
  - Foreground = **large, upscaled icon**
  - Soft drop shadow applied to the icon
  - Poster generation never modifies the icon itself

- **Fanart**

  - Always uses the bundled `fanart.jpg`
  - Same fanart for all apps and directories

---

### 5.3 Selecting an Application

Selecting an app opens an action dialog:

```
Open application
Create Favorite
Cancel
```

---

### 5.4 Open Application

If selected:

1. User is asked:

   ```
   Minimize Kodi and return on app close?
   ```

2. If **Yes**:

   - Kodi’s fullscreen/windowed state is recorded
   - Kodi is minimized
   - The macOS app is launched
   - After a short delay, the add-on monitors the app process
   - When the app exits:

     - Kodi is reactivated
     - Fullscreen state is restored if necessary

3. If **No**:

   - The app is launched without changing Kodi’s state

This behavior works identically for direct launches and favorites.

---

### 5.5 Create Favorite

Creates a persistent launcher entry with the following behavior:

- A **Kodi Favorite** is automatically created
- A corresponding entry is stored in **Saved Favorites**
- Artwork is initialized using the app’s icon and generated poster
- The minimize/return preference is stored per favorite

You do **not** need to manually add anything to Kodi favorites.

---

## 6. Saved Favorites

### 6.1 Purpose

**Saved Favorites** is the add-on’s *source of truth* for all configured launchers.

Even though Kodi Favorites are used for menu integration, the add-on **does not depend on Kodi’s favorites list to function**.

---

### 6.2 Hardened Favorites (Critical Feature)

If you:

- Delete a favorite directly from Kodi
- Rename it via skin tools
- Or otherwise modify it outside the add-on

**macOS Launcher will not break.**

When **Saved Favorites** is opened:

- Missing Kodi favorites are detected
- They are **silently recreated**
- User configuration and artwork are preserved

This prevents accidental corruption.

---

### 6.3 Saved Favorite Entries

Each entry in **Saved Favorites** behaves like a launcher:

- Selecting it launches the associated app
- Minimize/return behavior is applied
- Artwork is applied as configured

---

### 6.4 Context Menu (Saved Favorites)

Each saved favorite provides a rich context menu:

- **Rename**

  - Changes both the Saved Favorite and Kodi Favorite label

- **Change artwork**

  - Allows selecting a custom image
  - Replaces thumb and poster
  - Kodi favorite thumbnail is updated with cache-busting

- **Clear artwork**

  - Reverts to auto-generated icon + poster

- **Toggle minimize/return**

  - Switches whether Kodi minimizes before launching
  - Automatically updates the Kodi favorite

- **Delete**

  - Removes the Saved Favorite
  - Removes the associated Kodi favorite

All actions are safe and reversible.

---

## 7. Root Directory Artwork

Both root directories support custom artwork:

- **macOS Applications**
- **Saved Favorites**

Via the context menu you can:

- Change artwork
- Clear artwork

Fanart remains `fanart.jpg` regardless.

---

## 8. Kodi Menu Integration

Because the add-on auto-creates Kodi favorites:

- You can add them to:

  - Main menu
  - Submenus
  - Widgets (skin-dependent)

- Some skins may not display all artwork types consistently

  - This is a skin limitation, not an add-on issue

If artwork does not appear immediately:

- Use **cache-busted thumbnails**
- Or refresh Kodi’s texture cache

---

## 9. Icon Reliability

Some macOS apps store icons in non-traditional ways (e.g. asset catalogs).

To maximize success:

- Icon extraction attempts:

  1. `.icns` resolution via `Info.plist`
  2. Asset-based icon resolution
  3. `qlmanage` thumbnail generation

- When selecting an app, artwork is **re-polled** to improve capture reliability

If an icon cannot be extracted by the OS itself, the add-on will fall back gracefully.

---

## 10. What the Add-on Does *Not* Do

- Does **not** modify system files
- Does **not** replace Kodi’s shell behavior
- Does **not** alter app icons themselves
- Does **not** rely on backward compatibility with broken prior versions
- Does **not** require Steam, Big Picture Mode, or game-specific logic

---

## 11. Intended Use Case Summary

**macOS Launcher** is ideal for users who want:

- Kodi as a living-room UI
- Seamless launching of desktop apps
- Clean return behavior
- Consistent artwork
- Protection against accidental menu breakage

It treats macOS applications as **first-class Kodi citizens**, without fighting Kodi’s design.
