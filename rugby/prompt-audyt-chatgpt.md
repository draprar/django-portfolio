# Prompt: audyt i kierunek dla archiwum AFC Rugby Giżycko

Wklej **cały ten plik** do ChatGPT. Nie oceniaj kodu Django. Oceń treść, układ, sens produktu i pomysły na jeden moduł interaktywny.

Autor: Walery (Michał Walerowicz), data scientist. Buduje małe aplikacje pro bono w jednym Django i wystawia je na [jedzien.pl](https://jedzien.pl). Rugby to archiwum klubu, który sam założył jako nastolatek i który został rozwiązany w 2010. Chce je **dołączyć do huba**, ale nie jako muzeum „miałem drużynę”.

---

## Zadanie

Zrób trzy rzeczy naraz.

### 1. Archiwum — jak je zwinąć

Dziś to jedna długa strona: hero, trzy karty o drużynie, siatka mediów, oś czasu, potem 19 newsów w akordeonie (czerwiec 2008 – wrzesień 2010).

Autor skłania się do tego, żeby **newsy wyrzucić albo wchłonąć w oś czasu**, a teksty skrócić do zajawki. Pełne relacje są nudne jako archiwum i dublują oś czasu (trening z Borsem, sparing w Gągławkach, trening z Misiakiem, rozwiązanie klubu wracają i tu, i tu).

Oceń:

- co z osi czasu zostawić, co skleić, co skrócić do 1–2 zdań;
- które newsy wnoszą fakt, którego nie ma na osi (przerwy, hala, legitymacje, strona, koniec) — i czy warto je dopisać jako krótkie punkty, czy wyciąć;
- czy podziękowanie dla zawodników i informacja „klub rozwiązany” mają zostać na wierzchu;
- czego nie ruszać (nazwiska trenerów, daty, miejsca), bo to jedyny ślad.

Nie przepisuj całego archiwum. Daj **proponowany szkielet osi** (data lub etap → jedno zdanie) i listę newsów: zostań / sklej / wyrzuć.

### 2. UX / UI obecnej strony

Jedna kolumna, Bootstrap, czcionki Montserrat + Playfair, animacje przy scrollu, przełącznik PL/EN. To **nie** jest język wizualny huba (ciemne tło, złoto, Poppins, krótkie napisy).

Oceń jak dla kogoś, kto wchodzi z huba i nie zna klubu:

- co obiecuje hero („archiwum”, „udanego zwiedzania”) wobec treści;
- nabór i treningi są napisane tak, jakby drużyna nadal grała („trwał”, „trenowaliśmy” — czas przeszły jest, ale działy nadal wyglądają jak ogłoszenie);
- czy media (dwa plakaty, dwa skany gazet, skan encyklopedii, jeden film YouTube) zasługują na własną sekcję;
- nawigacja: Home, Drużyna, Promocja, Historia, Archiwum, Kontakt (kontakt leci na stronę portfolio);
- stopka to sam obrazek;
- dwujęzyczność: czy EN jest potrzebne na archiwum lokalnego klubu, skoro hub jest tylko po polsku.

Konkret: co wyciąć, co zostawić, jaka kolejność sekcji po dołączeniu do huba. Bez makiet piksel po pikselu.

### 3. Research — jeden moduł pro bono, nie kolejna duma z drużyny

Cel: coś **interaktywnego**, rozrywkowego albo naukowego (dzielenie się wiedzą). Klub jest martwy. Odbiorca to ktoś z huba albo ktoś, kto chce zrozumieć rugby, nie byli zawodnicy z Giżycka.

Już zrobione gdzie indziej (nie powtarzaj tego samego pomysłu pod inną nazwą):

- **wiciędze** — katalog sztuk walki i sportów walki (opisy, quiz dopasowania) oraz **mokuso** (krótka medytacja / wyciszenie wg Herberta Bensona).
- Nie idź w „analitykę walk” ani w kolejny katalog sportów kontaktowych.
- Nie idź w moduł „z AI” jako główny haczyk. Takich aplikacji jest dużo, a autor nie chce kolejnego czatu o rugby.

Szukaj **niszy rugby**, najlepiej pod to, co ten klub naprawdę robił: **rugby siedmioosobowe** (sevens), amatorski start od zera, bez trenera z licencją na początku. Odmiana XV jest osobnym sportem na boisku — nie mieszaj ich w jednym quizie bez powiedzenia, która obowiązuje.

Zbadaj, co już istnieje (oficjalne prawa World Rugby / World Rugby Sevens, materiały PZRugby, popularne aplikacje i strony do nauki przepisów) i napisz wprost, gdzie jest dziura, a gdzie byłbyś duplikatem. Przy każdym pomyśle podaj źródło albo napisz SOURCE GAP.

Zaproponuj **2–4 koncepcje** jednego małego modułu (da się zrobić samemu w Django, bez drużyny, bez transmisji, bez kont użytkowników jeśli nie są konieczne). Dla każdej:

- dla kogo i po co;
- co użytkownik klika / robi w 3–5 minutach;
- dlaczego to nie jest „pochwal się klubem” ani kopia wiciędzy;
- czego nie obiecywać (to nie szkolenie trenerskie, nie certyfikat, nie aplikacja meczowa);
- werdykt: rób / nie rób.

Na końcu **jedna rekomendacja**: archiwum w takiej a takiej formie + ten jeden moduł. Resztę odrzuć krótko.

---

## Format odpowiedzi

1. **Co jest nie tak z obecnym archiwum** (krótko, bez streszczania każdego newsa)
2. **Oś czasu po zwinięciu** (szkielet) + los newsów (zostań jako punkt / wyrzuć)
3. **UX/UI** — kolejność sekcji i co wyciąć
4. **Krajobraz** — co już uczy rugby (źródła) i gdzie jest luka
5. **Koncepcje modułu** (2–4) z werdyktem
6. **Rekomendacja** (jedna)
7. **Czego nie wiem / nie dało się sprawdzić**

Nie pisz kodu. Nie przepisuj newsów. Nie proponuj profilu osobowości ani „AI coacha”.

---

## Kontekst: co jest na jedzien.pl

Domena **jedzien.pl** serwuje ten sam Django. Strona główna to hub **`/wybierz/`** (na jedzien.pl także `/`). Nagłówek: „Se klikaj:”. Cztery kafelki, po polsku, bez przełącznika języka:

| Kafelek | Adres | Co to jest |
|---|---|---|
| kodzillin' | `/code/` | Wizytówka programistyczna: projekty, krótki opis, kontakt. To nie jest aplikacja do nauki. |
| Wyraj | `/wyraj/` | Słowiańskie Koło Roku: opisy świąt i obrzędów, koło do obracania. Czytanie, nie quiz. |
| LingwoŁamki | `/tonguetwister/` | Trener łamańców językowych: rozgrzewka, artykulatory, ćwiczenie głosu, własne treści użytkownika, konto. Pro bono, interaktywne. |
| wiciędze | `/wiciedze/` | Katalog sztuk walki (opisy, porównanie, quiz „co ci bliższe”) plus mokuso — krótkie wyciszenie. Pro bono, dzielenie się wiedzą. |

Wzorzec „moduł interaktywny”, pod który rugby ma się zbliżyć, to m.in. wiciędze i LingwoŁamki (tabela powyżej): krótka pętla „przeczytaj / kliknij / zrób coś”, nie ściana tekstu.

Rugby (`/rugby/`) **nie jest** na hubie. Wisi w menu portfolio jako archiwum. Plan: po przeróbce ma móc stanąć obok tamtych kafelków. Głos huba jest krótki i bezpośredni. Archiwum rugby jest długie, grzeczne i pisane jak strona klubu z 2008–2010.

---

## Jak działa rugby dziś

Jedna strona, jeden widok. Adres: `/rugby/`.

Kolejność od góry:

1. **Hero** — „Witaj w archiwum pierwszej drużyny rugby na Mazurach”.
2. **Drużyna** — trzy kolumny: Nabór, Treningi, Zawodnicy (fakty + podziękowanie).
3. **Promocja klubu** — karty ze zdjęciami: dwa plakaty (Jakub Turek), artykuł Gazety Giżyckiej (Paweł Mieczkowski), artykuł Gazety Olsztyńskiej (Sebastian Woźniak), skan „Encyklopedia Polskiego Rugby” (Maciej Powała-Niedźwiedzki i Jacek Wierzbicki), film YouTube (Michał Walerowicz, `https://www.youtube.com/watch?v=TBdK3AkhQKE`).
4. **Historia klubu** — akapit, skąd się wzięła ta strona (domena giżycka zdjęta w 2019, potem darmowy hosting, GitHub Pages, Django), potem oś czasu od „Początki” do „Klub został rozwiązany”. Oś jest wpisana na sztywno w szablon, nie w bazie.
5. **Archiwum** — newsy z bazy (`Post`: tytuł i treść PL oraz EN, data publikacji). Na stronie od najnowszego. Akordeon: widać tytuł i datę, treść po kliknięciu. Brak podstron, tagów, wyszukiwania.
6. **Stopka** — obrazek, bez tekstu.
7. Przełącznik **PL / EN** podmienia `data-pl` / `data-en`. Domyślnie polski.
8. Link „Home” idzie na `/`. „Kontakt” idzie na portfolio `#contact`. 404: „Ups! Strona nie istnieje.”

Model danych newsów: autor, `title_pl`, `title_en`, `text_pl`, `text_en`, daty. Treści newsów **nie ma w repozytorium** — są w bazie produkcyjnej (19 wpisów na `https://jedzien.pl/rugby/`, od końca działalności do startu). Wklej je w sekcji „Archiwum newsów” na końcu tego pliku, zanim wyślesz go do Chata.

Fakty, które widać z tekstów (żeby nie zgadywać): pierwsza drużyna rugby 7 na Mazurach, Giżycko, start ok. 6–10 czerwca 2008, stowarzyszenie AFC, potem Młodzieżowe Towarzystwo Sportowe / MTS, treningi 2–3 razy w tygodniu, boisko boczne MOSiR, zimą hala JW 4352, współpraca z WMPD PUDiZ Olsztyn (Leszek Bors, Krzysztof Olsiński), sparing w Gągławkach, wizyta Macieja Misiaka i Jakuba Sekleckiego, szczyt ok. 18 zawodników (15–22 lata), rozwiązanie 18.09.2010, bo założyciel wyjechał na studia. Na stronie nie ma wyników ligowych ani tabeli — to nie był klub rozgrywkowy.

---

## Teksty interfejsu (PL, pod spodem EN tam, gdzie jest osobna wersja)

### Hero

PL: AFC Rugby Giżycko / Witaj w archiwum pierwszej drużyny rugby na Mazurach / Udanego zwiedzania. / Przewiń

EN: Welcome to the archive of the first rugby team in Mazury / Enjoy your visit. / Scroll

### Nawigacja

Home · Drużyna / Team · Promocja / Promotion · Historia / History · Archiwum / Archive · Kontakt / Contact · PL · EN

Przycisk „Wróć na górę” / „Back to top”.

### Drużyna

Nagłówek: Drużyna / The Team

Lead: Poznaj kilka faktów dotyczących drużyny. / A few facts about the team.

**Nabór / Recruitment**

PL: Nabór do drużyny trwał cały rok, bez znaczenia był wiek, doświadczenie oraz warunki fizyczne - miejsce na boisku było dla każdego z chęcią do gry i zaangażowaniem. W okresie letnim (gdyż zimą trenowaliśmy na hali wojskowej dzięki uprzejmości Jednostki Wojskowej 4352) można było przyjść na trening i popatrzeć, nie biorąc w nim udziału. Trenowanie było bezpłatne.

EN: Recruitment ran year-round, regardless of age, experience or physical condition — there was a place on the pitch for anyone willing to play and commit. In summer (as in winter we trained at a military hall courtesy of Military Unit 4352) you could come to practice and just watch. Training was free of charge.

**Treningi / Training**

PL: Trenowaliśmy 2-3 razy w tygodniu w różnych miejscach: przez większą część działalności na stadionie MOSiR (płyta boczna), choć widziano nas także na miejscowych "Orlikach", boiskach szkolnych, a także w miejscowości Bystry. Graliśmy w odmianę siedmioosobową rugby. Ze względu na zredukowaną ilość zawodników w drużynie, na boisku jest więcej przestrzeni oraz zmniejsza się czas gry w kontakcie - liczy się przede wszystkim spryt i szybkość.

EN: We trained 2–3 times a week at various locations: mostly at the MOSiR stadium (side pitch), though we were also spotted at local Orliki pitches, school grounds and in the village of Bystry. We played seven-a-side rugby. With fewer players on the field there is more space and less contact time — speed and cunning matter most.

**Zawodnicy / Players**

PL: W najbardziej sowitych czasach zarejestrowanych było 18 aktywnych zawodników, w wieku 15-22 lata, o wadze 50-100 kg i wzroście 160-185 cm. Panowie, podopieczni, koledzy, również przyjaciele - dziękuję za te dwa lata zaangażowania z Waszej strony, wspólnej nauki, łapania dobrych chwil, zarówno rugbowych, jak i pozasportowych oraz przede wszystkim świetnej zabawy!

EN: At our peak we had 18 active registered players, aged 15–22, weighing 50–100 kg and standing 160–185 cm tall. Gentlemen, players, colleagues and friends — thank you for those two years of commitment, shared learning, great moments both on and off the pitch, and above all for the brilliant fun!

### Promocja klubu / Club Promotion

Lead: Wybrane materiały prasowe, plakaty oraz media. / Selected press materials, posters and media.

- Pierwszy plakat / First poster — Autor: Jakub Turek
- Drugi plakat / Second poster — Autor: Jakub Turek
- Artykuł (Gazeta Giżycka) / Article (Gazeta Giżycka) — Autor: Paweł Mieczkowski
- Artykuł (Gazeta Olsztyńska) / Article (Gazeta Olsztyńska) — Autor: Sebastian Woźniak
- Encyklopedia Polskiego Rugby / Encyclopaedia of Polish Rugby — Autorzy: Maciej Powała-Niedźwiedzki & Jacek Wierzbicki
- Film / Film — Autor: Michał Walerowicz

### Historia klubu / Club History

PL: Strona w 2019 r. została usunięta z giżyckiej domeny, stąd z sentymentu przeniosłem ją na darmowy hosting, później na GitHub Pages a następnie w ramach nauki opracowałem nową wersję z wykorzystaniem framework'a Django (testując przy okazji różne hostingi), która finalnie trafiła do mojego portfolio. W razie zainteresowania śledzeniem przeszłości klubu, zapraszam do skorzystania również z Wayback Machine :)

EN: The site was removed from the Giżycko domain in 2019, so out of nostalgia I moved it to free hosting, then to GitHub Pages, and finally rebuilt it with Django as part of my portfolio. If you want to explore the club's past further, feel free to use the Wayback Machine :)

Linki w tym akapicie: gizycko.pl, `https://draprar.github.io/html-rugby-gizycko/`, Wayback `rugby.gizycko.pl`.

**Oś czasu**

1. Początki / Beginnings — Pomysł na stworzenie w Giżycku, pierwszej na Mazurach, drużyny rugby "7" narodził się już parę miesięcy temu. Kilka dni przed 6 czerwca, gdy plakaty z informacją o naborze do sekcji pojawiły się w mieście i szkołach, klamka o powołaniu jej do życia zapadła. Plany zostały wdrążone w życie, bowiem właśnie 6 czerwca odbyło się w Giżyckim Centrum Kultury zebranie organizacyjne. Pomysłodawcą jest Michał Walerowicz - uczeń 1 LO w Giżycku. Posiadając jedynie wiedzę teoretyczną oraz ogromny zapał podjął się wyzwaniu prowadzenia drużyny sportowej.

   EN: The idea of creating Giżycko's first rugby sevens team — the first in Mazury — had been brewing for several months. A few days before 6 June, when recruitment posters appeared around the city and in schools, the decision to bring it to life was made. And so, on 6 June, an organisational meeting was held at the Giżycko Cultural Centre. The driving force was Michał Walerowicz, a student at the 1st High School in Giżycko, who — armed only with theoretical knowledge and enormous enthusiasm — took on the challenge of running a sports team.

2. Pierwsze zebranie / First Meeting — Na spotkaniu organizacyjnym zjawiło się 14 osób. Uzgodniony został termin pierwszego treningu, który odbył się 10 czerwca na stadionie MOSiR. Na pierwszym "sprawdzianie kondycyjnym" zostały ustalone terminy przyszłych treningów oraz kwestie formalne.

   EN: 14 people attended the organisational meeting. The date of the first training session was set — it took place on 10 June at the MOSiR stadium. At that first "fitness check", future training dates and formal matters were agreed.

3. Formalizacja sekcji / Formalisation — Nowa sekcja działała wówczas w stowarzyszeniu AFC (Active Free Crew). Po podjęciu uchwały o stworzeniu sekcji w stowarzyszeniu przestaliśmy być grupką znajomych, która rekreacyjnie bawi się w rugby. W niedługim czasie nastąpiło uruchomienie strony internetowej drużyny, co umożliwiło również reklamę. W międzyczasie część zawodników się wykruszyła, pojawili się również nowi - zaczęła się jednak formować stała grupa chłopaków uczęszczających regularnie na treningi.

   EN: The new section operated within the AFC (Active Free Crew) association. Once the resolution to create the section was passed, we were no longer just a group of friends playing rugby for fun. Shortly afterwards the team website went live, providing a platform for promotion. In the meantime some players dropped out and new ones joined — a stable core of regulars began to take shape.

4. Współpraca z Olsztynem / Cooperation with Olsztyn — Dzięki wsparciu Justyny Nierwińskiej na stronie Olsztyńskiego klubu ukazała się informacja, dotycząca pojawienia się naszej działalności oraz chęć pomocy ze strony olsztyńskiego zespołu. Niedługo potem zaaranżowane zostało spotkanie z doświadczonym trenerem Leszkiem Borsem, które odbyło się 26 czerwca na stadionie giżyckiego MOSiRu. Podczas wspólnego treningu nabyliśmy nowych doświadczeń oraz otrzymaliśmy cenne wskazówki, a po zakończonym spotkaniu dostaliśmy 5 piłek oraz materiały pomocnicze, które zostaną wykorzystane do dalszego szkolenia.

   EN: Thanks to the support of Justyna Nierwińska, the Olsztyn club's website published news about our activity and their willingness to help. Shortly afterwards, a meeting was arranged with experienced coach Leszek Bors, held on 26 June at the Giżycko MOSiR stadium. During the joint training session we gained new experience and received valuable tips, and after it ended we were given 5 balls and training materials to aid our further development.

5. Rozgłos / Media Coverage — Informacja o naszym spotkaniu z trenerem Leszkiem Borsem ukazała się w Gazecie Giżyckiej oraz Gazecie Olsztyńskiej. Artykuł z GO ukazał się również na stronie klubu z Olsztyna.

   EN: News of our meeting with coach Leszek Bors appeared in Gazeta Giżycka and Gazeta Olsztyńska. The GO article was also published on the Olsztyn club's website.

6. Współpracy ciąg dalszy / Cooperation Continues — 5 lipca wybraliśmy się do Olsztyna, skąd trenerzy pierwszoligowca - Leszek Bors i Krzysztof Olsiński przetransportowali nas do Gągławek, gdzie rozegraliśmy nasz pierwszy mecz sparingowy z okazji 650-lecia tejże miejscowości. To było pierwsze, lecz nie ostatnie takie spotkanie. Koledzy z Olsztyna okazali się bardzo życzliwi i udzielili nam wielu pomocnych wskazówek podczas gry. Żaden trening nie zastąpi doświadczenia zdobytego podczas rozegranego meczu.

   EN: On 5 July we headed to Olsztyn, from where coaches Leszek Bors and Krzysztof Olsiński drove us to Gągławki, where we played our first friendly match to mark that village's 650th anniversary. It was the first, but not the last such occasion. The Olsztyn lads were very generous and gave us plenty of useful guidance during the game. No training session replaces the experience gained in a real match.

7. Klub z prawdziwego zdarzenia / A Real Club — Dzięki pomocy trenera Andrzeja Paszkiewicza sekcja należy teraz do Młodzieżowego Towarzystwa Sportowego. Do Polskiego Związku Rugby zostało wysłane pismo zawierające informację o powstaniu drużyny. Od teraz nasz zespół doskonali swoje umiejętności gry w rugby jako część profesjonalnego klubu sportowego.

   EN: Thanks to coach Andrzej Paszkiewicz, the section became part of the Youth Sports Society. A letter informing the Polish Rugby Union of the team's establishment was sent. From that point on, our team developed its rugby skills as part of a professional sports club.

8. Czas na logo / Time for a Logo — Drużyna posiada swoje własne logo, które od teraz będzie pojawiać się na naszych strojach i wszelkich dogodnych do tego typu grafiki obiektach.

   EN: The team now has its own logo, which will appear on our kits and wherever else the design fits.

9. Poważny trening / Serious Training — Drugi trening, który sprawił, że nasz zapał do gry urósł jeszcze bardziej odbył się 13-go sierpnia. Kolejnym trenerem, który zgodził się poświęcić nam czas był selekcjoner kadry juniorów Maciej Misiak oraz zawodnik MKS Orkan Sochaczew Jakub Seklecki, którzy przebywali w Giżycku wraz ze swoją klubową drużyną na obozie sportowym. Wszyscy do treningu podeszli bardzo poważnie. A wrażenia po? Uśmiech na twarzach mówił wszystko. Serdecznie dziękujemy za ofiarowaną pomoc i przekazanie nam cząstki posiadanej wiedzy i umiejętności. Spożytkujemy ją jak najlepiej.

   EN: The second coaching visit, which fired up our enthusiasm even more, took place on 13 August. Another coach who agreed to give us his time was junior national team selector Maciej Misiak and MKS Orkan Sochaczew player Jakub Seklecki, who were in Giżycko with their club on a training camp. Everyone approached the session with great seriousness. The smiles on our faces afterwards said it all. We sincerely thank them for their help and for sharing a piece of their knowledge and skill. We will put it to the very best use.

10. Koniec osi, bez akapitu: „Klub został rozwiązany” / „Club was dissolved”.

### Archiwum (lead)

PL: Archiwum. Poniżej znajduje się archiwum newsów.

EN: Archive. Below you will find the news archive.

### 404

PL: Ups! Strona nie istnieje. / Powrót na stronę główną

(brak wersji EN)

---

## Archiwum newsów

Tu wklej newsy (tytuł, data, PL, EN jeśli jest). Na stronie jest ich 19, od najnowszego: 18.09.2010 „Koniec” → 10.06.2008 „Start strony”.

```
Start strony drużyny AFC Rugby Giżycko (10.06.2008)
Witam wszystkich sympatyków, kibiców oraz zawodników Rugby.

Ruszyła strona oficjalna drużyny, niestety jest w przebudowie i niektóre działy nie są dostępne lub informacje w nich są mocno ograniczone, ale to dopiero początki. Niedługo zapewne uda mi się uzupełnić braki.

Na ten moment cieszmy się widokiem.

Nabór, galeria oraz olsztyńskie rugby (11.06.2008)
Dodałem do Galerii zdjęcia z przedwczoraj.
Poza tym zapraszam na stronę http://www.rugby.olsztyn.pl/ i wiadomość z dnia 19-06-2008.

Zajrzyjcie do działu Nabór i na najbliższy trening (wtorek, 24.06). Podpowiem, że będą omawiane bardzo ważne sprawy dla zawodników.

Informacja o planowanym treningu z profesjonalnym trenerem (14.06.2008)
Czwartkowy trening odbędzie się o godzinie 17 na stadionie MOSiR (zbiórka na głównej płycie).
Na treningu obecny będzie trener pierwszoligowej drużyny WMPD PUDiZ OLSZTYN. Zapraszam wszystkich!

Zaktualizowałem dział Zawodnicy.

Trening z trenerem pierwszoligowego zespołu WMPD PUDiZ Olsztyn (16.06.2008)
W dzisiejszym dniu odbył się pierwszy trening z Panem Leszkiem Borsem - trenerem pierwszoligowego zespołu WMPD PUDiZ Olsztyn, który pokazał wiele przydatnych ćwiczeń i wyjaśnił zasady rugby. Wszystko wskazuje na to, że nawiązaliśmy stałą współpracę z olsztyńskim klubem i takie treningi będą odbywały się jeszcze nie jeden raz. Dostaliśmy również piłki, które przydadzą się na kolejnych treningach.
Serdecznie dziękujemy Panu Leszkowi i pozdrawiamy.

Doszło również kilku nowych zawodników, a co za tym idzie zaktualizowałem listę.

W Galerii możecie zobaczyć zdjęcia z dzisiejszego spotkania.

Następny trening: wtorek, 18:00. Serdecznie zapraszam!

Chciałbym również podziękować Justynie Nierwińskiej za okazaną pomoc.

Sparing z juniorami WMPD PUDiZ Olsztyn (25.06.2008)
W sobotę 05.07 o godzinie 13 w Gągławkach rozegramy sparing z juniorami WMPD PUDiZ Olsztyn. Zapraszamy!

Na stronie Olsztyńskiego klubu oraz tutaj (Gazeta Wyborcza Olsztyn) jest dostępny ciekawy artykuł.

Niedługo zostanie zaktualizowany dział Informacje o nas, na dzisiejszym treningu padły niestety baterie od aparatu i nie posiadam żadnych zdjęć.

Relacja ze sparingu z juniorską drużyną WMPD PUDiZ Olsztyn (07.07.2008)
W minioną sobotę (5.07) o godz. 5.49 wybraliśmy się do Olsztyna, skąd odebrali nas P. Leszek Bors i P. Krzysztof Olsiński, a następnie obraliśmy kierunek Gągławek, gdzie rozegraliśmy mecz sparingowy z juniorską drużyną WMPD PUDiZ Olsztyn. Spotkanie odbyło się z okazji 650-lecia miejscowości. Koledzy z Olsztyna udzielali przydatnych wskazówek, jak zachowywać się na boisku i starali się by głównie zawodnicy młodsi stażem byli przy piłce. Sobotnie spotkanie poprowadził międzynarodowy sędzia. Trenerzy byli zadowoleni z postawy, jaką zaprezentowaliśmy. Kilku naszych zawodników zrobiło bardzo dobre wrażenie na olsztyńskich szkoleniowcach i dostali propozycję wzięcia udziału w rozgrywkach "15".

Cieszy również fakt, że obyło się bez kontuzji naszych zawodników. Ucierpiały jedynie stroje, które otrzymaliśmy:)
Oprócz rozegranego meczu otrzymaliśmy również sporą dawkę informacji, które przydadzą się w rozkręceniu sekcji. Niebawem będziemy zamawiać stroje.

W przeciągu dwóch tygodni po raz kolejny na naszym treningu zjawi się P. Leszek.
Szykuje się również 14-dniowa przerwa, by zawodnicy mogli chwilę odetchnąć i nabrać sił.

W dalszym ciągu musimy trenować na treningowym boisku, tzw. bocznym, które nie nadaje się do trenowania rugby ze względu na dużą ilość kamieni i fatalną murawę, gdyż zarząd MOSiR nie zgodził się na udostępnienie nam płyty głównej. Trening, który rozpoczęliśmy na płycie głównej musieliśmy przerwać, gdyż zostaliśmy wyproszeni. Jesteśmy w trakcie poszukiwań lepszego miejsca w okolicach Giżycka.

W Galerii umieszczone zostały oczywiście zdjęcia z wyjazdu.
Dodałem dział Informacje o nas. Generalnie zaktualizowałem prawie wszystkie działy na stronie, więc zapraszam do odświeżenia informacji.

Zmieniły się dni treningów (poniedziałek, wtorek, czwartek o 18:00). Więcej w dziale trening.

UWAGA! Przypominam o naborze drużyny. Chciałbym wspomnieć również o tym, że szukamy sponsora. Jeżeli ktoś byłby zainteresowany zapraszam do działu kontakt (najlepiej kontaktować się telefonicznie bądź poprzez GG).

Dane personalne zawodników (17.07.2008)
Imię, nazwisko, data i miejsce urodzenia, adres zamieszkania, PESEL lub NIP – te dane należy przesłać do mnie mailem, zamieścić je w wiadomości na GG bądź przynieść na kartce na pierwszy trening po przerwie (5 sierpnia – godz. 18) Obie formy kontaktu zamieszczone są w dziale Kontakt. W przypadku, gdy do 5.08 nie otrzymam danych, osoba nie będzie mogła zostać członkiem klubu MTS Rugby Giżycko. Osoby chcące dopiero dołączyć do drużyny też muszą przesłać mi w/w informacje.

Od 20 lipca do 4 sierpnia mam będę urlopował- postaram się jednak sprawdzać skrzynkę mailową.

Mam nadzieję, że nikt nie przyjechał dziś na trening, gdyż jak wcześniej pisałem – nie odbył się:)

Pozdrawiam, do zobaczenia na następnym spotkaniu.

Po przerwie (06.08.2008)
Witam wszystkich po przerwie. Wczoraj odbył się trening, na którym pojawiły się tylko dwie osoby, mimo, iż zadeklarowali się prawie wszyscy. W każdy poniedziałek, wtorek i czwartek spotykamy się, bez wzglądu na pogodę.

Opracowałem logo zespołu i zaktualizowałem listę zawodników, które wstąpiły tym samym do klubu MTS Giżycko. Osoby wykreślone nie przyniosły koniecznych informacji na czas. Ci, którzy są zainteresowani grą w klubie mogą przynosić dane osobowe. Wykreśleni z listy, która znajdowała się w dziale Zawodnicy mają czas do 14.08.

Liczę na to, że na jutrzejszym treningu zjawią się wszyscy.

Trening z trenerem reprezentacji Polski juniorów oraz zawodnikiem Orkana Sochaczew (13.08.2008)
Jak zapewne zauważyliście zmienił się adres strony, a to za sprawą przeniesienia jej na serwer miasta gizycko.pl. Cała operacja mogła trwać krócej, lecz FTP freezoka.com padło. Od dziś można nas znaleźć pod adresem www.rugby.gizycko.pl. W związku ze tą zmianą musiałem usunąć licznik odwiedzin i komentarze (których nie będzie można już dodawać). Zmiany zaszły też w Galerii.

Dzisiaj o godzinie 10:30 na górnej płycie stadionu MOSiR odbył się trening z p. Maciejem Misiakiem - trenerem reprezentacji Polski juniorów oraz p. Jakubem Sekleckim - zawodnikiem Orkana Sochaczew. Panowie przyjechali do Giżycka na obóz wraz z wcześniej wspomnianą drużyną MKS Orkan Sochaczew, na których treningu mieliśmy także okazje dziś być. Możliwość doświadczenia takiego treningu codziennie się nie zdarza. Zobaczyliśmy jak można bawić się z piłką oraz jakie przydatne ćwiczenia wykorzystywać na naszych spotkaniach.
("Tak się bawi, tak się bawi MTS Rugby Giżycko!") :)
Serdecznie dziękujemy obu Panom i pozdrawiamy.

W Galerii umieściłem zdjęcia z dzisiaj.

UWAGA! Zmieniły się dni, w których odbywają się treningi oraz miejsce spotkań.
Gramy na boisku przy Szkole Podstawowej nr 7 we:
wtorek i czwartek - godz. 18 oraz sobotę - godz. 10:30.
Więcej w dziale Trening.

Aktualizacja strony oraz koszulka klubowa (21.10.2008)
Na stronie widać pare kosmetycznych poprawek.
Zaktualizowałem listę zawodników oraz dział Treningi.
Gramy w soboty o godz. 15:30 i niedziele o 11:00 na stadionie MOSiR (płyta treningowa).

Pojawiła się możliwość zakupu koszulki z logiem zespołu. Po więcej informacji oraz zdjęcia wszystkich zainteresowanych kieruje do działu Kontakt.

Zapraszam na sobotni trening.

Trening z udziałem zawodnika Skry Warszawa (10.11.2008)
Sobotni trening miał odbyć się na hali Szkoły Podstawowej nr 7, jak się jednak okazało dyrektor, z którym byliśmy umówieni na odbiór kluczy nie stawił się na spotkanie oraz nie odbierał telefonu. Aby nie zmarnować treningu, zdecydowaliśmy pograć na świeżym powietrzu. Szczęśliwie udało się, że nie było chłodno.

W treningu naszej drużyny brał udział p. Olgierd Grefkowicz, na co dzień występujący na pozycji skrzydłowego w Skrze Warszawa. Zobaczyliśmy, jaka jest między nami przepaść i ile jeszcze musimy się nauczyć, choć należy pamiętać, że jesteśmy na dobrej drodze. Dziękujemy i pozdrawiamy!

Co do treningów 15 i 16 listopada - pracuje jak mogę nad zdobyciem hali, więc będę informował na bieżąco w przypadku ew. zmiany miejsca treningu. Na ten czas zostaje po staremu i spotykamy się w sobotę o 15:30 na stadionie.

Legitymacje oraz zmiana obiektu (13.11.2008)
Sobotni trening odbędzie się na płycie treningowej MOSiR, lecz zmienia się godzina rozpoczęcia na 15. Trening będzie też nieco krótszy.

Zawodnicy proszeni są o podanie mi numeru swojej legitymacji, najlepiej w wiadomości na GG. Konieczne jest to, abyśmy uzyskali dostęp do hali sportowej. Im szybciej będę miał wszystkie numery, tym szybciej zagramy już na sali.

Informacja o przerwie oraz utworzeniu forum (25.11.2008)
Z uwagi na to, że hala będzie udostępniona nam dopiero po 10 grudnia, a pogoda jest jaka jest, treningi do tego czasu zostają odwołane.

EDIT:
W menu pojawił się link do forum. Po kliknięciu w odnośnik, strona otworzy się w nowym oknie (albo karcie). Zapraszam do zarejestrowania się i udzielania się :)

Przerwy ciąg dalszy - problemy z halą (11.12.2008)
Sobotni trening nie dojdzie do skutku. Wszystko z tego powodu, że w jednostce nie ma dowódcy, który do wczoraj miał podjąć decyzję w sprawie udostępnienia nam hali. Jest jego zastępca, który z pewnych przyczyn, nie udostępnia hali nikomu. Przed świętami dowódca pojawi się na kilka dni i od tego czasu będziemy mogli rozpocząć treningi. Przerwa więc nieco się wydłuży.

Wiadomo, że każdy by chciał już sobie pograć, ale taka karma.

Dostęp do hali oraz życzenia świąteczno-noworoczne (19.12.2008)
Od nowego roku zostanie udostępniona nam hala wojskowa na ul. Nowowiejskiej w godzinach od 15:00 do 18:00. Pierwszy trening w roku 2009 odbędzie się więc 3 stycznia. Od razu zaznaczam, żeby później nie zapomnieć: trzeba stawić się z tym dokumentem, którego numer mi podaliście.
Po świętach dokładnie opisze gdzie się stawić na trening, o której godzinie itd.

Trzeba wykorzystać fakt, że jest dużo czasu wolnego. Niedawno do użytku zostało oddane boisko przy gimnazjum nr 2. Jest okres zimowy i mało osób gra na świeżym powietrzu, więc mamy do dyspozycji wiele terminów. Proponuje wstępnie poniedziałek albo wtorek o godz. 19? Spotkalibyśmy się na 40min-1h, aby pograć. Jak najszybciej piszcie w tym temacie [forum], bo muszę zarezerwować termin.

Korzystam z okazji, żeby złożyć wszystkim najserdeczniejsze życzenia z okazji Bożego Narodzenia oraz Szczęśliwego Nowego Roku.

Trening na hali wojskowej oraz informacje dotyczące dołączania do drużyny (02.01.2009)
Sezon zbliża się wolnym krokiem, czas zacząć przygotowania. Aby występować w lidze zawodnik musi posiadać licencję. Do jej wyrobienia potrzebne są między innymi badania lekarskie. Niestety w Giżycku jest tylko jeden lekarz sportowy i przyjmuje on prywatnie. Koszt wizyty to wydatek rzędu 30 zł, proszę przygotować się na to, że aby zagrać w sezonie 2009 trzeba to załatwić. W następny wtorek będę wiedział, co i jak dokładnie, na forum więc wszystko opisze. Informuje o tym teraz, abyście mieli więcej czasu na ciułanie kasy.

Inna sprawa, przepustkę aktualnie posiada 17 osób, czyli wszyscy dotychczasowi zawodnicy. Jednak ciągle dostaję wiadomości z prośbą o przyłączenie do drużyny, aczkolwiek bez przepustki nie da się wejść na hale. Postarałem się o możliwość dołączenia do drużyny, ale nie wiem, ile w tym przypadku trwało będzie zaakceptowanie osoby i dopisanie jej do listy, więc proszę jak najszybciej przesyłać: imię, nazwisko, PESEL oraz numer dokumentu potwierdzającego tożsamość (dowód, legitymacja, paszport, etc.) wraz z jego nazwą (tzn., co to za dokument).

Treningu w tym tygodniu nie ma z uwagi na to, że nie będzie mnie na miejscu. Zajęcia zostają przeniesione na następną sobotę, tj. 17.01.2009r. Mamy już przepustkę, więc jest to pewniak.
O 14:45 spotykamy się pod Biedronką znajdującej się ul. Wilanowskiej 5 (koło obwodnicy). Nie ma spóźniania, o podanej godzinie wychodzimy spod Biedronki i kierujemy się na hale.

Szkolenie trenerów rugby 7 strefy północnej w Chojnicach (22.03.2009)
W weekend 13-15 marca w Chojnickim hotelu "Olimp" na szkoleniu strefy północnej zebrało się niemal 20 trenerów drużyn rugby 7. Przez 3 dni uczestnicy zdobywali doświadczenie podczas zajęć teoretyczno-praktycznych. Teorię wykładał Tomasz Kapustka oraz Jarosław Bator, praktykę dodatkowo Daniel Kowalski. Duży wkład pracy wniósł również Dominik Jastrzębski z Floty Gdynia.

Zaczynam od soboty, bo dopiero wtedy udało się dotrzeć na miejsce. Sobotni harmonogram przewidywał 4 wykłady teoretyczne (trening FIRA, filozofia gry, podstawowe info o sędziowaniu oraz puchar świata rugby 7) i 2 praktyczne. Podczas porannej praktyki organizatorzy przekazywali nam wiedzę nt. umiejętnej rozgrzewki, prawidłowego podawania piłki - mogliśmy tę wiedzę wykorzystać podczas gry. Na wieczornym treningu uczono nas m.in. prawidłowego ułożenia ciała podczas wykonywania określonych elementów gry, ćwiczyliśmy obronę i atak oraz wykonywaliśmy ćwiczenia ruchowe. Przed kolacją udaliśmy się na "mały rekonesans" do miasta. Zwiedzając Chojnice wpadliśmy m.in. na boisko miejscowego Tura Chojnice.

Niedziela była dniem krótkim dla kursantów, ponieważ wielu uczestników śpieszyło się na mecze swoich drużyn, a jeszcze innych goniły obowiązki. Podczas porannego treningu ćwiczyliśmy młyny oraz dopracowywaliśmy elementy, których prawidłowego wykonania nie byliśmy pewni. W trakcie teorii omawialiśmy m.in. położenie zawodników na boisku.

Kurs był poprowadzony profesjonalnie, kontakt z rugbowym środowiskiem zwiększa motywację i wyzwala chęć do działania. Wiedza zdobyta podczas zajęć pozwoli rozwijać giżycki klub rugby.
Wielkie dzięki dla p. Tomasza Kapustki za zaproszenie i pozdro dla uczestników kursu.

Mecz z WMPD PUDiZ Olsztyn (21.05.2010)
Dane znajdujące się na stronie są już aktualne.

W niedziele 23.05 wybieramy się do stolicy Warmii. Nasi kadeci będą grali z WMPD PUDiZ Olsztyn. Trzymajcie kciuki!

Koniec (18.09.2010)
W związku z moją wyprowadzką na studia nie będę już w stanie dalej prowadzić klubu, dlatego kończymy jego działalność.

Panowie, podopieczni, koledzy, przyjaciele, a także wszyscy, którzy wspierali naszą działalność i kibicowali nam przez te dwa lata – dziękuję za zaangażowanie, wspólną naukę, wiele dobrych chwil, zarówno rugbowych, jak i tych pozasportowych oraz przede wszystkim świetną zabawę.

Michał
```

