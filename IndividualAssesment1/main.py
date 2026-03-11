
import os
import configparser
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from grobid_client.grobid_client import GrobidClient

TEI_NS = "{http://www.tei-c.org/ns/1.0}"

def process_pdfs(config_path, input_path, output_path, n_workers, force):

    client = GrobidClient(config_path=config_path)
    client.process(
        service="processFulltextDocument",
        input_path=input_path,
        output=output_path,
        n=n_workers,
        force=force,
    )

def parse_grobid_xml(input_dir):
 
    all_abstracts = ""
    figure_counts = {}
    paper_links = {}

    for xml_file in sorted(os.listdir(input_dir)):
        if not xml_file.endswith(".xml"):
            continue

        filepath = os.path.join(input_dir, xml_file)
        tree = ET.parse(filepath)
        root = tree.getroot()

        abstract = root.find(f".//{TEI_NS}abstract")
        if abstract is not None:
            all_abstracts += "".join(abstract.itertext()) + " "

        figures = root.findall(f".//{TEI_NS}figure")
        figure_counts[xml_file] = len(figures)

        links = [
            ptr.get("target")
            for ptr in root.findall(f".//{TEI_NS}ptr")
            if ptr.get("target") is not None
        ]
        paper_links[xml_file] = links

    return all_abstracts, figure_counts, paper_links

def generate_wordcloud(text, output_path):

    wordcloud = WordCloud(
        width=800, height=400, background_color="white"
    ).generate(text)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title("")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()

def plot_figure_counts(figure_counts, output_path):

    short_labels = [
        name.replace(".grobid.tei.xml", "") for name in figure_counts.keys()
    ]

    plt.figure(figsize=(10, 5))
    plt.bar(short_labels, list(figure_counts.values()), color="#4C72B0")
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Number of Figures")
    plt.xlabel("Article")
    plt.title("Figures per Article")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    
def save_links(paper_links, output_path):

    with open(output_path, "w", encoding="utf-8") as f:
        for paper, links in paper_links.items():
            short_name = paper.replace(".grobid.tei.xml", "")
            f.write(f"{short_name} ({len(links)} links):\n")
            for link in links:
                f.write(f"  - {link}\n")
            f.write("\n")

def main():
    config = configparser.ConfigParser()
    config.read("setup.cfg")

    input_path = config["paths"]["input"]
    grobid_output = config["paths"]["grobid_output"]
    results = config["paths"]["results"]
    grobid_config = config["grobid"]["config"]
    workers = config.getint("grobid", "workers")
    force = config.getboolean("grobid", "force")


    process_pdfs(grobid_config, input_path, grobid_output, workers, force)
    all_abstracts, figure_counts, paper_links = parse_grobid_xml(grobid_output)
    generate_wordcloud(all_abstracts, os.path.join(results, "wordcloud.png"))
    plot_figure_counts(figure_counts, os.path.join(results, "figures_per_article.png"))
    save_links(paper_links, os.path.join(results, "links_per_paper.txt"))

if __name__ == "__main__":
    main()
