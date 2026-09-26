"""
process_file.py — Part 2: one file of package descriptions, uploaded.

A Streamlit app that accepts an uploaded text file with one package description
per line, shows the total for every line, and writes the parsed packages to a
JSON file in the `data/` folder — `data/packaging1.txt` in, `data/packaging1.json`
out.

New here: an uploaded file arrives as **bytes**, not text, so it has to be
decoded before it can be split into lines. And a text file usually ends with a
newline, so the last "line" is empty and must be skipped rather than parsed.

Run it:  Run and Debug -> "Streamlit Run: Current File"   (see README Reference #1)
Test it: pytest tests/test_streamlit.py -k process_file
"""

# --- The page ---------------------------------------------------------------------
#
# Less scaffolding this time. The steps are described, but which widget and which
# function does each job — and what to call the result — is now yours to work out.
# `one_package.py` is your worked example for anything structural, and README
# Reference #4 and #5 cover the two things that are new here.

import json
import os

import streamlit as st
from packaging_parser import calc_total_units, get_unit, parse_packaging


st.title("Process File of Packages")


uploaded_file = st.file_uploader("Choose a package file:", key="package_file")

if uploaded_file:
	# 1. Decode the uploaded bytes and split the text into lines.
	text = uploaded_file.getvalue().decode("utf-8")
	lines = text.splitlines()

	packages = []

	# 2. Parse each non-empty line and show its total.
	for line in lines:
		description = line.strip()
		if not description:
			continue

		package = parse_packaging(description)
		packages.append(package)

		total = calc_total_units(package)
		unit = get_unit(package)
		st.info(f"{description} ➡️ Total 📦 Size: {total} {unit}")

	# 3. Write the parsed packages to a JSON file with the same base name.
	filename = os.path.splitext(os.path.basename(uploaded_file.name))[0] + ".json"
	output_path = os.path.join("data", filename)
	with open(output_path, "w", encoding="utf-8") as output_file:
		json.dump(packages, output_file)

	# 4. Say what happened.
	st.success(f"{len(packages)} packages written to {output_path}")
