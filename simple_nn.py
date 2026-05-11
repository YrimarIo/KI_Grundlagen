#!/usr/bin/env python3
"""
Beispiel 2: Einfaches neuronales Netz mit einer versteckten Schicht

Dieses Skript zeigt ein neuronales Netz mit MEHREREN Schichten:
- Eingabeschicht: Empfängt die Daten
- Versteckte Schicht: Verarbeitet die Daten (hier: 3 Neuronen)
- Ausgabeschicht: Gibt das Endergebnis aus

Was dieses Skript zeigt:
- Wie mehrere Schichten zusammenarbeiten
- Wie Daten durch das Netz "durchgereicht" werden (Vorwaertspropagierung)
- Dass ein Netz OHNE Training nur zufällige Ausgaben liefert

Warum mehrere Schichten?
- Ein einzelnes Neuron (Beispiel 1) kann nur lineare Probleme loesen
- Mit versteckten Schichten kann man komplexe Muster erkennen
- Beispiel: XOR (siehe Beispiel 1) erfordert mindestens eine versteckte Schicht

Fuer Systemintegratoren:
Stellen Sie sich das wie eine Produktionslinie vor:
  Eingang -> Station A -> Station B -> Station C -> Ausgang
  Jede Station macht einen Verarbeitungsschritt und reicht es weiter
"""

import numpy as np


def sigmoid(x):
    """
    Sigmoid-Aktivierungsfunktion (wie in Beispiel 1).

    Hier nochmals zur Erinnerung:
    - Wandelt beliebige Zahlen in den Bereich 0 bis 1 um
    - 0 = "Nein", 1 = "Ja", 0.5 = "unsicher"

    Mathematisch: sigmoid(x) = 1 / (1 + e^(-x))
    """
    return 1 / (1 + np.exp(-x))


class SimpleNeuralNetwork:
    """
    Ein einfaches neuronales Netz mit einer versteckten Schicht.

    Klassen-Struktur erklaerung:
    - class: Eine Vorlage fuer Objekte (wie eine Bauplan)
    - __init__: Der Konstruktor - wird beim Erstellen eines Objekts aufgerufen
    - self: Verweist auf das aktuelle Objekt (wie 'dieses' in anderen Sprachen)
    - self.gewichte_1: Eigenschaft des Objekts - speichert die Gewichte

    Die Gewichte sind wie die 'Kenntnisse' des Netzes:
    - Vor dem Training sind sie zufällig (das Netz 'weiß' noch nichts)
    - Nach dem Training enthalten sie die gelernten Muster
    """

    def __init__(self, eingangs_groesse, versteckte_groesse, ausgangs_groesse):
        """
        Initialisiert das Netz mit zufälligen Gewichten.

        Warum zufällige Gewichte?
        - Ein neues Netz kennt die Welt noch nicht
        - Zufällige Startwerte geben dem Netz eine Basis zum Lernen
        - WICHTIG: Nicht alle gleich! Sonst lernen alle Neuronen das Gleiche

        np.random.seed(42) sorgt fuer Reproduzierbarkeit:
        - Bei jedem Start bekommt das Netz DIESELBen zufälligen Gewichte
        - Damit koennen wir Ergebnisse vergleichen

        Parameter erklaert:
        eingangs_groesse: Wie viele Werte kommen rein? (z.B. 2 Sensoren = 2)
        versteckte_groesse: Wie viele Neuronen in der verborgenen Schicht?
        ausgangs_groesse: Wie viele Werte sollen rauskommen? (z.B. 1 Ja/Nein)

        Gewichte-Formate (Matrix-Mathematik):
        - gewichte_1: (eingabe, versteckt) = (2, 3) fuer 2 Eingaben, 3 versteckte
        - gewichte_2: (versteckt, ausgabe) = (3, 1) fuer 3 versteckte, 1 Ausgabe
        """
        np.random.seed(42)  # Immer gleiche Zufallswerte fuer Reproduzierbarkeit

        # Gewichte fuer erste Schicht (Eingabe -> versteckt)
        # np.random.randn erzeugt Zufallszahlen mit normaler Verteilung
        # Shape: (eingangs_groesse, versteckte_groesse)
        self.gewichte_1 = np.random.randn(eingangs_groesse, versteckte_groesse)

        # Bias fuer erste Schicht - immer 0 als Startwert
        # Shape: (1, versteckte_groesse) - eine Zeile pro Neuron
        self.bias_1 = np.zeros((1, versteckte_groesse))

        # Gewichte fuer zweite Schicht (versteckt -> Ausgabe)
        # Shape: (versteckte_groesse, ausgangs_groesse)
        self.gewichte_2 = np.random.randn(versteckte_groesse, ausgangs_groesse)

        # Bias fuer zweite Schicht
        self.bias_2 = np.zeros((1, ausgangs_groesse))

    def vorwaerts(self, x):
        """
        Vorwaertspropagierung - Daten durchs Netz schicken.

        Dieser Schritt berechnet die Ausgabe des Netzes fuer eine gegebene Eingabe.
        Es wird KEINE Mathematik veraendert - nur berechnet!

        Ablauf (wie eine Produktionslinie):
        1. Eingangswerte kommen rein
        2. Erste Schicht: gewichtet + bias -> Sigmoid -> versteckte Werte
        3. Zweite Schicht: gewichtet + bias -> Sigmoid -> Ausgabe

        Parameter:
            x: Eingabedaten als 2D-Array, z.B. [[0.5, 0.8]]
               Warum 2D? Weil wir spaeter mehrere Eingaben gleichzeitig
               verarbeiten wollen (Batch-Verarbeitung)

        Returns:
            Ausgabe des Netzes als 2D-Array, z.B. [[0.6234]]
        """
        # ========== ERSTE SCHICHT (Eingabe -> Versteckt) ==========
        # np.dot = Matrixmultiplikation
        # x (1,2) dot gewichte_1 (2,3) = versteckte_input (1,3)
        # Das bedeutet: Jeder der 3 versteckten Neuronen bekommt eine
        # kombinierte Eingabe aus allen 2 Eingabewerten
        self.versteckte_input = np.dot(x, self.gewichte_1) + self.bias_1

        # Sigmoid anwenden - jedes der 3 Neuronen aktiviert sich
        self.versteckte_output = sigmoid(self.versteckte_input)

        # ========== ZWEITE SCHICHT (Versteckt -> Ausgabe) ==========
        # versteckte_output (1,3) dot gewichte_2 (3,1) = ausgabe_input (1,1)
        # Das eine Ausgabeneuron kombiniert alle 3 versteckten Werte
        self.ausgabe_input = np.dot(self.versteckte_output, self.gewichte_2) + self.bias_2

        # Sigmoid fuer die endgültige Ausgabe
        self.ausgabe = sigmoid(self.ausgabe_input)

        return self.ausgabe

    def get_weights_info(self):
        """
        Zeigt Informationen über die Netzwerk-Struktur an.

        Hilft zu verstehen, wie viele Verbindungen es gibt:
        - Gewichte = Verbindungen zwischen Neuronen
        - Mehr Neuronen = mehr Gewichte = komplexeres Netz
        """
        print("\nNetzwerk-Architektur:")
        print(f"  Eingabeschicht: {self.gewichte_1.shape[0]} Neuronen")
        print(f"  Versteckte Schicht: {self.gewichte_1.shape[1]} Neuronen")
        print(f"  Ausgabeschicht: {self.gewichte_2.shape[1]} Neuronen")
        print(f"\nGewichte Schicht 1 Shape: {self.gewichte_1.shape}")
        print(f"Gewichte Schicht 2 Shape: {self.gewichte_2.shape}")


def main():
    """
    Hauptfunktion: Erstellt ein Netz und zeigt Vorhersagen.
    """
    print("=" * 50)
    print("Einfaches neuronales Netz - Demo")
    print("=" * 50)

    # ========== NETZWERK ERSTELLEN ==========
    print("\n--- Netzwerke Aufbau ---")
    netzwerk = SimpleNeuralNetwork(
        eingangs_groesse=2,    # 2 Eingabewerte (z.B. 2 Sensoren)
        versteckte_groesse=3,  # 3 Neuronen in der versteckten Schicht
        ausgangs_groesse=1     # 1 Ausgabewert (Ja/Nein Entscheidung)
    )

    # Informationen über das Netz anzeigen
    netzwerk.get_weights_info()

    print("\nWas bedeuten diese Zahlen?")
    print("-" * 50)
    print("Gewichte Schicht 1 (2, 3):")
    print("  - 2 Eingabewerte, jeder verbindet sich mit 3 Neuronen")
    print("  - Also 2 x 3 = 6 Gewichte in dieser Schicht")
    print()
    print("Gewichte Schicht 2 (3, 1):")
    print("  - 3 versteckte Neuronen, alle verbinden sich mit 1 Ausgabeneuron")
    print("  - Also 3 x 1 = 3 Gewichte in dieser Schicht")
    print()
    print("GESAMT: 6 + 3 = 9 Gewichte, die das Netz 'lernen' kann")

    # ========== TESTVORHERSAGEN ==========
    print("\n--- Testvorhersagen (VOR dem Training) ---")
    print("Hinweis: Da das Netz noch nicht trainiert ist, sind die")
    print("Ausgaben zufällig und haben keine sinnvolle Bedeutung.")
    print()

    # Alle moeglichen Kombinationen bei 2 Eingaben (0 oder 1)
    test_eingaeben = [
        [0, 0],
        [0, 1],
        [1, 0],
        [1, 1]
    ]

    for eingang in test_eingaeben:
        # Umwandeln in 2D-Array (wie in der vorwaerts()-Methode erwartet)
        test_input = np.array([eingang])

        # Durchs Netz schicken
        ausgabe = netzwerk.vorwaerts(test_input)

        print(f"Eingang: {eingang} -> Ausgabe: {ausgabe[0][0]:.4f}")

    print("\n" + "=" * 50)
    print("WICHTIG: Dieses Netz ist NOCH NICHT TRAINIERT!")
    print()
    print("Die Ausgaben sind zufaellig. Erst durch Training (siehe")
    print("Beispiel 3) lernt das Netz, sinnvolle Vorhersagen zu treffen.")
    print("=" * 50)


if __name__ == "__main__":
    main()
