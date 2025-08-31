import os
import json
import re
from docx import Document
import roner
import openai
from openai import OpenAI
from utils import batcher, paragraph_iterator

# -----------------------------
# CONFIG
# -----------------------------
openai.api_key = os.getenv("OPENAI_API_KEY")  # Set your OpenAI key in environment variables
CHUNK_SIZE = 50  # number of names per API call

NAME_PARTICLES = {"de", "van", "von", "di", "da", "der", "le", "la"}


# -----------------------------
# LOCAL NER FUNCTION
# -----------------------------
def extract_names(doc_path):
    """Extract person names from a docx using roner, including initials, particles, hyphens."""
    doc = Document(doc_path)
    ner = roner.NER(named_persons_only=True, use_gpu=True, batch_size=6, num_workers=4)

    name_list = []
    for batch in batcher(paragraph_iterator(doc), ner.batch_size):
        output_texts = ner(batch)
        for output_text in output_texts:
            current_name = []
            for word in output_text['words']:
                text = word['text']
                if (word['tag'] == 'PERSON' or
                        re.match(r'^[A-Z]\.$', text) or
                        text.lower() in NAME_PARTICLES or
                        '-' in text):
                    current_name.append(text)
                else:
                    if current_name:
                        name_list.append(' '.join(current_name))
                        current_name = []
            if current_name:
                name_list.append(' '.join(current_name))
    # Deduplicate
    return list(dict.fromkeys(name_list))


# -----------------------------
# GPT ANNOTATION FUNCTION
# -----------------------------


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
def annotate_names_with_gpt(name_chunk):
    """Send a list of names to GPT and get explanations for each."""
    names_str = "\n".join(name_chunk)
    prompt = f"""
You are an expert annotator. For each of the following names, provide a short explanation or context as if creating an index for a book. 
Return a JSON array with objects in the format: {{"name": "NAME", "explanation": "EXPLANATION"}}.

Names:
{names_str}
"""
    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    content = response.choices[0].message.content

    # Ensure JSON parsing
    import json, re
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        content_fixed = re.sub(r'([a-zA-Z0-9_]+):', r'"\1":', content)
        return json.loads(content_fixed)

# -----------------------------
# MAIN FUNCTION
# -----------------------------
def create_annotated_index(doc_path, output_path="annotated_index.json"):
    print("Extracting names with local NER...")
    all_names = extract_names(doc_path)
    print(f"Found {len(all_names)} unique names.")

    annotated_index = []
    for i in range(0, len(all_names), CHUNK_SIZE):
        chunk = all_names[i:i + CHUNK_SIZE]
        print(f"Annotating names {i + 1} to {i + len(chunk)}...")
        annotations = annotate_names_with_gpt(chunk)
        annotated_index.extend(annotations)

    # Save to JSON
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(annotated_index, f, ensure_ascii=False, indent=2)

    print(f"Annotated index saved to {output_path}")
    return annotated_index


# -----------------------------
# USAGE EXAMPLE
# -----------------------------
if __name__ == "__main__":
    doc_file = r"C:\Users\Tudor\Desktop\aaa.docx"
    create_annotated_index(doc_file)
