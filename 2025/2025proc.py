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

def output_markdown(motogp_totals, point_totals):
    lines = []
    lines.append("| Rank | Name                            | MotoGP Score | Total Points     |")
    lines.append("|------|----------------------------------|---------------|------------------|")
    for i, (name, gp_score) in enumerate(motogp_totals, 1):
        lines.append(f"| {i:<4} | {name:<32} | {gp_score:13.3f} | {point_totals[name]:16,.1f} |")
    return "\n".join(lines)

def main():
    filename = "2025.txt"
    data = parse_file(filename)
    motogp_totals, point_totals = compute_combined_stats(data)

    markdown = output_markdown(motogp_totals, point_totals)

    # Save to markdown file
    with open("combined_stats.md", "w", encoding="utf-8") as f:
        f.write(markdown)

    print("✅ Combined statistics saved to `combined_stats.md` as Markdown table.")

if __name__ == "__main__":
    main()