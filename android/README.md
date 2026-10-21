# Seva Sankalp - Android Native Mobile App

This directory contains the production Android wrapper for **Seva Sankalp**. It connects directly to your live Flask backend and provides native hardware features.

---

## Key Features

1. **Camera & Gallery Integration**:
   - Donors can click photos of books, clothes, and items directly from their camera or pick from their gallery when uploading resources (`<input type="file">`).
2. **Persistent Sessions**:
   - Handled via Android's `CookieManager` so user logins, DigiLocker verification sessions, and admin states persist even after closing the app.
3. **Pull-to-Refresh**:
   - Native `SwipeRefreshLayout` lets users pull down to refresh item feeds and dashboards.
4. **Offline Resilience**:
   - If internet connection drops, the app gracefully presents an offline screen with a one-tap **Retry** button.
5. **Smart External Intents**:
   - Clicking phone numbers, emails, WhatsApp links, or UPI payment links automatically hands off to native Android apps.
6. **Hardware Back Button**:
   - Navigates through browsing history before displaying a double-tap prompt to exit.

---

## How to Build the APK

### Method 1: Automatic Cloud Build via GitHub Actions (Easiest - No Android Studio Required)
1. Commit and push the project to GitHub:
   ```bash
   git add .
   git commit -m "Add Seva Sankalp Android app and GitHub Actions workflow"
   git push origin main
   ```
2. Open your repository on GitHub: `https://github.com/Anish-S-06/donation_tracker`
3. Click on the **Actions** tab.
4. You will see the **Build Seva Sankalp Android APK** workflow running.
5. Once completed (typically ~2 minutes), click on the completed run and download the **SevaSankalp-Android-App** artifact containing your `.apk`!
6. Transfer the `.apk` to your phone, tap install, and run!

---

### Method 2: Local Build via Android Studio
1. Install [Android Studio](https://developer.android.com/studio).
2. Open Android Studio and select **Open**.
3. Choose the `android/` folder inside this repository.
4. Allow Gradle to sync dependencies.
5. Connect your Android phone via USB (with USB Debugging enabled) or start an Android Emulator.
6. Click the green **Run (Shift + F10)** button to install and launch directly on your device.
7. To generate a shareable APK:
   - Go to **Build > Build Bundle(s) / APK(s) > Build APK(s)**.
   - Click **locate** in the popup to retrieve `app-debug.apk`.

---

## Configuring the Server URL

The target URL is set in:
`android/app/src/main/res/values/strings.xml`

```xml
<string name="server_url">https://anishs06.pythonanywhere.com</string>
```

If you ever change your domain or run locally on a Wi-Fi IP (e.g. `http://192.168.1.10:5000`), simply update this string.
