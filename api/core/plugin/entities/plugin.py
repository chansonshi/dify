import datetime
from collections.abc import Mapping
from enum import StrEnum, auto
from typing import Any, Optional

from packaging.version import InvalidVersion, Version
from pydantic import BaseModel, Field, field_validator, model_validator

from core.agent.plugin_entities import AgentStrategyProviderEntity
from core.datasource.entities.datasource_entities import DatasourceProviderEntity
from core.model_runtime.entities.provider_entities import ProviderEntity
from core.plugin.entities.base import BasePluginEntity
from core.plugin.entities.endpoint import EndpointProviderDeclaration
from core.tools.entities.common_entities import I18nObject
from core.tools.entities.tool_entities import ToolProviderEntity
from core.trigger.entities.entities import TriggerProviderEntity


class PluginInstallationSource(StrEnum):
    Github = auto()
    Marketplace = auto()
    Package = auto()
    Remote = auto()


class PluginResourceRequirements(BaseModel):
    memory: int

    class Permission(BaseModel):
        class Tool(BaseModel):
            enabled: Optional[bool] = Field(default=False)

        class Model(BaseModel):
            enabled: Optional[bool] = Field(default=False)
            llm: Optional[bool] = Field(default=False)
            text_embedding: Optional[bool] = Field(default=False)
            rerank: Optional[bool] = Field(default=False)
            tts: Optional[bool] = Field(default=False)
            speech2text: Optional[bool] = Field(default=False)
            moderation: Optional[bool] = Field(default=False)

        class Node(BaseModel):
            enabled: Optional[bool] = Field(default=False)

        class Endpoint(BaseModel):
            enabled: Optional[bool] = Field(default=False)

        class Storage(BaseModel):
            enabled: Optional[bool] = Field(default=False)
            size: int = Field(ge=1024, le=1073741824, default=1048576)

        tool: Optional[Tool] = Field(default=None)
        model: Optional[Model] = Field(default=None)
        node: Optional[Node] = Field(default=None)
        endpoint: Optional[Endpoint] = Field(default=None)
        storage: Optional[Storage] = Field(default=None)

    permission: Optional[Permission] = Field(default=None)


class PluginCategory(StrEnum):
    Tool = auto()
    Model = auto()
    Extension = auto()
    AgentStrategy = auto()
    Datasource = auto()
    Trigger = auto()


class PluginDeclaration(BaseModel):
    class Plugins(BaseModel):
        tools: Optional[list[str]] = Field(default_factory=list[str])
        models: Optional[list[str]] = Field(default_factory=list[str])
        endpoints: Optional[list[str]] = Field(default_factory=list[str])
        triggers: Optional[list[str]] = Field(default_factory=list[str])
        datasources: list[str] | None = Field(default_factory=list[str])

    class Meta(BaseModel):
        minimum_dify_version: Optional[str] = Field(default=None, pattern=r"^\d{1,4}(\.\d{1,4}){1,3}(-\w{1,16})?$")
        version: Optional[str] = Field(default=None)

        @field_validator("minimum_dify_version")
        @classmethod
        def validate_minimum_dify_version(cls, v: str | None) -> str | None:
            if v is None:
                return v
            try:
                Version(v)
                return v
            except InvalidVersion as e:
                raise ValueError(f"Invalid version format: {v}") from e

    version: str = Field(..., pattern=r"^\d{1,4}(\.\d{1,4}){1,3}(-\w{1,16})?$")
    author: Optional[str] = Field(..., pattern=r"^[a-zA-Z0-9_-]{1,64}$")
    name: str = Field(..., pattern=r"^[a-z0-9_-]{1,128}$")
    description: I18nObject
    icon: str
    icon_dark: Optional[str] = Field(default=None)
    label: I18nObject
    category: PluginCategory
    created_at: datetime.datetime
    resource: PluginResourceRequirements
    plugins: Plugins
    tags: list[str] = Field(default_factory=list)
    repo: Optional[str] = Field(default=None)
    verified: bool = Field(default=False)
    tool: Optional[ToolProviderEntity] = None
    model: Optional[ProviderEntity] = None
    endpoint: Optional[EndpointProviderDeclaration] = None
    agent_strategy: Optional[AgentStrategyProviderEntity] = None
    datasource: DatasourceProviderEntity | None = None
    trigger: Optional[TriggerProviderEntity] = None
    meta: Meta

    @field_validator("version")
    @classmethod
    def validate_version(cls, v: str) -> str:
        try:
            Version(v)
            return v
        except InvalidVersion as e:
            raise ValueError(f"Invalid version format: {v}") from e

    @model_validator(mode="before")
    @classmethod
    def validate_category(cls, values: dict) -> dict:
        # auto detect category
        if values.get("tool"):
            values["category"] = PluginCategory.Tool
        elif values.get("model"):
            values["category"] = PluginCategory.Model
        elif values.get("datasource"):
            values["category"] = PluginCategory.Datasource
        elif values.get("agent_strategy"):
            values["category"] = PluginCategory.AgentStrategy
        elif values.get("trigger"):
            values["category"] = PluginCategory.Trigger
        else:
            values["category"] = PluginCategory.Extension
        return values


class PluginInstallation(BasePluginEntity):
    tenant_id: str
    endpoints_setups: int
    endpoints_active: int
    runtime_type: str
    source: PluginInstallationSource
    meta: Mapping[str, Any]
    plugin_id: str
    plugin_unique_identifier: str
    version: str
    checksum: str
    declaration: PluginDeclaration


class PluginEntity(PluginInstallation):
    name: str
    installation_id: str
    version: str

    @model_validator(mode="after")
    def set_plugin_id(self):
        if self.declaration.tool:
            self.declaration.tool.plugin_id = self.plugin_id
        return self


class PluginDependency(BaseModel):
    class Type(StrEnum):
        Github = PluginInstallationSource.Github
        Marketplace = PluginInstallationSource.Marketplace
        Package = PluginInstallationSource.Package

    class Github(BaseModel):
        repo: str
        version: str
        package: str
        github_plugin_unique_identifier: str

        @property
        def plugin_unique_identifier(self) -> str:
            return self.github_plugin_unique_identifier

    class Marketplace(BaseModel):
        marketplace_plugin_unique_identifier: str
        version: str | None = None

        @property
        def plugin_unique_identifier(self) -> str:
            return self.marketplace_plugin_unique_identifier

    class Package(BaseModel):
        plugin_unique_identifier: str
        version: str | None = None

    type: Type
    value: Github | Marketplace | Package
    current_identifier: Optional[str] = None


class MissingPluginDependency(BaseModel):
    plugin_unique_identifier: str
    current_identifier: Optional[str] = None
