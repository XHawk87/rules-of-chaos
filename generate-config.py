#!/usr/bin/env python3
import json
import os
import random
import re
from math import floor, copysign
from random import randint
from typing import List, Union, Tuple, TypeVar, Literal, Generic, Callable, \
    Dict, Generator, overload, Any

project_json = os.getenv('PROJECT_JSON')
game_json = os.getenv('GAME_JSON')
config_json = os.getenv('CONFIG_JSON')

# Type hints
T = TypeVar('T')


def as_tuple(*values: T) -> Tuple[T, ...]:
    return values


ListTOrEmpty = Union[List[T], Tuple]
ListOrEmpty = Union[List, Tuple]
K = TypeVar('K')
V = TypeVar('V')
DictOrEmpty = Union[Dict, Tuple]
DictKVOrEmpty = Union[Dict[K, V], Tuple]
IntOrUnlimited = Union[int, Literal["unlimited"]]

ValueFunc = Callable[[], int]

EffectType = Literal[
    "Action_Odds_Pct", "Action_Success_Actor_Move_Cost",
    "Action_Success_Target_Move_Cost", "Airlift", "Any_Government",
    "Attack_Bonus", "Bombard_Limit_Pct", "Border_Vision",
    "Building_Build_Cost_Pct", "Building_Buy_Cost_Pct",
    "Building_Saboteur_Resistant", "Capital_City", "Casus_Belli_Caught",
    "Casus_Belli_Complete", "Casus_Belli_Success", "City_Build_Slots",
    "City_Image", "City_Radius_Sq", "City_Unhappy_Size",
    "City_Vision_Radius_Sq", "Civil_War_Chance", "Combat_Rounds",
    "Conquest_Tech_Pct", "Defend_Bonus", "Empire_Size_Base",
    "Empire_Size_Step", "Enable_Nuke", "Enable_Space",
    "Enemy_Citizen_Unhappy_Pct", "Fanatics", "Force_Content",
    "Fortify_Defense_Bonus", "Gain_AI_Love", "Give_Imm_Tech", "Gov_Center",
    "Growth_Food", "Growth_Surplus_Pct", "HP_Regen", "HP_Regen_Min",
    "Happiness_To_Gold", "Has_Senate", "Have_Contacts", "Have_Embassies",
    "Health_Pct", "History", "Illegal_Action_HP_Cost",
    "Illegal_Action_Move_Cost", "Incite_Cost_Pct", "Infra_Points",
    "Inspire_Partisans", "Irrigation_Pct", "Make_Content", "Make_Content_Mil",
    "Make_Content_Mil_Per", "Make_Happy", "Maps_Stolen_Pct",
    "Martial_Law_Each", "Martial_Law_Max", "Max_Rates", "Max_Stolen_Gold_Pm",
    "Max_Trade_Routes", "Migration_Pct", "Mining_Pct", "Move_Bonus",
    "Nation_Intelligence", "National_History", "National_Performance",
    "No_Anarchy", "No_Diplomacy", "No_Unhappy", "Not_Tech_Source",
    "Nuke_Improvement_Pct", "Nuke_Infrastructure_Pct", "Nuke_Proof",
    "Output_Add_Tile", "Output_Bonus", "Output_Bonus_2", "Output_Inc_Tile",
    "Output_Inc_Tile_Celebrate", "Output_Penalty_Tile", "Output_Per_Tile",
    "Output_Tile_Punish_Pct", "Output_Waste", "Output_Waste_By_Distance",
    "Output_Waste_By_Rel_Distance", "Output_Waste_Pct", "Performance",
    "Pollu_Pop_Pct", "Pollu_Pop_Pct_2", "Pollu_Prod_Pct", "Pollu_Trade_Pct",
    "Rapture_Grow", "Retire_Pct", "Reveal_Cities", "Reveal_Map",
    "Revolution_Unhappiness", "SS_Component", "SS_Module", "SS_Structural",
    "Shield2Gold_Factor", "Size_Adj", "Size_Unlimit", "Slow_Down_Timeline",
    "Specialist_Output", "Spy_Resistant", "Stealings_Ignore",
    "Tech_Cost_Factor", "Tech_Parasite", "Tech_Upkeep_Free", "Thiefs_Share_Pm",
    "Tile_Workable", "Trade_Revenue_Bonus", "Trade_Revenue_Exponent",
    "Traderoute_Pct", "Turn_Fragments", "Turn_Years", "Unhappy_Factor",
    "Unit_Bribe_Cost_Pct", "Unit_Build_Cost_Pct", "Unit_Buy_Cost_Pct",
    "Unit_No_Lose_Pop", "Unit_Recover", "Unit_Shield_Value_Pct", "Unit_Slots",
    "Unit_Upkeep_Free_Per_City", "Unit_Vision_Radius_Sq", "Upgrade_Price_Pct",
    "Upgrade_Unit", "Upkeep_Factor", "Upkeep_Free", "Veteran_Build",
    "Veteran_Combat", "Victory", "Visible_Walls", "Wonder_Visible"
]

Building = Literal[
    "A.Smith's Trading Co.", "Academy", "Airport", "Amphitheater",
    "Apollo Program", "Aqueduct", "Aqueduct, Lake", "Aqueduct, River",
    "Atlantic Telegraph Company", "Bank", "Barracks II", "Barracks III",
    "Barracks", "Cathedral", "City Walls", "Coastal Defense", "Coinage",
    "Colosseum", "Colossus", "Copernicus' Observatory", "Courthouse",
    "Cure For Cancer", "Darwin's Voyage", "Eiffel Tower", "Factory",
    "Global Emission Union", "Granary", "Great Library", "Great Wall",
    "Hal Saflieni Hypogeum", "Hanging Gardens", "Harbor", "Harbour",
    "Hoover Dam", "Hydro Plant", "Internet", "Isaac Newton's College",
    "J.S. Bach's Cathedral", "King Richard's Crusade", "Leonardo's Workshop",
    "Library", "Lighthouse", "Magellan's Expedition", "Manhattan Project",
    "Marco Polo's Embassy", "Marketplace", "Mass Transit",
    "Mausoleum of Mausolos", "Mercantile Exchange", "Mfg. Plant",
    "Michelangelo's Chapel", "Nuclear Plant", "Occupation Government",
    "Offshore Platform", "Palace", "Police Station", "Port Facility",
    "Port of Guangzhou", "Power Plant", "Pyramids", "Recycling Center",
    "Research Lab", "SAM Battery", "SDI Defense I", "SDI Defense II",
    "SDI Defense III", "School of Baudhayana sutras", "Second Palace",
    "Sewer System", "Shakespeare's Theatre", "Solar Plant", "Space Component",
    "Space Module", "Space Structural", "Statue of Liberty", "Statue of Zeus",
    "Stock Exchange", "Sun Tzu's War Academy", "Super Highways", "Supermarket",
    "Temple of Artemis", "Temple", "Terracotta Army", "The Paris Agreement",
    "Trade Company", "United Nations", "University", "Verrocchio's Workshop",
    "Workshop"
]

BuildingGenus = Literal["GreatWonder", "Improvement", "SmallWonder", "Special"]

Wonder = Literal[
    "A.Smith's Trading Co.", "Apollo Program", "Atlantic Telegraph Company",
    "Colossus", "Copernicus' Observatory", "Cure For Cancer",
    "Darwin's Voyage", "Eiffel Tower", "Global Emission Union",
    "Great Library", "Great Wall", "Hal Saflieni Hypogeum", "Hanging Gardens",
    "Hoover Dam", "Internet", "Isaac Newton's College",
    "J.S. Bach's Cathedral", "King Richard's Crusade", "Leonardo's Workshop",
    "Lighthouse", "Magellan's Expedition", "Manhattan Project",
    "Marco Polo's Embassy", "Mausoleum of Mausolos", "Michelangelo's Chapel",
    "Palace", "Port of Guangzhou", "Pyramids", "School of Baudhayana sutras",
    "Second Palace", "Shakespeare's Theatre", "Statue of Liberty",
    "Statue of Zeus", "Sun Tzu's War Academy", "Temple of Artemis",
    "Terracotta Army", "The Paris Agreement", "Trade Company",
    "United Nations", "Verrocchio's Workshop"
]

Technology = Literal[
    "Advanced Engineering", "Advanced Espionage", "Advanced Flight",
    "Amphibious Warfare", "Astronomy", "Atomic Theory", "Automobile",
    "Aviation Endurance", "Banking", "Bridge Building", "Bronze Working",
    "Ceremonial Burial", "Chemistry", "Chivalry", "Code of Laws",
    "Combined Arms", "Combustion", "Communism", "Computers", "Conscription",
    "Construction", "Currency", "Democracy", "Economics", "Electricity",
    "Electronics", "Engineering", "Environmentalism", "Espionage",
    "Explosives", "Feudalism", "Flight", "Folklore", "Fusion Power",
    "Genetic Engineering", "Global Intergovernmentalism", "Guerilla Warfare",
    "Gunpowder", "Horseback Riding", "Industrialization",
    "Intergovernmentalism", "Invention", "Iron Working", "Labor Union",
    "Laser", "Leadership", "Literacy", "Machine Tools", "Magnetism",
    "Map Making", "Masonry", "Mass Production", "Mathematics", "Medicine",
    "Metallurgy", "Miniaturization", "Mobile Warfare", "Monarchy",
    "Monotheism", "Mysticism", "Navigation", "Nuclear Fission",
    "Nuclear Power", "Philosophy", "Physics", "Pictography", "Plastics",
    "Polytheism", "Pottery", "Radio", "Railroad", "Recycling", "Refining",
    "Refrigeration", "Robotics", "Rocketry", "Sanitation", "Seafaring",
    "Space Flight", "Stealth", "Steam Engine", "Steel", "Superconductors",
    "Tactics", "The Corporation", "The Republic", "The Wheel", "Theology",
    "Theory of Gravity", "Trade", "University", "Warrior Code", "Writing"
]

TechnologyFlag = Literal[
    "Bonus_Tech", "Bridge", "Build_Airborne", "Claim_Ocean",
    "Claim_Ocean_Limited"
]

GovernmentType = Literal[
    "Anarchy", "City States", "Communism", "Democracy", "Despotism",
    "Federation", "Fundamentalism", "Monarchy", "Republic", "Tribal"
]

AIDifficultyLevel = Literal[
    "Handicapped", "Novice", "Easy", "Normal", "Hard", "Cheating",
    "Experimental"
]

Terrain = Literal[
    "Deep Ocean", "Desert", "Forest", "Glacier", "Grassland", "Hills",
    "Jungle", "Lake", "Mountains", "Ocean", "Plains", "Swamp", "Tundra"
]

TerrainFlag = Literal[
    "CanHaveRiver", "FreshWater", "Frozen", "NoBarbs", "NoCities", "NoFortify",
    "NoPollution", "NoZoc", "NotGenerated", "Oil", "Sea", "Starter",
    "UnsafeCoast", "Unworkable"
]

TerrainClass = Literal["Land", "Oceanic"]

TerrainExtra = Literal[
    "Airbase", "Buffalo", "Buoy", "Coal", "Fallout", "Farmland", "Fish",
    "Fortress", "Fruit", "Furs", "Game", "Gems", "Gold", "Hut", "Iron",
    "Irrigation", "Ivory", "Maglev", "Mine", "Oasis", "Oil Platform",
    "Oil Well", "Oil", "Peat", "Pheasant", "Pollution", "Pre-Fortress",
    "Railroad", "Resources", "River", "Road", "Ruins", "Silk", "Spice",
    "Whales", "Wheat", "Wine"
]

TerrainExtraFlag = Literal[
    "AllowsFarmlandOnDesert", "AlwaysOnCityCenter", "AutoOnCityCenter",
    "ConnectLand", "GlobalWarming", "IrrigationSource", "NativeTile",
    "NaturalDefense", "NoStackDeath", "NuclearWinter", "ParadropFrom",
    "Refuel", "ShowFlag", "TerrChangeRemoves",
]

TerrainRoadExtra = Literal["Road", "Railroad", "Maglev", "River"]
TerrainBaseExtra = Literal["Pre-Fortress", "Fortress", "Airbase", "Buoy"]

TerrainAlteration = Literal[
    "Airbase", "Buoy", "Farmland", "Fortress", "Irrigation", "Maglev", "Mine",
    "Oil Platform", "Oil Well", "Pre-Fortress", "Railroad", "Road",
]

DisasterEffect = Literal[
    "DestroyBuilding", "EmptyFoodStock", "EmptyProdStock", "Fallout",
    "Pollution", "ReducePopDestroy", "ReducePopulation",
]

UnitClassFlag = Literal[
    "Air", "Airliftable", "AttFromNonNative", "AttackNonNative",
    "BuildAnywhere", "CanFortify", "CanOccupyCity", "CanPillage",
    "CollectRansom", "DamageSlows", "DoesntOccupyTile", "KillCitizen", "Land",
    "Missile", "Sea", "TerrainDefense", "TerrainSpeed", "Unreachable", "ZOC",
]

UnitState = Literal[
    "HasHomeCity", "InNativeExtra", "MovedThisTurn", "OnDomesticTile",
    "OnLivableTile", "OnNativeTile", "Transported", "Transporting",
]

UnitActivity = Literal[
    "Base", "Convert", "Cultivate", "Explore", "Fallout", "Fortified",
    "Fortifying", "Fortress", "Goto", "Idle", "Irrigate", "Mine", "Pillage",
    "Plant", "Pollution", "Road", "Sentry", "Transform",
]

VisionLayer = Literal["Main", "Stealth", "Subsurface"]

Action = Literal[
    "Airlift Unit", "Attack", "Bombard", "Bribe Unit", "Build Base",
    "Build Irrigation", "Build Mine", "Build Road", "Capture Units",
    "Clean Fallout", "Clean Pollution", "Conquer City 2", "Conquer City",
    "Cultivate", "Disband Unit", "Establish Embassy Stay", "Establish Embassy",
    "Establish Trade Route", "Explode Nuclear", "Fortify", "Found City",
    "Help Wonder", "Home City", "Incite City Escape", "Incite City",
    "Investigate City Spend Unit", "Investigate City", "Join City",
    "Paradrop Unit", "Pillage", "Plant", "Poison City Escape", "Recycle Unit",
    "Sabotage City Escape", "Sabotage City Production Escape", "Sabotage City",
    "Sabotage Unit Escape", "Steal Tech", "Suicide Attack",
    "Targeted Sabotage City Escape", "Transform Terrain", "Transport Alight",
    "Transport Board", "Transport Disembark 2", "Transport Disembark",
    "Transport Embark", "Transport Unload", "Upgrade Unit",
]

OutputType = Literal["Food", "Shield", "Trade", "Gold", "Luxury", "Science"]
Specialist = Literal["Elvis", "Scientist", "Taxman"]

DiplomaticRelationship = Literal[
    "Alliance", "Armistice", "Cease-fire", "Gives shared vision",
    "Has Casus Belli", "Has embassy", "Has real embassy", "Hosts embassy",
    "Hosts real embassy", "Is foreign", "Never met", "Peace",
    "Provided Casus Belli", "Receives shared vision", "Team", "War",
]
NationalIntelligence = Literal[
    "Culture", "Diplomacy", "Gold", "Government", "History", "Mood",
    "Multipliers", "Score", "Tax Rates", "Techs", "Wonders",
]

TradeGood = Literal["Goods"]

MapTopology = Literal["WrapX", "WrapY", "ISO", "Hex"]
ServerSetting = Literal[
    "autoattack", "ec_chat", "killstack", "migration", "multiresearch",
    "savepalace", "scorelog", "unitwaittime_extended",
]
Achievement = Literal[
    "Cultured City", "Cultured Nation", "Entire Map Known", "Land Ahoy",
    "Literate", "Metropolis", "Multicultural", "Spaceship Launch",
]

Nation = str
NationGroup = Literal[
    "African", "American", "Ancient", "Asian", "Barbarian", "Early Modern",
    "European", "Imaginary", "Medieval", "Modern", "Oceanian",
]
NationStyle = Literal[
    "European", "Classical", "Tropical", "Asian", "Babylonian", "Celtic"
]

CityTile = Literal["Center", "Claimed"]
CityStatus = Literal["OwnedByOriginal"]

UnitType = Literal[
    "AEGIS Cruiser", "AWACS", "Advanced Torpedo", "Air Defense Missile",
    "Alpine Troops", "Archers", "Armor", "Artillery", "Barbarian Leader",
    "Barge", "Battleship", "Bomber", "Cannon", "Caravan", "Caravel",
    "Cargo Aircraft", "Carrier", "Catapult", "Cavalry", "Chariot", "Cog",
    "Cruise Missile", "Cruiser", "Crusaders", "Destroyer", "Diplomat",
    "Dragoons", "Elephants", "Engineers", "Explorer", "Explosive Settlers",
    "Fanatics", "Fighter", "Flagship Frigate", "Freight", "Frigate",
    "Fusion Armor", "Fusion Battleship", "Fusion Bomber", "Fusion Fighter",
    "Galleon", "Helicopter", "Horsemen", "Howitzer", "Immigrants", "Infantry",
    "Intercontinental Missile", "Inventor", "Ironclad", "Knights", "Leader",
    "Longboat", "Marines", "Mech. Inf.", "Migrants", "Musketeers",
    "Navy Troops", "Nuclear Bomb", "Nuclear Submarine Type II",
    "Nuclear Submarine", "Nuclear", "Operative", "Paratroopers", "Partisan",
    "Patrol Cutter", "Phalanx", "Pikemen", "Pirogue", "Riflemen", "Scholar",
    "Scribe", "Settlers", "Spy", "Square-Rigged Caravel", "Stealth Bomber",
    "Stealth Fighter", "Submarine", "Swordsmen", "Transport", "Trebuchet",
    "Tribal Workers", "Trireme", "War Longboat", "Warriors", "Workers",
]

UnitFlag = Literal[
    "AddToCity", "AirAttacker", "Airbase", "BadCityDefender",
    "BadWallAttacker", "BarbarianOnly", "Bombarder", "CanEscape",
    "CanKillEscaping", "Cant_Fortify", "Capturable", "Capturer", "Cities",
    "CityBuster", "Coast", "CoastStrict", "Diplomat", "EvacuateFirst",
    "Fanatic", "FieldUnit", "GameLoss", "HasNoZOC", "HelpWonder", "Horse",
    "IgTer", "IgZOC", "Marines", "NeverProtects", "NewCityGamesOnly",
    "NoBuild", "NoHome", "NoVeteran", "NonMil", "Nuclear", "OneAttack",
    "OneEye", "Only_Native_Attack", "Paratroopers", "Provoking",
    "RealDiplomat", "RealSpy", "Settlers", "Shield2Gold", "Spy", "Submarine",
    "SuperSpy", "TradeRoute", "Transform", "Unbribable", "Unique",
]

UnitClass = Literal[
    "Air", "Amphibious", "Ancient Land", "Big Land", "Big Siege", "Deep Sea",
    "Helicopter", "Land", "Levitating", "Merchant", "Missile", "Nuclear",
    "Patrol", "Sea", "Small Land", "Small Sea", "Small Unit", "Trireme",
]

RequirementType = Literal[
    "AI", "Achievement", "Action", "Activity", "Age", "BaseFlag", "Building",
    "BuildingGenus", "CityStatus", "CityTile", "DiplRel", "Extra", "ExtraFlag",
    "Good", "Gov", "MaxUnitsOnTile", "MinCalFrag", "MinCulture",
    "MinForeignPct", "MinHitPoints", "MinMoveFrags", "MinSize", "MinTechs",
    "MinVeteran", "MinYear", "Nation", "NationGroup", "NationalIntelligence",
    "Nationality", "OutputType", "RoadFlag", "ServerSetting", "Specialist",
    "Style", "Tech", "TechFlag", "Terrain", "TerrainAlter", "TerrainClass",
    "TerrainFlag", "Topology", "UnitClass", "UnitClassFlag", "UnitFlag",
    "UnitState", "UnitType", "VisionLayer",
]

RequirementRange = Literal[
    "Adjacent", "Alliance", "CAdjacent", "City", "Continent", "Local",
    "Player", "Team", "Traderoute", "World",
]

ReqBuildingRange = Literal[
    "Alliance", "City", "Continent", "Local", "Player", "Team", "Traderoute",
    "World",
]
ReqMinCultureRange = Literal[
    "World", "Alliance", "Team", "Player", "Traderoute", "City"
]

ReqExtraRange = Literal[
    "Local", "Adjacent", "CAdjacent", "Traderoute", "City"
]
ReqBaseFlagRange = Literal[
    "Local", "Adjacent", "CAdjacent", "Traderoute", "City"
]
ReqRoadFlagRange = Literal[
    "Local", "Adjacent", "CAdjacent", "Traderoute", "City"
]
ReqExtraFlagRange = Literal[
    "Local", "Adjacent", "CAdjacent", "Traderoute", "City"
]
ReqTerrainRange = Literal[
    "Local", "Adjacent", "CAdjacent", "Traderoute", "City"
]
ReqTerrainClassRange = Literal[
    "Local", "Adjacent", "CAdjacent", "Traderoute", "City"
]
ReqTerrainFlagRange = Literal[
    "Local", "Adjacent", "CAdjacent", "Traderoute", "City"
]
ReqDiplRepRange = Literal["Player", "Team", "Alliance", "World", "Local"]
ReqTechRange = Literal["Player", "Team", "Alliance", "World"]
ReqTechFlagRange = Literal["Player", "Team", "Alliance", "World"]
ReqAchievementRange = Literal["Player", "Team", "Alliance", "World"]
ReqNationRange = Literal["Player", "Team", "Alliance", "World"]
ReqNationGroupRange = Literal["Player", "Team", "Alliance", "World"]
ReqMaxUnitsOnTileRange = Literal["Local", "Adjacent", "CAdjacent"]
ReqCityTileRange = Literal["Local", "Adjacent", "CAdjacent"]
ReqNationalityRange = Literal["Traderoute", "City"]
ReqMinSizeRange = Literal["Traderoute", "City"]
ReqMinForeignPctRange = Literal["Traderoute", "City"]
ReqCityStatusRange = Literal["Traderoute", "City"]
ReqMinTechsRange = Literal["Player", "World"]
ReqBuildingGenusRange = Literal["Local"]
ReqUnitTypeRange = Literal["Local"]
ReqUnitFlagRange = Literal["Local"]
ReqUnitClassRange = Literal["Local"]
ReqUnitClassFlagRange = Literal["Local"]
ReqActionRange = Literal["Local"]
ReqOutputTypeRange = Literal["Local"]
ReqSpecialistRange = Literal["Local"]
ReqAgeRange = Literal["Local", "City", "Player"]
ReqTerrainAlterRange = Literal["Local"]
ReqUnitStateRange = Literal["Local"]
ReqActivityRange = Literal["Local"]
ReqMinMoveFragsRange = Literal["Local"]
ReqMinVeteranRange = Literal["Local"]
ReqMinHitPointsRange = Literal["Local"]
ReqVisionLayerRange = Literal["Local"]
ReqNationalIntelligenceRange = Literal["Local"]
ReqGoodRange = Literal["City"]
ReqMinYearRange = Literal["World"]
ReqMinCalFragRange = Literal["World"]
ReqTopologyRange = Literal["World"]
ReqServerSettingRange = Literal["World"]
ReqGovRange = Literal["Player"]
ReqAIRange = Literal["Player"]
ReqStyleRange = Literal["Player"]


# Randomisation tools


def random_bool_pct(chance: int) -> int:
    return randint(1, 100) <= chance


class Choice(Generic[T]):
    def __init__(self, weight: int, value: T):
        self.weight = weight
        self.value = value


IntOrUnlimitedChoices = Union[Choice[Literal["unlimited"]], Choice[int]]


@overload
def weighted_random_possibilities(*choices: Choice[int]) -> int:
    ...


@overload
def weighted_random_possibilities(*choices: Choice[DictOrEmpty]) -> DictOrEmpty:
    ...


@overload
def weighted_random_possibilities(
        *choices: Choice[Callable[[], DictOrEmpty]]) -> Callable[
    [], DictOrEmpty]:
    ...


@overload
def weighted_random_possibilities(
        *choices: IntOrUnlimitedChoices) -> IntOrUnlimited:
    ...


@overload
def weighted_random_possibilities(*choices: Choice[T]) -> T:
    ...


def weighted_random_possibilities(*choices: Choice[T]) -> T:
    weights = [choice.weight for choice in choices]
    values = [choice.value for choice in choices]
    return random.choices(values, weights)


def possibility(weight: int, value: T) -> Choice[T]:
    return Choice(weight, value)


def stable_possibility(weight: int, value: T) -> Choice[T]:
    return Choice(stable() * weight, value)


def chaotic_possibility(weight: int, value: T) -> Choice[T]:
    return Choice(chaos * weight, value)


def stable(factor: float = 1.0) -> int:
    if factor >= 1.0:
        return round(100 - (chaos / factor))
    else:
        return round((100 - chaos) * factor)


def min_skewed_randint(min_int: int, max_int: int, skew: int = 1) -> int:
    if skew == 0:
        return randint(min_int, max_int)
    return randint(min_int, min_skewed_randint(min_int, max_int, skew - 1))


def max_skewed_randint(min_int: int, max_int: int, skew: int = 1) -> int:
    if skew == 0:
        return randint(min_int, max_int)
    return randint(max_skewed_randint(min_int, max_int, skew - 1), max_int)


def mid_skewed_randint(min_int: int, max_int: int, skew: int = 1) -> int:
    if skew == 0:
        return randint(min_int, max_int)
    mid_int = (min_int + max_int) // 2
    return mid_skewed_randint(
        randint(min_int, mid_int),
        randint(mid_int, max_int),
        skew - 1
    )


def random_multiplier_pct(min_pct: int, max_pct: int,
                          randfunc: Callable[
                              [int, int, int], int] = mid_skewed_randint,
                          skew: int = 0) -> int:
    min_divisor = max(100, 10000 // max_pct)
    max_divisor = max(100, 10000 // min_pct)
    min_multiplier = max(100, min_pct)
    max_multiplier = max(100, max_pct)
    qualified_min = (100 - max_divisor) if max_divisor > 100 else (
            min_multiplier - 100)
    qualified_max = (max_multiplier - 100) if max_multiplier > 100 else (
            100 - min_divisor)
    qualified_factor = randfunc(qualified_min, qualified_max, skew)
    if qualified_factor < 0:
        return 10000 // (100 - qualified_factor)
    else:
        return qualified_factor + 100


def load_json_config(json_file_name: str) -> Dict:
    with open(json_file_name, 'r') as json_file:
        return json.load(json_file)


def all_governments() -> List[GovernmentType]:
    return ["Anarchy", "Tribal", "Despotism", "Monarchy", "City States",
            "Communism", "Fundamentalism", "Federation", "Republic",
            "Democracy"]


def all_buildings() -> List[Building]:
    return ["Academy", "Airport", "Aqueduct", "Aqueduct, Lake",
            "Aqueduct, River", "Colosseum", "Occupation Government", "Bank",
            "Mercantile Exchange", "Barracks", "Barracks II", "Barracks III",
            "Cathedral", "City Walls", "Coastal Defense", "Amphitheater",
            "Courthouse", "Workshop", "Factory", "Granary", "Harbor",
            "Hydro Plant", "Library", "Marketplace", "Mass Transit",
            "Mfg. Plant", "Nuclear Plant", "Offshore Platform", "Palace",
            "Second Palace", "Police Station", "Port Facility", "Harbour",
            "Port of Guangzhou", "Power Plant", "Recycling Center",
            "Research Lab", "SAM Battery", "SDI Defense I", "SDI Defense II",
            "SDI Defense III", "Sewer System", "Solar Plant", "Space Component",
            "Space Module", "Space Structural", "Stock Exchange",
            "Super Highways", "Supermarket", "Temple", "University",
            "Apollo Program", "A.Smith's Trading Co.", "Colossus",
            "Copernicus' Observatory", "Cure For Cancer", "Darwin's Voyage",
            "Eiffel Tower", "Great Library", "Great Wall", "Hanging Gardens",
            "Hoover Dam", "Isaac Newton's College", "J.S. Bach's Cathedral",
            "King Richard's Crusade", "Leonardo's Workshop",
            "Verrocchio's Workshop", "Lighthouse", "Magellan's Expedition",
            "Manhattan Project", "Marco Polo's Embassy", "Trade Company",
            "Atlantic Telegraph Company", "The Paris Agreement",
            "Global Emission Union", "Michelangelo's Chapel",
            "Mausoleum of Mausolos", "Statue of Zeus", "Temple of Artemis",
            "Pyramids", "Internet", "Shakespeare's Theatre",
            "Sun Tzu's War Academy", "Terracotta Army", "United Nations",
            "School of Baudhayana sutras", "Hal Saflieni Hypogeum", "Coinage",
            "Statue of Liberty"]


def all_building_genuses() -> List[BuildingGenus]:
    return ["GreatWonder", "Improvement", "SmallWonder", "Special"]


def all_unit_types() -> List[UnitType]:
    return [
        "AEGIS Cruiser", "AWACS", "Advanced Torpedo", "Air Defense Missile",
        "Alpine Troops", "Archers", "Armor", "Artillery", "Barbarian Leader",
        "Barge", "Battleship", "Bomber", "Cannon", "Caravan", "Caravel",
        "Cargo Aircraft", "Carrier", "Catapult", "Cavalry", "Chariot", "Cog",
        "Cruise Missile", "Cruiser", "Crusaders", "Destroyer", "Diplomat",
        "Dragoons", "Elephants", "Engineers", "Explorer", "Explosive Settlers",
        "Fanatics", "Fighter", "Flagship Frigate", "Freight", "Frigate",
        "Fusion Armor", "Fusion Battleship", "Fusion Bomber", "Fusion Fighter",
        "Galleon", "Helicopter", "Horsemen", "Howitzer", "Immigrants",
        "Infantry", "Intercontinental Missile", "Inventor", "Ironclad",
        "Knights", "Leader", "Longboat", "Marines", "Mech. Inf.", "Migrants",
        "Musketeers", "Navy Troops", "Nuclear Bomb",
        "Nuclear Submarine Type II", "Nuclear Submarine", "Nuclear",
        "Operative", "Paratroopers", "Partisan", "Patrol Cutter", "Phalanx",
        "Pikemen", "Pirogue", "Riflemen", "Scholar", "Scribe", "Settlers",
        "Spy", "Square-Rigged Caravel", "Stealth Bomber", "Stealth Fighter",
        "Submarine", "Swordsmen", "Transport", "Trebuchet", "Tribal Workers",
        "Trireme", "War Longboat", "Warriors", "Workers",
    ]


def all_unit_classes() -> List[UnitClass]:
    return [
        "Air", "Amphibious", "Ancient Land", "Big Land", "Big Siege",
        "Deep Sea", "Helicopter", "Land", "Levitating", "Merchant", "Missile",
        "Nuclear", "Patrol", "Sea", "Small Land", "Small Sea", "Small Unit",
        "Trireme",
    ]


def all_unit_flags() -> List[UnitFlag]:
    return [
        "AddToCity", "AirAttacker", "Airbase", "BadCityDefender",
        "BadWallAttacker", "BarbarianOnly", "Bombarder", "CanEscape",
        "CanKillEscaping", "Cant_Fortify", "Capturable", "Capturer", "Cities",
        "CityBuster", "Coast", "CoastStrict", "Diplomat", "EvacuateFirst",
        "Fanatic", "FieldUnit", "GameLoss", "HasNoZOC", "HelpWonder", "Horse",
        "IgTer", "IgZOC", "Marines", "NeverProtects", "NewCityGamesOnly",
        "NoBuild", "NoHome", "NoVeteran", "NonMil", "Nuclear", "OneAttack",
        "OneEye", "Only_Native_Attack", "Paratroopers", "Provoking",
        "RealDiplomat", "RealSpy", "Settlers", "Shield2Gold", "Spy",
        "Submarine", "SuperSpy", "TradeRoute", "Transform", "Unbribable",
        "Unique",
    ]


def all_unit_class_flags() -> List[UnitClassFlag]:
    return [
        "Air", "Airliftable", "AttFromNonNative", "AttackNonNative",
        "BuildAnywhere", "CanFortify", "CanOccupyCity", "CanPillage",
        "CollectRansom", "DamageSlows", "DoesntOccupyTile", "KillCitizen",
        "Land", "Missile", "Sea", "TerrainDefense", "TerrainSpeed",
        "Unreachable", "ZOC",
    ]


def all_wonders() -> List[Wonder]:
    return ["Palace", "A.Smith's Trading Co.", "Apollo Program",
            "Atlantic Telegraph Company", "Colossus", "Copernicus' Observatory",
            "Cure For Cancer", "Darwin's Voyage", "Eiffel Tower",
            "Global Emission Union", "Great Library", "Great Wall",
            "Hal Saflieni Hypogeum", "Hanging Gardens", "Hoover Dam",
            "Internet", "Isaac Newton's College", "J.S. Bach's Cathedral",
            "King Richard's Crusade", "Leonardo's Workshop", "Lighthouse",
            "Magellan's Expedition", "Manhattan Project",
            "Marco Polo's Embassy", "Mausoleum of Mausolos",
            "Michelangelo's Chapel", "Port of Guangzhou", "Pyramids",
            "School of Baudhayana sutras", "Second Palace",
            "Shakespeare's Theatre", "Statue of Liberty", "Statue of Zeus",
            "Sun Tzu's War Academy", "Temple of Artemis", "Terracotta Army",
            "The Paris Agreement", "Trade Company", "United Nations",
            "Verrocchio's Workshop"]


def all_techs() -> List[Technology]:
    return ["Advanced Flight", "Pictography", "Folklore", "Amphibious Warfare",
            "Astronomy", "Atomic Theory", "Automobile", "Banking",
            "Bridge Building", "Bronze Working", "Ceremonial Burial",
            "Chemistry", "Chivalry", "Code of Laws", "Combined Arms",
            "Combustion", "Communism", "Computers", "Conscription",
            "Construction", "Currency", "Democracy", "Economics", "Electricity",
            "Electronics", "Engineering", "Environmentalism", "Espionage",
            "Intergovernmentalism", "Global Intergovernmentalism", "Explosives",
            "Feudalism", "Flight", "Fusion Power", "Advanced Espionage",
            "Aviation Endurance", "Genetic Engineering", "Guerilla Warfare",
            "Gunpowder", "Horseback Riding", "Industrialization", "Invention",
            "Iron Working", "Labor Union", "Laser", "Leadership", "Literacy",
            "Machine Tools", "Magnetism", "Map Making", "Masonry",
            "Mass Production", "Mathematics", "Medicine", "Metallurgy",
            "Miniaturization", "Mobile Warfare", "Monarchy", "Monotheism",
            "Mysticism", "Navigation", "Nuclear Fission", "Nuclear Power",
            "Philosophy", "Physics", "Plastics", "Polytheism", "Pottery",
            "Radio", "Railroad", "Recycling", "Refining", "Refrigeration",
            "Robotics", "Rocketry", "Sanitation", "Seafaring", "Space Flight",
            "Stealth", "Advanced Engineering", "Steam Engine", "Steel",
            "Superconductors", "Tactics", "The Corporation", "The Republic",
            "The Wheel", "Theology", "Theory of Gravity", "Trade", "University",
            "Warrior Code", "Writing"]


def all_terrain() -> List[Terrain]:
    return ["Lake", "Ocean", "Deep Ocean", "Glacier", "Desert", "Forest",
            "Grassland", "Hills", "Jungle", "Mountains", "Plains", "Swamp",
            "Tundra"]


def all_extras() -> List[TerrainExtra]:
    return ["Irrigation", "Mine", "Oil Well", "Oil Platform", "Pollution",
            "Hut", "Farmland", "Fallout", "Pre-Fortress",
            "Fortress", "Airbase", "Buoy", "Ruins", "Road", "Railroad",
            "Maglev", "River", "Gold", "Iron", "Game", "Furs",
            "Coal", "Fish", "Fruit", "Gems", "Buffalo", "Wheat", "Oasis",
            "Peat", "Pheasant", "Resources", "Ivory", "Silk", "Spice",
            "Whales", "Wine", "Oil"]


def all_aqueducts() -> List[Building]:
    return ["Aqueduct", "Aqueduct, Lake", "Aqueduct, River"]


def all_barracks() -> List[Building]:
    return ["Barracks", "Barracks II", "Barracks III"]


def all_palaces() -> List[Building]:
    return ["Palace", "Second Palace"]


def unit_class_theatre_flags() -> List[UnitClassFlag]:
    return ["Air", "Land", "Sea", "Missile"]


def disaster_effects() -> List[DisasterEffect]:
    return ["DestroyBuilding", "ReducePopulation", "EmptyFoodStock",
            "EmptyProdStock", "Pollution", "Fallout", "ReducePopDestroy"]


def random_pct_of_buildings(pct: int) -> Generator[Building]:
    return (building for building in all_buildings() if random_bool_pct(pct))


def random_pct_of_building_genuses(pct: int) -> Generator[BuildingGenus]:
    return (genus for genus in all_building_genuses() if random_bool_pct(pct))


def random_pct_of_units(pct: int) -> Generator[UnitType]:
    return (unit for unit in all_unit_types() if random_bool_pct(pct))


def random_pct_of_unit_classes(pct: int) -> Generator[UnitClass]:
    return (unit for unit in all_unit_classes() if random_bool_pct(pct))


def random_pct_of_unit_flags(pct: int) -> Generator[UnitFlag]:
    return (unit for unit in all_unit_flags() if random_bool_pct(pct))


def random_pct_of_unit_class_flags(pct: int) -> Generator[UnitClassFlag]:
    return (unit for unit in all_unit_class_flags() if random_bool_pct(pct))


def random_pct_of_wonders(pct: int) -> Generator[Wonder]:
    return (x for x in all_wonders() if random_bool_pct(pct))


def random_pct_of_techs(pct: int) -> Generator[Technology]:
    return (x for x in all_techs() if random_bool_pct(pct))


def random_pct_of_govs(pct: int) -> Generator[GovernmentType]:
    return (x for x in all_governments() if random_bool_pct(pct))


def random_pct_of_extras(pct: int) -> Generator[TerrainExtra]:
    return (x for x in all_extras() if random_bool_pct(pct))


def random_pct_of_terrain(pct: int) -> Generator[Terrain]:
    return (x for x in all_terrain() if random_bool_pct(pct))


def random_pct_of_buildings_and_extras(pct: int) -> Generator[
    (Building, TerrainExtra)]:
    return (building, extra
            for building in all_buildings() if random_bool_pct(pct)
            for extra in all_extras())


def random_pct_of_wonders_and_extras(pct: int) -> Generator[
    (Wonder, TerrainExtra)]:
    return (wonder, extra
            for wonder in all_wonders() if random_bool_pct(pct)
            for extra in all_extras())


def random_pct_of_techs_and_extras(pct: int) -> Generator[
    (Technology, TerrainExtra)]:
    return (tech, extra
            for tech in all_techs() if random_bool_pct(pct)
            for extra in all_extras())


def random_pct_of_govs_and_extras(pct: int) -> Generator[
    (GovernmentType, TerrainExtra)]:
    return (gov, extra
            for gov in all_governments() if random_bool_pct(pct)
            for extra in all_extras())


def random_pct_of_buildings_and_terrain(pct: int) -> Generator[
    (Building, Terrain)]:
    return (building, terrain
            for building in all_buildings() if random_bool_pct(pct)
            for terrain in all_terrain())


def random_pct_of_wonders_and_terrain(pct: int) -> Generator[
    (Wonder, Terrain)]:
    return (wonder, terrain
            for wonder in all_wonders() if random_bool_pct(pct)
            for terrain in all_terrain())


def random_pct_of_techs_and_terrain(pct: int) -> Generator[
    (Technology, Terrain)]:
    return (tech, terrain
            for tech in all_techs() if random_bool_pct(pct)
            for terrain in all_terrain())


def random_pct_of_govs_and_terrain(pct: int) -> Generator[
    (GovernmentType, Terrain)]:
    return (gov, terrain
            for gov in all_governments() if random_bool_pct(pct)
            for terrain in all_terrain())


class Requirement:
    @overload
    def __init__(
            self, rtype: Literal["Building"], name: Building,
            rrange: ReqBuildingRange,
            present: bool = None, survives: bool = None, quiet: bool = None):
        ...

    @overload
    def __init__(
            self, rtype: Literal["MinCulture"], name: int,
            rrange: ReqMinCultureRange,
            present: bool = None, survives: bool = None, quiet: bool = None):
        ...

    @overload
    def __init__(
            self, rtype: Literal["Extra"], name: TerrainExtra,
            rrange: ReqExtraRange,
            present: bool = None, survives: bool = None, quiet: bool = None):
        ...

    @overload
    def __init__(
            self, rtype: Literal["BaseFlag"], name: TerrainBaseExtra,
            rrange: ReqBaseFlagRange,
            present: bool = None, survives: bool = None, quiet: bool = None):
        ...

    @overload
    def __init__(
            self, rtype: Literal["RoadFlag"], name: TerrainRoadExtra,
            rrange: ReqRoadFlagRange,
            present: bool = None, survives: bool = None, quiet: bool = None):
        ...

    @overload
    def __init__(
            self, rtype: Literal["ExtraFlag"], name: TerrainExtraFlag,
            rrange: ReqExtraFlagRange,
            present: bool = None, survives: bool = None, quiet: bool = None):
        ...

    @overload
    def __init__(
            self, rtype: Literal["Terrain"], name: Terrain,
            rrange: ReqTerrainRange,
            present: bool = None, survives: bool = None, quiet: bool = None):
        ...

    @overload
    def __init__(
            self, rtype: Literal["TerrainClass"], name: TerrainClass,
            rrange: ReqTerrainClassRange,
            present: bool = None, survives: bool = None, quiet: bool = None):
        ...

    @overload
    def __init__(
            self, rtype: Literal["TerrainFlag"], name: TerrainFlag,
            rrange: ReqTerrainFlagRange,
            present: bool = None, survives: bool = None, quiet: bool = None):
        ...

    @overload
    def __init__(
            self, rtype: Literal["DiplRep"], name: DiplomaticRelationship,
            rrange: ReqDiplRepRange,
            present: bool = None, survives: bool = None, quiet: bool = None):
        ...

    @overload
    def __init__(
            self, rtype: Literal["Tech"], name: Technology,
            rrange: ReqTechRange,
            present: bool = None, survives: bool = None, quiet: bool = None):
        ...

    @overload
    def __init__(
            self, rtype: Literal["TechFlag"], name: TechnologyFlag,
            rrange: ReqTechFlagRange,
            present: bool = None, survives: bool = None, quiet: bool = None):
        ...

    @overload
    def __init__(
            self, rtype: Literal["Achievement"], name: Achievement,
            rrange: ReqAchievementRange,
            present: bool = None, survives: bool = None, quiet: bool = None):
        ...

    @overload
    def __init__(
            self, rtype: Literal["Nation"], name: Nation,
            rrange: ReqNationRange,
            present: bool = None, survives: bool = None, quiet: bool = None):
        ...

    @overload
    def __init__(
            self, rtype: Literal["NationGroup"], name: NationGroup,
            rrange: ReqNationGroupRange,
            present: bool = None, survives: bool = None, quiet: bool = None):
        ...

    @overload
    def __init__(
            self, rtype: Literal["MaxUnitsOnTile"], name: int,
            rrange: ReqMaxUnitsOnTileRange,
            present: bool = None, survives: bool = None, quiet: bool = None):
        ...

    @overload
    def __init__(
            self, rtype: Literal["CityTile"], name: CityTile,
            rrange: ReqCityTileRange,
            present: bool = None, survives: bool = None, quiet: bool = None):
        ...

    @overload
    def __init__(
            self, rtype: Literal["Nationality"], name: Nation,
            rrange: ReqNationalityRange,
            present: bool = None, survives: bool = None, quiet: bool = None):
        ...

    @overload
    def __init__(
            self, rtype: Literal["MinSize"], name: int,
            rrange: ReqMinSizeRange,
            present: bool = None, survives: bool = None, quiet: bool = None):
        ...

    @overload
    def __init__(
            self, rtype: Literal["MinForeignPct"], name: int,
            rrange: ReqMinForeignPctRange,
            present: bool = None, survives: bool = None, quiet: bool = None):
        ...

    @overload
    def __init__(
            self, rtype: Literal["CityStatus"], name: CityStatus,
            rrange: ReqCityStatusRange,
            present: bool = None, survives: bool = None, quiet: bool = None):
        ...

    @overload
    def __init__(
            self, rtype: Literal["MinTechs"], name: int,
            rrange: ReqMinTechsRange,
            present: bool = None, survives: bool = None, quiet: bool = None):
        ...

    @overload
    def __init__(
            self, rtype: Literal["BuildingGenus"], name: BuildingGenus,
            rrange: ReqBuildingGenusRange,
            present: bool = None, survives: bool = None, quiet: bool = None):
        ...

    @overload
    def __init__(
            self, rtype: Literal["UnitType"], name: UnitType,
            rrange: ReqUnitTypeRange,
            present: bool = None, survives: bool = None, quiet: bool = None):
        ...

    @overload
    def __init__(
            self, rtype: Literal["UnitFlag"], name: UnitFlag,
            rrange: ReqUnitFlagRange,
            present: bool = None, survives: bool = None, quiet: bool = None):
        ...

    @overload
    def __init__(
            self, rtype: Literal["UnitClass"], name: UnitClass,
            rrange: ReqUnitClassRange,
            present: bool = None, survives: bool = None, quiet: bool = None):
        ...

    @overload
    def __init__(
            self, rtype: Literal["UnitClassFlag"], name: UnitClassFlag,
            rrange: ReqUnitClassFlagRange,
            present: bool = None, survives: bool = None, quiet: bool = None):
        ...

    @overload
    def __init__(
            self, rtype: Literal["Action"], name: Action,
            rrange: ReqActionRange,
            present: bool = None, survives: bool = None, quiet: bool = None):
        ...

    @overload
    def __init__(
            self, rtype: Literal["OutputType"], name: OutputType,
            rrange: ReqOutputTypeRange,
            present: bool = None, survives: bool = None, quiet: bool = None):
        ...

    @overload
    def __init__(
            self, rtype: Literal["Specialist"], name: Specialist,
            rrange: ReqSpecialistRange,
            present: bool = None, survives: bool = None, quiet: bool = None):
        ...

    @overload
    def __init__(
            self, rtype: Literal["Age"], name: int,
            rrange: ReqAgeRange,
            present: bool = None, survives: bool = None, quiet: bool = None):
        ...

    @overload
    def __init__(
            self, rtype: Literal["TerrainAlter"], name: TerrainAlteration,
            rrange: ReqTerrainAlterRange,
            present: bool = None, survives: bool = None, quiet: bool = None):
        ...

    @overload
    def __init__(
            self, rtype: Literal["UnitState"], name: UnitState,
            rrange: ReqUnitStateRange,
            present: bool = None, survives: bool = None, quiet: bool = None):
        ...

    @overload
    def __init__(
            self, rtype: Literal["Activity"], name: UnitActivity,
            rrange: ReqActivityRange,
            present: bool = None, survives: bool = None, quiet: bool = None):
        ...

    @overload
    def __init__(
            self, rtype: Literal["MinMoveFrags"], name: int,
            rrange: ReqMinMoveFragsRange,
            present: bool = None, survives: bool = None, quiet: bool = None):
        ...

    @overload
    def __init__(
            self, rtype: Literal["MinVeteran"], name: int,
            rrange: ReqMinVeteranRange,
            present: bool = None, survives: bool = None, quiet: bool = None):
        ...

    @overload
    def __init__(
            self, rtype: Literal["MinHitPoints"], name: int,
            rrange: ReqMinHitPointsRange,
            present: bool = None, survives: bool = None, quiet: bool = None):
        ...

    @overload
    def __init__(
            self, rtype: Literal["VisionLayer"], name: VisionLayer,
            rrange: ReqVisionLayerRange,
            present: bool = None, survives: bool = None, quiet: bool = None):
        ...

    @overload
    def __init__(
            self, rtype: Literal["NationalIntelligence"],
            name: NationalIntelligence,
            rrange: ReqNationalIntelligenceRange,
            present: bool = None, survives: bool = None, quiet: bool = None):
        ...

    @overload
    def __init__(
            self, rtype: Literal["Good"], name: TradeGood,
            rrange: ReqGoodRange,
            present: bool = None, survives: bool = None, quiet: bool = None):
        ...

    @overload
    def __init__(
            self, rtype: Literal["MinYear"], name: int,
            rrange: ReqMinYearRange,
            present: bool = None, survives: bool = None, quiet: bool = None):
        ...

    @overload
    def __init__(
            self, rtype: Literal["MinCalFrag"], name: int,
            rrange: ReqMinCalFragRange,
            present: bool = None, survives: bool = None, quiet: bool = None):
        ...

    @overload
    def __init__(
            self, rtype: Literal["Topology"], name: MapTopology,
            rrange: ReqTopologyRange,
            present: bool = None, survives: bool = None, quiet: bool = None):
        ...

    @overload
    def __init__(
            self, rtype: Literal["ServerSetting"], name: ServerSetting,
            rrange: ReqServerSettingRange,
            present: bool = None, survives: bool = None, quiet: bool = None):
        ...

    @overload
    def __init__(
            self, rtype: Literal["Gov"], name: GovernmentType,
            rrange: ReqGovRange,
            present: bool = None, survives: bool = None, quiet: bool = None):
        ...

    @overload
    def __init__(
            self, rtype: Literal["AI"], name: AIDifficultyLevel,
            rrange: ReqAIRange,
            present: bool = None, survives: bool = None, quiet: bool = None):
        ...

    @overload
    def __init__(
            self, rtype: Literal["Style"], name: NationStyle,
            rrange: ReqStyleRange,
            present: bool = None, survives: bool = None, quiet: bool = None):
        ...

    def __init__(self, rtype: RequirementType,
                 name: Any,
                 rrange: RequirementRange,
                 present: bool = None,
                 survives: bool = None,
                 quiet: bool = None):
        self.type = rtype
        self.name = name
        self.range = rrange
        if present is not None:
            self.present = present
        if survives is not None:
            self.survives = survives
        if quiet is not None:
            self.quiet = quiet

    def negate(self) -> "Requirement":
        # noinspection PyArgumentList
        # It's a copy so it must be correct
        return Requirement(
            rtype=self.type,
            name=self.name,
            range=self.range,
            present=(not self.present),
            survives=self.survives,
            quiet=self.quiet
        )

    @classmethod
    def building(cls, building: Building) -> list["Requirement"]:
        return [cls("Building", building, "City")]

    @classmethod
    def unit_type(cls, unit_type: UnitType) -> list["Requirement"]:
        return [cls("UnitType", unit_type, "Local")]

    @classmethod
    def unit_class(cls, unit_class: UnitClass) -> list["Requirement"]:
        return [cls("UnitClass", unit_class, "Local")]

    @classmethod
    def unit_flag(cls, unit_flag: UnitFlag) -> list["Requirement"]:
        return [cls("UnitFlag", unit_flag, "Local")]

    @classmethod
    def buildings(cls, building_list: List[Building]) -> list["Requirement"]:
        return [req_list[0] for req_list in (cls.building(building)
                                             for building in building_list)]

    @classmethod
    def exclude_building(cls, building: Building) -> list["Requirement"]:
        return [cls("Building", building, "City", present=False)]

    @classmethod
    def exclude_gov(cls, gov: GovernmentType) -> list["Requirement"]:
        return [cls("Gov", gov, "Player", present=False)]

    @classmethod
    def exclude_govs(cls, gov_list: List[GovernmentType]) -> list[
        "Requirement"]:
        return [req_list[0] for req_list in (cls.exclude_gov(gov)
                                             for gov in gov_list)]

    @classmethod
    def wonder(cls, wonder: Wonder) -> list["Requirement"]:
        return [cls("Building", wonder, "Player")]

    @classmethod
    def wonder_worldwide(cls, wonder: Wonder) -> list["Requirement"]:
        return [cls("Building", wonder, "World")]

    @classmethod
    def not_wonder_worldwide(cls, wonder: Wonder) -> list["Requirement"]:
        return [cls("Building", wonder, "World", present=False)]

    @classmethod
    def after_wonder(cls, wonder: Wonder) -> list["Requirement"]:
        return [cls("Building", wonder, "Player", survives=True)]

    @classmethod
    def after_wonder_worldwide(cls, wonder: Wonder) -> list["Requirement"]:
        return [cls("Building", wonder, "World", survives=True)]

    @classmethod
    def tech(cls, tech: Technology) -> list["Requirement"]:
        return [cls("Tech", tech, "Player")]

    @classmethod
    def not_tech(cls, tech: Technology) -> list["Requirement"]:
        return [cls("Tech", tech, "Player", present=False)]

    @classmethod
    def gov(cls, gov: GovernmentType) -> list["Requirement"]:
        return [cls("Gov", gov, "Player")]

    @classmethod
    def not_gov(cls, gov: GovernmentType) -> list["Requirement"]:
        return [cls("Gov", gov, "Player", present=False)]

    @classmethod
    def on_city(cls) -> list["Requirement"]:
        return [cls("CityTile", "Center", "Local")]

    @classmethod
    def not_on_city(cls) -> list["Requirement"]:
        return [cls("CityTile", "Center", "Local", present=False)]

    @classmethod
    def min_size(cls, size: int) -> list["Requirement"]:
        return [cls("MinSize", size, "City")]

    @classmethod
    def max_size(cls, size: int) -> list["Requirement"]:
        return [cls("MinSize", size + 1, "City", present=False)]

    @classmethod
    def unit_class_flag(cls, unit_class_flag: UnitClassFlag) -> list[
        "Requirement"]:
        return [cls("UnitClassFlag", unit_class_flag, "Local")]

    @classmethod
    def on_terrain(cls, terrain: Terrain) -> list["Requirement"]:
        return [cls("Terrain", terrain, "Local")]

    @classmethod
    def not_on_terrain(cls, terrain: Terrain) -> list["Requirement"]:
        return [cls("Terrain", terrain, "Local", present=False)]

    @classmethod
    def on_land(cls) -> list["Requirement"]:
        return [cls("TerrainClass", "Land", "Local")]

    @classmethod
    def at_sea(cls) -> list["Requirement"]:
        return [cls("TerrainClass", "Oceanic", "Local")]

    @classmethod
    def on_irrigatable_terrain(cls) -> list["Requirement"]:
        return [cls("TerrainAlter", "Irrigation", "Local")]

    @classmethod
    def on_terrain_with_flag(cls, terrain_flag: TerrainFlag) -> list[
        "Requirement"]:
        return [cls("TerrainFlag", terrain_flag, "Local")]

    @classmethod
    def on_extra(cls, extra: TerrainExtra) -> list["Requirement"]:
        return [cls("Extra", extra, "Local")]

    @classmethod
    def not_on_extra(cls, extra: TerrainExtra) -> list["Requirement"]:
        return [cls("Extra", extra, "Local", present=False)]

    @classmethod
    def adjacent_extra(cls, extra: TerrainExtra) -> list["Requirement"]:
        return [cls("Extra", extra, "Adjacent")]

    @classmethod
    def negated(cls, *reqs: "Requirement") -> list["Requirement"]:
        return [req.negate() for req in reqs]

    @classmethod
    def specialist(cls, specialist: Specialist) -> list["Requirement"]:
        return [cls("Specialist", specialist, "Local")]

    @classmethod
    def output_type(cls, output_type: OutputType) -> list["Requirement"]:
        return [cls("OutputType", output_type, "Local")]

    @classmethod
    def luxuries(cls) -> list["Requirement"]:
        return cls.output_type("Luxury")

    @classmethod
    def tech_worldwide(cls, tech: Technology) -> list["Requirement"]:
        return [cls("Tech", tech, "World")]

    @classmethod
    def not_barbarian(cls) -> list["Requirement"]:
        return [cls("NationGroup", "Barbarian", "Player", present=False)]

    @classmethod
    def food(cls) -> list["Requirement"]:
        return cls.output_type("Food")

    @classmethod
    def on_city_auto_irrigation(cls) -> list["Requirement"]:
        return (cls.on_city() +
                cls.on_irrigatable_terrain() +
                cls.not_on_extra("Irrigation") +
                cls.not_on_extra("Mine"))

    @classmethod
    def building_genus(cls, building_genus: BuildingGenus) -> list[
        "Requirement"]:
        return [cls("BuildingGenus", building_genus, "Local")]


r = Requirement


def evaluate_once(func):
    cache = {}

    def wrapper(*args):
        if args not in cache:
            cache[args] = func(args)
        return cache[args]

    return wrapper


@evaluate_once
def rule_effects() -> Dict:
    return {}


class Effect:
    def __init__(self, name: str, value: int, reqs: ListTOrEmpty[Requirement]):
        self.name = name
        self.value = value
        self.reqs = reqs


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)  # Remove special characters
    text = re.sub(r'\s+', '_', text)  # Replace whitespace with underscores
    return text


class EffectGroup:
    def __init__(self, etype: EffectType,
                 prefix: str = None,
                 reqs: ListTOrEmpty[Requirement] = (),
                 children: ListTOrEmpty["EffectGroup"] = ()):
        self.etype = etype
        self.prefix = prefix if prefix else slugify(etype)
        self.reqs = reqs
        self.children = children or []

    def add_children(self, children: ListTOrEmpty["EffectGroup"]):
        self.children += children

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def add_effect(self, effect: Effect) -> None:
        self._add_effect(effect.name, effect.value, effect.reqs)

    def _add_effect(self, name: str, value: int,
                    reqs: ListTOrEmpty[Requirement]) -> None:
        if self.children:
            for g in self.children:
                g._add_effect(name, value, reqs)
        else:
            rule_effects()[f"{self.prefix}_{name}"] = {
                "type": self.etype,
                "reqs": reqs + self.reqs,
                "value": value
            }

    def maybe_add_effect(self, pct: int, effect: Effect) -> None:
        if random_bool_pct(pct):
            self.add_effect(effect)

    def base_effect(self, value: int = 1) -> None:
        self._add_effect("base", value, ())

    def with_building(self, building: Building, value: int = 1) -> None:
        self._add_effect(f"building_{slugify(building)}", value,
                         r.building(building))

    def with_unit_type(self, unit_type: UnitType, value: int = 1) -> None:
        self._add_effect(f"unit_{slugify(unit_type)}", value,
                         r.unit_type(unit_type))

    def with_unit_class(self, unit_class: UnitClass, value: int = 1) -> None:
        self._add_effect(f"unit_class_{slugify(unit_class)}", value,
                         r.unit_class(unit_class))

    def with_unit_flag(self, unit_flag: UnitFlag, value: int = 1) -> None:
        self._add_effect(f"unit_flag_{slugify(unit_flag)}", value,
                         r.unit_flag(unit_flag))

    def with_building_excluding_building(self, building: Building,
                                         excluded_building: Building,
                                         value: int = 1) -> None:
        self._add_effect(
            f"building_{slugify(building)}"
            f"_excluding_building_{slugify(excluded_building)}",
            value,
            r.building(building) + r.exclude_building(excluded_building))

    def with_building_on_extra(self, building: Building, extra: TerrainExtra,
                               value: int = 1) -> None:
        self._add_effect(f"building_{slugify(building)}"
                         f"_on_extra_{slugify(extra)}", value,
                         r.building(building) + r.on_extra(extra))

    def with_wonder_on_extra(self, wonder: Wonder, extra: TerrainExtra,
                             value: int = 1) -> None:
        self._add_effect(f"wonder_{slugify(wonder)}"
                         f"_on_extra_{slugify(extra)}", value,
                         r.wonder(wonder) + r.on_extra(extra))

    def with_tech_on_extra(self, tech: Technology, extra: TerrainExtra,
                           value: int = 1) -> None:
        self._add_effect(f"tech_{slugify(tech)}"
                         f"_on_extra_{slugify(extra)}", value,
                         r.tech(tech) + r.on_extra(extra))

    def with_gov_on_extra(self, gov: GovernmentType, extra: TerrainExtra,
                          value: int = 1) -> None:
        self._add_effect(f"gov_{slugify(gov)}"
                         f"_on_extra_{slugify(extra)}", value,
                         r.gov(gov) + r.on_extra(extra))

    def with_building_on_terrain(self, building: Building, terrain: Terrain,
                                 value: int = 1) -> None:
        self._add_effect(f"building_{slugify(building)}"
                         f"_on_terrain_{slugify(terrain)}",
                         value,
                         r.building(building) + r.on_terrain(terrain))

    def with_wonder_on_terrain(self, wonder: Wonder, terrain: Terrain,
                               value: int = 1) -> None:
        self._add_effect(
            f"wonder_{slugify(wonder)}_on_terrain_{slugify(terrain)}", value,
            r.wonder(wonder) + r.on_terrain(terrain))

    def with_tech_on_terrain(self, tech: Technology, terrain: Terrain,
                             value: int = 1) -> None:
        self._add_effect(f"tech_{slugify(tech)}_on_terrain_{slugify(terrain)}",
                         value,
                         r.tech(tech) + r.on_terrain(terrain))

    def with_gov_on_terrain(self, gov: GovernmentType, terrain: Terrain,
                            value: int = 1) -> None:
        self._add_effect(f"gov_{slugify(gov)}_on_terrain_{slugify(terrain)}",
                         value,
                         r.gov(gov) + r.on_terrain(terrain))

    def with_building_on_terrain_with_flag(self, building: Building,
                                           terrain_flag: TerrainFlag,
                                           value: int = 1) -> None:
        self._add_effect(
            f"building_{slugify(building)}_terrain_flag_{slugify(terrain_flag)}",
            value,
            r.building(building)
            + r.on_terrain_with_flag(terrain_flag)
        )

    def with_buildings(self, building_list: List[Building],
                       value: int = 1) -> None:
        buildings = "_".join(building_list)
        self._add_effect(f"buildings_{slugify(buildings)}", value,
                         r.buildings(building_list))

    def without_building(self, building: Building, value: int = 1) -> None:
        self._add_effect(f"sans_building_{slugify(building)}", value,
                         r.exclude_building(building))

    def excluding_gov(self, gov: GovernmentType, value: int = 1) -> None:
        self._add_effect(f"sans_gov_{slugify(gov)}", value, r.exclude_gov(gov))

    def excluding_govs(self, gov_list: List[GovernmentType],
                       value: int = 1) -> None:
        govs = "_".join(gov_list)
        self._add_effect(f"sans_govs_{slugify(govs)}", value,
                         r.exclude_govs(gov_list))

    def with_wonder(self, wonder: Wonder, value: int = 1) -> None:
        self._add_effect(f"wonder_{slugify(wonder)}", value, r.wonder(wonder))

    def with_wonder_worldwide(self, wonder: Wonder, value: int = 1) -> None:
        self._add_effect(f"world_wonder_{slugify(wonder)}", value,
                         r.wonder_worldwide(wonder))

    def maybe_with_wonder_worldwide(self, pct: int, wonder: Wonder,
                                    value: int = 1) -> None:
        if random_bool_pct(pct):
            self.with_wonder_worldwide(wonder, value)

    def after_wonder(self, wonder: Wonder, value: int = 1) -> None:
        self._add_effect(f"after_wonder_{slugify(wonder)}", value,
                         r.after_wonder(wonder))

    def after_wonder_worldwide(self, wonder: Wonder, value: int = 1) -> None:
        self._add_effect(f"after_world_wonder_{slugify(wonder)}", value,
                         r.after_wonder_worldwide(wonder))

    def maybe_after_wonder_worldwide(self, pct: int, wonder: Wonder,
                                     value: int = 1) -> None:
        if random_bool_pct(pct):
            self.after_wonder_worldwide(wonder, value)

    def with_tech(self, tech: Technology, value: int = 1) -> None:
        self._add_effect(f"tech_{slugify(tech)}", value, r.tech(tech))

    def with_gov(self, gov: GovernmentType, value: int = 1) -> None:
        self._add_effect(f"gov_{slugify(gov)}", value, r.gov(gov))

    def with_gov_and_tech(self, gov: GovernmentType, tech: Technology,
                          value: int = 1) -> None:
        self._add_effect(f"gov_{slugify(gov)}_tech_{slugify(tech)}", value,
                         r.gov(gov) + r.tech(tech))

    def on_terrain(self, terrain: Terrain, value: int = 1) -> None:
        self._add_effect(f"on_terrain_{slugify(terrain)}", value,
                         r.on_terrain(terrain))

    def on_extra(self, extra: TerrainExtra, value: int = 1) -> None:
        self._add_effect(f"on_extra_{slugify(extra)}", value, r.on_extra(extra))

    def with_gov_on_land(self, gov: GovernmentType, value: int = 1) -> None:
        self._add_effect(f"gov_{slugify(gov)}_on_land", value,
                         r.gov(gov) + r.on_land())

    def on_city(self, value: int = 1) -> None:
        self._add_effect("on_city", value, r.on_city())

    def not_on_city(self, value: int = 1) -> None:
        self._add_effect("not_on_city", value, r.not_on_city())

    def from_city_size(self, size: int, value: int = 1) -> None:
        self._add_effect(f"size_{size}", value, r.min_size(size))

    def maybe_from_city_size(self, pct: int, size: int, value: int = 1) -> None:
        if random_bool_pct(pct):
            self.from_city_size(size, value)

    def with_unit_class_flag(self, unit_class_flag: UnitClassFlag,
                             value: int = 1) -> None:
        self._add_effect(f"ucflag_{slugify(unit_class_flag)}", value,
                         r.unit_class_flag(unit_class_flag))

    def with_unit_class_flag_on_extra(self, unit_class_flag: UnitClassFlag,
                                      extra: TerrainExtra,
                                      value: int = 1) -> None:
        self._add_effect(
            f"ucflag_{slugify(unit_class_flag)}_on_extra_{slugify(extra)}",
            value,
            r.unit_class_flag(unit_class_flag) + r.on_extra(extra)
        )

    def with_building_and_tech(self, building: Building, tech: Technology,
                               value: int = 1) -> None:
        self._add_effect(f"building_{slugify(building)}_tech_{slugify(tech)}",
                         value,
                         r.building(building) + r.tech(tech))

    def with_building_and_gov(self, building: Building, gov: GovernmentType,
                              value: int = 1) -> None:
        self._add_effect(f"building_{slugify(building)}_gov_{slugify(gov)}",
                         value,
                         r.building(building) + r.gov(gov))

    def with_building_and_wonder(self, building: Building, wonder: Wonder,
                                 value: int = 1) -> None:
        self._add_effect(
            f"building_{slugify(building)}_wonder_{slugify(wonder)}", value,
            r.building(building) + r.wonder(wonder))

    def with_one_of_buildings(self, building_list: List[Building],
                              value: int = 1) -> None:
        buildings_slug = "_".join(building_list)
        for i in range(len(building_list)):
            name = f"one_of_buildings_{slugify(buildings_slug)}_{i}"
            self._add_effect(
                name, value,
                r.building(building_list[i]) +
                [r.exclude_building(building_list[j])
                 for j in range(i + 1, len(building_list))]
            )

    def with_any_palace(self, value: int = 1) -> None:
        self.with_one_of_buildings(all_palaces(), value)

    def maybe_with_any_palace(self, pct: int, value: int = 1) -> None:
        if random_bool_pct(pct):
            self.with_any_palace(value)

    def with_any_aqueduct(self, value: int = 1) -> None:
        return self.with_one_of_buildings(all_aqueducts(), value)

    def maybe_with_building(self, pct: int, building: Building,
                            value: int = 1) -> None:
        if random_bool_pct(pct):
            self.with_building(building, value)

    def maybe_with_building_on_extra(self, pct: int, building: Building,
                                     extra: TerrainExtra,
                                     value: int = 1) -> None:
        if random_bool_pct(pct):
            self.with_building_on_extra(building, extra, value)

    def maybe_with_palace(self, pct: int, value: int = 1) -> None:
        if random_bool_pct(pct):
            self.with_any_palace(value)

    def maybe_with_wonder(self, pct: int, wonder: Wonder,
                          value: int = 1) -> None:
        if random_bool_pct(pct):
            self.with_wonder(wonder, value)

    def maybe_with_tech(self, pct: int, tech: Technology,
                        value: int = 1) -> None:
        if random_bool_pct(pct):
            self.with_tech(tech, value)

    def maybe_with_gov(self, pct: int, gov: GovernmentType,
                       value: int = 1) -> None:
        if random_bool_pct(pct):
            self.with_gov(gov, value)

    def maybe_on_extra(self, pct: int, extra: TerrainExtra,
                       value: int = 1) -> None:
        if random_bool_pct(pct):
            self.on_extra(extra, value)

    def maybe_with_gov_on_land(self, pct: int, gov: GovernmentType,
                               value: int = 1) -> None:
        if random_bool_pct(pct):
            self.with_gov_on_land(gov, value)

    def maybe_with_buildings(self, pct: int, building_list: List[Building],
                             value: int = 1) -> None:
        if random_bool_pct(pct):
            self.with_buildings(building_list, value)

    def maybe_with_building_excluding_building(self, pct: int,
                                               building: Building,
                                               excluded_building: Building,
                                               value: int = 1) -> None:
        if random_bool_pct(pct):
            self.with_building_excluding_building(building, excluded_building,
                                                  value)

    def maybe_with_one_of_buildings(self, pct: int,
                                    building_list: List[Building],
                                    value: int = 1) -> None:
        if random_bool_pct(pct):
            self.with_one_of_buildings(building_list, value)

    def maybe_with_aqueduct(self, pct: int, value: int = 1) -> None:
        if random_bool_pct(pct):
            self.with_any_aqueduct(value)

    def maybe_with_building_and_tech(self, pct: 100, building: Building,
                                     tech: Technology,
                                     value: int = 1) -> None:
        if random_bool_pct(pct):
            self.with_building_and_tech(building, tech, value)

    def maybe_with_building_and_gov(self, pct: int, building: Building,
                                    gov: GovernmentType,
                                    value: int = 1) -> None:
        if random_bool_pct(pct):
            self.with_building_and_gov(building, gov, value)

    def maybe_with_building_and_wonder(self, pct: int, building: Building,
                                       wonder: Wonder,
                                       value: int = 1) -> None:
        if random_bool_pct(pct):
            self.with_building_and_wonder(building, wonder, value)

    def with_random_pct_of_buildings(self, pct: int,
                                     value_func: ValueFunc = lambda: 1) -> None:
        for building in random_pct_of_buildings(pct):
            self.with_building(building, value_func())

    def with_random_pct_of_building_genuses(self, pct: int,
                                            value_func: ValueFunc = lambda: 1) -> None:
        for genus in random_pct_of_building_genuses(pct):
            self.with_building_genus(genus, value_func())

    def with_random_pct_of_units(self, pct: int,
                                 value_func: ValueFunc = lambda: 1) -> None:
        for unit in random_pct_of_units(pct):
            self.with_unit_type(unit, value_func())

    def with_random_pct_of_unit_classes(self, pct: int,
                                        value_func: ValueFunc = lambda: 1) -> None:
        for unit_class in random_pct_of_unit_classes(pct):
            self.with_unit_class(unit_class, value_func())

    def with_random_pct_of_unit_flags(self, pct: int,
                                      value_func: ValueFunc = lambda: 1) -> None:
        for flag in random_pct_of_unit_flags(pct):
            self.with_unit_flag(flag, value_func())

    def with_random_pct_of_unit_class_flags(self, pct: int,
                                            value_func: ValueFunc = lambda: 1) -> None:
        for flag in random_pct_of_unit_class_flags(pct):
            self.with_unit_class_flag(flag, value_func())

    def with_random_pct_of_wonders(self, pct: int,
                                   value_func: ValueFunc = lambda: 1) -> None:
        for wonder in random_pct_of_wonders(pct):
            self.with_wonder(wonder, value_func())

    def with_random_pct_of_techs(self, pct: int,
                                 value_func: ValueFunc = lambda: 1) -> None:
        for tech in random_pct_of_techs(pct):
            self.with_tech(tech, value_func())

    def with_random_pct_of_govs(self, pct: int,
                                value_func: ValueFunc = lambda: 1) -> None:
        for gov in random_pct_of_govs(pct):
            self.with_gov(gov, value_func())

    def with_random_pct_of_terrain(self, pct: int,
                                   value_func: ValueFunc = lambda: 1) -> None:
        for terrain in random_pct_of_terrain(pct):
            self.on_terrain(terrain, value_func())

    def with_random_pct_of_extras(
            self, pct: int, value_func: ValueFunc = lambda: 1) -> None:
        for building, extra in random_pct_of_extras(pct):
            self.on_extra(extra, value_func())

    def with_random_pct_of_buildings_on_extras(
            self, pct: int, value_func: ValueFunc = lambda: 1) -> None:
        for building, extra in random_pct_of_buildings_and_extras(pct):
            self.with_building_on_extra(building, extra, value_func())

    def with_random_pct_of_wonders_on_extras(
            self, pct: int, value_func: ValueFunc = lambda: 1) -> None:
        for wonder, extra in random_pct_of_wonders_and_extras(pct):
            self.with_wonder_on_extra(wonder, extra, value_func())

    def with_random_pct_of_techs_on_extras(
            self, pct: int, value_func: ValueFunc = lambda: 1) -> None:
        for tech, extra in random_pct_of_techs_and_extras(pct):
            self.with_tech_on_extra(tech, extra, value_func())

    def with_random_pct_of_govs_on_extras(
            self, pct: int, value_func: ValueFunc = lambda: 1) -> None:
        for gov, extra in random_pct_of_govs_and_extras(pct):
            self.with_gov_on_extra(gov, extra, value_func())

    def with_random_pct_of_buildings_on_terrain(
            self, pct: int, value_func: ValueFunc = lambda: 1) -> None:
        for building, terrain in random_pct_of_buildings_and_terrain(pct):
            self.with_building_on_terrain(building, terrain, value_func())

    def with_random_pct_of_wonders_on_terrain(
            self, pct: int, value_func: ValueFunc = lambda: 1) -> None:
        for wonder, terrain in random_pct_of_wonders_and_terrain(pct):
            self.with_wonder_on_terrain(wonder, terrain, value_func())

    def with_random_pct_of_techs_on_terrain(
            self, pct: int, value_func: ValueFunc = lambda: 1) -> None:
        for tech, terrain in random_pct_of_techs_and_terrain(pct):
            self.with_tech_on_terrain(tech, terrain, value_func())

    def with_random_pct_of_govs_on_terrain(
            self, pct: int, value_func: ValueFunc = lambda: 1) -> None:
        for gov, terrain in random_pct_of_govs_and_terrain(pct):
            self.with_gov_on_terrain(gov, terrain, value_func())

    def maybe_with_random_pct_of_buildings(
            self, chance: int, freq: int,
            value_func: ValueFunc = lambda: 1) -> None:
        if random_bool_pct(chance):
            self.with_random_pct_of_buildings(freq, value_func)

    def maybe_with_random_pct_of_building_genuses(
            self, chance: int, freq: int,
            value_func: ValueFunc = lambda: 1) -> None:
        if random_bool_pct(chance):
            self.with_random_pct_of_building_genuses(freq, value_func)

    def maybe_with_random_pct_of_units(
            self, chance: int, freq: int,
            value_func: ValueFunc = lambda: 1) -> None:
        if random_bool_pct(chance):
            self.with_random_pct_of_units(freq, value_func)

    def maybe_with_random_pct_of_unit_classes(
            self, chance: int, freq: int,
            value_func: ValueFunc = lambda: 1) -> None:
        if random_bool_pct(chance):
            self.with_random_pct_of_unit_classes(freq, value_func)

    def maybe_with_random_pct_of_unit_flags(
            self, chance: int, freq: int,
            value_func: ValueFunc = lambda: 1) -> None:
        if random_bool_pct(chance):
            self.with_random_pct_of_unit_flags(freq, value_func)

    def maybe_with_random_pct_of_unit_class_flags(
            self, chance: int, freq: int,
            value_func: ValueFunc = lambda: 1) -> None:
        if random_bool_pct(chance):
            self.with_random_pct_of_unit_class_flags(freq, value_func)

    def maybe_with_random_pct_of_wonders(
            self, chance: int, freq: int,
            value_func: ValueFunc = lambda: 1) -> None:
        if random_bool_pct(chance):
            self.with_random_pct_of_wonders(freq, value_func)

    def maybe_with_random_pct_of_techs(
            self, chance: int, freq: int,
            value_func: ValueFunc = lambda: 1) -> None:
        if random_bool_pct(chance):
            self.with_random_pct_of_techs(freq, value_func)

    def maybe_with_random_pct_of_govs(
            self, chance: int, freq: int,
            value_func: ValueFunc = lambda: 1) -> None:
        if random_bool_pct(chance):
            self.with_random_pct_of_govs(freq, value_func)

    def maybe_with_random_pct_of_terrain(
            self, chance: int, freq: int,
            value_func: ValueFunc = lambda: 1) -> None:
        if random_bool_pct(chance):
            self.with_random_pct_of_terrain(freq, value_func)

    def maybe_with_random_pct_of_extras(
            self, chance: int, freq: int,
            value_func: ValueFunc = lambda: 1) -> None:
        if random_bool_pct(chance):
            self.with_random_pct_of_extras(freq, value_func)

    def maybe_with_random_pct_of_buildings_on_extras(
            self, chance: int, freq: int,
            value_func: ValueFunc = lambda: 1) -> None:
        if random_bool_pct(chance):
            self.with_random_pct_of_buildings_on_extras(freq, value_func)

    def maybe_with_random_pct_of_wonders_on_extras(
            self, chance: int, freq: int,
            value_func: ValueFunc = lambda: 1) -> None:
        if random_bool_pct(chance):
            self.with_random_pct_of_wonders_on_extras(freq, value_func)

    def maybe_with_random_pct_of_techs_on_extras(
            self, chance: int, freq: int,
            value_func: ValueFunc = lambda: 1) -> None:
        if random_bool_pct(chance):
            self.with_random_pct_of_techs_on_extras(freq, value_func)

    def maybe_with_random_pct_of_govs_on_extras(
            self, chance: int, freq: int,
            value_func: ValueFunc = lambda: 1) -> None:
        if random_bool_pct(chance):
            self.with_random_pct_of_govs_on_extras(freq, value_func)

    def maybe_base(self, chance: int, value: int = 1) -> None:
        if random_bool_pct(chance):
            self.base_effect(value)

    def on_irrigation(self, value: int = 1) -> None:
        self._add_effect("on_irrigation", value, r.on_extra("Irrigation"))

    def on_city_auto_irrigation(self, value: int = 1) -> None:
        self._add_effect("on_city_auto_irrigation", value,
                         r.on_city() +
                         r.not_on_extra("Irrigation") +
                         r.on_irrigatable_terrain() +
                         r.not_on_extra("Mine"))

    def on_flood_plain(self, value: int = 1) -> None:
        self._add_effect("on_flood_plain", value,
                         r.on_terrain("Desert")
                         + r.on_extra("River")
                         + r.not_on_extra("Oasis"))

    def on_super_highways(self, value: int = 1) -> None:
        self._add_effect("on_super_highways", value,
                         r.on_extra("Road")
                         + r.building("Super Highways")
                         + r.not_on_extra("Farmland")
                         + r.not_on_city())
        self._add_effect("city_auto_super_highways", value,
                         r.on_extra("Road")
                         + r.building("Super Highways")
                         + r.on_city())

    def with_building_genus(self, building_genus: BuildingGenus,
                            value: int) -> None:
        self._add_effect(f"building_genus_{slugify(building_genus)}", value,
                         r.building_genus(building_genus))

    def all_excluding_building(self, building: Building, value: int) -> None:
        self._add_effect(f"excluding_building_{slugify(building)}", value,
                         r.exclude_building(building))

    # Sub groups
    def sub_group(self, prefix: str, reqs: List[Requirement]) -> "EffectGroup":
        return EffectGroup(self.etype, f"{self.prefix}_{prefix}_and_",
                           self.reqs + reqs, self.children)

    def on_city_group(self) -> "EffectGroup":
        return self.sub_group("on_city", r.on_city())

    def not_on_city_group(self) -> "EffectGroup":
        return self.sub_group("not_on_city", r.not_on_city())

    def on_extra_group(self, extra: TerrainExtra) -> "EffectGroup":
        return self.sub_group(f"on_extra_{slugify(extra)}", r.on_extra(extra))

    def not_on_extra_group(self, extra: TerrainExtra) -> "EffectGroup":
        return self.sub_group(f"not_on_extra_{slugify(extra)}",
                              r.not_on_extra(extra))

    def on_farmland_group(self) -> "EffectGroup":
        return self.sub_group("on_farmland", r.on_extra("Farmland"))

    def on_city_auto_farmland_group(self) -> "EffectGroup":
        return self.sub_group(
            "on_city_auto_farmland",
            r.on_city()
            + r.not_on_extra("Farmland")
            + r.on_irrigatable_terrain()
            + r.not_on_extra("Mine")
            + r.not_on_extra("Oil Well")
        )

    def on_sea_group(self) -> "EffectGroup":
        return self.sub_group("on_sea", r.on_terrain_with_flag("Sea"))

    def with_building_group(self, building: Building) -> "EffectGroup":
        return self.sub_group(f"building_{slugify(building)}",
                              r.building(building))

    def with_gov_group(self, gov: GovernmentType) -> "EffectGroup":
        return self.sub_group(f"gov_{slugify(gov)}", r.gov(gov))

    def with_building_genus_group(
            self, building_genus: BuildingGenus) -> "EffectGroup":
        return self.sub_group(f"building_genus_{slugify(building_genus)}",
                              r.building_genus(building_genus))

    def with_unit_class_flag_group(self, flag: UnitClassFlag) -> "EffectGroup":
        return self.sub_group(f"unit_class_flag_{slugify(flag)}",
                              r.unit_class_flag(flag))

    def with_any_of_buildings_group(
            self, building_list: List[Building]) -> "EffectGroup":
        return EffectGroup(
            self.etype, self.prefix, self.reqs,
            [self.with_building_group(building) for building in building_list]
        ) #TODO does this work?

    def with_any_barracks_group(self) -> "EffectGroup":
        return self.with_any_of_buildings_group(all_barracks())

    # Other group types
    def first_match_in_group(self):
        return FirstMatchEffectGroup(self.etype, f"{self.prefix}_first_",
                                     self.reqs, self.children)


class FirstMatchEffectGroup(EffectGroup):
    def __init__(self, etype: EffectType, prefix: str, reqs: List[Requirement],
                 children: ListTOrEmpty[EffectGroup]):
        super().__init__(etype, prefix, reqs, children)

    def __enter__(self):
        self.child_effect_groups = [c.to_effect_group(self)
                                    for c in self.children]
        self.earlier_match_reqs = []
        return self

    def _add_effect(self, name: str, value: int,
                    reqs: ListTOrEmpty[Requirement]) -> None:
        if self.children:
            for g in self.child_effect_groups:
                g.add_effect(Effect(name, value, reqs +
                                    self.earlier_match_reqs))
        else:
            rule_effects()[f"{self.prefix}_{name}"] = {
                "type": self.etype,
                "reqs": reqs + self.reqs + self.earlier_match_reqs,
                "value": value
            }
        self.earlier_match_reqs.append(r.negated(*reqs))


def path_get(data: Dict, path: str) -> Any | None:
    keys = path.split('.')
    current = data
    for key in keys[:-1]:
        if key not in current:
            return None
        current = current[key]
    return current[keys[-1]]


def path_set(data: Dict, name: str, value: Any) -> None:
    keys = name.split('.')
    current = data
    for key in keys[:-1]:
        if key not in current:
            current[key] = {}
        current = current[key]
    current[keys[-1]] = value


@evaluate_once
def server_options() -> Dict:
    return {}


# TODO: Setting name and value type hints
def setting(name: str, value: T) -> T:
    path_set(server_options(), name, value)
    return value


@evaluate_once
def chaos_features() -> Dict:
    return {}


# TODO: Feature name and value type hints
def feature(name: str, value: T) -> T:
    path_set(chaos_features(), name, value)
    return value


class UnitTypeDef:
    def __init__(self, utype: UnitType):
        self.utype = utype
        self.flags = []


@evaluate_once
def unit_type_defs() -> Dict[UnitType, UnitTypeDef]:
    return {}


def unit_type_def(utype: UnitType) -> UnitTypeDef:
    if not unit_type_defs()[utype]:
        unit_type_defs()[utype] = UnitTypeDef(utype)
    return unit_type_defs()[utype]


def unit_type_add_flag(utype: UnitType, flag: UnitFlag) -> None:
    unit_type_def(utype).flags.append(flag)


# Config definition
def starting_units_and_cities():
    def _standard():
        setting("start.firstCityBuilt", False)
        setting("start.units.cityFounders", 5)
        setting("start.units.terrainWorkers", 6)
        setting("start.units.explorers", 2)
        setting("start.units.leaders", 0)
        setting("start.units.diplomats", 0)
        setting("start.units.ferryBoats", 0)
        setting("start.units.okayDefenders", 0)
        setting("start.units.goodDefenders", 0)
        setting("start.units.fastAttackers", 0)
        setting("start.units.strongAttackers", 0)

    def _random():
        @evaluate_once
        def _first_city_built():
            return random_bool_pct(50)

        def _standard_military():
            setting("start.units.okayDefenders", 0)
            setting("start.units.goodDefenders", 0)
            setting("start.units.fastAttackers", 0)
            setting("start.units.strongAttackers", 0)

        def _random_military():
            setting("start.units.okayDefenders", min_skewed_randint(0, 12))
            setting("start.units.goodDefenders", min_skewed_randint(0, 12))
            setting("start.units.fastAttackers", min_skewed_randint(0, 12))
            setting("start.units.strongAttackers", min_skewed_randint(0, 12))

        setting("start.firstCityBuilt", _first_city_built())
        setting("start.units.cityFounders", mid_skewed_randint(2, 8) -
                (1 if _first_city_built() else 0))
        setting("start.units.terrainWorkers", mid_skewed_randint(3, 9))
        setting("start.units.explorers", weighted_random_possibilities(
            stable_possibility(70, 2),
            stable_possibility(30, 0),
            chaotic_possibility(100, min_skewed_randint(2, 12))
        ))
        setting("start.units.leaders", 0)
        setting("start.units.diplomats", weighted_random_possibilities(
            stable_possibility(100, 0),
            chaotic_possibility(100, min_skewed_randint(0, 12))
        ))
        setting("start.units.ferryBoats", weighted_random_possibilities(
            stable_possibility(100, 0),
            chaotic_possibility(100, min_skewed_randint(0, 12))
        ))
        weighted_random_possibilities(
            stable_possibility(120, _standard_military),
            chaotic_possibility(100, _random_military)
        )()

    weighted_random_possibilities(
        stable_possibility(60, _standard),
        chaotic_possibility(100, _random),
    )()


@evaluate_once
def min_dist_between_cities():
    return weighted_random_possibilities(
        stable_possibility(50, 4),
        stable_possibility(50, 5),
        chaotic_possibility(40, 1),
        chaotic_possibility(40, 11),
        chaotic_possibility(40, randint(1, 11)),
    )


def city_work_radius():
    def _city_radius_sq_effect_group():
        return EffectGroup("City_Radius_Sq", "city_radius")

    def _standard():
        setting("cities.workRadiusSq.initial", 15)
        with _city_radius_sq_effect_group() as g:
            g.with_tech("Theology", 3)
            g.with_building("Mass Transit", 6)

    def _relates_to_min_dist():
        min_dist = min_dist_between_cities()
        initial_radius = max(0, (min_dist - 1) // 2)
        initial_radius_sq = floor(initial_radius ** 2)
        theology_bonus = (((5 + initial_radius) // 2) ** 2) - initial_radius_sq
        mass_transit_bonus = 25 - theology_bonus - initial_radius_sq

        with _city_radius_sq_effect_group() as g:
            g.with_tech("Theology", theology_bonus)
            g.with_building("Mass Transit", mass_transit_bonus)
        setting("cities.workRadiusSq.initial", initial_radius_sq)

    def _random():
        def _randomised():
            return weighted_random_possibilities(
                stable_possibility(100, randint(1, 4)),
                chaotic_possibility(100,
                                    mid_skewed_randint(-25, 25, 3)),
            )

        with _city_radius_sq_effect_group() as g:
            g.with_random_pct_of_techs(10, _randomised)
            g.with_random_pct_of_buildings(10, _randomised)
            g.maybe_with_building(80, "Mass Transit", _randomised())
            g.with_random_pct_of_wonders(5, _randomised)
            g.with_random_pct_of_govs(30, _randomised)

        setting("cities.workRadiusSq.initial",
                min_skewed_randint(1, 5, skew=2) ** 2)

    weighted_random_possibilities(
        stable_possibility(70, _standard),
        stable_possibility(30, _random),
        chaotic_possibility(100, _relates_to_min_dist),
    )()


def city_migration():
    def _disabled():
        setting("cities.migration.enabled", False)

    def _maximised():
        setting("cities.migration.enabled", True)
        setting("cities.migration.maxDistanceFromWorkingArea", 6)
        setting("cities.migration.newCitizensNeedATileWith2Food", False)
        setting("cities.migration.turnsBetweenAttempts", 1)
        setting("cities.migration.baseNationalMigrationChancePct", 100)
        setting("cities.migration.baseInternationalMigrationChancePct", 100)

    def _random():
        setting("cities.migration.enabled", True)
        setting("cities.migration.maxDistanceFromWorkingArea", randint(-5, 6))
        setting("cities.migration.newCitizensNeedATileWith2Food",
                random_bool_pct(50))
        setting("cities.migration.turnsBetweenAttempts",
                min_skewed_randint(1, 100, skew=4))
        setting("cities.migration.baseNationalMigrationChancePct",
                randint(0, 100))
        setting("cities.migration.baseInternationalMigrationChancePct",
                randint(0, 100))

    return weighted_random_possibilities(
        stable_possibility(60, _disabled),
        chaotic_possibility(30, _maximised),
        chaotic_possibility(70, _random),
    )()


def rapture_growth():
    def _disabled():
        setting("cities.growth.fromCelebration.enabled", False)

    def _random():
        setting("cities.growth.fromCelebration.enabled", True)
        setting("cities.growth.fromCelebration.turnsBetweenGrowth",
                randint(1, 5))
        with EffectGroup("Rapture_Grow", "celebration_growth") as g:
            g.with_random_pct_of_govs(20)
            g.maybe_with_gov(80, "Democracy")
            g.maybe_with_gov(60, "Republic")
            g.with_random_pct_of_wonders(3)
            g.maybe_with_wonder(70, "Pyramids")
            g.with_random_pct_of_techs(2)
            g.with_random_pct_of_buildings(4)

    return weighted_random_possibilities(
        stable_possibility(120, _disabled),
        chaotic_possibility(100, _random)
    )()


def max_city_size():
    def _standard():
        setting("cities.growth.maxSize.enabled", True)
        setting("cities.growth.maxSize.base", 8)
        with EffectGroup("Size_Adj", "city_size") as g:
            g.with_any_aqueduct(8)
        with EffectGroup("Size_Unlimit", "city_size_unlocked") as g:
            g.with_building("Sewer System")

    def _disabled():
        setting("cities.growth.maxSize.enabled", False)
        with EffectGroup("Size_Unlimit", "city_size_unlocked") as g:
            g.base_effect(1)

    def _strict_max():
        setting("cities.growth.maxSize.enabled", True)
        setting("cities.growth.maxSize.base", 8)
        with EffectGroup("Size_Adj", "city_size") as g:
            g.with_any_aqueduct(8)
            g.with_building("Sewer System", 8)

    def _random():
        frequency = randint(5, 50)
        amplitude = 100 // frequency

        def _building_bonus():
            return mid_skewed_randint(-amplitude * 2, amplitude * 2)

        def _wonder_bonus():
            return mid_skewed_randint(-amplitude, amplitude)

        def _tech_bonus():
            return mid_skewed_randint(-amplitude, amplitude)

        def _gov_bonus():
            return mid_skewed_randint(-amplitude, amplitude)

        setting("cities.growth.maxSize.enabled", True)
        setting("cities.growth.maxSize.base", weighted_random_possibilities(
            stable_possibility(100, mid_skewed_randint(1, 16)),
            chaotic_possibility(100, min_skewed_randint(1, 255, skew=3)),
        ))
        with EffectGroup("Size_Adj", "city_size") as g:
            g.with_random_pct_of_buildings(frequency, _building_bonus)
            g.maybe_with_building(70, "Sewer System", mid_skewed_randint(1, 16))
            g.maybe_with_aqueduct(80, mid_skewed_randint(1, 16))
            g.with_random_pct_of_wonders(frequency, _wonder_bonus)
            g.with_random_pct_of_techs(frequency, _tech_bonus)
            g.with_random_pct_of_govs(frequency, _gov_bonus)

    return weighted_random_possibilities(
        stable_possibility(60, _standard),
        stable_possibility(40, _disabled),
        chaotic_possibility(70, _strict_max),
        chaotic_possibility(30, _random),
    )()


def entertainer_luxuries():
    def _elvis_lux_output_effect_group():
        return EffectGroup("Specialist_Output", "elvis",
                           r.specialist("Elvis") +
                           r.luxuries())

    def _standard():
        with _elvis_lux_output_effect_group() as g:
            g.base_effect(2)
            g.after_wonder_worldwide("Shakespeare's Theatre", 1)

    def _random():
        with _elvis_lux_output_effect_group() as g:
            g.base_effect(randint(1, 3))
            g.maybe_after_wonder_worldwide(
                70, "Shakespeare's Theatre", weighted_random_possibilities(
                    possibility(60, randint(1, 2)),
                    possibility(10, min_skewed_randint(1, 100, skew=5)),
                ))

    def _wacky():
        def _randomised():
            return mid_skewed_randint(-100, 100, skew=5)

        with _elvis_lux_output_effect_group() as g:
            g.base_effect(min_skewed_randint(1, 100, skew=6))
            g.with_random_pct_of_wonders(20, _randomised)
            g.with_random_pct_of_buildings(15, _randomised)
            g.with_random_pct_of_govs(50, _randomised)
            g.with_random_pct_of_techs(20, _randomised)

    return weighted_random_possibilities(
        stable_possibility(80, _standard),
        chaotic_possibility(50, _random),
        chaotic_possibility(50, _wacky),
    )()


def empire_size_unhappiness():
    def _disabled():
        return ()

    def _standard():
        return {
            "Tribal": {"initial": 10, "step": 10},
            "Despotism": {"initial": 10, "step": 10},
            "Monarchy": {"initial": 20, "step": 20},
            "City States": {"initial": 7, "step": 1},
            "Communism": {"initial": 28, "step": 28},
            "Fundamentalism": {"initial": 20, "step": 20},
            "Federation": {"initial": 24, "step": 24},
            "Republic": {"initial": 16, "step": 16},
            "Democracy": {"initial": 16, "step": 16}
        }

    def _random():
        def __randomised():
            return {
                "initial": mid_skewed_randint(
                    min_int=1,
                    max_int=min_skewed_randint(20, 100, skew=2)
                ),
                "step": mid_skewed_randint(
                    min_int=1,
                    max_int=min_skewed_randint(20, 100, skew=2)
                )
            }

        return {_gov: __randomised() for _gov in all_governments()}

    @evaluate_once
    def _gov_settings():
        return weighted_random_possibilities(
            stable_possibility(80, _standard),
            chaotic_possibility(50, _disabled),
            chaotic_possibility(50, _random),
        )()

    with EffectGroup("Empire_Size_Base", "empire_size_base") as g:
        for gov, settings in _gov_settings():
            g.with_gov(gov, settings.initial)
    with EffectGroup("Empire_Size_Step", "empire_size_step") as g:
        for gov, settings in _gov_settings():
            g.with_gov(gov, settings.step)


def martial_law():
    def _disabled():
        return ()

    def _unlimited():
        return {
            "Anarchy": {"citizensPerUnit": 1},
            "Tribal": {"citizensPerUnit": 1},
            "Despotism": {"citizensPerUnit": 2},
            "Monarchy": {"citizensPerUnit": 1},
            "Communism": {"citizensPerUnit": 2}
        }

    def _standard():
        return {
            "Anarchy": {"citizensPerUnit": 1},
            "Tribal": {"citizensPerUnit": 1, "maxUnits": 3},
            "Despotism": {"citizensPerUnit": 1, "maxUnits": 20},
            "Monarchy": {"citizensPerUnit": 1, "maxUnits": 3},
            "Communism": {"citizensPerUnit": 2, "maxUnits": 3}
        }

    def _random():
        def __randomised():
            return {
                "citizensPerUnit": weighted_random_possibilities(
                    possibility(50, 1),
                    possibility(25, 2),
                    possibility(15, 3),
                    possibility(10, min_skewed_randint(1, 255, skew=5)),
                ),
                "maxUnits": weighted_random_possibilities(
                    possibility(50, 3),
                    possibility(30, randint(1, 20)),
                    possibility(20, min_skewed_randint(1, 1000, skew=5)),
                )
            }

        return {_gov: __randomised() for _gov in random_pct_of_govs(50)}

    @evaluate_once
    def _gov_settings():
        return weighted_random_possibilities(
            stable_possibility(80, _standard),
            chaotic_possibility(30, _disabled),
            chaotic_possibility(30, _unlimited),
            chaotic_possibility(40, _random),
        )()

    with EffectGroup("Martial_Law_Each") as g:
        for gov, settings in _gov_settings():
            if settings.citizensPerUnit:
                g.with_gov(gov, settings.citizensPerUnit)
    with EffectGroup("Martial_Law_Max") as g:
        for gov, settings in _gov_settings():
            if settings.maxUnits:
                g.with_gov(gov, settings.maxUnits)


def city_luxury_bonus():
    def city_tile_lux_bonus_group():
        return EffectGroup("Output_Add_Tile", "city_tile_lux_bonus",
                           r.on_city() + r.luxuries())

    def _standard():
        with city_tile_lux_bonus_group() as g:
            g.with_gov("Federation", 2)
            g.with_building("Hanging Gardens", 4)
            g.with_building("Shakespeare's Theatre", 5)
            g.with_building("Hal Saflieni Hypogeum", 6)
            g.with_wonder("Cure For Cancer", 4)
            g.with_wonder("J.S. Bach's Cathedral", 5)
            g.with_wonder("Shakespeare's Theatre", 6)

    def _random():
        def _gov_bonus():
            return weighted_random_possibilities(
                stable_possibility(100, randint(1, 3)),
                chaotic_possibility(100,
                                    min_skewed_randint(1, 1000, skew=6)),
            )

        def _building_bonus():
            return weighted_random_possibilities(
                stable_possibility(100, randint(1, 6)),
                chaotic_possibility(100,
                                    min_skewed_randint(1, 1000, skew=5)),
            )

        def _special_bonus():
            return weighted_random_possibilities(
                stable_possibility(100, mid_skewed_randint(1, 9)),
                chaotic_possibility(100,
                                    min_skewed_randint(1, 1000, skew=5)),
            )

        def _wonder_bonus():
            return weighted_random_possibilities(
                stable_possibility(100, randint(1, 6)),
                chaotic_possibility(100,
                                    min_skewed_randint(1, 1000, skew=5)),
            )

        def _tech_bonus():
            return weighted_random_possibilities(
                stable_possibility(100, randint(1, 6)),
                chaotic_possibility(100,
                                    min_skewed_randint(1, 1000, skew=5)),
            )

        with city_tile_lux_bonus_group() as g:
            g.with_random_pct_of_govs(15, _gov_bonus)
            g.maybe_with_gov(70, "Federation", _gov_bonus())
            g.with_random_pct_of_buildings(15, _building_bonus)
            g.maybe_with_building(70, "Hanging Gardens", _special_bonus())
            g.maybe_with_building(70, "Shakespeare's Theatre", _special_bonus())
            g.maybe_with_building(70, "Hal Saflieni Hypogeum", _special_bonus())
            g.with_random_pct_of_wonders(15, _wonder_bonus)
            g.maybe_with_wonder(70, "Cure For Cancer", _special_bonus())
            g.maybe_with_wonder(70, "J.S. Bach's Cathedral", _special_bonus())
            g.maybe_with_wonder(70, "Shakespeare's Theatre", _special_bonus())
            g.with_random_pct_of_techs(10, _tech_bonus)

    return weighted_random_possibilities(
        stable_possibility(100, _standard),
        chaotic_possibility(100, _random),
    )()


def city_luxury_output_bonus_pct():
    def _luxury_output_bonus_effects():
        return EffectGroup("Output_Bonus", "lux_output_bonus", r.luxuries())

    def _standard():
        with _luxury_output_bonus_effects() as g:
            g.with_gov("Anarchy", -50)
            g.with_building("Marketplace", 50)
            g.with_building("Bank", 30)
            g.with_building("Mercantile Exchange", 30)
            g.with_building("Stock Exchange", 40)
            g.with_buildings(["Super Highways", "Stock Exchange"], 25)

    def _random():
        def _gov_bonus():
            return mid_skewed_randint(-100, 100)

        def _building_bonus():
            return mid_skewed_randint(-100, 100)

        def _wonder_bonus():
            return mid_skewed_randint(-100, 100, skew=2)

        def _tech_bonus():
            return mid_skewed_randint(-100, 100, skew=2)

        with _luxury_output_bonus_effects() as g:
            g.with_random_pct_of_govs(30, _gov_bonus)
            g.maybe_with_gov(70, "Anarchy", mid_skewed_randint(-100, 0))
            g.with_random_pct_of_buildings(5, _building_bonus)
            g.maybe_with_building(70, "Marketplace", mid_skewed_randint(0, 100))
            g.maybe_with_building(70, "Bank", mid_skewed_randint(0, 100))
            g.maybe_with_building(70, "Mercantile Exchange",
                                  mid_skewed_randint(0, 100))
            g.maybe_with_building(70, "Stock Exchange",
                                  mid_skewed_randint(0, 100))
            g.with_random_pct_of_wonders(10, _wonder_bonus)
            g.with_random_pct_of_techs(10, _tech_bonus)
            g.maybe_with_buildings(70, ["Super Highways", "Stock Exchange"],
                                   mid_skewed_randint(0, 50))

    return weighted_random_possibilities(
        stable_possibility(100, _standard),
        chaotic_possibility(100, _random),
    )()


def city_contentment_bonuses():
    def _standard():
        with EffectGroup("Make_Content") as g:
            g.with_building("Cathedral", 3)
            g.with_building("Colosseum", 3)
            g.with_building("Courthouse", 1)
            g.with_building("Police Station", 2)
            g.with_building("Temple", 1)
            g.with_wonder("Hanging Gardens", 1)
            g.with_building_and_tech("Cathedral", "Theology", 1)
            g.with_building_and_gov("Cathedral", "Communism", -1)
            g.with_building_and_wonder("Cathedral", "Michelangelo's Chapel", 3)
            g.with_building_and_tech("Colosseum", "Electricity", 1)
            g.with_building_and_wonder("Courthouse", "Mausoleum of Mausolos", 1)
            g.with_building_and_wonder("City Walls", "Mausoleum of Mausolos", 1)
            g.with_building_and_gov("Palace", "City States", 8)
            g.with_building_and_tech("Temple", "Mysticism", 1)
            g.with_building_and_gov("Temple", "Communism", -1)

    def _random():
        def _randomised(_base=2):
            sign = round(copysign(_base))
            mid = _base * sign
            return weighted_random_possibilities(
                possibility(70, sign * randint(1, (mid * 2) - 1)),
                possibility(20, min_skewed_randint(1, 255, skew=5)),
                possibility(10, -min_skewed_randint(1, 255, skew=5)),
            )

        with EffectGroup("Make_Content") as g:
            g.with_random_pct_of_buildings(15, _randomised)
            g.maybe_with_building(70, "Cathedral", _randomised(3))
            g.maybe_with_building(70, "Colosseum", _randomised(3))
            g.maybe_with_building(70, "Courthouse", _randomised(1))
            g.maybe_with_building(70, "Police Station", _randomised(2))
            g.maybe_with_building(70, "Temple", _randomised(1))
            g.with_random_pct_of_wonders(8, _randomised)
            g.maybe_with_wonder(70, "Hanging Gardens", _randomised(1))
            g.with_random_pct_of_techs(8, _randomised)
            g.with_random_pct_of_govs(20, _randomised)
            g.maybe_with_building_and_tech(
                70, "Cathedral", "Theology", _randomised(1))
            g.maybe_with_building_and_gov(
                70, "Cathedral", "Communism", _randomised(-1))
            g.maybe_with_building_and_wonder(
                70, "Cathedral", "Michelangelo's Chapel", _randomised(3))
            g.maybe_with_building_and_tech(
                70, "Colosseum", "Electricity", _randomised(1))
            g.maybe_with_building_and_wonder(
                70, "Courthouse", "Mausoleum of Mausolos", _randomised(1))
            g.maybe_with_building_and_wonder(
                70, "City Walls", "Mausoleum of Mausolos", _randomised(1))
            g.maybe_with_building_and_gov(
                70, "Palace", "City States", _randomised(8))
            g.maybe_with_building_and_tech(
                70, "Temple", "Mysticism", _randomised(1))
            g.maybe_with_building_and_gov(
                70, "Temple", "Communism", _randomised(-1))

    return weighted_random_possibilities(
        stable_possibility(100, _standard),
        chaotic_possibility(100, _random),
    )()


def city_nationalism_unhappiness():
    def _nationalism_unhappiness_effect_group():
        return EffectGroup("Enemy_Citizen_Unhappy_Pct",
                           "nationalism_unhappiness")

    def _standard():
        with _nationalism_unhappiness_effect_group() as g:
            g.with_gov("Communism", 30)
            g.with_gov("Despotism", 60)
            g.with_gov("Federation", 60)
            g.with_gov("Monarchy", 50)
            g.with_gov("Tribal", 80)
            g.with_gov("Fundamentalism", 20)
            g.with_gov("City States", 20)
            g.with_gov("Republic", 40)
            g.with_gov("Democracy", 80)
            g.with_building_and_gov("Occupation Government", "Communism", -15)
            g.with_building_and_gov("Occupation Government", "Despotism", -30)
            g.with_building_and_gov("Occupation Government", "Federation", -40)
            g.with_building_and_gov("Occupation Government", "Monarchy", -25)
            g.with_building_and_gov("Occupation Government", "Tribal", -40)
            g.with_building_and_gov("Occupation Government",
                                    "Fundamentalism", -40)
            g.with_building_and_gov("Occupation Government", "Republic", -20)
            g.with_building_and_gov("Occupation Government", "Democracy", -40)

    def _random():
        def _base():
            return randint(0, 100)

        def _randomised():
            return mid_skewed_randint(-100, 100, skew=2)

        def _reduction():
            return mid_skewed_randint(-60, -1)

        with _nationalism_unhappiness_effect_group() as g:
            g.with_random_pct_of_govs(90, _base)
            g.with_random_pct_of_buildings(10, _randomised)
            g.with_random_pct_of_wonders(10, _randomised)
            g.with_random_pct_of_techs(10, _randomised)
            g.maybe_with_building_and_gov(
                70, "Occupation Government", "Communism", _reduction())
            g.maybe_with_building_and_gov(
                70, "Occupation Government", "Despotism", _reduction())
            g.maybe_with_building_and_gov(
                70, "Occupation Government", "Federation", _reduction())
            g.maybe_with_building_and_gov(
                70, "Occupation Government", "Monarchy", _reduction())
            g.maybe_with_building_and_gov(
                70, "Occupation Government", "Tribal", _reduction())
            g.maybe_with_building_and_gov(
                70, "Occupation Government", "Fundamentalism", _reduction())
            g.maybe_with_building_and_gov(
                70, "Occupation Government", "Republic", _reduction())
            g.maybe_with_building_and_gov(
                70, "Occupation Government", "Democracy", _reduction())

    return weighted_random_possibilities(
        stable_possibility(100, _standard),
        chaotic_possibility(100, _random),
    )()


def city_defender_bonuses():
    @evaluate_once
    def _city_defence_effect_group():
        return EffectGroup("Defend_Bonus", "city_defence", r.on_city())

    def _city_land_defence_effect_group():
        return (_city_defence_effect_group()
                .sub_group("land", r.unit_class_flag("Land")))

    def _city_sea_defence_effect_group():
        return (_city_defence_effect_group()
                .sub_group("sea", r.unit_class_flag("Sea")))

    def _city_air_defence_effect_group():
        return (_city_defence_effect_group()
                .sub_group("air", r.unit_class_flag("Air")))

    def _city_missile_defence_effect_group():
        return (_city_defence_effect_group()
                .sub_group("missile", r.unit_class_flag("Missile")))

    def _standard():
        with _city_land_defence_effect_group() as g:
            g.from_city_size(1, 50)
            g.from_city_size(9, 50)
            g.with_building("City Walls", 50)
            g.with_wonder("Great Wall", 40)
        with _city_sea_defence_effect_group() as g:
            g.from_city_size(9, 50)
            g.with_building("Coastal Defense", 50)
        with _city_air_defence_effect_group() as g:
            g.with_building("SAM Battery", 50)
        with _city_missile_defence_effect_group() as g:
            g.with_building("SDI Defense I", 30)
            g.with_buildings(["SDI Defense I", "Palace"], 70)
            g.with_building_excluding_building(
                "SDI Defense II", "Palace", 30)
            g.with_building_excluding_building(
                "SDI Defense III", "Palace", 40)

    def _random():
        def _randomised():
            return mid_skewed_randint(-100, 100)

        def _random_positive():
            return mid_skewed_randint(1, 100)

        def _from_city_size(_g):
            if random_bool_pct(chaos):
                for size in range(1, 255):
                    if random_bool_pct(1 + (256 - size) // 16):
                        _g.from_city_size(size, _randomised())

        def _random_modifiers(_g):
            if random_bool_pct(chaos):
                _from_city_size(_g)
                _g.with_random_pct_of_buildings(5, _randomised)
                _g.with_random_pct_of_wonders(5, _randomised)
                _g.with_random_pct_of_govs(7, _randomised)
                _g.with_random_pct_of_techs(4, _randomised)

        with _city_land_defence_effect_group() as g:
            _random_modifiers(g)
            g.maybe_from_city_size(70, 1, _random_positive())
            g.maybe_from_city_size(70, 9, _random_positive())
            g.maybe_with_building(70, "City Walls", _random_positive())
            g.maybe_with_wonder(70, "Great Wall", _random_positive())
        with _city_sea_defence_effect_group() as g:
            _random_modifiers(g)
            g.maybe_from_city_size(70, 9, _random_positive())
            g.maybe_with_building(70, "Coastal Defense", _random_positive())
        with _city_air_defence_effect_group() as g:
            _random_modifiers(g)
            g.maybe_with_building(70, "SAM Battery", _random_positive())
        with _city_missile_defence_effect_group() as g:
            _random_modifiers(g)
            g.maybe_with_building(70, "SDI Defense I", _random_positive())
            g.maybe_with_buildings(
                70, ["SDI Defense I", "Palace"], _random_positive())
            g.maybe_with_building_excluding_building(
                70, "SDI Defense II", "Palace", _random_positive())
            g.maybe_with_building_excluding_building(
                70, "SDI Defense III", "Palace", _random_positive())

    return weighted_random_possibilities(
        stable_possibility(100, _standard),
        chaotic_possibility(100, _random),
    )()


def city_inspire_partisans():
    def _partisans_effect_group():
        return EffectGroup("Inspire_Partisans", "partisans",
                           r.tech("Conscription") +
                           r.tech_worldwide("Leadership") +
                           r.not_barbarian())

    def _standard():
        with _partisans_effect_group() as g:
            g.with_gov("Monarchy")
            g.with_gov("Fundamentalism")
            g.with_gov("Federation")
            g.with_gov("Republic")
            g.with_gov("Democracy")

    def _disabled():
        pass

    def _random():
        with _partisans_effect_group() as g:
            g.with_random_pct_of_govs(25)
            g.maybe_with_gov(75, "Monarchy")
            g.maybe_with_gov(75, "Fundamentalism")
            g.maybe_with_gov(75, "Federation")
            g.maybe_with_gov(75, "Republic")
            g.maybe_with_gov(75, "Democracy")
            g.with_random_pct_of_buildings(2)

    return weighted_random_possibilities(
        stable_possibility(100, _standard),
        chaotic_possibility(30, _disabled),
        chaotic_possibility(70, _random),
    )()


def city_nuclear_defence():
    def _nuclear_defence_effect_group():
        return EffectGroup("Nuke_Proof", "sdi")

    def _standard():
        with _nuclear_defence_effect_group() as g:
            g.with_building("SDI Defense I", 50)
            g.with_buildings(["SDI Defense I", "Palace"], 50)
            g.with_building_excluding_building("SDI Defense II", "Palace", 20)
            g.with_building_excluding_building("SDI Defense III", "Palace", 20)

    def _defenceless():
        pass

    def _random():
        def _random_positive():
            return min_skewed_randint(0, 100, skew=3)

        def _random_wild():
            return mid_skewed_randint(-100, 100, skew=2)

        def _randomised():
            return weighted_random_possibilities(
                possibility(70, _random_positive),
                possibility(30, _random_wild),
            )()

        with _nuclear_defence_effect_group() as g:
            g.with_random_pct_of_buildings(10, _randomised)
            g.with_random_pct_of_techs(10, _randomised)
            g.with_random_pct_of_wonders(15, _randomised)
            g.with_random_pct_of_govs(20, _randomised)
            g.maybe_with_building(70, "SDI Defense I", _random_positive())
            g.maybe_with_buildings(
                70, ["SDI Defense I", "Palace"], _random_positive())
            g.maybe_with_building_excluding_building(
                70, "SDI Defense II", "Palace", _random_positive())
            g.maybe_with_building_excluding_building(
                70, "SDI Defense III", "Palace", _random_positive())

    return weighted_random_possibilities(
        stable_possibility(100, _standard),
        chaotic_possibility(30, _defenceless),
        chaotic_possibility(70, _random),
    )()


def city_health_bonus():
    def _city_health_effect_group():
        return EffectGroup("Health_Pct", "city_health")

    def _standard():
        with _city_health_effect_group() as g:
            g.with_tech("Medicine", 30)
            g.with_building("Sewer System", 30)
            g.with_any_aqueduct(30)
            g.with_wonder("Cure For Cancer", 10)

    def _random():
        def _sensible():
            return mid_skewed_randint(1, 50)

        def _wild():
            return mid_skewed_randint(-100, 100, skew=2)

        def _randomised():
            return weighted_random_possibilities(
                possibility(70, _sensible),
                possibility(30, _wild),
            )()

        with _city_health_effect_group() as g:
            g.with_random_pct_of_techs(10, _randomised)
            g.with_random_pct_of_buildings(10, _randomised)
            g.with_random_pct_of_wonders(10, _randomised)
            g.with_random_pct_of_govs(20, _randomised)
            g.maybe_with_tech(70, "Medicine", _sensible())
            g.maybe_with_building(70, "Sewer System", _sensible())
            g.maybe_with_aqueduct(70, _sensible())
            g.maybe_with_wonder(70, "Cure For Cancer", _sensible())

    return weighted_random_possibilities(
        stable_possibility(100, _standard),
        chaotic_possibility(100, _random),
    )()


def city_disasters():
    # Every turn, every city rolls a number between 0 and 1,000,000 against
    # every disaster type. If it rolls below 'global' x 'disaster' frequency,
    # it occurs.

    def _disaster(name, frequency, chance=100, reqs=(), *effects):
        if random_bool_pct(chance):
            return {name: {
                "name": name,
                "reqs": reqs,
                "frequency": frequency,
                "effects": effects
            }}
        else:
            return ()

    def _earthquake(frequency, chance=100):
        return _disaster("Earthquake", frequency, chance,
                         r.on_terrain("Hills"),
                         "EmptyProdStock")

    def _flood(frequency, chance=100):
        return _disaster("Flood", frequency, chance,
                         r.adjacent_extra("River"),
                         "EmptyFoodStock")

    def _fire(frequency, chance=100):
        return _disaster("Fire", frequency, chance,
                         r.min_size(9),
                         "DestroyBuilding")

    def _industrial_accident(frequency, chance=100):
        return _disaster("Industrial Accident", frequency, chance,
                         r.building("Mfg. Plant"),
                         "ReducePopulation", "Pollution")

    def _nuclear_accident(frequency, chance=100):
        return _disaster("Nuclear Accident", frequency, chance,
                         r.building("Nuclear Plant"),
                         "ReducePopulation", "Fallout")

    def _standard():
        setting("cities.disasters.frequency", 10)
        setting("cities.disasters.disasters", (
                _earthquake(100)
                | _flood(100)
                | _fire(100)
                | _industrial_accident(100)
                | _nuclear_accident(100)
        ))

    def _disabled():
        setting("cities.disasters.frequency", 10)
        setting("cities.disasters.disasters", ())

    def _random():
        def _randomised():
            return mid_skewed_randint(1, 255)

        setting("cities.disasters.frequency", weighted_random_possibilities(
            stable_possibility(100, randint(1, 20)),
            chaotic_possibility(
                100, min_skewed_randint(1, 1000, skew=6)),
        ))
        setting("cities.disasters.disasters", (
                _earthquake(_randomised(), 80)
                | _flood(_randomised(), 80)
                | _fire(_randomised(), 80)
                | _industrial_accident(_randomised(), 80)
                | _nuclear_accident(_randomised(), 80)
        ))

    return weighted_random_possibilities(
        stable_possibility(70, _standard),
        stable_possibility(30, _disabled),
        chaotic_possibility(100, _random),
    )()


def city_food_waste():
    def _base_food_waste_effect_group():
        return EffectGroup("Output_Waste", "base_food_waste",
                           r.food())

    def _food_waste_by_distance_effect_group():
        return EffectGroup("Output_Waste_By_Distance", "food_waste_by_distance",
                           r.food())

    def _food_waste_reduction_effect_group():
        return EffectGroup("Output_Waste_Pct", "food_waste_reduction",
                           r.food())

    def _standard():
        with _food_waste_by_distance_effect_group() as g:
            g.excluding_gov("Anarchy", 50)
        with _food_waste_reduction_effect_group() as g:
            g.with_building("Granary", 50)
            g.with_building("Courthouse", 50)

    def _disabled():
        pass

    def _random():
        def _base():
            with _base_food_waste_effect_group() as g:
                g.maybe_base(30, randint(1, 50))

        def _distance():
            def _gov_distance_penalty():
                return mid_skewed_randint(1, 100)

            def _distance_modifier():
                return mid_skewed_randint(-100, 100, skew=3)

            def _standard_govs():
                with _food_waste_reduction_effect_group() as g:
                    g.excluding_gov("Anarchy", _gov_distance_penalty())

            def _random_govs():
                with _food_waste_by_distance_effect_group() as g:
                    g.with_random_pct_of_govs(70, _gov_distance_penalty)
                    g.with_random_pct_of_techs(10, _distance_modifier)
                    g.with_random_pct_of_buildings(10, _distance_modifier)
                    g.with_random_pct_of_wonders(10, _distance_modifier)

            weighted_random_possibilities(
                possibility(70, _standard_govs),
                possibility(30, _random_govs)
            )()

        def _reduction():
            def _positive():
                return randint(1, 100)

            def _wild():
                return mid_skewed_randint(-100, 100)

            def _randomised():
                return weighted_random_possibilities(
                    possibility(70, _positive),
                    possibility(30, _wild),
                )()

            with _food_waste_reduction_effect_group() as g:
                g.with_random_pct_of_buildings(15, _randomised)
                g.with_random_pct_of_wonders(10, _randomised)
                g.with_random_pct_of_techs(10, _randomised)
                g.with_random_pct_of_govs(20, _randomised)
                g.maybe_with_building(80, "Granary", _positive())
                g.maybe_with_building(80, "Courthouse", _positive())

        _base()
        _distance()
        _reduction()

    return weighted_random_possibilities(
        stable_possibility(70, _standard),
        stable_possibility(30, _disabled),
        chaotic_possibility(100, _random),
    )()


def city_food_worked_tile_penalty():
    def _tile_penalty_food_effect_group():
        return EffectGroup("Output_Penalty_Tile", "tile_penalty_food",
                           r.food())

    def _standard():
        with _tile_penalty_food_effect_group() as g:
            g.base_effect(2)
            g.excluding_govs(["Anarchy", "Tribal", "Despotism"], 65535)
            g.with_tech("Railroad", 65535)
            g.with_wonder("Pyramids", 65535)

    def _disabled():
        pass

    def _random():
        def _base():
            return weighted_random_possibilities(
                possibility(70, 2),
                possibility(30, mid_skewed_randint(0, 4)),
            )

        def _modifier():
            return weighted_random_possibilities(
                possibility(5, 65535),
                possibility(65, 1),
                possibility(20, -1),
            )

        with _tile_penalty_food_effect_group() as g:
            g.base_effect(_base())
            g.with_random_pct_of_buildings(5, _modifier)
            g.with_random_pct_of_wonders(10, _modifier)
            g.with_random_pct_of_govs(70, _modifier)
            g.with_random_pct_of_techs(10, _modifier)

    return weighted_random_possibilities(
        stable_possibility(100, _standard),
        stable_possibility(30, _disabled),
        chaotic_possibility(70, _random),
    )()


def city_food_worked_tile_bonus():
    def _tile_food_add_group():
        return EffectGroup("Output_Add_Tile", "tile_food_add", r.food())

    def _tile_food_inc_group():
        return EffectGroup("Output_Inc_Tile", "tile_food_inc", r.food())

    def _tile_food_inc_pct_group():
        return EffectGroup("Output_Per_Tile", "tile_food_inc_pct", r.food())

    def _standard():
        with _tile_food_inc_pct_group() as g:
            g.with_building_on_extra("Supermarket", "Farmland", 50)
            with g.on_city_auto_farmland_group() as f:
                f.with_building("Supermarket", 50)
        with _tile_food_add_group() as g:
            with g.on_sea_group() as s:
                s.with_building("Harbour", 1)

    def _random():
        def _positive_pct():
            return weighted_random_possibilities(
                possibility(70, mid_skewed_randint(1, 100)),
                possibility(30, min_skewed_randint(100, 1000, skew=2))
            )

        def _wild_pct():
            return mid_skewed_randint(-100, 100, skew=2)

        def _random_pct():
            return weighted_random_possibilities(
                possibility(70, _positive_pct),
                possibility(30, _wild_pct),
            )()

        def _positive():
            return weighted_random_possibilities(
                possibility(70, 1),
                possibility(30, min_skewed_randint(1, 4)),
            )

        def _wild():
            return weighted_random_possibilities(
                possibility(60, min_skewed_randint(1, 4, skew=2)),
                possibility(40, -min_skewed_randint(1, 4, skew=2)),
            )

        def _randomised():
            return weighted_random_possibilities(
                possibility(70, _positive),
                possibility(30, _wild),
            )()

        with _tile_food_inc_pct_group() as g:
            g.with_random_pct_of_buildings_on_extras(10, _random_pct)
            g.with_random_pct_of_wonders_on_extras(10, _random_pct)
            g.with_random_pct_of_techs_on_extras(10, _random_pct)
            g.with_random_pct_of_govs_on_extras(10, _random_pct)
            g.with_random_pct_of_buildings_on_terrain(10, _random_pct)
            g.with_random_pct_of_wonders_on_terrain(10, _random_pct)
            g.with_random_pct_of_techs_on_terrain(10, _random_pct)
            g.with_random_pct_of_govs_on_terrain(10, _random_pct)
            if random_bool_pct(80):
                with g.on_farmland_group() as f:
                    f.with_building("Supermarket", _positive_pct())
                with g.on_city_auto_farmland_group() as f:
                    f.with_building("Supermarket", _positive_pct())
        with _tile_food_inc_group() as g:
            g.with_random_pct_of_buildings_on_extras(10, _randomised)
            g.with_random_pct_of_wonders_on_extras(10, _randomised)
            g.with_random_pct_of_techs_on_extras(10, _randomised)
            g.with_random_pct_of_govs_on_extras(10, _randomised)
            g.with_random_pct_of_buildings_on_terrain(10, _randomised)
            g.with_random_pct_of_wonders_on_terrain(10, _randomised)
            g.with_random_pct_of_techs_on_terrain(10, _randomised)
            g.with_random_pct_of_govs_on_terrain(10, _randomised)
        with _tile_food_add_group() as g:
            g.with_random_pct_of_buildings_on_extras(10, _randomised)
            g.with_random_pct_of_wonders_on_extras(10, _randomised)
            g.with_random_pct_of_techs_on_extras(10, _randomised)
            g.with_random_pct_of_govs_on_extras(10, _randomised)
            g.with_random_pct_of_buildings_on_terrain(10, _randomised)
            g.with_random_pct_of_wonders_on_terrain(10, _randomised)
            g.with_random_pct_of_techs_on_terrain(10, _randomised)
            g.with_random_pct_of_govs_on_terrain(10, _randomised)
            with g.on_sea_group() as s:
                s.with_building("Harbour", _positive())

    return weighted_random_possibilities(
        stable_possibility(100, _standard),
        chaotic_possibility(100, _random),
    )()


def city_irrigation_bonus_pct():
    def _irrigation_pct_group():
        return EffectGroup(
            "Irrigation_Pct", "irrigation_pct", (),
            [
                OrGroup.on_irrigation(),
                OrGroup.on_city_auto_irrigation()
            ]
        )

    def _standard():
        with _irrigation_pct_group() as g:
            g.base_effect(100)
            g.on_flood_plain(100)

    def _random():
        def _positive():
            return mid_skewed_randint(1, 200)

        def _wild():
            return weighted_random_possibilities(
                possibility(70,
                            min_skewed_randint(1, 400, skew=2)),
                possibility(30, -min_skewed_randint(0, 99))
            )

        def _randomised():
            return weighted_random_possibilities(
                possibility(70, _positive),
                possibility(30, _wild),
            )()

        with _irrigation_pct_group() as g:
            g.base_effect(weighted_random_possibilities(
                possibility(80, 100),
                possibility(20, _positive())
            ))
            if random_bool_pct(80):
                g.on_flood_plain(_positive())
            if random_bool_pct(20):
                g.with_random_pct_of_terrain(90, _randomised)

    return weighted_random_possibilities(
        stable_possibility(100, _standard),
        chaotic_possibility(100, _random),
    )


def city_size_trade_restriction():
    def _standard():
        setting("cities.trade.noTradeBelowSize", 0)
        setting("cities.trade.fullTradeAtSize", 1)

    def _random():
        _min = min_skewed_randint(1, 255, skew=5)
        setting("cities.trade.noTradeBelowSize", _min)
        setting("cities.trade.fullTradeAtSize",
                min_skewed_randint(_min + 1, 255, skew=5))

    return weighted_random_possibilities(
        stable_possibility(100, _standard),
        chaotic_possibility(100, _random),
    )()


def city_trade_worked_tile_bonus():
    def _trade_add_group():
        return EffectGroup("Output_Add_Tile", "tile_trade_add",
                           r.output_type("Trade"))

    def _trade_inc_group():
        return EffectGroup("Output_Inc_Tile", "tile_trade_inc",
                           r.output_type("Trade"))

    def _trade_inc_pct_group():
        return EffectGroup("Output_Per_Tile", "tile_trade_inc_pct",
                           r.output_type("Trade"))

    def _trade_celebration_inc_group():
        return EffectGroup("Output_Inc_Tile_Celebrate", "tile_trade_celebrate",
                           r.output_type("Trade"))

    def _standard():
        with _trade_inc_group() as g:
            g.with_gov("City States", 1)
            g.with_gov_on_land("Republic", 1)
            g.with_gov_on_land("Democracy", 1)
            g.with_building("Colossus", 1)
            g.with_building("Atlantic Telegraph Company", 1)
            g.on_extra("Ruins", 1)
            g.on_super_highways(1)
        with _trade_celebration_inc_group() as g:
            g.with_gov("Monarchy", 1)
            g.with_gov("Federation", 1)
            g.with_gov("Republic", 1)
            g.with_gov("Democracy", 1)
            g.with_gov("City States", 1)

    def _random():
        def _positive_pct():
            return weighted_random_possibilities(
                possibility(70, mid_skewed_randint(1, 100)),
                possibility(30, min_skewed_randint(100, 1000, skew=2))
            )

        def _wild_pct():
            return mid_skewed_randint(-100, 100, skew=2)

        def _random_pct():
            return weighted_random_possibilities(
                possibility(70, _positive_pct),
                possibility(30, _wild_pct),
            )()

        def _positive():
            return weighted_random_possibilities(
                possibility(70, 1),
                possibility(30, min_skewed_randint(1, 4)),
            )

        def _wild():
            return weighted_random_possibilities(
                possibility(60, min_skewed_randint(1, 4, skew=2)),
                possibility(40, -min_skewed_randint(1, 4, skew=2)),
            )

        def _randomised():
            return weighted_random_possibilities(
                possibility(70, _positive),
                possibility(30, _wild),
            )()

        if random_bool_pct(chaos):
            with _trade_inc_pct_group() as g:
                g.with_random_pct_of_buildings_on_extras(10, _random_pct)
                g.with_random_pct_of_wonders_on_extras(10, _random_pct)
                g.with_random_pct_of_techs_on_extras(10, _random_pct)
                g.with_random_pct_of_govs_on_extras(10, _random_pct)
                g.with_random_pct_of_buildings_on_terrain(10, _random_pct)
                g.with_random_pct_of_wonders_on_terrain(10, _random_pct)
                g.with_random_pct_of_techs_on_terrain(10, _random_pct)
                g.with_random_pct_of_govs_on_terrain(10, _random_pct)

        with _trade_inc_group() as g:
            g.with_random_pct_of_buildings_on_extras(10, _randomised)
            g.with_random_pct_of_wonders_on_extras(10, _randomised)
            g.with_random_pct_of_techs_on_extras(10, _randomised)
            g.with_random_pct_of_govs_on_extras(10, _randomised)
            g.with_random_pct_of_buildings_on_terrain(10, _randomised)
            g.with_random_pct_of_wonders_on_terrain(10, _randomised)
            g.with_random_pct_of_techs_on_terrain(10, _randomised)
            g.with_random_pct_of_govs_on_terrain(10, _randomised)
            g.maybe_with_gov(70, "City States", 1)
            g.maybe_with_gov_on_land(70, "Republic", 1)
            g.maybe_with_gov_on_land(70, "Democracy", 1)
            g.maybe_with_building(70, "Colossus", 1)
            g.maybe_with_building(70, "Atlantic Telegraph Company", 1)
            g.maybe_on_extra(70, "Ruins", 1)
            if random_bool_pct(70):
                g.on_super_highways(_positive())

        with _trade_add_group() as g:
            g.with_random_pct_of_buildings_on_extras(10, _randomised)
            g.with_random_pct_of_wonders_on_extras(10, _randomised)
            g.with_random_pct_of_techs_on_extras(10, _randomised)
            g.with_random_pct_of_govs_on_extras(10, _randomised)
            g.with_random_pct_of_buildings_on_terrain(10, _randomised)
            g.with_random_pct_of_wonders_on_terrain(10, _randomised)
            g.with_random_pct_of_techs_on_terrain(10, _randomised)
            g.with_random_pct_of_govs_on_terrain(10, _randomised)

        with _trade_celebration_inc_group() as g:
            g.with_random_pct_of_buildings_on_extras(10, _randomised)
            g.with_random_pct_of_wonders_on_extras(10, _randomised)
            g.with_random_pct_of_techs_on_extras(10, _randomised)
            g.with_random_pct_of_govs_on_extras(10, _randomised)
            g.with_random_pct_of_buildings_on_terrain(10, _randomised)
            g.with_random_pct_of_wonders_on_terrain(10, _randomised)
            g.with_random_pct_of_techs_on_terrain(10, _randomised)
            g.with_random_pct_of_govs_on_terrain(10, _randomised)
            g.maybe_with_gov(70, "Monarchy", 1)
            g.maybe_with_gov(70, "Federation", 1)
            g.maybe_with_gov(70, "Republic", 1)
            g.maybe_with_gov(70, "Democracy", 1)
            g.maybe_with_gov(70, "City States", 1)

    return weighted_random_possibilities(
        stable_possibility(100, _standard),
        chaotic_possibility(100, _random),
    )()


def city_trade_worked_tile_penalty():
    def _tile_penalty_trade_group():
        return EffectGroup("Output_Penalty_Tile", "tile_penalty_trade",
                           r.output_type("Trade"))

    def _standard():
        with _tile_penalty_trade_group() as g:
            g.base_effect(2)
            g.excluding_govs(["Anarchy", "Tribal", "Despotism"], 65535)
            g.with_tech("Railroad", 65535)
            g.with_wonder("Pyramids", 65535)

    def _disabled():
        pass

    def _random():
        def _base():
            return weighted_random_possibilities(
                possibility(70, 2),
                possibility(30, mid_skewed_randint(0, 4)),
            )

        def _modifier():
            return weighted_random_possibilities(
                possibility(5, 65535),
                possibility(70, 1),
                possibility(25, -1),
            )

        with _tile_penalty_trade_group() as g:
            g.base_effect(_base())
            g.with_random_pct_of_buildings(5, _modifier)
            g.with_random_pct_of_wonders(10, _modifier)
            g.with_random_pct_of_govs(70, _modifier)
            g.with_random_pct_of_techs(10, _modifier)

    return weighted_random_possibilities(
        stable_possibility(100, _standard),
        stable_possibility(30, _disabled),
        chaotic_possibility(70, _random),
    )()


def city_trade_output_bonus_pct():
    def _trade_bonus_pct_group():
        return EffectGroup("Output_Bonus", "trade_effect_bonus",
                           r.output_type("Trade"))

    def _standard():
        with _trade_bonus_pct_group() as g:
            g.with_wonder_worldwide("Marco Polo's Embassy", 30)
            g.with_wonder("Trade Company", 10)
            g.from_city_size(9, 10)
            g.from_city_size(17, 10)
            g.from_city_size(30, 10)

    def _random():
        def _positive_pct():
            return min_skewed_randint(1, 100, skew=3)

        def _random_pct():
            return weighted_random_possibilities(
                possibility(60, min_skewed_randint(1, 100, skew=4)),
                possibility(40, -min_skewed_randint(1, 100, skew=4)),
            )

        with _trade_bonus_pct_group() as g:
            g.with_random_pct_of_buildings(15, _random_pct)
            g.with_random_pct_of_wonders(10, _random_pct)
            g.with_random_pct_of_techs(10, _random_pct)
            g.with_random_pct_of_govs(30, _random_pct)
            g.maybe_with_wonder_worldwide(70, "Marco Polo's Embassy",
                                          _positive_pct())
            g.maybe_with_wonder(70, "Trade Company", _positive_pct())
            for size in range(1, 255):
                if random_bool_pct(1):
                    g.from_city_size(size, _positive_pct())
            g.maybe_from_city_size(70, 9, _positive_pct())
            g.maybe_from_city_size(70, 17, _positive_pct())
            g.maybe_from_city_size(70, 30, _positive_pct())

    return weighted_random_possibilities(
        stable_possibility(100, _standard),
        chaotic_possibility(100, _random),
    )()


def city_trade_waste():
    def _base_pct_group():
        return EffectGroup("Output_Waste", "base_trade_waste",
                           r.output_type("Trade"))

    def _dist_group():
        return EffectGroup("Output_Waste_By_Distance",
                           "trade_waste_by_distance",
                           r.output_type("Trade"))

    def _reduction_group():
        return EffectGroup("Output_Waste_Pct", "trade_waste_reduction",
                           r.output_type("Trade"))

    def _primitive_waste():
        return Effect("primitive", 200,
                      r.not_gov("Communism")
                      + r.not_gov("Federation")
                      + r.not_tech("The Corporation"))

    def _early_federation():
        return Effect("early_federation", 100,
                      r.gov("Federation")
                      + r.not_tech("The Corporation"))

    def _simple_corporate():
        return Effect("simple_corporate", 100,
                      r.tech("The Corporation")
                      + r.not_gov("Federation")
                      + r.not_gov("Communism"))

    def _standard():
        with _base_pct_group() as g:
            g.with_gov("Tribal", 30)
            g.with_gov("Despotism", 20)
            g.with_gov("City States", 20)
            g.with_gov("Monarchy", 10)
            g.with_gov("Communism", 30)
            g.with_gov("Fundamentalism", 15)
            g.with_gov("Federation", 0)
            g.with_gov("Republic", 25)
            g.with_gov("Democracy", 5)
        with _dist_group() as g:
            g.add_effect(_primitive_waste())
            g.add_effect(_early_federation())
            g.add_effect(_simple_corporate())
        with _reduction_group() as g:
            g.with_building("Courthouse", 50)
            g.with_any_palace(50)

    def _disabled():
        pass

    def _random():
        def _base_only():
            with _base_pct_group() as g:
                g.base_effect(randint(1, 50))

        def _by_gov():
            with _base_pct_group() as g:
                g.with_random_pct_of_govs(70, lambda: randint(1, 50))

        def _distance():
            return weighted_random_possibilities(
                possibility(60, -min_skewed_randint(1, 400, skew=3)),
                possibility(40, min_skewed_randint(1, 400, skew=3)),
            )

        def _positive():
            return randint(1, 100)

        def _wild():
            return mid_skewed_randint(-100, 100)

        def _randomised():
            return weighted_random_possibilities(
                possibility(70, _positive),
                possibility(30, _wild),
            )()

        weighted_random_possibilities(
            possibility(20, _disabled),
            possibility(30, _base_only),
            possibility(50, _by_gov),
        )()
        with _dist_group() as g:
            g.base_effect(mid_skewed_randint(1, 400))
            g.with_random_pct_of_wonders(10, _distance)
            g.with_random_pct_of_techs(10, _distance)
            g.with_random_pct_of_govs(20, _distance)
            g.maybe_with_gov(80, "Federation", -mid_skewed_randint(1, 200))
            g.maybe_with_gov(80, "Communism", -mid_skewed_randint(1, 400))
            g.maybe_with_tech(80, "The Corporation",
                              -mid_skewed_randint(1, 200))
        with _reduction_group() as g:
            g.with_random_pct_of_buildings(15, _randomised)
            g.with_random_pct_of_wonders(10, _randomised)
            g.with_random_pct_of_techs(10, _randomised)
            g.with_random_pct_of_govs(20, _randomised)
            g.maybe_with_building(80, "Courthouse", _positive())
            g.maybe_with_palace(80, _positive())

    weighted_random_possibilities(
        stable_possibility(100, _standard),
        chaotic_possibility(30, _disabled),
        chaotic_possibility(70, _random),
    )()


def city_unit_batch_production():
    def _group():
        return EffectGroup("City_Build_Slots")

    def _standard():
        with _group() as g:
            g.base_effect(3)
            g.with_building("Mfg. Plant", 1)

    def _disabled():
        pass

    def _random():
        def _positive():
            return randint(1, 2)

        def _randomised():
            return weighted_random_possibilities(
                possibility(60, min_skewed_randint(1, 5, skew=2)),
                possibility(40, -min_skewed_randint(1, 5, skew=2)),
            )

        with _group() as g:
            g.base_effect(mid_skewed_randint(1, 5))
            g.with_random_pct_of_buildings(20, _randomised)
            g.with_random_pct_of_govs(20, _randomised)
            g.with_random_pct_of_techs(5, _randomised)
            g.with_random_pct_of_wonders(5, _randomised)
            g.maybe_with_building(70, "Mfg. Plant", _positive())

    weighted_random_possibilities(
        stable_possibility(100, _standard),
        chaotic_possibility(50, _disabled),
        chaotic_possibility(50, _random),
    )()


def city_production_output_bonus_pct():
    def _shield_output_bonus_pct_group():
        return EffectGroup("Output_Bonus", "shield_output_bonus",
                           r.output_type("Shield"))

    def _the_paris_agreement(value):
        return Effect("special_the_paris_agreement", value,
                      r.wonder_worldwide("The Paris Agreement") +
                      r.not_gov("Communism") +
                      r.not_gov("Anarchy") +
                      r.not_gov("Fundamentalism") +
                      r.not_gov("City States") +
                      r.not_wonder_worldwide("Global Emission Union"))

    def _global_emissions_union(value):
        return Effect("special_global_emission_union", value,
                      r.wonder_worldwide("Global Emission Union") +
                      r.not_gov("Anarchy"))

    def _standard():
        with _shield_output_bonus_pct_group() as g:
            g.with_building_and_gov("Workshop", "Monarchy", 30)
            g.with_building_and_gov("Workshop", "Republic", 30)
            g.with_building_and_gov("Workshop", "City States", 30)
            g.with_building("Occupation Government", -50)
            with g.with_building_group("Factory") as f:
                f.base_effect(50)
                with f.first_match_in_group() as m:
                    m.with_building("Hoover Dam", 100)
                    m.with_building("Solar Plant", 50)
                    m.with_building("Hydro Plant", 50)
                    m.with_building("Nuclear Plant", 75)
                    m.with_building("Power Plant", 50)
            with g.with_building_group("Mfg. Plant") as p:
                p.base_effect(50)
                with p.first_match_in_group() as m:
                    m.with_building("Hoover Dam", 100)
                    m.with_building("Solar Plant", 50)
                    m.with_building("Hydro Plant", 50)
                    m.with_building("Nuclear Plant", 75)
                    m.with_building("Power Plant", 50)
            g.add_effect(_the_paris_agreement(-25))
            g.add_effect(_global_emissions_union(-20))

    def _random():
        def _positive_pct(_factor=1.0):
            return min_skewed_randint(1, round(100 * _factor), skew=1)

        def _negative_pct(_factor=1.0):
            return -min_skewed_randint(1, round(100 * _factor), skew=1)

        def _random_pct():
            return weighted_random_possibilities(
                possibility(60, min_skewed_randint(1, 100, skew=4)),
                possibility(40, -min_skewed_randint(1, 100, skew=4)),
            )

        with _shield_output_bonus_pct_group() as g:
            g.with_random_pct_of_buildings(15, _random_pct)
            g.with_random_pct_of_wonders(10, _random_pct)
            g.with_random_pct_of_techs(10, _random_pct)
            g.with_random_pct_of_govs(30, _random_pct)
            g.maybe_with_building_and_gov(70, "Workshop", "Monarchy",
                                          _positive_pct())
            g.maybe_with_building_and_gov(70, "Workshop", "Republic",
                                          _positive_pct())
            g.maybe_with_building_and_gov(70, "Workshop", "City States",
                                          _positive_pct())
            if random_bool_pct(70):
                with g.with_building_group("Factory") as f:
                    f.base_effect(_positive_pct(2))
                    with f.first_match_in_group() as m:
                        m.with_building("Hoover Dam", _positive_pct(4))
                        m.with_building("Solar Plant", _positive_pct(2))
                        m.with_building("Hydro Plant", _positive_pct(2))
                        m.with_building("Nuclear Plant", _positive_pct(3))
                        m.with_building("Power Plant", _positive_pct(2))
                with g.with_building_group("Mfg. Plant") as p:
                    p.base_effect(_positive_pct(2))
                    with f.first_match_in_group() as m:
                        m.with_building("Hoover Dam", _positive_pct(4))
                        m.with_building("Solar Plant", _positive_pct(2))
                        m.with_building("Hydro Plant", _positive_pct(2))
                        m.with_building("Nuclear Plant", _positive_pct(3))
                        m.with_building("Power Plant", _positive_pct(2))
            g.maybe_add_effect(70, _the_paris_agreement(_negative_pct()))
            g.maybe_add_effect(70, _global_emissions_union(_negative_pct()))
            g.maybe_with_building(70, "Occupation Government", _negative_pct(2))

    return weighted_random_possibilities(
        stable_possibility(100, _standard),
        chaotic_possibility(100, _random),
    )()


def city_production_worked_tile_bonus():
    def _add_group():
        return EffectGroup("Output_Add_Tile", "tile_production_add",
                           r.output_type("Shield"))

    def _inc_group():
        return EffectGroup("Output_Add_Tile", "tile_production_increase",
                           r.output_type("Shield"))

    def _inc_pct_group():
        return EffectGroup("Output_Add_Tile", "tile_production_inc_pct",
                           r.output_type("Shield"))

    def _celebration_group():
        return EffectGroup("Output_Add_Tile", "tile_production_celebrate",
                           r.output_type("Shield"))

    def _offshore_platform_shallow(value):
        return Effect("special_offshore_platform_shallow", value,
                      r.building("Offshore Platform") +
                      r.at_sea() +
                      r.not_on_terrain("Deep Ocean"))

    def _offshore_platform_deep(value):
        return Effect("special_offshore_platform_deep", value,
                      r.building("Offshore Platform") +
                      r.on_terrain("Deep Ocean") +
                      r.on_extra("Oil Platform"))

    def _standard():
        with _add_group() as g:
            g.add_effect(_offshore_platform_shallow(1))
            g.add_effect(_offshore_platform_deep(1))
        with _inc_group() as g:
            g.with_building("Pyramids", 1)

    def _random():
        def _positive_pct():
            return weighted_random_possibilities(
                possibility(70, mid_skewed_randint(1, 100)),
                possibility(30, min_skewed_randint(100, 1000, skew=2))
            )

        def _wild_pct():
            return mid_skewed_randint(-100, 100, skew=2)

        def _random_pct():
            return weighted_random_possibilities(
                possibility(70, _positive_pct),
                possibility(30, _wild_pct),
            )()

        def _positive():
            return weighted_random_possibilities(
                possibility(70, 1),
                possibility(30, min_skewed_randint(1, 4)),
            )

        def _wild():
            return weighted_random_possibilities(
                possibility(60, min_skewed_randint(1, 4, skew=2)),
                possibility(40, -min_skewed_randint(1, 4, skew=2)),
            )

        def _randomised():
            return weighted_random_possibilities(
                possibility(70, _positive),
                possibility(30, _wild),
            )()

        if random_bool_pct(chaos):
            with _inc_pct_group() as g:
                g.with_random_pct_of_buildings_on_extras(10, _random_pct)
                g.with_random_pct_of_wonders_on_extras(10, _random_pct)
                g.with_random_pct_of_techs_on_extras(10, _random_pct)
                g.with_random_pct_of_govs_on_extras(10, _random_pct)
                g.with_random_pct_of_buildings_on_terrain(10, _random_pct)
                g.with_random_pct_of_wonders_on_terrain(10, _random_pct)
                g.with_random_pct_of_techs_on_terrain(10, _random_pct)
                g.with_random_pct_of_govs_on_terrain(10, _random_pct)
        with _inc_group() as g:
            g.maybe_with_building(70, "Pyramids", 1)
            g.with_random_pct_of_buildings_on_extras(10, _randomised)
            g.with_random_pct_of_wonders_on_extras(10, _randomised)
            g.with_random_pct_of_techs_on_extras(10, _randomised)
            g.with_random_pct_of_govs_on_extras(10, _randomised)
            g.with_random_pct_of_buildings_on_terrain(10, _randomised)
            g.with_random_pct_of_wonders_on_terrain(10, _randomised)
            g.with_random_pct_of_techs_on_terrain(10, _randomised)
            g.with_random_pct_of_govs_on_terrain(10, _randomised)
        with _add_group() as g:
            g.with_random_pct_of_buildings_on_extras(10, _randomised)
            g.with_random_pct_of_wonders_on_extras(10, _randomised)
            g.with_random_pct_of_techs_on_extras(10, _randomised)
            g.with_random_pct_of_govs_on_extras(10, _randomised)
            g.with_random_pct_of_buildings_on_terrain(10, _randomised)
            g.with_random_pct_of_wonders_on_terrain(10, _randomised)
            g.with_random_pct_of_techs_on_terrain(10, _randomised)
            g.with_random_pct_of_govs_on_terrain(10, _randomised)
            g.maybe_add_effect(70, _offshore_platform_shallow(_positive()))
            g.maybe_add_effect(70, _offshore_platform_deep(_positive()))
        if random_bool_pct(chaos):
            with _celebration_group() as g:
                g.with_random_pct_of_buildings_on_extras(10, _randomised)
                g.with_random_pct_of_wonders_on_extras(10, _randomised)
                g.with_random_pct_of_techs_on_extras(10, _randomised)
                g.with_random_pct_of_govs_on_extras(10, _randomised)
                g.with_random_pct_of_buildings_on_terrain(10, _randomised)
                g.with_random_pct_of_wonders_on_terrain(10, _randomised)
                g.with_random_pct_of_techs_on_terrain(10, _randomised)
                g.with_random_pct_of_govs_on_terrain(10, _randomised)

    return weighted_random_possibilities(
        stable_possibility(100, _standard),
        chaotic_possibility(100, _random),
    )()


def city_production_worked_tile_penalty():
    def _worked_tile_penalty_group():
        return EffectGroup("Output_Penalty_Tile", "worked_tile_penalty",
                           r.output_type("Shield"))

    def _standard():
        with _worked_tile_penalty_group() as g:
            g.base_effect(2)
            g.excluding_govs(["Anarchy", "Tribal", "Despotism"], 65535)
            g.with_tech("Railroad", 65535)
            g.with_wonder("Pyramids", 65535)

    def _disabled():
        pass

    def _random():
        def _base():
            return weighted_random_possibilities(
                possibility(70, 2),
                possibility(30, mid_skewed_randint(0, 4)),
            )

        def _modifier():
            return weighted_random_possibilities(
                possibility(5, 65535),
                possibility(65, 1),
                possibility(20, -1),
            )

        with _worked_tile_penalty_group() as g:
            g.base_effect(_base())
            g.with_random_pct_of_buildings(5, _modifier)
            g.with_random_pct_of_wonders(10, _modifier)
            g.with_random_pct_of_govs(70, _modifier)
            g.with_random_pct_of_techs(10, _modifier)

    return weighted_random_possibilities(
        stable_possibility(100, _standard),
        stable_possibility(30, _disabled),
        chaotic_possibility(70, _random),
    )()


def city_production_waste():
    def _base_waste_group():
        return EffectGroup("Output_Waste", "base_production_waste",
                           r.output_type("Shield"))

    def _waste_by_dist_group():
        return EffectGroup("Output_Waste_By_Distance", "base_production_waste",
                           r.output_type("Shield"))

    def _waste_reduction_group():
        return EffectGroup("Output_Waste_Pct", "base_production_waste",
                           r.output_type("Shield"))

    def _add_gov(gov: GovernmentType, base: int, per_dist: int, trade: int = 0):
        if base:
            with _base_waste_group() as g:
                g.with_gov(gov, base)
        if per_dist:
            with _waste_by_dist_group() as g:
                g.with_gov(gov, per_dist)
        if trade:
            with _waste_by_dist_group() as g:
                g.with_gov_and_tech(gov, "Trade", -trade)

    def _maybe_add_gov(pct: int, gov: GovernmentType, base: int, per_dist: int,
                       trade: int = 0):
        if random_bool_pct(pct):
            _add_gov(gov, base, per_dist, trade)

    def _standard():
        _add_gov("Anarchy", base=30, per_dist=200, trade=100)
        _add_gov("Tribal", base=0, per_dist=300, trade=100)
        _add_gov("Despotism", base=10, per_dist=300, trade=100)
        _add_gov("Monarchy", base=10, per_dist=200, trade=100)
        _add_gov("City States", base=10, per_dist=500, trade=100)
        _add_gov("Republic", base=20, per_dist=200, trade=100)
        _add_gov("Democracy", base=25, per_dist=200, trade=100)
        _add_gov("Fundamentalism", base=15, per_dist=200, trade=100)
        _add_gov("Communism", base=0, per_dist=0)
        _add_gov("Federation", base=30, per_dist=0)
        with _waste_reduction_group() as g:
            g.with_building("Courthouse", 50)
            g.with_any_palace(50)

    def _disabled():
        pass

    def _random():
        def _base():
            return randint(1, 50)

        def _dist_base():
            return mid_skewed_randint(1, 400)

        def _dist_mod():
            return weighted_random_possibilities(
                possibility(60, -min_skewed_randint(1, 400, skew=3)),
                possibility(40, min_skewed_randint(1, 400, skew=3)),
            )

        def _reduction():
            return randint(1, 100)

        def _wild_reduction():
            return mid_skewed_randint(-100, 100)

        def _rand_reduction():
            return weighted_random_possibilities(
                possibility(70, _reduction),
                possibility(30, _wild_reduction),
            )()

        with _base_waste_group() as g:
            g.with_random_pct_of_govs(90, _base)
        with _waste_by_dist_group() as g:
            g.with_random_pct_of_govs(80, _dist_base)
            g.with_random_pct_of_wonders(10, _dist_mod)
            g.with_random_pct_of_techs(10, _dist_mod)
        with _waste_reduction_group() as g:
            g.with_random_pct_of_buildings(15, _rand_reduction)
            g.maybe_with_building(70, "Courthouse", _reduction())
            g.maybe_with_any_palace(70, _reduction())
            g.with_random_pct_of_wonders(10, _rand_reduction)
            g.with_random_pct_of_techs(10, _rand_reduction)
            g.with_random_pct_of_govs(20, _rand_reduction)
        _maybe_add_gov(70, "Anarchy", base=30, per_dist=200, trade=100)
        _maybe_add_gov(70, "Tribal", base=0, per_dist=300, trade=100)
        _maybe_add_gov(70, "Despotism", base=10, per_dist=300, trade=100)
        _maybe_add_gov(70, "Monarchy", base=10, per_dist=200, trade=100)
        _maybe_add_gov(70, "City States", base=10, per_dist=500, trade=100)
        _maybe_add_gov(70, "Republic", base=20, per_dist=200, trade=100)
        _maybe_add_gov(70, "Democracy", base=25, per_dist=200, trade=100)
        _maybe_add_gov(70, "Fundamentalism", base=15, per_dist=200, trade=100)
        _maybe_add_gov(70, "Communism", base=0, per_dist=0)
        _maybe_add_gov(70, "Federation", base=30, per_dist=0)

    return weighted_random_possibilities(
        stable_possibility(100, _standard),
        chaotic_possibility(30, _disabled),
        chaotic_possibility(70, _random),
    )()


def city_scientists_output():
    def _scientists_group():
        return EffectGroup("Specialist_Output", "scientist_bonus",
                           r.output_type("Science") +
                           r.specialist("Scientist"))

    def _standard():
        with _scientists_group() as g:
            g.base_effect(2)
            g.after_wonder_worldwide("Darwin's Voyage", 1)

    def _random():
        def _positive():
            return randint(1, 2)

        def _wacky():
            return mid_skewed_randint(-100, 100, skew=5)

        def _no_bonuses():
            pass

        def _random_bonuses():
            with _scientists_group() as g:
                g.maybe_after_wonder_worldwide(70, "Darwin's Voyage",
                                               _positive())
                g.maybe_with_random_pct_of_buildings(30, 5, _positive)
                g.maybe_with_random_pct_of_wonders(30, 5, _positive)
                g.maybe_with_random_pct_of_techs(30, 5, _positive)
                g.maybe_with_random_pct_of_govs(30, 20, _positive)

        def _wacky_bonuses():
            with _scientists_group() as g:
                g.with_random_pct_of_wonders(20, _wacky)
                g.with_random_pct_of_buildings(15, _wacky)
                g.with_random_pct_of_govs(50, _wacky)
                g.with_random_pct_of_techs(20, _wacky)

        with _scientists_group() as g:
            g.base_effect(weighted_random_possibilities(
                possibility(70, randint(1, 3)),
                possibility(30, min_skewed_randint(1, 100, skew=6)),
            ))
        weighted_random_possibilities(
            possibility(30, _no_bonuses),
            possibility(60, _random_bonuses),
            possibility(10, _wacky_bonuses),
        )()

    return weighted_random_possibilities(
        stable_possibility(80, _standard),
        chaotic_possibility(100, _random),
    )()


def city_taxmen_output():
    def _taxmen_group():
        return EffectGroup("Specialist_Output", "taxmen_bonus",
                           r.output_type("Gold") +
                           r.specialist("Taxman"))

    def _standard():
        with _taxmen_group() as g:
            g.base_effect(2)
            g.after_wonder_worldwide("A.Smith's Trading Co.", 1)

    def _random():
        def _positive():
            return randint(1, 2)

        def _wacky():
            return mid_skewed_randint(-100, 100, skew=5)

        def _no_bonuses():
            pass

        def _base():
            with _taxmen_group() as g:
                g.base_effect(weighted_random_possibilities(
                    possibility(70, randint(1, 3)),
                    possibility(30, min_skewed_randint(1, 100, skew=6)),
                ))

        def _random_bonuses():
            with _taxmen_group() as g:
                g.maybe_after_wonder_worldwide(70, "A.Smith's Trading Co.",
                                               _positive())
                g.maybe_with_random_pct_of_buildings(30, 5, _positive)
                g.maybe_with_random_pct_of_wonders(30, 5, _positive)
                g.maybe_with_random_pct_of_techs(30, 5, _positive)
                g.maybe_with_random_pct_of_govs(30, 20, _positive)

        def _wacky_bonuses():
            with _taxmen_group() as g:
                g.with_random_pct_of_wonders(20, _wacky)
                g.with_random_pct_of_buildings(15, _wacky)
                g.with_random_pct_of_govs(50, _wacky)
                g.with_random_pct_of_techs(20, _wacky)

        _base()
        weighted_random_possibilities(
            possibility(30, _no_bonuses),
            possibility(60, _random_bonuses),
            possibility(10, _wacky_bonuses),
        )()

    return weighted_random_possibilities(
        stable_possibility(80, _standard),
        chaotic_possibility(100, _random),
    )()


def city_tile_science_bonus():
    def _centre_tile_group():
        return EffectGroup("Output_Add_Tile", "city_tile_science",
                           r.on_city() + r.output_type("Science"))

    def _standard():
        with _centre_tile_group() as g:
            g.with_building("School of Baudhayana sutras", 4)
            g.with_building("Great Library", 10)
            g.with_building("Isaac Newton's College", 12)
            g.with_wonder("Darwin's Voyage", 1)

    def _random():
        def _building_bonus():
            return min_skewed_randint(1, 100, skew=3)

        def _wonder_bonus():
            return min_skewed_randint(1, 100, skew=5)

        with _centre_tile_group() as g:
            g.with_random_pct_of_buildings(10, _building_bonus)
            g.with_random_pct_of_wonders(10, _wonder_bonus)
            g.maybe_with_random_pct_of_govs(30, 50, _wonder_bonus)
            g.maybe_with_random_pct_of_techs(30, 10, _wonder_bonus)
            g.maybe_with_building(70, "School of Baudhayana sutras",
                                  _building_bonus())
            g.maybe_with_building(70, "Great Library", _building_bonus())
            g.maybe_with_building(70, "Isaac Newton's College",
                                  _building_bonus())
            g.maybe_with_wonder(70, "Darwin's Voyage", _wonder_bonus())

    return weighted_random_possibilities(
        stable_possibility(100, _standard),
        chaotic_possibility(100, _random),
    )()


def city_science_worked_tile_bonus():
    def _add_group():
        return EffectGroup("Output_Add_Tile", "tile_science_add",
                           r.output_type("Science"))

    def _standard():
        with _add_group() as g:
            g.with_building("Copernicus' Observatory", 1)

    def _random():
        def _positive():
            return min_skewed_randint(1, 100, skew=5)

        with _add_group() as g:
            g.maybe_with_random_pct_of_terrain(30, 20, _positive)
            g.maybe_with_random_pct_of_wonders_on_extras(30, 5, _positive)
            g.maybe_with_random_pct_of_buildings_on_extras(30, 10, _positive)
            g.maybe_with_random_pct_of_techs_on_extras(30, 5, _positive)
            g.maybe_with_random_pct_of_govs_on_extras(30, 20, _positive)
            g.maybe_with_random_pct_of_buildings(30, 1, _positive)
            g.maybe_with_building(70, "Copernicus' Observatory", _positive())

    return weighted_random_possibilities(
        stable_possibility(100, _standard),
        chaotic_possibility(100, _random),
    )


def city_science_output_bonus_pct():
    def _output_bonus_group():
        return EffectGroup("Output_Bonus", "science_output_bonus",
                           r.output_type("Science"))

    def _output_bonus_factor_group():
        return EffectGroup("Output_Bonus_2", "science_output_bonus_factor",
                           r.output_type("Science"))

    def _standard():
        with _output_bonus_group() as g:
            with g.with_building_group("Library") as l:
                l.base_effect(50)
                l.after_wonder_worldwide("Great Library", 50)
            with g.with_building_group("University") as u:
                u.base_effect(50)
                u.after_wonder_worldwide("Isaac Newton's College", 25)
            with g.with_building_group("Research Lab") as r:
                r.base_effect(50)
                r.after_wonder_worldwide("Internet", 25)
            g.with_building("Occupation Government", -50)
            g.with_gov("Fundamentalism", -40)
        with _output_bonus_factor_group() as g:
            g.with_gov("Federation", 50)
            g.with_gov_and_tech("Federation", "The Corporation", 25)
            g.with_gov_and_tech("Communism", "The Corporation", 50)

    def _random():
        def _positive():
            return min_skewed_randint(1, 100)

        def _wild():
            return weighted_random_possibilities(
                possibility(60, min_skewed_randint(1, 100)),
                possibility(40, -min_skewed_randint(1, 100)),
            )

        with _output_bonus_group() as g:
            g.with_random_pct_of_buildings(15, _wild)
            g.maybe_with_random_pct_of_govs(70, 20, _wild)
            g.maybe_with_random_pct_of_wonders(30, 10, _wild)
            if random_bool_pct(70):
                with g.with_building_group("Library") as l:
                    l.base_effect(_positive())
                    l.after_wonder_worldwide("Great Library", _positive())
            if random_bool_pct(70):
                with g.with_building_group("University") as u:
                    u.base_effect(_positive())
                    u.after_wonder_worldwide("Isaac Newton's College",
                                             _positive())
            if random_bool_pct(70):
                with g.with_building_group("Research Lab") as l:
                    l.base_effect(_positive())
                    l.after_wonder_worldwide("Internet", _positive())

            g.maybe_with_building(70, "Occupation Government", -50)
            g.maybe_with_gov(70, "Fundamentalism", -40)

        with _output_bonus_factor_group() as g:
            if random_bool_pct(70):
                with g.with_gov_group("Federation") as f:
                    f.base_effect(_positive())
                    f.with_tech("The Corporation", _positive())
            if random_bool_pct(70):
                g.with_gov_and_tech("Communism", "The Corporation", _positive())

    weighted_random_possibilities(
        stable_possibility(100, _standard),
        chaotic_possibility(100, _random),
    )()


def city_improvement_upkeep():
    def _upkeep_free_group():
        return EffectGroup("Upkeep_Free", "building_upkeep")

    def _standard():
        with _upkeep_free_group() as g:
            g.with_gov("Anarchy", 99)
            with g.first_match_in_group() as m:
                m.with_gov("Communism", 1)
                m.with_building_and_wonder("Stock Exchange",
                                           "A.Smith's Trading Co.", 1)

    def _random():
        def _positive():
            return min_skewed_randint(1, 4, skew=2)

        def _wild():
            return weighted_random_possibilities(
                possibility(60, _positive()),
                possibility(40, -_positive()),
            )

        with _upkeep_free_group() as g:
            g.maybe_with_random_pct_of_wonders(30, 5, _wild)
            g.maybe_with_random_pct_of_govs(30, 80, _wild)
            g.maybe_with_random_pct_of_terrain(10, 50, _wild)
            g.maybe_with_gov(90, "Anarchy", 99)
            g.maybe_with_gov(70, "Communism", 1)
            g.maybe_with_building_and_wonder(70, "Stock Exchange",
                                             "A.Smith's Trading Co.", 1)

    weighted_random_possibilities(
        stable_possibility(100, _standard),
        chaotic_possibility(100, _random),
    )()


def city_gold_buyout_costs():
    def _building_buy_cost_pct_group():
        return EffectGroup("Building_Buy_Cost_Pct")

    def _unit_buy_cost_pct_group():
        return EffectGroup("Unit_Buy_Cost_Pct")

    def _standard():
        with _building_buy_cost_pct_group() as g:
            g.with_building_genus("GreatWonder", 100)
            with g.with_building_genus_group("SmallWonder") as s:
                s.all_excluding_building("Palace", 100)

    def _random():
        def _reduced():
            return -max_skewed_randint(1, 99, skew=2)

        def _increased():
            return min_skewed_randint(1, 1000, skew=3)

        def _wild():
            return weighted_random_possibilities(
                possibility(50, _reduced),
                possibility(50, _increased),
            )()

        with _building_buy_cost_pct_group() as g:
            g.maybe_with_random_pct_of_buildings(50, 90, _wild)
            g.maybe_with_random_pct_of_building_genuses(50, 90, _wild)
            if random_bool_pct(70):
                factor = _increased()
                g.with_building_genus("GreatWonder", factor)
                with g.with_building_genus_group("SmallWonder") as s:
                    s.all_excluding_building("Palace", factor)
        with _unit_buy_cost_pct_group() as g:
            g.maybe_with_random_pct_of_units(25, 90, _wild)
            g.maybe_with_random_pct_of_unit_classes(25, 90, _wild)
            g.maybe_with_random_pct_of_unit_flags(25, 90, _wild)
            g.maybe_with_random_pct_of_unit_class_flags(25, 90, _wild)

    weighted_random_possibilities(
        stable_possibility(100, _standard),
        chaotic_possibility(100, _random),
    )()


def city_gold_output_bonus():
    def _gold_output_bonus_group():
        return EffectGroup("Output_Bonus", "gold_output_bonus",
                           r.output_type("Gold"))

    def _standard():
        with _gold_output_bonus_group() as g:
            g.with_building("Marketplace", 50)
            g.with_building("Bank", 30)
            g.with_building("Mercantile Exchange", 30)
            with g.with_building_group("Stock Exchange") as s:
                s.base_effect(40)
                s.with_building("Super Highways", 25)
            with g.with_any_palace() as p:
                p.with_gov("Despotism", 75)
                p.with_gov("Monarchy", 50)
            g.with_building("Occupation Government", -50)

    def _random():
        def _positive(factor=1):
            return mid_skewed_randint(1, 25 + 25 * factor)

        def _wild():
            return weighted_random_possibilities(
                possibility(60, min_skewed_randint(1, 1000, skew=4)),
                possibility(40, -min_skewed_randint(1, 400, skew=3))
            )

        with _gold_output_bonus_group() as g:
            g.maybe_with_random_pct_of_buildings(30, 10, _wild)
            g.maybe_with_random_pct_of_wonders(30, 15, _wild)
            g.maybe_with_random_pct_of_govs(30, 70, _wild)
            g.maybe_with_building(70, "Marketplace", _positive(2))
            g.maybe_with_building(70, "Bank", _positive())
            g.maybe_with_building(70, "Mercantile Exchange", _positive())
            if random_bool_pct(70):
                with g.with_building_group("Stock Exchange") as s:
                    s.base_effect(_positive(2))
                    s.with_building("Super Highways", _positive())
            if random_bool_pct(70):
                with g.with_any_palace() as p:
                    p.with_gov("Despotism", _positive(3))
                    p.with_gov("Monarchy", _positive(2))
            g.maybe_with_building(70, "Occupation Government",
                                  -mid_skewed_randint(1, 100))

    weighted_random_possibilities(
        stable_possibility(100, _standard),
        chaotic_possibility(100, _random),
    )()


def units_airlifting():
    def _airlift_group():
        return EffectGroup("Airlift")

    def _standard():
        setting("units.airlifting.maxRange", "unlimited")
        setting("units.airlifting.fromAllies", True)
        setting("units.airlifting.toAllies", True)
        setting("units.airlifting.unlimitedFromSourceCity", False)
        setting("units.airlifting.unlimitedToDestinationCity", True)
        with _airlift_group() as g:
            g.with_building("Airport")

    def _random():
        def _max():
            setting("units.airlifting.maxRange", "unlimited")
            setting("units.airlifting.fromAllies", True)
            setting("units.airlifting.toAllies", True)
            setting("units.airlifting.unlimitedFromSourceCity", True)
            setting("units.airlifting.unlimitedToDestinationCity", True)
            with _airlift_group() as g:
                g.base_effect(1)

        def _disabled():
            setting("units.airlifting.maxRange", 1)
            setting("units.airlifting.fromAllies", False)
            setting("units.airlifting.toAllies", False)
            setting("units.airlifting.unlimitedFromSourceCity", False)
            setting("units.airlifting.unlimitedToDestinationCity", False)

        def _randomised():
            setting("units.airlifting.maxRange",
                    weighted_random_possibilities(*as_tuple(
                        possibility(50, "unlimited"),
                        possibility(50, randint(1, map_max_dist()))
                    )))
            setting("units.airlifting.fromAllies", False)
            setting("units.airlifting.toAllies", False)
            setting("units.airlifting.unlimitedFromSourceCity", False)
            setting("units.airlifting.unlimitedToDestinationCity", False)
            with _airlift_group() as g:
                g.with_building("Airport")

        weighted_random_possibilities(
            possibility(20, _max),
            possibility(20, _disabled),
            possibility(60, _randomised),
        )()

    weighted_random_possibilities(
        stable_possibility(100, _standard),
        chaotic_possibility(100, _random),
    )()


def units_attacking():
    setting("units.attacking.autoAttackUnitsEnteringZoneOfControl",
            random_bool_pct(chaos))
    setting("units.attacking.onDefenderKilled.neverKillStack",
            random_bool_pct(50))
    setting("units.attacking.onClearingTile.moveIntoTileChancePct",
            weighted_random_possibilities(
                stable_possibility(70, 0),
                stable_possibility(30, 100),
                chaotic_possibility(100, randint(1, 99)),
            ))


def units_barbarians():
    setting("units.barbarians.enabled", False)
    setting("units.barbarians.fromHuts", True)
    setting("units.barbarians.frequency", "NORMAL")
    setting("units.barbarians.startAppearingAfter", 120)
    setting("units.barbarians.initialAnimalsPerThousandTiles", 20)
    setting("units.barbarians.leaderRansomGold", 100)


def units_bombarding():
    def _bombard_limit_pct_group():
        return EffectGroup("Bombard_Limit_Pct", "bombard_limit")

    def _standard_bombarders() -> List[UnitType]:
        return ["Bomber", "Stealth Bomber", "Fusion Bomber"]

    def _ranged_bombarders() -> List[UnitType]:
        return ["AEGIS Cruiser", "Archers", "Artillery", "Battleship", "Bomber",
                "Cannon", "Catapult", "Cruiser", "Destroyer", "Freight",
                "Fusion Battleship", "Fusion Bomber", "Howitzer", "Ironclad",
                "Stealth Bomber", "Trebuchet"]

    def _standard():
        setting("units.bombarding.enabled", True)
        setting("units.bombarding.forced", True)
        with _bombard_limit_pct_group() as g:
            g.base_effect(1)
        setting("units.bombarding.canBombardFromVehicle", False)
        setting("units.bombarding.canTargetOceanic", False)
        for unit in _standard_bombarders():
            unit_type_add_flag(unit, "Bombarder")

    def _ranged_units_bombard():
        setting("units.bombarding.enabled", True)
        setting("units.bombarding.forced", False)
        with _bombard_limit_pct_group() as g:
            g.base_effect(1)
            g.on_city(32)
            g.on_extra("Fortress", 32)
            with g.not_on_city_group().not_on_extra_group("Fortress") as o:
                o.on_terrain("Mountains", 19)
                o.on_terrain("Hills", 14)
                o.on_terrain("Swamp", 29)
                o.on_terrain("Forest", 19)
                o.on_terrain("Jungle", 39)

        setting("units.bombarding.canBombardFromVehicle", True)
        setting("units.bombarding.canTargetOceanic", False)
        for unit in _ranged_bombarders():
            unit_type_add_flag(unit, "Bombarder")

    def _disabled():
        setting("units.bombarding.enabled", False)
        setting("units.bombarding.forced", False)

    def _random():
        def _random_base():
            return min_skewed_randint(1, 99)

        def _random_modifier():
            return weighted_random_possibilities(
                possibility(60, min_skewed_randint(1, 25)),
                possibility(40, -min_skewed_randint(1, 25)),
            )

        setting("units.bombarding.enabled", True)
        setting("units.bombarding.forced", random_bool_pct(50))
        with _bombard_limit_pct_group() as g:
            if random_bool_pct(30):
                g.with_random_pct_of_terrain(90, _random_base)
            else:
                g.base_effect(_random_base())
                g.maybe_with_random_pct_of_terrain(30, 90, _random_modifier)
            g.maybe_with_random_pct_of_extras(30, 90, _random_modifier)
            g.maybe_with_random_pct_of_units(30, 90, _random_modifier)

        setting("units.bombarding.canBombardFromVehicle", random_bool_pct(50))
        setting("units.bombarding.canTargetOceanic", random_bool_pct(50))
        for unit in random_pct_of_units(min_skewed_randint(1, 99)):
            unit_type_add_flag(unit, "Bombarder")
        for unit in _standard_bombarders():
            if random_bool_pct(30):
                unit_type_add_flag(unit, "Bombarder")
        for unit in _ranged_bombarders():
            if random_bool_pct(40):
                unit_type_add_flag(unit, "Bombarder")

    weighted_random_possibilities(
        stable_possibility(30, _standard),
        stable_possibility(40, _ranged_units_bombard),
        stable_possibility(30, _disabled),
        chaotic_possibility(70, _random),
    )


def units_hitpoint_regen():
    def _hp_regen_group():
        return EffectGroup("HP_Regen")

    def _standard():
        with _hp_regen_group() as g:
            with g.with_unit_class_flag_group("Land") as l:
                l.on_extra("Fortress", 25)
                with l.with_any_barracks_group() as b:
                    pass
            with g.with_unit_class_flag_group("Air") as a:
                a.on_extra("Airbase", 34)
                a.with_building("Airport", 100)
        pass

    # {% set regen = options.units.hitpointRegen -%}
    # {% set bases = options.terrain.bases -%}
    #
    # {% set barracksBuildings = ["Barracks", "Barracks II", "Barracks III"] -%}
    # {% for class, regen in regen.barracksByClass | items %}
    # {% for barracks in barracksBuildings %}
    # [effect_{{ barracks | slugify }}_hp_{{ class | slugify }}]
    # type    = "HP_Regen"
    # value   = {{ regen }}
    # reqs    =
    #     { "type", "name", "range", "present"
    #       "Building", "{{ barracks }}", "City", TRUE
    #       "UnitClass", "{{ class }}", "Local", TRUE
    #     }
    # {% endfor %}
    # {% endfor %}
    #
    # [effect_port_facility_1]
    # type    = "HP_Regen"
    # value   = {{ regen.portFacilityBonus }}
    # reqs    =
    #     { "type", "name", "range"
    #       "Building", "Port Facility", "City"
    #       "UnitClassFlag", "Sea", "Local"
    #     }
    #
    # [effect_port_facility_guangzhou_1]
    # type    = "HP_Regen"
    # value   = {{ regen.guangzhouBonus }}
    # reqs    =
    #     { "type", "name", "range"
    #       "Building", "Port of Guangzhou", "City"
    #       "UnitClassFlag", "Sea", "Local"
    #     }
    #         "units.hitpointRegen.portFacilityBonus": 100,
    #         "units.hitpointRegen.guangzhouBonus": 100,
    #         "units.hitpointRegen.barracksByClass": {
    #             "Land": 100,
    #             "Big Land": 100,
    #             "Big Siege": 60,
    #             "Small Unit": 60,
    #             "Ancient Land": 100
    #         }
    pass


# TODO: Settings start

# Starting conditions
starting_units_and_cities()
setting("start.unitDispersion", weighted_random_possibilities(
    stable_possibility(70, 6),
    stable_possibility(30, 0),
    chaotic_possibility(100, randint(0, 10))
))
setting("start.gold", weighted_random_possibilities(
    stable_possibility(70, 50),
    stable_possibility(30, 0),
    chaotic_possibility(100, min_skewed_randint(0, 50000, skew=2)),
))
setting("start.initialTechs", weighted_random_possibilities(
    stable_possibility(70, 0),
    stable_possibility(30, random.randint(1, 3)),
    chaotic_possibility(100, min_skewed_randint(0, len(all_techs()), skew=3)),
))

# Victory
setting("victory.spaceRace.enabled", True)
setting("victory.spaceRace.endsGame", True)
setting("victory.spaceRace.travelTimeMultiplierPct", 200)
setting("victory.finalTurn", 5000)

# Cities
setting("cities.minDistBetween", min_dist_between_cities())
city_work_radius()
city_migration()
setting("cities.cannotAddToCityAtOrAboveSize", weighted_random_possibilities(
    stable_possibility(80, 8),
    chaotic_possibility(30, 0),
    chaotic_possibility(30, 255),
    chaotic_possibility(40, min_skewed_randint(0, 255, skew=2)),
))

# City Granary
setting("cities.growth.noAqueductOnGrowthFoodLossPct", 0)
setting("cities.growth.granary.sizeFactorPct", weighted_random_possibilities(
    stable_possibility(100, 100),
    chaotic_possibility(70, random_multiplier_pct(50, 200)),
    chaotic_possibility(30, random_multiplier_pct(1, 10000,
                                                  mid_skewed_randint)),
))
setting("cities.growth.granary.perCitizen", [12, 14, 16, 20, 24, 28, 34, 40])
setting("cities.growth.granary,perExtraCitizen", 0)
setting("cities.growth.granary.foodRetainedOnGrowth.smallCityBonusPct", 50)
setting("cities.growth.granary.foodRetainedOnGrowth.smallCitySizeMax", 3)
setting("cities.growth.granary.foodRetainedOnGrowth.granaryBonusPct", 50)
setting("cities.growth.granary.foodRetainedOnGrowth.surplusPct", 100)
max_city_size()
rapture_growth()

# City Happiness
setting("cities.happiness.celebrateSizeMin", weighted_random_possibilities(
    stable_possibility(80, 3),
    chaotic_possibility(30, 1),
    chaotic_possibility(70, min_skewed_randint(1, 255, skew=3)),
))
setting("cities.happiness.happinessLuxuryCost", weighted_random_possibilities(
    stable_possibility(100, 2),
    chaotic_possibility(33, 1),
    chaotic_possibility(33, 3),
    chaotic_possibility(33, min_skewed_randint(1, 10000, skew=12)),
))
setting("cities.happiness.baseContentCitizens", weighted_random_possibilities(
    stable_possibility(50, 4),
    chaotic_possibility(30, 0),
    chaotic_possibility(20, 255),
    chaotic_possibility(50, min_skewed_randint(0, 255, skew=6)),
))
entertainer_luxuries()
empire_size_unhappiness()
martial_law()
city_luxury_bonus()
city_luxury_output_bonus_pct()
city_contentment_bonuses()
city_nationalism_unhappiness()

# City Nationalism
setting("cities.nationality.convertSpeed", weighted_random_possibilities(
    stable_possibility(60, 50),
    stable_possibility(40, 0),
    chaotic_possibility(100, min_skewed_randint(1, 1000, skew=4)),
))
setting("cities.nationality.partisansMinPct", weighted_random_possibilities(
    stable_possibility(60, 75),
    stable_possibility(40, 0),
    chaotic_possibility(100, randint(1, 100)),
))

# City Defence
city_defender_bonuses()
setting("cities.defence.onDefenderKilled.loseOneCitizen", random_bool_pct(80))
setting("cities.defence.onDefenderKilled.cityWallsPreventsCitizenLoss",
        random_bool_pct(80))
setting("cities.defence.onCityLost.palaceIsRebuiltForFreeAtRandomCity",
        random_bool_pct(stable(1.5)))
setting("cities.defence.onCityLost.buildingDestructionChancePct",
        weighted_random_possibilities(
            stable_possibility(80, 10),
            chaotic_possibility(25, 0),
            chaotic_possibility(25, 100),
            chaotic_possibility(50, randint(0, 100)),
        ))
city_inspire_partisans()
city_nuclear_defence()

# City Health
setting("cities.illness.enabled", random_bool_pct(stable(1.5)))
setting("cities.illness.baseFactor", weighted_random_possibilities(
    stable_possibility(100, 10),
    chaotic_possibility(100, min_skewed_randint(0, 100, skew=2)),
))
setting("cities.illness.minCitySize", weighted_random_possibilities(
    stable_possibility(80, 5),
    chaotic_possibility(50, 1),
    chaotic_possibility(50, min_skewed_randint(1, 255, skew=5)),
))
city_health_bonus()

# Disasters
city_disasters()

# City Food
setting("cities.food.citizenUpkeep", weighted_random_possibilities(
    stable_possibility(100, 2),
    chaotic_possibility(70, 1),
    chaotic_possibility(15, 3),
    chaotic_possibility(15, 0),
))
setting("cities.food.centreTile.minimum", weighted_random_possibilities(
    stable_possibility(100, 1),
    chaotic_possibility(70, randint(0, 2)),
    chaotic_possibility(30, min_skewed_randint(0, 255, skew=6)),
))
setting("cities.food.centreTile.bonus", weighted_random_possibilities(
    stable_possibility(100, 0),
    chaotic_possibility(70, randint(0, 2)),
    chaotic_possibility(30, min_skewed_randint(0, 255, skew=6))
))
city_food_waste()
city_food_worked_tile_penalty()
city_food_worked_tile_bonus()
city_irrigation_bonus_pct()

# City Trade
setting("cities.trade.centreTile.minimum", weighted_random_possibilities(
    stable_possibility(100, 0),
    chaotic_possibility(70, randint(0, 2)),
    chaotic_possibility(30, min_skewed_randint(0, 255, skew=4)),
))
setting("cities.trade.centreTile.bonus", weighted_random_possibilities(
    stable_possibility(100, 0),
    chaotic_possibility(70, randint(0, 2)),
    chaotic_possibility(30, min_skewed_randint(0, 255, skew=4))
))
city_size_trade_restriction()
city_trade_worked_tile_bonus()
city_trade_worked_tile_penalty()
city_trade_output_bonus_pct()
city_trade_waste()

# City Production
setting("cities.production.costMultiplierPct", weighted_random_possibilities(
    stable_possibility(100, 100),
    chaotic_possibility(100, random_multiplier_pct(50, 200)),
))
setting("cities.production.centreTile.minimum", weighted_random_possibilities(
    stable_possibility(100, 1),
    chaotic_possibility(70, randint(0, 2)),
    chaotic_possibility(30, min_skewed_randint(0, 255, skew=4)),
))
setting("cities.production.centreTile.bonus", weighted_random_possibilities(
    stable_possibility(100, 1),
    chaotic_possibility(70, randint(0, 2)),
    chaotic_possibility(30, min_skewed_randint(0, 255, skew=4))
))
city_unit_batch_production()
city_production_output_bonus_pct()
city_production_worked_tile_bonus()
city_production_worked_tile_penalty()
city_production_waste()

# City Science
city_scientists_output()
city_tile_science_bonus()
city_science_worked_tile_bonus()
city_science_output_bonus_pct()

# City Gold
city_taxmen_output()
city_improvement_upkeep()
city_gold_buyout_costs()
city_gold_output_bonus()

# Units
units_airlifting()
units_attacking()
units_barbarians()
units_bombarding()
units_hitpoint_regen()

# TODO: settings end
options["units"] = {
    "units.disbanding": {
        "shieldReturnPct": {
            "base": 50
        }
    },
    "units.fortifyDefenceBonus": 50,
    "units.countAsFortifiedInCities": True,
    "units.nuclear": {
        "cityPopLossPct": 30,
        "unitSurvivalChancePct": 20,
        "improvementDestroyedChancePct": 20,
        "terrainInfrastructureDestroyedChancePct": 20
    },
    "units.upkeep": {
        "multiplier": {
            "food": 1,
            "gold": 1,
            "shields": 1,
            "happiness": 1
        },
        "freePerCity": {
            "fromSize": {
                "happiness": {
                    "1": 2,
                    "9": 2
                },
                "shields": {},
                "gold": {},
                "food": {
                    "base": 4,
                    "fromSize": 5,
                    "toSize": 40,
                    "perSize": 1
                }
            },
            "policeStation": 1,
            "kingRichards": {
                "happiness": 1,
                "gold": 2
            },
            "statueOfZeus": {
                "happiness": 1,
                "shields": 1
            }
        },
        "byGov": {
            "Anarchy": {
                "multiplier": {
                    "gold": 0,
                    "shields": 1,
                    "happiness": 0
                },
                "freePerCity": {
                    "fromSize": {
                        "happiness": {
                            "1": 2,
                            "9": 2
                        },
                        "shields": {
                            "1": 2,
                            "9": 2
                        }
                    }
                }
            },
            "Tribal": {
                "multiplier": {
                    "gold": 0,
                    "shields": 1,
                    "happiness": 0
                },
                "freePerCity": {
                    "fromSize": {
                        "happiness": {
                            "1": 2,
                            "9": 2
                        },
                        "shields": {
                            "1": 2,
                            "9": 2
                        }
                    }
                }
            },
            "Communism": {
                "multiplier": {
                    "gold": 0,
                    "shields": 1,
                    "happiness": 1
                },
                "freePerCity": {
                    "fromSize": {
                        "happiness": {
                            "1": 3,
                            "9": 3
                        },
                        "shields": {
                            "1": 3,
                            "9": 3
                        }
                    }
                }
            },
            "Republic": {
                "multiplier": {
                    "gold": 0,
                    "shields": 1,
                    "happiness": 1
                },
                "freePerCity": {
                    "fromSize": {
                        "happiness": {
                            "1": 1,
                            "9": 1
                        },
                        "shields": {
                            "1": 1,
                            "9": 1
                        }
                    }
                }
            },
            "Despotism": {
                "multiplier": {
                    "gold": 1,
                    "shields": 0,
                    "happiness": 0
                },
                "freePerCity": {
                    "fromSize": {
                        "happiness": {
                            "1": 2,
                            "9": 2
                        },
                        "gold": {
                            "1": 2,
                            "9": 2
                        }
                    }
                }
            },
            "Monarchy": {
                "multiplier": {
                    "gold": 1,
                    "shields": 0,
                    "happiness": 1
                },
                "freePerCity": {
                    "fromSize": {
                        "happiness": {
                            "1": 3,
                            "9": 3
                        },
                        "gold": {
                            "1": 3,
                            "9": 3
                        }
                    }
                }
            },
            "Fundamentalism": {
                "multiplier": {
                    "gold": 2,
                    "shields": 0,
                    "happiness": 1
                },
                "freePerCity": {
                    "fromSize": {
                        "happiness": {
                            "1": 2,
                            "9": 2
                        },
                        "gold": {
                            "1": 4,
                            "9": 4
                        }
                    }
                }
            },
            "Federation": {
                "multiplier": {
                    "gold": 2,
                    "shields": 0,
                    "happiness": 1
                },
                "freePerCity": {
                    "fromSize": {
                        "happiness": {
                            "1": 2,
                            "9": 2
                        },
                        "gold": {
                            "1": 4,
                            "9": 4
                        }
                    }
                }
            },
            "Democracy": {
                "multiplier": {
                    "gold": 2,
                    "shields": 0,
                    "happiness": 2
                },
                "freePerCity": {
                    "fromSize": {
                        "happiness": {
                            "1": 1,
                            "9": 1
                        },
                        "gold": {
                            "1": 2,
                            "9": 2
                        }
                    },
                    "policeStation": 2
                }
            },
            "City States": {
                "multiplier": {
                    "gold": 0,
                    "shields": 0,
                    "happiness": 0
                },
                "freePerCity": {
                    "fromSize": {
                        "happiness": {
                            "1": 1,
                            "9": 1
                        },
                        "gold": {
                            "1": 6,
                            "9": 6
                        }
                    }
                }
            }
        }
    },
    "units.upgrades": {
        "shield2GoldFactorPct": 50,
        "inventionCostReduction": 20,
        "roboticsCostReduction": 30,
        "freeUpgradesPerTurn": {
            "espionageBonus": 2,
            "radioBonus": 2,
            "verrochios": 1,
            "leonardos": 2
        }
    },
    "units.movement": {
        "nukeAdvancedFlightBonus": 9,
        "nukeRocketryBonus": 9,
        "nuclearBoatBonus": 3,
        "fusionBoatBonus": 6,
        "lighthouseBonus": 1,
        "magellanBonus": 1
    },
    "units.capturing": {
        "canCaptureAllies": False
    },
    "units.settling": {
        "inAlliedTerritory": False
    },
    "units.transporting": {
        "allowForeignBoarding": False
    },
    "units.homecity": {
        "allowRehoming": True,
        "automaticallyRehomeCapturedUnits": True,
        "unhomedUnits": {
            "hitpointLossPctPerTurn": 0
        }
    },
    "units.veterancy": {
        "initialLevelBonus": {
            "airport": 1,
            "barracks": 1,
            "portFacility": 1,
            "guangzhou": 1,
            "lighthouse": 1,
            "sunTzus": 1,
            "terracotta": 1,
            "academy": 1
        },
        "combatPromotionChanceBonusPct": {
            "tribalLand": 50,
            "magellans": 50
        },
        "levels": [
            {
                "name": "green",
                "baseRaiseChance": 50,
                "workRaiseChance": 9,
                "powerFactor": 100,
                "moveBonus": 0
            },
            {
                "name": "veteran 1",
                "baseRaiseChance": 45,
                "workRaiseChance": 6,
                "powerFactor": 150,
                "moveBonus": 3
            },
            {
                "name": "veteran 2",
                "baseRaiseChance": 40,
                "workRaiseChance": 6,
                "powerFactor": 175,
                "moveBonus": 6
            },
            {
                "name": "veteran 3",
                "baseRaiseChance": 35,
                "workRaiseChance": 6,
                "powerFactor": 200,
                "moveBonus": 9
            },
            {
                "name": "hardened 1",
                "baseRaiseChance": 30,
                "workRaiseChance": 5,
                "powerFactor": 225,
                "moveBonus": 12
            },
            {
                "name": "hardened 2",
                "baseRaiseChance": 25,
                "workRaiseChance": 5,
                "powerFactor": 250,
                "moveBonus": 15
            },
            {
                "name": "hardened 3",
                "baseRaiseChance": 20,
                "workRaiseChance": 4,
                "powerFactor": 275,
                "moveBonus": 18
            },
            {
                "name": "elite 1",
                "baseRaiseChance": 15,
                "workRaiseChance": 4,
                "powerFactor": 300,
                "moveBonus": 21
            },
            {
                "name": "elite 2",
                "baseRaiseChance": 10,
                "workRaiseChance": 3,
                "powerFactor": 325,
                "moveBonus": 24
            },
            {
                "name": "elite 3",
                "baseRaiseChance": 0,
                "workRaiseChance": 0,
                "powerFactor": 350,
                "moveBonus": 27
            }
        ]
    }
}

options["terrain"] = {
    "transition": {
        "oceanToLand": {
            "adjacentLandPctRequired": 0
        },
        "landToOcean": {
            "adjacentOceanPctRequired": 10
        },
        "frozenToUnfrozen": {
            "adjacentUnfrozenPctRequired": 0
        },
        "unfrozenToFrozen": {
            "adjacentFrozenPctRequired": 0
        }
    },
    "generation": {
        "mode": "FRACTURE",
        "seed": 0,
        "size": {
            "mode": "player",
            "player": {
                "tilesPerPlayer": 400
            },
            "aspectRatio": {
                "width": 100,
                "height": 100
            },
            "standard": {
                "tiles": 10000
            }
        },
        "playerStartLocations": {
            "mode": "VARIABLE",
            "teamPlacementMode": "CLOSEST"
        },
        "lakeMaxSize": 14,
        "allTemperate": False,
        "poles": {
            "flattenedByPct": 0,
            "areSeparateFromOtherContinents": True,
            "singleHemisphereMapWithOneNonWrappingPole": False
        },
        "hutsPerThousandTiles": 0,
        "specialsPerThousandTiles": 300,
        "mapLandPct": 40,
        "steepnessPct": 45,
        "averageTemperaturePct": 60,
        "averageLandWetnessPct": 60,
        "allowTinyIslands": False,
        "topology": {
            "wrapEastWest": True,
            "wrapNorthSouth": True
        }
    },
    "movement": {
        "moveFragments": 9,
        "ignoreTerrainCost": 3,
        "roadMoveCost": 3,
        "railMoveCost": 1,
        "maglevMoveCost": 0,
        "riverMoveCost": 3,
        "mountainStartPenalty": 1
    },
    "bases": {
        "fortress": {
            "defenceBonus": 100
        },
        "airbase": {
            "regen": 34,
            "defenceBonus": 100
        }
    },
    "extras": {
        "pollutionOutputPenaltyPct": 50,
        "falloutOutputPenaltyPct": 50
    }
}

options["climate"] = {
    "globalWarming": {
        "enabled": True,
        "accumulationFactorPct": 40
    },
    "nuclearWinter": {
        "enabled": True,
        "accumulationFactorPct": 100
    }
}

options["pollution"] = {
    "enabled": True,
    "contributesToGlobalWarming": True,
    "baseCityPollution": -20,
    "illnessPenaltyPct": 50,
    "populationFactorPct": {
        "base": -100,
        "factory": 25,
        "workshop": 15,
        "manufacturingPlant": 50,
        "offshorePlatform": 25,
        "superHighways": 25,
        "massTransit": -50,
        "eiffelTower": -25,
        "parisAgreement": -40,
        "globalEmissionsUnion": -50
    },
    "productionFactorPct": {
        "recyclingCentre": {
            "base": -25,
            "noPlants": -25
        },
        "solar": -75,
        "hooverDam": -75,
        "hydro": -50,
        "hooverDamNation": -15,
        "nuclear": -50
    }
}

options["civilWar"] = {
    "enabled": True,
    "minCities": 10,
    "celebratingCityChanceModifier": -5,
    "unhappyCityChanceModifier": 5,
    "governmentChanceModifierPct": {
        "Anarchy": 49,
        "Tribal": 45,
        "Despotism": 40,
        "Monarchy": 35,
        "Communism": 25,
        "City States": 20,
        "Fundamentalism": 30,
        "Federation": 10,
        "Republic": 20,
        "Democracy": 15
    }
}

options["economy"] = {
    "goldUpkeepStyle": "Mixed"
}

options["tech"] = {
    "individualTechProgressBars": False,
    "baseCost": 20,
    "costMultiplier": 3,
    "costMultiplierPct": 100,
    "midResearchSwitchingPenaltyPct": 10,
    "leakageCostReductionGradient": {
        "enabled": True,
        "onlyNationsWithEmbassyCount": False,
        "techIsFreeWhenKnownByPctNations": 66.6,
        "reductionPctWhenKnownByAllNations": 150
    },
    "upkeep": {
        "mode": "Basic",
        "bulbsResearchedPerUpkeepIncrease": 300,
        "reduction": {
            "base": -3
        },
        "techLossOnNegativeBulbs": {
            "enabled": False,
            "negativeAllowedAsPctOfCurrentResearch": 100,
            "restoreBulbsOnTechLoss": {
                "enabled": True,
                "resetToZero": False,
                "pctOfCurrentResearchCost": 50
            }
        }
    },
    "stealTechOnConquest": {
        "enabled": False,
        "bulbCostPct": 30
    },
    "freeTech": {
        "mode": "Goal",
        "bulbCostPct": 0
    },
    "teamMatesShareTechs": False
}

options["tradeRoutes"] = {
    "tradeRevenueStyle": "CLASSIC",
    "routeFormedBonusStyle": "CLASSIC",
    "minimumDistanceBetweenDomesticRoutes": 999,
    "distanceFactorRelativeToWorldSizePct": 50,
    "routeWithPlaguedCityIllnessPenaltyPct": 50,
    "maxNumberOfRoutes": 0,
    "tradeRevenueExponentPerThousand": {
        "base": 585,
        "railroad": -1000,
        "onEnterMarketplace": -1585
    }
}

options["diplomacy"] = {
    "allowedBetween": {
        "humanAndHuman": True,
        "aiAndAI": False,
        "humanAndAI": False,
        "onlyTeamMates": False
    },
    "turnsToContactLost": 1,
    "goldTrading": {
        "enabled": True,
        "goldLostPct": 40
    },
    "techTrading": {
        "enabled": False,
        "bulbCost": 20,
        "chanceReceiverFailsToLearnTechPct": 0,
        "chanceSenderForgetsTechPct": 0
    },
    "cityTrading": {
        "enabled": False
    }
}

options["espionage"] = {
    "baseChancePct": 40,
    "bribing": {
        "baseCost": 750
    },
    "inciteCity": {
        "inciteCost": {
            "base": 1000,
            "improvementFactor": 1,
            "unitFactor": 2,
            "totalFactor": 100,
            "courthousePct": 300,
            "emptyCourthousePct": 100,
            "emptyPct": -50
        },
        "goldLossOnFailChancePct": 0,
        "goldCaptureChancePct": 0
    },
    "poisonEmptiesFoodStock": False,
    "veterancy": {
        "communismBonus": 1,
        "federationBonus": 1
    },
    "diplomaticBattle": {
        "defenceBonusPct": {
            "palace": 50,
            "academy": 10
        }
    },
    "sabotage": {
        "defenceBonusPct": {
            "palace": 50,
            "academy": 10
        }
    },
    "oddsPct": {
        "stealTech": 50,
        "stealTechEscape": 50,
        "stealSpecificTechEscape": 50,
        "sabotageSpecificBuildingEscape": 50,
        "sabotageProductionEscape": 50
    }
}

options["vision"] = {
    "startingLocationRadiusSq": 36,
    "fogOfWar": True,
    "apolloRevealsMap": True,
    "internetRevealsCities": True,
    "mountainBonus": 18,
    "airbaseBonus": 18,
    "fortressAstronomyBonus": 18,
    "buoyRadiusSq": 18,
    "cities": {
        "base": 5,
        "electricityBonus": 25
    }
}

options["borders"] = {
    "enabled": "ENABLED",
    "borderChangesHiddenInFog": True,
    "unitsInBordersCauseNoUnhappiness": "NATIONAL",
    "onlyAlliesMayUseMovementInfrastructure": True,
    "cityBaseRadiusSq": 15,
    "citySizeIncrement": 1,
    "nearCityProtectedRadius": -3
}

options["governance"] = {
    "revolution": {
        "mode": "FIXED",
        "length": 2,
        "statueOfLibertyFastSwitching": True,
        "disorderForcesAnarchy": {
            "enabled": True,
            "turnsByGovernment": {
                "Republic": 2,
                "Democracy": 2
            },
            "unitedNationsEnablesForAllGovs": 2
        }
    },
    "maxSliderRatesPct": {
        "Anarchy": 100,
        "Tribal": 60,
        "City States": 50,
        "Despotism": 60,
        "Monarchy": 70,
        "Communism": 80,
        "Fundamentalism": 60,
        "Federation": 90,
        "Republic": 80,
        "Democracy": 90
    },
    "senate": {
        "governments": [
            "Democracy",
            "Federation"
        ],
        "unitedNations": True
    }
}

options["chronology"] = {
    "startYear": -4000,
    "skipYearZero": True,
    "yearFragments": [],
    "postZeroEraLabel": "CE",
    "preZeroEraLabel": "BCE",
    "steps": [
        {"from": -4000, "to": 0, "turns": 40},
        {"from": 0, "to": 1500, "turns": 30},
        {"from": 1500, "to": 1750, "turns": 10},
        {"from": 1750, "to": 1850, "turns": 10},
        {"from": 1850, "to": 1950, "turns": 20},
        {"from": 1950, "to": 1980, "turns": 10},
        {"from": 1980, "to": 2000, "turns": 10},
        {"from": 2000, "step": 1}
    ]
}

options["stats"] = {
    "demography": {
        "score": True,
        "leagueScore": True,
        "population": True,
        "citizenCount": True,
        "cityCount": True,
        "improvements": True,
        "wonderCount": True,
        "landArea": True,
        "settledArea": True,
        "literacyRate": True,
        "foodYield": True,
        "shieldYield": True,
        "tradeYield": True,
        "goldYield": False,
        "scienceYield": False,
        "militaryService": True,
        "militaryUnits": False,
        "unitsBuilt": False,
        "unitsKilled": True,
        "unitsLost": True,
        "pollution": True,
        "culture": True,
        "columns": {
            "quantity": True,
            "rank": True,
            "bestNation": True
        }
    }
}

config['options'] = options

config['features'] = {
    "impetuousUnits": {
        "enabled": True,
        "provokingChance": 0.15
    },
    "inaccessibleClimates": {
        "enabled": True,
        "baseCityPollution": 1,
        "globalWarmingAccumulationFactor": 200,
        "pollutionProductionIncrease": 1
    },
    "explosiveExpansion": {
        "enabled": True
    },
    "invisiblePortals": {
        "enabled": True,
        "allowFatalTransit": False,
        "allowFatalTransitAI": False,
        "density": 0.027,
        "halfLife": 8
    },
    "blindWorld": {
        "enabled": True,
        "blindVisionRadius": 0,
        "nonBlindUnderwaterVisionRadius": 1,
        "nonBlindSurfaceVisionRadius": 2,
        "nonBlindAirVisionRadius": 5,
        "surfaceMountainVisionBonus": 1
    },
    "powerfulSpecials": {
        "enabled": True,
        "perThousandTiles": 30
    },
    "spaceExodus": {
        "enabled": True,
        "expectedLaunchTurn": 250,
        "earlyFinishMultiplier": 15,
        "firstPlaceBonus": 500
    }
}


def generate_config():
    return {
        "project": load_json_config(project_json),
        "game": load_json_config(game_json),
        "options": server_options(),
        "unitTypeDefs": unit_type_defs(),
        "features": chaos_features()
    }


def save_config(config):
    with open(file=config_json, mode='w',
              encoding='utf-8') as json_file:
        json.dump(obj=config, fp=json_file, indent=2)

    print(f"{config_json} has been generated.")


chaos = 15
save_config(generate_config())
