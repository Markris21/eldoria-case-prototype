# Roadmap badań

## Cel

Roadmap opisuje kolejność najbliższych eksperymentów.

Nie jest harmonogramem produkcji gry. Każdy etap może zostać zmieniony, uproszczony albo odrzucony na podstawie wyników wcześniejszych testów.

## Etap 0 — Fundament projektu

### Cel

Przygotować repozytorium, zasady pracy i środowisko pozwalające szybko wykonywać kolejne eksperymenty.

### Zakres

- `README.md`,
- `AGENTS.md`,
- dziennik eksperymentów,
- decyzje projektowe,
- roadmap,
- minimalna konfiguracja Pythona,
- uruchamialny program bazowy,
- podstawowy test automatyczny.

### Warunek zakończenia

Na każdym wspieranym komputerze można pobrać repozytorium, uruchomić program i testy tymi samymi poleceniami.

---

## Etap 1 — Najmniejsza prawda przypadku

### Pytanie badawcze

Czy program potrafi sam złożyć jedną logiczną prawdę przypadku z małych, niezależnych elementów danych?

### Minimalny zakres

- jeden archetyp,
- jedno źródło problemu,
- kilka wariantów miejsca lub kontaktu,
- pacjent,
- prosty ciąg zdarzeń,
- seed,
- tekstowy raport techniczny przypadku.

### Poza zakresem

- wywiad,
- dialogi,
- leczenie,
- pełny model chorób,
- grafika.

### Warunek przejścia dalej

Wiele seedów tworzy spójne warianty bez ręcznej korekty każdego przypadku.

---

## Etap 2 — Walidator spójności

### Pytanie badawcze

Czy możemy automatycznie wykrywać niedozwolone lub sprzeczne kombinacje?

### Zakres

- wymagane elementy,
- relacje czasowe,
- zgodność kontaktu ze źródłem,
- sprzeczności,
- czytelny powód odrzucenia przypadku.

### Warunek przejścia dalej

Generator nie zwraca znanych typów błędnych przypadków jako poprawnych.

---

## Etap 3 — Uczestnicy i wiedza

### Pytanie badawcze

Czy wiedza różnych osób może wynikać z ich rzeczywistego udziału w historii?

### Zakres

- pacjent,
- co najmniej jeden dodatkowy uczestnik,
- fakty znane i nieznane,
- pochodzenie wiedzy,
- możliwość częściowej wiedzy.

### Warunek przejścia dalej

Rozmówcy posiadają różne, logicznie uzasadnione informacje bez arbitralnego rozdawania faktów.

---

## Etap 4 — Minimalny wywiad terminalowy

### Pytanie badawcze

Czy odkrywanie wygenerowanych faktów przez wybór rozmówcy i tematów daje podstawę sensownej dedukcji?

### Zakres

- zgłoszenie sprawy,
- wybór rozmówcy,
- lista kilku tematów,
- odpowiedzi wynikające wyłącznie z wiedzy rozmówcy,
- możliwość zakończenia wywiadu i pokazania prawdy przypadku.

### Warunek przejścia dalej

Wywiad wnosi realną informację i nie jest wyłącznie tekstową prezentacją wcześniej widocznych danych.

---

## Etap 5 — Hipotezy i rozwiązywalność

### Pytanie badawcze

Czy generator potrafi tworzyć sprawę, w której gracz może logicznie odróżnić poprawne wyjaśnienie od co najmniej jednej sensownej alternatywy?

### Zakres

- hipoteza właściwa,
- alternatywa,
- tropy wspierające i osłabiające,
- minimalny mechanizm postawienia diagnozy lub hipotezy.

### Warunek przejścia dalej

Przypadek można rozwiązać przez dostępne informacje bez zgadywania i bez jednego oczywistego zdania zdradzającego odpowiedź.

---

## Etap 6 — Różnorodność

### Pytanie badawcze

Czy generator tworzy realnie różne śledztwa, a nie tylko kosmetyczne warianty?

### Zakres

- seryjne generowanie,
- co najmniej setki seedów,
- analiza powtarzalności,
- porównanie struktur historii,
- wykrywanie dominujących schematów.

### Warunek przejścia dalej

Znacząca część przypadków różni się przebiegiem informacji lub tokiem dedukcji, nie tylko nazwami.

---

## Etap 7 — Rozszerzanie domeny

Dopiero po pozytywnym wyniku wcześniejszych etapów dodajemy kolejne archetypy, źródła i rodzaje problemów.

Każde rozszerzenie powinno sprawdzić, czy nową zawartość można dodać głównie przez dane i istniejące reguły.

## Etap 8 — Ocena strategiczna

Po zebraniu wystarczającej liczby eksperymentów podejmujemy decyzję:

- kontynuować pełny generator proceduralny,
- stosować model hybrydowy,
- ograniczyć proceduralność,
- wrócić do ręcznie projektowanych przypadków,
- zmienić kierunek Eldorii, jeśli rdzeń nie spełnia oczekiwań.

Negatywny wynik na tym etapie jest sukcesem badawczym, jeżeli pozwala uniknąć inwestowania czasu w nieskuteczny kierunek.
