import os
from openai import OpenAI
from firewall_core_logic import enforce_logic
from decision_ledger import DecisionLedger

ledger = DecisionLedger()


def _get_client():
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")

    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set")

    return OpenAI(api_key=api_key, base_url=base_url)


def call_grok_and_enforce(prompt: str, principal: dict):

    client = _get_client()

    response = client.chat.completions.create(
        model="grok-4-0709",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    content = response.choices[0].message.content

    ledger.log_interaction("llm_response", {"prompt": prompt})

    action = {
        "tool": "llm_output",
        "content": content
    }

    decision = enforce_logic(
        action=action,
        principal=principal,
        context=action
    )

    return {
        "llm_output": content,
        "firewall_decision": decision
    }
