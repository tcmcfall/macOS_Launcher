# macOS Launcher for Kodi

**Programs Add-on — Installation & Usage Manual**

---

## 1. Overview

**macOS Launcher** is a Kodi *Programs* add-on designed to integrate native macOS applications into the Kodi interface in a clean and transparent manner.

Its goals are:

- Allow browsing and launching of macOS applications directly from Kodi
- Creation of Kodi Favorites, for inclusion within Kodi menus
- Seamlessly return Kodi to its prior state after an app exits
- Provide rich, configurable artwork without altering original app icons

---

## 2. Supported Platforms

- **macOS only**
- Tested against Kodi Omega (21.3) on macOS Tahoe (26.2) using Python 3
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
   - **Install from zip file** (must be previously enabled)
   - Select the ZIP

The add-on will appear under:

```
Add-ons → Program add-ons → macOS Launcher
```

---

## 4. Add-on Structure

When opened, **macOS Launcher** presents two root-level entries:

```
macOS Applications
Saved Favorites
```

---

## 5. macOS Applications

### 5.1 Purpose

This directory lists all discoverable macOS applications found in standard locations:

- `/Applications`
- `/System/Applications`
- `~/Applications`

Image cache is built on first open of this directory and may take several seconds

---

### 5.2 Artwork Behavior (macOS Applications)

For each application:

- **Icon / Thumb**

  - Uses the app’s **original icon**

- **Poster**

  - Generated automatically
  - Background color = **dominant color extracted from the icon**
  - Foreground = **large, upscaled icon**
  - Soft drop shadow applied to the icon for clarity and definition
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

---

## 6. Saved Favorites

### 6.1 Purpose

**Saved Favorites** is the add-on’s *source of truth* for all configured launchers.

Even though Kodi Favorites are used for menu integration, the add-on **does not depend on Kodi’s favorites list to function**.

---

### 6.2 Hardened Favorites (Critical Feature)

This means that if you:

- Delete a favorite directly from Kodi
- Rename it via skin tools
- Or otherwise modify it outside the add-on

**macOS Launcher will recreate it.**

When **Saved Favorites** is opened:

- Missing Kodi favorites are detected
- They are **silently recreated**
- User configuration and artwork are preserved

This prevents accidental corruption.

**If a favorite was created with macOS Launcher, it must be edited/deleted there as well.**

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

