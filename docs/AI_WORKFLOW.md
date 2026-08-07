# AI workflow

## Cel

Ten dokument definiuje podział odpowiedzialności pomiędzy użytkownika, ChatGPT i Codex w projekcie `eldoria-case-prototype`.

GitHub jest jedynym źródłem prawdy. Lokalna kopia repozytorium służy do implementacji przez Codex, uruchamiania programu i ręcznego testowania.

## Role

### Użytkownik

Użytkownik pełni rolę właściciela produktu i głównego projektanta doświadczenia gracza.

Odpowiada za:

- zatwierdzanie i odrzucanie kierunków,
- ocenę gameplayu,
- ręczne testowanie prototypu,
- zgłaszanie problemów i obserwacji,
- podejmowanie decyzji po eksperymentach,
- pilnowanie, aby lokalne repozytorium było zsynchronizowane z GitHubem przed testem lub rozpoczęciem kolejnego zadania.

Użytkownik nie musi ręcznie implementować kodu, chyba że wyraźnie zdecyduje inaczej.

### ChatGPT

ChatGPT pełni rolę architekta systemu i prowadzącego część badawczo-projektową.

Odpowiada za:

- analizę problemów projektowych,
- projektowanie eksperymentów,
- prowadzenie i aktualizowanie dokumentacji bezpośrednio na GitHubie,
- identyfikowanie ryzyk i konsekwencji,
- przygotowywanie precyzyjnych zadań dla Codexa,
- przegląd wyników eksperymentów i Pull Requestów,
- pilnowanie spójności z celem projektu.

ChatGPT nie powinien implementować większych zmian kodu produkcyjnego, jeśli użytkownik nie poprosi o to wyraźnie.

Krótkie przykłady kodu są dopuszczalne wyłącznie jako wyjaśnienie koncepcji lub pomoc diagnostyczna.

### Codex

Codex pełni rolę głównego programisty prototypu i pracuje lokalnie w VS Code na repozytorium użytkownika.

Odpowiada za:

- implementację kodu,
- testy automatyczne,
- refaktoryzację,
- naprawę błędów,
- pracę na krótkich gałęziach,
- sprawdzenie aktualnego stanu repozytorium przed zmianami,
- commit po zakończeniu logicznego zakresu,
- push zmian na GitHub,
- tworzenie Pull Requestów, gdy dany workflow tego wymaga,
- techniczne raportowanie wyników.

Codex nie powinien samodzielnie zmieniać zatwierdzonych decyzji projektowych.

## Główna zasada synchronizacji

GitHub jest jedynym źródłem prawdy, ale praca odbywa się zarówno zdalnie, jak i lokalnie.

Dlatego obowiązuje zasada:

```text
Przed lokalną pracą
↓
sprawdź git status
↓
pobierz aktualne zmiany z GitHuba
↓
Codex implementuje i testuje lokalnie
↓
commit
↓
push
↓
GitHub zawiera aktualny kod
↓
ChatGPT może zaktualizować dokumentację na GitHubie
↓
przed dalszą lokalną pracą wykonaj pull
```

Nie rozpoczynamy kolejnego etapu pracy lokalnej, jeżeli istnieją nieopublikowane zmiany Codexa lub lokalna kopia nie zawiera najnowszych zmian z GitHuba.

## Główny przepływ pracy

```text
Użytkownik
↓
decyzja / obserwacja / pytanie
↓
ChatGPT
↓
analiza + projekt eksperymentu + dokumentacja
↓
Użytkownik synchronizuje lokalne repozytorium
↓
Codex w VS Code
↓
implementacja + testy
↓
commit + push + opcjonalnie Pull Request
↓
GitHub
↓
ChatGPT
↓
review + analiza wyniku + aktualizacja dokumentacji
↓
Użytkownik
↓
git pull + test gameplayu + decyzja
```

Nie każdy krok musi zawierać wszystkie trzy role. Prosta zmiana dokumentacyjna może zostać wykonana przez ChatGPT bez angażowania Codexa.

## GitHub jako źródło prawdy

- Zatwierdzone dokumenty i kod muszą znajdować się na GitHubie.
- Lokalne pliki, które nie zostały opublikowane, nie są jeszcze częścią wspólnego stanu projektu.
- Po zakończeniu pracy Codexa jego zmiany muszą zostać opublikowane na GitHubie przed rozpoczęciem kolejnego etapu przez ChatGPT.
- Po zmianach wykonanych przez ChatGPT bezpośrednio na GitHubie lokalna kopia musi zostać zaktualizowana przed dalszą pracą Codexa lub testem użytkownika.
- Nie synchronizujemy projektu przez ręczne kopiowanie plików, pendrive ani dyski chmurowe.

## Bezpieczny pull

Przed każdym `pull` należy sprawdzić stan lokalnego repozytorium.

Preferowany przebieg:

```text
git status
```

Jeżeli working tree jest czysty, można pobrać zmiany z GitHuba.

Jeżeli istnieją lokalne zmiany, nie wykonujemy bezrefleksyjnie `pull`. Najpierw ustalamy, czy zmiany:

- należą do aktualnej pracy Codexa i powinny zostać commitowane i wypchnięte,
- są tylko lokalnym eksperymentem i mogą zostać odrzucone,
- wymagają osobnego brancha lub świadomego połączenia.

## Bezpieczny push po pracy Codexa

Po zakończeniu każdego logicznego zadania Codex powinien:

1. uruchomić odpowiednie testy,
2. sprawdzić `git status`,
3. sprawdzić zakres zmian,
4. wykonać commit,
5. wykonać push na aktualny branch,
6. utworzyć PR, jeżeli zmiana nie jest przeznaczona do bezpośredniej publikacji na `main`.

Nie zostawiamy zakończonej pracy wyłącznie lokalnie między sesjami, chyba że użytkownik wyraźnie zdecyduje inaczej.

## Stabilny main

`main` ma być zawsze stanem możliwym do uruchomienia.

Zmiany kodu powinny zwykle powstawać na krótkich gałęziach:

- `experiment/...` — eksperyment badawczy,
- `feature/...` — konkretna funkcja,
- `research/...` — narzędzie lub zmiana wspierająca badanie,
- `fix/...` — poprawka błędu,
- `docs/...` — większa zmiana dokumentacji.

Mała, jednoznaczna aktualizacja dokumentacji może zostać wykonana bezpośrednio na `main`, jeżeli nie niesie ryzyka dla kodu.

## Pull Requesty

Dla zmian kodu preferowany jest Pull Request.

PR powinien:

- mieć jeden mały cel,
- wyjaśniać, jakie pytanie badawcze lub problem realizuje,
- zawierać wynik testów,
- nie mieszać niezwiązanych zmian,
- zachować działający program.

PR może dokumentować negatywny wynik eksperymentu. Niepowodzenie hipotezy nie oznacza niepowodzenia PR.

## Lokalny workflow użytkownika

Podstawowy model pracy lokalnej:

```text
sprawdź git status
↓
git pull
↓
Codex implementuje lub użytkownik uruchamia prototyp
↓
testy
↓
jeżeli Codex zmieniał kod: commit + push
↓
GitHub
↓
jeżeli ChatGPT zmienił dokumentację: kolejny pull przed dalszą pracą
```

Użytkownik nie musi regularnie tworzyć ręcznych commitów. Przy zmianach kodu tę odpowiedzialność przejmuje Codex.

## Praca na wielu urządzeniach

Chromebook, laptop domowy i komputer w pracy są równorzędnymi lokalnymi klientami tego samego repozytorium.

Przed zmianą urządzenia preferowany jest stan:

```text
working tree clean
wszystkie zakończone zmiany wypchnięte na GitHub
```

Na kolejnym urządzeniu rozpoczynamy od aktualizacji repozytorium z GitHuba.

Nie zakładamy, że zmiany wykonane na jednym komputerze automatycznie istnieją na pozostałych urządzeniach.

## VS Code i terminal

Na lokalnych urządzeniach preferujemy:

- VS Code do implementacji przez Codex, przeglądania kodu, diffów i Source Control,
- terminal do uruchamiania programu, testów i operacji Git, gdy są potrzebne.

Codex działający w VS Code może wykonywać operacje Git w imieniu użytkownika zgodnie z zasadami projektu.

## Zasada małych kroków

Każda zmiana powinna odpowiadać na jedno z pytań:

- Co chcemy sprawdzić?
- Jaka jest najmniejsza implementacja potrzebna do testu?
- Po czym poznamy wynik?

Jeżeli zmiana nie pomaga odpowiedzieć na aktualne pytanie badawcze, prawdopodobnie jest przedwczesna.
