import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models

from care.emr.models import EMRBaseModel
from care.emr.models.organization import FacilityOrganization, Organization


class Questionnaire(EMRBaseModel):
    version = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, default=uuid.uuid4, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(default="")
    subject_type = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    styling_metadata = models.JSONField(default=dict)
    questions = models.JSONField(default=dict)
    organization_cache = ArrayField(models.IntegerField(), default=list)
    internal_organization_cache = ArrayField(models.IntegerField(), default=list)


class QuestionnaireResponse(EMRBaseModel):
    questionnaire = models.ForeignKey(
        Questionnaire, on_delete=models.CASCADE, null=True, blank=True
    )
    subject_id = models.UUIDField()
    responses = models.JSONField(default=list)
    structured_responses = models.JSONField(default=dict)
    structured_response_type = models.CharField(default=None, blank=True, null=True)
    patient = models.ForeignKey("emr.Patient", on_delete=models.CASCADE)
    encounter = models.ForeignKey(
        "emr.Encounter", on_delete=models.CASCADE, null=True, blank=True
    )

    # TODO : Add index for subject_id and subject_type in descending order


class QuestionnaireOrganization(EMRBaseModel):
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    # TODO Add instance level roles, ie roles would be added here

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.sync_questionnaire_cache()

    def sync_questionnaire_cache(self):
        questionnaire_organization_objects = QuestionnaireOrganization.objects.filter(
            questionnaire=self.questionnaire
        )
        cache = []
        for questionnaire_organization in questionnaire_organization_objects:
            cache.extend(questionnaire_organization.organization.parent_cache)
            cache.append(questionnaire_organization.organization.id)
        cache = list(set(cache))
        self.questionnaire.organization_cache = cache
        self.questionnaire.save(update_fields=["organization_cache"])


class QuestionnaireFacilityOrganization(EMRBaseModel):
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    organization = models.ForeignKey(FacilityOrganization, on_delete=models.CASCADE)
    # TODO Add instance level roles, ie roles would be added here

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.sync_questionnaire_cache()

    def sync_questionnaire_cache(self):
        questionnaire_organization_objects = (
            QuestionnaireFacilityOrganization.objects.filter(
                questionnaire=self.questionnaire
            )
        )
        cache = []
        for questionnaire_organization in questionnaire_organization_objects:
            cache.extend(questionnaire_organization.organization.parent_cache)
            cache.append(questionnaire_organization.organization.id)
        cache = list(set(cache))
        self.questionnaire.internal_organization_cache = cache
        self.questionnaire.save(update_fields=["internal_organization_cache"])
