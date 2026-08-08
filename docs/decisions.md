# Decyzje projektowe

## Cel dokumentu

Ten plik zawiera decyzje, które są na tyle trwałe, aby kierować dalszą pracą nad prototypem.

Pomysły i niepotwierdzone hipotezy powinny trafiać do `docs/experiments.md`, nie tutaj.

---

## DEC-001 — Osobne repozytorium prototypu

**Status:** ZATWIERDZONA

### Decyzja

Generator przypadków jest rozwijany w osobnym repozytorium `eldoria-case-prototype`, niezależnie od głównego repozytorium Eldorii.

### Powód

Prototyp ma charakter eksperymentalny. Kod może być wielokrotnie przepisywany, upraszczany lub całkowicie odrzucany bez wpływu na główny projekt gry.

### Konsekwencje

- główne repozytorium Eldorii pozostaje czyste,
- prototyp może używać innej technologii niż finalna gra,
- do Eldorii przenosimy przede wszystkim potwierdzone wnioski i modele, niekoniecznie kod.

---

## DEC-002 — Python jako język prototypu

**Status:** ZATWIERDZONA

### Decyzja

Pierwsza wersja prototypu jest tworzona w Pythonie 3.

### Powód

Python pozwala szybko zmieniać model danych i logikę generatora, łatwo uruchamia się na słabszym Chromebooku i dobrze nadaje się do testów seryjnych.

### Konsekwencje

- kod prototypu może nie zostać bezpośrednio użyty w finalnej grze,
- szybkość iteracji jest ważniejsza niż zgodność technologiczna z przyszłym silnikiem Eldorii.

---

## DEC-003 — Terminal jako pierwszy interfejs

**Status:** ZATWIERDZONA

### Decyzja

Pierwszy grywalny prototyp działa w terminalu.

### Powód

Celem jest testowanie generatora, faktów, wiedzy, pytań, odpowiedzi i dedukcji, a nie grafiki ani finalnego UI.

### Konsekwencje

- brak JavaFX i GUI na tym etapie,
- interfejs może być prosty i techniczny,
- łatwo uruchomić prototyp na Chromebooku, laptopie i komputerze w pracy.

---

## DEC-004 — GitHub jako źródło prawdy

**Status:** ZATWIERDZONA

### Decyzja

Repozytorium GitHub jest jedynym źródłem prawdy projektu.

### Powód

Projekt ma być rozwijany z wielu urządzeń i przez kilka narzędzi AI.

### Konsekwencje

- lokalne zmiany powinny być regularnie commitowane i publikowane,
- decyzje i eksperymenty należy zapisywać w repozytorium,
- pamięć rozmów nie zastępuje dokumentacji.

---

## DEC-005 — Kod jako narzędzie badawcze

**Status:** ZATWIERDZONA

### Decyzja

Nie projektujemy finalnego silnika na zapas. Każdy etap implementacji ma służyć weryfikacji konkretnej hipotezy lub technicznego założenia.

### Powód

Największym ryzykiem projektu jest nie to, czy umiemy napisać kod, lecz czy proceduralne przypadki będą spójne, różnorodne i ciekawe.

### Konsekwencje

- preferowane są małe eksperymenty,
- dopuszczamy wyrzucanie kodu,
- nie tworzymy abstrakcji i modułów bez bieżącej potrzeby.

---

## DEC-006 — Ograniczenie rozmiaru dokumentów

**Status:** ZATWIERDZONA

### Decyzja

Dokument Markdown powinien mieć maksymalnie około 300 linii.

### Powód

Mniejsze dokumenty są łatwiejsze do przeglądania, aktualizacji i używania przez ludzi oraz agentów AI.

### Konsekwencje

Po zbliżeniu się do limitu dokument należy podzielić według odpowiedzialności zamiast stale go rozbudowywać.

---

## DEC-007 — Kontrolowane archetypy śledztwa

**Status:** ZATWIERDZONA

### Decyzja

Dalszy rozwój proceduralnego generatora przypadków będzie oparty na kontrolowanych archetypach śledztwa.

Nie próbujemy budować całkowicie uniwersalnego generatora dowolnych historii ani wracać do ręcznego pisania każdego przypadku.

Archetyp ma definiować charakterystyczny typ problemu i tok dedukcji, natomiast generator proceduralnie składa konkretne osoby, miejsca, zdarzenia, chronologię, źródła, obserwatorów, fakty i warianty.

### Powód

Pierwszy cykl badań potwierdził, że prawda przypadku, wiedza uczestników i dedukcja mogą wynikać z danych i zdarzeń.

Jednocześnie analiza różnorodności wykazała, że duża liczba kombinacji danych nie przekłada się automatycznie na różne ścieżki gameplayu.

Kontrolowane archetypy pozwalają świadomie projektować różne rodzaje rozumowania, zachowując proceduralną różnorodność wewnątrz każdego archetypu.

### Konsekwencje

- nowe archetypy powinny wnosić rzeczywistą różnicę w przebiegu śledztwa lub dedukcji,
- sama zmiana nazw, miejsc, kontaktów lub źródeł nie jest traktowana jako nowa struktura gameplayu,
- istniejący analizator różnorodności pozostaje narzędziem kontroli regresji,
- małe jawne branche archetypowe są dopuszczalne w prototypie, jeśli nie prowadzą do duplikowania całego pipeline'u,
- nie budujemy ogólnego frameworka archetypów, dopóki kolejne eksperymenty nie pokażą realnej potrzeby,
- do głównej Eldorii przenosimy przede wszystkim potwierdzone modele i wnioski, a nie automatycznie cały kod prototypu.
