from openai import OpenAI
import os

# Ensure you have your key set in your environment or replace the string below
client = OpenAI(
    api_key="XAI_API_KEY=xai-eRQyUSQ0hLpG5f641DB7n4iyrzksgyfxvPUMkgxKSQ0CBIx2cO7ZglOFR26hXWhEK5kNXufGhLw9s0I7SQ0CBIx2cO7ZglOFR26hXWhEK5kNXufGhLw9s0I7",
    base_url="https://api.x.ai/v1"
)

models = client.models.list()
for model in models:
    print(model.id)