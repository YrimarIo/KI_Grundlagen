# Anleitung für Azubis  
**Raspberry Pi Imager herunterladen, SD‑Karte flashen, SSH‑Server aktivieren und ein Installationsskript von GitHub ausführen**

---

## 📌 Einleitung  
In dieser Anleitung erfährst du Schritt für Schritt, wie du den **Raspberry Pi Imager** installierst, ein Betriebssystem auf eine SD‑Karte flashst, den SSH‑Server aktivierst und anschließend ein Skript aus einem GitHub‑Repository auf dem Pi ausführst.

---

## ✅ Voraussetzungen  
| Was du brauchst | Wie du es bekommst |
|-----------------|---------------------|
| 1 × SD‑Karte (mind. 8 GB, Klasse 10 empfohlen) | Aus dem Online‑Shop, AT‑Store, oder aus dem vorhandenen Zubehör |
| SD‑Kartenleser | In den meisten Laptops integrierter, sonst USB‑Kartenleser |
| PC/Notebook | Windows 10/11, macOS 10.14+, Ubuntu 20.04+ |
| Internetverbindung | Für den Download des Imagers und ggf. Updates |
| Optional: SSH‑Client (z. B. PuTTY, Terminal, MobaXterm) | Für den späteren Zugriff auf den Pi |

---

## 📥 Schritt 1 – Raspberry Pi Imager herunterladen  

1. **Website öffnen**  
   👉 [https://www.raspberrypi.org/software/](https://www.raspberrypi.org/software/)

2. **Download‑Option wählen**  
   | Betriebssystem | Dateityp |
   |----------------|----------|
   | Windows        | `Raspberry_Pi_Imager_Setup.exe` |
   | macOS          | `Raspberry_Pi_Imager-*.dmg` |
   | Linux (Debian/Ubuntu) | `raspberry-pi-imager_*_amd64.deb` |
   | Linux (arch, etc.) | `raspberry-pi-imager-*.*.*-any.pkg.tar.zst` |
   | Andere Linux‑Distributionen | `.AppImage` (beispielsweise `raspberry-pi-imager-*.*.*-any.AppImage`) |

3. **Download starten**  
   Klicke auf den entsprechenden Link, speichere die Datei auf deinem Rechner.

> **Tipps**  
> - Bei Windows: Nach dem Download die `.exe` ausführen und dem Installations‑Assistenten folgen.  
> - Bei macOS: Die `.dmg` öffnen, die Anwendung in den **Applications**‑Ordner ziehen.  
> - Bei Linux:  
>   ```bash
>   sudo dpkg -i raspberry-pi-imager_*.deb      # Debian/Ubuntu
>   sudo pacman -U raspberry-pi-imager-*.pkg.tar.zst   # Arch Linux
>   # oder
>   ./raspberry-pi-imager-*-any.AppImage          # AppImage
>   ```

---

## 🛠 Schritt 2 – Raspberry Pi Imager starten  

| OS | Start‑Befehl |
|----|--------------|
| Windows | `Start` → `Raspberry Pi Imager` |
| macOS | `Applications` → `Raspberry Pi Imager` |
| Linux | `raspberry-pi-imager` im Terminal (oder aus dem Anwendungs‑Menü) |

---

## 🔐 Schritt 3 – SD‑Karte vorbereiten  
1. **SD‑Karte einstecken** (z. B. in den Kartenleser).  
2. Im Imager erscheint die Karte im Abschnitt **“Speichergerät”**.  
   - Prüfe, ob die richtige Karte ausgewählt ist (z. B. `mmcblk0` oder `mmcblk1`).  

---

## 📦 Schritt 4 – Image wählen und sichern  
1. Klicke **“Image auswählen”** und **"Raspberry Pi OS (other)"** wähle **“Raspberry Pi OS Lite (64‑bit)”**.  
2. Klicke **“Weiter”**.

---

## 🔧 Schritt 4 – SSH‑Server aktivieren  
1. Klicke auf **“Optionen”** (rechts oben).  
2. Aktiviere die Checkbox **“SSH‑Server (OpenSSH) aktivieren”**.  
3. Optional: Optional‑Schreiboptionen (z. B. **VNC** oder **Wi‑Fi‑Einstellungen**) konfigurieren.  
4. Klicke **“OK”** und **“Start”**.

> **Hinweis**  
> Für ältere Imager‑Versionen (unter Windows/macOS) kann das „Advanced Options“-Menü fehlen. In diesem Fall **aktualisiere** den Imager, bevor du fortfährst.

---

## 📦 Schritt 4 – Raspberry Pi OS Lite‑Image wählen  
1. Klicke **“Image auswählen”** erneut und wähle **“Raspberry Pi OS Lite (64‑bit)”**.  
2. Klicke **“Weiter”**.

---

## 🪙 Schritt 5 – Netzwerkeinrichtung  
1. Klicke **“Optionen”** → **“Wi‑Fi‑Verbindung konfigurieren”**.  
2. Gib **SSID** und **Passwort** ein, wenn du das Pi per WLAN starten möchtest.  
3. Klicke **“OK”** und **“Start”**.

---

## 🔑 Schritt 6 – SSH‑Server aktivieren  
- **Im Imager**: „SSH‑Server (OpenSSH) aktivieren“ bereits im Schritt 4 aktiviert → kein weiteres Vorgehen nötig.  
- **Falls du SSH noch manuell aktivieren möchtest**:  
  ```bash
  sudo systemctl enable ssh
  sudo systemctl start ssh
  ```
  
---

## 🚀 Schritt 7 – Image auf die SD‑Karte schreiben  
1. **Karte wählen** und **“Start”** klicken.  
2. Der Imager formatiert, lädt das OS‑Image und schreibt es auf die Karte.  
3. Nach Abschluss erscheint eine **“Success”**‑Meldung.

---

## 🚀 Schritt 8 – SSH‑Verbindung zum Pi herstellen  
Prüfe die IP‑Adresse des Pi (z. B. im Router‑Dashboard oder über `arp -a`).  
Öffne einen SSH‑Client und verbinde dich:  
`ssh pi@<IP‑Adresse>`  
(Standard‑Benutzername = `pi`, Standard‑Passwort = `raspberry`)

---

## 📁 Schritt 9 – Installationsskript aus GitHub herunterladen & ausführen  

### Skript von GitHub holen  

Du kannst das Skript direkt mit `curl`/`wget` herunterladen oder das komplette Repository klonen.

**Einfacher Ansatz (Raw‑Download):**

```bash
wget https://github.com/YrimarIo/KI_Grundlagen/blob/main/install.sh
# Das Skript liegt jetzt in der aktuellen Arbeitsverzeichnis unter install.sh
```

**Alternative (Repository klonen):**

```bash
git clone https://github.com/YrimarIo/KI_Grundlagen.git
# Dann kannst du die Datei aus dem geklonten Ordner kopieren
```

### Skript in einen neuen `install.sh`‑Datei auf dem Pi einfügen  

Du bist bereits im Home‑Verzeichnis des Pi (`~`).

```bash
# Gehe zum Desktop-Ordner
cd ~/Desktop

# Erstelle oder öffne die install.sh‑Datei
nano install.sh
# (oder `vi install.sh` / `vim install.sh` je nach Vorliebe)

# Kopiere den Inhalt des heruntergeladenen Skripts (oder den Code aus dem Repository) in das nano‑Fenster.

# Drücke Strg + O → Enter (Datei speichern).
# Drücke Strg + X (nano schließen).
```

### Datei ausführbar machen  

```bash
chmod +x install.sh
```

### Skript ausführen  

```bash
# Falls das Skript Root‑Rechte benötigt, nutze sudo
sudo ./install.sh
# Oder einfach ohne sudo, falls das Skript keine Root‑Rechte verlangt:
./install.sh
```

### Installation prüfen  

Folge den Ausgaben des Skripts.  
Bei erfolgreicher Installation sollte die Konsole eine Bestätigung ausgeben.  
Falls Fehler auftreten, prüfe die Fehlermeldungen und richte ggf. fehlende Abhängigkeiten nach.
