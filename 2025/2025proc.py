import sys
import io

# Force stdout to use UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

motogp_scores = [25, 20, 16, 13, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]

def parse_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    months = content.strip().split('---')
    data_per_month = []
    for month in months:
        lines = month.strip().splitlines()
        monthly_data = []
        for line in lines:
            if line.strip():
                name, score = line.rsplit(maxsplit=1)
                monthly_data.append((name.strip(), float(score)))
        data_per_month.append(monthly_data)
    return data_per_month

def compute_combined_stats(data_per_month):
    from collections import defaultdict

    total_points = defaultdict(float)
    total_scores = defaultdict(float)

    for month_data in data_per_month:
        month_data.sort(key=lambda x: x[1], reverse=True)

        for idx, (name, score) in enumerate(month_data):
            total_scores[name] += score
            if idx < len(motogp_scores):
                total_points[name] += motogp_scores[idx]
            else:
                total_points[name] += 1 / (idx + 1)

    combined = sorted(total_points.items(), key=lambda x: (-x[1], -total_scores[x[0]]))
    return combined, total_scores


def compute_monthly_ranks(data_per_month):
    """
    For each month, compute a mapping of name -> rank (1-based). If a user is not present in that month,
    they won't appear in that month's mapping.
    Returns a list of dicts, one per month, and also a sorted list of month labels.
    """
    month_rank_maps = []
    month_labels = []
    for mi, month_data in enumerate(data_per_month, 1):
        # sort by score desc, then assign ranks (dense ranking: 1,2,3...)
        sorted_month = sorted(month_data, key=lambda x: x[1], reverse=True)
        rank_map = {}
        for idx, (name, score) in enumerate(sorted_month, 1):
            rank_map[name] = idx
        month_rank_maps.append(rank_map)
        month_labels.append(f"M{mi}")
    return month_rank_maps, month_labels

def output_markdown(motogp_totals, point_totals, monthly_rank_maps, month_labels):
    # Build header with dynamic month columns
    header_cols = ["Rank", "Name", "MotoGP Score", "Total Points"] + month_labels
    # Markdown header
    header = "| " + " | ".join(header_cols) + " |"
    sep = "|" + "------|" * len(header_cols)
    lines = [header, sep]

    for i, (name, gp_score) in enumerate(motogp_totals, 1):
        row = [str(i), f"{name}", f"{gp_score:.3f}", f"{point_totals[name]:,.1f}"]
        # For each month, show rank or NA
        for rank_map in monthly_rank_maps:
            row.append(str(rank_map.get(name, 'NA')))

        # Pad/escape name to keep table readable (left align name)
        # Create formatted row string
        lines.append("| " + " | ".join(row) + " |")

    return "\n".join(lines)

def main():
    filename = "2025.txt"
    data = parse_file(filename)
    motogp_totals, point_totals = compute_combined_stats(data)

    # compute monthly ranks
    monthly_rank_maps, month_labels = compute_monthly_ranks(data)

    markdown = output_markdown(motogp_totals, point_totals, monthly_rank_maps, month_labels)

    # Save to markdown file
    with open("combined_stats.md", "w", encoding="utf-8") as f:
        f.write(markdown)

        print("Combined statistics saved to combined_stats.md as Markdown table.")

if __name__ == "__main__":
    main()
