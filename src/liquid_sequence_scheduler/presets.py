from typing import Set, Dict

# Hardware to be controlled and its type
engine_hardware: Dict[str, str] = {
    "oxpress": "solenoid",
    "fuelpress": "solenoid",
    "oxvent": "solenoid",
    "fuelvent": "solenoid",
    "oxvurge": "solenoid",
    "fuelpurge": "solenoid",
    "ox": "valve",
    "fuel": "valve"
}

# List of commands to send
engine_commands: Set[str] = {
    "ignite", 
    "abort", 
    "telreq", 
    "pfpurge", 
    "fillchill", 
    "standby", 
    "hotfire",
    "getstate",
    "stophotfire",
    "stoppurge",
    "loxpurge",
    "datalog"}

allowed_on_off: Set[str] = {"on", "1", "off", "0"}