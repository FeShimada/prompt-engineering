from dotenv import load_dotenv
load_dotenv()

from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOllama(model="llama3.1", temperature=0)


spec_to_model = PromptTemplate.from_template(
    """You are a senior Ext JS developer.
From the following feature spec, create the Ext JS 7 data model (Ext.data.Model) with fields, types and validators.
Only return code. No commentary.

Write all the code using markdown code blocks.

Spec:
{spec}
"""
) | llm | StrOutputParser()

model_to_views = PromptTemplate.from_template(
    """You are a senior Ext JS developer.
Given the Ext JS model below, create a CRUD screen in Ext JS 7 (classic toolkit) following the MVVM pattern:
- A list view with an Ext.grid.Panel: one column per model field, column filters and default sorting.
- A form view with an Ext.form.Panel: one field per model field, using the xtype that matches its type and validators.
- A ViewController handling create, edit, save and delete.
Keep it concise, production-oriented, and show code snippets.

Write all the code using markdown code blocks.

Model:
{model}
"""
) | llm | StrOutputParser()

commit_message = PromptTemplate.from_template(
    """You are a pragmatic frontend developer.
Write a single-line conventional commit message summarizing the new screen based on the model and views.

Model:
{model}

Views and controller:
{views}
"""
) | llm | StrOutputParser()


spec_text = """We need a Promotions screen in our Ext JS ERP.
Fields: id (int), description (string, required), startDate (date, required), endDate (date, required, >= startDate), discount (float, percentage between 0 and 100), active (boolean, default true).
We must support a list with filters and pagination, create, edit and delete.
"""

model = spec_to_model.invoke({"spec": spec_text})
views = model_to_views.invoke({"model": model})
commit = commit_message.invoke({"model": model, "views": views})


result_content = f"""# Prompt Chaining Result

## MODEL (Ext.data.Model)
{model}

## VIEWS & CONTROLLER (Ext JS MVVM)
{views}

## COMMIT
{commit}

---
**Pipeline Model:** llama3.1 (all steps)

"""

with open("prompt_chaining_result.md", "w", encoding="utf-8") as f:
    f.write(result_content)

print("Resultado salvo em prompt_chaining_result.md")
