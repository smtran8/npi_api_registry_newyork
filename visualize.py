"""Visualization helpers for NPI research project

Contains functions to create bar charts from research results.
"""
from datetime import datetime
from collections import Counter

try:
    import matplotlib.pyplot as plt
except Exception:
    plt = None


def visualize_results(all_results, major_companies, out_dir='.'):
    """Save a bar chart summarizing category counts and major companies found.

    Returns the generated filename or None if matplotlib is unavailable.
    """
    if plt is None:
        print("⚠️ matplotlib not available. Install matplotlib to enable visualization.")
        return None

    category_counts = Counter([r.get('category', 'Unknown') for r in all_results])
    categories = list(category_counts.keys())
    counts = [category_counts[c] for c in categories]

    total_orgs = len(all_results)
    major_found = len(major_companies)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    fig, axs = plt.subplots(1, 2, figsize=(14, 6))

    # Left: category counts
    axs[0].bar(categories, counts, color='tab:blue')
    axs[0].set_title('Organizations by Category')
    axs[0].set_ylabel('Count')
    # Rotate x-axis labels for readability
    axs[0].tick_params(axis='x', rotation=45)

    # Right: total vs major companies
    axs[1].bar(['Total Organizations', 'Major Companies Found'], [total_orgs, major_found], color=['tab:green', 'tab:orange'])
    axs[1].set_title('Total vs Major Companies Found')
    for i, v in enumerate([total_orgs, major_found]):
        axs[1].text(i, v + max(1, int(0.02 * max(total_orgs, 1))), str(v), ha='center')

    fig.tight_layout()
    out_filename = f"{out_dir}/research_summary_{timestamp}.png"
    fig.savefig(out_filename, dpi=150)
    plt.close(fig)
    print(f"\n💾 Visualization saved to {out_filename}")
    return out_filename
