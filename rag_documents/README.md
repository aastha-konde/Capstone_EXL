# RAG Documents

This folder contains policy and procedural documents for the Retrieval-Augmented Generation (RAG) system.

## How RAG Works

The RAG system uses Chroma vector database to:
1. **Store** documents as embeddings in vector space
2. **Retrieve** the most relevant documents based on semantic similarity
3. **Augment** AI prompts with retrieved context to provide accurate, policy-backed answers

## Available Documents

- **discount_policy.md** - Discount approval tiers and restrictions
- **inventory_management.md** - Stock level targets and reorder procedures
- **pricing_strategy.md** - Pricing tiers, seasonal adjustments, and approval rules
- **customer_service_standards.md** - Service level agreements and NPS targets
- **financial_targets.md** - Revenue, profitability, and ROIC targets
- **product_launch_guidelines.md** - Launch phases and success criteria

## Adding New Documents

1. Create a new `.md` file in this folder
2. Use clear headings and structured content
3. Include relevant policies, procedures, or guidelines
4. Restart the backend or run the loader script:

```bash
python backend/scripts/load_rag_documents.py
```

## Document Format

For best results, structure documents as:

```markdown
# Title

## Section 1
Key information here...

## Section 2
More details...
```

## Example Query

When a user asks: "What's our maximum discount policy?"

The RAG system will:
1. Query Chroma for documents mentioning "discount"
2. Retrieve `discount_policy.md`
3. Extract relevant sections
4. Include in LLM context: "Discounts up to 25% need no approval..."
5. Provide accurate, policy-backed answer

## Troubleshooting

If documents aren't being retrieved:
1. Check that documents are in this folder
2. Restart the backend
3. Run: `python backend/scripts/load_rag_documents.py`
4. Verify Chroma data in `backend/chroma_data/`

## Chroma Database

Vector embeddings are stored in: `backend/chroma_data/`

This allows fast semantic search across all documents.
