import re
from collections import defaultdict
from collections import Counter
from unstructured.documents.elements import ElementType
from unstructured.documents.coordinates import RelativeCoordinateSystem
from unstructured.partition.pdf import partition_pdf

from spdp import get_database

from superduper.components.schema import FieldType
from superduper import ObjectModel
from superduper import logging

COLLECTION_NAME = "source"

# Build a chunks model and return chunk results with coordinate information.

def remove_sidebars(elements):

    if not elements:
        return elements
    points_groups = defaultdict(list)
    min_x = 99999999
    max_x = 0
    e2index = {e.id: i for i, e in enumerate(elements)}
    for e in elements:
        x_l = int(e.metadata.coordinates.points[0][0])
        x_r = int(e.metadata.coordinates.points[2][0])
        points_groups[(x_l, x_r)].append(e)
        min_x = min(min_x, x_l)
        max_x = max(max_x, x_r)
    sidebars_elements = set()
    for (x_l, x_r), es in points_groups.items():
        first_id = e2index[es[0].id]
        last_id = e2index[es[-1].id]
        on_left = first_id == 0 and x_l == min_x
        on_right = (last_id == len(elements) - 2) and x_r == max_x
        loc_match = [on_left, on_right]
        total_text = "".join(map(str, es))
        condiction = [
            any(loc_match),
            len(es) >= 3,
            re.findall("^[A-Z\s\d,]+$", total_text),
        ]
        if not all(condiction):
            continue
        sidebars_elements.update(map(lambda x: x.id, es))
        if on_left:
            check_page_num_e = elements[last_id + 1]
        else:
            check_page_num_e = elements[-1]
        if (
            check_page_num_e.category == ElementType.UNCATEGORIZED_TEXT
            and check_page_num_e.text.strip().isalnum()
        ):
            sidebars_elements.add(check_page_num_e.id)

    elements = [e for e in elements if e.id not in sidebars_elements]
    return elements


def remove_annotation(elements):

    page_num = max(e.metadata.page_number for e in elements)
    un_texts_counter = Counter(
        [e.text for e in elements if e.category == ElementType.UNCATEGORIZED_TEXT]
    )
    rm_text = set()
    for text, count in un_texts_counter.items():
        if count / page_num >= 0.5:
            rm_text.add(text)
    elements = [e for e in elements if e.text not in rm_text]
    return elements


def create_chunk_and_metadatas(page_elements, stride=2, window=5):
    page_elements = remove_sidebars(page_elements)
    for index, page_element in enumerate(page_elements):
        page_element.metadata.num = index
    datas = []
    for i in range(0, len(page_elements), stride):
        windown_elements = page_elements[i : i + window]
        chunk = "\n".join([e.text for e in windown_elements])
        source_elements = [e.to_dict() for e in windown_elements]
        datas.append(
            {
                "txt": chunk,
                "source_elements": source_elements,
            }
        )
    return datas

# Build a chunks model and return chunk results with coordinate information.
def get_chunks(pdf):

    elements = partition_pdf(pdf)
    elements = remove_annotation(elements)

    pages_elements = defaultdict(list)
    for element in elements:
        element.convert_coordinates_to_new_system(
            RelativeCoordinateSystem(), in_place=True
        )
        pages_elements[element.metadata.page_number].append(element)

    all_chunks_and_links = sum(
        [
            create_chunk_and_metadatas(page_elements)
            for _, page_elements in pages_elements.items()
        ],
        [],
    )
    return all_chunks_and_links

