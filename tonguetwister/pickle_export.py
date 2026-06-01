import pickle

# Data
keyword_responses = {
    "rejestracja": [
        "Aby się zarejestrować, kliknij przycisk 'Logowanie'.",
        "Zarejestruj się już teraz, aby korzystać z pełni funkcji naszej aplikacji!",
        "Nie masz konta? Rejestracja to tylko chwila!",
    ],
    "kontakt": [
        "Aby się z nami skontaktować, kliknij przycisk 'Kontakt'.",
        "Masz pytania? Napisz do nas!",
        "Kontakt? Jasne, oto link!",
    ],
    "nagrać": [
        "Kliknij przycisk 'Nagraj swój głos', aby rozpocząć nagrywanie.",
        "Chcesz coś nagrać? Śmiało, kliknij 'Nagraj'!",
        "Twoje nagrania są dla Ciebie ważne, aby poprawić swoje umiejętności.",
    ],
    "nagranie": [
        "Kliknij przycisk 'Nagraj swój głos', aby rozpocząć nagrywanie.",
        "Twoje nagrania pomogą Ci śledzić swoje postępy!",
        "Nagranie gotowe? Odsłuchaj i sprawdź swoją wymowę!",
    ],
    "mikrofon": [
        "Proszę zezwolić swojemu urządzeniu na używanie mikrofonu.",
        "Upewnij się, że Twój mikrofon jest włączony.",
        "Jeśli nie słyszysz swojego głosu, sprawdź ustawienia mikrofonu.",
    ],
    "użytkownik": [
        "Korzystaj z przycisku 'Logowanie', aby przejść do swojego konta.",
        "Twoje konto daje Ci dostęp do wszystkich funkcji!",
        "Jesteś zalogowany? Sprawdź swój profil!",
    ],
    "hasło": [
        "Wpisz swoje hasło podczas logowania, aby uzyskać dostęp do aplikacji.",
        "Masz problem z hasłem? Możesz je zresetować!",
        "Nie pamiętasz hasła? Kliknij 'Przypomnij hasło'.",
    ],
    "konto": [
        "Kliknij przycisk 'Zarejestruj się', aby założyć nowe konto.",
        "Posiadanie konta daje Ci pełny dostęp do funkcji aplikacji!",
        "Stwórz konto i zacznij swoją podróż z LingwoŁamkami!",
    ],
    "powrót": [
        "Kliknij przycisk 'Wróć', aby powrócić do poprzedniego ekranu.",
        "Chcesz wrócić? Kliknij przycisk 'Powrót'.",
        "Cofamy się? Żaden problem! Kliknij 'Wróć'.",
    ],
    "lingwołamki": [
        "Lingwołamki to aplikacja, która pomoże Ci poprawić wymowę i nabrać pewności siebie.",
        "Nasza aplikacja LingwoŁamki to zbiór ćwiczeń pomagających w poprawie wymowy.",
        "Ćwicz z LingwoŁamkami i zobacz efekty!",
    ],
    "powtórki": [
        "Dodawaj swoje ulubione ćwiczenia do powtórek, aby zawsze mieć je pod ręką.",
        "Powtórki pomagają w utrwaleniu umiejętności!",
        "Chcesz coś powtórzyć? Sprawdź swoje zapisane ćwiczenia!",
    ],
    "drukować": [
        "Możesz wydrukować swoje ulubione ćwiczenia, klikając odpowiedni przycisk.",
        "Drukuj ćwiczenia, aby korzystać z nich offline!",
        "Przygotuj papier i drukarkę – czas na naukę bez ekranu!",
    ],
    "zacząć": [
        "Przesuń palce, aby rozpocząć.",
        "Każde kliknięcie przybliża Cię do lepszej wymowy!",
        "Zacznij już teraz i zobacz efekty ćwiczeń!",
    ],
    "problem": [
        "Masz problem? Zapytaj naszego czata – jesteśmy tutaj, aby pomóc Ci na każdym kroku.",
        "Nie martw się, chętnie pomożemy!",
        "Potrzebujesz pomocy? Skontaktuj się z nami!",
    ],
    "artykulacyjne": [
        "Ćwiczenia artykulacyjne poprawią Twoją wymowę!",
        "Rozgrzej aparat mowy i zacznij ćwiczyć!",
        "Lepsza artykulacja to lepsza dykcja – spróbuj!",
    ],
    "głosowe": [
        "Ćwiczenia głosowe poprawią Twoją dykcję i ton głosu.",
        "Ćwicz swój głos i mów wyraźniej!",
        "Trenuj swój głos, aby brzmieć pewniej!",
    ],
    "oddechowe": [
        "Ćwiczenia oddechowe pomagają w kontrolowaniu mowy.",
        "Kontrola oddechu to klucz do lepszej artykulacji!",
        "Ćwiczenia oddechowe wspierają naturalny rytm mówienia.",
    ],
    "lusterko": [
        "Kliknij 'Otwórz Lusterko', aby sprawdzić swoje ruchy w lustrze.",
        "Ćwicz przed lustrem, aby kontrolować mimikę i dykcję!",
        "Zobacz, jak porusza się Twój aparat mowy!",
    ],
    "zemsta": [
        "Zemsta logopedy to łamańce językowe – podejmiesz wyzwanie?",
        "Spróbuj zmierzyć się z Zemstą logopedy – dasz radę?",
        "Czy jesteś gotów na wyzwanie? Sprawdź Zemstę logopedy!",
    ],
    "awatar": [
        "Kliknij 'Zarządzaj Awatarem', aby dostosować swoje zdjęcie profilowe.",
        "Chcesz zmienić swój awatar? Możesz to zrobić w ustawieniach!",
        "Dodaj swój własny awatar i wyróżnij się!",
    ],
    "kurs": [
        "Lingwołamki oferują specjalistyczne kursy wymowy.",
        "Zapisz się na kurs i popraw swoją wymowę!",
        "Nasze kursy wymowy pomogą Ci mówić wyraźniej.",
    ],
    "sesja": [
        "Zaplanuj swoją sesję i ćwicz regularnie!",
        "Regularność to klucz do sukcesu – planuj swoje treningi!",
        "Planowanie sesji ćwiczeniowych pomoże Ci osiągnąć zamierzone cele.",
    ],
    "pomoc": [
        "Jeśli potrzebujesz pomocy, odwiedź sekcję 'Kontakt'.",
        "Masz problem? Możesz liczyć na naszą pomoc!",
        "W czym mogę pomóc? Sprawdź sekcję Pomoc!",
    ],
    "artykulator": [
        "Zarządzaj artykulatorami i dostosuj je do swoich potrzeb.",
        "Ćwicz artykulację i popraw swoją dykcję!",
        "Artykulatory pomagają w lepszej wymowie – sprawdź je!",
    ],
    "ćwiczenie": [
        "Odkrywaj i zarządzaj ćwiczeniami oraz personalizuj swoje treningi.",
        "Chcesz zrobić ćwiczenie? Oto lista dostępnych!",
        "Ćwiczenia pomogą Ci w poprawie wymowy!",
    ],
    "porada": [
        "Przeglądaj i zarządzaj poradami językowymi.",
        "Masz ochotę na dobrą poradę językową?",
        "Porady językowe mogą poprawić Twoją wymowę!",
    ],
    "ciekawostka": [
        "Odkrywaj i zarządzaj ciekawostkami językowymi.",
        "Czy wiesz, że język polski ma ponad 140 tysięcy słów?",
        "Chcesz poznać coś nowego? Sprawdź ciekawostki!",
    ],
    "staropolszczyzna": [
        "Odkrywaj słowa ze staropolszczyzny.",
        "Dawne słowa mają swoją magię – zobacz, jakie wyszły z użycia!",
        "Znasz jakieś słowo ze staropolszczyzny? Sprawdź naszą bazę!",
    ],
    "łamaniec": [
        "Zarządzaj łamańcami językowymi i sprawdzaj swoje umiejętności.",
        "Próbowałeś już jakiegoś łamańca? Sprawdź dostępne!",
        "Łamańce językowe to świetny sposób na poprawę dykcji!",
    ],
    "logopeda": [
        "Zemsta logopedy to łamańce językowe, które znajdziesz w aplikacji Lingwołamki.",
        "Czy jesteś gotów na wyzwanie logopedyczne? Sprawdź nasze ćwiczenia!",
        "Ćwiczenia logopedyczne pomagają w wyraźnej i płynnej mowie.",
    ],
    "zdjęcie": [
        "Kliknij przycisk 'Zarządzaj Awatarem', aby dostosować swoje zdjęcie profilowe.",
        "Chcesz zmienić swoje zdjęcie? Możesz to zrobić w ustawieniach!",
        "Dodaj swój awatar, aby spersonalizować swoje konto!",
    ],
    "święto": [
        "🎉 Wszystkiego najlepszego z okazji Dnia Kobiet! LingwoŁamek życzy samych sukcesów i radości!",
    ],
}


negative_words = {
    "okropne",
    "straszne",
    "tragiczne",
    "złe",
    "smutne",
    "przykre",
    "beznadziejne",
    "denerwujące",
    "nudne",
    "uciążliwe",
    "stresujące",
    "nieprzyjemne",
    "irytujące",
    "fatalne",
    "przerażające",
    "problematyczne",
    "nieakceptowalne",
    "męczące",
    "niezadowalające",
    "odpychające",
    "zawstydzające",
    "frustrujące",
    "niszczące",
    "potworne",
    "kiepskie",
    "bezwartościowe",
    "nieszczęśliwe",
    "depresyjne",
    "żenujące",
    "katastrofalne",
    "zdradliwe",
    "niedopuszczalne",
    "niewygodne",
    "bolesne",
    "krępujące",
    "żałosne",
    "rozczarowujące",
    "nieudane",
    "zniechęcające",
    "rozpaczliwe",
    "wrogie",
    "nieprzystępne",
    "niszczycielskie",
    "przytłaczające",
    "zdołowane",
    "toksyczne",
    "żałobne",
    "bezsilne",
    "tłamszące",
    "odrażające",
}

positive_words = {
    "wspaniałe",
    "niesamowite",
    "świetne",
    "fantastyczne",
    "pozytywne",
    "doskonałe",
    "radosne",
    "inspirujące",
    "przyjemne",
    "relaksujące",
    "imponujące",
    "satysfakcjonujące",
    "wyjątkowe",
    "cudowne",
    "piękne",
    "zachwycające",
    "fenomenalne",
    "wartościowe",
    "podnoszące na duchu",
    "motywujące",
    "porywające",
    "rewelacyjne",
    "ekscytujące",
    "owocne",
    "energetyzujące",
    "szczęśliwe",
    "optymistyczne",
    "fascynujące",
    "budujące",
    "genialne",
    "urocze",
    "radosne",
    "promienne",
    "pomyślne",
    "zdumiewające",
    "odprężające",
    "hojne",
    "zabawne",
    "pewne",
    "wyborne",
    "magiczne",
    "natchnione",
    "radosne",
    "dobroczynne",
    "życzliwe",
    "spektakularne",
    "harmonijne",
    "kojące",
    "twórcze",
    "szlachetne",
    "dobre",
}

# Save to .pkl
with open("data/keywords.pkl", "wb") as f:
    pickle.dump(keyword_responses, f)

with open("data/negative_words.pkl", "wb") as f:
    pickle.dump(negative_words, f)

with open("data/positive_words.pkl", "wb") as f:
    pickle.dump(positive_words, f)

print("Saved in .pkl!")
