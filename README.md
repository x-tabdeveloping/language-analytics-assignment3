# language-analytics-assignment3
Third Assignment for Language Analytics in Cultural Data Science

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

You can query songs by using the `src/query.py` script.

```bash
python3 src/query -a "Steely Dan" -w "cousin"
```

## Interface

| Parameter | Description | Default |
| - | - | - |
| `-a` or `--artist` | Name of the artist to query the songs of. | - |
| `-w` or `--query_word` | The seed word to base the semantic query on. | - |
| `-k` or `--k_expansion` | Number of termas most similar to the seed term to include in the query. | `10` |
| --print_songs | Flag to indicate whether the names of the songs should be printed. | `False` |
