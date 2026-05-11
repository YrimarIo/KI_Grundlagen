#!/usr/bin/env python3
"""
Beispiel 3: Trainierbares neuronales Netz mit Backpropagation

Dieses Skript zeigt, wie ein neuronales Netz LERNEN kann:
- Das Netz startet ohne Wissen (zufällige Gewichte)
- Durch Training passt es seine Gewichte an
- Am Ende kann es komplexe Probleme loesen (wie XOR)

Was ist Backpropagation?
- "Rückwaertspropagierung" des Fehlers
- Idee: Wenn das Netz einen Fehler macht, passen wir die Gewichte so an,
  dass der Fehler beim naechsten Mal kleiner wird
- Analogie: Wie beim Lernen fur eine Pruefung - nach jeder falschen Antwort
  verstehen wir, was wir falsch gemacht haben und korrigieren es

Was dieses Skript loest:
- Das XOR-Problem (siehe Beispiel 1 - dort konnte ein einzelnes Neuron das nicht)
- XOR braucht mindestens eine versteckte Schicht

Fuer Systemintegratoren:
Backpropagation ist wie ein Selbst-Optimierungssystem:
  1. Messen (Vorwaerts: Eingabe -> Ausgabe)
  2. Fehler berechnen (Soll - Ist)
  3. Rueckwärts korrigieren (Jede Schicht passt ihre Gewichte an)
  4. Wiederholen bis Fehler klein genug
"""

import numpy as np


class TrainierbaresNeuronalesNetz:
    """
    Neuronales Netz mit Backpropagation zum Lernen.

    Dieses Netz kann sich selbst korrigieren:
    - Vorwaerts: Berechnet Ausgabe
    - Fehler berechnen: Wie falsch war die Vorhersage?
    - Backpropagation: Passe Gewichte an, um Fehler zu reduzieren
    - Wiederhole: Bis das Netz gut ist
    """

    def __init__(self, eingangs_groesse, versteckte_groesse, ausgangs_groesse):
        """
        Initialisiert das Netz mit zufälligen Gewichten.

        Wie bei Beispiel 2 werden hier die Gewichte zufällig初始isiert.
        Das Netz startet also "unwissend" und muss lernen.
        """
        np.random.seed(42)  # Reproduzierbarkeit

        # Gewichte initialisieren (wie in Beispiel 2)
        self.gewichte_1 = np.random.randn(eingangs_groesse, versteckte_groesse)
        self.bias_1 = np.zeros((1, versteckte_groesse))
        self.gewichte_2 = np.random.randn(versteckte_groesse, ausgangs_groesse)
        self.bias_2 = np.zeros((1, ausgangs_groesse))

    def vorwaerts(self, x):
        """
        Vorwärtspropagierung - berechnet die Ausgabe.

        Gleiche Logik wie in Beispiel 2, nur dass wir hier die
        Zwischenwerte speichern, um sie spaeter fuer Backpropagation
        zu benoetzen.
        """
        self.versteckte_input = np.dot(x, self.gewichte_1) + self.bias_1
        self.versteckte_output = self.sigmoid(self.versteckte_input)
        self.ausgabe_input = np.dot(self.versteckte_output, self.gewichte_2) + self.bias_2
        self.ausgabe = self.sigmoid(self.ausgabe_input)
        return self.ausgabe

    def trainieren(self, x_eingabe, y_ziel, learning_rate=0.1, epochen=100):
        """
        Trainiert das Netz mit Backpropagation.

        Was passiert hier?
        1. Wiederhole 'epochen' mal:
           a) Vorwaerts: Berechne Ausgabe
           b) Fehler: Wie weit sind wir vom Ziel entfernt?
           c) Backpropagation: Korrigiere Gewichte basierend auf Fehler
           d) Wiederhole bis Fehler klein ist

        Parameter:
            x_eingabe: Trainingsdaten - alle Eingaben (z.B. [[0,0],[0,1],[1,0],[1,1]])
            y_ziel: Gewünschte Ausgaben (z.B. [[0],[1],[1],[0]] fuer XOR)
            learning_rate: Wie stark korrigieren wir pro Schritt?
                           - Zu hoch: Netz "zittert" um die Loesung
                           - Zu niedrig: Training dauert ewig
                           - Typisch: 0.1 bis 1.0
            epochen: Wie oft durchlaeuft das Netz die gesamten Daten?
                     - Mehr Epochs = besseres Training (aber mehr Zeit)
                     - Typisch: 1000 bis 100000

        Returns:
            losses: Liste aller Loss-Werte (damit kann man den Verlauf plotten)
        """
        losses = []  # Speichert den Fehler jeder Epoche

        for epoch in range(epochen):
            # ========== SCHRITT 1: Vorwaertspropagierung ==========
            ausgabe = self.vorwaerts(x_eingabe)

            # ========== SCHRITT 2: Fehler berechnen ==========
            # Wie weit ist unsere Ausgabe vom Ziel entfernt?
            fehler = y_ziel - ausgabe

            # Loss = Mittlerer Quadratischer Fehler (MSE)
            # Je kleiner, desto besser lernt das Netz
            loss = np.mean(fehler**2)
            losses.append(loss)

            # ========== SCHRITT 3: Backpropagation ==========
            # Jetzt gehen wir Rueckwaerts und korrigieren die Gewichte

            # --- Ausgabe-Schicht korrigieren ---
            # Wie viel "Schuld" hat das Ausgabeneuron am Fehler?
            # Wir multiplizieren den Fehler mit der Ableitung der Sigmoid-Funktion
            # Das gibt uns die "Richtung" in der wir korrigieren muessen
            #d_ausgabe = fehler * self.sigmoid_ableitung(self.ausgabe_input)
            d_ausgabe = fehler * self.sigmoid_ableitung(self.ausgabe)
            # --- Versteckte Schicht korrigieren ---
            # Wie viel "Schuld" haben die versteckten Neuronen?
            # Wir uebertragen die "Schuld" des Ausgabeneurons zurueck
            #d_versteckt = np.dot(d_ausgabe, self.gewichte_2.T) * self.sigmoid_ableitung(self.versteckte_input)
            d_versteckt = np.dot(d_ausgabe, self.gewichte_2.T) * self.sigmoid_ableitung(self.versteckte_output)
            # ========== SCHRITT 4: Gewichte aktualisieren ==========
            # Jetzt passen wir alle Gewichte an - in die Richtung die den Fehler verringert

            # Gewichte Schicht 2 anpassen
            # delta = learning_rate * (wie wichtig war diese Verbindung?) * (wie falsch war das Ergebnis?)
            self.gewichte_2 += learning_rate * np.dot(self.versteckte_output.T, d_ausgabe)
            self.bias_2 += learning_rate * d_ausgabe.sum(axis=0, keepdims=True)

            # Gewichte Schicht 1 anpassen
            self.gewichte_1 += learning_rate * np.dot(x_eingabe.T, d_versteckt)
            self.bias_1 += learning_rate * d_versteckt.sum(axis=0, keepdims=True)

            # Status alle 1000 Epochen anzeigen
            if epoch % 1000 == 0:
                print(f"Epoch {epoch}: Loss = {loss:.4f}")

        return losses

    @staticmethod
    def sigmoid(x):
        """Sigmoid-Funktion - wie in Beispiel 1 und 2"""
        return 1 / (1 + np.exp(-x))

    @staticmethod
    def sigmoid_ableitung(x):
        """
        Ableitung der Sigmoid-Funktion.

        Warum brauchen wir die Ableitung?
        - Die Ableitung zeigt uns die "Steigung" der Sigmoid-Funktion
        - Bei steiler Steigung = kleine Aenderung in Input = grosse Aenderung in Output
        - Bei flacher Steigung = grosse Aenderung in Input = kleine Aenderung in Output
        - Fuer Backpropagation: Wir muessen wissen, wie stark sich eine Aenderung
          der Gewichte auf den Fehler auswirkt

        Mathematisch: sigmoid'(x) = sigmoid(x) * (1 - sigmoid(x))
        Da wir schon sigmoid(x) berechnet haben (als 'x' uebergeben),
        koennen wir die Ableitung einfach berechnen.
        """
        return x * (1 - x)


def main():
    """
    Hauptfunktion: Trainiert das Netz auf dem XOR-Problem.
    """
    print("=" * 50)
    print("Trainierbares neuronales Netz - XOR Problem")
    print("=" * 50)

    # ========== XOR TRAININGSDATEN ==========
    # XOR = "Exclusive OR" - Ausgabe ist 1 wenn EXAKT EINE Eingabe 1 ist
    #
    # Warum ist XOR schwer?
    # - AND und OR sind "linear trennbar" (eine Gerade reicht zur Trennung)
    # - XOR ist "nicht linear trennbar" (braucht gekruemmte Trennlinie)
    # - Deshalb braucht XOR mindestens eine versteckte Schicht

    # Eingabedaten: Alle 4 Kombinationen bei 2 Bit
    x_train = np.array([[0, 0],   # Beide aus
                        [0, 1],   # Zweiter an
                        [1, 0],   # Erster an
                        [1, 1]])  # Beide an

    # Gewünschte Ausgaben fuer XOR
    y_train = np.array([[0],   # XOR(0,0) = 0
                        [1],   # XOR(0,1) = 1
                        [1],   # XOR(1,0) = 1
                        [0]])  # XOR(1,1) = 0

    print("\nXOR-Truth Table:")
    print("XOR(0, 0) = 0  (beide gleich -> 0)")
    print("XOR(0, 1) = 1  (verschieden -> 1)")
    print("XOR(1, 0) = 1  (verschieden -> 1)")
    print("XOR(1, 1) = 0  (beide gleich -> 0)")

    # ========== NETZWERK ERSTELLEN ==========
    print("\n--- Netzwerk Architektur ---")
    netzwerk = TrainierbaresNeuronalesNetz(
        eingangs_groesse=2,    # 2 Eingaben (die beiden Bit)
        versteckte_groesse=4,  # 4 Neuronen in versteckter Schicht
        ausgangs_groesse=1     # 1 Ausgabe (XOR-Ergebnis)
    )
    print("Eingang: 2 Neuronen")
    print("Versteckt: 4 Neuronen")
    print("Ausgabe: 1 Neuron")

    # ========== NETZWERK TRAINIEREN ==========
    print("\n--- Training startet ---")
    print("Das Netz lernt jetzt XOR durch Wiederholung...")
    print("(Dies kann einige Sekunden dauern)")

    losses = netzwerk.trainieren(x_train, y_train, learning_rate=0.5, epochen=10000)

    print("\n--- Ergebnisse nach dem Training ---")

    # ========== ERGEBNISSE UEBERPRUEFEN ==========
    alle_korrekt = True
    for i in range(len(x_train)):
        test_input = x_train[i:i+1]  # Einzelne Zeile als 2D-Array
        ergebnis = netzwerk.vorwaerts(test_input)
        erwartet = int(y_train[i][0])
        # Ausgabe > 0.5 bedeutet "1", sonst "0"
        klassifiziert = 1 if ergebnis[0][0] > 0.5 else 0
        status = "OK" if klassifiziert == erwartet else "FEHLER"
        if klassifiziert != erwartet:
            alle_korrekt = False
        print(f"XOR({int(x_train[i][0])}, {int(x_train[i][1])}) = {ergebnis[0][0]:.4f} -> {klassifiziert} (erwartet: {erwartet}) [{status}]")

    print("\n" + "=" * 50)
    if alle_korrekt:
        print("ERFOLG! Das Netzwerk hat XOR gelernt!")
        print()
        print("Das Netz konnte die nicht-linear trennbare XOR-Funktion")
        print("durch die versteckte Schicht erfolgreich lernen.")
    else:
        print("Das Netzwerk hat nicht alle Fälle korrekt.")
        print("Versuchen Sie mehr Epochen oder eine andere learning_rate.")
    print("=" * 50)
    
    print("\n--- Ein Blick in das Gehirn (Die gelernten Gewichte) ---")
    print("Gewichte Schicht 1 (Verbindungen: Eingänge -> Versteckte Schicht):")
    print(np.round(netzwerk.gewichte_1, 2))
    print("\nBias Schicht 1:")
    print(np.round(netzwerk.bias_1, 2))
    
    print("\nGewichte Schicht 2 (Verbindungen: Versteckte Schicht -> Ausgabe):")
    print(np.round(netzwerk.gewichte_2, 2))
    print("\nBias Schicht 2:")
    print(np.round(netzwerk.bias_2, 2))


if __name__ == "__main__":
    main()
