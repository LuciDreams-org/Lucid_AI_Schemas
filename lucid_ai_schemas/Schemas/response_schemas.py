import datetime
import json
import logging
from typing import Annotated, List, Optional
from pydantic import BaseModel, ConfigDict, Field, constr, field_validator

from lucid_ai_schemas.Schemas.enums import (
    ClassifierOptions,
    Departments,
    GraphType,
    Stages,
    Sectors,
    Countries,
    SubscriptionType,
    countries_list,
    stages_list,
    sectors_list
)
from lucid_ai_schemas.Schemas.input_schemas import Ai_utilsBase
from lucid_ai_schemas.Schemas.variable import MAX_LEN_STR_S

# @as_declarative()
# class Base:
#     id: Column(Integer, primary_key=True, autoincrement=True)
#     __name__: str

#     # Generate __tablename__ automatically

#     @declared_attr
#     def __tablename__(cls) -> str:
#         return cls.__name__.lower()

#     def to_dict(self):
#         """returns a dictionary representation of the object"""
#         res = dict()
#         for c in self.__table__.columns:
#             val = getattr(self, c.name)
#             if hasattr(val, 'to_dict'):
#                 val = val.to_dict()
#             res[c.name] = val
#         return res

#     def model_to_dict(self, ignore_fields: List[str] = None):
#         """
#         Serialize the model to a dictionary.
#         created separately from "to_dict" to not break existing code
#         (it might not anyway).
#         different from "to_dict" in that handles enum fields
#         and has an option to leave out selected fields
#         passed in the "ignore_fields" argument.
#         @param ignore_fields:
#         @return:
#         """
#         if ignore_fields is None:
#             ignore_fields = []
#         data = {}
#         for column in class_mapper(self.__class__).columns:
#             if column.key in ignore_fields:
#                 continue
#             value = getattr(self, column.key)

#             if hasattr(value, 'model_to_dict'):
#                 value = value.model_to_dict()
#             elif isinstance(value, Enum):
#                 value = value.value

#             data[column.key] = value
#         return data


class TemplateAssignerResponseSchema(BaseModel):
    templates: Optional[str] = Field(
        default=None,
        description="The templates that the business can use.")


class AssumptionsGeneratorResponse(BaseModel):
    calculations: List["AssumptionsGeneratorResponse.Calculation"] = Field(
        default=None,
        description="The calculations that are assumed by the model."
    )

    class Calculation(BaseModel):
        key: Optional[str] = Field(
            default=None,
            description="The key of the calculation."
        )
        value: Optional[str] = Field(
            default=None,
            description="The value of the calculation."
        )

        model_config = ConfigDict(extra="forbid")

    model_config = ConfigDict(extra="forbid")


class StringResponse(BaseModel):
    """
    Schema for expanding company details input.
    """
    response: Optional[str] = Field(
        default=None,
        description="A string response for the relevant object.")


class CompanyGoalsExtractorResponse(BaseModel):
    """
    Schema for extracting company goals from company output.
    """

    WHEN: Optional[str] = Field(
        default=str(datetime.now().strftime("%Y-%m-%d")),
        description="When the company plans to raise funding",
    )
    FUNDING: Optional[int] = Field(
        default=0,
        description="How much additional capital the company plans to raise.",
    )
    REVENUE: Optional[int] = Field(
        default=0,
        description="The revenue the company plans to have in a year."
    )
    EMPLOYEES: Optional[int] = Field(
        default=0,
        description="""The number of employees the company plans to have in a year.
        This is the number of employees the company plans
        to have in a year."""
    )

    @field_validator("WHEN", mode="before")
    def validate_date(cls, value: str) -> str:
        try:
            # Convert string to date
            input_date = datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError(
                f"Invalid date format: {value}. Expected format: YYYY-MM-DD"
            )
        # If the date is before today, return today's date as a string
        today_str = datetime.date.today().strftime("%Y-%m-%d")
        return today_str if input_date < datetime.date.today() else value

    model_config = ConfigDict(extra="allow")


class CompanyFieldExtractorResponse(BaseModel):
    """
    Schema for extracting fields from company output.
    """
    LOCATION: Optional[Countries] = Field(
        default=Countries.UNITED_STATES_OF_AMERICA_USA,
        description="The location from the list of countries/states.",
    )
    SECTORS: Optional[List[Sectors | str]] = Field(
        default_factory=list,
        description="Sectors (can be from the enum or any other string).",
    )
    FUNDING: Optional[int] = Field(
        default=0,
        description="Funding amount.",
    )
    STAGE: Optional[Stages] = Field(
        default=Stages.EARLY_STAGE,
        description="Stage of the company.",
    )
    ai_response_time: Optional[float] = None

    @field_validator("LOCATION", mode="before", check_fields=False)
    def validate_location(cls, value):
        # Validate LOCATION; default to USA if invalid.
        if value not in countries_list:
            logging.error(
                f"""Invalid LOCATION: {value}.
                Must be one of {countries_list}.""",
                exc_info=True,
            )
            return Countries.UNITED_STATES_OF_AMERICA_USA
        return value

    @field_validator("STAGE", mode="before", check_fields=False)
    def validate_stage(cls, value):
        # Validate STAGE; default to EARLY_STAGE if invalid.
        if value not in stages_list:
            logging.error(
                f"""Invalid STAGES: {value}.
                Must be one of {stages_list}.""",
                exc_info=True,
            )
            return Stages.EARLY_STAGE
        return value

    @field_validator("response", mode="before", check_fields=False)
    def parse_response(cls, value):
        # Parse JSON string to dict if necessary.
        if isinstance(value, str):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                raise ValueError("response is not valid JSON")
        return value

    model_config = ConfigDict(extra="allow")


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


class SalaryGeneratorResponse(BaseModel):
    positions: List[
        "SalaryGeneratorResponse.PositionSalaryGeneratorResponse"
        ] = Field(
        ...,
        description="The positions that are being filled with salaries.")

    class PositionSalaryGeneratorResponse(BaseModel):
        id: Optional[int] = Field(
            0,
            description="The ID of the employee.")
        yearly_salary: Optional[int] = Field(
            0,
            description="The yearly salary of the employee.")

        model_config = ConfigDict(extra="forbid")

    model_config = ConfigDict(extra="forbid")


SalaryGeneratorResponse.update_forward_refs()


class PromptTypeResponse(BaseModel):
    """
    Schema for the response of hp_classifier
    """
    sector: Optional[List[Sectors | str]] = Field(
        default_factory=list,
        description="Sectors (can be from the enum or any other string).",
    )
    balance: Optional[int] = Field(
        default=None,
        description="The balance of the company.")
    location: Optional[Countries] = Field(
        default=Countries.UNITED_STATES_OF_AMERICA_USA,
        description="The location from the list of countries/states.",
    )
    category: Optional[ClassifierOptions] = Field(
        default=ClassifierOptions.null,
        description="The category of which hiring plan prompt to use.")

    @field_validator("location", mode="before", check_fields=False)
    def validate_location(cls, value):
        # Validate location; default to USA if invalid.
        if value not in countries_list:
            logging.error(
                f"""Invalid location: {value}.
                Must be one of {countries_list}.""",
                exc_info=True,
            )
            return Countries.UNITED_STATES_OF_AMERICA_USA
        return value

    @field_validator("sector", mode="before", check_fields=False)
    def validate_sector(cls, value):
        # Validate sector; default to null if invalid.
        if value not in sectors_list:
            logging.error(
                f"""Invalid sector: {value}.
                Must be one of {sectors_list}.""",
                exc_info=True,
            )
            return Sectors.OTHER
        return value

    @field_validator("balance", mode="before", check_fields=False)
    def validate_balance(cls, value):
        # Validate balance; default to 0 if invalid.
        if value < 0:
            logging.error(
                f"""Invalid balance: {value}.
                Must be a positive integer.""",
                exc_info=True,
            )
            return 0
        return value

    @field_validator("category", mode="before", check_fields=False)
    def validate_category(cls, value):
        # Validate category; default to null if invalid.
        if value not in ClassifierOptions:
            logging.error(
                f"""Invalid category: {value}.
                Must be one of {ClassifierOptions}.""",
                exc_info=True,
            )
            return ClassifierOptions.null
        return value


class PlotCollectionResponse(BaseModel):
    """
    Schema for the plot generator response.
    """
    plots: List["PlotCollectionResponse.Plot"] = Field(
        default=None,
        description="The plots that are offered by the plot generator."
    )

    class Plot(BaseModel):
        """
        Schema for each individual plot that is
        suggested by the plot generator.
        """
        name: Optional[str] = Field(
            default=None,
            description="The name of the plot."
        )
        type: Optional[GraphType] = Field(
            default=GraphType.Bar,
            description="The type of the plot."
        )
        time_period: Optional[str] = Field(
            default=None,
            description="The time period the plot represents."
        )
        formulas: Optional[List[int]] = Field(
            default=None,
            description="The formulas that are used in the plot."
        )

    @field_validator("type", mode="before", check_fields=False)
    def validate_type(cls, value):
        if isinstance(value, str):
            value = value.strip()  # allowing AI to respond with Donut as well
            if value.lower() == "donut":
                return GraphType.donut

        # Validate type; default to BAR if invalid.
        if value not in GraphType:
            logging.error(
                f"""Invalid plot type: {value}.
                Must be one of {GraphType}.""",
                exc_info=True,
            )
            return GraphType.Bar
        return value


class ProductGeneratorOutput(BaseModel):
    """
    Combined schema for product generation.
    Contains a list of product details.
    """
    products: List["ProductGeneratorOutput.Product"] = Field(
        ...,
        description="A list of products offered by the company."
    )

    class Product(BaseModel):
        name: Optional[Annotated[str, constr(
            max_length=MAX_LEN_STR_S)]] = Field(
            0,
            description="The name of the product the company offers."
        )
        price: Optional[Annotated[float, Field(ge=0)]] = Field(
            description="The cost associated with the product."
        )
        amount_sold_last_m: Optional[Annotated[float, Field(ge=0)]] = Field(
            description="The number of units/subscriptions sold last month."
        )
        amount_sold_y_ago: Optional[Annotated[float, Field(ge=0)]] = Field(
            description="Number of units sold in the same month a year ago."
        )
        subscription_type: SubscriptionType = Field(
            SubscriptionType.monthly_subscription.value,
            description="The type of subscription the product entails."
        )
        CAC: Optional[Annotated[float, Field(ge=0)]] = Field(
            description="""Customer Acquisition Cost
            associated with the product."""
        )

        model_config = ConfigDict(extra="allow")

    model_config = ConfigDict(extra="allow")


# Ensure forward references are resolved.
ProductGeneratorOutput.update_forward_refs()


# Properties to receive via API on update
class Ai_utilsUpdate(Ai_utilsBase):
    """
    Schema for updating the AI utils.
    This is also used for Formula Selector, as it returns a single ID.
    """
    id: int = Field(
        default=None,
        description="The ID of the retrieved object.")
