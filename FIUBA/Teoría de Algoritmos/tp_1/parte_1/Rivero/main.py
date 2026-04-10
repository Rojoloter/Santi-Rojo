import sys
from tdas import AVLTree

def search_optimal_stack(stacks: AVLTree[int, None], card: int) -> int | None:
    """
    Search for the stack where top_card is the minimal posible but greater than the passed card.
    Returns the key (card_on_top) of the stack founded (or None).
    """
    for top_card, _ in stacks.range(low=card+1):
        return top_card
    return None

def push(stacks: AVLTree[int, None], key: int | None, card: int):
    """
    Push card in stack of passed key.
    If key is None it creates another stack.
    """
    if key is not None:
        del stacks[key]
    stacks[card] = None
    
def main():    
    stacks = AVLTree[int, None]()
    try:
        with open(sys.argv[1], "r", encoding="utf-8") as file:
            for line in file:
                card = int(line.strip())
                stack_key = search_optimal_stack(stacks, card)
                push(stacks, stack_key, card)
            print(len(stacks))

    except FileNotFoundError:
        print(f"Error: El archivo '{sys.argv[1]}' no existe.")
    except Exception as e:
        print(f"Error: {e}")
        
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: formato invalido.")
        print("Formato de ejecución del programa: `main.py <archivo>`.")
        sys.exit(1)
    main()

