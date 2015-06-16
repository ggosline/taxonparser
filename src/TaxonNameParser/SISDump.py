from collections import OrderedDict

__author__ = 'gg12kg'

import csv
from lxml import etree
import os

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
                    "CountryOccurrence..CountryOccurrenceSubfield.presence",
                    "CountryOccurrence..CountryOccurrenceSubfield.origin")


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
    ('AssessmentVersion', 'RedListCriteriaVersion.criteriaVersion'),
    ('Assessment_date', 'RedListAssessmentDate.value'),
    ('Assessors', 'RedListAssessors.text'),
    ('Assessment_text', 'RedListRationale.value'),
    ('Realm', 'BiogeographicRealm.realm')
])
OurAllfields = OrderedDict([
    ('TaxonID', 'internal_taxon_id'),
    ('AOO', 'AOO.range',),
    ('EOO', 'EOO.range'),
    ('ElevFrom', 'ElevationLower.limit'),
    ('ElevTo', 'ElevationUpper.limit'),
    ('GrowthForm', 'PlantGrowthForms.PlantGrowthFormsLookup'),
    ('AssessmentVersion', 'RedListCriteriaVersion.criteriaVersion'),
    ('Assessors', 'RedListAssessors.text')
])

OurTaxonomyFields = OrderedDict([
    ('TaxonID', 'internal_taxon_id'),
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
    ("Country","CountryOccurrence.CountryOccurrenceLookup"),
    ("Extant","CountryOccurrence.presence"),
    ("Native","CountryOccurrence.origin"),
    ("Resident","CountryOccurrence.seasonality")
])


def SIS_dump(taxonxml, faname):

    """
    :type taxonxml: etree.ElementTree.ElementTree
    """
    if not os.path.exists(faname):
        os.makedirs(faname)

    with open(faname + '\\Allfields.csv', 'w', newline='', encoding="utf-8") as afcsv:
        awcsw = csv.DictWriter(afcsv, OurAllfields.values(), restval="")
        awcsw.writeheader()
        for tx in taxonxml.findall('Taxon'):
            allfdict = {}
            for fn in OurAllfields.keys():
                el = tx.find('.//' + fn)
                if el is not None:
                    allfdict[OurAllfields[fn]] = el.text
                    print(OurAllfields[fn], el.text)
            awcsw.writerow(allfdict)

    with open(faname + '\\Assessment.csv', 'w', newline='', encoding="utf-8") as txcsv:
        txcsw = csv.DictWriter(txcsv, OurAssessmentFields.values(), restval="")
        txcsw.writeheader()
        for tx in taxonxml.findall('Taxon'):
            txdict = {}
            for fn in OurAssessmentFields.keys():
                el = tx.find('.//' + fn)
                if el is not None:
                    txdict[OurAssessmentFields[fn]] = el.text
                    print(OurAssessmentFields[fn], el.text)
            txdict['System.value'] = 'Terrestrial'
            txcsw.writerow(txdict)

    with open(faname + '\\Taxonomy.csv','w', newline='', encoding="utf-8") as txcsv:
        txcsw = csv.DictWriter(txcsv, OurTaxonomyFields.values(), restval="")
        txcsw.writeheader()
        for tx in taxonxml.findall('Taxon'):
            txdict = {}
            for fn in OurTaxonomyFields.keys():
                el = tx.find('.//' + fn)
                if el is not None:
                    txdict[OurTaxonomyFields[fn]] = el.text
                    print(OurTaxonomyFields[fn], el.text)
            txcsw.writerow(txdict)

    with open(faname + '\\Countries.csv','w', newline='') as cntrycsv:
        cntrycsw = csv.DictWriter(cntrycsv, OurCountryFields.values(), restval="")
        cntrycsw.writeheader()
        for tx in taxonxml.findall('Taxon'):
            cntrydict = {}
            txid = tx.find('TaxonID')
            cntrydict["internal_taxon_id"] = txid.text
            for cntry in tx.findall('.//Country'):
                cntrydict["CountryOccurrence.CountryOccurrenceLookup"] = cntry.text
                cntrydict["CountryOccurrence.presence"] = 'Extant'
                cntrydict["CountryOccurrence.origin"] = 'Native'
                cntrydict["CountryOccurrence.seasonality"] = 'Resident'
                cntrycsw.writerow(cntrydict)

    pass

