__author__ = 'gg12kg'

import re
from recordtype import recordtype

countrylist = dict(Cameroon="Cm",
                   Nigeria="Ng",
                   Gabon="Ga",
                   Angola="Ao",
                   Brazzaville="Cg",
                   Kinshasa="Cd",
                   DRC="Cd",
                   Equatorial="Gq",
                   Ghana="Gh",
                   CAR="Cf"
                   )

# countrylist = dict(Cameroon="Cameroon",
#                    Nigeria="Nigeria",
#                    Gabon="Gabon",
#                    Angola="Angola",
#                    Brazzaville="Congo-Brazzaville",
#                    Kinshasa="Congo-Kinshasa",
#                    Equatorial="Equatorial Guinea",
#                    Ghana="Ghana"
#                    )

digits = dict(one = '1',
              two = '2',
              three = '3',
              four = '4',
              five = '5',
              six = '6',
              seven = '7',
              eight = '8',
              nine = '9',
              ten = '10')

def get_country_names(rangetxt):
    clist = [countrylist[ckey] for ckey in countrylist.keys() if ckey in rangetxt]
    return clist

locRec = recordtype('locRec','AOO,EOO,Locations',default=None)

def getAOOandEOO(assessment_text):

    AOO = None
    EOO = None
    Locations = None
    m = re.search(r'AOO\D+(\d+) km', assessment_text )
    if m:
        AOO = m.group(1)
    m = re.search(r'EOO\D+(\d+) km', assessment_text )
    if m:
        EOO = m.group(1)
    m = re.search(r'(one|two|three|four|five|six|seven|eight|nine|ten) location', assessment_text )
    if m:
        Locations = digits[m.group(1)]

    return locRec(AOO, EOO, Locations)

elevRec = recordtype('elevRec','ElevFrom,ElevTo',default=None)
reelev = re.compile(r'(\d+).(\d+) m|(\d+) m')

def getElevations(habitattxt):
    minElev=None
    maxElev=None

    m = reelev.search(habitattxt )
    if m:
        if m.group(3):
            minElev = m.group(3)
        else:
            minElev = m.group(1)
            maxElev = m.group(2)

    return elevRec(minElev,maxElev)


if __name__ == "__main__":
    rtext = r"Cameroon (S: 25 km S Djoum.  E: 36 km NE Moloundou.  C: Mefou proposed NP), Gabon (Minkebe;" \
            "and Lastoursville-Poungou; ibid-Bounzoco; Moila-Mounabounou) and Angola (Golungo Alto, type)."
    print(get_country_names(rtext))

    print(getAOOandEOO('Here Dracaena talbotii is assessed as Endangered since only two locations (above; AOO 8 km² with 4 km² cells) are known, with threats as below'))

    print(getElevations('lowland forest; c. 450-1000 m alt.'))