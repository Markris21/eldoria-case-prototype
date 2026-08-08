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

**Status:** POTWIERDZONA

### Hipoteza

Ciekawy przypadek może być zbudowany przez generator z kontrolowanych faktów, zdarzeń, uczestników i zależności zamiast z gotowego, ręcznie napisanego scenariusza.

### Oczekiwany test

Minimalny generator powinien samodzielnie stworzyć prawdę przypadku z prostego zbioru danych i reguł, bez ręcznego napisania konkretnej historii.

### Kryterium pozytywne

Wygenerowany przypadek jest logiczny i można wskazać, które reguły oraz dane doprowadziły do jego powstania.

### Kryterium negatywne

Większość sensownych historii wymaga ręcznego dopisywania konkretnych sekwencji zdarzeń albo wyjątków w kodzie.

### Metoda

Zaimplementowano minimalny generator pełnej prawdy przypadku oparty na seedzie.

Generator składa przypadek z małych elementów danych:

- pacjenta,
- jednego źródła problemu,
- miejsca kontaktu,
- sposobu kontaktu,
- prostego ciągu zdarzeń,
- łańcucha przyczynowego.

Zgodność kontaktu z miejscem wynika z prostej reguły dozwolonych kombinacji. Generator nie przechowuje i nie losuje gotowych kompletnych scenariuszy.

Wykonano testy automatyczne oraz ręczny przegląd 20 kolejnych seedów od 100 do 119.

### Wynik

Testy automatyczne zakończyły się wynikiem `122 passed`.

W ręcznie przejrzanych 20 przypadkach nie znaleziono nielogicznych kombinacji miejsca, sposobu kontaktu ani łańcucha przyczynowego.

Różne seedy tworzyły różne kombinacje pacjenta, miejsca i sposobu kontaktu, a ten sam seed pozostawał odtwarzalny.

Eksperyment pokazał, że na tym poziomie można zbudować spójną prawdę przypadku przez składanie danych i prostych reguł bez ręcznego pisania każdego przypadku.

### Ograniczenia wyniku

Struktura ciągu wydarzeń pozostaje obecnie sztywna. Zmieniają się elementy przypadku, ale przebieg zdarzeń korzysta z tego samego schematu.

EXP-001 nie potwierdza jeszcze, że generator tworzy różnorodne lub ciekawe historie, dobrą dedukcję ani że model będzie skalował się na wiele źródeł i problemów.

### Wniosek

Hipoteza została potwierdzona na aktualnym poziomie eksperymentu.

Możemy przejść do badania kolejnego ryzyka bez rozbudowywania EXP-001 na zapas.

---

## Etap 2 — Minimalny walidator spójności

**Status:** POTWIERDZONA

### Hipoteza

Prosty, niezależny krok walidacji może wykrywać znane błędne lub sprzeczne przypadki i wskazywać konkretny powód odrzucenia bez automatycznej naprawy danych.

### Metoda

Dodano minimalny `validate_case(case)`, który zwraca wynik `VALID` albo `INVALID` wraz z powodami.

Eksperyment celowo obejmował tylko trzy typy błędów:

- niedozwolone połączenie miejsca i sposobu kontaktu,
- brak wymaganej wartości,
- skutek występujący przed kontaktem.

Walidator korzysta z istniejącej reguły kompatybilności miejsca i kontaktu zamiast duplikować ją w osobnej tabeli.

Do `CaseTruth` dodano tylko strukturalne pola czasu potrzebne do sprawdzenia minimalnej chronologii. Nie zbudowano ogólnego silnika osi czasu ani reguł.

### Wynik

Po poprawce dotyczącej efektu występującego tego samego dnia pełny zestaw testów zakończył się wynikiem `127 passed`.

Ręczna demonstracja na lokalnym `main` poprawnie zwróciła:

- jeden wygenerowany przypadek jako `VALID`,
- niedozwolone połączenie miejsca i kontaktu jako `INVALID`,
- brak pacjenta jako `INVALID`,
- skutek wcześniejszy niż kontakt jako `INVALID`.

Każdy błędny przypadek podał właściwy powód odrzucenia.

### Ograniczenia wyniku

Walidator potwierdza wyłącznie możliwość wykrywania znanych klas błędów na obecnym małym modelu.

Nie potwierdza jeszcze kompletności walidacji, skalowania do rozbudowanej domeny ani potrzeby tworzenia ogólnego silnika reguł.

Efekt w tym samym dniu co kontakt jest celowo dopuszczony, ponieważ eksperyment nie ustanawia dodatkowej reguły domenowej dotyczącej minimalnego czasu wystąpienia skutku.

### Wniosek

Etap 2 został potwierdzony na aktualnym poziomie eksperymentu.

Możemy przejść do badania uczestników i rozdzielania wiedzy bez dalszego rozbudowywania walidatora na zapas.

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

EXP-001 potwierdził składanie minimalnej prawdy przypadku, a Etap 2 potwierdził możliwość niezależnego wykrywania znanych sprzeczności.

Następny eksperyment powinien sprawdzić EXP-002: czy wiedza uczestników może wynikać z ich rzeczywistego udziału w historii zamiast z arbitralnego przypisywania informacji.
