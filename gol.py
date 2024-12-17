#!/usr/bin/env python
"""
The universe of the Game of Life is an infinite two-dimensional orthogonal grid of square cells,
each of which is in one of two possible states, alive or dead (populated or unpopulated).
Every cell interacts with its eight neighbours, which are the cells that are horizontally,
vertically, or diagonally adjacent.

At each step in time, the following transitions occur:

****************************************************************************************************
   1. Any live cell with fewer than two live neighbours dies, as if caused by underpopulation.
   2. Any live cell with two or three live neighbours lives on to the next generation.
   3. Any live cell with more than three live neighbours dies, as if by overpopulation.
   4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
****************************************************************************************************

The initial pattern constitutes the seed of the system.

The first generation is created by applying the above rules simultaneously to every cell in the
seed—births and deaths occur simultaneously, and the discrete moment at which this happens is
sometimes called a tick. The rules continue to be applied repeatedly to create further generations.

You run this script as a module:
    python -m Project.gol.py
"""

import argparse
import random
import json
import logging
import itertools
from pathlib import Path
from ast import literal_eval
from time import sleep

import Project.code_base as cb

__version__ = '1.0'
__desc__ = "A simplified implementation of Conway's Game of Life."

RESOURCES = Path(__file__).parent / "../_Resources/"


# -----------------------------------------
# IMPLEMENTATIONS FOR HIGHER GRADES, C - B
# -----------------------------------------

def load_seed_from_file(_file_name: str) -> tuple:
    """ Load population seed from file. Returns tuple: population (dict) and world_size (tuple). """
    pass


def create_logger() -> logging.Logger:
    """ Creates a logging object to be used for reports. """
    pass


def simulation_decorator(func):
    """ Function decorator, used to run full extent of simulation. """
    pass


# -----------------------------------------
# BASE IMPLEMENTATIONS
# -----------------------------------------

def parse_world_size_arg(_arg: str) -> tuple:
    """ Parse width and height from command argument. """
    pass


def populate_world(_world_size: tuple, _seed_pattern: str = None) -> dict:
    """ Populate the world with cells and initial states. """
    pass


def calc_neighbour_positions(_cell_coord: tuple) -> list:
    """ Calculate neighbouring cell coordinates in all directions (cardinal + diagonal).
    Returns list of tuples. """
    pass


def run_simulation(_generations: int, _population: dict, _world_size: tuple):
    """ Runs simulation for specified amount of generations. """
    pass


def update_world(_cur_gen: dict, _world_size: tuple) -> dict:
    """ Represents a tick in the simulation. """
    pass


def count_alive_neighbours(_neighbours: list, _cells: dict) -> int:
    """ Determine how many of the neighbouring cells are currently alive. """
    pass


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
