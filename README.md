# ascii_table

ASCII/Unicode reference and encoding toolkit.

## Usage

```bash
python3 ascii_table.py lookup "Hello🐺"
python3 ascii_table.py ascii                    # full ASCII table
python3 ascii_table.py range 0x2600 0x26FF      # Unicode block
python3 ascii_table.py search "arrow" -n 20     # search by name
python3 ascii_table.py encode "café" -e utf-8,utf-16
python3 ascii_table.py decode "C3A9" -e utf-8
python3 ascii_table.py stats "Hello World 🌍"
```

## Features

- Character lookup (code point, hex, binary, category, name)
- Full ASCII table with control character names
- Unicode range display
- Name search across all Unicode
- Multi-encoding encode/decode
- Text Unicode statistics
- Zero dependencies
