"""
process_files.py — Part 3: many files, one after another, with a running total.

The same job as process_file.py, but the app now remembers what it has already
done: how many files have been processed, how many packages that came to, and a
one-line summary of each file — and it keeps remembering across uploads.

That is the hard part, and it is hard for a specific reason: every interaction
reruns this whole script from the top, so an ordinary variable like
`files_processed = 0` is reset to zero on every rerun. Anything that has to
survive a rerun lives in `st.session_state` instead, and is initialised only
once — the first time the script runs.

The other trap is the uploader itself. Once a file has been chosen it stays
chosen on every rerun, so an app that processes "whenever there is a file" would
count the same file again on every interaction. Processing happens on a button
click instead: `st.button` is True only on the one rerun the click caused.

Run it:  Run and Debug -> "Streamlit Run: Current File"   (see README Reference #1)
Test it: pytest tests/test_streamlit.py -k process_files
"""

import json
import os

import streamlit as st
from packaging_parser import parse_packaging


st.title("Process Package Files")

uploaded_file = st.file_uploader("Choose a package file:", key="package_file")
process_clicked = st.button("Process file", key="process")

if "files_processed" not in st.session_state:
	st.session_state.files_processed = 0
	st.session_state.packages_processed = 0
	st.session_state.file_summaries = []

if uploaded_file is not None and process_clicked:
	text = uploaded_file.getvalue().decode("utf-8")
	packages = []

	for line in text.splitlines():
		description = line.strip()
		if description:
			packages.append(parse_packaging(description))

	filename = os.path.splitext(os.path.basename(uploaded_file.name))[0] + ".json"
	output_path = os.path.join("data", filename)
	with open(output_path, "w", encoding="utf-8") as output_file:
		json.dump(packages, output_file)

	summary = f"{len(packages)} packages written to {output_path}"
	st.session_state.files_processed += 1
	st.session_state.packages_processed += len(packages)
	st.session_state.file_summaries.append(summary)

columns = st.columns(2)
columns[0].metric("Files processed", st.session_state.files_processed)
columns[1].metric("Packages processed", st.session_state.packages_processed)

for summary in st.session_state.file_summaries:
	st.info(summary)
