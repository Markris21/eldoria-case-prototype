# AI workflow

## Cel

Ten dokument definiuje podział odpowiedzialności pomiędzy użytkownika, ChatGPT i Codex w projekcie `eldoria-case-prototype`.

GitHub jest jedynym źródłem prawdy. Lokalne kopie służą głównie do uruchamiania i testowania aktualnego stanu repozytorium.

## Role

### Użytkownik

Użytkownik pełni rolę właściciela produktu i głównego projektanta doświadczenia gracza.

Odpowiada za:

- zatwierdzanie i odrzucanie kierunków,
- ocenę gameplayu,
- ręczne testowanie prototypu,
- zgłaszanie problemów i obserwacji,
- podejmowanie decyzji po eksperymentach,
- lokalne pobieranie zmian z GitHuba i ich uruchamianie.

Użytkownik nie musi ręcznie implementować kodu, chyba że wyraźnie zdecyduje inaczej.

### ChatGPT

ChatGPT pełni rolę architekta systemu i prowadzącego część badawczo-projektową.

Odpowiada za:

- analizę problemów projektowych,
- projektowanie eksperymentów,
- prowadzenie i aktualizowanie dokumentacji,
- identyfikowanie ryzyk i konsekwencji,
- przygotowywanie precyzyjnych zadań dla Codexa,
- przegląd wyników eksperymentów i Pull Requestów,
- pilnowanie spójności z celem projektu.

ChatGPT nie powinien implementować większych zmian kodu produkcyjnego, jeśli użytkownik nie poprosi o to wyraźnie.

Krótkie przykłady kodu są dopuszczalne wyłącznie jako wyjaśnienie koncepcji lub pomoc diagnostyczna.

### Codex

Codex pełni rolę głównego programisty prototypu.

Odpowiada za:

- implementację kodu,
- testy automatyczne,
- refaktoryzację,
- naprawę błędów,
- pracę na krótkich gałęziach,
- commity,
- push,
- tworzenie Pull Requestów,
- techniczne raportowanie wyników.

Codex nie powinien samodzielnie zmieniać zatwierdzonych decyzji projektowych.

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
Codex
↓
implementacja + testy + Pull Request
↓
ChatGPT
↓
review i analiza wyniku
↓
Użytkownik
↓
git pull + test gameplayu + decyzja
```

Nie każdy krok musi zawierać wszystkie trzy role. Prosta zmiana dokumentacyjna może zostać wykonana przez ChatGPT bez angażowania Codexa.

## GitHub jako źródło prawdy

- Zatwierdzone dokumenty i kod muszą znajdować się na GitHubie.
- Lokalne pliki, które nie zostały opublikowane, nie są częścią projektu.
- Użytkownik powinien utrzymywać lokalne repozytorium możliwie blisko `origin/main`.
- Przed lokalnym testem preferowany jest `pull` aktualnego `main`.
- Nie synchronizujemy projektu przez ręczne kopiowanie plików, pendrive ani dyski chmurowe.

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
GitHub
↓
git pull
↓
uruchomienie prototypu
↓
test gameplayu
↓
obserwacje przekazane ChatGPT
```

Użytkownik nie musi regularnie tworzyć lokalnych commitów. Lokalna kopia pełni przede wszystkim rolę środowiska testowego.

Jeżeli użytkownik wprowadza lokalne zmiany, przed kolejnym `pull` należy sprawdzić `git status` i świadomie zdecydować, czy zmiany zachować.

## VS Code i terminal

Na lokalnych urządzeniach preferujemy:

- VS Code do przeglądania kodu, diffów i Source Control,
- terminal do uruchamiania programu, testów i wyjątkowych operacji Git.

Nie ma obowiązku wykonywania każdej operacji Git w terminalu.

## Zasada małych kroków

Każda zmiana powinna odpowiadać na jedno z pytań:

- Co chcemy sprawdzić?
- Jaka jest najmniejsza implementacja potrzebna do testu?
- Po czym poznamy wynik?

Jeżeli zmiana nie pomaga odpowiedzieć na aktualne pytanie badawcze, prawdopodobnie jest przedwczesna.
