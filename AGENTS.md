# AGENTS.md

## Cel repozytorium

Repozytorium `eldoria-case-prototype` jest projektem badawczo-rozwojowym służącym do sprawdzenia, czy da się zbudować proceduralny generator przypadków i śledztw diagnostycznych dla Eldorii.

Kod jest narzędziem do testowania hipotez. Celem nie jest jak najszybsze zbudowanie rozbudowanego programu, lecz możliwie wcześnie sprawdzać, czy proponowane mechaniki są spójne, skalowalne i dają wartościową rozgrywkę.

## Źródło prawdy

- Repozytorium GitHub jest jedynym źródłem prawdy dla tego prototypu.
- Nie opieraj się na pamięci rozmów, jeżeli dokumentacja repozytorium mówi inaczej.
- Przed rozpoczęciem pracy przeczytaj `README.md`, `AGENTS.md` oraz dokumenty dotyczące aktualnego eksperymentu.

## Zasady pracy dla AI

1. Nie projektuj dużych systemów na zapas.
2. Każdy nowy plik, klasa, funkcja i zależność musi mieć konkretny cel wynikający z aktualnego eksperymentu.
3. Preferuj małe, odwracalne zmiany.
4. Jeden krok powinien odpowiadać na jedno pytanie badawcze lub realizować jeden mały techniczny cel.
5. Po każdym kroku program powinien pozostać uruchamialny.
6. Nie dodawaj funkcji tylko dlatego, że prawdopodobnie przydadzą się później.
7. Jeżeli prostszy eksperyment może odpowiedzieć na pytanie równie dobrze, wybierz prostszy eksperyment.
8. Nie ukrywaj negatywnego wyniku. Odrzucona hipoteza jest wartościowym rezultatem projektu.
9. Rozdzielaj fakty potwierdzone od hipotez i pomysłów.
10. Nie zmieniaj zatwierdzonych decyzji bez wyraźnej zgody użytkownika.
11. Jeżeli zauważysz niespójność, kosztowną konsekwencję lub ryzyko, przedstaw je przed implementacją.
12. Nie twórz złożonej architektury tylko po to, aby kod wyglądał profesjonalnie.

## Limit rozmiaru dokumentów

- Pojedynczy dokument Markdown powinien mieć maksymalnie około 300 linii.
- Jeżeli dokument zbliża się do tego limitu, podziel go na logiczne dokumenty zamiast dalej go rozbudowywać.
- Wyjątek jest dopuszczalny tylko wtedy, gdy podział wyraźnie pogorszyłby czytelność i użytkownik go zatwierdzi.

## Kod i architektura

- Prototyp jest obecnie tworzony w Pythonie.
- Interfejs pierwszych eksperymentów ma działać w terminalu.
- Dane konfiguracyjne i definicje zawartości powinny być oddzielone od logiki programu tam, gdzie przynosi to realną wartość eksperymentowi.
- YAML jest preferowanym formatem dla czytelnych definicji danych, jeżeli faktycznie jest potrzebny.
- Nie wiąż prototypu z JavaFX ani finalnym silnikiem Eldorii.
- Kod prototypu może później zostać częściowo lub całkowicie wyrzucony.
- Wnioski z prototypu są ważniejsze niż zachowanie jego kodu.

## Testowanie

- Każdy eksperyment powinien mieć jasne kryterium sukcesu lub porażki.
- Jeżeli dodawana funkcja posiada jednoznaczne zachowanie, dodaj test automatyczny, jeśli koszt testu jest rozsądny.
- Preferowany framework testowy: `pytest`.
- Generator powinien docelowo umożliwiać odtwarzanie przypadków przez seed.
- Przy błędach generatora zapisuj seed i dane wejściowe pozwalające odtworzyć problem.

## Dziennik badań

Projekt prowadzi dziennik eksperymentów w `docs/experiments.md`.

Każdy istotny eksperyment powinien zapisywać co najmniej:

- identyfikator eksperymentu,
- hipotezę,
- metodę testu,
- wynik,
- wniosek,
- status: `TESTOWANA`, `POTWIERDZONA` albo `ODRZUCONA`.

Nie przepisuj historii projektu po fakcie. Jeżeli hipoteza była błędna, zostaw jej wynik jako część historii badań.

## Decyzje projektowe

Trwałe decyzje zapisuj w `docs/decisions.md`.

Decyzja powinna zawierać:

- problem,
- rozważane opcje,
- wybraną opcję,
- powód,
- konsekwencje,
- datę lub numer eksperymentu, który do niej doprowadził.

## Workflow Git

- `main` powinien zawsze zawierać działający stan projektu.
- Małe eksperymenty mogą być wykonywane na krótkich gałęziach.
- Preferowane prefiksy gałęzi: `experiment/`, `feature/`, `research/`, `fix/`.
- Jeden commit powinien obejmować jeden logiczny zakres.
- Wiadomości commitów pisz krótko i po angielsku.
- Nie wykonuj force push, `git reset --hard` ani destrukcyjnego usuwania bez wyraźnej zgody użytkownika.

Przed publikacją zmian sprawdź:

```text
git status
git diff
git diff --check
```

Uruchom także odpowiednie testy dla zmienianego zakresu.

## Pull Requesty

- PR powinien mieć mały i czytelny zakres.
- Opis PR powinien podawać, co zmieniono, dlaczego i jaki eksperyment lub problem obsługuje.
- Jeżeli PR dotyczy eksperymentu, wynik eksperymentu nie musi być pozytywny, aby PR był wartościowy.

## Dokumentacja a eksperymenty

Preferowany cykl pracy:

```text
Pomysł / hipoteza
↓
Najmniejszy możliwy eksperyment
↓
Implementacja
↓
Uruchomienie i obserwacja
↓
Wniosek
↓
Aktualizacja dokumentacji
```

Nie spędzaj więcej czasu na dokumentowaniu nieprzetestowanej koncepcji niż na zbudowaniu eksperymentu, który może ją szybko zweryfikować.

## Komunikacja z użytkownikiem

- Odpowiadaj po polsku, chyba że użytkownik poprosi inaczej.
- Pracuj krok po kroku.
- Przy konfiguracji lokalnego środowiska podawaj jeden krok i czekaj na wynik.
- W kodzie podawaj wersje gotowe do kopiowania oraz dokładną ścieżkę pliku, gdy użytkownik ma coś wkleić ręcznie.
- Nie zgadzaj się automatycznie z pomysłem użytkownika. Pokazuj zalety, wady i konsekwencje.
- Nie komplikuj odpowiedzi, jeżeli kolejny krok jest prosty i jednoznaczny.

## Główne pytanie projektu

Każda większa decyzja powinna być oceniana przez pryzmat pytania:

> Czy ten krok pomaga sprawdzić, czy Eldoria może proceduralnie tworzyć spójne, różnorodne i satysfakcjonujące śledztwa diagnostyczne?

Jeżeli odpowiedź brzmi `nie`, krok prawdopodobnie nie należy jeszcze do tego prototypu.
