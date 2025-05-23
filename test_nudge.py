# test_nudge.py
import os
from dotenv import load_dotenv

load_dotenv()  # Pick up .env locally, or rely on GH secret in CI

from src.nudge_api import generate_hf_nudge

print(
    generate_hf_nudge(
        user_id="test123",
        usage_frequency=5,
        support_calls=0,
        payment_delay=2,
        contract_length="Month-to-month",
        tech_support="No",
        monthly_charges=45.0,
        paperless_billing="Yes",
        variant="A",
    )
)
