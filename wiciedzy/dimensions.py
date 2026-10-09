"""Training-profile axes. These describe practice, not effectiveness."""

from __future__ import annotations

DIMENSIONS: tuple[str, ...] = (
    "striking",
    "grappling",
    "clinch",
    "throws",
    "takedowns",
    "ground_fighting",
    "submissions",
    "punches",
    "kicks",
    "knees",
    "elbows",
    "weapons",
    "solo_training",
    "partner_training",
    "contact_level",
    "competition_level",
    "tradition_level",
    "technical_complexity",
    "athletic_demand",
    "endurance_demand",
    "explosiveness",
    "equipment_required",
)

DIMENSION_LABELS: dict[str, tuple[str, str]] = {
    "striking": ("Uderzenia", "Striking"),
    "grappling": ("Chwyt", "Grappling"),
    "clinch": ("Klincz", "Clinch"),
    "throws": ("Rzuty", "Throws"),
    "takedowns": ("Obalenia", "Takedowns"),
    "ground_fighting": ("Parter", "Ground fighting"),
    "submissions": ("Poddania", "Submissions"),
    "punches": ("Pięści", "Punches"),
    "kicks": ("Kopnięcia", "Kicks"),
    "knees": ("Kolana", "Knees"),
    "elbows": ("Łokcie", "Elbows"),
    "weapons": ("Broń", "Weapons"),
    "solo_training": ("Trening solo", "Solo training"),
    "partner_training": ("Praca z partnerem", "Partner work"),
    "contact_level": ("Kontakt", "Contact"),
    "competition_level": ("Zawody", "Competition"),
    "tradition_level": ("Tradycja", "Tradition"),
    "technical_complexity": ("Złożoność techniczna", "Technical complexity"),
    "athletic_demand": ("Obciążenie fizyczne", "Athletic demand"),
    "endurance_demand": ("Wytrzymałość", "Endurance"),
    "explosiveness": ("Eksplozywność", "Explosiveness"),
    "equipment_required": ("Sprzęt", "Equipment"),
}

def level_words(value: int) -> tuple[str, str]:
    if value <= 1:
        return ("nisko", "low")
    if value <= 3:
        return ("średnio", "medium")
    return ("wysoko", "high")


DIMENSION_GROUPS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("uderzenia", ("striking", "punches", "kicks", "knees", "elbows")),
    ("chwyt", ("grappling", "clinch", "throws", "takedowns", "ground_fighting", "submissions")),
    ("bron", ("weapons",)),
    ("trening", ("solo_training", "partner_training", "contact_level", "competition_level", "tradition_level", "technical_complexity", "athletic_demand", "endurance_demand", "explosiveness", "equipment_required")),
)

HEADLINE_AXES: tuple[str, ...] = (
    "striking",
    "grappling",
    "contact_level",
    "competition_level",
    "weapons",
)

# plus, style-higher minus, user-higher minus. Each pair is Polish, English.
REASON_COPY: dict[str, tuple[tuple[str, str], tuple[str, str], tuple[str, str]]] = {
    "striking": (
        ("Uderzeń jest tu mniej więcej tyle, ile chcesz.", "There's about as much striking here as you want."),
        ("Uderzeń jest tu więcej, niż szukasz.", "There's more striking here than you're after."),
        ("Uderzeń jest tu mniej, niż szukasz.", "There's less striking here than you're after."),
    ),
    "grappling": (
        ("Chwytania jest tu mniej więcej tyle, ile chcesz.", "There's about as much grappling here as you want."),
        ("Chwytania jest tu więcej, niż szukasz.", "There's more grappling here than you're after."),
        ("Chwytania jest tu mniej, niż szukasz.", "There's less grappling here than you're after."),
    ),
    "clinch": (
        ("Klincz jest tu mniej więcej tak ważny, jak chcesz.", "Clinch work matters here about as much as you want."),
        ("Klinczu jest tu więcej, niż szukasz.", "There's more clinch work here than you're after."),
        ("Klinczu jest tu mniej, niż szukasz.", "There's less clinch work here than you're after."),
    ),
    "throws": (
        ("Rzuty są tu mniej więcej tak ważne, jak chcesz.", "Throws matter here about as much as you want."),
        ("Rzutów jest tu więcej, niż szukasz.", "There are more throws here than you're after."),
        ("Rzutów jest tu mniej, niż szukasz.", "There are fewer throws here than you're after."),
    ),
    "takedowns": (
        ("Obaleń jest tu mniej więcej tyle, ile chcesz.", "There are about as many takedowns here as you want."),
        ("Obaleń jest tu więcej, niż szukasz.", "There are more takedowns here than you're after."),
        ("Obaleń jest tu mniej, niż szukasz.", "There are fewer takedowns here than you're after."),
    ),
    "ground_fighting": (
        ("Parteru jest tu mniej więcej tyle, ile chcesz.", "There's about as much ground work here as you want."),
        ("Parteru jest tu więcej, niż szukasz.", "There's more ground work here than you're after."),
        ("Parteru jest tu mniej, niż szukasz.", "There's less ground work here than you're after."),
    ),
    "submissions": (
        ("Szukanie poddania pasuje do tego treningu mniej więcej tak, jak chcesz.", "Going for a submission fits this training about as much as you want."),
        ("Poddania liczą się tu bardziej, niż szukasz.", "Submissions matter more here than you're after."),
        ("Poddania pojawiają się tu rzadziej, niż szukasz.", "Submissions show up less often here than you're after."),
    ),
    "punches": (
        ("Praca pięściami jest tu mniej więcej tak ważna, jak chcesz.", "Punch work matters here about as much as you want."),
        ("Pięści liczą się tu bardziej, niż szukasz.", "Fists matter more here than you're after."),
        ("Pięści liczą się tu mniej, niż szukasz.", "Fists matter less here than you're after."),
    ),
    "kicks": (
        ("Kopnięcia są tu mniej więcej tak istotne, jak chcesz.", "Kicks matter here about as much as you want."),
        ("Kopnięć jest tu więcej, niż szukasz.", "There are more kicks here than you're after."),
        ("Kopnięć jest tu mniej, niż szukasz.", "There are fewer kicks here than you're after."),
    ),
    "knees": (
        ("Kolana są tu mniej więcej tak ważne, jak chcesz.", "Knees matter here about as much as you want."),
        ("Kolana liczą się tu bardziej, niż szukasz.", "Knees matter more here than you're after."),
        ("Kolana liczą się tu mniej, niż szukasz.", "Knees matter less here than you're after."),
    ),
    "elbows": (
        ("Łokcie są tu mniej więcej tak ważne, jak chcesz.", "Elbows matter here about as much as you want."),
        ("Łokcie liczą się tu bardziej, niż szukasz.", "Elbows matter more here than you're after."),
        ("Łokcie liczą się tu mniej, niż szukasz.", "Elbows matter less here than you're after."),
    ),
    "weapons": (
        ("Broń na tym treningu jest mniej więcej tak ważna, jak chcesz.", "Weapons matter in this training about as much as you want."),
        ("Broń jest tu ważniejsza, niż szukasz.", "Weapons matter more here than you're after."),
        ("Broń jest tu mniej ważna, niż szukasz.", "Weapons matter less here than you're after."),
    ),
    "solo_training": (
        ("Jest tu miejsce na pracę solo, której szukasz.", "There's room here for the solo work you're after."),
        ("Pracy solo jest tu więcej, niż szukasz.", "There's more solo work here than you're after."),
        ("Pracy solo jest tu mniej, niż szukasz.", "There's less solo work here than you're after."),
    ),
    "partner_training": (
        ("Praca z partnerem jest tu mniej więcej tak ważna, jak chcesz.", "Partner work matters here about as much as you want."),
        ("Pracy z partnerem jest tu więcej, niż szukasz.", "There's more partner work here than you're after."),
        ("Pracy z partnerem jest tu mniej, niż szukasz.", "There's less partner work here than you're after."),
    ),
    "contact_level": (
        ("Poziom kontaktu pasuje do tego, czego szukasz.", "The amount of contact fits what you're after."),
        ("Kontakt jest mocniejszy, niż chcesz.", "The contact is harder than you want."),
        ("Kontaktu jest tu mniej, niż szukasz.", "There's less contact here than you're after."),
    ),
    "competition_level": (
        ("Zawodów jest tu mniej więcej tyle, ile chcesz.", "There's about as much competition here as you want."),
        ("Jest tu więcej zawodów, niż chcesz.", "There's more competition here than you want."),
        ("Jest tu mniej zawodów, niż chcesz.", "There's less competition here than you want."),
    ),
    "tradition_level": (
        ("Zwyczajów i tradycji na sali jest tu mniej więcej tyle, ile chcesz.", "There's about as much custom and tradition in the hall here as you want."),
        ("Zwyczajów i tradycji na sali jest tu więcej, niż szukasz.", "There's more custom and tradition in the hall here than you're after."),
        ("Zwyczajów i tradycji na sali jest tu mniej, niż szukasz.", "There's less custom and tradition in the hall here than you're after."),
    ),
    "technical_complexity": (
        ("Złożoność techniczna pasuje do tego, czego szukasz.", "The technical complexity fits what you're after."),
        ("Złożoność techniczna jest tu większa, niż szukasz.", "The technical complexity is higher here than you're after."),
        ("Złożoność techniczna jest tu mniejsza, niż szukasz.", "The technical complexity is lower here than you're after."),
    ),
    "athletic_demand": (
        ("Obciążenie ciała jest tu mniej więcej takie, jakiego szukasz.", "The physical demand is about what you're after."),
        ("Ciało jest tu obciążane mocniej, niż chcesz.", "The body is loaded harder here than you want."),
        ("Ciało jest tu obciążane lżej, niż chcesz.", "The body is loaded lighter here than you want."),
    ),
    "endurance_demand": (
        ("Wytrzymałość jest tu mniej więcej tak ważna, jak chcesz.", "Endurance matters here about as much as you want."),
        ("Wytrzymałości trzeba tu więcej, niż szukasz.", "It takes more endurance here than you're after."),
        ("Wytrzymałości trzeba tu mniej, niż szukasz.", "It takes less endurance here than you're after."),
    ),
    "explosiveness": (
        ("Tempo i zryw pasują do tego, czego szukasz.", "The pace and the burst fit what you're after."),
        ("Jest tu więcej zrywu, niż chcesz.", "There's more burst here than you want."),
        ("Jest tu mniej zrywu, niż chcesz.", "There's less burst here than you want."),
    ),
    "equipment_required": (
        ("Sprzętu jest tu mniej więcej tyle, ile chcesz.", "There's about as much kit here as you want."),
        ("Sprzętu jest tu więcej, niż szukasz.", "There's more kit here than you're after."),
        ("Sprzętu jest tu mniej, niż szukasz.", "There's less kit here than you're after."),
    ),
}

DIFF_COPY: dict[str, tuple[str, str]] = {
    "striking": ("{higher} ma więcej uderzeń niż {lower}.", "{higher} has more striking than {lower}."),
    "grappling": ("{higher} ma więcej chwytów niż {lower}.", "{higher} has more grappling than {lower}."),
    "clinch": ("{higher} spędza więcej czasu w zwarciu niż {lower}.", "{higher} spends more time at close range than {lower}."),
    "throws": ("{higher} mocniej opiera się na rzutach niż {lower}.", "{higher} leans on throws more than {lower}."),
    "takedowns": ("{higher} częściej próbuje obalić rywala niż {lower}.", "{higher} goes for takedowns more often than {lower}."),
    "ground_fighting": ("{higher} dłużej zostaje w parterze niż {lower}.", "{higher} stays on the ground longer than {lower}."),
    "submissions": ("{higher} częściej szuka poddania niż {lower}.", "{higher} looks for a submission more often than {lower}."),
    "punches": ("{higher} więcej pracuje pięściami niż {lower}.", "{higher} uses the fists more than {lower}."),
    "kicks": ("{higher} więcej kopie niż {lower}.", "{higher} kicks more than {lower}."),
    "knees": ("{higher} częściej używa kolan niż {lower}.", "{higher} uses knees more often than {lower}."),
    "elbows": ("{higher} częściej używa łokci niż {lower}.", "{higher} uses elbows more often than {lower}."),
    "weapons": ("{higher} wyraźniej stawia na broń niż {lower}.", "{higher} puts more weight on weapons than {lower}."),
    "solo_training": ("{higher} zostawia więcej miejsca na pracę solo niż {lower}.", "{higher} leaves more room for solo practice than {lower}."),
    "partner_training": ("{higher} bardziej potrzebuje partnera niż {lower}.", "{higher} needs a partner more than {lower}."),
    "contact_level": ("{higher} trenuje z mocniejszym kontaktem niż {lower}.", "{higher} trains with harder contact than {lower}."),
    "competition_level": ("{higher} przykłada większą wagę do zawodów niż {lower}.", "{higher} puts more weight on competition than {lower}."),
    "tradition_level": ("{higher} przykłada większą wagę do tradycji sali niż {lower}.", "{higher} puts more weight on the hall's traditions than {lower}."),
    "technical_complexity": ("{higher} ma bardziej rozbudowany arsenał technik niż {lower}.", "{higher} has a broader technical arsenal than {lower}."),
    "athletic_demand": ("{higher} bardziej obciąża ciało niż {lower}.", "{higher} loads the body more than {lower}."),
    "endurance_demand": ("{higher} wymaga większej wytrzymałości niż {lower}.", "{higher} asks more of your endurance than {lower}."),
    "explosiveness": ("{higher} ma więcej zrywu niż {lower}.", "{higher} is more explosive than {lower}."),
    "equipment_required": ("{higher} wymaga więcej sprzętu niż {lower}.", "{higher} needs more kit than {lower}."),
}

# Both sides low, and close. The high-agreement line would claim a lot of the thing.
LOW_REASON_COPY: dict[str, tuple[str, str]] = {
    "striking": ("Uderzeń jest tu mało — i dobrze, bo właśnie tego szukasz.", "There's little striking here — and that's what you want."),
    "grappling": ("Chwytania jest tu mało — i dobrze, bo właśnie tego szukasz.", "There's little grappling here — and that's what you want."),
    "clinch": ("Zwarcia jest tu mało — i dobrze, bo właśnie tego szukasz.", "There's little close-range work here — and that's what you want."),
    "throws": ("Rzutów jest tu mało — i dobrze, bo właśnie tego szukasz.", "There are few throws here — and that's what you want."),
    "takedowns": ("Obaleń jest tu mało — i dobrze, bo właśnie tego szukasz.", "There are few takedowns here — and that's what you want."),
    "ground_fighting": ("Parteru jest tu mało — i dobrze, bo właśnie tego szukasz.", "There's little ground work here — and that's what you want."),
    "submissions": ("Poddania prawie tu nie mają znaczenia — i dobrze, bo właśnie tego szukasz.", "Submissions barely matter here — and that's what you want."),
    "punches": ("Pięści prawie tu nie mają znaczenia — i dobrze, bo właśnie tego szukasz.", "Fists barely matter here — and that's what you want."),
    "kicks": ("Kopnięć jest tu mało — i dobrze, bo właśnie tego szukasz.", "There are few kicks here — and that's what you want."),
    "knees": ("Kolana prawie tu nie mają znaczenia — i dobrze, bo właśnie tego szukasz.", "Knees barely matter here — and that's what you want."),
    "elbows": ("Łokcie prawie tu nie mają znaczenia — i dobrze, bo właśnie tego szukasz.", "Elbows barely matter here — and that's what you want."),
    "weapons": ("Broni prawie tu nie ma — i dobrze, bo właśnie tego szukasz.", "There's almost no weapon here — and that's what you want."),
    "solo_training": ("Pracy solo jest tu mało — i dobrze, bo właśnie tego szukasz.", "There's little solo work here — and that's what you want."),
    "partner_training": ("Pracy z partnerem jest tu mało — i dobrze, bo właśnie tego szukasz.", "There's little partner work here — and that's what you want."),
    "contact_level": ("Kontaktu jest tu mało — i dobrze, bo właśnie tego szukasz.", "There's little contact here — and that's what you want."),
    "competition_level": ("Zawodów jest tu mało — i dobrze, bo właśnie tego szukasz.", "There's little competition here — and that's what you want."),
    "tradition_level": ("Zwyczajów i tradycji na sali jest tu mało — i dobrze, bo właśnie tego szukasz.", "There's little custom and tradition in the hall here — and that's what you want."),
    "technical_complexity": ("Technicznie jest tu prościej — i dobrze, bo właśnie tego szukasz.", "Technically it's simpler here — and that's what you want."),
    "athletic_demand": ("Obciążenia fizycznego jest tu mało — i dobrze, bo właśnie tego szukasz.", "The physical demand is low here — and that's what you want."),
    "endurance_demand": ("Nie potrzeba tu dużej wytrzymałości — i dobrze, bo właśnie tego szukasz.", "You don't need much endurance here — and that's what you want."),
    "explosiveness": ("Zrywu jest tu mało — i dobrze, bo właśnie tego szukasz.", "There's little burst here — and that's what you want."),
    "equipment_required": ("Sprzętu jest tu mało — i dobrze, bo właśnie tego szukasz.", "There's little kit here — and that's what you want."),
}
