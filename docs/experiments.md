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

## Etap 5 — Hipotezy i rozwiązywalność

**Status:** POTWIERDZONA

### Hipoteza

Przypadek może zawierać jedną poprawną hipotezę i co najmniej jedną sensowną alternatywę, które gracz potrafi rozróżnić przez odkryte fakty zamiast przez zgadywanie.

### Metoda

Do istniejącego przypadku dodano dokładnie dwie hipotezy: jedną odpowiadającą rzeczywistemu `contact_id` w `CaseTruth` oraz jedną alternatywną.

Ocena wyboru gracza porównuje wyłącznie wybraną hipotezę z ukrytą prawdą przypadku. Odkrycia gracza nie są używane przez program do automatycznej dedukcji i nie istnieje tabela typu „trop wspiera odpowiedź A”.

Dodano strukturalne zdarzenie `food_history`. Dla przypadku wodnego z seeda `18472` pacjent wie, że nie jadł nic podczas pobytu w lesie. Fakt zachowuje pochodzenie w systemie zdarzeń i jest odkrywany przez ten sam mechanizm wiedzy co wcześniejsze informacje.

Do wywiadu dodano jeden temat dotyczący jedzenia. Pacjent może ujawnić ten fakt, natomiast świadek bez odpowiedniej wiedzy odpowiada `I don't know.`.

### Wynik

Pełny zestaw testów zakończył się wynikiem `178 passed`.

Ręczny test dla seeda `18472` pokazał, że:

- początkowy raport nie sugeruje wody ani jedzenia,
- informacja, że Oren pił wodę, wskazuje istotny kierunek, ale sama nie wyklucza alternatywy związanej z jedzeniem,
- informacja, że Oren nie jadł nic podczas pobytu w lesie, osłabia hipotezę dotyczącą jedzenia,
- żadna odpowiedź nie ujawnia wprost skażenia ani zarodników,
- gracz może wybrać hipotezę dotyczącą skażonej wody na podstawie odkrytych informacji,
- poprawność wyboru jest sprawdzana względem `CaseTruth`, a nie względem ręcznie przypisanych tropów.

W ręcznym teście poprawna hipoteza została wybrana bez konieczności poznania pełnej prawdy przypadku.

### Ważne obserwacje gameplayowe

Test ujawnił dwa problemy, które nie unieważniają wyniku Etapu 5, ale mogą prowadzić do mechanicznego przepytywania zamiast naturalnego śledztwa:

- wszystkie tematy są dostępne od początku, nawet jeśli wcześniejsze odpowiedzi nie dały jeszcze graczowi powodu, aby o nie pytać; przykładowo pytanie o jedzenie jest dostępne zanim gracz dowie się, gdzie wydarzenie miało miejsce,
- po każdym pytaniu interfejs wraca do wyboru rozmówcy, przez co jedna rozmowa jest sztucznie przerywana; naturalniejszy przepływ powinien pozwalać kontynuować pytania z wybraną osobą i wrócić do listy rozmówców dopiero na żądanie gracza.

Istotna jest również pozytywna obserwacja: odkrycie picia wody nie podaje rozwiązania wprost, lecz daje graczowi powód, aby zainteresować się wodą i w przyszłości wykonać dalsze badania lub szukać dowodów.

### Ograniczenia wyniku

Eksperyment obejmuje dokładnie dwie hipotezy i jeden dodatkowy fakt rozróżniający.

Alternatywy nadal są budowane z bardzo małej domeny kontaktów, więc wynik nie potwierdza jeszcze jakości wielu hipotez, skalowania, trudności dedukcji ani różnorodności spraw.

Obecny interfejs tematów może sugerować graczowi kierunek śledztwa przez sam fakt wyświetlenia wszystkich dostępnych pytań. Nie potwierdzono jeszcze modelu, w którym kolejne pytania lub działania stają się dostępne jako konsekwencja wcześniej odkrytych informacji.

Etap 5 nie testuje również badań środowiskowych, dowodów fizycznych, laboratoryjnego potwierdzenia źródła, punktacji dowodów ani pełnej diagnozy.

### Wniosek

Etap 5 został potwierdzony na aktualnym poziomie eksperymentu.

Minimalny przypadek może wymagać połączenia kilku odkrytych informacji, aby odróżnić poprawną hipotezę od sensownej alternatywy, bez ujawniania odpowiedzi w jednym oczywistym fakcie.

Jednocześnie kolejny rozwój śledztwa powinien uwzględnić warunkowe pojawianie się tematów lub działań oraz bardziej ciągły przebieg rozmowy, aby ograniczyć strategię polegającą na mechanicznym zadawaniu wszystkich pytań po kolei.

---

## Etap 6 — Różnorodność śledztw

**Status:** POTWIERDZONA

### Hipoteza

Można odróżnić różnorodność konkretnych danych przypadku od rzeczywistej różnorodności struktury śledztwa i zmierzyć, czy generator tworzy odmienne ścieżki gameplayu zamiast jedynie kosmetycznych wariantów.

### Metoda

Dodano niezależny analizator `case_diversity.py`, który domyślnie generuje 500 kolejnych seedów `0–499` i porównuje dwa poziomy różnorodności.

`ConcreteCaseSignature` liczy istniejące konkretne kombinacje danych, w tym pacjenta, świadka, miejsce, kontakt oraz relacje obserwacji i uczestnictwa.

`InvestigationStructureSignature` celowo pomija seed, imiona, lokalizację, tożsamość kontaktu, tożsamość hipotez i renderowane teksty. Po korekcie review opisuje wyłącznie:

- kategorie zdarzeń znane pacjentowi,
- kategorie zdarzeń znane świadkowi,
- liczbę dostępnych hipotez,
- rolę faktu rozróżniającego w dedukcji.

Zmiana treści kontaktu bez zmiany ścieżki wiedzy i dedukcji nie tworzy nowej struktury. Zmiana rzeczywistego wzorca wiedzy tworzy inną sygnaturę.

### Wynik

Po korekcie definicji struktury pełny zestaw testów zakończył się wynikiem `187 passed`.

Analiza seedów `0–499` dała:

- `500` analizowanych seedów,
- `118` unikalnych konkretnych przypadków,
- tylko `2` unikalne struktury śledztwa,
- struktura dominująca: `335/500` (`67.0%`),
- druga struktura: `165/500` (`33.0%`).

W obu strukturach pacjent zna `presence`, `contact`, `food_history`, `affected`, a świadek zna `presence`, `contact`. Dostępne są zawsze dwie hipotezy.

Różnica między dwiema wykrytymi strukturami dotyczy wyłącznie roli faktu `food_history` w rozumowaniu:

- w `67.0%` przypadków fakt eliminuje alternatywę,
- w `33.0%` przypadków fakt bezpośrednio wspiera poprawną hipotezę.

### Interpretacja

Wynik pokazuje wyraźnie, że różnorodność konkretnych kombinacji danych nie przekłada się obecnie na podobną różnorodność gameplayu.

`118` różnych konkretnych przypadków sprowadza się do `2` struktur dedukcyjnych, a z perspektywy przebiegu gracza są one jeszcze bardziej podobne: w obu przypadkach gracz odkrywa kontakt, sprawdza historię jedzenia i wybiera między dwiema hipotezami.

Dlatego obecny prototyp ma bardzo niską różnorodność strukturalną. Jest to oczekiwany i użyteczny wynik badawczy dla celowo małej domeny, a nie powód do sztucznego zwiększania liczby struktur w tym eksperymencie.

### Ważna obserwacja z review

Pierwsza wersja analizatora bezpośrednio uwzględniała `actual_contact_id` oraz tożsamość hipotez. Dawało to `3` struktury, ale zawyżało różnorodność, ponieważ inny kontakt nie musi oznaczać innej ścieżki śledztwa.

Po usunięciu tożsamości treści i opisaniu roli faktu w dedukcji wynik spadł do `2` struktur. Ta korekta potwierdziła, że metryka musi opisywać to, jak gracz bada i rozumuje, a nie tylko jakie wartości danych zostały wylosowane.

### Ograniczenia wyniku

Sygnatura odzwierciedla tylko obecne mechaniki i będzie wymagała świadomej aktualizacji, gdy pojawią się nowe sposoby zdobywania informacji, różne wzorce wiedzy, badania, dowody lub inne ścieżki dedukcji.

Analiza nie mierzy jakości narracji, ciekawości, trudności ani naturalności rozmowy.

Etap 6 nie zwiększa różnorodności generatora i nie potwierdza, że obecny poziom różnorodności jest wystarczający dla finalnej gry.

### Wniosek

Etap 6 został potwierdzony jako metoda pomiaru różnorodności strukturalnej.

Jednocześnie wynik generatora jest negatywny w sensie jakościowym: obecny prototyp tworzy bardzo mało rzeczywiście różnych ścieżek śledztwa. Dalsze rozszerzanie powinno być oceniane ponownie tą samą metodą, aby sprawdzić, czy dodawane mechaniki zwiększają różnorodność gameplayu, a nie tylko liczbę wariantów danych.

---

## Następny eksperyment

Dotychczasowe etapy potwierdziły spójne składanie prawdy przypadku, walidację, wiedzę uczestników, odkrywanie informacji, minimalną dedukcję oraz możliwość mierzenia różnorodności strukturalnej.

Etap 6 pokazał jednocześnie, że obecna bardzo mała domena daje tylko dwie niemal identyczne struktury dedukcyjne.

Następny krok powinien przejść do Etapu 7 i sprawdzić kontrolowane rozszerzenie domeny: czy nowy rodzaj zawartości można dodać głównie przez dane i istniejące reguły oraz czy faktycznie zwiększa on różnorodność śledztw, zamiast jedynie mnożyć kosmetyczne warianty.
