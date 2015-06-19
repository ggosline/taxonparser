from collections import OrderedDict

__author__ = 'gg12kg'

import csv
from lxml import etree
import os

tx_upper_levels = {}
with open('SIS_taxonomy_upper_levels.csv') as txulcsv:
    txulrdr = csv.DictReader(txulcsv)
    for row in txulrdr:
        tx_upper_levels[row['family']] = row

Allfields = r"internal_taxon_id	LocationsNumber.range	MapStatus.status	BiogeographicRealm.realm	System.value	" \
            r"ElevationLower.limit	ElevationUpper.limit	PopulationTrend.value	PopulationSize.range	" \
            r"MaxSubpopulationSize.range	SubpopulationNumber.range	SubpopulationSingle.value	" \
            r"GenerationLength.range	PopulationDocumentation.narrative	RangeDocumentation.narrative	" \
            r"HabitatDocumentation.narrative	ThreatsDocumentation.value	ConservationActionsDocumentation.narrative	" \
            r"RedListCriteriaVersion.criteriaVersion	RedListAssessmentDate.value	RedListCriteria.manualCategory	RedListCriteria.manualCriteria	" \
            r"ExtinctionProbabilityGenerations3.range	ExtinctionProbabilityGenerations5.range	ExtinctionProbabilityYears100.range	" \
            r"RedListRationale.value	AssessmentGeographicScope.geographicScope	AssessmentGeographicScope.region	" \
            r"CropWildRelative.isRelative	" \
            r"AOO.range	EOO.range	AOOContinuingDecline.isInContinuingDecline	AOOContinuingDecline.qualifier	" \
            r"AOOExtremeFluctuation.isFluctuating	EOOContinuingDecline.isInContinuingDecline	EOOContinuingDecline.qualifier	" \
            r"EOOExtremeFluctuation.isFluctuating	PopulationContinuingDecline.isInContinuingDecline	" \
            r"PopulationContinuingDecline.qualifier	PopulationExtremeFluctuation.isFluctuating	" \
            r"SevereFragmentation.isFragmented	SubpopulationContinuingDecline.isDeclining	SubpopulationContinuingDecline.qualifier	" \
            r"SubpopulationExtremeFluctuation.isFluctuating	HabitatContinuingDecline.isInContinuingDecline	" \
            r"HabitatContinuingDecline.qualifier	LocationContinuingDecline.isDeclining	LocationContinuingDecline.qualifier	" \
            r"LocationExtremeFluctuation.isFluctuating	inplaceresearchrecoveryplan.value	inplaceresearchmonitoringscheme.value	" \
            r"inplacelandwaterprotectionsitesidentified.value	inplacelandwaterprotectioninpa.value	inplacelandwaterprotectionareaplanned.value	" \
            r"inplacelandwaterprotectioninvasivecontrol.value	inplacespeciesmanagementharvestplan.value	inplacespeciesmanagementreintroduced.value	" \
            r"inplacespeciesmanagementexsitu.value	inplaceeducationsubjecttoprograms.value	inplaceeducationinternationallegislation.value	" \
            r"inplaceeducationcontrolled.value	inplacelandwaterprotectionpercentprotected.value	" \
            r"PopulationReductionPast.range	PopulationReductionPastReversible.value	PopulationReductionPastUnderstood.value	" \
            r"PopulationReductionPastCeased.value	PopulationReductionPastBasis.value	PopulationReductionFuture.range	" \
            r"PopulationReductionFutureBasis.value	PopulationReductionPastandFuture.range	PopulationReductionPastandFutureReversible.value	" \
            r"PopulationReductionPastandFutureUnderstood.value	PopulationReductionPastandFutureCeased.value	" \
            r"PopulationReductionPastandFutureBasis.value	PopulationDeclineGenerations1.range	" \
            r"PopulationDeclineGenerations1.qualifier	PopulationDeclineGenerations2.range	" \
            r"PopulationDeclineGenerations2.qualifier	PopulationDeclineGenerations3.range	" \
            r"PopulationDeclineGenerations3.qualifier	PopulationDeclineGenerations3.qualifier"

Assessment = "internal_taxon_id" \
             "RangeDocumentation.narrative MapStatus.status BiogeographicRealm.realm PopulationDocumentation.narrative PopulationTrend.value " \
             "HabitatDocumentation.narrative System.value UseTradeDocumentation.value ThreatsDocumentation.value ConservationActionsDocumentation.narrative " \
             "RedListCriteria.critVersion RedListCriteria.isManual RedListCriteria.manualCategory RedListCriteria.manualCriteria RedListCriteria.possiblyExtinct " \
             "RedListCriteria.possiblyExtinctCandidate RedListCriteria.yearLastSeen RedListCriteria.dataDeficientReason RedListAssessmentDate.value " \
             "RedListRationale.value RangeDocumentation.narrative MapStatus.status BiogeographicRealm.realm PopulationDocumentation.narrative " \
             "PopulationTrend.value HabitatDocumentation.narrative System.value UseTradeDocumentation.value ThreatsDocumentation.value " \
             "ConservationActionsDocumentation.narrative RedListCriteria.critVersion RedListCriteria.isManual RedListCriteria.manualCategory " \
             "RedListCriteria.manualCriteria RedListCriteria.possiblyExtinct RedListCriteria.possiblyExtinctCandidate RedListCriteria.yearLastSeen " \
             "RedListCriteria.dataDeficientReason RedListAssessmentDate.value RedListRationale.value"

Taxonomy = r"internal_taxon_id	kingdom	phylum	classname	ordername	family	genus	species	taxonomicAuthority	infraType	infra_name	infra_authority	TaxonomicNotes.value"

Threats = r"internal_taxon_id	Threats.ThreatsLookup	Threats.timing	Threats.scope	Threats.severity	Threats.stress"

ConservationNeededFieldList = ("internal_taxon_id",
                               "ConservationActions.ConservationActionsLookup", "ConservationActions.Note")

HabitatsFieldList = ("internal_taxon_id",
                     "GeneralHabitats.GeneralHabitatsLookup", "GeneralHabitats.suitability",
                     "GeneralHabitats.majorImportance")

CountryFieldList = ("internal_taxon_id", "CountryOccurrence.CountryOccurrenceSubfield.CountryOccurrenceLookup",
                    "CountryOccurrence.CountryOccurrenceSubfield.presence",
                    "CountryOccurrence.CountryOccurrenceSubfield.origin")

CreditsFieldList = ('internal_taxon_id', 'credit_type', 'firstName', 'lastName', 'Order',
                    'email', 'user_id')

MartinCheek = {'credit_type': 'Assessor', 'firstName': 'Martin', 'lastName': 'Cheek', 'Order': '1',
               'email': 'm.cheek@kew.org', 'user_id': '2'}

JMOnana = {'credit_type': 'Reviewer', 'firstName': 'Jean Michel', 'lastName': 'Onana', 'Order': '2',
           'email': 'jmonana2002@yahoo.fr', 'user_id': '1'}

ReferencesRB = {'type': 'Book', 'author': 'Onona, J.M. & Cheek, H.', 'year': '2011',
                'title': 'Red Data Book of the Flowering Plants of Cameroon: IUCN Global Assessments',
                'publisher': 'Kew Publishing',
                'Reference_type': 'Assessment',
                'internal_taxon_id': None}

AllfieldsList = (s.strip() for s in Allfields.split())
AssessmentFieldsList = (s.strip() for s in Assessment.split())
TaxonomyFieldList = (s.strip() for s in Taxonomy.split())
ThreatsFieldList = (s.strip() for s in Threats.split())

OurAssessmentFields = OrderedDict([
    ('TaxonID', 'internal_taxon_id'),
    ('RangeText', 'RangeDocumentation.narrative'),
    ('Population', 'PopulationDocumentation.narrative'),
    ('Habitat', 'HabitatDocumentation.narrative'),
    ('System', 'System.value'),
    ('Threats', 'ThreatsDocumentation.value'),
    ('Management', 'ConservationActionsDocumentation.narrative'),
    ('RLCategory', 'RedListCriteria.manualCategory'),
    ('RLCriteria', 'RedListCriteria.manualCriteria'),
    ('AssessmentVersion', 'RedlistCriteria.critVersion'),
    ('Assessment_date', 'RedListAssessmentDate.value'),
    # ('Assessors', 'RedListAssessors.text'),
    ('Assessment_text', 'RedListRationale.value'),
    ('Realm', 'BiogeographicRealm.realm'),
    ('PopulationTrend', 'PopulationTrend.value'),
    ('MapStatus', 'MapStatus.status'),
])
OurAllfields = OrderedDict([
    ('TaxonID', 'internal_taxon_id'),
    ('AOO', 'AOO.range',),
    ('EOO', 'EOO.range'),
    ('ElevFrom', 'ElevationLower.limit'),
    ('ElevTo', 'ElevationUpper.limit'),
    # ('GrowthForm', 'PlantGrowthForms.PlantGrowthFormsLookup'),
    ('Assessors', 'RedListAssessors.text')
])

OurTaxonomyFields = OrderedDict([
    ('TaxonID', 'internal_taxon_id'),
    ('kingdom', 'kingdom'),
    ('phylum', 'phylum'),
    ('classname', 'classname'),
    ('ordername', 'ordername'),
    ('family', 'family'),
    ('genus', 'genus'),
    ('species', 'species'),
    ('rank', 'infraType'),
    ('infraepi', 'infra_name'),
    ('author', 'authority'),
    ('infraauth', 'infra_authority')
])

OurCountryFields = OrderedDict([
    ("TaxonID", "internal_taxon_id"),
    ("Country", "CountryOccurrence.CountryOccurrenceSubfield.CountryOccurrenceLookup"),
    ("Extant", "CountryOccurrence.CountryOccurrenceSubfield.presence"),
    ("Native", "CountryOccurrence.CountryOccurrenceSubfield.origin"),
    ("Resident", "CountryOccurrence.CountryOccurrenceSubfield.seasonality")
])



def SIS_dump(taxonxml, faname):

    """
    :type taxonxml: etree.ElementTree.ElementTree
    """
    if not os.path.exists(faname):
        os.makedirs(faname)

    with open(faname + '\\allfields.csv', 'w', newline='', encoding="utf-8") as afcsv:
        afcsw = csv.DictWriter(afcsv, OurAllfields.values(), restval="")
        afcsw.writeheader()
        for tx in taxonxml.findall('Taxon'):
            allfdict = {}
            for fn in OurAllfields.keys():
                el = tx.find('.//' + fn)
                if el is not None:
                    allfdict[OurAllfields[fn]] = el.text
                    print(OurAllfields[fn], el.text)
            txid = tx.find('TaxonID')
            allfdict["internal_taxon_id"] = faname + ' ' + txid.text
            afcsw.writerow(allfdict)

    with open(faname + '\\assessments.csv', 'w', newline='', encoding="utf-8") as ascsv:
        ascsw = csv.DictWriter(ascsv, OurAssessmentFields.values(), restval="")
        ascsw.writeheader()
        for tx in taxonxml.findall('Taxon'):
            asdict = {}
            for fn in OurAssessmentFields.keys():
                el = tx.find('.//' + fn)
                if el is not None:
                    asdict[OurAssessmentFields[fn]] = el.text
                    print(OurAssessmentFields[fn], el.text)
            txid = tx.find('TaxonID')
            asdict["internal_taxon_id"] = faname + ' ' + txid.text
            asdict["RedlistCriteria.critVersion"] = '3.1'
            asdict['System.value'] = 'Terrestrial'
            asdict['MapStatus.status'] = 'Incomplete'
            asdict['RedListAssessmentDate.value'] = '03/01/2011'
            asdict['PopulationTrend.value'] = 'Unknown'
            ascsw.writerow(asdict)

    with open(faname + '\\taxonomy.csv', 'w', newline='', encoding="utf-8") as txcsv:
        txcsw = csv.DictWriter(txcsv, OurTaxonomyFields.values(), restval="")
        txcsw.writeheader()
        for tx in taxonxml.findall('Taxon'):
            txdict = {}
            for fn in OurTaxonomyFields.keys():
                el = tx.find('.//' + fn)
                if el is not None:
                    txdict[OurTaxonomyFields[fn]] = el.text
                    print(OurTaxonomyFields[fn], el.text)
            txid = tx.find('TaxonID')
            txdict["internal_taxon_id"] = faname + ' ' + txid.text
            txdict.update(tx_upper_levels[txdict['family'].upper()])
            txcsw.writerow(txdict)

    with open(faname + '\\countries.csv', 'w', newline='') as cntrycsv:
        cntrycsw = csv.DictWriter(cntrycsv, OurCountryFields.values(), restval="")
        cntrycsw.writeheader()
        for tx in taxonxml.findall('Taxon'):
            cntrydict = {}
            txid = tx.find('TaxonID')
            cntrydict["internal_taxon_id"] = faname + ' ' + txid.text
            for cntry in tx.findall('.//Country'):
                cntrydict["CountryOccurrence.CountryOccurrenceSubfield.CountryOccurrenceLookup"] = cntry.text
                cntrydict["CountryOccurrence.CountryOccurrenceSubfield.presence"] = 'Extant'
                cntrydict["CountryOccurrence.CountryOccurrenceSubfield.origin"] = 'Native'
                cntrydict["CountryOccurrence.CountryOccurrenceSubfield.seasonality"] = 'Resident'
                cntrycsw.writerow(cntrydict)

    with open(faname + '\\credits.csv', 'w', newline='') as creditscsv:
        creditscsw = csv.DictWriter(creditscsv, CreditsFieldList, restval="")
        creditscsw.writeheader()
        for tx in taxonxml.findall('Taxon'):
            creditsdict = {}
            txid = tx.find('TaxonID')
            creditsdict["internal_taxon_id"] = faname + ' ' + txid.text
            creditsdict.update(MartinCheek)
            creditscsw.writerow(creditsdict)
            creditsdict.update(JMOnana)
            creditscsw.writerow(creditsdict)

    with open(faname + '\\references.csv', 'w', newline='') as filecsv:
        filecsw = csv.DictWriter(filecsv, ReferencesRB.keys(), restval="")
        filecsw.writeheader()
        for tx in taxonxml.findall('Taxon'):
            referencesdict = {}
            txid = tx.find('TaxonID')
            referencesdict.update(ReferencesRB)
            referencesdict["internal_taxon_id"] = faname + ' ' + txid.text
            filecsw.writerow(referencesdict)

    pass

