"""tznow CLI - show current time across multiple timezones."""

import sys
import zoneinfo
from datetime import datetime
from typing import List, Optional

# Default timezones to show if none specified
DEFAULT_ZONES = ["UTC", "America/New_York", "Europe/London", "Asia/Tokyo"]

# Aliases for common timezone names
ALIASES = {
    "utc": "UTC",
    "ny": "America/New_York",
    "nyc": "America/New_York",
    "london": "Europe/London",
    "paris": "Europe/Paris",
    "berlin": "Europe/Berlin",
    "tokyo": "Asia/Tokyo",
    "sydney": "Australia/Sydney",
    "sf": "America/Los_Angeles",
    "la": "America/Los_Angeles",
    "sf": "America/Los_Angeles",
}


def format_time(dt: datetime, tz_name: str, width: int = 30) -> str:
    """Format a datetime for display with timezone name."""
    time_str = dt.strftime("%H:%M:%S")
    date_str = dt.strftime("%Y-%m-%d")
    tz_short = dt.strftime("%Z")
    return f"{tz_name:<20} {time_str}  {date_str}  {tz_short}"


def resolve_timezone(name: str) -> zoneinfo.ZoneInfo:
    """Resolve timezone name, checking aliases first."""
    normalized = name.lower().strip()
    if normalized in ALIASES:
        return zoneinfo.ZoneInfo(ALIASES[normalized])
    return zoneinfo.ZoneInfo(name)


def get_times(timezones: Optional[List[str]] = None, now: Optional[datetime] = None) -> List[str]:
    """Get formatted time strings for given timezones.
    
    Args:
        timezones: List of timezone names/aliases. Uses defaults if None.
        now: Current datetime (for testing). Uses datetime.now() if None.
    
    Returns:
        List of formatted time strings.
    """
    if timezones is None:
        timezones = DEFAULT_ZONES
    if now is None:
        now = datetime.now(zoneinfo.ZoneInfo("UTC"))
    
    results = []
    for tz_name in timezones:
        try:
            tz = resolve_timezone(tz_name)
            local_time = now.astimezone(tz)
            results.append(format_time(local_time, tz_name))
        except Exception as e:
            results.append(f"{tz_name:<20} ERROR: {e}")
    
    return results


def main(argv: Optional[List[str]] = None) -> int:
    """Main entry point for tznow CLI.
    
    Args:
        argv: Command line arguments. Uses sys.argv if None.
    
    Returns:
        Exit code (0 for success).
    """
    if argv is None:
        argv = sys.argv[1:]
    
    # Parse arguments
    timezones = argv if argv else DEFAULT_ZONES
    
    # Get and print times
    results = get_times(timezones)
    print("\n".join(results))
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
