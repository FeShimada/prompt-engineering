from langchain_ollama import ChatOllama
from dotenv import load_dotenv
from utils import print_llm_result

load_dotenv()
msg1 = """
You are a senior frontend engineer. A junior developer asked you how to avoid unnecessary re-renders and improve performance in a React application.
Follow the Skeleton of Thought approach: 

Step 1: Generate only the skeleton of your answer in 3–5 concise bullet points. 
Step 2: Expand each bullet point into a clear and detailed explanation with examples. 
Make sure the final answer is structured and easy to follow.
"""

msg2 = f"""
You are a frontend architect. I want you to produce an Architecture Decision Record (ADR) about building new modules of a legacy ExtJS application in React, migrating incrementally instead of rewriting everything at once.

Follow the Skeleton of Thought approach:
Step 1: First, output only the skeleton of the ADR as section headers (no explanations yet). 
Use the standard ADR structure with 5 sections: Context, Decision, Alternatives Considered, Consequences, References. 
Step 2: After showing the skeleton, expand each section with clear and detailed content. 
Keep the final ADR professional, structured, and easy to read.
"""

msg3 = f"""
You are a senior QA automation engineer specialized in Playwright. I want you to help me plan an end-to-end test suite in TypeScript for a product management screen built in React.

Follow the Skeleton of Thought approach:

Step 1: Output only the skeleton of the solution in 6–8 concise bullet points.
The skeleton must cover: project structure, playwright.config.ts setup, Page Object Model, fixtures, selector strategy, API mocking, assertions, and CI execution. Do not expand yet.

Step 2: Expand each bullet point with clear technical details, examples, and Playwright best practices.
Include sample code snippets in TypeScript (page objects, fixtures, tests) and considerations about user-facing locators (e.g., getByRole, getByTestId), mocking the backend with page.route, avoiding flaky tests with auto-waiting and web-first assertions, and how to organize the project into folders (tests, pages, fixtures).
Use concise and professional language.

The screen must support CRUD operations for products with fields: id, name, description, price, stock.
"""

msg4 = """
You are a senior Roblox game designer. I'm building a mining game where players collect pickaxes of different rarities. I want you to create the pickaxe catalog for the game.

Follow the Skeleton of Thought approach:

Step 1: Output only the skeleton of the catalog.
List the 5 rarities in order (Common, Rare, Epic, Legendary, Mythic) and, under each one, a single pickaxe with its name and type (e.g., Fire, Ice, Lightning). Do not describe the pickaxes or their powers yet.

Step 2: Expand each pickaxe with:
- A short description (lore) that matches its type.
- Exactly 3 powers, each with a name, a one-line description and its gameplay effect (e.g., +20% mining speed, 10s cooldown).
- A balancing note explaining why its strength fits the rarity.

Powers must scale with rarity: higher rarities unlock new mechanics, not just bigger numbers.
Keep the final catalog structured and easy to read.
"""

# llm = ChatOllama(model="ollama-gpt-3")
llm = ChatOllama(model="llama3.1")
# llm = ChatOllama(model="ollama-gpt-5-nano") # reasoning model


response1 = llm.invoke(msg1)
response2 = llm.invoke(msg2)
response3 = llm.invoke(msg3)
response4 = llm.invoke(msg4)

print_llm_result(msg1, response1)
print_llm_result(msg2, response2)
print_llm_result(msg3, response3)
print_llm_result(msg4, response4)
