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
    "athletic_demand": ("Wymaganie fizyczne", "Athletic demand"),
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
        ("Odpowiada Ci trening, w którym dużo się uderza.", "A training with a lot of striking fits you."),
        ("Uderzeń jest tu więcej niż chcesz.", "There is more striking here than you want."),
        ("Uderzeń jest tu mniej niż chcesz.", "There is less striking here than you want."),
    ),
    "grappling": (
        ("Odpowiada Ci trening, w którym dużo się chwyta.", "A training with a lot of gripping fits you."),
        ("Chwytu jest tu więcej niż chcesz.", "There is more gripping here than you want."),
        ("Chwytu jest tu mniej niż chcesz.", "There is less gripping here than you want."),
    ),
    "clinch": (
        ("Walka w zwarciu pasuje do tego, czego szukasz.", "Close-range work fits what you are looking for."),
        ("Zwarcia jest tu więcej niż chcesz.", "There is more close-range work here than you want."),
        ("Zwarcia jest tu mniej niż chcesz.", "There is less close-range work here than you want."),
    ),
    "throws": (
        ("Rzuty są tu tak ważne, jak chcesz.", "Throws matter here about as much as you want."),
        ("Rzutów jest tu więcej niż chcesz.", "There are more throws here than you want."),
        ("Rzutów jest tu mniej niż chcesz.", "There are fewer throws here than you want."),
    ),
    "takedowns": (
        ("Obaleń jest tu tyle, ile chcesz.", "Takedowns sit where you are looking."),
        ("Obaleń jest tu więcej niż chcesz.", "There are more takedowns here than you want."),
        ("Obaleń jest tu mniej niż chcesz.", "There are fewer takedowns here than you want."),
    ),
    "ground_fighting": (
        ("Parteru jest tu tyle, ile chcesz.", "The ground is as present here as you want."),
        ("Parteru jest tu więcej niż chcesz.", "There is more ground work here than you want."),
        ("Parteru jest tu mniej niż chcesz.", "There is less ground work here than you want."),
    ),
    "submissions": (
        ("Poddań jest tu tyle, ile chcesz.", "Looking for a submission fits this training."),
        ("Poddań jest tu więcej niż chcesz.", "Submissions matter more here than you want."),
        ("Poddań jest tu mniej niż chcesz.", "Submissions matter less here than you want."),
    ),
    "punches": (
        ("Praca pięścią jest tu tak ważna, jak chcesz.", "Fist work matters here about as much as you want."),
        ("Pracy pięścią jest tu więcej niż chcesz.", "There is more fist work here than you want."),
        ("Pracy pięścią jest tu mniej niż chcesz.", "There is less fist work here than you want."),
    ),
    "kicks": (
        ("Kopnięcia są tu tak częste, jak chcesz.", "Kicks are about as common here as you want."),
        ("Kopnięć jest tu więcej niż chcesz.", "There are more kicks here than you want."),
        ("Kopnięć jest tu mniej niż chcesz.", "There are fewer kicks here than you want."),
    ),
    "knees": (
        ("Kolan jest tu tyle, ile chcesz.", "Knees are as present here as you want."),
        ("Kolan jest tu więcej niż chcesz.", "Knees matter more here than you want."),
        ("Kolan jest tu mniej niż chcesz.", "Knees matter less here than you want."),
    ),
    "elbows": (
        ("Łokci jest tu tyle, ile chcesz.", "Elbows are as present here as you want."),
        ("Łokci jest tu więcej niż chcesz.", "Elbows matter more here than you want."),
        ("Łokci jest tu mniej niż chcesz.", "Elbows matter less here than you want."),
    ),
    "weapons": (
        ("Broń w tym treningu jest tak ważna, jak chcesz.", "Weapons matter in this training about as much as you want."),
        ("Broń w tym treningu jest ważniejsza niż chcesz.", "Weapons matter more in this training than you want."),
        ("Broni jest tu mniej niż chcesz.", "Weapons matter less here than you want."),
    ),
    "solo_training": (
        ("Jest tu miejsce na pracę solo, której szukasz.", "There is room here for the solo work you want."),
        ("Pracy solo jest tu więcej niż chcesz.", "There is more solo work here than you want."),
        ("Pracy solo jest tu mniej niż chcesz.", "There is less solo work here than you want."),
    ),
    "partner_training": (
        ("Praca z partnerem jest tu tak ważna, jak chcesz.", "Partner work matters here about as much as you want."),
        ("Pracy z partnerem jest tu więcej niż chcesz.", "There is more partner work here than you want."),
        ("Pracy z partnerem jest tu mniej niż chcesz.", "There is less partner work here than you want."),
    ),
    "contact_level": (
        ("Poziom kontaktu pasuje do tego, czego szukasz.", "The amount of contact fits what you are looking for."),
        ("Kontakt jest tu mocniejszy niż chcesz.", "The contact here is harder than you want."),
        ("Kontaktu jest tu mniej niż chcesz.", "There is less contact here than you want."),
    ),
    "competition_level": (
        ("Zawodów jest tu tyle, ile chcesz.", "Competition is as present here as you want."),
        ("Zawody są tu ważniejsze niż chcesz.", "Competition matters more here than you want."),
        ("Zawodów jest tu mniej niż chcesz.", "There is less competition here than you want."),
    ),
    "tradition_level": (
        ("Tradycji sali jest tu tyle, ile chcesz.", "The hall's tradition is as present here as you want."),
        ("Tradycji jest tu więcej niż chcesz.", "Tradition matters more here than you want."),
        ("Tradycji jest tu mniej niż chcesz.", "Tradition matters less here than you want."),
    ),
    "technical_complexity": (
        ("Złożoność techniczna pasuje do tego, czego szukasz.", "The technical load fits what you are looking for."),
        ("Techniki jest tu więcej niż chcesz.", "The technical load is higher here than you want."),
        ("Techniki jest tu mniej niż chcesz.", "The technical load is lower here than you want."),
    ),
    "athletic_demand": (
        ("Obciążenie ciała jest tu takie, jakiego szukasz.", "The physical demand fits what you are looking for."),
        ("Ciało jest tu bardziej obciążone niż chcesz.", "The body is loaded more here than you want."),
        ("Obciążenia fizycznego jest tu mniej niż chcesz.", "The physical demand is lower here than you want."),
    ),
    "endurance_demand": (
        ("Wytrzymałość jest tu tak ważna, jak chcesz.", "Endurance matters here about as much as you want."),
        ("Wytrzymałości trzeba tu więcej niż chcesz.", "Endurance matters more here than you want."),
        ("Wytrzymałości trzeba tu mniej niż chcesz.", "Endurance matters less here than you want."),
    ),
    "explosiveness": (
        ("Tempo i zryw pasują do tego, czego szukasz.", "Pace and burst fit what you are looking for."),
        ("Zrywu jest tu więcej niż chcesz.", "There is more burst here than you want."),
        ("Zrywu jest tu mniej niż chcesz.", "There is less burst here than you want."),
    ),
    "equipment_required": (
        ("Sprzętu jest tu tyle, ile chcesz.", "There is about as much kit here as you want."),
        ("Sprzętu jest tu więcej niż chcesz.", "There is more kit here than you want."),
        ("Sprzętu jest tu mniej niż chcesz.", "There is less kit here than you want."),
    ),
}

DIFF_COPY: dict[str, tuple[str, str]] = {
    "striking": ("{higher} ma więcej uderzeń niż {lower}.", "{higher} has more striking than {lower}."),
    "grappling": ("{higher} ma więcej chwytu niż {lower}.", "{higher} has more gripping than {lower}."),
    "clinch": ("{higher} spędza więcej czasu w zwarciu niż {lower}.", "{higher} spends more time at close range than {lower}."),
    "throws": ("{higher} opiera się mocniej na rzutach niż {lower}.", "{higher} leans more on throws than {lower}."),
    "takedowns": ("{higher} częściej schodzi do obalenia niż {lower}.", "{higher} looks for takedowns more often than {lower}."),
    "ground_fighting": ("{higher} zostaje dłużej w parterze niż {lower}.", "{higher} stays on the ground longer than {lower}."),
    "submissions": ("{higher} częściej szuka poddania niż {lower}.", "{higher} looks for a submission more often than {lower}."),
    "punches": ("{higher} więcej pracuje pięścią niż {lower}.", "{higher} uses the fists more than {lower}."),
    "kicks": ("{higher} więcej kopie niż {lower}.", "{higher} kicks more than {lower}."),
    "knees": ("{higher} częściej używa kolan niż {lower}.", "{higher} uses knees more than {lower}."),
    "elbows": ("{higher} częściej używa łokci niż {lower}.", "{higher} uses elbows more than {lower}."),
    "weapons": ("Broń jest ważniejsza w {higher} niż w {lower}.", "Weapons matter more in {higher} than in {lower}."),
    "solo_training": ("W {higher} jest więcej pracy solo niż w {lower}.", "{higher} leaves more work for solo practice than {lower}."),
    "partner_training": ("{higher} mocniej wymaga partnera niż {lower}.", "{higher} needs a partner more than {lower}."),
    "contact_level": ("{higher} trenuje z mocniejszym kontaktem niż {lower}.", "{higher} trains with harder contact than {lower}."),
    "competition_level": ("Zawody są ważniejsze w {higher} niż w {lower}.", "Competition matters more in {higher} than in {lower}."),
    "tradition_level": ("Tradycja sali jest ważniejsza w {higher} niż w {lower}.", "Hall tradition weighs more in {higher} than in {lower}."),
    "technical_complexity": ("W {higher} techniki jest więcej niż w {lower}.", "{higher} is technically denser than {lower}."),
    "athletic_demand": ("{higher} bardziej obciąża ciało niż {lower}.", "{higher} loads the body more than {lower}."),
    "endurance_demand": ("W {higher} wytrzymałość liczy się bardziej niż w {lower}.", "{higher} asks more of endurance than {lower}."),
    "explosiveness": ("W {higher} jest więcej zrywu niż w {lower}.", "{higher} is more explosive than {lower}."),
    "equipment_required": ("{higher} wymaga więcej sprzętu niż {lower}.", "{higher} needs more kit than {lower}."),
}

# Both sides low, and close. The high-agreement line would claim a lot of the thing.
LOW_REASON_COPY: dict[str, tuple[str, str]] = {
    "striking": ("Uderzeń jest tu mało. Właśnie tego szukasz.", "There is little striking here, and that is what you want."),
    "grappling": ("Chwytu jest tu mało. Właśnie tego szukasz.", "There is little gripping here, and that is what you want."),
    "clinch": ("Zwarcia jest tu mało. Właśnie tego szukasz.", "There is little close-range work here, and that is what you want."),
    "throws": ("Rzutów jest tu mało. Właśnie tego szukasz.", "There are few throws here, and that is what you want."),
    "takedowns": ("Obaleń jest tu mało. Właśnie tego szukasz.", "There are few takedowns here, and that is what you want."),
    "ground_fighting": ("Parteru jest tu mało. Właśnie tego szukasz.", "There is little ground work here, and that is what you want."),
    "submissions": ("Poddań jest tu mało. Właśnie tego szukasz.", "Submissions barely matter here, and that is what you want."),
    "punches": ("Pracy pięścią jest tu mało. Właśnie tego szukasz.", "There is little fist work here, and that is what you want."),
    "kicks": ("Kopnięć jest tu mało. Właśnie tego szukasz.", "There are few kicks here, and that is what you want."),
    "knees": ("Kolan jest tu mało. Właśnie tego szukasz.", "Knees barely matter here, and that is what you want."),
    "elbows": ("Łokci jest tu mało. Właśnie tego szukasz.", "Elbows barely matter here, and that is what you want."),
    "weapons": ("Broni tu prawie nie ma. Właśnie tego szukasz.", "There is almost no weapon here, and that is what you want."),
    "solo_training": ("Pracy solo jest tu mało. Właśnie tego szukasz.", "There is little solo work here, and that is what you want."),
    "partner_training": ("Pracy z partnerem jest tu mało. Właśnie tego szukasz.", "There is little partner work here, and that is what you want."),
    "contact_level": ("Kontaktu jest tu mało. Właśnie tego szukasz.", "There is little contact here, and that is what you want."),
    "competition_level": ("Zawodów jest tu mało. Właśnie tego szukasz.", "There is little competition here, and that is what you want."),
    "tradition_level": ("Tradycji jest tu mało. Właśnie tego szukasz.", "Tradition barely matters here, and that is what you want."),
    "technical_complexity": ("Techniki jest tu mało. Właśnie tego szukasz.", "The technical load is low here, and that is what you want."),
    "athletic_demand": ("Obciążenia fizycznego jest tu mało. Właśnie tego szukasz.", "The physical demand is low here, and that is what you want."),
    "endurance_demand": ("Wytrzymałości trzeba tu mało. Właśnie tego szukasz.", "Endurance barely matters here, and that is what you want."),
    "explosiveness": ("Zrywu jest tu mało. Właśnie tego szukasz.", "There is little burst here, and that is what you want."),
    "equipment_required": ("Sprzętu jest tu mało. Właśnie tego szukasz.", "There is little kit here, and that is what you want."),
}
