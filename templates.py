from jinja2 import Template

TEMPLATES = {
    "high_value": "Hi {{ first_name }}, thanks for being a premium user! Unlock your exclusive feature bundle today.",
    "trial_user": "Hi {{ first_name }}, your trial is active. Explore premium features before your trial ends.",
    "inactive": "Hi {{ first_name }}, we miss you! Come back and see what is new.",
    "default": "Hi {{ first_name }}, check out your personalized dashboard today."
}

def render_message(template_name: str, context: dict) -> str:
    template_text = TEMPLATES.get(template_name, TEMPLATES["default"])
    return Template(template_text).render(**context)
