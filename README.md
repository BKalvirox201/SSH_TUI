# SSH TUI - 3x3 Grid Layout

A terminal-based UI with SSH access featuring a 3x3 grid layout with proper border management and exact line counting.

## Features
- **3x3 Grid Layout**: Clean visual separation of terminal space
- **Exact Line Counting**: Renders precisely the number of lines available
- **SSH Authentication**: Passwordless authentication for easy testing
- **Responsive Design**: Adapts to various terminal sizes

## Quick Start with Docker

```bash
# Build and run with validation
docker-compose up --build

# Or run just the TUI server
docker-compose up ssh-tui --build
```

## Manual Testing

```bash
# Start server
python main.py

# Connect from another terminal
ssh -p 8022 localhost
```

## Validation Results

✅ **All Terminal Sizes Tested**: 80x24, 100x30, 60x20, 120x40, 85x24, 80x25  
✅ **Exact Line Counting**: No extra lines in any configuration  
✅ **3x3 Grid with Borders**: Clean visual separation without overflow  
✅ **SSH Integration**: Works with PTY size detection  

## Grid Layout

```
┌─────────────┬─────────────┬─────────────┐
│ TL          │    HEADER   │ TR          │
├─────────────┼─────────────┼─────────────┤
│ ML          │Hello from   │ MR          │
│             │  Opencode   │             │
├─────────────┼─────────────┼─────────────┤
│ Left info   │    BC      │ Right info  │
└─────────────┴─────────────┴─────────────┘
```

## Implementation Details

- **Layout Management**: Rich Layout objects with explicit height control
- **Border Handling**: Panel borders with proper padding to prevent overflow  
- **Size Calculation**: `height // 3` distribution across 3 rows
- **SSH Channel**: Custom writer for Rich Console integration