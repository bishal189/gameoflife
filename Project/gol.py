import argparse
import random
from time import sleep
import Project.code_base as cb

__version__ = '1.0'
__desc__ = "A simplified implementation of Conway's Game of Life."

# -----------------------------------------
# BASE IMPLEMENTATIONS
# -----------------------------------------

def parse_world_size_arg(_arg: str) -> tuple:
    """ Parse width and height from command argument. """
    try:
        width, height = map(int, _arg.split('x'))
        if width < 1 or height < 1:
            raise ValueError("Both width and height need to have positive values above zero.")
        return width, height
    except (ValueError, AssertionError):
        print("World size should contain width and height, separated by ‘x’. Ex: ‘80x40’")
        print("Using default world size: 80x40")
        return 80, 40


def calc_neighbour_positions(_cell_coord: tuple) -> list:
    """ Calculate neighbouring cell coordinates in all directions (cardinal + diagonal). """
    x, y = _cell_coord
    offsets = [-1, 0, 1]
    neighbours = [
        (x + dx, y + dy)
        for dx in offsets for dy in offsets
        if not (dx == 0 and dy == 0)
    ]
    return neighbours


def populate_world(_world_size: tuple, _seed_pattern: str = None) -> dict:
    """ Populate the world with cells and initial states. """
    width, height = _world_size
    population = {}
    pattern = cb.get_pattern(_seed_pattern, _world_size) if _seed_pattern else []

    for y in range(height):
        for x in range(width):
            if x == 0 or y == 0 or x == width - 1 or y == height - 1:
                population[(x, y)] = None  # Rim cell
            else:
                state = cb.STATE_ALIVE if (x, y) in pattern else cb.STATE_DEAD
                if not _seed_pattern:  # Randomize cells if no seed
                    state = cb.STATE_ALIVE if random.randint(0, 20) > 16 else cb.STATE_DEAD
                population[(x, y)] = {
                    "state": state,
                    "neighbours": calc_neighbour_positions((x, y))
                }
    return population


def count_alive_neighbours(_neighbours: list, _cells: dict) -> int:
    """ Determine how many of the neighbouring cells are currently alive. """
    return sum(1 for pos in _neighbours if pos in _cells and _cells[pos] and _cells[pos]['state'] == cb.STATE_ALIVE)


def update_world(_cur_gen: dict, _world_size: tuple) -> dict:
    """ Represents a tick in the simulation. """
    next_gen = {}
    for coord, cell in _cur_gen.items():
        if cell is None:  # Rim cells remain unchanged
            next_gen[coord] = None
            continue

        alive_neighbours = count_alive_neighbours(cell['neighbours'], _cur_gen)
        next_state = cell['state']

        # Apply Conway's Rules
        if cell['state'] == cb.STATE_ALIVE:
            if alive_neighbours < 2 or alive_neighbours > 3:
                next_state = cb.STATE_DEAD
        elif cell['state'] == cb.STATE_DEAD and alive_neighbours == 3:
            next_state = cb.STATE_ALIVE

        next_gen[coord] = {
            "state": next_state,
            "neighbours": cell['neighbours']
        }
    return next_gen


def run_simulation(_nth_generation: int, _population: dict, _world_size: tuple, generation: int = 1):
    """ Runs simulation for specified amount of generations recursively. """
    if _nth_generation == 0:
        return

    # Display the current generation grid
    cb.clear_console()
    print(f"Generation {generation}")
    for y in range(_world_size[1]):
        for x in range(_world_size[0]):
            cell = _population.get((x, y))
            if cell is None:  # Rim cell
                cb.progress(cb.get_print_value(cb.STATE_RIM))
            else:
                cb.progress(cb.get_print_value(cell['state']))
        print()  # Newline after each row

    sleep(0.2)

    # Compute the next generation
    next_population = update_world(_population, _world_size)

    # Recursively call for the next generation
    run_simulation(_nth_generation - 1, next_population, _world_size, generation + 1)


def main():
    """ The main program execution. YOU MAY NOT MODIFY ANYTHING IN THIS FUNCTION!! """
    epilog = "DT179G Project v" + __version__
    parser = argparse.ArgumentParser(description=__desc__, epilog=epilog, add_help=True)
    parser.add_argument('-g', '--generations', dest='generations', type=int, default=50,
                        help='Amount of generations the simulation should run. Defaults to 50.')
    parser.add_argument('-s', '--seed', dest='seed', type=str,
                        help='Starting seed. If omitted, a randomized seed will be used.')
    parser.add_argument('-ws', '--worldsize', dest='worldsize', type=str, default='80x40',
                        help='Size of the world, in terms of width and height. Defaults to 80x40.')
    parser.add_argument('-f', '--file', dest='file', type=str,
                        help='Load starting seed from file.')

    args = parser.parse_args()

    try:
        if not args.file:
            raise AssertionError
        population, world_size = load_seed_from_file(args.file)
    except (AssertionError, FileNotFoundError):
        world_size = parse_world_size_arg(args.worldsize)
        population = populate_world(world_size, args.seed)

    run_simulation(args.generations, population, world_size)


if __name__ == "__main__":
    main()
