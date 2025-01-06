from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class Coding(BaseModel):
    """Represents a code from a code system"""

    model_config = ConfigDict(
        extra="forbid",
    )
    system: str | None = Field(
        None,
        description="The identification of the code system that defines the meaning of the symbol in the code.",
    )
    version: str | None = Field(
        None,
        description="The version of the code system which was used when choosing this code. Note that a well-maintained code system does not need the version reported, because the meaning of codes is consistent across versions. However this cannot consistently be assured, and when the meaning is not guaranteed to be consistent, the version SHOULD be exchanged.",
    )
    code: str = Field(
        description="A symbol in syntax defined by the system. The symbol may be a predefined code or an expression in a syntax defined by the coding system (e.g. post-coordination).",
    )
    display: str | None = Field(
        None,
        description="A representation of the meaning of the code in the system, following the rules of the system.",
    )
    user_selected: bool | None = Field(
        None,
        description="Indicates that this coding was chosen by a user directly - e.g. off a pick list of available items (codes or displays).",
    )
