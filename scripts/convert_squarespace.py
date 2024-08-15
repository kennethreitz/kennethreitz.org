import os
import re
import xml.etree.ElementTree as ET
from datetime import datetime
import markdownify
import pathlib
import unicodedata


def slugify(value, allow_unicode=False):
    """
    Convert a string to a valid filename, ensuring no unintended directories are created.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "_", value).strip("-_")


def extract_text_from_cdata(cdata):
    """
    Extracts text content from CDATA and cleans it up for markdown.
    """
    html_content = re.sub(r"\s+", " ", cdata)
    return markdownify.markdownify(html_content, heading_style="ATX")


def save_post_as_markdown(title, content, pub_date, destination_dir):
    """
    Saves the blog post as a markdown file organized by year with the original publication date as the file's creation time.
    """
    # Determine the year and create a directory for it
    year = pub_date.year
    year_dir = destination_dir / str(year)
    year_dir.mkdir(parents=True, exist_ok=True)

    # Generate a safe filename
    filename = f"{slugify(title)}.md"
    file_path = year_dir / filename

    # Write the content to the file
    with open(file_path, "w") as file:
        file.write(f"# {title}\n\n")
        file.write(content)

    # Set the file's creation and modification time to the original publication date
    pub_timestamp = pub_date.timestamp()
    os.utime(file_path, (pub_timestamp, pub_timestamp))


def parse_xml_and_save_posts(xml_file, destination_dir):
    """
    Parses the provided XML file, extracts blog posts, and saves them to the destination directory organized by year.
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()

    destination_dir = pathlib.Path(destination_dir)
    destination_dir.mkdir(parents=True, exist_ok=True)

    # Define namespaces to handle XML namespaces in the file
    namespaces = {
        "content": "http://purl.org/rss/1.0/modules/content/",
        "wp": "http://wordpress.org/export/1.2/",
    }

    for item in root.findall(".//item"):
        title = item.find("title").text
        pub_date_str = item.find("pubDate").text
        pub_date = datetime.strptime(pub_date_str, "%a, %d %b %Y %H:%M:%S %z")
        content = item.find("content:encoded", namespaces).text

        # Convert HTML content to Markdown
        markdown_content = extract_text_from_cdata(content)

        # Save the post as a markdown file organized by year
        save_post_as_markdown(title, markdown_content, pub_date, destination_dir)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Convert XML blog export to Markdown files organized by year."
    )
    parser.add_argument("xml_file", help="Path to the XML file to be processed.")
    parser.add_argument("destination_dir", help="Directory to save the Markdown files.")

    args = parser.parse_args()

    parse_xml_and_save_posts(args.xml_file, args.destination_dir)
