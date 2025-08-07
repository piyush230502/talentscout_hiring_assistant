import os
import json

# Create the directory structure for the TalentScout hiring assistant
directories = [
    "talentscout_hiring_assistant",
    "talentscout_hiring_assistant/config",
    "talentscout_hiring_assistant/prompts",
    "talentscout_hiring_assistant/services",
    "talentscout_hiring_assistant/models",
    "talentscout_hiring_assistant/utils",
    "talentscout_hiring_assistant/data",
    "talentscout_hiring_assistant/assets",
    "talentscout_hiring_assistant/tests"
]

for directory in directories:
    os.makedirs(directory, exist_ok=True)
    print(f"Created directory: {directory}")

print("Directory structure created successfully!")