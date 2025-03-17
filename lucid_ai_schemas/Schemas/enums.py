import datetime
from enum import Enum
from enum import Enum as PythonEnum
from sqlalchemy import DateTime, ForeignKey, Boolean, Integer, String, Column
from sqlalchemy.orm import relationship
# from sympy import Integer
# from tables import Column


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


class SubscriptionType(str, Enum):
    monthly_and_yearly_subscription = "Monthly & Yearly Subscription"
    one_time_purchase = "One Time Purchase"
    monthly_subscription = "Monthly Subscription"
    yearly_subscription = "Yearly Subscription"


class ClassifierOptions(str, Enum):
    generate = "generate"
    decrease = "decrease"
    modify = "modify"
    expand = "expand"
    null = None


class Departments(str, Enum):
    G_A = "G&A"
    R_D = "R&D"
    S_M = "S&M"
    COGS = "COGS"


class GraphType(PythonEnum):
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


class CompanyStageEnum(str, Enum):
    IDEA_STAGE = "Idea Stage"
    SEED_STAGE = "Seed Stage"
    EARLY_STAGE = "Early Stage"
    GROWTH_STAGE = "Growth Stage"
    SERIES_A = "Series A"
    SERIES_B = "Series B"
    SERIES_C = "Series C"
    SERIES_D_PLUS = "Series D+"
    EXIT_STAGE = "Exit Stage"
    EMPTY = ""


class Graph(Base):
    __tablename__ = "graphs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)
    name = Column(String(255))
    type = Column(Enum(GraphType))
    is_forecast_vs_actuals = Column(Boolean)
    is_single_scenario = Column(Boolean)
    is_monthly = Column(Boolean)
    is_quarterly = Column(Boolean)
    is_annualy = Column(Boolean)
    is_culmutative = Column(Boolean, default=False)

    branch_id = Column(Integer, ForeignKey("branches.id"))
    branches = relationship("Branch", back_populates="graphs")

    dashboard_id = Column(Integer, ForeignKey("dashboard.id",
                                              ondelete="CASCADE"))
    dashboard = relationship("Dashboard", back_populates="graph")

    graph_options = relationship("GraphOptions",
                                 back_populates="graph",
                                 cascade="all, delete-orphan")

    graph_layout_data = relationship("GraphLayoutData",
                                     back_populates="graph",
                                     cascade="all, delete-orphan")

    data_groups = relationship("DataGroup",
                               back_populates="graph",
                               cascade="all, delete-orphan")

    graph_data_points = relationship("GraphDataPoint",
                                     back_populates="graph",
                                     cascade="all, delete-orphan")

    # template_id = Column(Integer, ForeignKey('templates.id'))
    # dashboard = relationship('Dashboard', back_populates='graphs')
    # template = relationship('Template', back_populates='graphs')
