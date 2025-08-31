

def paragraph_iterator(doc):
    """This returns one paragraph at a time, skips ones that are empty"""
    for p in doc.paragraphs:
        if p.text.strip():
            yield p.text


def batcher(iterator, batch_size):
    """Returns a list of paragraphs of the number batch_size"""
    batch = []
    for item in iterator:
        batch.append(item)
        if len(batch) == batch_size:
            yield batch
            batch = []
    if batch:
        yield batch