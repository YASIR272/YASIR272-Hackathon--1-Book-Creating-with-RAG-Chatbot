---
id: 1
title: Create Book RAG Constitution
stage: constitution
date: 2025-12-16
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: user
command: /sp.constitution
labels: [constitution, docusaurus, rag, chatbot, spec-kit-plus]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

You are a prompt engineer with 20 years of experience:

I give the project requirements and also i give you reference constitution file. Your task is generate prompt based on the project requirements of sp.consitution file.

Project Requirements:

"""You are required to complete a unified book project using Claude Code and Spec-Kit Plus. The core deliverables are:

1. AI/Spec-Driven Book Creation: Write a book using Docusaurus and deploy it to GitHub Pages. You will use Spec-Kit Plus ( https://github.com/panaversity/spec-kit-plus/ ) and Claude Code ( https://www.claude.com/product/claude-code ) to write the book.

2. Integrated RAG Chatbot Development: Build and embed a Retrieval-Augmented Generation (RAG) chatbot within the published book. This chatbot, utilizing the OpenAI Agents/ChatKit SDKs, FastAPI, Neon Serverless Postgres database, and Qdrant Cloud Free Tier, must be able to answer user questions about the book's content, including answering questions based only on text selected by the user. """

her

## Response snapshot

Created a comprehensive constitution file for the Docusaurus Book with RAG Chatbot project that addresses all specified requirements including AI/Spec-driven development, Docusaurus-first approach, RAG integration excellence, deployment-ready architecture, and performance standards. The constitution includes core principles, technical constraints, development workflow, and governance guidelines.

## Outcome

- ✅ Impact: Created foundational constitution file for Docusaurus book and RAG chatbot project
- 🧪 Tests: none
- 📁 Files: Updated .specify/memory/constitution.md with project-specific principles
- 🔁 Next prompts: Proceed with feature specification and planning
- 🧠 Reflection: Constitution properly captures all project requirements and constraints

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin feature specification based on constitution