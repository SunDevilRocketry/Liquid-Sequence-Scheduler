from typing import Set

# List of hardware to be controlled
engine_hardware: Set[str] = {
    "sol1", 
    "sol2", 
    "ox", 
    "fuel", 
    "stepper1", 
    "stepper2"}

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