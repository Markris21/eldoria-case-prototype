# Eldoria Case Prototype

## Cel

To repozytorium jest osobnym projektem badawczo-rozwojowym dla Eldorii.

Jego głównym celem jest sprawdzenie, czy możliwe jest zbudowanie systemu, który proceduralnie tworzy spójne, różnorodne i grywalne przypadki diagnostyczne oraz śledztwa, zamiast polegać wyłącznie na ręcznie napisanych scenariuszach.

Najważniejsze pytanie projektu:

> Czy potrafimy zbudować generator, który sam składa logiczne historie przypadków, rozdziela wiedzę między uczestników i daje graczowi materiał do dedukcji?

## Charakter projektu

To nie jest jeszcze silnik Eldorii.

To laboratorium R&D, w którym możemy:

- szybko testować hipotezy,
- pisać uproszczony kod,
- odrzucać nietrafione rozwiązania,
- przepisywać architekturę,
- generować duże serie przypadków,
- badać powtarzalność i spójność,
- sprawdzać interaktywny wywiad w terminalu.

Kod prototypu nie musi zostać później przeniesiony do finalnej gry.

## Kryterium sukcesu

Prototyp będzie uznawany za obiecujący, jeżeli pokaże, że system potrafi tworzyć przypadki, które:

- są logicznie spójne,
- mają odtwarzalną prawdę przypadku,
- nie wymagają ręcznego pisania każdej historii,
- posiadają sensowne tropy,
- rozdzielają informacje między uczestników w wiarygodny sposób,
- pozwalają graczowi dojść do wniosku przez dedukcję,
- różnią się strukturą i przebiegiem, a nie tylko imionami i nazwami miejsc,
- skalują się przez dodawanie danych i reguł bez ciągłego dopisywania wyjątków do kodu.

## Kryterium porażki

Negatywny wynik jest również wartościowy.

Projekt powinien zostać poważnie przebudowany lub zatrzymany, jeżeli okaże się, że:

- większość przypadków wymaga ręcznej naprawy,
- generator tworzy logiczny, ale nudny materiał,
- przypadki szybko stają się powtarzalne,
- rozwiązywanie sprowadza się do klikania wszystkich pytań,
- każdy nowy archetyp wymaga osobnej logiki w kodzie,
- koszt tworzenia systemu jest nieproporcjonalny do jakości rozgrywki.

## Aktualny kierunek technologiczny

Na etapie prototypu:

- język: Python 3,
- interfejs: terminal,
- testy: pytest,
- dane: początkowo proste struktury Pythona, a YAML tam, gdzie oddzielenie danych od kodu okaże się przydatne,
- repozytorium GitHub jest źródłem prawdy.

Nie używamy jeszcze:

- JavaFX,
- grafiki,
- finalnego UI,
- pełnego silnika Eldorii,
- rozbudowanej bazy danych,
- generatywnego AI jako wymaganego elementu działania gry.

## Planowany sposób pracy

Projekt rozwijamy eksperymentalnie:

```text
Hipoteza
↓
Najmniejszy możliwy prototyp
↓
Kod
↓
Test w terminalu
↓
Ocena wyniku
↓
Wniosek
↓
Dokumentacja
```

Każdy etap powinien udowodnić jedną konkretną rzecz.

Nie budujemy funkcji na zapas.

## Pierwszy docelowy prototyp

Pierwsza grywalna wersja terminalowa powinna docelowo pozwolić:

1. wygenerować przypadek,
2. zobaczyć zgłoszenie,
3. wybrać rozmówcę,
4. wybrać pytanie lub temat wywiadu,
5. otrzymać odpowiedź wynikającą z wiedzy tej osoby,
6. wykonać ograniczone badanie,
7. postawić hipotezę,
8. po zakończeniu zobaczyć pełną prawdę przypadku i seed.

Nie oznacza to, że wszystkie te funkcje powstaną od razu.

## Zasady projektu

Szczegółowe zasady dla ludzi i agentów AI znajdują się w `AGENTS.md`.

Najważniejsze z nich:

- jeden mały krok naraz,
- działający stan po każdym kroku,
- brak projektowania na zapas,
- maksymalnie około 300 linii na dokument Markdown,
- hipotezy i decyzje muszą być odróżnione od potwierdzonych wyników,
- dokumentacja ma zapisywać wnioski z eksperymentów, a nie zastępować eksperymenty.

## Struktura repozytorium

Planowana podstawowa struktura:

```text
src/                kod prototypu
data/               definicje danych używane przez generator
tests/              testy automatyczne
docs/               dokumentacja badań i decyzji
README.md            cel i kierunek projektu
AGENTS.md            zasady pracy
pyproject.toml       konfiguracja projektu Python
requirements.txt     zależności, jeśli będą potrzebne
```

## Dokumentacja badań

`docs/experiments.md`

Zawiera hipotezy, eksperymenty, wyniki i wnioski.

`docs/decisions.md`

Zawiera decyzje, które uznajemy za wystarczająco trwałe, aby kierowały dalszym rozwojem.

`docs/roadmap.md`

Zawiera najbliższe etapy badań. Nie jest sztywnym harmonogramem wdrożenia produktu.

## Relacja z Eldorią

Główne repozytorium Eldorii pozostaje osobne.

Ten projekt ma dostarczać Eldorii:

- potwierdzone koncepcje,
- modele danych,
- wyniki eksperymentów,
- wiedzę o tym, co działa i co nie działa.

Nie zakładamy automatycznie, że kod prototypu stanie się kodem finalnej gry.
