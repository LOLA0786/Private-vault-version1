from config import GROK_API_KEY
from enforcement_core import enforce

def _get_client():
    if not GROK_API_KEY:
        return None
    from openai import OpenAI
    return OpenAI(api_key=GROK_API_KEY)

def call_grok_and_enforce(prompt, tenant="alpha", principal=None):
    client = _get_client()

    if client is None:
        mock_response = "Mocked Grok response"
        return enforce(
            {"tenant": tenant, "prompt": prompt, "llm_output": mock_response},
            principal=principal
        )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )

    output = response.choices[0].message.content

    return enforce(
        {"tenant": tenant, "prompt": prompt, "llm_output": output},
        principal=principal
    )
