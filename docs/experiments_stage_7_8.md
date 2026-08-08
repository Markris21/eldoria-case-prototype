# Dziennik eksperymentów — Etapy 7–8

## Cel dokumentu

Ten plik kontynuuje `docs/experiments.md`, który osiągnął rozmiar wymagający podziału zgodnie z DEC-006.

Dokument zapisuje wynik kontrolowanego rozszerzenia domeny oraz ocenę strategiczną prototypu R&D.

---

## Etap 7 — Kontrolowane rozszerzenie domeny

**Status:** POTWIERDZONA

### Hipoteza

Nowy, rzeczywiście inny archetyp przypadku można dodać bez tworzenia osobnego generatora i osobnego pipeline'u śledztwa, wykorzystując istniejące mechanizmy faktów, zdarzeń, wiedzy, provenance, wywiadu i oceny hipotez.

Nowy archetyp powinien również tworzyć inną ścieżkę dedukcji, a nie tylko nowy zestaw nazw i kontaktów.

### Metoda

Do prototypu dodano dokładnie jeden nowy archetyp: `biological_carrier_contact`.

W biologicznym przypadku:

- pacjent ma bliski kontakt z drugą osobą,
- druga osoba była widocznie chora wcześniej,
- pacjent staje się chory później,
- pełna prawda przypadku przechowuje biologiczny kontakt jako ukrytą przyczynę,
- fakty widoczne dla uczestników nie stwierdzają wprost zakażenia, transmisji ani roli nosiciela.

Do reprezentacji dodano minimalne dane dotyczące uczestnika kontaktu, czasu jego wcześniejszego stanu i obserwatorów tego stanu.

Istniejący mechanizm `derive_knowledge()` i provenance zdarzeń został ponownie użyty bez osobnego systemu wiedzy.

Istniejący wywiad i mechanizm `is_correct_hypothesis()` zostały ponownie użyte. Dodano tylko temat dotyczący wcześniejszego stanu drugiej osoby oraz biologiczną hipotezę.

### Ścieżka dedukcji

Przypadki środowiskowe nadal opierają się głównie na schemacie:

`kontakt -> historia jedzenia -> porównanie dwóch hipotez`

Nowy archetyp wykorzystuje inną ścieżkę:

`kontakt z osobą -> wcześniejszy widoczny stan tej osoby -> chronologia -> porównanie hipotez`

Nie ma w nim zdarzenia `food_history` jako podstawowego faktu rozróżniającego.

### Wynik techniczny

Po poprawce usuwającej przeciek ukrytej roli `carrier` z menu gracza pełny zestaw testów zakończył się wynikiem `202 passed`.

Ręczny test dla seeda `1` pokazał:

- pacjent Mira spotkała Lysę,
- Lysa była widocznie chora wcześniej,
- odpowiedzi nie mówiły, że Lysa zaraziła Mirę,
- gracz mógł połączyć kontakt i chronologię i wybrać hipotezę biologiczną,
- wewnętrzna rola `carrier` pozostała ukrytą prawdą, a w menu gracza Lysa jest neutralnym `participant`.

### Koszt rozszerzenia domeny

Nie powstał osobny generator ani osobny pipeline wywiadu.

Ponownie wykorzystano:

- zdarzenia i `CaseTruth`,
- mechanizm wyprowadzania wiedzy,
- provenance,
- filtrowanie odpowiedzi wywiadu,
- listę odkryć gracza,
- ocenę poprawności hipotezy względem ukrytej prawdy,
- analizę różnorodności.

Konieczne były małe, jawne branche archetypowe dotyczące:

- składu zdarzeń biologicznych,
- wyboru kontaktu i źródła,
- generowania hipotez,
- sposobu opisu struktury dedukcji w analizie różnorodności.

Na obecnym poziomie koszt ten jest akceptowalny i nie uzasadnia budowania ogólnego frameworka archetypów na zapas.

### Wpływ na różnorodność

Bazowy wynik Etapu 6:

- `500` seedów,
- `118` konkretnych przypadków,
- `2` struktury śledztwa,
- dominująca struktura `67.0%`.

Po dodaniu archetypu biologicznego:

- `500` seedów,
- `162` konkretne przypadki,
- `3` struktury śledztwa,
- biologiczna chronologia: `250/500` (`50.0%`),
- środowiskowa struktura eliminująca alternatywę: `173/500` (`34.6%`),
- środowiskowa struktura wspierająca poprawną hipotezę: `77/500` (`15.4%`).

Nowa struktura nie wynika z ID archetypu ani konkretnej treści kontaktu. Wynika z innego wzorca wiedzy oraz innej roli faktu rozróżniającego w dedukcji.

### Ograniczenia wyniku

Etap 7 testuje tylko jeden dodatkowy archetyp.

Nie potwierdza jeszcze skalowania do kilkunastu lub kilkudziesięciu archetypów ani jakości długoterminowej rozgrywki.

Przepływ wywiadu nadal ma znane ograniczenia: wszystkie tematy są widoczne od początku, rozmowa wraca do wyboru rozmówcy po każdym pytaniu, a tekst odpowiedzi jest techniczny.

Nie testowano chorób, patogenów, inkubacji, badań laboratoryjnych, dowodów fizycznych ani leczenia.

### Wniosek

Etap 7 został potwierdzony na aktualnym poziomie eksperymentu.

Kontrolowane rozszerzenie domeny jest możliwe bez duplikowania całego pipeline'u, a nowy archetyp może stworzyć rzeczywiście nową ścieżkę dedukcji.

---

## Etap 8 — Ocena strategiczna

**Status:** POTWIERDZONA

### Pytanie

Czy wyniki prototypu uzasadniają dalszy rozwój proceduralnego generatora przypadków dla Eldorii, a jeśli tak, w jakim modelu?

### Potwierdzone wyniki

Prototyp pokazał, że:

- spójną prawdę przypadku można składać z małych danych i reguł,
- znane sprzeczności można automatycznie walidować,
- wiedza NPC może wynikać z uczestnictwa i obserwacji zdarzeń,
- pełną prawdę można oddzielić od faktów obserwowalnych,
- gracz może zaczynać z niepełną wiedzą i odkrywać informacje przez działania,
- minimalna dedukcja między poprawną i sensowną alternatywną hipotezą działa,
- strukturalną różnorodność śledztw można mierzyć niezależnie od kosmetycznej różnorodności danych,
- dodanie nowego archetypu może ponownie używać istniejących mechanizmów i jednocześnie tworzyć nową ścieżkę dedukcji.

### Najważniejszy negatywny wynik

Etap 6 pokazał, że duża liczba kombinacji danych nie daje automatycznie dużej różnorodności gameplayu.

Przed rozszerzeniem domeny `118` różnych konkretnych przypadków dawało tylko `2` bardzo podobne struktury śledztwa.

Oznacza to, że samo dokładanie nazw, miejsc, kontaktów i źródeł nie wystarczy.

### Decyzja strategiczna

**GO — kontynuować koncepcję proceduralnego generatora przypadków.**

Nie rozwijamy jednak modelu jako całkowicie uniwersalnego generatora dowolnych historii.

Rekomendowany kierunek to:

**proceduralny generator oparty na kontrolowanych archetypach śledztwa.**

Archetyp określa charakterystyczną strukturę problemu i możliwy tok dedukcji, a generator proceduralnie tworzy konkretne osoby, miejsca, wydarzenia, chronologię, źródła, obserwatorów, fakty i warianty.

### Konsekwencje

Dalsze archetypy powinny być projektowane świadomie pod kątem innego toku śledztwa, np.:

- ekspozycja środowiskowa,
- kontakt biologiczny,
- zatrucie,
- pasożyt,
- uraz z nieoczywistą przyczyną,
- skażenie magiczne,
- inne przyszłe kategorie, jeśli wymagają odmiennego rozumowania.

Nowa zawartość nie powinna być uznawana za zwiększenie różnorodności tylko dlatego, że zmienia dane lub narracyjne opakowanie.

Analizator różnorodności powinien pozostać narzędziem regresyjnym do sprawdzania, czy nowe mechaniki faktycznie tworzą nowe ścieżki gameplayu.

### Czego decyzja nie oznacza

Ta decyzja nie oznacza, że obecny kod prototypu jest finalną architekturą Eldorii.

Nie oznacza też, że generator jest już gotowy do przeniesienia w całości do głównego projektu.

Do głównej Eldorii powinny trafiać przede wszystkim potwierdzone modele i wnioski, a kod tylko tam, gdzie jego ponowne użycie ma realną wartość.

### Największe pozostałe ryzyka

Przed uznaniem systemu za gotowy gameplayowo nadal trzeba sprawdzić przede wszystkim:

- warunkowe pojawianie się pytań i działań na podstawie odkrytych informacji,
- bardziej naturalny przebieg jednej rozmowy,
- badania i dowody poza samym wywiadem,
- więcej niż dwie sensowne hipotezy,
- trudność i czytelność dedukcji,
- różnorodność po dodaniu wielu archetypów,
- zachowanie ciekawości systemu po wielu godzinach gry.

### Wniosek końcowy

Prototyp R&D spełnił główny cel pierwszego cyklu badań: wykazał, że proceduralne przypadki oparte na faktach, zdarzeniach, rozdzielonej wiedzy i kontrolowanych archetypach śledztwa są technicznie i gameplayowo obiecującym kierunkiem dla Eldorii.

Następne prace powinny rozwijać ten model poprzez kolejne małe eksperymenty, a nie przez budowę finalnego silnika na zapas.
