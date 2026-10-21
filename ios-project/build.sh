#!/bin/bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$DIR")"
DIST_DIR="$ROOT_DIR/dist"
APP_DIR="$DIR/build/IP, PLEASE.app"
PAYLOAD_DIR="$DIR/build/Payload"

echo "=== Building iOS App ==="
rm -rf "$DIR/build"
mkdir -p "$APP_DIR"
mkdir -p "$APP_DIR/web"
mkdir -p "$DIST_DIR"

# 1. Compile Swift sources
xcrun -sdk iphoneos swiftc -O -parse-as-library \
  -target arm64-apple-ios13.0 \
  "$DIR/App/AppDelegate.swift" "$DIR/App/GameViewController.swift" \
  -o "$APP_DIR/IP, PLEASE"

# 2. Copy Info.plist
cp "$DIR/App/Info.plist" "$APP_DIR/Info.plist"

# 3. Generate App Icons from macOS AppIcon.icns
TMP_ICON="/tmp/ipplease_ios_icon.png"
sips -s format png "$ROOT_DIR/dist/IP, PLEASE.app/Contents/Resources/AppIcon.icns" --out "$TMP_ICON" >/dev/null 2>&1 || true

if [ -f "$TMP_ICON" ]; then
  sips -z 120 120 "$TMP_ICON" --out "$APP_DIR/AppIcon60x60@2x.png" >/dev/null 2>&1
  sips -z 180 180 "$TMP_ICON" --out "$APP_DIR/AppIcon60x60@3x.png" >/dev/null 2>&1
  sips -z 152 152 "$TMP_ICON" --out "$APP_DIR/AppIcon76x76@2x~ipad.png" >/dev/null 2>&1
  sips -z 167 167 "$TMP_ICON" --out "$APP_DIR/AppIcon83.5x83.5@2x~ipad.png" >/dev/null 2>&1
  sips -z 1024 1024 "$TMP_ICON" --out "$APP_DIR/AppIcon1024.png" >/dev/null 2>&1
fi

# 4. Copy web assets
cp "$ROOT_DIR"/*.html "$APP_DIR/web/"
cp "$ROOT_DIR"/*.js "$APP_DIR/web/"
cp "$ROOT_DIR"/*.txt "$APP_DIR/web/" 2>/dev/null || true
cp "$ROOT_DIR"/LICENSE "$APP_DIR/web/" 2>/dev/null || true

# 5. Sign App Bundle
YU_LIANG_HASH=$(security find-identity -v -p codesigning 2>/dev/null | grep -i "Yu Liang" | head -n 1 | awk '{print $2}')
IDENTITY_HASH=${YU_LIANG_HASH:-$(security find-identity -v -p codesigning 2>/dev/null | grep -E "Apple Development|iPhone Developer" | head -n 1 | awk '{print $2}')}

if [ -n "$IDENTITY_HASH" ]; then
  echo "Signing with identity hash: $IDENTITY_HASH"
  codesign --force --deep --sign "$IDENTITY_HASH" --timestamp=none "$APP_DIR" || codesign --force --deep --sign - "$APP_DIR"
else
  echo "Signing with ad-hoc signature"
  codesign --force --deep --sign - "$APP_DIR"
fi

# 6. Package into IPA
mkdir -p "$PAYLOAD_DIR"
cp -r "$APP_DIR" "$PAYLOAD_DIR/"

IPA_PATH="$DIST_DIR/IP_PLEASE_iOS.ipa"
rm -f "$IPA_PATH"
(cd "$DIR/build" && zip -qry "$IPA_PATH" Payload)

echo "=== Successfully built iOS IPA: $IPA_PATH ==="
ls -lh "$IPA_PATH"
