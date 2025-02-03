from typing import List, Optional, Any
from pydantic import BaseModel, ConfigDict


# Shared properties
class Ai_utilsBase(BaseModel):
    pass

    def to_dict(self):
        return self.model_dump()


class CompanyDetailsSchema(Ai_utilsBase):
    sectors: Optional[str | List[str]] = None
    freetext: Optional[str] = None
    location: Optional[str] = None
    products: Optional[Any] = None
    company_stage: Optional[str] = None
    funding_raise: Optional[float] = None
    target_employees_in_one_year: Optional[float] = None
    target_revenue_in_one_year: Optional[float] = None
    raise_next_round_date: Optional[str] = None
    target_round_funding: Optional[float] = None

    def to_dict(self):
        return self.model_dump()


class AssumptionsInputSchema(Ai_utilsBase):
    date: Optional[str] = None
    formulas: Optional[Any] = None  # list { model_name: [formula1, formula2] }
    sectors: Optional[str | List[str]] = None
    freetext: Optional[str] = None
    location: Optional[str] = None
    products: Optional[Any] = None
    company_stage: Optional[str] = None
    funding_raise: Optional[float] = None


class TemplateAssignmentDataSchema(BaseModel):
    sectors: List[str]
    freetext: str
    location: str
    products: List[Any]
    company_stage: str
    funding_raise: float
    target_employees_in_one_year: int
    target_revenue_in_one_year: float
    raise_next_round_date: str
    target_round_funding: float
    template_list: List[Any]


class TemplateAssignerSchema(CompanyDetailsSchema):
    # template_list: List[str]
    pass


class OrchestratorSchema(Ai_utilsBase):
    branch_id: Optional[int] = None
    freetext: Optional[str] = None


class AIVoiceRequestSchema(Ai_utilsBase):
    voice_id: Optional[str] = 'iP95p4xoKVk53GoZ742B'
    freetext: str = None


class AssumptionsGeneratorSchema(Ai_utilsBase):
    date: Optional[str] = None
    formulas: Optional[dict[str, List[str]]] = None  # list { model_name: [formula1, formula2] }

    def to_dict(self):
        return self.model_dump()


class CompanyDetailsExpanderSchema(Ai_utilsBase):
    freetext: str
    questions: List[str] = [
        "what_are_you_building",
        "who_are_you_building_it_for",
        "when_and_where_will_it_launch",
        "how_will_it_be_delivered"
    ]

    def to_dict(self):
        return self.model_dump()


# company_summary_refiner
class CompanySummaryRefinerSchema(Ai_utilsBase):
    seo_description: str
    short_description: str
    scraped_website_data: str
    company_object: Optional[str] = None

    def to_dict(self):
        return {
            "descriptions": f"""
        [[seo_description: {self.seo_description}]],
        [[short_description: {self.short_description}],
        [[scraped_website_data:{self.scraped_website_data}]]
        [[company_object: {self.company_object}]]
        """
        }


class ExtractFieldsFromCompanyDetails(Ai_utilsBase):
    freetext: str

    def to_dict(self):
        return self.model_dump()


class GetPromptSummsrizerSchema(Ai_utilsBase):
    user_input: Optional[str] = None
    response: Any = None
    prompt_type: Optional[str] = None
    prompt_operation: Optional[str] = None


# Properties to receive via API on creation
class Ai_utilsCreate(Ai_utilsBase):
    pass


# Properties to receive via API on update
class Ai_utilsUpdate(Ai_utilsBase):
    id: int = None


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


# HIring Plan sechemas


class PromptFilterSchema(Ai_utilsBase):
    slug: str


class PositionSchema(Ai_utilsBase):
    role: Optional[str]
    yearly_salary: Optional[int] = None
    bonus: Optional[int] = None
    department: Optional[str]
    start_date: Optional[str] = None
    id: Optional[int] = None
    geo_location: Optional[str] = None

    model_config = ConfigDict(extra='allow')


class HiringGenerateSchema(Ai_utilsBase):
    balance: Optional[str] = None
    sector: Optional[str] = None
    country: Optional[str] = None
    freetext: Optional[str] = None


class HiringIncreaseUpdateSchema(HiringGenerateSchema):
    positions: Optional[List[PositionSchema]] = None


class MultiCurrencyModifyEmployeesSchema(HiringIncreaseUpdateSchema):
    country: Optional[str] = None


class HiringUpdateSchema(HiringGenerateSchema):
    positions: Optional[List[PositionSchema]] = None


class HiringGenerateOutSchema(BaseModel):
    hiring_positions: List[PositionSchema]


# Job Role Suggestions schemas


class JobInSchema(Ai_utilsBase):
    sector: str
    letters: str


# class OutputSchema(BaseModel):
#     job_title: str
#     seniority: int
#     salary: int
#     bonuses: datetime


# class JobOutSchema(BaseModel):
#     output: List[OutputSchema]


class PromptUpdateSchema(Ai_utilsBase):
    prompt: str
    engine: Optional[str] = None


class PromptTypeSchema(Ai_utilsBase):
    input: str


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
    input: List[CellData]


class MessageSchema(Ai_utilsBase):
    role: str
    content: str


class GeneralRequestSchema(Ai_utilsBase):
    input: str
    system: Optional[str] = None
    messages: Optional[List[MessageSchema]] = None
    engine: Optional[str] = None
