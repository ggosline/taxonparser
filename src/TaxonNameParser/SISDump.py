from collections import OrderedDict

__author__ = 'gg12kg'

import csv
from lxml import etree
import os

Allfields = r"Internal_taxon_id	LocationsNumber.range	MapStatus.status	BiogeographicRealm.realm	System.value	" \
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

Taxonomy = r"Internal_taxon_id	Kingdom	Phylum	Class	Order	Family	Genus	Species	Authority	Infra_rank	Infra_name	infra_authority	TaxonomicNotes.value"

Threats = r"Internal_taxon_id	Threats.ThreatsLookup	Threats.timing	Threats.scope	Threats.severity	Threats.stress"

ConservationNeededFieldList = ("Internal_taxon_id",
                               "ConservationActions.ConservationActionsLookup", "ConservationActions.Note")

HabitatsFieldList = ("Internal_taxon_id",
                     "GeneralHabitats.GeneralHabitatsLookup", "GeneralHabitats.suitability",
                     "GeneralHabitats.majorImportance")

CountryFieldList = ("Internal_taxon_id","CountryOccurrence.CountryOccurrenceLookup","CountryOccurrence.presence","CountryOccurrence.origin","CountryOccurrence.seasonality")

AllfieldsList = (s.strip() for s in Allfields.split())
TaxonomyFieldList = (s.strip() for s in Taxonomy.split())
ThreatsFieldList = (s.strip() for s in Threats.split())

OurAllfields = OrderedDict([
    ('TaxonID', 'Internal_taxon_id',),
    ('RangeText', 'RangeDocumentation.narrative'),
    ('AOO', 'AOO.range',),
    ('EOO', 'EOO.range'),
    ('ElevFrom', 'ElevationLower.limit'),
    ('ElevTo', 'ElevationUpper.limit'),
    ('Population', 'PopulationDocumentation.narrative'),
    ('Habitat', 'HabitatDocumentation.narrative'),
    ('System', 'System.value'),
    ('GrowthForm', 'PlantGrowthForms.PlantGrowthFormsLookup'),
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

OurTaxonomyFields = OrderedDict([
    ('TaxonID', 'Internal_taxon_id'),
    ('family', 'family'),
    ('genus', 'genus'),
    ('species', 'species'),
    ('rank', 'infra_rank'),
    ('infraepi', 'infra_name'),
    ('author', 'authority'),
    ('infraauth', 'infra_authority')
])

OurCountryFields = OrderedDict([
    ("TaxonID","Internal_taxon_id"),
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
            cntrydict["Internal_taxon_id"] = txid.text
            for cntry in tx.findall('.//Country'):
                cntrydict["CountryOccurrence.CountryOccurrenceLookup"] = cntry.text
                cntrydict["CountryOccurrence.presence"] = 'Extant'
                cntrydict["CountryOccurrence.origin"] = 'Native'
                cntrydict["CountryOccurrence.seasonality"] = 'Resident'
                cntrycsw.writerow(cntrydict)

    pass

