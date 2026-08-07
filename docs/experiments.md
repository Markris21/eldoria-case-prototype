# Dziennik eksperymentów

## Cel dokumentu

Ten plik zapisuje historię badań prowadzonych w projekcie.

Nie służy do opisywania finalnej architektury. Ma zachować informacje o tym:

- co chcieliśmy sprawdzić,
- jak to sprawdziliśmy,
- jaki był wynik,
- czego się nauczyliśmy,
- czy hipoteza została potwierdzona, odrzucona czy nadal jest testowana.

## Statusy

- `TESTOWANA` — eksperyment trwa albo nie mamy jeszcze wystarczających danych.
- `POTWIERDZONA` — wynik daje wystarczające podstawy, aby używać hipotezy w dalszych pracach.
- `ODRZUCONA` — eksperyment pokazał, że hipoteza nie działa wystarczająco dobrze.

Potwierdzenie w prototypie nie oznacza, że rozwiązanie jest finalną architekturą gry. Oznacza jedynie, że sprawdziło się wystarczająco dobrze na aktualnym poziomie testu.

---

## EXP-000 — Dlaczego istnieje osobny prototyp

**Status:** POTWIERDZONA

### Hipoteza

Największe ryzyko Eldorii należy sprawdzić przed dalszą rozbudową głównego silnika gry.

### Problem

Możliwe jest zbudowanie poprawnego technicznie modelu pacjenta, alchemii i świata, a następnie odkrycie, że proceduralnie tworzone przypadki są nudne, powtarzalne albo niespójne narracyjnie.

### Metoda

Wydzielono osobne repozytorium R&D przeznaczone wyłącznie do eksperymentowania z generowaniem przypadków i śledztw diagnostycznych.

### Wynik

Prototyp może być rozwijany niezależnie od finalnego silnika Eldorii i może zostać swobodnie przebudowany lub odrzucony.

### Wniosek

Najpierw należy zweryfikować rdzeń generowania przypadków. Dopiero pozytywne wyniki powinny wpływać na docelową architekturę Eldorii.

---

## EXP-001 — Fakty zamiast ręcznie pisanych historii

**Status:** TESTOWANA

### Hipoteza

Ciekawy przypadek może być zbudowany przez generator z kontrolowanych faktów, zdarzeń, uczestników i zależności zamiast z gotowego, ręcznie napisanego scenariusza.

### Oczekiwany test

Minimalny generator powinien samodzielnie stworzyć prawdę przypadku z prostego zbioru danych i reguł, bez ręcznego napisania konkretnej historii.

### Kryterium pozytywne

Wygenerowany przypadek jest logiczny i można wskazać, które reguły oraz dane doprowadziły do jego powstania.

### Kryterium negatywne

Większość sensownych historii wymaga ręcznego dopisywania konkretnych sekwencji zdarzeń albo wyjątków w kodzie.

### Wynik

Jeszcze nie wykonano testu implementacyjnego.

---

## EXP-002 — Rozdzielona wiedza uczestników

**Status:** TESTOWANA

### Hipoteza

Rozdzielenie faktów między pacjenta, rodzinę i świadków może tworzyć wartościową dedukcję podczas wywiadu.

### Oczekiwany test

Generator utworzy przypadek z kilkoma uczestnikami, a system przypisze im wiedzę wynikającą z ich udziału w wydarzeniach.

Gracz w terminalu będzie mógł wybierać rozmówcę i temat pytania.

### Kryterium pozytywne

Informacje od różnych osób realnie zmieniają rozumienie przypadku i nie sprowadzają się do wielokrotnego powtarzania tych samych danych.

### Kryterium negatywne

Optymalna strategia polega na mechanicznym przepytaniu wszystkich osób ze wszystkich tematów albo dodatkowi rozmówcy nie wnoszą wartości.

### Wynik

Jeszcze nie wykonano testu implementacyjnego.

---

## EXP-003 — Generator śledztwa, a nie tylko choroby

**Status:** TESTOWANA

### Hipoteza

Generator powinien tworzyć nie tylko stan medyczny pacjenta, ale również historię kontaktów, uczestników, źródła informacji i tropy potrzebne do rozwiązania sprawy.

### Oczekiwany test

Przypadek powinien posiadać pełną prawdę, ale gracz początkowo otrzymuje tylko jej część i odkrywa kolejne informacje przez działania.

### Kryterium pozytywne

Rozwiązanie wymaga połączenia kilku informacji, a sama lista objawów nie ujawnia odpowiedzi.

### Kryterium negatywne

Narracyjna warstwa nie wnosi decyzji i można równie dobrze wyświetlić od razu techniczną kartę pacjenta.

### Wynik

Jeszcze nie wykonano testu implementacyjnego.

---

## Następny eksperyment

Pierwszy eksperyment implementacyjny powinien być możliwie mały.

Nie budujemy jeszcze pełnego terminalowego wywiadu.

Najpierw chcemy odpowiedzieć na pytanie:

> Czy program potrafi samodzielnie złożyć jedną spójną prawdę przypadku z małego zestawu danych i reguł?
