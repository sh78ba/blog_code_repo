def normalize_email(email: str) -> str:
    email = email.strip().lower()

    try:
        local, domain = email.split("@")
    except ValueError:
        return email

    if domain in ["gmail.com", "googlemail.com"]:
        local = local.replace(".", "")
        local = local.split("+")[0]

    return f"{local}@{domain}"