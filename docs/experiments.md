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

**Status:** POTWIERDZONA

### Hipoteza

Rozdzielenie faktów między uczestników na podstawie ich rzeczywistego udziału i obserwacji zdarzeń może tworzyć różną, logicznie uzasadnioną wiedzę bez ręcznego przypisywania list informacji do ról.

### Metoda

Do minimalnej prawdy przypadku dodano jednego świadka różnego od pacjenta oraz strukturalne rekordy zdarzeń zawierające uczestników i obserwatorów.

Wiedza jest wyprowadzana przez jedną funkcję na podstawie zdarzeń, w których dana osoba uczestniczyła albo które obserwowała.

Każdy znany fakt zachowuje `source_event_id`, dzięki czemu można wskazać zdarzenie będące źródłem wiedzy.

Pacjent uczestniczy w zdarzeniu obecności, kontakcie i późniejszym skutku. Świadek uczestniczy w zdarzeniu obecności i obserwuje kontakt, ale nie uczestniczy ani nie obserwuje późniejszego skutku.

### Wynik

Po poprawce usuwającej przeciek pełnej prawdy do wiedzy uczestników pełny zestaw testów zakończył się wynikiem `155 passed`.

Test behawioralny potwierdził, że usunięcie świadka z obserwatorów kontaktu usuwa z jego wiedzy fakt kontaktu.

Ręczna demonstracja na lokalnym `main` dla seeda `18472` pokazała:

- pacjent zna swoją obecność w miejscu, obserwowalny kontakt oraz późniejszy skutek,
- świadek zna obecność pacjenta i obserwowalny kontakt,
- świadek nie zna późniejszego skutku,
- ani pacjent, ani świadek nie otrzymują automatycznie informacji, że kontakt dotyczył skażonego źródła,
- pełna prawda przypadku nadal zachowuje źródło i skażenie.

### Ważna obserwacja z testu ręcznego

Pierwsza wersja eksperymentu ujawniała uczestnikom informację diagnostyczną, ponieważ tekst zdarzenia kontaktu zawierał określenie skażenia.

Zostało to rozdzielone na pełną prawdę przypadku oraz obserwowalną czynność. Dzięki temu fakt znany uczestnikowi opisuje to, co mógł rzeczywiście zaobserwować, bez automatycznego ujawniania ukrytej przyczyny.

### Ograniczenia wyniku

Eksperyment obejmuje tylko jednego pacjenta, jednego świadka i kilka prostych zdarzeń.

Nie potwierdza jeszcze wartości gameplayowej wywiadu, częściowej wiedzy, błędnej interpretacji, pamięci, kłamstw ani wnioskowania przez uczestników.

Nie potwierdza również, że każda przyszła informacja może być bezpiecznie reprezentowana bez dodatkowego rozdzielenia prawdy świata od informacji obserwowalnej.

### Wniosek

EXP-002 został potwierdzony na aktualnym poziomie eksperymentu.

Wiedza może wynikać z udziału i obserwacji zdarzeń oraz zachowywać pochodzenie informacji bez ręcznego przypisywania list wiedzy do ról.

---

## EXP-003 — Generator śledztwa, a nie tylko choroby

**Status:** POTWIERDZONA

### Hipoteza

Generator powinien tworzyć nie tylko stan medyczny pacjenta, ale również historię kontaktów, uczestników, źródła informacji i tropy potrzebne do rozwiązania sprawy.

### Oczekiwany test

Przypadek powinien posiadać pełną prawdę, ale gracz początkowo otrzymuje tylko jej część i odkrywa kolejne informacje przez działania.

### Kryterium pozytywne

Rozwiązanie wymaga połączenia kilku informacji, a sama lista objawów nie ujawnia odpowiedzi.

### Kryterium negatywne

Narracyjna warstwa nie wnosi decyzji i można równie dobrze wyświetlić od razu techniczną kartę pacjenta.

### Metoda

Dodano minimalny terminalowy wywiad oparty wyłącznie na wiedzy uczestników potwierdzonej w EXP-002.

Gracz rozpoczyna od krótkiego raportu przypadku, który informuje jedynie, że pacjent zachorował po niedawnym wyjściu. Raport nie ujawnia miejsca, sposobu kontaktu, źródła, skażenia ani pełnego łańcucha przyczynowego.

Gracz może wybrać pacjenta albo świadka oraz jeden z trzech tematów:

- gdzie wydarzenie miało miejsce,
- co wydarzyło się podczas kontaktu,
- co wydarzyło się później.

Odpowiedzi są filtrowane z `KnownFact` rozmówcy przez istniejące identyfikatory zdarzeń. Funkcja odpowiedzi nie otrzymuje pełnego `CaseTruth`, dzięki czemu ukryta prawda nie jest dostępna jako skrót do generowania odpowiedzi.

Fakty odkryte przez gracza są zapisywane tylko wtedy, gdy zostały rzeczywiście zwrócone podczas wywiadu.

### Wynik

Po poprawce semantyki pytania o miejsce pełny zestaw testów zakończył się wynikiem `168 passed`.

Ręczny test gameplayu dla seeda `18472` pokazał, że:

- początkowe zgłoszenie nie wystarcza do poznania pełnej prawdy,
- pacjent ujawnia miejsce, obserwowalny kontakt i późniejszy skutek,
- świadek ujawnia miejsce i obserwowalny kontakt,
- świadek odpowiada `I don't know.` na pytanie o późniejszy stan,
- żadna odpowiedź nie ujawnia zarodników redcap ani skażenia,
- powtarzające się informacje nie są duplikowane w `PLAYER DISCOVERIES`,
- po zakończeniu wywiadu pełna prawda pokazuje informacje, których gracz wcześniej nie znał.

### Ważna obserwacja z testu ręcznego

Pierwsza wersja pytania o miejsce brzmiała `Where were you?`, ale świadek odpowiadał faktem dotyczącym miejsca pobytu pacjenta. Fakt był prawdziwy, lecz nie odpowiadał semantycznie na pytanie.

Temat zmieniono na neutralne `Where did this happen?`, które poprawnie pasuje do tego samego faktu zarówno dla pacjenta, jak i świadka bez tworzenia odpowiedzi zależnych od roli.

### Ograniczenia wyniku

Eksperyment używa tylko dwóch rozmówców i trzech tematów. Odpowiedzi są bezpośrednią prezentacją technicznych faktów, a nie naturalnym dialogiem.

Nie testowano jeszcze jakości języka, osobowości, swobodnych pytań, kłamstw, niepewności, pamięci, dowodów fizycznych, alternatywnych hipotez ani diagnozy.

W szczególności tekst `The exposure affected Oren.` jest wystarczający do testu przepływu informacji, ale nie jest docelową wypowiedzią NPC.

EXP-003 potwierdza istnienie podstawowej pętli odkrywania informacji, nie potwierdza jeszcze, że śledztwo jest wystarczająco głębokie lub ciekawe jako docelowy gameplay.

### Wniosek

EXP-003 został potwierdzony na aktualnym poziomie eksperymentu.

Gracz może rozpocząć z niepełną wiedzą i zwiększać ją przez celowy wybór rozmówcy oraz tematu, a odpowiedzi pozostają ograniczone do wiedzy rozmówcy.

---

## Następny eksperyment

EXP-001 potwierdził składanie minimalnej prawdy przypadku, Etap 2 potwierdził wykrywanie znanych sprzeczności, EXP-002 potwierdził wyprowadzanie wiedzy uczestników, a EXP-003 potwierdził minimalną pętlę odkrywania informacji przez wywiad.

Następny krok powinien sprawdzić kolejne ryzyko z roadmapy: czy przypadek można rozwiązać przez odróżnienie poprawnej hipotezy od sensownej alternatywy na podstawie dostępnych informacji, bez zgadywania.