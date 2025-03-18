from datetime import datetime
from enum import Enum
import json
import logging
from typing import Annotated, List, Optional, Any
from pydantic import BaseModel, ConfigDict, Field, constr, field_validator
from lucid_ai_schemas.Schemas.variable import MAX_LEN_STR_S


# Shared properties
class Ai_utilsBase(BaseModel):
    pass

    def to_dict(self):
        return self.model_dump()


# General Prompts
class GraphType(Enum):
    Area = "Area"
    Bar = "Bar"
    Line = "Line"
    BarCombo = "BarCombo"
    Stacked = "Stacked"
    StackedCombo = "StackedCombo"
    donut = "donut"
    rankedList = "rankedList"
    Scorecard = "Scorecard"
    GroupedStackedCombo = "GroupedStackedCombo"


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
        Schema for each individual plot that
        is suggested by the plot generator.
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


class Ai_utilsUpdate(Ai_utilsBase):
    """
    Schema for updating the AI utils.
    This is also used for Formula Selector, as it returns a single ID.
    """
    id: int = Field(
        default=None,
        description="The ID of the retrieved object.")


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


class StringResponse(BaseModel):
    """
    Schema for expanding company details input.
    """
    response: Optional[str] = Field(
        default=None,
        description="A string response for the relevant object.")


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
            description="""The transactions of the formula."""
        )

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
        description="""A conversational description of the business
        by the client."""
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
        description="""The amount of funding the business plans
        to raise in the future."""
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
        description="""The number of employees the business expects
        to have in a year."""
    )


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


class CompanyDetailsSchema(Ai_utilsBase):
    """
    Input schema for company details.
    """
    sectors: Optional[str | List[str]] = Field(
        default=None, description="The sectors the business is involved in."
    )
    freetext: Optional[str] = Field(
        default=None,
        description="""A conversational description of the business
        by the client."""
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
        description="""The number of employees the business expects
        to have in a year."""
    )
    target_revenue_in_one_year: Optional[str | int] = Field(
        default=None, description="""The revenue the business expects
        to have in a year."""
    )
    raise_next_round_date: Optional[str] = Field(
        default=None,
        description="""The date when the business plans to get funding,
        as a string."""
    )
    target_round_funding: Optional[str | int] = Field(
        default=None,
        description="""The amount of funding the business plans
        to raise in the future."""
    )

    def to_dict(self):
        return self.model_dump(exclude_none=True)


class SubscriptionType(str, Enum):
    monthly_and_yearly_subscription = "Monthly & Yearly Subscription"
    one_time_purchase = "One Time Purchase"
    monthly_subscription = "Monthly Subscription"
    yearly_subscription = "Yearly Subscription"


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
            description="""The type of subscription the product entails."""
        )
        CAC: Optional[Annotated[float, Field(ge=0)]] = Field(
            description="""Customer Acquisition Cost associated
            with the product."""
        )

        model_config = ConfigDict(extra="allow")

    model_config = ConfigDict(extra="allow")


class TemplateAssignerSchema(CompanyDetailsSchema):
    template_list: Optional[str] = Field(
        default=None,
        description="The templates that the business can use.")


class TemplateAssignerResponseSchema(BaseModel):
    templates: Optional[str] = Field(
        default=None,
        description="The templates that the business can use.")


# Onboarding Prompts
class CompanyDetailsExpanderSchema(Ai_utilsBase):
    freetext: Optional[str] = Field(
        default=None,
        description="""A conversational description of the business by the client.
        This will always be empty.""",
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


# Enum for sectors
class Sectors(str, Enum):
    FINTECH = "Fintech"
    HEALTHTECH = "Healthtech"
    SAAS_SOFTWARE_AS_A_SERVICE = "SaaS (Software as a Service)"
    E_COMMERCE = "E-commerce"
    ARTIFICIAL_INTELLIGENCE_AND_MACHINE_LEARNING = (
        "Artificial Intelligence (AI) and Machine Learning (ML)"
    )
    EDTECH = "Edtech"
    CYBERSECURITY = "Cybersecurity"
    BIOTECHNOLOGY = "Biotechnology"
    INTERNET_OF_THINGS = "Internet of Things (IoT)"
    CLEAN_ENERGY_AND_SUSTAINABILITY = "Clean Energy and Sustainability"
    PROPTECH = "Proptech (Property Technology)"
    AUGMENTED_AND_VIRTUAL_REALITY = """Augmented Reality (AR) and
    Virtual Reality (VR)"""
    FOODTECH = "Foodtech"
    AUTONOMOUS_VEHICLES = "Autonomous Vehicles"
    ROBOTICS = "Robotics"
    AGTECH = "Agtech (Agriculture Technology)"
    INSURTECH = "Insurtech (Insurance Technology)"
    MEDTECH = "Medtech (Medical Technology)"
    BLOCKCHAIN_AND_CRYPTOCURRENCY = "Blockchain and Cryptocurrency"
    DIGITAL_HEALTH = "Digital Health"
    DESIGN = "Design"
    MARTECH = "MarTech (Marketing Technology)"
    HRTECH = "HRTech (Human Resources Technology)"
    TRAVEL_AND_TOURISM_TECHNOLOGY = "Travel and Tourism Technology"
    ENTERTAINMENT_AND_MEDIA_TECHNOLOGY = "Entertainment and Media Technology"
    RETAIL_AND_CONSUMER_GOODS = "Retail and Consumer Goods"
    LEGAL = "Legal"
    SPORTSTECH = "SportsTech"
    FASHION = "Fashion"
    ADTECH = "AdTech (Advertising Technology)"
    GAMING_AND_ESPORTS = "Gaming and Esports"
    MANUFACTURING_AND_INDUSTRIAL_AUTOMATION = """Manufacturing and
    Industrial Automation"""
    BANKING_AND_FINANCIAL_SERVICES = "Banking and Financial Services"
    CONSTRUCTION_AND_ENGINEERING = "Construction and Engineering"
    REAL_ESTATE = "Real Estate"
    EVENT_PLANNING = "Event Planning"
    CONSULTING_SERVICES = "Consulting Services"
    CONTENT_CREATION = "Content Creation"
    OTHER = "Other"


# Enums for stages
class Stages(str, Enum):
    IDEA_STAGE = "Idea Stage"
    SEED_STAGE = "Seed Stage"
    EARLY_STAGE = "Early Stage"
    GROWTH_STAGE = "Growth Stage"
    SERIES_A = "Series A"
    SERIES_B = "Series B"
    SERIES_C = "Series C"
    SERIES_D_PLUS = "Series D+"
    EXIT_STAGE = "Exit Stage"


# Enums for countries (includes US states as listed)
class Countries(str, Enum):
    UNITED_STATES_OF_AMERICA_USA = "United States of America (USA)"
    AFGHANISTAN = "Afghanistan"
    ALBANIA = "Albania"
    ALGERIA = "Algeria"
    ANDORRA = "Andorra"
    ANGOLA = "Angola"
    ANTIGUA_AND_BARBUDA = "Antigua and Barbuda"
    ARGENTINA = "Argentina"
    ARMENIA = "Armenia"
    AUSTRALIA = "Australia"
    AUSTRIA = "Austria"
    AZERBAIJAN = "Azerbaijan"
    BAHAMAS = "Bahamas"
    BAHRAIN = "Bahrain"
    BANGLADESH = "Bangladesh"
    BARBADOS = "Barbados"
    BELARUS = "Belarus"
    BELGIUM = "Belgium"
    BELIZE = "Belize"
    BENIN = "Benin"
    BHUTAN = "Bhutan"
    BOLIVIA = "Bolivia"
    BOSNIA_AND_HERZEGOVINA = "Bosnia and Herzegovina"
    BOTSWANA = "Botswana"
    BRAZIL = "Brazil"
    BRUNEI = "Brunei"
    BULGARIA = "Bulgaria"
    BURKINA_FASO = "Burkina Faso"
    BURUNDI = "Burundi"
    CABO_VERDE = "Cabo Verde"
    CAMBODIA = "Cambodia"
    CAMEROON = "Cameroon"
    CANADA = "Canada"
    CENTRAL_AFRICAN_REPUBLIC_CAR = "Central African Republic (CAR)"
    CHAD = "Chad"
    CHILE = "Chile"
    CHINA = "China"
    COLOMBIA = "Colombia"
    COMOROS = "Comoros"
    DEMOCRATIC_REPUBLIC_OF_THE_CONGO = "Democratic Republic of the Congo"
    REPUBLIC_OF_THE_CONGO = "Republic of the Congo"
    COSTA_RICA = "Costa Rica"
    CROATIA = "Croatia"
    CUBA = "Cuba"
    CYPRUS = "Cyprus"
    CZECH_REPUBLIC = "Czech Republic"
    DENMARK = "Denmark"
    DJIBOUTI = "Djibouti"
    DOMINICA = "Dominica"
    DOMINICAN_REPUBLIC = "Dominican Republic"
    EAST_TIMOR_TIMOR_LESTE = "East Timor (Timor-Leste)"
    ECUADOR = "Ecuador"
    EGYPT = "Egypt"
    EL_SALVADOR = "El Salvador"
    EQUATORIAL_GUINEA = "Equatorial Guinea"
    ERITREA = "Eritrea"
    ESTONIA = "Estonia"
    ESWATINI = "Eswatini"
    ETHIOPIA = "Ethiopia"
    FIJI = "Fiji"
    FINLAND = "Finland"
    FRANCE = "France"
    GABON = "Gabon"
    GAMBIA = "Gambia"
    GEORGIA = "Georgia"
    GERMANY = "Germany"
    GHANA = "Ghana"
    GREECE = "Greece"
    GRENADA = "Grenada"
    GUATEMALA = "Guatemala"
    GUINEA = "Guinea"
    GUINEA_BISSAU = "Guinea-Bissau"
    GUYANA = "Guyana"
    HAITI = "Haiti"
    HONDURAS = "Honduras"
    HUNGARY = "Hungary"
    ICELAND = "Iceland"
    INDIA = "India"
    INDONESIA = "Indonesia"
    IRAN = "Iran"
    IRAQ = "Iraq"
    IRELAND = "Ireland"
    ISRAEL = "Israel"
    ITALY = "Italy"
    IVORY_COAST = "Ivory Coast"
    JAMAICA = "Jamaica"
    JAPAN = "Japan"
    JORDAN = "Jordan"
    KAZAKHSTAN = "Kazakhstan"
    KENYA = "Kenya"
    KIRIBATI = "Kiribati"
    KOSOVO = "Kosovo"
    KUWAIT = "Kuwait"
    KYRGYZSTAN = "Kyrgyzstan"
    LAOS = "Laos"
    LATVIA = "Latvia"
    LEBANON = "Lebanon"
    LESOTHO = "Lesotho"
    LIBERIA = "Liberia"
    LIBYA = "Libya"
    LIECHTENSTEIN = "Liechtenstein"
    LITHUANIA = "Lithuania"
    LUXEMBOURG = "Luxembourg"
    MADAGASCAR = "Madagascar"
    MALAWI = "Malawi"
    MALAYSIA = "Malaysia"
    MALDIVES = "Maldives"
    MALI = "Mali"
    MALTA = "Malta"
    MARSHALL_ISLANDS = "Marshall Islands"
    MAURITANIA = "Mauritania"
    MAURITIUS = "Mauritius"
    MEXICO = "Mexico"
    MICRONESIA = "Micronesia"
    MOLDOVA = "Moldova"
    MONACO = "Monaco"
    MONGOLIA = "Mongolia"
    MONTENEGRO = "Montenegro"
    MOROCCO = "Morocco"
    MOZAMBIQUE = "Mozambique"
    MYANMAR_BURMA = "Myanmar (Burma)"
    NAMIBIA = "Namibia"
    NAURU = "Nauru"
    NEPAL = "Nepal"
    NETHERLANDS = "Netherlands"
    NEW_ZEALAND = "New Zealand"
    NICARAGUA = "Nicaragua"
    NIGER = "Niger"
    NIGERIA = "Nigeria"
    NORTH_KOREA = "North Korea"
    NORTH_MACEDONIA = "North Macedonia"
    NORWAY = "Norway"
    OMAN = "Oman"
    PAKISTAN = "Pakistan"
    PALAU = "Palau"
    PALESTINE = "Palestine"
    PANAMA = "Panama"
    PAPUA_NEW_GUINEA = "Papua New Guinea"
    PARAGUAY = "Paraguay"
    PERU = "Peru"
    PHILIPPINES = "Philippines"
    POLAND = "Poland"
    PORTUGAL = "Portugal"
    QATAR = "Qatar"
    ROMANIA = "Romania"
    RUSSIA = "Russia"
    RWANDA = "Rwanda"
    SAINT_KITTS_AND_NEVIS = "Saint Kitts and Nevis"
    SAINT_LUCIA = "Saint Lucia"
    SAINT_VINCENT_AND_THE_GRENADINES = "Saint Vincent and the Grenadines"
    SAMOA = "Samoa"
    SAN_MARINO = "San Marino"
    SAO_TOME_AND_PRINCIPE = "Sao Tome and Principe"
    SAUDI_ARABIA = "Saudi Arabia"
    SENEGAL = "Senegal"
    SERBIA = "Serbia"
    SEYCHELLES = "Seychelles"
    SIERRA_LEONE = "Sierra Leone"
    SINGAPORE = "Singapore"
    SLOVAKIA = "Slovakia"
    SLOVENIA = "Slovenia"
    SOLOMON_ISLANDS = "Solomon Islands"
    SOMALIA = "Somalia"
    SOUTH_AFRICA = "South Africa"
    SOUTH_KOREA = "South Korea"
    SOUTH_SUDAN = "South Sudan"
    SPAIN = "Spain"
    SRI_LANKA = "Sri Lanka"
    SUDAN = "Sudan"
    SURINAME = "Suriname"
    SWEDEN = "Sweden"
    SWITZERLAND = "Switzerland"
    SYRIA = "Syria"
    TAIWAN = "Taiwan"
    TAJIKISTAN = "Tajikistan"
    TANZANIA = "Tanzania"
    THAILAND = "Thailand"
    TOGO = "Togo"
    TONGA = "Tonga"
    TRINIDAD_AND_TOBAGO = "Trinidad and Tobago"
    TUNISIA = "Tunisia"
    TURKEY = "Turkey"
    TURKMENISTAN = "Turkmenistan"
    TUVALU = "Tuvalu"
    UGANDA = "Uganda"
    UKRAINE = "Ukraine"
    UNITED_ARAB_EMIRATES_UAE = "United Arab Emirates (UAE)"
    UNITED_KINGDOM_UK = "United Kingdom (UK)"
    URUGUAY = "Uruguay"
    UZBEKISTAN = "Uzbekistan"
    VANUATU = "Vanuatu"
    VATICAN_CITY_HOLY_SEE = "Vatican City (Holy See)"
    VENEZUELA = "Venezuela"
    VIETNAM = "Vietnam"
    YEMEN = "Yemen"
    ZAMBIA = "Zambia"
    ZIMBABWE = "Zimbabwe"
    ALABAMA = "Alabama"
    ALASKA = "Alaska"
    ARIZONA = "Arizona"
    ARKANSAS = "Arkansas"
    CALIFORNIA = "California"
    COLORADO = "Colorado"
    CONNECTICUT = "Connecticut"
    DELAWARE = "Delaware"
    FLORIDA = "Florida"
    GEORGIA_US = "Georgia"
    HAWAII = "Hawaii"
    IDAHO = "Idaho"
    ILLINOIS = "Illinois"
    INDIANA = "Indiana"
    IOWA = "Iowa"
    KANSAS = "Kansas"
    KENTUCKY = "Kentucky"
    LOUISIANA = "Louisiana"
    MAINE = "Maine"
    MARYLAND = "Maryland"
    MASSACHUSETTS = "Massachusetts"
    MICHIGAN = "Michigan"
    MINNESOTA = "Minnesota"
    MISSISSIPPI = "Mississippi"
    MISSOURI = "Missouri"
    MONTANA = "Montana"
    NEBRASKA = "Nebraska"
    NEVADA = "Nevada"
    NEW_HAMPSHIRE = "New Hampshire"
    NEW_JERSEY = "New Jersey"
    NEW_MEXICO = "New Mexico"
    NEW_YORK = "New York"
    NORTH_CAROLINA = "North Carolina"
    NORTH_DAKOTA = "North Dakota"
    OHIO = "Ohio"
    OKLAHOMA = "Oklahoma"
    OREGON = "Oregon"
    PENNSYLVANIA = "Pennsylvania"
    RHODE_ISLAND = "Rhode Island"
    SOUTH_CAROLINA = "South Carolina"
    SOUTH_DAKOTA = "South Dakota"
    TENNESSEE = "Tennessee"
    TEXAS = "Texas"
    UTAH = "Utah"
    VERMONT = "Vermont"
    VIRGINIA = "Virginia"
    WASHINGTON = "Washington"
    WEST_VIRGINIA = "West Virginia"
    WISCONSIN = "Wisconsin"
    WYOMING = "Wyoming"


sectors_list = [sector.value for sector in Sectors]
stages_list = [stage.value for stage in Stages]
countries_list = [country.value for country in Countries]


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
        default=0, description="""The revenue the company plans
        to have in a year."""
    )
    EMPLOYEES: Optional[int] = Field(
        default=0,
        description="""The number of employees the company plans
        to have in a year.""",
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


class Departments(str, Enum):
    G_A = "G&A"
    R_D = "R&D"
    S_M = "S&M"
    COGS = "COGS"


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


class HiringDecreaseResponseSchema(BaseModel):
    positions: Optional[List[
        "HiringDecreaseResponseSchema.DecreasePosition"]] = Field(
        default=None,
        description="The positions to be removed.")

    class DecreasePosition(BaseModel):
        id: Optional[int] = Field(
            default=None,
            description="The ID of the employee to remove.")


class HiringUpdateSchema(HiringGenerateSchema):
    positions: Optional[List["PositionSchema.Positions"]] = Field(
        default=None,
        description="The positions to be updated.")


class PromptTypeSchema(Ai_utilsBase):
    """
    Schema for the input of hp_classifier
    """
    input: Optional[str] = Field(
        default=None,
        description="The input of the prompt.")


class ClassifierOptions(str, Enum):
    generate = "generate"
    decrease = "decrease"
    modify = "modify"
    expand = "expand"
    null = None


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


class SalaryGeneratorResponse(BaseModel):
    positions: List[
        "SalaryGeneratorResponse.PositionSalaryGeneratorResponse"] = Field(
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
