
import os
import tempfile
import shutil
import pytest
import xml.etree.ElementTree as ET

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from main import parse_grobid_xml, generate_wordcloud, plot_figure_counts, save_links

TEI_NS = "{http://www.tei-c.org/ns/1.0}"


SAMPLE_XML_WITH_DATA = """\
<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
  <teiHeader>
    <profileDesc>
      <abstract>
        <p>Machine learning is transforming software engineering practices.</p>
      </abstract>
    </profileDesc>
  </teiHeader>
  <text>
    <body>
      <figure xml:id="fig_0"><head>Figure 1</head></figure>
      <figure xml:id="fig_1"><head>Figure 2</head></figure>
      <figure xml:id="fig_2"><head>Figure 3</head></figure>
      <ptr target="https://example.com/paper1" />
      <ptr target="https://example.com/paper2" />
    </body>
  </text>
</TEI>
"""

SAMPLE_XML_NO_ABSTRACT = """\
<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
  <teiHeader>
    <profileDesc/>
  </teiHeader>
  <text>
    <body>
      <figure xml:id="fig_0"><head>Figure 1</head></figure>
    </body>
  </text>
</TEI>
"""

SAMPLE_XML_EMPTY = """\
<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
  <teiHeader><profileDesc/></teiHeader>
  <text><body/></text>
</TEI>
"""


@pytest.fixture
def xml_dir_with_data(tmp_path):
    """Create a temp directory with a sample XML file containing data."""
    xml_file = tmp_path / "sample.grobid.tei.xml"
    xml_file.write_text(SAMPLE_XML_WITH_DATA, encoding="utf-8")
    return tmp_path


@pytest.fixture
def xml_dir_no_abstract(tmp_path):
    """Create a temp directory with an XML file missing the abstract."""
    xml_file = tmp_path / "no_abstract.grobid.tei.xml"
    xml_file.write_text(SAMPLE_XML_NO_ABSTRACT, encoding="utf-8")
    return tmp_path


@pytest.fixture
def xml_dir_empty(tmp_path):
    """Create a temp directory with an XML file with no figures/links."""
    xml_file = tmp_path / "empty.grobid.tei.xml"
    xml_file.write_text(SAMPLE_XML_EMPTY, encoding="utf-8")
    return tmp_path


@pytest.fixture
def xml_dir_multiple(tmp_path):
    """Create a temp directory with multiple XML files."""
    (tmp_path / "paper_a.grobid.tei.xml").write_text(SAMPLE_XML_WITH_DATA, encoding="utf-8")
    (tmp_path / "paper_b.grobid.tei.xml").write_text(SAMPLE_XML_NO_ABSTRACT, encoding="utf-8")
    (tmp_path / "paper_c.grobid.tei.xml").write_text(SAMPLE_XML_EMPTY, encoding="utf-8")
    return tmp_path


@pytest.fixture
def output_dir(tmp_path):
    """Create a temp directory for outputs."""
    out = tmp_path / "output"
    out.mkdir()
    return out


# ─── Tests: Grobid XML Parser ─────────────────────────────────────────────────

class TestParseGrobidXml:
    def test_extracts_abstract_text(self, xml_dir_with_data):
        abstracts, _, _ = parse_grobid_xml(str(xml_dir_with_data))
        assert "Machine learning" in abstracts
        assert "software engineering" in abstracts

    def test_counts_figures_correctly(self, xml_dir_with_data):
        _, figure_counts, _ = parse_grobid_xml(str(xml_dir_with_data))
        assert figure_counts["sample.grobid.tei.xml"] == 3

    def test_extracts_links(self, xml_dir_with_data):
        _, _, paper_links = parse_grobid_xml(str(xml_dir_with_data))
        links = paper_links["sample.grobid.tei.xml"]
        assert len(links) == 2
        assert "https://example.com/paper1" in links
        assert "https://example.com/paper2" in links

    def test_missing_abstract_returns_empty(self, xml_dir_no_abstract):
        abstracts, _, _ = parse_grobid_xml(str(xml_dir_no_abstract))
        assert abstracts.strip() == ""

    def test_no_figures_returns_zero(self, xml_dir_empty):
        _, figure_counts, _ = parse_grobid_xml(str(xml_dir_empty))
        assert figure_counts["empty.grobid.tei.xml"] == 0

    def test_no_links_returns_empty_list(self, xml_dir_empty):
        _, _, paper_links = parse_grobid_xml(str(xml_dir_empty))
        assert paper_links["empty.grobid.tei.xml"] == []

    def test_multiple_files_parsed(self, xml_dir_multiple):
        abstracts, figure_counts, paper_links = parse_grobid_xml(str(xml_dir_multiple))
        assert len(figure_counts) == 3
        assert len(paper_links) == 3

    def test_ignores_non_xml_files(self, xml_dir_with_data):
        (xml_dir_with_data / "notes.txt").write_text("not xml", encoding="utf-8")
        _, figure_counts, _ = parse_grobid_xml(str(xml_dir_with_data))
        assert "notes.txt" not in figure_counts

    def test_empty_directory(self, tmp_path):
        abstracts, figure_counts, paper_links = parse_grobid_xml(str(tmp_path))
        assert abstracts == ""
        assert figure_counts == {}
        assert paper_links == {}


# ─── Tests: Wordcloud ───────────────────────────────────────────────

class TestGenerateWordcloud:

    def test_creates_png_file(self, output_dir):
        output_path = str(output_dir / "wordcloud.png")
        generate_wordcloud("machine learning deep neural networks", output_path)
        assert os.path.exists(output_path)

    def test_output_file_is_not_empty(self, output_dir):
        output_path = str(output_dir / "wordcloud.png")
        generate_wordcloud("machine learning deep neural networks", output_path)
        assert os.path.getsize(output_path) > 0


# ─── Tests: Chart Figure Counter ───────────────────────────────────────────────

class TestPlotFigureCounts:

    def test_creates_png_file(self, output_dir):
        counts = {"paper_a.grobid.tei.xml": 5, "paper_b.grobid.tei.xml": 3}
        output_path = str(output_dir / "figures.png")
        plot_figure_counts(counts, output_path)
        assert os.path.exists(output_path)

    def test_output_file_is_not_empty(self, output_dir):
        counts = {"paper_a.grobid.tei.xml": 5}
        output_path = str(output_dir / "figures.png")
        plot_figure_counts(counts, output_path)
        assert os.path.getsize(output_path) > 0


# ─── Tests: links ──────────────────────────────────────────────────────

class TestSaveLinks:

    def test_creates_output_file(self, output_dir):
        links = {"paper.grobid.tei.xml": ["https://example.com"]}
        output_path = str(output_dir / "links.txt")
        save_links(links, output_path)
        assert os.path.exists(output_path)

    def test_writes_correct_content(self, output_dir):
        links = {
            "paper_a.grobid.tei.xml": ["https://a.com", "https://b.com"],
            "paper_b.grobid.tei.xml": [],
        }
        output_path = str(output_dir / "links.txt")
        save_links(links, output_path)

        with open(output_path, "r", encoding="utf-8") as f:
            content = f.read()

        assert "paper_a (2 links):" in content
        assert "  - https://a.com" in content
        assert "  - https://b.com" in content
        assert "paper_b (0 links):" in content

    def test_strips_xml_extension_from_name(self, output_dir):
        links = {"test.grobid.tei.xml": ["https://example.com"]}
        output_path = str(output_dir / "links.txt")
        save_links(links, output_path)

        with open(output_path, "r", encoding="utf-8") as f:
            content = f.read()

        assert "test (1 links):" in content
        assert ".grobid.tei.xml" not in content

    def test_empty_links_dict(self, output_dir):
        output_path = str(output_dir / "links.txt")
        save_links({}, output_path)
        with open(output_path, "r", encoding="utf-8") as f:
            content = f.read()
        assert content == ""
