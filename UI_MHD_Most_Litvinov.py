import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QComboBox, QStackedWidget, QMessageBox, QTextEdit, QSizePolicy,
    QSpinBox, QLineEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Analýza MHD Most & Litvínov")
        self.setGeometry(100, 100, 800, 600)

        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        self._create_main_menu_screen()
        self._create_analyza1_linka_screen()
        self._create_analyza1_den_screen()
        self._create_analyza1_casovy_usek_screen()
        self._create_analyza1_delka_useku_screen()
        self._create_analyza2_uzel_screen()
        self._create_analyza2_linka_screen()
        self._create_analyza2_den_screen()
        self._create_o_projektu_screen()

        self.stacked_widget.setCurrentWidget(self.main_menu_widget)
        self.setMinimumSize(600, 400)

    # --- Funkce pro vytváření jednotlivých obrazovek ---

    def _create_main_menu_screen(self):
        self.main_menu_widget = QWidget()
        layout = QVBoxLayout(self.main_menu_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        btn_analyza1 = QPushButton("Analýza rozložení zpoždění na dané lince", self.main_menu_widget)
        btn_analyza2 = QPushButton("Analýza spolehlivosti přestupních vazeb", self.main_menu_widget)
        btn_o_projektu = QPushButton("O projektu", self.main_menu_widget)

        btn_analyza1.setFixedSize(250, 50)
        btn_analyza2.setFixedSize(250, 50)
        btn_o_projektu.setFixedSize(250, 50)

        layout.addStretch()
        layout.addWidget(btn_analyza1)
        layout.addWidget(btn_analyza2)
        layout.addWidget(btn_o_projektu)
        layout.addStretch()

        btn_analyza1.clicked.connect(self._on_btn_analyza1_clicked)
        btn_analyza2.clicked.connect(self._on_btn_analyza2_clicked)
        btn_o_projektu.clicked.connect(self._on_btn_o_projektu_clicked)

        self.stacked_widget.addWidget(self.main_menu_widget)

    def _create_analyza1_linka_screen(self):
        self.analyza1_linka_widget = QWidget()
        layout = QVBoxLayout(self.analyza1_linka_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label = QLabel("Zvolte číslo anylyzované linky:", self.analyza1_linka_widget)
        self.analyza1_linky_combo = QComboBox(self.analyza1_linka_widget)
        self.analyza1_linky_combo.addItems(["Linka 1", "Linka 2", "Linka 3", "Linka 4", "Linka 5", "Linka 8", "Linka 9", "Linka 10", "Linka 12", "Linka 13", "Linka 14", "Linka 15", "Linka 16", "Linka 17", "Linka 18", "Linka 20", "Linka 21", "Linka 22", "Linka 23", "Linka 25", "Linka 27", "Linka 28", "Linka 30", "Linka 31", "Linka 40", "Linka 50", "Linka 51", "Linka 53", "Linka 60"])
        self.analyza1_linky_combo.setMinimumWidth(200)
        self.analyza1_linky_combo.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        # NOVÉ TLAČÍTKO POKRAČOVAT
        btn_pokracovat = QPushButton("Pokračovat", self.analyza1_linka_widget)
        btn_pokracovat.setFixedSize(150, 35)

        btn_zpet = QPushButton("Zpět", self.analyza1_linka_widget)
        btn_zpet.setFixedSize(150, 35)

        layout.addStretch()
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.analyza1_linky_combo, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(20)
        layout.addWidget(btn_pokracovat, alignment=Qt.AlignmentFlag.AlignCenter) # Přidání tlačítka Pokračovat
        layout.addWidget(btn_zpet, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()

        # Důležité: Odpojíme přímé přepínání přes currentIndexChanged
        # self.analyza1_linky_combo.currentIndexChanged.connect(self._on_analyza1_linka_selected)
        # Nyní propojíme tlačítko Pokračovat
        btn_pokracovat.clicked.connect(self._on_analyza1_linka_pokracovat_clicked)
        btn_zpet.clicked.connect(self._on_analyza1_zpet_linka_clicked)

        self.stacked_widget.addWidget(self.analyza1_linka_widget)

    def _create_analyza1_den_screen(self):
        self.analyza1_den_widget = QWidget()
        layout = QVBoxLayout(self.analyza1_den_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label = QLabel("Zvolte dny v týdnu, pro které bude analyzováno rozložení zpoždění:", self.analyza1_den_widget)
        # Seznam s možností výběru více dnů
        self.analyza1_dny_list = QListWidget(self.analyza1_den_widget)
        self.analyza1_dny_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.analyza1_dny_list.setMinimumWidth(200)
        self.analyza1_dny_list.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

# Dny v týdnu s pořadím (pondělí = 0)
dny = ["Pondělí", "Úterý", "Středa", "Čtvrtek", "Pátek", "Sobota", "Neděle"]
for den in dny:
    self.analyza1_dny_list.addItem(QListWidgetItem(den))

# Funkce pro získání indexů vybraných dnů (např. [0, 1, 2] pro Po–St)
def get_selected_days():
    return [
        dny.index(item.text())
        for item in self.analyza1_dny_list.selectedItems()
    ]

        btn_pokracovat = QPushButton("Pokračovat", self.analyza1_den_widget)
        btn_pokracovat.setFixedSize(150, 35)
        btn_zpet = QPushButton("Zpět", self.analyza1_den_widget)
        btn_zpet.setFixedSize(150, 35)

        layout.addStretch()
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.analyza1_dny_combo, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(20)
        layout.addWidget(btn_pokracovat, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(btn_zpet, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()

        self.analyza1_dny_combo.currentIndexChanged.connect(self._on_analyza1_den_selected)
        btn_pokracovat.clicked.connect(self._on_analyza1_den_pokracovat_clicked)
        btn_zpet.clicked.connect(self._on_analyza1_zpet_den_clicked)

        self.stacked_widget.addWidget(self.analyza1_den_widget)

    def _create_analyza1_casovy_usek_screen(self):
        self.analyza1_casovy_usek_widget = QWidget()
        layout = QVBoxLayout(self.analyza1_casovy_usek_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label_start = QLabel("Zadejte počáteční hodinu časového intervalu (0-24):", self.analyza1_casovy_usek_widget)
        self.analyza1_hodina_start_spinbox = QSpinBox(self.analyza1_casovy_usek_widget)
        self.analyza1_hodina_start_spinbox.setRange(0, 24)
        self.analyza1_hodina_start_spinbox.setMinimumWidth(100)
        self.analyza1_hodina_start_spinbox.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.analyza1_hodina_start_spinbox.setValue(0)

        label_end = QLabel("Zadejte koncovou hodinu časového intervalu (0-24):", self.analyza1_casovy_usek_widget)
        self.analyza1_hodina_konec_spinbox = QSpinBox(self.analyza1_casovy_usek_widget)
        self.analyza1_hodina_konec_spinbox.setRange(0, 24)
        self.analyza1_hodina_konec_spinbox.setMinimumWidth(100)
        self.analyza1_hodina_konec_spinbox.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.analyza1_hodina_konec_spinbox.setValue(24)

        btn_pokracovat = QPushButton("Pokračovat", self.analyza1_casovy_usek_widget)
        btn_pokracovat.setFixedSize(150, 35)
        btn_zpet = QPushButton("Zpět", self.analyza1_casovy_usek_widget)
        btn_zpet.setFixedSize(150, 35)

        layout.addStretch()
        layout.addWidget(label_start, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.analyza1_hodina_start_spinbox, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(10)
        layout.addWidget(label_end, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.analyza1_hodina_konec_spinbox, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(20)
        layout.addWidget(btn_pokracovat, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(btn_zpet, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()

        btn_pokracovat.clicked.connect(self._on_analyza1_casovy_usek_pokracovat_clicked)
        btn_zpet.clicked.connect(self._on_analyza1_casovy_usek_zpet_clicked)

        self.stacked_widget.addWidget(self.analyza1_casovy_usek_widget)

    def _create_analyza1_delka_useku_screen(self):
        self.analyza1_delka_useku_widget = QWidget()
        layout = QVBoxLayout(self.analyza1_delka_useku_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label = QLabel("Zadejte délku úseku pro analýzu zpoždění (v metrech):", self.analyza1_delka_useku_widget)
        self.analyza1_delka_useku_lineedit = QLineEdit(self.analyza1_delka_useku_widget)
        self.analyza1_delka_useku_lineedit.setPlaceholderText("Např. 1000 (metrů)")
        self.analyza1_delka_useku_lineedit.setMinimumWidth(200)
        self.analyza1_delka_useku_lineedit.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        validator = QIntValidator(1, 99999, self.analyza1_delka_useku_lineedit)
        self.analyza1_delka_useku_lineedit.setValidator(validator)

        btn_proved_analizu = QPushButton("Provést analýzu", self.analyza1_delka_useku_widget)
        btn_proved_analizu.setFixedSize(150, 35)
        btn_zpet = QPushButton("Zpět", self.analyza1_delka_useku_widget)
        btn_zpet.setFixedSize(150, 35)

        layout.addStretch()
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.analyza1_delka_useku_lineedit, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(20)
        layout.addWidget(btn_proved_analizu, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(btn_zpet, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()

        btn_proved_analizu.clicked.connect(self._on_analyza1_proved_analizu_clicked)
        btn_zpet.clicked.connect(self._on_analyza1_delka_useku_zpet_clicked)

        self.stacked_widget.addWidget(self.analyza1_delka_useku_widget)

    # --- Zbytek obrazovek (beze změny) ---

    def _create_analyza2_uzel_screen(self):
        self.analyza2_uzel_widget = QWidget()
        layout = QVBoxLayout(self.analyza2_uzel_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label = QLabel("Zvolte centrální přestupní uzel (CPU):", self.analyza2_uzel_widget)
        btn_uzel1 = QPushButton("CPU Most", self.analyza2_uzel_widget)
        btn_uzel2 = QPushButton("CPU Litvínov", self.analyza2_uzel_widget)
        btn_zpet = QPushButton("Zpět", self.analyza2_uzel_widget)

        btn_uzel1.setFixedSize(200, 40)
        btn_uzel2.setFixedSize(200, 40)
        btn_zpet.setFixedSize(150, 35)

        layout.addStretch()
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(btn_uzel1, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(btn_uzel2, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(20)
        layout.addWidget(btn_zpet, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()

        btn_uzel1.clicked.connect(self._on_analyza2_uzel1_clicked)
        btn_uzel2.clicked.connect(self._on_analyza2_uzel2_clicked)
        btn_zpet.clicked.connect(self._on_analyza2_zpet_uzel_clicked)

        self.stacked_widget.addWidget(self.analyza2_uzel_widget)

    def _create_analyza2_linka_screen(self):
        self.analyza2_linka_widget = QWidget()
        layout = QVBoxLayout(self.analyza2_linka_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label = QLabel("Zvolte linku pro Analýzu 2:", self.analyza2_linka_widget)
        self.analyza2_linky_combo = QComboBox(self.analyza2_linka_widget)
        self.analyza2_linky_combo.addItems(["Linka 1", "Linka 2", "Linka 3", "Linka 4", "Linka 5", "Linka 8", "Linka 9", "Linka 10", "Linka 12", "Linka 13", "Linka 14", "Linka 15", "Linka 16", "Linka 17", "Linka 18", "Linka 20", "Linka 21", "Linka 22", "Linka 23", "Linka 25", "Linka 27", "Linka 28", "Linka 30", "Linka 31", "Linka 40", "Linka 50", "Linka 51", "Linka 53", "Linka 60"])
        self.analyza2_linky_combo.setMinimumWidth(200)
        self.analyza2_linky_combo.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        btn_zpet = QPushButton("Zpět", self.analyza2_linka_widget)
        btn_zpet.setFixedSize(150, 35)

        layout.addStretch()
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.analyza2_linky_combo, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(20)
        layout.addWidget(btn_zpet, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()

        self.analyza2_linky_combo.currentIndexChanged.connect(self._on_analyza2_linka_selected)
        btn_zpet.clicked.connect(self._on_analyza2_zpet_linka_clicked)

        self.stacked_widget.addWidget(self.analyza2_linka_widget)

    def _create_analyza2_den_screen(self):
        self.analyza2_den_widget = QWidget()
        layout = QVBoxLayout(self.analyza2_den_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label = QLabel("Zvolte den v týdnu pro Analýzu 2:", self.analyza2_den_widget)
        self.analyza2_dny_combo = QComboBox(self.analyza2_den_widget)
        self.analyza2_dny_combo.addItems(["Pondělí", "Úterý", "Středa", "Čtvrtek", "Pátek", "Sobota", "Neděle"])
        self.analyza2_dny_combo.setMinimumWidth(200)
        self.analyza2_dny_combo.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        btn_proved_analizu = QPushButton("Provést analýzu", self.analyza2_den_widget)
        btn_zpet = QPushButton("Zpět", self.analyza2_den_widget)

        btn_proved_analizu.setFixedSize(150, 35)
        btn_zpet.setFixedSize(150, 35)

        layout.addStretch()
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.analyza2_dny_combo, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(20)
        layout.addWidget(btn_proved_analizu, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(btn_zpet, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()

        self.analyza2_dny_combo.currentIndexChanged.connect(self._on_analyza2_den_selected)
        btn_proved_analizu.clicked.connect(self._on_analyza2_proved_analizu_clicked)
        btn_zpet.clicked.connect(self._on_analyza2_zpet_den_clicked)

        self.stacked_widget.addWidget(self.analyza2_den_widget)

    def _create_o_projektu_screen(self):
        self.o_projektu_widget = QWidget()
        layout = QVBoxLayout(self.o_projektu_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        text_edit = QTextEdit(
            "<h1>O projektu: Analýza MHD Most & Litvínov</h1>"
            "<p>Tato aplikace slouží k demonstraci uživatelského rozhraní pro analýzu dat hromadné dopravy ve městech Most a Litvínov.</p>"
            "<p><b>Funkce:</b></p>"
            "<ul>"
            "<li><b>Analýza rozložení zpoždění na dané lince</b> - Umožňuje zvolit linku, den v týdnu, časový interval a délku úseku pro hypotetickou analýzu.</li>"
            "<li><b>Analýza spolehlivosti přestupních vazeb</b> - Umožňuje zvolit konkrétní přestupní uzel, linku a den v týdnu pro hypotetickou analýzu.</li>"
            "</ul>"
            "<p><b>Autor:</b> Tvoje jméno/Tým</p>"
            "<p><b>Verze:</b> 0.1 (UI Prototyp)</p>"
            "<p>Propojení s reálnými daty a analytickými algoritmy je v plánu do budoucna.</p>",
            self.o_projektu_widget
        )
        text_edit.setReadOnly(True)
        text_edit.setFixedSize(500, 350)

        btn_zpet = QPushButton("Zpět", self.o_projektu_widget)
        btn_zpet.setFixedSize(150, 35)

        layout.addStretch()
        layout.addWidget(text_edit, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(20)
        layout.addWidget(btn_zpet, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()

        btn_zpet.clicked.connect(self._on_o_projektu_zpet_clicked)

        self.stacked_widget.addWidget(self.o_projektu_widget)

    # --- Implementace slotů pro navigaci a fiktivní analýzu ---

    # Hlavní menu
    def _on_btn_analyza1_clicked(self):
        self.stacked_widget.setCurrentWidget(self.analyza1_linka_widget)

    def _on_btn_analyza2_clicked(self):
        self.stacked_widget.setCurrentWidget(self.analyza2_uzel_widget)

    def _on_btn_o_projektu_clicked(self):
        self.stacked_widget.setCurrentWidget(self.o_projektu_widget)

    # Analýza 1 - NAVIGACE ZMĚNA!
    # Nový slot pro tlačítko Pokračovat z výběru linky
    def _on_analyza1_linka_pokracovat_clicked(self):
        self.stacked_widget.setCurrentWidget(self.analyza1_den_widget)

    # Původní slot, který byl připojen k currentIndexChanged. Nyní se volá až po kliknutí na tlačítko "Pokračovat" z Linky.
    # Tento slot už primárně neslouží k navigaci.
    def _on_analyza1_linka_selected(self, index):
        # Tato metoda se nyní nevolá pro navigaci, pouze když by bylo potřeba reagovat na změnu linky
        # aniž by se ihned přešlo na další obrazovku.
        # V tomto případě, protože jsme odpojili connect, se tato metoda již NEBUDE VOLAT.
        # Můžete ji bezpečně smazat, nebo ponechat pro budoucí logiku (např. přednačtení dat).
        pass

    def _on_analyza1_den_selected(self, index):
        pass
    
    def _on_analyza1_den_pokracovat_clicked(self):
        self.stacked_widget.setCurrentWidget(self.analyza1_casovy_usek_widget)

    def _on_analyza1_casovy_usek_pokracovat_clicked(self):
        hodina_start = self.analyza1_hodina_start_spinbox.value()
        hodina_konec = self.analyza1_hodina_konec_spinbox.value()

        if hodina_start > hodina_konec:
            QMessageBox.warning(self, "Chybný vstup", "Počáteční hodina nesmí být větší než koncová hodina.")
        else:
            self.stacked_widget.setCurrentWidget(self.analyza1_delka_useku_widget)

    def _on_analyza1_proved_analizu_clicked(self):
        linka = self.analyza1_linky_combo.currentText()
        den = self.analyza1_dny_combo.currentText()
        hodina_start = self.analyza1_hodina_start_spinbox.value()
        hodina_konec = self.analyza1_hodina_konec_spinbox.value()
        delka_useku_text = self.analyza1_delka_useku_lineedit.text()

        if not delka_useku_text:
            QMessageBox.warning(self, "Chybný vstup", "Délka úseku nesmí být prázdná.")
            return
        
        try:
            delka_useku = int(delka_useku_text)
            if delka_useku <= 0:
                QMessageBox.warning(self, "Chybný vstup", "Délka úseku musí být kladné číslo.")
                return
        except ValueError:
            QMessageBox.warning(self, "Chybný vstup", "Délka úseku musí být celé číslo.")
            return

        QMessageBox.information(self, "Simulace Analýzy",
                                f"Simulace provedení analýzy rozložení zpoždění pro:<br>"
                                f"Linka: <b>{linka}</b><br>"
                                f"Den: <b>{den}</b><br>"
                                f"Časový interval: <b>{hodina_start}:00 - {hodina_konec}:00</b><br>"
                                f"Délka úseku: <b>{delka_useku} metrů</b><br>"
                                f"<i>(Zde by se zobrazily výsledky analýzy)</i>")

        self.stacked_widget.setCurrentWidget(self.main_menu_widget)

    # Návratová tlačítka pro Analýzu 1
    def _on_analyza1_zpet_linka_clicked(self):
        self.stacked_widget.setCurrentWidget(self.main_menu_widget)

    def _on_analyza1_zpet_den_clicked(self):
        self.stacked_widget.setCurrentWidget(self.analyza1_linka_widget)
        
    def _on_analyza1_casovy_usek_zpet_clicked(self):
        self.stacked_widget.setCurrentWidget(self.analyza1_den_widget)

    def _on_analyza1_delka_useku_zpet_clicked(self):
        self.stacked_widget.setCurrentWidget(self.analyza1_casovy_usek_widget)


    # Analýza 2 (beze změny)
    def _on_analyza2_uzel1_clicked(self):
        self.stacked_widget.setCurrentWidget(self.analyza2_linka_widget)

    def _on_analyza2_uzel2_clicked(self):
        self.stacked_widget.setCurrentWidget(self.analyza2_linka_widget)

    def _on_analyza2_linka_selected(self, index):
        self.stacked_widget.setCurrentWidget(self.analyza2_den_widget)

    def _on_analyza2_den_selected(self, index):
        pass

    def _on_analyza2_proved_analizu_clicked(self):
        linka = self.analyza2_linky_combo.currentText()
        den = self.analyza2_dny_combo.currentText()

        QMessageBox.information(self, "Simulace Analýzy",
                                f"Simulace provedení analýzy přestupních uzlů pro linku: <b>{linka}</b>, den: <b>{den}</b>.<br><i>(Zde by se zobrazily výsledky analýzy)</i>")

        self.stacked_widget.setCurrentWidget(self.main_menu_widget)

    def _on_analyza2_zpet_uzel_clicked(self):
        self.stacked_widget.setCurrentWidget(self.main_menu_widget)

    def _on_analyza2_zpet_linka_clicked(self):
        self.stacked_widget.setCurrentWidget(self.analyza2_uzel_widget)

    def _on_analyza2_zpet_den_clicked(self):
        self.stacked_widget.setCurrentWidget(self.analyza2_linka_widget)

    # O projektu (beze změny)
    def _on_o_projektu_zpet_clicked(self):
        self.stacked_widget.setCurrentWidget(self.main_menu_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())