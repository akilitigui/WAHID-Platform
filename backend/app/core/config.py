from typing import Optional

# Paiements - CinetPay (Optionnel pour MVP)
CINETPAY_MODE: str = Field(default="TEST", env="CINETPAY_MODE")
CINETPAY_API_KEY: Optional[str] = Field(default=None, env="CINETPAY_API_KEY")
CINETPAY_SITE_ID: Optional[str] = Field(default=None, env="CINETPAY_SITE_ID")
CINETPAY_SECRET: Optional[str] = Field(default=None, env="CINETPAY_SECRET")
CINETPAY_WEBHOOK_URL: str = Field(
    default="https://wahid-backend.onrender.com/api/v1/payments/webhook",
    env="CINETPAY_WEBHOOK_URL"
)

@property
def CINETPAY_ENABLED(self) -> bool:
    """Vérifie si CinetPay est configuré"""
    return bool(
        self.CINETPAY_API_KEY and 
        self.CINETPAY_SITE_ID and 
        self.CINETPAY_SECRET
    )