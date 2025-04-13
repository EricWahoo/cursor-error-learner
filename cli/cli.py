"""
Command-line interface for the error learner package.

This module provides a CLI for analyzing and managing error tracking.
"""

import argparse
import logging
from typing import Optional
from error_learner.core import ErrorTracker
from error_learner.utils import setup_logging, get_error_stats, get_error_count

def main(args: Optional[argparse.Namespace] = None) -> None:
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(description="Error Learner CLI")
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Set the logging level"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Stats command
    stats_parser = subparsers.add_parser("stats", help="Get error statistics")
    stats_parser.add_argument(
        "--function",
        type=str,
        help="Get stats for a specific function"
    )
    
    args = parser.parse_args(args)
    
    # Set up logging
    setup_logging(getattr(logging, args.log_level))
    
    if args.command == "stats":
        tracker = ErrorTracker()
        if args.function:
            count = get_error_count(tracker, args.function)
            print(f"Error count for {args.function}: {count}")
        else:
            stats = get_error_stats(tracker)
            for func_name, errors in stats.items():
                print(f"{func_name}: {len(errors)} errors")
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 