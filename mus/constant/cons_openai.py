OPENAI_MODEL = "gpt-3.5-turbo"
OPENAI_MODEL_WIN_MAX_LEN = 4096

OAI_COMP_MAX_TOCKEN = 100
OAI_COMP_WIN_MAX_LEN = OPENAI_MODEL_WIN_MAX_LEN - OAI_COMP_MAX_TOCKEN - 8  # - tldr
OAI_COMP_TL_DR = "\nTl;dr"

OAI_COMP_TEMPERATURE = 0.1
OAI_COMP_TOP_P = 1.0
OAI_COMP_FREQUENCY_PENALTY = 0.0
OAI_COMP_PRESENCE_PENALTY = 1