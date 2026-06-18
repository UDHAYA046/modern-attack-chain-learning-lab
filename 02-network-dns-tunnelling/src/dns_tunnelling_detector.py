import json
import math
from collections import Counter
from pathlib import Path

#shanon enthorpy
def calculate_entropy(text):
    probabilities = [n / len(text) for n in Counter(text).values()]
    return -sum(p * math.log2(p) for p in probabilities)

#query length
def query_length(domain):
    return len(domain)

#subdomain depth
def subdomain_depth(domain):
    return max(0, len(domain.split(".")) - 2)

#risk level
def risk_level(score):

    if score <= 4:
        return "Low"

    elif score <= 8:
        return "Medium"

    elif score <= 12:
        return "High"

    else:
        return "Critical"