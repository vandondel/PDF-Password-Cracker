#!/usr/bin/env python3

import itertools
import pikepdf
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
import string
import os
import sys
from pathlib import Path


def generate_passwords(chars, min_len, max_len):
    """Generate passwords with given characters and length range."""
    for length in range(min_len, max_len + 1):
        for password in itertools.product(chars, repeat=length):
            yield ''.join(password)


def load_wordlist(wordlist_file):
    """Load passwords from a wordlist file."""
    try:
        with open(wordlist_file, 'r', encoding='utf-8', errors='ignore') as file:
            for line in file:
                password = line.strip()
                if password:  # Skip empty lines
                    yield password
    except FileNotFoundError:
        print(f"[-] Wordlist file '{wordlist_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"[-] Error reading wordlist: {e}")
        sys.exit(1)


def try_password(pdf_file, password):
    """Try to open PDF with given password."""
    try:
        with pikepdf.open(pdf_file, password=password):
            return password
    except pikepdf.exceptions.PasswordError:
        return None
    except Exception:
        return None


def count_passwords(chars, min_len, max_len):
    """Calculate total number of passwords to be generated."""
    total = 0
    for length in range(min_len, max_len + 1):
        total += len(chars) ** length
    return total


def count_wordlist_lines(wordlist_file):
    """Count non-empty lines in wordlist file."""
    try:
        with open(wordlist_file, 'r', encoding='utf-8', errors='ignore') as file:
            return sum(1 for line in file if line.strip())
    except Exception:
        return 0


def crack_pdf_threaded(pdf_file, passwords, total_passwords, max_workers=4):
    """Crack PDF using multithreading with proper early termination."""
    found_password = None

    try:
        with tqdm(total=total_passwords, desc='Cracking PDF', unit='pwd') as pbar:
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                # Submit initial batch of futures
                futures = {}
                passwords_iter = iter(passwords)

                # Fill initial batch
                for _ in range(max_workers * 10):  # Buffer size
                    try:
                        pwd = next(passwords_iter)
                        future = executor.submit(try_password, pdf_file, pwd)
                        futures[future] = pwd
                    except StopIteration:
                        break

                processed = 0

                while futures and not found_password:
                    try:
                        # Process completed futures
                        for future in as_completed(futures, timeout=1):
                            result = future.result()
                            processed += 1
                            pbar.update(1)

                            if result:
                                found_password = result
                                print(f"\n[+] Password found: {result}")
                                # Cancel remaining futures
                                for f in futures:
                                    f.cancel()
                                return found_password

                            # Remove completed future and add new one
                            del futures[future]
                            try:
                                pwd = next(passwords_iter)
                                new_future = executor.submit(
                                    try_password, pdf_file, pwd)
                                futures[new_future] = pwd
                            except StopIteration:
                                pass  # No more passwords to try

                    except KeyboardInterrupt:
                        print(f"\n[!] Keyboard interrupt received. Stopping...")
                        # Cancel all remaining futures
                        for future in futures:
                            future.cancel()
                        pbar.close()
                        print(
                            f"[*] Stopped after trying {processed} passwords.")
                        return None

        print(f"[-] Password not found after trying {processed} passwords.")
        return None

    except KeyboardInterrupt:
        print(f"\n[!] Operation interrupted by user.")
        return None


def validate_inputs(args):
    """Validate command line arguments."""
    # Check if PDF file exists
    if not os.path.exists(args.pdf_file):
        print(f"[-] PDF file '{args.pdf_file}' not found.")
        return False

    # Check if it's actually a PDF
    try:
        with pikepdf.open(args.pdf_file):
            print(f"[-] PDF file '{args.pdf_file}' is not password protected.")
            return False
    except pikepdf.exceptions.PasswordError:
        pass  # Good, it's password protected
    except Exception as e:
        print(f"[-] Error opening PDF file: {e}")
        return False

    # Validate generation parameters
    if args.generate:
        if args.min_length < 1 or args.max_length < 1:
            print("[-] Password length must be at least 1.")
            return False
        if args.min_length > args.max_length:
            print("[-] Minimum length cannot be greater than maximum length.")
            return False
        if args.max_length > 8:
            print("[-] Warning: Maximum length > 8 may take very long time.")

    # Validate wordlist
    if args.wordlist and not os.path.exists(args.wordlist):
        print(f"[-] Wordlist file '{args.wordlist}' not found.")
        return False

    return True


def main():
    parser = argparse.ArgumentParser(
        description='Crack password-protected PDF files using wordlists or brute force.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python pdf_cracker.py protected.pdf -w passwords.txt
  python pdf_cracker.py protected.pdf -g -min 1 -max 4 -c "0123456789"
  python pdf_cracker.py protected.pdf -w rockyou.txt -t 8

Note: Press Ctrl+C to stop the cracking process at any time.
        """
    )

    parser.add_argument('pdf_file', help='Path to password-protected PDF file')
    parser.add_argument('-w', '--wordlist',
                        help='Path to wordlist file containing passwords')
    parser.add_argument('-g', '--generate', action='store_true',
                        help='Generate passwords using brute force')
    parser.add_argument('-min', '--min-length', type=int, default=1,
                        help='Minimum password length for generation (default: 1)')
    parser.add_argument('-max', '--max-length', type=int, default=4,
                        help='Maximum password length for generation (default: 4)')
    parser.add_argument('-c', '--charset', type=str,
                        default=string.ascii_lowercase + string.digits,
                        help='Character set for password generation (default: a-z + 0-9)')
    parser.add_argument('-t', '--max-workers', type=int, default=4,
                        help='Maximum number of worker threads (default: 4)')

    args = parser.parse_args()

    try:
        # Validate inputs
        if not validate_inputs(args):
            sys.exit(1)

        # Check if either wordlist or generate is specified
        if not args.wordlist and not args.generate:
            print("[-] Either --wordlist or --generate must be specified.")
            parser.print_help()
            sys.exit(1)

        # Setup password source and count
        if args.generate:
            print(f"[*] Generating passwords with charset: {args.charset}")
            print(f"[*] Length range: {args.min_length}-{args.max_length}")

            total_passwords = count_passwords(
                args.charset, args.min_length, args.max_length)
            print(f"[*] Total passwords to try: {total_passwords:,}")

            if total_passwords > 1000000:
                response = input(
                    "This will try over 1 million passwords. Continue? (y/N): ")
                if response.lower() != 'y':
                    sys.exit(0)

            passwords = generate_passwords(
                args.charset, args.min_length, args.max_length)

        else:  # wordlist mode
            print(f"[*] Loading wordlist: {args.wordlist}")
            total_passwords = count_wordlist_lines(args.wordlist)
            print(f"[*] Total passwords in wordlist: {total_passwords:,}")
            passwords = load_wordlist(args.wordlist)

        print(f"[*] Using {args.max_workers} worker threads")
        print(f"[*] Starting password cracking... (Press Ctrl+C to stop)")

        # Start cracking
        found_password = crack_pdf_threaded(
            args.pdf_file, passwords, total_passwords, args.max_workers)

        if found_password:
            print(f"[+] SUCCESS! Password found: '{found_password}'")
            sys.exit(0)
        else:
            print(f"[-] FAILED! Password not found.")
            sys.exit(1)

    except KeyboardInterrupt:
        print(f"\n[!] Program interrupted by user. Exiting...")
        sys.exit(130)  # Standard exit code for Ctrl+C
    except Exception as e:
        print(f"[-] Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
