from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações lidas de variáveis de ambiente (ou do arquivo .env)."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    ai_provider: str = "gemini"  # "gemini" ou "mock" (respostas simuladas, sem chave)
    gemini_api_key: str = ""
    gemini_model: str = "gemini-3.1-flash-lite"
    ai_timeout_seconds: float = 60.0
    cors_origins: str = "http://localhost:3000"
    # SQLite local por padrão; em produção use a URL do PostgreSQL (Neon) em DATABASE_URL
    database_url: str = "sqlite:///./nivela.db"
    jwt_secret: str = ""  # obrigatório para login (defina no .env e no Render)
    jwt_expire_minutes: int = 480
    # usuário de demonstração opcional (recriado a cada reinício da API)
    demo_nome: str = "Professor Demo"
    demo_email: str = ""
    demo_senha: str = ""

    @property
    def cors_origins_list(self) -> list[str]:
        return [origem.strip() for origem in self.cors_origins.split(",") if origem.strip()]


settings = Settings()
