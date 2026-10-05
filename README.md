# tznow

Show current time in multiple timezones at once.

## Install

```bash
pip install tznow
```

## Usage

```bash
# Default: UTC, New York, London, Tokyo
$ tznow
UTC                  06:30:45  2026-10-05  UTC
America/New_York     02:30:45  2026-10-05  EDT
Europe/London        07:30:45  2026-10-05  BST
Asia/Tokyo           15:30:45  2026-10-05  JST

# Specify timezones
$ tznow UTC ny tokyo paris

# Full timezone names
$ tznow America/Los_Angeles Europe/Berlin

# Aliases: utc, ny, nyc, london, paris, berlin, tokyo, sydney, sf, la
```

## As a Python library

```python
from tznow.cli import get_times

results = get_times(["UTC", "ny", "tokyo"])
for line in results:
    print(line)
```

## License

MIT
