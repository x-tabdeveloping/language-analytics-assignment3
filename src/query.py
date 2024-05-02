import argparse
import warnings
from pathlib import Path

import gensim.downloader as api
import numpy as np
import pandas as pd
from codecarbon import EmissionsTracker
from gensim.utils import tokenize
from thefuzz import process


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="Query Expansion")
    parser.add_argument(
        "-a", "--artist", help="Name of the artist to query songs of.", type=str
    )
    parser.add_argument(
        "-w", "--query_word", help="Word to semantically query.", type=str
    )
    parser.add_argument(
        "-k",
        "--k_expansion",
        help="Number of terms to expand the search query to.",
        type=int,
        default=10,
    )
    parser.add_argument(
        "--print_songs",
        default=False,
        action="store_true",
        help="Prints song names that contain the search terms if the flag is added.",
    )
    return parser


def contains_search_term(text: str, search_terms: list[str]) -> bool:
    tokens = tokenize(text, lower=True)
    for token in tokens:
        if token in search_terms:
            return True
    return False


def main():
    parser = create_parser()
    args = parser.parse_args()
    emissions_dir = Path("emissions")
    emissions_dir.mkdir(exist_ok=True)
    with EmissionsTracker(
        project_name="query_expansion",
        save_to_file=True,
        output_file="emissions.csv",
        output_dir=emissions_dir,
    ) as tracker:
        tracker.start_task("load_model")
        wv = api.load("glove-wiki-gigaword-50")
        tracker.stop_task()
        tracker.start_task("load_data")
        songs = pd.read_csv("dat/Spotify Million Song Dataset_exported.csv")
        tracker.stop_task()
        tracker.start_task("fuzzy_finding")
        # Fuzzy finding artist
        artist, _ = process.extractOne(args.artist, songs["artist"].unique())
        if artist.lower() != args.artist.lower():
            warnings.warn(f"{args.artist} not found, the closest match is {artist}.")
        # Filtering for artist
        songs = songs[songs["artist"] == artist]
        # Fuzzy finding query word
        query_word, _ = process.extractOne(args.query_word, list(wv.index_to_key))
        if query_word.lower() != args.query_word.lower():
            warnings.warn(
                f"{args.query_word} not found, the closest match is {query_word}."
            )
        tracker.stop_task()
        tracker.start_task("query_expansion")
        most_similar = wv.most_similar(positive=query_word, topn=args.k_expansion)
        search_words = [query_word] + [word.lower() for word, _ in most_similar]
        tracker.stop_task()
        tracker.start_task("querying")
        # Tokenizing songs
        songs["contains_search_term"] = songs["text"].map(
            lambda t: contains_search_term(t, search_words)
        )
        n_total = len(songs.index)
        n_songs_containing_search_terms = np.sum(songs["contains_search_term"])
        percentage = (n_songs_containing_search_terms / n_total) * 100
        tracker.stop_task()
    print("-------------------------------------------------------------\n")
    print(
        "\nThe most similar terms are the following: {terms}".format(
            terms=", ".join(search_words)
        )
    )
    print("-------------------------------------------------------------\n")
    print(
        f"Artist {artist} has {n_songs_containing_search_terms} songs ({percentage:.2f}%) that contain words related to {query_word}."
    )
    if args.print_songs:
        relevant_songs = songs[songs["contains_search_term"]]["song"]
        print("These are: ")
        for song in relevant_songs:
            print(f" - {song}")
    print("-------------------------------------------------------------")


if __name__ == "__main__":
    main()
