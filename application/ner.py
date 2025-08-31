
from docx import Document
import roner

from utils import *

import re

def name_filter(doc):
    name_list = []

    print("Initializing NER...")
    ner = roner.NER(named_persons_only=True, use_gpu=True, batch_size=6, num_workers=4)
    print("Processing text...")

    for batch in batcher(paragraph_iterator(doc), ner.batch_size):
        output_texts = ner(batch)

        for output_text in output_texts:
            current_name = []
            for word in output_text['words']:
                text = word['text']

                # Keep word if tagged PERSON or if it's an initial (e.g., "I.")
                if word['tag'] == 'PERSON' or re.match(r'^[A-Z]\.$', text):
                    current_name.append(text)
                else:
                    if current_name:
                        # Append the full name accumulated so far
                        name_list.append(' '.join(current_name))
                        current_name = []

            # Catch a name at the very end of the paragraph
            if current_name:
                name_list.append(' '.join(current_name))


    return name_list