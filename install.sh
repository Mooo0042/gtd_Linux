#!/bin/bash

# Installationsverzeichnis
INSTALL_DIR="$HOME/.local/share/gtd"

# .desktop-Datei
DESKTOP_FILE="$HOME/.local/share/applications/gtd.desktop"

# Icon-Verzeichnis
ICON_DIR="$HOME/.local/share/icons/hicolor/512x512/apps"

# Erstelle das Installationsverzeichnis
mkdir -p "$INSTALL_DIR"

# Erstelle das Icon-Verzeichnis
mkdir -p "$ICON_DIR"

# Kopiere die ausführbare Datei
cp dist/gtd_test "$INSTALL_DIR/gtd"
cp scores.txt "$INSTALL_DIR/scores.txt"

# Kopiere das Icon
cp door.png "$ICON_DIR/gtd.png"

# Erstelle die .desktop-Datei
cat <<EOF > "$DESKTOP_FILE"
[Desktop Entry]
Name=Guess the Door
Exec="$INSTALL_DIR/gtd"
Icon=gtd_test
Type=Application
Categories=Game;
EOF

# Mache die ausführbare Datei ausführbar
chmod +x "$INSTALL_DIR/gtd"

# Aktualisiere die Desktop-Datenbank
update-desktop-database "$HOME/.local/share/applications"

echo "gtd_test wurde erfolgreich installiert!"