# langchain_prompts

Prompts are the input instructions or query given to a model to guide it's output 

Static Prompts :

These act like a standard instruction set. Because they do not change, they ensure high consistency, which is useful when you need the AI to perform the exact same task every time (e.g."Summarize this text in three bullet points"). However, they lack the flexibility to handle nuanced user needs or evolving conversational history.

Dynamic prompts 

Dynamic Prompts (The "Barista"):

These function more like templates, where specific parts are filled in at runtime. By using placeholders (e.g.{user_name} or {context}), dynamic prompts allow the AI to "know" who it is talking to and what data it should reference. This is essential for:
Personalization: Tailoring responses based on user profiles and past interactions.
Context Awareness: Incorporating data from Retrieval-Augmented Generation (RAG) pipelines to provide accurate, up-to-date answers.
Agentic Workflows: Allowing AI agents to adjust their behavior based on the current step in a task.
