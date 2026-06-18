import os
from google.antigravity import Agent, LocalAgentConfig, CapabilitiesConfig
from google.antigravity.hooks import policy
from google.antigravity.types import TemplatedSystemInstructions
from lumina_travel.tools import get_destination_info, search_accommodations, execute_booking

# 1. Define Persona & System Instructions
travel_persona = (
    "You are Lumina Travel, a proactive AI Trip Concierge that acts as a highly capable personal assistant for modern travelers. "
    "You own the entire travel lifecycle: early inspiration/research, lodging discovery, and booking support.\n\n"
    "CRITICAL RULES:\n"
    "1. You MUST ALWAYS obtain explicit user confirmation before booking or taking any financial/binding actions.\n"
    "2. For bookings, you must present the listing details (name, price, cancellation policy) to the user first. "
    "Only call `execute_booking` with `confirmation=True` when the user has explicitly typed 'yes', 'confirm', or otherwise approved the booking of that specific listing.\n"
    "3. Ground all recommendations in real-time information from your tools. Provide clear, transparent reasoning with citations (ratings, prices, local norms).\n"
    "4. For destination research, provide weather, events, transit info, and local etiquette clearly and concisely.\n"
    "5. Be professional, friendly, and structured in your responses."
)

system_instructions = TemplatedSystemInstructions(
    identity=travel_persona
)

# 2. Safety Policies
# By default, deny any CLI command execution, but allow all other tools.
# We also include a custom policy/hook if needed, but let's stick to clean standard policies.
policies = [
    policy.confirm_run_command(),  # Denies run_command, allows everything else
]

# 3. Create Agent Configuration
def get_travel_agent_config(app_data_dir: str = None) -> LocalAgentConfig:
    # Use environment GEMINI_API_KEY
    api_key = os.environ.get("GEMINI_API_KEY", "")
    
    config_args = {
        "model": "gemini-3.5-flash", # Use a robust model for general tool use and reasoning
        "system_instructions": system_instructions,
        "tools": [get_destination_info, search_accommodations, execute_booking],
        "capabilities": CapabilitiesConfig(), # Enables read/write tools
        "policies": policies
    }
    
    if api_key:
        config_args["api_key"] = api_key
        
    if app_data_dir:
        config_args["app_data_dir"] = app_data_dir
        
    return LocalAgentConfig(**config_args)
