import logging
from typing import List, Optional, Any
from pydantic import BaseModel, ConfigDict, Field, field_validator
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.runnables import RunnableSerializable
from lucid_ai_schemas.Schemas.enums import (
    Countries,
    Departments,
    countries_list
)


# Shared properties
class Ai_utilsBase(BaseModel):
    pass

    def to_dict(self):
        return self.model_dump()


class FillDictSchema(BaseModel):
    user_input_schema: str
    user_output_schema: Optional[str] = None
    user_output_schema_values: Optional[str] = None
    current_day: Optional[str] = None


class LogAIResponseObject(Ai_utilsBase):
    prompt_object: Optional[dict] = None
    response: Optional[dict] = None
    response_time: Optional[float] = None
    payload: Optional[dict] = None
    parsed_input: Optional[str] = None


class CompanyDetailsSchema(Ai_utilsBase):
    """
    Input schema for company details.
    """
    sectors: Optional[str | List[str]] = Field(
        default=None, description="The sectors the business is involved in."
    )
    freetext: Optional[str] = Field(
        default=None,
        description="""A conversational description of the
        business by the client."""
    )
    location: Optional[str] = Field(
        default=None,
        description="""The location where the business is located."""
    )
    products: Optional[List[Any]] = Field(
        default=None,
        description="""Potential products that the company is known to have.
        This will always be empty."""
    )
    company_stage: Optional[str] = Field(
        default=None,
        description="""The funding stage the company is currently in."""
    )
    funding_raise: Optional[str | int] = Field(
        default=None,
        description="""The amount of funding the business has raised."""
    )
    target_employees_in_one_year: Optional[float] = Field(
        default=None,
        description="""The number of employees the business
        expects to have in a year."""
    )
    target_revenue_in_one_year: Optional[str | int] = Field(
        default=None,
        description="""The revenue the business expects to have in a year."""
    )
    raise_next_round_date: Optional[str] = Field(
        default=None,
        description="""The date when the business plans to get funding,
        as a string."""
    )
    target_round_funding: Optional[str | int] = Field(
        default=None,
        description="""The amount of funding the business plans to
        raise in the future."""
    )

    def to_dict(self):
        return self.model_dump(exclude_none=True)


class AssumptionsInputSchema(Ai_utilsBase):
    date: Optional[str] = Field(
        default=None,
        description="The date of the assumptions.")
    formulas: Optional[Any] = Field(
        default=None,
        description="The formulas to be used in the assumptions.")
    sectors: Optional[str | List[str]] = Field(
        default=None,
        description="The sectors the business is involved in.")
    freetext: Optional[str] = Field(
        default=None,
        description="""A conversational description of the
        business by the client."""
    )
    location: Optional[str] = Field(
        default=None,
        description="""The location where the business is located."""
    )
    products: Optional[Any] = Field(
        default=None,
        description="""Potential products that the company is known to have."""
    )
    company_stage: Optional[str] = Field(
        default=None,
        description="The funding stage the company is currently in.")
    funding_raise: Optional[str] = Field(
        default=None,
        description="The amount of funding the business has raised.")
    target_round_funding: Optional[str] = Field(
        default=None,
        description="""The amount of funding the business plans to
        raise in the future."""
    )
    raise_next_round_date: Optional[str] = Field(
        default=None,
        description="""The date when the business plans to get funding,
        as a string."""
    )
    target_revenue_in_one_year: Optional[str] = Field(
        default=None,
        description="""The revenue the business expects to have in a year."""
    )
    target_employees_in_one_year: Optional[float] = Field(
        default=None,
        description="""The number of employees the business
        expects to have in a year."""
    )


class TemplateAssignerSchema(CompanyDetailsSchema):
    template_list: Optional[str] = Field(
        default=None,
        description="The templates that the business can use.")


class OrchestratorSchema(Ai_utilsBase):
    branch_id: Optional[int] = Field(
        default=None,
        description="The branch ID of the business.")
    freetext: Optional[str] = Field(
        default=None,
        description="""A conversational description of the
        business by the client."""
    )


class AIVoiceRequestSchema(Ai_utilsBase):
    voice_id: Optional[str] = "iP95p4xoKVk53GoZ742B"
    freetext: str = None


class CompanyDetailsExpanderSchema(Ai_utilsBase):
    freetext: Optional[str] = Field(
        default=None,
        description="""A conversational description of the
        business by the client."""
    )
    questions: Optional[List[str]] = Field(
        default=[
            "what_are_you_building",
            "who_are_you_building_it_for",
            "when_and_where_will_it_launch",
            "how_will_it_be_delivered",
        ],
        description="A list of questions to expand the free text into.",
    )

    def to_dict(self):
        return self.model_dump()


class CompanySummaryRefinerSchema(Ai_utilsBase):
    """
    Schema for refining company summary input.
    """
    seo_description: str = Field(
        default=None,
        description="A SEO description of the business.",
    )
    short_description: str = Field(
        default=None,
        description="A short description of the business by the client.",
    )
    scraped_website_data: str = Field(
        default=None,
        description="Scraped data from the company's website.",
    )
    company_object: Optional[str] = Field(
        default=None,
        description="A JSON object representing the company.",
    )

    def to_dict(self):
        return {
            "descriptions": f"""
        [[seo_description: {self.seo_description}]],
        [[short_description: {self.short_description}],
        [[scraped_website_data:{self.scraped_website_data}]]
        [[company_object: {self.company_object}]]
        """
        }


class ExtractGoalsORFieldsInputSchema(Ai_utilsBase):
    """
    Schema for extracting fields from company input.
    """
    freetext: str = Field(...,
                          description="Input free text provided by the user.")
    additional_info: str = Field(
        None, description="Additional context or details to aid summarization."
    )

    def to_dict(self):
        return self.model_dump()


class GetPromptSummarizerSchema(Ai_utilsBase):
    """
    Input Schema for the prompt summarizer.
    """

    response: Any = Field(
        default=None,
        description="The response that is received by the prompt.")
    user_input: Optional[str] = Field(
        default=None,
        description="The user input to be used in the prompt.")
    prompt_type: Optional[str] = Field(
        default=None,
        description="The type of prompt that is being summarized.")
    prompt_operation: Optional[str] = Field(
        default=None,
        description="The operation the prompt is performing.")


class Ai_utilsCreate(Ai_utilsBase):
    pass


class Ai_utilsInDBBase(Ai_utilsBase):
    pass


# Additional properties to return via API
class Ai_utils(Ai_utilsInDBBase):
    pass


# Additional properties stored in DB
class Ai_utilsInDB(Ai_utilsInDBBase):
    pass


class Ai_utilsOutSchema(Ai_utilsBase):
    pass


class PromptFilterSchema(Ai_utilsBase):
    slug: str


class SalaryGeneratorSchema(BaseModel):
    positions: List[
        "SalaryGeneratorSchema.PositionSalaryGeneratorSchema"] = Field(
        ...,
        description="The positions that need to be filled with salaries.")

    class PositionSalaryGeneratorSchema(BaseModel):
        id: Optional[int] = Field(
            description="The ID of the employee.")
        role: Optional[str] = Field(
            description="The role of the employee.")
        department: Optional[Departments] = Field(
            description="The department of the employee.")
        geo_location: Optional[Countries] = Field(
            description="The geo location of the employee.")

        @field_validator("geo_location", mode="before", check_fields=False)
        def validate_location(cls, value):
            if value not in countries_list:
                logging.error(
                    f"""Invalid location: {value}.
                    Must be one of {countries_list}.""",
                    exc_info=True,
                )
                return Countries.UNITED_STATES_OF_AMERICA_USA
            return value

        model_config = ConfigDict(extra="forbid")

    model_config = ConfigDict(extra="forbid")


SalaryGeneratorSchema.update_forward_refs()


class PositionSchema(Ai_utilsBase):
    class Positions(BaseModel):
        id: Optional[int] = Field(
            default=None,
            description="The ID of the employee.")
        role: Optional[str] = Field(
            default=None,
            description="The role of the employee.")
        bonus: Optional[int] = Field(
            default=None,
            description="The yearly bonus of the employee.")
        full_name: Optional[str] = Field(
            default=None,
            description="The full name of the employee.")
        department: Optional[Departments] = Field(
            default=Departments.G_A,
            description="The department of the employee.")
        start_date: Optional[str] = Field(
            default=None,
            description="The start date of the employee.")
        geo_location: Optional[Countries] = Field(
            default=Countries.UNITED_STATES_OF_AMERICA_USA,
            description="The geo location of the employee.")
        yearly_salary: Optional[int] = Field(
            default=None,
            description="The yearly salary of the employee.")

        @field_validator("geo_location", mode="before", check_fields=False)
        def validate_location(cls, value):
            if value not in countries_list:
                logging.error(
                    f"""Invalid location: {value}.
                    Must be one of {countries_list}.""",
                    exc_info=True,
                )
                return Countries.UNITED_STATES_OF_AMERICA_USA
            return value

        model_config = ConfigDict(extra="allow")

        @field_validator("department", mode="before", check_fields=False)
        def normalize_department(cls, value):
            department_mapping = {
                "rnd": "R&D",
                "snm": "S&M",
                "gna": "G&A",
                "cogs": "COGS"
            }
            if isinstance(value, str) and value.lower() in department_mapping:
                return department_mapping[value.lower()]
            return value

    positions: Optional[List[Positions]] = Field(
        default=None,
        description="The positions that should be added to the hiring plan.")

    model_config = ConfigDict(extra="allow")


class HiringGenerateSchema(Ai_utilsBase):
    sectors: Optional[str] = Field(
        default=None,
        description="The sector of the company.")
    balance: Optional[int | str] = Field(
        default=None,
        description="The balance of the company.")
    location: Optional[str] = Field(
        default=None,
        description="The country of the company.")
    stage: Optional[str] = Field(
        default=None,
        description="The stage that the company is in.")
    freetext: Optional[str] = Field(
        default=None,
        description="The user input regarding his request.")


class HiringUpdateSchema(HiringGenerateSchema):
    positions: Optional[List["PositionSchema.Positions"]] = Field(
        default=None,
        description="The positions to be updated.")


class HiringDecreaseResponseSchema(BaseModel):
    positions: Optional[List[
        "HiringDecreaseResponseSchema.DecreasePosition"]] = Field(
        default=None,
        description="The positions to be removed.")

    class DecreasePosition(BaseModel):
        id: Optional[int] = Field(
            default=None,
            description="The ID of the employee to remove.")


class JobInSchema(Ai_utilsBase):
    sector: str
    letters: str


class PromptUpdateSchema(Ai_utilsBase):
    prompt: str
    engine: Optional[str] = None


class PromptTypeSchema(Ai_utilsBase):
    """
    Schema for the input of hp_classifier
    """
    input: Optional[str] = Field(
        default=None,
        description="The input of the prompt.")


class Transaction(Ai_utilsBase):
    date: str  # The date on which the transaction transpired.
    name: str  # The name of the transaction.
    amount: float  # The transaction's amount.


class CellData(Ai_utilsBase):
    name: str  # The name of the formula or calculation the cell represents.
    date: str  # The date to which the cell is associated.
    total_value: float
    transactions: List[
        Transaction
    ]  # A list of the transactions associated with the cell.


class ExplainerSchema(Ai_utilsBase):
    input: Optional[List["ExplainerSchema.Formula"]] = Field(
        default=None,
        description="The input of the explainer.")

    class Formula(BaseModel):
        date: Optional[str] = Field(
            default=None,
            description="The date of the formula.")
        name: Optional[str] = Field(
            default=None,
            description="The name of the formula.")
        total_value: Optional[float] = Field(
            default=None,
            description="The total value of the formula.")
        transactions: Optional[List[
            "ExplainerSchema.Formula.Transaction"]] = Field(
            default=None,
            description="The transactions of the formula.")

        class Transaction(BaseModel):
            date: Optional[str] = Field(
                default=None,
                description="The date of the transaction.")
            name: Optional[str] = Field(
                default=None,
                description="The name of the transaction.")
            amount: Optional[float] = Field(
                default=None,
                description="The amount of the transaction.")


class PlotORFormulaSchema(BaseModel):
    """
    Schema for the plot generator response.
    """
    formulas: List["PlotORFormulaSchema.Formula"] = Field(
        default=None,
        description="List of formula objects")
    freetext: str = Field(
        default=None,
        description="The user's input for the plot generator.")

    class Formula(BaseModel):
        """
        Represents a single formula object with an integer ID
        and string name.
        """
        id: int = Field(
            default=None,
            description="Unique identifier for the formula")
        name: str = Field(
            default=None,
            description="Human-readable name of the formula")


class MessageSchema(Ai_utilsBase):
    role: str
    content: str


class GeneralRequestSchema(Ai_utilsBase):
    input: str
    system: Optional[str] = None
    messages: Optional[List[MessageSchema]] = None
    engine: Optional[str] = None


class GetChainConfigReturnSchema(BaseModel):
    """
    Schema for returning chain configuration details -
    this function get_chain_for_prompt
    """
    prompt_text: str = Field("",
                             description="""The prompt text to be
                             used in the chain.""")
    prompt_template: Optional[ChatPromptTemplate] = Field(
        None, description="The prompt template to be used in the chain."
    )
    llm: Optional[RunnableSerializable] = Field(
        None, description="The Langsmith model to be used in the chain."
    )

# TODO: Fix this input schema so that it works
# Validate Question
# class ValidateQuestionInput(BaseModel):
#     """
#     Schema for validating questions input.
#     """

#     freetext: str = Field(
#         default=None,
#         description="""A conversational description of
#         the business by the client.
#         This will be used to answer the questions.""",
#     )
# questions: List[str] = Field(
#     default=None, description="A list of specific questions to be answered."
# )
