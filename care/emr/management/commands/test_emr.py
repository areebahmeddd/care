# ruff : noqa : T201 F841

from django.core.management.base import BaseCommand

from care.emr.fhir.resources.code_concept import CodeConceptResource
from care.emr.fhir.resources.code_system import CodeSystemResource
from care.emr.fhir.resources.valueset import ValueSetResource
from care.emr.resources.allergy_intolerance.valueset import CARE_ALLERGY_CODE_VALUESET


class Command(BaseCommand):
    """ """

    help = ""

    def handle(self, *args, **options):
        code_system = CodeSystemResource().filter(url="http://loinc.org").get()
        code_concept = (
            CodeConceptResource().filter(system=code_system.url, code="8302-2").get()
        )
        valueset = (
            ValueSetResource()
            .filter(
                search="Pressure",
                count=2,
                include=[{"system": code_system.url, "filter": []}],
            )
            .search()
        )
        print(CARE_ALLERGY_CODE_VALUESET.composition)
        for i in CARE_ALLERGY_CODE_VALUESET.search("nut"):
            print(i)
