# language-analytics-assignment3
Third Assignment for Language Analytics in Cultural Data Science

The assignments is about using word embeddings for expanding search queries in a lyrics database.
The code finds how many, and what proportion of a given artists' songs contain a given keyword or words semantically closely related to that keyword.

I chose a fault tolerant approach, this has the following implications:
 - If the given artist can't be exactly matched, you will get a warning, but the code will continue running with the closest fuzzy match. 
 - If the given keyword can't be exactly matched in the embedding models' vocabulary, you will get a warning, but the code will continue running with the closest fuzzy match. 

## Setup

You will need to download the [Spotfy Million Song dataset](https://www.kaggle.com/datasets/joebeachcapital/57651-spotify-songs).
the file should be placed in a `dat` directory.

```
- dat/
    - "Spotify Million Song Dataset_exported.csv"
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

You can query songs by using the `src/query.py` command line interface for checking how many songs of a given artist contain a keyword or closesly related word.

```bash
python3 src/query.py -a "Steely Dan" -w "cousin"
```
```
The most similar terms are the following: cousin, nephew, brother, son, uncle, eldest, grandson, daughter, father, grandfather, niece
-------------------------------------------------------------

Artist Steely Dan has 15 songs (17.05%) that contain words related to cousin.
-------------------------------------------------------------
```

By passing the `--print_songs` flag you can also see the individual songs containing these terms.

```
These are: 
 - Cousin Dupree
 - Almost Gothic
 - Babylon Sisters
 - Chain Lightning
 - Deacon Blues
 - Don't Take Me Alive
 - Godwhacker
 - Green Flower Street
 - Kid Charlemagne
 - Pixeleen
 - Pretzel Logic
 - Sign In Stranger
 - Time Out Of Mind
 - Turn That Heartbeat Over Again
 - Two Against Nature
```

### Parameters

| Parameter | Description | Default |
| - | - | - |
| `-a` or `--artist` | Name of the artist to query the songs of. | - |
| `-w` or `--query_word` | The seed word to base the semantic query on. | - |
| `-k` or `--k_expansion` | Number of termas most similar to the seed term to include in the query. | `10` |
| `--print_songs` | Flag to indicate whether the names of the songs should be printed. | `False` |

> Additionally the script will produce csv files with the CO2 emissions of the substasks in the code (`emissions/`).
> This is necessary for Assignment 5, and is not directly relevant to this assignment.

> Note: The `emissions/emissions.csv` file should be ignored. This is due to the fact, that codecarbon can't track process and task emissions at the same time.

## Potential Limitations

It would be good to know how the number of expansion terms affect results and to which extent the pipeline is sensitive to this parameter.
Systematic evaluations might give us more information about the implications of setting higher or lower values.
