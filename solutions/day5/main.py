from collections import defaultdict
from sys import argv
from typing import Dict, List, Set, Tuple


def validate_page_updates(page_updates: List[int], page_dependencies: Dict[int, Set[int]]) -> bool:
    subsequent_pages = set(page_updates)

    for i in range(len(page_updates)):
        page = page_updates[i]
        dependencies = page_dependencies[page]

        subsequent_pages.remove(page)

        if not subsequent_pages.isdisjoint(dependencies):
            return False

    return True 


def reorder_page_updates(page_updates: List[int], page_dependencies: Dict[int, Set[int]]) -> List[int]:
    page_dependencies = get_relevent_page_dependencies_for_reordering(page_updates, page_dependencies)

    page_to_dependent_pages: Dict[int, Set[int]] = defaultdict(set)
    page_to_remaining_dependency_count: Dict[int, int] = {}

    for dependent_page, dependencies in page_dependencies.items():
        for page in dependencies:
            page_to_dependent_pages[page].add(dependent_page)

    stack: List[int] = []

    for dependent_page, dependencies in page_dependencies.items():
        dependency_count = len(dependencies)
        page_to_remaining_dependency_count[dependent_page] = dependency_count

        if dependency_count == 0:
            stack.append(dependent_page)

    reordered_page_updates: List[int] = []

    while len(stack) > 0:
        page = stack.pop()
        reordered_page_updates.append(page)

        dependent_pages = page_to_dependent_pages[page]

        for dependent_page in dependent_pages:
            page_to_remaining_dependency_count[dependent_page] -= 1

            if page_to_remaining_dependency_count[dependent_page] == 0:
                stack.append(dependent_page)

    assert len(page_updates) == len(reordered_page_updates), "Reordered page updates size does not match"
    assert set(page_updates) == set(reordered_page_updates), "Reordered page updates do not contains correct values"

    return reordered_page_updates


def get_relevent_page_dependencies_for_reordering(page_updates: List[int], page_dependencies: Dict[int, Set[int]]) -> Dict[int, Set[int]]:
    relevent_page_dependencies: Dict[int, Set[int]] = {}

    for page, dependencies in page_dependencies.items():
        if page in page_updates:
            relevent_page_dependencies[page] = dependencies.intersection(page_updates)

    return relevent_page_dependencies


def setup_page_dependencies(page_ordering_rules: List[Tuple[int, int]]) -> Dict[int, Set[int]]:
    page_dependencies: Dict[int, Set[int]] = {}

    for (before, after) in page_ordering_rules:
        if after not in page_dependencies:
            page_dependencies[after] = set()

        page_dependencies[after].add(before)

        if (before not in page_dependencies):
            page_dependencies[before] = set()

    return page_dependencies


def get_page_data(file_path: str) -> Tuple[List[Tuple[int, int]], List[List[int]]]:
    with open(file_path, "r") as file:
        sections = file.read().strip().split("\n\n")
        return (get_page_ordering_rules(sections[0]), get_page_updates(sections[1]))
    

def get_page_ordering_rules(data: str) -> List[Tuple[int, int]]:
    page_ordering_rules: List[Tuple[int, int]] = []

    for x in data.strip().split("\n"):
        pages = [int(x) for x in x.split("|")]
        page_ordering_rules.append((pages[0], pages[1]))

    return page_ordering_rules


def get_page_updates(data: str) -> List[List[int]]:
    page_updates: List[List[int]] = []

    for x in data.strip().split("\n"):
        page_updates.append([int(x) for x in x.split(",")])

    return page_updates


if __name__ == "__main__":
    input_file_path = argv[1]
    (page_ordering_rules, page_updates) = get_page_data(input_file_path)

    page_dependencies = setup_page_dependencies(page_ordering_rules)

    middle_page_sum = 0
    for page_update in page_updates:
        if validate_page_updates(page_update, page_dependencies):
            middle_page = page_update[len(page_update) // 2]
            middle_page_sum += middle_page
    print(f"Part 1: {middle_page_sum}")

    reordered_middle_page_sum = 0
    for page_update in page_updates:
        if validate_page_updates(page_update, page_dependencies):
            continue

        relevent_page_dependencies = get_relevent_page_dependencies_for_reordering(page_update, page_dependencies)
        reordered_page_update = reorder_page_updates(page_update, relevent_page_dependencies)

        middle_page = reordered_page_update[len(reordered_page_update) // 2]
        reordered_middle_page_sum += middle_page
    print(f"Part 2: {reordered_middle_page_sum}")
