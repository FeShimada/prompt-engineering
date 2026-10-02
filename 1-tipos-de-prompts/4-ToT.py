from langchain_ollama import ChatOllama
from dotenv import load_dotenv
from utils import print_llm_result

load_dotenv()
msg1 = """
You are a senior software engineer. 
A user reports that an API request to the endpoint `/users` is taking 5 seconds to respond, which is too slow. 
Think in a Tree of Thought manner: 
- Generate at least 3 different possible causes for this latency. 
- For each cause, reason step by step about how likely it is and how you would verify it. 
- Then compare the branches and choose the most plausible one as the primary hypothesis. 
- Finish with a recommended next action to debug or fix the issue.
"""

msg2 = f"""
You are designing a service that processes millions of images daily. 
Think in a Tree of Thought manner: 
- Generate at least 3 different architecture options. 
- For each option, reason step by step about scalability, cost, and complexity. 
- Compare the options. 
- Choose the best trade-off and explain why it is superior to the others.
- Finish with "Final Answer: " + the chosen option.
"""

msg3 = f"""
You are designing a service that processes millions of images daily. 
Think in a Tree of Thought manner: 
- Think about at least 3 different architecture options. 
- For each option, reason step by step about scalability, cost, and complexity. 
- Compare the options. 
- Choose the best trade-off and explain why it is superior to the others.
- Finish with "Final Answer: " + the chosen option with 6 words or less.

- OUTPUT ONLY THE FINAL ANSWER, WITHOUT ANY OTHER TEXT.
"""

msg4 = """
You are a senior Roblox game designer. I'm building a mining game where players collect pickaxes of different rarities. Each pickaxe has exactly 3 powers.

Pickaxe:
- Name: Magma Pickaxe
- Rarity: Epic
- Type: Fire
- Description: Forged in the core of a volcano, it melts through rock instead of breaking it.

Think in a Tree of Thought manner:
- Generate 15 creative power ideas for this pickaxe, based on its type and description. For each: name and a one-line description.
- Score each idea from 1 to 5 against these rules:
  Rule 1 - Theme: does it fit the pickaxe's type and description?
  Rule 2 - Balance: is its strength appropriate for the rarity, without breaking the game economy?
  Rule 3 - Feasibility: can it be implemented in Roblox (Luau) with reasonable effort?
- Prune: discard ideas with any score below 3 and merge near-duplicates.
- For the remaining ideas, reason step by step about how they would work together on the same pickaxe (synergy or conflict).
- Compare the combinations and choose the best 3 powers, explaining why they beat the alternatives.
- Finish with "Final Answer: " + the 3 chosen powers.
"""

# llm = ChatOllama(model="ollama-gpt-3")
llm = ChatOllama(model="llama3.1")
# llm = ChatOllama(model="ollama-gpt-5-nano") # reasoning model


# response1 = llm.invoke(msg1)
response2 = llm.invoke(msg2)
# response3 = llm.invoke(msg3)
response4 = llm.invoke(msg4)

# print_llm_result(msg1, response1)
print_llm_result(msg2, response2)
# print_llm_result(msg3, response3)
print_llm_result(msg4, response4)
