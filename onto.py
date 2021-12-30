from owlready2 import *


onto = get_ontology("file://movie_onto.owl").load()
with onto:
    class MotionPicture(Thing): pass
    class Person(Thing): pass
    class Company(Thing): pass

    class FeatureFilm(MotionPicture): pass
    class TVSeries(MotionPicture): pass
    class ShortFilm(MotionPicture): pass
    class SmallSeries(MotionPicture): pass
    AllDisjoint([FeatureFilm, TVSeries, ShortFilm, SmallSeries])
    
    class Genre(Thing): pass
    class ReleaseDate(Thing): pass
    class Country(Thing): pass
    class Award(Thing): pass
    class Rating(Thing): pass
    class Runtime(Thing): pass
    class Soundtrack(Thing): pass
    class VisualEffects(Company): pass

    class Studio(Company): pass
    class Director(Person): pass
    class Actor(Person): pass
    class Writer(Person): pass
    class Composer(Person): pass
    class ProductionDesigner(Person): pass
    class VFXCompany(Company): pass
    class Cinematographer(Person): pass
    class Crew(Company): pass

    class has_genre(MotionPicture >> Genre): pass
    class released_on(MotionPicture >> ReleaseDate): pass
    class produced_where(MotionPicture >> Country): pass
    class is_rated(MotionPicture >> Rating): pass
    class has_runtime(MotionPicture >> Runtime): pass
    class is_awarded(MotionPicture >> Award): pass
    class awarded_to(ObjectProperty):
        domain           = [Award]
        range            = [MotionPicture]
        inverse_property = is_awarded

    class GoodMovie(FeatureFilm):
        is_a = [is_awarded.some(Award)]

    class part_of(Crew >> Crew, TransitiveProperty): pass
    class consists_of(Crew >> Person): pass
    class is_in(ObjectProperty):
        domain           = [Person]
        range            = [Crew]
        inverse_property = consists_of

    class produced_by(MotionPicture >> Studio): pass
    class directed_by(MotionPicture >> Director): pass
    class shot_by(MotionPicture >> Cinematographer): pass
    class written_by(MotionPicture >> Writer): pass
    class recorded_by(Soundtrack >> Composer): pass
    class designed_by(MotionPicture >> ProductionDesigner): pass
    class created_by(VisualEffects >> VFXCompany): pass
    class played_by(MotionPicture >> Actor): pass
    class acted_in(ObjectProperty):
        domain           = [Actor]
        range            = [MotionPicture]
        inverse_property = played_by

    the_dark_knight = FeatureFilm("The Dark Knight")
    the_prestige = FeatureFilm("The Prestige")

    oscar = Award("Oscar")
    emmy = Award("Emmy")
    empire_award = Award("Empire Awards")
    bafta = Award("BAFTA")
    
    Christopher_Nolan = Director("Christopher Nolan")
    Wally_Pfister = Cinematographer("Wally Pfister")
    Nathan_Crowley = ProductionDesigner("Nathan Crowley")
    Hans_Zimmer = Composer("Hans Zimmer")
    David_Julyan = Composer("David Julyan")
    Jonathan_Nolan = Writer("Jonathan Nolan")

    Christian_Bale = Actor("Christian Bale")
    Heath_Ledger = Actor("Heath Ledger")
    Michael_Caine = Actor("Michael Caine")
    Hugh_Jackman = Actor("Hugh Jackman")
    Rebecca_Hall = Actor("Rebecca Hall")
    Scarlett_Johansson = Actor("Scarlett Johansson")

    dneg = VFXCompany("DNEG")
    buf = VFXCompany("BUF")
    Warner = Studio("Warner Bros.")
    
    the_dark_knight_soundtrack = Soundtrack("The Dark Knight")
    the_dark_knight_soundtrack.recorded_by = [Hans_Zimmer]
    the_dark_knight.directed_by = [Christopher_Nolan]
    the_dark_knight.written_by = [Jonathan_Nolan]
    the_dark_knight.produced_by = [Warner]
    the_dark_knight.designed_by = [Nathan_Crowley]
    the_dark_knight.created_by = [dneg]
    the_dark_knight.played_by = [Christian_Bale, Heath_Ledger, Michael_Caine]
    the_dark_knight.is_awarded = [oscar, bafta, empire_award]

    the_prestige_soundtrack = Soundtrack("The Prestige")
    the_prestige_soundtrack.recorded_by = [David_Julyan]
    the_prestige.directed_by = [Christopher_Nolan]
    the_prestige.written_by = [Jonathan_Nolan]
    the_prestige.produced_by = [Warner]
    the_prestige.designed_by = [Nathan_Crowley]
    the_prestige.created_by = [buf]
    the_prestige.played_by = [Christian_Bale, Hugh_Jackman, Michael_Caine, Rebecca_Hall, Scarlett_Johansson]
    the_prestige.is_awarded = [empire_award]

    print("{} is played by {}".format(the_dark_knight, the_dark_knight.played_by))
    print("{} acted in {}".format(Christian_Bale, Christian_Bale.acted_in))
    print("{} awarded to {}".format(oscar, oscar.awarded_to))

    print("\nSynchronization of the reasoner...")
    sync_reasoner()
    print()

#print(list(default_world.inconsistent_classes()))
print(onto.get_parents_of(Christian_Bale))
print(onto.get_parents_of(the_dark_knight_soundtrack))
print(onto.GoodMovie.is_a)
onto.save(file = "result.rdfxml", format = "rdfxml")
