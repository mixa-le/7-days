import csv
import re

CSV_FILE = "game_messages.csv"
OUTPUT_FILE = "long_lines.txt"
LANG_COLUMN = "esla"
MAX_LENGTH = 44

# Remove commands such as \etalk[7], \name[John], etc.
COMMAND_PATTERN = re.compile(r'\\[A-Za-z]+(?:\[[^\]]*\])?')

# Remove inline control codes that should not count
# \! \| \.
INLINE_CODES_PATTERN = re.compile(r'\\[!|.]')

with open(CSV_FILE, "r", encoding="utf-8-sig", newline="") as f, \
     open(OUTPUT_FILE, "w", encoding="utf-8") as out:

    reader = csv.DictReader(f, delimiter=";")

    found = False

    for csv_row_num, row in enumerate(reader, start=2):
        text = row.get(LANG_COLUMN, "")

        if not text:
            continue

        # Remove commands and control codes
        cleaned = COMMAND_PATTERN.sub('', text)
        cleaned = INLINE_CODES_PATTERN.sub('', cleaned)

        # Check each displayed line separately
        lines = cleaned.splitlines()

        if not lines:
            lines = [cleaned]

        for line_num, line in enumerate(lines, start=1):
            length = len(line)

            if length > MAX_LENGTH:
                found = True

                out.write(
                    f"CSV row {csv_row_num}, line {line_num}: "
                    f"{length} characters\n"
                )
                out.write(f"{line}\n")
                out.write("-" * 80 + "\n")

    if not found:
        out.write("No lines exceed 44 characters.\n")

print(f"Report saved to: {OUTPUT_FILE}")