# No-Train-Get-Attention

**No-Train-Get-Attention** is a tiny Python experiment for generating attention-like token weights without training a model.

It uses a deterministic heuristic instead of neural network layers: recent tokens receive stronger context influence, repeated words are boosted, common function words are suppressed, and similar-looking words can reinforce each other.

This is not Transformer self-attention. It is a lightweight scoring toy for exploring how "attention" can be approximated with simple rules.

## Features

- **No training required** - no model weights, datasets, or optimization loop.
- **No external dependencies** - runs with the Python standard library.
- **Token-level scores** - returns one normalized score for each input token.
- **Stop-word suppression** - common low-information English words receive lower attention.
- **Repetition boost** - repeated words become more important.
- **Similarity propagation** - words with shared prefixes can transfer part of their score to each other.
- **Small and hackable** - the whole implementation lives in `main.py`.

## How It Works

The main function is:

```python
att_pt(sen: list, qua: int = 4)
```

It expects a list of lowercase tokens and returns a list of floating-point weights with the same length.

The scoring pipeline is roughly:

1. Build a positional decay curve so nearby/recent context has more influence.
2. Accumulate attention-like mass for each token across the sequence.
3. Penalize words from `LOW_ATT_LIST`, such as articles, pronouns, prepositions, and common auxiliaries.
4. Detect similar words with `same_word()`.
5. Add related-word reinforcement.
6. Normalize scores so they can be compared as token weights.

## Quick Start

Clone the repository:

```bash
git clone https://github.com/Vesflux/No-Train-Get-Attention.git
cd No-Train-Get-Attention
```

Run the built-in demo:

```bash
python main.py
```

You should see a list of numeric weights:

```text
[0.0009, 0.0289, 0.0267, ...]
```

Each value corresponds to the token at the same position in the input sentence.

## Usage

```python
from main import att_pt

text = "the rich get richer and the poor get poorer"
tokens = text.lower().split()

scores = att_pt(tokens)

for token, score in zip(tokens, scores):
    print(f"{token:>10}  {score}")
```

Example output:

```text
       the  0.0194
      rich  0.1944
       get  0.1388
    richer  0.2014
       and  0.0299
       the  0.0074
      poor  0.1246
       get  0.1639
    poorer  0.1202
```

Exact values may change if you edit the scoring constants or stop-word list.

## API

### `att_pt(sen, qua=DEFAULT_QUA)`

Returns normalized attention-like weights for a token list.

Parameters:

- `sen`: list of tokens.
- `qua`: decimal precision used during intermediate rounding. Defaults to `4`.

Returns:

- `list[float]`: one score per token.

### `same_word(sen, kill_line=0, qua=DEFAULT_QUA)`

Finds words that are similar enough to reinforce each other.

Parameters:

- `sen`: list of tokens.
- `kill_line`: minimum similarity score required to keep a relation.
- `qua`: decimal precision.

Returns:

- `dict[str, list[list[str, float]]]`: mapping of each word to similar words and similarity scores.

## Notes

- Input should already be tokenized. The demo uses `lower().split()`.
- The built-in stop-word list is English-focused.
- Punctuation is not stripped automatically.
- This is an experimental heuristic, not a drop-in replacement for model attention.
- Scores are useful for quick exploration, ranking, highlighting, or educational demos.

## Repository Structure

```text
.
|-- main.py     # heuristic attention implementation and demo
|-- LICENSE     # GPL-3.0 license
`-- README.md
```

## License

This project is licensed under the **GNU General Public License v3.0**. See [LICENSE](LICENSE) for details.

## Author

Created by **Vesflux**.

- GitHub: [@Vesflux](https://github.com/Vesflux)
