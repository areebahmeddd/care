# ruff: noqa: F403 N815 F405 ERA001 - Naming convention is disabled for this file because it needs to match the FHIR schema
# Partly generated from fhir.schema.json R5 on 2024-11-09

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, constr

from care.emr.fhir.schema.base import *


class ValueSet(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )

    # id: Id | None = Field(
    #     None,
    #     description="The logical id of the resource, as used in the URL for the resource. Once assigned, this value never changes.",
    # )
    meta: Meta | None = Field(
        None,
        description="The metadata about the resource. This is content that is maintained by the infrastructure. Changes to the content might not always be associated with version changes to the resource.",
    )
    implicitRules: Uri | None = Field(
        None,
        description="A reference to a set of rules that were followed when the resource was constructed, and which must be understood when processing the content. Often, this is a reference to an implementation guide that defines the special rules along with other profiles etc.",
    )
    # field_implicitRules: Element | None = Field(
    #     None, alias="_implicitRules", description="Extensions for implicitRules"
    # )
    language: Code | None = Field(
        None, description="The base language in which the resource is written."
    )
    # field_language: Element | None = Field(
    #     None, alias="_language", description="Extensions for language"
    # )
    text: Narrative | None = Field(
        None,
        description='A human-readable narrative that contains a summary of the resource and can be used to represent the content of the resource to a human. The narrative need not encode all the structured data, but is required to contain sufficient detail to make it "clinically safe" for a human to just read the narrative. Resource definitions may define what content should be represented in the narrative to ensure clinical safety.',
    )
    # contained: list[ResourceList] | None = Field(
    #     None,
    #     description="These resources do not have an independent existence apart from the resource that contains them - they cannot be identified independently, nor can they have their own independent transaction scope. This is allowed to be a Parameters resource if and only if it is referenced by a resource that provides context/meaning.",
    # )
    extension: list[Extension] | None = Field(
        None,
        description="May be used to represent additional information that is not part of the basic definition of the resource. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifierExtension: list[Extension] | None = Field(
        None,
        description="May be used to represent additional information that is not part of the basic definition of the resource and that modifies the understanding of the element that contains it and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer is allowed to define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions.\n\nModifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    url: Uri | None = Field(
        None,
        description="An absolute URI that is used to identify this value set when it is referenced in a specification, model, design or an instance; also called its canonical identifier. This SHOULD be globally unique and SHOULD be a literal address at which an authoritative instance of this value set is (or will be) published. This URL can be the target of a canonical reference. It SHALL remain the same when the value set is stored on different servers.",
    )
    # field_url: Element | None = Field(
    #     None, alias="_url", description="Extensions for url"
    # )
    identifier: list[Identifier] | None = Field(
        None,
        description="A formal identifier that is used to identify this value set when it is represented in other formats, or referenced in a specification, model, design or an instance.",
    )
    version: String | None = Field(
        None,
        description="The identifier that is used to identify this version of the value set when it is referenced in a specification, model, design or instance. This is an arbitrary value managed by the value set author and is not expected to be globally unique. For example, it might be a timestamp (e.g. yyyymmdd) if a managed version is not available. There is also no expectation that versions can be placed in a lexicographical sequence.",
    )
    # field_version: Element | None = Field(
    #     None, alias="_version", description="Extensions for version"
    # )
    versionAlgorithmString: constr(pattern="^^[\\s\\S]+$$") | None = Field(
        None,
        description="Indicates the mechanism used to compare versions to determine which ValueSet is more current.",
    )
    # field_versionAlgorithmString: Element | None = Field(
    #     None,
    #     alias="_versionAlgorithmString",
    #     description="Extensions for versionAlgorithmString",
    # )
    versionAlgorithmCoding: Coding | None = Field(
        None,
        description="Indicates the mechanism used to compare versions to determine which ValueSet is more current.",
    )
    name: String = Field(
        ...,
        description="A natural language name identifying the value set. This name should be usable as an identifier for the module by machine processing applications such as code generation.",
    )
    # field_name: Element | None = Field(
    #     None, alias="_name", description="Extensions for name"
    # )
    title: String | None = Field(
        None, description="A short, descriptive, user-friendly title for the value set."
    )
    # field_title: Element | None = Field(
    #     None, alias="_title", description="Extensions for title"
    # )
    status: Code | None = Field(
        None,
        description="The status of this value set. Enables tracking the life-cycle of the content. The status of the value set applies to the value set definition (ValueSet.compose) and the associated ValueSet metadata. Expansions do not have a state.",
    )
    # field_status: Element | None = Field(
    #     None, alias="_status", description="Extensions for status"
    # )
    experimental: Boolean | None = Field(
        None,
        description="A Boolean value to indicate that this value set is authored for testing purposes (or education/evaluation/marketing) and is not intended to be used for genuine usage.",
    )
    # field_experimental: Element | None = Field(
    #     None, alias="_experimental", description="Extensions for experimental"
    # )
    date: DateTime | None = Field(
        None,
        description="The date (and optionally time) when the value set metadata or content logical definition (.compose) was created or revised.",
    )
    # field_date: Element | None = Field(
    #     None, alias="_date", description="Extensions for date"
    # )
    publisher: String | None = Field(
        None,
        description="The name of the organization or individual responsible for the release and ongoing maintenance of the value set.",
    )
    # field_publisher: Element | None = Field(
    #     None, alias="_publisher", description="Extensions for publisher"
    # )
    contact: list[ContactDetail] | None = Field(
        None,
        description="Contact details to assist a user in finding and communicating with the publisher.",
    )
    description: String = Field(
        ...,
        description="A free text natural language description of the value set from a consumer's perspective. The textual description specifies the span of meanings for concepts to be included within the Value Set Expansion, and also may specify the intended use and limitations of the Value Set.",
    )
    # field_description: Element | None = Field(
    #     None, alias="_description", description="Extensions for description"
    # )
    useContext: list[UsageContext] | None = Field(
        None,
        description="The content was developed with a focus and intent of supporting the contexts that are listed. These contexts may be general categories (gender, age, ...) or may be references to specific programs (insurance plans, studies, ...) and may be used to assist with indexing and searching for appropriate value set instances.",
    )
    jurisdiction: list[CodeableConcept] | None = Field(
        None,
        description="A legal or geographic region in which the value set is intended to be used.",
    )
    purpose: Markdown | None = Field(
        None,
        description="Explanation of why this value set is needed and why it has been designed as it has.",
    )
    # field_purpose: Element | None = Field(
    #     None, alias="_purpose", description="Extensions for purpose"
    # )
    copyright: Markdown | None = Field(
        None,
        description="A copyright statement relating to the value set and/or its contents. Copyright statements are generally legal restrictions on the use and publishing of the value set.",
    )
    # field_copyright: Element | None = Field(
    #     None, alias="_copyright", description="Extensions for copyright"
    # )
    copyrightLabel: String | None = Field(
        None,
        description="A short string (<50 characters), suitable for inclusion in a page footer that identifies the copyright holder, effective period, and optionally whether rights are resctricted. (e.g. 'All rights reserved', 'Some rights reserved').",
    )
    # field_copyrightLabel: Element | None = Field(
    #     None, alias="_copyrightLabel", description="Extensions for copyrightLabel"
    # )
    approvalDate: Date | None = Field(
        None,
        description="The date on which the resource content was approved by the publisher. Approval happens once when the content is officially approved for usage.",
    )
    # field_approvalDate: Element | None = Field(
    #     None, alias="_approvalDate", description="Extensions for approvalDate"
    # )
    lastReviewDate: Date | None = Field(
        None,
        description="The date on which the resource content was last reviewed. Review happens periodically after approval but does not change the original approval date.",
    )
    # field_lastReviewDate: Element | None = Field(
    #     None, alias="_lastReviewDate", description="Extensions for lastReviewDate"
    # )
    effectivePeriod: Period | None = Field(
        None,
        description="The period during which the ValueSet content was or is planned to be in active use.",
    )
    topic: list[CodeableConcept] | None = Field(
        None,
        description="Descriptions related to the content of the ValueSet. Topics provide a high-level categorization as well as keywords for the ValueSet that can be useful for filtering and searching.",
    )
    author: list[ContactDetail] | None = Field(
        None,
        description="An individiual or organization primarily involved in the creation and maintenance of the ValueSet.",
    )
    editor: list[ContactDetail] | None = Field(
        None,
        description="An individual or organization primarily responsible for internal coherence of the ValueSet.",
    )
    reviewer: list[ContactDetail] | None = Field(
        None,
        description="An individual or organization asserted by the publisher to be primarily responsible for review of some aspect of the ValueSet.",
    )
    endorser: list[ContactDetail] | None = Field(
        None,
        description="An individual or organization asserted by the publisher to be responsible for officially endorsing the ValueSet for use in some setting.",
    )
    # relatedArtifact: list[RelatedArtifact] | None = Field(
    #     None,
    #     description="Related artifacts such as additional documentation, justification, dependencies, bibliographic references, and predecessor and successor artifacts.",
    # )
    immutable: Boolean | None = Field(
        None,
        description="If this is set to 'true', then no new versions of the content logical definition can be created.  Note: Other metadata might still change.",
    )
    # field_immutable: Element | None = Field(
    #     None, alias="_immutable", description="Extensions for immutable"
    # )
    compose: ValueSetCompose = Field(
        ...,
        description="A set of criteria that define the contents of the value set by including or excluding codes selected from the specified code system(s) that the value set draws from. This is also known as the Content Logical Definition (CLD).",
    )
    expansion: ValueSetExpansion | None = Field(
        None,
        description='A value set can also be "expanded", where the value set is turned into a simple collection of enumerated codes. This element holds the expansion, if it has been performed.',
    )
    scope: ValueSetScope | None = Field(
        None,
        description="Description of the semantic space the Value Set Expansion is intended to cover and should further clarify the text in ValueSet.description.",
    )


class ValueSetCompose(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    id: String | None = Field(
        None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: list[Extension] | None = Field(
        None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifierExtension: list[Extension] | None = Field(
        None,
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions.\n\nModifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    lockedDate: Date | None = Field(
        None,
        description="The Locked Date is  the effective date that is used to determine the version of all referenced Code Systems and Value Set Definitions included in the compose that are not already tied to a specific version.",
    )
    # field_lockedDate: Element | None = Field(
    #     None, alias="_lockedDate", description="Extensions for lockedDate"
    # )
    inactive: Boolean | None = Field(
        None,
        description="Whether inactive codes - codes that are not approved for current use - are in the value set. If inactive = true, inactive codes are to be included in the expansion, if inactive = false, the inactive codes will not be included in the expansion. If absent, the behavior is determined by the implementation, or by the applicable $expand parameters (but generally, inactive codes would be expected to be included).",
    )
    # field_inactive: Element | None = Field(
    #     None, alias="_inactive", description="Extensions for inactive"
    # )
    include: list[ValueSetInclude] = Field(
        ...,
        description="Include one or more codes from a code system or other value set(s).",
    )
    exclude: list[ValueSetInclude] | None = Field(
        None,
        description="Exclude one or more codes from the value set based on code system filters and/or other value sets.",
    )
    property: list[String] | None = Field(
        None,
        description="A property to return in the expansion, if the client doesn't ask for any particular properties. May be either a code from the code system definition (convenient) or a the formal URI that refers to the property. The special value '*' means all properties known to the server.",
    )
    # field_property: list[Element] | None = Field(
    #     None, alias="_property", description="Extensions for property"
    # )


class ValueSetInclude(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    id: String | None = Field(
        None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: list[Extension] | None = Field(
        None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifierExtension: list[Extension] | None = Field(
        None,
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions.\n\nModifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    system: Uri | None = Field(
        None,
        description="An absolute URI which is the code system from which the selected codes come from.",
    )
    # field_system: Element | None = Field(
    #     None, alias="_system", description="Extensions for system"
    # )
    version: String | None = Field(
        None,
        description="The version of the code system that the codes are selected from, or the special version '*' for all versions.",
    )
    # field_version: Element | None = Field(
    #     None, alias="_version", description="Extensions for version"
    # )
    concept: list[ValueSetConcept] | None = Field(
        None, description="Specifies a concept to be included or excluded."
    )
    filter: list[ValueSetFilter] | None = Field(
        None,
        description="Select concepts by specifying a matching criterion based on the properties (including relationships) defined by the system, or on filters defined by the system. If multiple filters are specified within the include, they SHALL all be true.",
    )
    valueSet: list[Canonical] | None = Field(
        None,
        description="Selects the concepts found in this value set (based on its value set definition). This is an absolute URI that is a reference to ValueSet.url.  If multiple value sets are specified this includes the intersection of the contents of all of the referenced value sets.",
    )
    copyright: String | None = Field(
        None,
        description="A copyright statement for the specific code system asserted by the containing ValueSet.compose.include element's system value (if the associated ValueSet.compose.include.version element is not present); or the code system and version combination (if the associated ValueSet.compose.include.version element is present).",
    )
    # field_copyright: Element | None = Field(
    #     None, alias="_copyright", description="Extensions for copyright"
    # )


class ValueSetConcept(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    id: String | None = Field(
        None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: list[Extension] | None = Field(
        None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifierExtension: list[Extension] | None = Field(
        None,
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions.\n\nModifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    code: Code | None = Field(
        None, description="Specifies a code for the concept to be included or excluded."
    )
    # field_code: Element | None = Field(
    #     None, alias="_code", description="Extensions for code"
    # )
    display: String | None = Field(
        None,
        description="The text to display to the user for this concept in the context of this valueset. If no display is provided, then applications using the value set use the display specified for the code by the system.",
    )
    # field_display: Element | None = Field(
    #     None, alias="_display", description="Extensions for display"
    # )
    designation: list[ValueSetDesignation] | None = Field(
        None,
        description="Additional representations for this concept when used in this value set - other languages, aliases, specialized purposes, used for particular purposes, etc.",
    )


class ValueSetDesignation(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    id: String | None = Field(
        None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: list[Extension] | None = Field(
        None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifierExtension: list[Extension] | None = Field(
        None,
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions.\n\nModifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    language: Code | None = Field(
        None, description="The language this designation is defined for."
    )
    # field_language: Element | None = Field(
    #     None, alias="_language", description="Extensions for language"
    # )
    use: Coding | None = Field(
        None, description="A code that represents types of uses of designations."
    )
    additionalUse: list[Coding] | None = Field(
        None,
        description="Additional codes that detail how this designation would be used, if there is more than one use.",
    )
    value: String | None = Field(
        None, description="The text value for this designation."
    )
    # field_value: Element | None = Field(
    #     None, alias="_value", description="Extensions for value"
    # )


class ValueSetFilter(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    id: String | None = Field(
        None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: list[Extension] | None = Field(
        None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifierExtension: list[Extension] | None = Field(
        None,
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions.\n\nModifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    property: Code | None = Field(
        None,
        description="A code that identifies a property or a filter defined in the code system.",
    )
    # field_property: Element | None = Field(
    #     None, alias="_property", description="Extensions for property"
    # )
    op: Code | None = Field(
        None,
        description="The kind of operation to perform as a part of the filter criteria.",
    )
    # field_op: Element | None = Field(None, alias="_op", description="Extensions for op")
    value: String | None = Field(
        None,
        description="The match value may be either a code defined by the system, or a string value, which is a regex match on the literal string of the property value  (if the filter represents a property defined in CodeSystem) or of the system filter value (if the filter represents a filter defined in CodeSystem) when the operation is 'regex', or one of the values (true and false), when the operation is 'exists'.",
    )
    # field_value: Element | None = Field(
    #     None, alias="_value", description="Extensions for value"
    # )


class ValueSetExpansion(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    id: String | None = Field(
        None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: list[Extension] | None = Field(
        None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifierExtension: list[Extension] | None = Field(
        None,
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions.\n\nModifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    identifier: Uri | None = Field(
        None,
        description="An identifier that uniquely identifies this expansion of the valueset, based on a unique combination of the provided parameters, the system default parameters, and the underlying system code system versions etc. Systems may re-use the same identifier as long as those factors remain the same, and the expansion is the same, but are not required to do so. This is a business identifier.",
    )
    # field_identifier: Element | None = Field(
    #     None, alias="_identifier", description="Extensions for identifier"
    # )
    next: Uri | None = Field(
        None,
        description="As per paging Search results, the next URLs are opaque to the client, have no dictated structure, and only the server understands them.",
    )
    # field_next: Element | None = Field(
    #     None, alias="_next", description="Extensions for next"
    # )
    timestamp: DateTime | None = Field(
        None,
        description="The time at which the expansion was produced by the expanding system.",
    )
    # field_timestamp: Element | None = Field(
    #     None, alias="_timestamp", description="Extensions for timestamp"
    # )
    total: Integer | None = Field(
        None,
        description="The total number of concepts in the expansion. If the number of concept nodes in this resource is less than the stated number, then the server can return more using the offset parameter.",
    )
    # field_total: Element | None = Field(
    #     None, alias="_total", description="Extensions for total"
    # )
    offset: Integer | None = Field(
        None,
        description="If paging is being used, the offset at which this resource starts.  I.e. this resource is a partial view into the expansion. If paging is not being used, this element SHALL NOT be present.",
    )
    # field_offset: Element | None = Field(
    #     None, alias="_offset", description="Extensions for offset"
    # )
    parameter: list[ValueSetParameter] | None = Field(
        None,
        description="A parameter that controlled the expansion process. These parameters may be used by users of expanded value sets to check whether the expansion is suitable for a particular purpose, or to pick the correct expansion.",
    )
    property: list[ValueSetProperty] | None = Field(
        None,
        description="A property defines an additional slot through which additional information can be provided about a concept.",
    )
    contains: list[ValueSetContains] | None = Field(
        None, description="The codes that are contained in the value set expansion."
    )


class ValueSetParameter(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    id: String | None = Field(
        None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: list[Extension] | None = Field(
        None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifierExtension: list[Extension] | None = Field(
        None,
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions.\n\nModifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    name: String | None = Field(
        None,
        description="Name of the input parameter to the $expand operation; may be a server-assigned name for additional default or other server-supplied parameters used to control the expansion process.",
    )
    # field_name: Element | None = Field(
    #     None, alias="_name", description="Extensions for name"
    # )
    valueString: constr(pattern="^^[\\s\\S]+$$") | None = Field(
        None, description="The value of the parameter."
    )
    field_valueString: Element | None = Field(
        None, alias="_valueString", description="Extensions for valueString"
    )
    valueBoolean: bool | None = Field(None, description="The value of the parameter.")
    # field_valueBoolean: Element | None = Field(
    #     None, alias="_valueBoolean", description="Extensions for valueBoolean"
    # )
    valueInteger: float | None = Field(None, description="The value of the parameter.")
    # field_valueInteger: Element | None = Field(
    #     None, alias="_valueInteger", description="Extensions for valueInteger"
    # )
    valueDecimal: float | None = Field(None, description="The value of the parameter.")
    # field_valueDecimal: Element | None = Field(
    #     None, alias="_valueDecimal", description="Extensions for valueDecimal"
    # )
    valueUri: constr(pattern="^\\S*$") | None = Field(
        None, description="The value of the parameter."
    )
    # field_valueUri: Element | None = Field(
    #     None, alias="_valueUri", description="Extensions for valueUri"
    # )
    valueCode: constr(pattern="^[^\\s]+( [^\\s]+)*$") | None = Field(
        None, description="The value of the parameter."
    )
    # field_valueCode: Element | None = Field(
    #     None, alias="_valueCode", description="Extensions for valueCode"
    # )
    valueDateTime: (
        constr(
            pattern="^([0-9]([0-9]([0-9][1-9]|[1-9]0)|[1-9]00)|[1-9]000)(-(0[1-9]|1[0-2])(-(0[1-9]|[1-2][0-9]|3[0-1])(T([01][0-9]|2[0-3]):[0-5][0-9]:([0-5][0-9]|60)(\\.[0-9]{1,9})?)?)?(Z|(\\+|-)((0[0-9]|1[0-3]):[0-5][0-9]|14:00)?)?)?$"
        )
        | None
    ) = Field(None, description="The value of the parameter.")
    # field_valueDateTime: Element | None = Field(
    #     None, alias="_valueDateTime", description="Extensions for valueDateTime"
    # )


class ValueSetProperty(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    id: String | None = Field(
        None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: list[Extension] | None = Field(
        None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifierExtension: list[Extension] | None = Field(
        None,
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions.\n\nModifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    code: Code | None = Field(
        None,
        description="A code that is used to identify the property. The code is used in ValueSet.expansion.contains.property.code.",
    )
    # field_code: Element | None = Field(
    #     None, alias="_code", description="Extensions for code"
    # )
    uri: Uri | None = Field(
        None,
        description="Reference to the formal meaning of the property. One possible source of meaning is the [Concept Properties](codesystem-concept-properties.html) code system.",
    )
    # field_uri: Element | None = Field(
    #     None, alias="_uri", description="Extensions for uri"
    # )


class ValueSetContains(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    id: String | None = Field(
        None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: list[Extension] | None = Field(
        None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifierExtension: list[Extension] | None = Field(
        None,
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions.\n\nModifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    system: Uri | None = Field(
        None,
        description="An absolute URI which is the code system in which the code for this item in the expansion is defined.",
    )
    # field_system: Element | None = Field(
    #     None, alias="_system", description="Extensions for system"
    # )
    abstract: Boolean | None = Field(
        None,
        description="If true, this entry is included in the expansion for navigational purposes, and the user cannot select the code directly as a proper value.",
    )
    # field_abstract: Element | None = Field(
    #     None, alias="_abstract", description="Extensions for abstract"
    # )
    inactive: Boolean | None = Field(
        None,
        description="If the concept is inactive in the code system that defines it. Inactive codes are those that are no longer to be used, but are maintained by the code system for understanding legacy data. It might not be known or specified whether a concept is inactive (and it may depend on the context of use).",
    )
    # field_inactive: Element | None = Field(
    #     None, alias="_inactive", description="Extensions for inactive"
    # )
    version: String | None = Field(
        None,
        description="The version of the code system from this code was taken. Note that a well-maintained code system does not need the version reported, because the meaning of codes is consistent across versions. However this cannot consistently be assured, and when the meaning is not guaranteed to be consistent, the version SHOULD be exchanged.",
    )
    # field_version: Element | None = Field(
    #     None, alias="_version", description="Extensions for version"
    # )
    code: Code | None = Field(
        None,
        description="The code for this item in the expansion hierarchy. If this code is missing the entry in the hierarchy is a place holder (abstract) and does not represent a valid code in the value set.",
    )
    # field_code: Element | None = Field(
    #     None, alias="_code", description="Extensions for code"
    # )
    display: String | None = Field(
        None, description="The recommended display for this item in the expansion."
    )
    # field_display: Element | None = Field(
    #     None, alias="_display", description="Extensions for display"
    # )
    designation: list[ValueSetDesignation] | None = Field(
        None,
        description="Additional representations for this item - other languages, aliases, specialized purposes, used for particular purposes, etc. These are relevant when the conditions of the expansion do not fix to a single correct representation.",
    )
    property: list[ValueSetProperty1] | None = Field(
        None, description="A property value for this concept."
    )
    contains: list[ValueSetContains] | None = Field(
        None,
        description="Other codes and entries contained under this entry in the hierarchy.",
    )


class ValueSetProperty1(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    id: String | None = Field(
        None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: list[Extension] | None = Field(
        None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifierExtension: list[Extension] | None = Field(
        None,
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions.\n\nModifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    code: Code | None = Field(
        None,
        description="A code that is a reference to ValueSet.expansion.property.code.",
    )
    # field_code: Element | None = Field(
    #     None, alias="_code", description="Extensions for code"
    # )
    valueCode: constr(pattern="^[^\\s]+( [^\\s]+)*$") | None = Field(
        None, description="The value of this property."
    )
    # field_valueCode: Element | None = Field(
    #     None, alias="_valueCode", description="Extensions for valueCode"
    # )
    valueCoding: Coding | None = Field(None, description="The value of this property.")
    valueString: constr(pattern="^^[\\s\\S]+$$") | None = Field(
        None, description="The value of this property."
    )
    # field_valueString: Element | None = Field(
    #     None, alias="_valueString", description="Extensions for valueString"
    # )
    valueInteger: float | None = Field(None, description="The value of this property.")
    # field_valueInteger: Element | None = Field(
    #     None, alias="_valueInteger", description="Extensions for valueInteger"
    # )
    valueBoolean: bool | None = Field(None, description="The value of this property.")
    # field_valueBoolean: Element | None = Field(
    #     None, alias="_valueBoolean", description="Extensions for valueBoolean"
    # )
    valueDateTime: (
        constr(
            pattern="^([0-9]([0-9]([0-9][1-9]|[1-9]0)|[1-9]00)|[1-9]000)(-(0[1-9]|1[0-2])(-(0[1-9]|[1-2][0-9]|3[0-1])(T([01][0-9]|2[0-3]):[0-5][0-9]:([0-5][0-9]|60)(\\.[0-9]{1,9})?)?)?(Z|(\\+|-)((0[0-9]|1[0-3]):[0-5][0-9]|14:00)?)?)?$"
        )
        | None
    ) = Field(None, description="The value of this property.")
    # field_valueDateTime: Element | None = Field(
    #     None, alias="_valueDateTime", description="Extensions for valueDateTime"
    # )
    valueDecimal: float | None = Field(None, description="The value of this property.")
    # field_valueDecimal: Element | None = Field(
    #     None, alias="_valueDecimal", description="Extensions for valueDecimal"
    # )
    subProperty: list[ValueSetSubProperty] | None = Field(
        None, description="A subproperty value for this concept."
    )


class ValueSetSubProperty(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    id: String | None = Field(
        None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: list[Extension] | None = Field(
        None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifierExtension: list[Extension] | None = Field(
        None,
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions.\n\nModifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    code: Code | None = Field(
        None,
        description="A code that is a reference to ValueSet.expansion.property.code.",
    )
    # field_code: Element | None = Field(
    #     None, alias="_code", description="Extensions for code"
    # )
    valueCode: constr(pattern="^[^\\s]+( [^\\s]+)*$") | None = Field(
        None, description="The value of this subproperty."
    )
    # field_valueCode: Element | None = Field(
    #     None, alias="_valueCode", description="Extensions for valueCode"
    # )
    valueCoding: Coding | None = Field(
        None, description="The value of this subproperty."
    )
    valueString: constr(pattern="^^[\\s\\S]+$$") | None = Field(
        None, description="The value of this subproperty."
    )
    # field_valueString: Element | None = Field(
    #     None, alias="_valueString", description="Extensions for valueString"
    # )
    valueInteger: float | None = Field(
        None, description="The value of this subproperty."
    )
    # field_valueInteger: Element | None = Field(
    #     None, alias="_valueInteger", description="Extensions for valueInteger"
    # )
    valueBoolean: bool | None = Field(
        None, description="The value of this subproperty."
    )
    # field_valueBoolean: Element | None = Field(
    #     None, alias="_valueBoolean", description="Extensions for valueBoolean"
    # )
    valueDateTime: (
        constr(
            pattern="^([0-9]([0-9]([0-9][1-9]|[1-9]0)|[1-9]00)|[1-9]000)(-(0[1-9]|1[0-2])(-(0[1-9]|[1-2][0-9]|3[0-1])(T([01][0-9]|2[0-3]):[0-5][0-9]:([0-5][0-9]|60)(\\.[0-9]{1,9})?)?)?(Z|(\\+|-)((0[0-9]|1[0-3]):[0-5][0-9]|14:00)?)?)?$"
        )
        | None
    ) = Field(None, description="The value of this subproperty.")
    # field_valueDateTime: Element | None = Field(
    #     None, alias="_valueDateTime", description="Extensions for valueDateTime"
    # )
    valueDecimal: float | None = Field(
        None, description="The value of this subproperty."
    )
    # field_valueDecimal: Element | None = Field(
    #     None, alias="_valueDecimal", description="Extensions for valueDecimal"
    # )


class ValueSetScope(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    id: String | None = Field(
        None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: list[Extension] | None = Field(
        None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifierExtension: list[Extension] | None = Field(
        None,
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions.\n\nModifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    inclusionCriteria: String | None = Field(
        None,
        description="Criteria describing which concepts or codes should be included and why.",
    )
    # field_inclusionCriteria: Element | None = Field(
    #     None, alias="_inclusionCriteria", description="Extensions for inclusionCriteria"
    # )
    exclusionCriteria: String | None = Field(
        None,
        description="Criteria describing which concepts or codes should be excluded and why.",
    )
    # field_exclusionCriteria: Element | None = Field(
    #     None, alias="_exclusionCriteria", description="Extensions for exclusionCriteria"
    # )


class VerificationResult(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    resourceType: Literal["VerificationResult"] = Field(
        ..., description="This is a VerificationResult resource"
    )
    id: Id | None = Field(
        None,
        description="The logical id of the resource, as used in the URL for the resource. Once assigned, this value never changes.",
    )
    meta: Meta | None = Field(
        None,
        description="The metadata about the resource. This is content that is maintained by the infrastructure. Changes to the content might not always be associated with version changes to the resource.",
    )
    implicitRules: Uri | None = Field(
        None,
        description="A reference to a set of rules that were followed when the resource was constructed, and which must be understood when processing the content. Often, this is a reference to an implementation guide that defines the special rules along with other profiles etc.",
    )
    # field_implicitRules: Element | None = Field(
    #     None, alias="_implicitRules", description="Extensions for implicitRules"
    # )
    language: Code | None = Field(
        None, description="The base language in which the resource is written."
    )
    # field_language: Element | None = Field(
    #     None, alias="_language", description="Extensions for language"
    # )
    text: Narrative | None = Field(
        None,
        description='A human-readable narrative that contains a summary of the resource and can be used to represent the content of the resource to a human. The narrative need not encode all the structured data, but is required to contain sufficient detail to make it "clinically safe" for a human to just read the narrative. Resource definitions may define what content should be represented in the narrative to ensure clinical safety.',
    )
    # contained: list[ResourceList] | None = Field(
    #     None,
    #     description="These resources do not have an independent existence apart from the resource that contains them - they cannot be identified independently, nor can they have their own independent transaction scope. This is allowed to be a Parameters resource if and only if it is referenced by a resource that provides context/meaning.",
    # )
    extension: list[Extension] | None = Field(
        None,
        description="May be used to represent additional information that is not part of the basic definition of the resource. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifierExtension: list[Extension] | None = Field(
        None,
        description="May be used to represent additional information that is not part of the basic definition of the resource and that modifies the understanding of the element that contains it and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer is allowed to define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions.\n\nModifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    target: list[Reference] | None = Field(
        None, description="A resource that was validated."
    )
    targetLocation: list[String] | None = Field(
        None,
        description="The fhirpath location(s) within the resource that was validated.",
    )
    # field_targetLocation: list[Element] | None = Field(
    #     None, alias="_targetLocation", description="Extensions for targetLocation"
    # )
    need: CodeableConcept | None = Field(
        None,
        description="The frequency with which the target must be validated (none; initial; periodic).",
    )
    status: Code | None = Field(
        None,
        description="The validation status of the target (attested; validated; in process; requires revalidation; validation failed; revalidation failed).",
    )
    # field_status: Element | None = Field(
    #     None, alias="_status", description="Extensions for status"
    # )
    statusDate: DateTime | None = Field(
        None, description="When the validation status was updated."
    )
    # field_statusDate: Element | None = Field(
    #     None, alias="_statusDate", description="Extensions for statusDate"
    # )
    validationType: CodeableConcept | None = Field(
        None,
        description="What the target is validated against (nothing; primary source; multiple sources).",
    )
    validationProcess: list[CodeableConcept] | None = Field(
        None,
        description="The primary process by which the target is validated (edit check; value set; primary source; multiple sources; standalone; in context).",
    )
    frequency: Timing | None = Field(None, description="Frequency of revalidation.")
    lastPerformed: DateTime | None = Field(
        None,
        description="The date/time validation was last completed (including failed validations).",
    )
    # field_lastPerformed: Element | None = Field(
    #     None, alias="_lastPerformed", description="Extensions for lastPerformed"
    # )
    nextScheduled: Date | None = Field(
        None, description="The date when target is next validated, if appropriate."
    )
    # field_nextScheduled: Element | None = Field(
    #     None, alias="_nextScheduled", description="Extensions for nextScheduled"
    # )
    failureAction: CodeableConcept | None = Field(
        None,
        description="The result if validation fails (fatal; warning; record only; none).",
    )
    # primarySource: list[VerificationResultPrimarySource] | None = Field(
    #     None,
    #     description="Information about the primary source(s) involved in validation.",
    # )
    # attestation: VerificationResultAttestation | None = Field(
    #     None, description="Information about the entity attesting to information."
    # )
    # validator: list[VerificationResultValidator] | None = Field(
    #     None, description="Information about the entity validating information."
    # )


ValueSetInclude.model_rebuild()
ValueSetCompose.model_rebuild()
ValueSetExpansion.model_rebuild()
