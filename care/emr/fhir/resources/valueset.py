from pydantic.main import BaseModel

from care.emr.fhir.resources.base import ResourceManger
from care.emr.fhir.resources.code_concept import MinimalCodeConcept
from care.emr.fhir.schema.base import Coding
from care.emr.fhir.schema.valueset.valueset import ValueSetInclude


class ValueSetFilterValidation(BaseModel):
    include: list[ValueSetInclude] = None
    exclude: list[ValueSetInclude] = None
    search: str = None
    count: int = None


class ValueSetResource(ResourceManger):
    allowed_properties = ["include", "exclude", "search", "count"]

    def serialize(self, result):
        return MinimalCodeConcept(
            system=result["system"], code=result["code"], display=result["display"]
        )

    def validate_filter(self):
        ValueSetFilterValidation(**self._filters)

    def lookup(self, code: Coding):
        parameters = [
            {
                "name": "valueSet",
                "resource": {
                    "resourceType": "ValueSet",
                    "compose": {
                        "include": self._filters.get("include", []),
                        "exclude": self._filters.get("exclude", []),
                    },
                },
            },
            {"name": "coding", "valueCoding": code.model_dump(exclude_defaults=True)},
        ]
        request_json = {"resourceType": "Parameters", "parameter": parameters}
        full_result = self.query("POST", "ValueSet/$validate-code", request_json)
        try:
            results = full_result["parameter"]
            for result in results:
                if result["name"] == "result":
                    return result["valueBoolean"]
        except Exception as e:
            err = "Unknown Value Returned from Terminology Server"
            raise Exception(err) from e

    def search(self):
        parameters = []
        for key in self._filters:
            if key == "search" and self._filters[key]:
                parameters.append({"name": "filter", "valueString": self._filters[key]})
            if key == "count":
                parameters.append({"name": "count", "valueInteger": self._filters[key]})
        parameters.append(
            {
                "name": "valueSet",
                "resource": {
                    "resourceType": "ValueSet",
                    "compose": {
                        "include": self._filters.get("include", []),
                        "exclude": self._filters.get("exclude", []),
                    },
                },
            }
        )
        request_json = {"resourceType": "Parameters", "parameter": parameters}
        full_result = self.query("POST", "ValueSet/$expand", request_json)
        # TODO Add Exception Handling
        if "expansion" not in full_result:
            return []
        results = full_result["expansion"]
        if "contains" not in results:
            return []
        return self.handle_list(results["contains"])
