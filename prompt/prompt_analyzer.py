from langchain_core.prompts import ChatPromptTemplate

      # Prompt for document analysis

prompt_1 = ChatPromptTemplate.from_template("""
You are a highly capable assistant trained to analyze and summarize documents.
Return ONLY valid JSON matching the exact schema below.
                        {format_instructions}

Analyze this document:
{document_text}
""")

Prompt_2 = ChatPromptTemplate.from_template()
Prompt_directory = {
    "document_analysis": prompt_1,
    "document_comparision": Prompt_2}